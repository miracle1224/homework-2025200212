#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lab2-general：读取 components.csv + mission_profile.csv + model.json
- 由 mission_profile 计算每个元件 duty
- 由 network_model 精确计算一般网络任务可靠度
- 由 repairable_model 计算可修系统稳态可用度
- 生成 output/lab2_general_report_<student_id>_<name>.md

用法：
python src/calc.py --student_id 2026XXXXXX --student_name zhangsan --N 60
"""

import argparse
import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
COMP_PATH = DATA_DIR / "components.csv"
PROFILE_PATH = DATA_DIR / "mission_profile.csv"
MODEL_PATH = DATA_DIR / "model.json"

EXPERIMENT_NAME = "实验2：一般网络与可修系统可靠性分析（lab2-general）"


def r_exp(lmbda: float, t: float) -> float:
    return math.exp(-lmbda * t)


def steady_availability(lmbda: float, mu: float) -> float:
    if lmbda < 0 or mu <= 0:
        raise ValueError(f"可用度参数非法：lambda={lmbda}, mu={mu}")
    return mu / (lmbda + mu)


def load_components() -> Dict[str, Dict[str, Any]]:
    comps: Dict[str, Dict[str, Any]] = {}
    with COMP_PATH.open("r", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        required = ["id", "name", "lambda_per_h", "mu_per_h"]
        missing_cols = [c for c in required if c not in (rd.fieldnames or [])]
        if missing_cols:
            raise ValueError(f"components.csv 缺少列：{missing_cols}")
        for row in rd:
            cid = row["id"].strip()
            if cid in comps:
                raise ValueError(f"components.csv 中存在重复元件编号：{cid}")
            comps[cid] = {
                "name": row["name"].strip(),
                "lambda_per_h": float(row["lambda_per_h"]),
                "mu_per_h": float(row["mu_per_h"]),
            }
    return comps


def load_profile(component_ids: List[str]) -> Tuple[float, Dict[str, float], List[Dict[str, Any]]]:
    rows: List[Dict[str, Any]] = []
    work_time = {cid: 0.0 for cid in component_ids}
    t_cyc = 0.0

    with PROFILE_PATH.open("r", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        required = ["phase", "duration_h"] + component_ids
        missing = [c for c in required if c not in (rd.fieldnames or [])]
        if missing:
            raise ValueError(f"mission_profile.csv 缺少列：{missing}")
        for row in rd:
            phase = row["phase"].strip()
            dur = float(row["duration_h"])
            if dur <= 0:
                raise ValueError(f"阶段 {phase} 的 duration_h 必须>0")
            t_cyc += dur
            phase_row = {"phase": phase, "duration_h": dur}
            for cid in component_ids:
                flag = int(float(row[cid]))
                if flag not in (0, 1):
                    raise ValueError(f"{phase} 阶段 {cid} 标记必须为0/1")
                phase_row[cid] = flag
                if flag == 1:
                    work_time[cid] += dur
            rows.append(phase_row)

    if t_cyc <= 0:
        raise ValueError("t_cyc 计算得到 <=0，请检查 mission_profile.csv")

    duty = {cid: work_time[cid] / t_cyc for cid in component_ids}
    return t_cyc, duty, rows


def load_model_data() -> Dict[str, Any]:
    data = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    if "network_model" not in data:
        raise ValueError("data/model.json 缺少 network_model，无法进行 lab2-general 计算。")
    if "repairable_model" not in data:
        raise ValueError("data/model.json 缺少 repairable_model，无法进行可修系统分析。")
    return data


def validate_network_model(network_model: Dict[str, Any], component_ids: List[str]) -> List[Dict[str, Any]]:
    required = ["source", "target", "nodes", "edges"]
    missing = [k for k in required if k not in network_model]
    if missing:
        raise ValueError(f"network_model 缺少字段：{missing}")

    nodes = network_model["nodes"]
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("network_model.nodes 必须为非空列表")
    node_set = set(nodes)

    source = network_model["source"]
    target = network_model["target"]
    if source not in node_set or target not in node_set:
        raise ValueError("network_model 的 source/target 必须包含在 nodes 中")

    edges = network_model["edges"]
    if not isinstance(edges, list) or not edges:
        raise ValueError("network_model.edges 必须为非空列表")

    seen_edge_ids = set()
    used_components = []
    for edge in edges:
        for field in ["id", "from", "to", "component"]:
            if field not in edge:
                raise ValueError(f"网络边缺少字段：{field}")
        if edge["id"] in seen_edge_ids:
            raise ValueError(f"存在重复边编号：{edge['id']}")
        seen_edge_ids.add(edge["id"])
        if edge["from"] not in node_set or edge["to"] not in node_set:
            raise ValueError(f"边 {edge['id']} 的端点未在 nodes 中定义")
        used_components.append(edge["component"])

    unknown = sorted(set(used_components) - set(component_ids), key=lambda x: int(x[1:]) if x.startswith("C") else x)
    if unknown:
        raise ValueError(f"network_model 引用了未知元件：{unknown}")

    missing_components = [cid for cid in component_ids if cid not in used_components]
    if missing_components:
        raise ValueError(f"network_model 未包含全部元件，缺少：{missing_components}")

    duplicates = sorted({cid for cid in used_components if used_components.count(cid) > 1}, key=lambda x: int(x[1:]))
    if duplicates:
        raise ValueError(
            "当前模板要求一个元件只映射到一条网络边，以避免重复计入同一元件的独立性。"
            f"重复元件：{duplicates}"
        )

    return edges


def build_out_edges(edges: List[Dict[str, Any]]) -> Dict[str, List[Tuple[int, str]]]:
    out_edges: Dict[str, List[Tuple[int, str]]] = {}
    for idx, edge in enumerate(edges):
        out_edges.setdefault(edge["from"], []).append((idx, edge["to"]))
    return out_edges


def has_path(mask: int, out_edges: Dict[str, List[Tuple[int, str]]], source: str, target: str) -> bool:
    if source == target:
        return True
    stack = [source]
    visited = {source}
    while stack:
        node = stack.pop()
        for edge_idx, nxt in out_edges.get(node, []):
            if not (mask & (1 << edge_idx)) or nxt in visited:
                continue
            if nxt == target:
                return True
            visited.add(nxt)
            stack.append(nxt)
    return False


def exact_connectivity_probability(
    edges: List[Dict[str, Any]],
    edge_probs: List[float],
    source: str,
    target: str,
) -> float:
    if len(edges) != len(edge_probs):
        raise ValueError("边数量与概率数量不一致")
    for prob in edge_probs:
        if prob < 0.0 or prob > 1.0:
            raise ValueError(f"边概率超出 [0,1]：{prob}")

    out_edges = build_out_edges(edges)
    total = 0.0
    edge_count = len(edges)
    full_mask = 1 << edge_count

    for mask in range(full_mask):
        p_state = 1.0
        for idx, prob in enumerate(edge_probs):
            p_state *= prob if (mask & (1 << idx)) else (1.0 - prob)
            if p_state == 0.0:
                break
        if p_state == 0.0:
            continue
        if has_path(mask, out_edges, source, target):
            total += p_state

    return min(max(total, 0.0), 1.0)


def compute_network_metric(network_model: Dict[str, Any], metric_map: Dict[str, float]) -> float:
    edges = network_model["edges"]
    edge_probs = [metric_map[edge["component"]] for edge in edges]
    return exact_connectivity_probability(
        edges=edges,
        edge_probs=edge_probs,
        source=network_model["source"],
        target=network_model["target"],
    )


def strip_redundant_edges(network_model: Dict[str, Any]) -> Dict[str, Any]:
    kept_edges: List[Dict[str, Any]] = []
    seen_pairs = set()
    for edge in network_model["edges"]:
        pair = (edge["from"], edge["to"])
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        kept_edges.append(edge)
    stripped = dict(network_model)
    stripped["edges"] = kept_edges
    return stripped


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--student_id", required=True)
    ap.add_argument("--student_name", required=True)
    ap.add_argument("--N", type=int, default=60, help="班次循环次数")
    args = ap.parse_args()
    if args.N <= 0:
        raise ValueError("N 必须>0")

    safe_name = re.sub(r"[^\w\u4e00-\u9fa5]", "", str(args.student_name))
    out_path = REPO_ROOT / "output" / f"lab2_general_report_{args.student_id}_{safe_name}.md"

    comps = load_components()
    component_ids = sorted(comps.keys(), key=lambda x: int(x[1:]))
    t_cyc, duty, profile_rows = load_profile(component_ids)
    T = args.N * t_cyc

    model_data = load_model_data()
    network_model = model_data["network_model"]
    validate_network_model(network_model, component_ids)
    repairable_model = model_data["repairable_model"]
    use_effective_lambda = bool(repairable_model.get("use_effective_lambda", True))

    lam_eff: Dict[str, float] = {}
    lambda_for_availability: Dict[str, float] = {}
    reliability_map: Dict[str, float] = {}
    availability_map: Dict[str, float] = {}

    for cid in component_ids:
        lam = comps[cid]["lambda_per_h"]
        mu = comps[cid]["mu_per_h"]
        lam_eff[cid] = lam * duty[cid]
        lambda_for_availability[cid] = lam_eff[cid] if use_effective_lambda else lam
        reliability_map[cid] = r_exp(lam_eff[cid], T)
        availability_map[cid] = steady_availability(lambda_for_availability[cid], mu)

    r_sys = compute_network_metric(network_model, reliability_map)
    a_sys = compute_network_metric(network_model, availability_map)

    stripped_network = strip_redundant_edges(network_model)
    r_sys_stripped = compute_network_metric(stripped_network, reliability_map)
    a_sys_stripped = compute_network_metric(stripped_network, availability_map)

    reliability_map_half_t = {cid: r_exp(lam_eff[cid], T / 2.0) for cid in component_ids}
    r_sys_half_t = compute_network_metric(network_model, reliability_map_half_t)

    availability_map_half_mu = {
        cid: steady_availability(lambda_for_availability[cid], comps[cid]["mu_per_h"] / 2.0)
        for cid in component_ids
    }
    a_sys_half_mu = compute_network_metric(network_model, availability_map_half_mu)

    check_r_redundancy = r_sys_stripped <= r_sys + 1e-12
    check_r_time = r_sys_half_t >= r_sys - 1e-12
    check_a_redundancy = a_sys_stripped <= a_sys + 1e-12
    check_a_repair = a_sys_half_mu <= a_sys + 1e-12
    if not all([check_r_redundancy, check_r_time, check_a_redundancy, check_a_repair]):
        raise RuntimeError(
            "Sanity check 未通过：\n"
            f"- 去冗余应变差（可靠度）：{check_r_redundancy}\n"
            f"- 缩短任务时间应变好（可靠度）：{check_r_time}\n"
            f"- 去冗余应变差（可用度）：{check_a_redundancy}\n"
            f"- 降低维修率应变差（可用度）：{check_a_repair}"
        )

    weak_r_id = min(component_ids, key=lambda cid: reliability_map[cid])
    weak_a_id = min(component_ids, key=lambda cid: availability_map[cid])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append(f"# {EXPERIMENT_NAME}")
    lines.append(f"{args.student_id}，{args.student_name}")
    lines.append("")

    lines.append("## 1. 任务与剖面参数")
    lines.append(f"- 单循环时长：t_cyc = {t_cyc:.3f} h")
    lines.append(f"- 循环次数：N = {args.N}")
    lines.append(f"- 班次任务时间：T = N * t_cyc = {T:.3f} h")
    lines.append(f"- 可修系统口径：use_effective_lambda = {use_effective_lambda}")
    lines.append("")

    lines.append("## 2. 一般网络模型摘要")
    lines.append(f"- source = {network_model['source']}")
    lines.append(f"- target = {network_model['target']}")
    lines.append(f"- 节点数 = {len(network_model['nodes'])}")
    lines.append(f"- 边数 = {len(network_model['edges'])}")
    lines.append("```json")
    lines.append(json.dumps(network_model, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")

    lines.append("## 3. 任务剖面（阶段时长）")
    lines.append("| 阶段 | duration_h |")
    lines.append("|---|---:|")
    for row in profile_rows:
        lines.append(f"| {row['phase']} | {row['duration_h']:.3f} |")
    lines.append("")

    lines.append("## 4. 单元件参数、可靠度与可用度")
    lines.append("| 编号 | 元件 | λ(1/h) | μ(1/h) | duty | λ_eff(1/h) | R(T) | A_ss |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for cid in component_ids:
        comp = comps[cid]
        lines.append(
            f"| {cid} | {comp['name']} | {comp['lambda_per_h']:.2e} | {comp['mu_per_h']:.2f} | "
            f"{duty[cid]:.3f} | {lam_eff[cid]:.2e} | {reliability_map[cid]:.6f} | {availability_map[cid]:.6f} |"
        )
    lines.append("")

    lines.append("## 5. 系统层结果")
    lines.append(f"- 一般网络任务可靠度：R_sys(T) = {r_sys:.6f}")
    lines.append(f"- 可修系统稳态可用度：A_sys = {a_sys:.6f}")
    lines.append("")

    lines.append("## 6. 薄弱环节")
    lines.append(
        f"- 最低单元可靠度：{weak_r_id} {comps[weak_r_id]['name']}，"
        f"R(T) = {reliability_map[weak_r_id]:.6f}，λ_eff = {lam_eff[weak_r_id]:.2e} 1/h"
    )
    lines.append(
        f"- 最低单元可用度：{weak_a_id} {comps[weak_a_id]['name']}，"
        f"A_ss = {availability_map[weak_a_id]:.6f}，μ = {comps[weak_a_id]['mu_per_h']:.2f} 1/h"
    )
    lines.append("")

    lines.append("## 7. Sanity checks")
    lines.append(f"- 去冗余应变差（可靠度）：PASS（R_noRed={r_sys_stripped:.6f} <= R={r_sys:.6f}）")
    lines.append(f"- 缩短任务时间应变好（可靠度）：PASS（R_halfT={r_sys_half_t:.6f} >= R={r_sys:.6f}）")
    lines.append(f"- 去冗余应变差（可用度）：PASS（A_noRed={a_sys_stripped:.6f} <= A={a_sys:.6f}）")
    lines.append(f"- 降低维修率应变差（可用度）：PASS（A_halfMu={a_sys_half_mu:.6f} <= A={a_sys:.6f}）")
    lines.append("")

    lines.append(f"> 报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    custom_block_title = "## 8. 学生自定义补充区（请在此区块内补充任务1/4内容，不会被自动覆盖）"
    custom_block = (
        f"{custom_block_title}\n\n"
        "### 任务1：一般网络建模与公式\n"
        "（请在此处补充你的建模思路、公式推导等）\n\n"
        "### 任务4：结果解释与工程分析（必做）\n"
        "（请在此处补充你的可靠度/可用度结果解释、薄弱环节分析、改进建议等）\n"
    )
    if out_path.exists():
        old = out_path.read_text(encoding="utf-8")
        if custom_block_title in old:
            custom_block = old.split(custom_block_title, 1)[1].lstrip("\n")
            custom_block = f"{custom_block_title}\n" + custom_block

    lines.append(custom_block)
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"已生成：{out_path}")
    print(f"R_sys(T={T:.3f}h) = {r_sys:.6f}")
    print(f"A_sys = {a_sys:.6f}")


if __name__ == "__main__":
    main()
