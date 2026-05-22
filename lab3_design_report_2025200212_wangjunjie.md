# 实验3：可靠性模型设计（lab3-design）- 阿林斯法
2025200212，wangjunjie

## 1. 任务与剖面参数
- 单循环时长：t_cyc = 0.225 h
- 循环次数：N = 60
- 班次任务时间：T = N * t_cyc = 13.500 h
- 可修系统口径：use_effective_lambda = True

## 2. 阿林斯法（Alims Method）原理
### 方法概述
阿林斯法通过计算最小路集和最小割集来近似求解复杂系统可靠度：

**最小路集（Minimal Path Sets）**：从源点到汇点的最小边集合，所有边正常工作则系统成功
**最小割集（Minimal Cut Sets）**：导致系统失效的最小边集合，所有边失效则系统失效

### 核心公式
```
上限（Upper Bound）：
R_upper = ΣP(path_i) - ΣP(path_i ∩ path_j) + ΣP(path_i ∩ path_j ∩ path_k) - ...

下限（Lower Bound）：
R_lower = 1 - ΣP(cut_i) + ΣP(cut_i ∩ cut_j) - ΣP(cut_i ∩ cut_j ∩ cut_k) + ...

估计值（Estimation）：
R_est = (R_upper + R_lower) / 2
```

## 3. 一般网络模型摘要
- source = START
- target = TASK_DONE
- 节点数 = 14
- 边数 = 19
```json
{
  "type": "general_network",
  "source": "START",
  "target": "TASK_DONE",
  "success_criterion": "source_to_target_connectivity",
  "nodes": [
    "START",
    "PWR_IN",
    "EMI_OK",
    "DC_BUS",
    "CTRL_CORE",
    "SAFETY_OK",
    "ACT_GATE",
    "HOIST_PATH",
    "TROLLEY_PATH",
    "BRIDGE_LINK",
    "MOTION_OK",
    "LIMIT_OK",
    "POSITION_OK",
    "TASK_DONE"
  ],
  "edges": [
    {
      "id": "E1",
      "from": "START",
      "to": "PWR_IN",
      "component": "C1",
      "role": "main_power_in"
    },
    {
      "id": "E2",
      "from": "PWR_IN",
      "to": "EMI_OK",
      "component": "C2",
      "role": "emi_filter"
    },
    {
      "id": "E3",
      "from": "EMI_OK",
      "to": "DC_BUS",
      "component": "C3",
      "role": "rectifier_a"
    },
    {
      "id": "E4",
      "from": "EMI_OK",
      "to": "DC_BUS",
      "component": "C4",
      "role": "rectifier_b"
    },
    {
      "id": "E5",
      "from": "DC_BUS",
      "to": "CTRL_CORE",
      "component": "C5",
      "role": "dc_bus_capacitor"
    },
    {
      "id": "E6",
      "from": "CTRL_CORE",
      "to": "SAFETY_OK",
      "component": "C6",
      "role": "plc_control"
    },
    {
      "id": "E7",
      "from": "SAFETY_OK",
      "to": "ACT_GATE",
      "component": "C7",
      "role": "safety_relay"
    },
    {
      "id": "E8",
      "from": "ACT_GATE",
      "to": "HOIST_PATH",
      "component": "C8",
      "role": "hoist_drive"
    },
    {
      "id": "E9",
      "from": "HOIST_PATH",
      "to": "MOTION_OK",
      "component": "C9",
      "role": "hoist_motor"
    },
    {
      "id": "E10",
      "from": "HOIST_PATH",
      "to": "BRIDGE_LINK",
      "component": "C10",
      "role": "hoist_brake"
    },
    {
      "id": "E11",
      "from": "BRIDGE_LINK",
      "to": "MOTION_OK",
      "component": "C11",
      "role": "rope_drum_path"
    },
    {
      "id": "E12",
      "from": "ACT_GATE",
      "to": "TROLLEY_PATH",
      "component": "C12",
      "role": "trolley_drive"
    },
    {
      "id": "E13",
      "from": "TROLLEY_PATH",
      "to": "MOTION_OK",
      "component": "C13",
      "role": "trolley_motor"
    },
    {
      "id": "E14",
      "from": "TROLLEY_PATH",
      "to": "BRIDGE_LINK",
      "component": "C14",
      "role": "wheel_rail_bridge"
    },
    {
      "id": "E15",
      "from": "MOTION_OK",
      "to": "LIMIT_OK",
      "component": "C15",
      "role": "upper_limit_a"
    },
    {
      "id": "E16",
      "from": "MOTION_OK",
      "to": "LIMIT_OK",
      "component": "C16",
      "role": "upper_limit_b"
    },
    {
      "id": "E17",
      "from": "LIMIT_OK",
      "to": "POSITION_OK",
      "component": "C17",
      "role": "encoder_a"
    },
    {
      "id": "E18",
      "from": "LIMIT_OK",
      "to": "POSITION_OK",
      "component": "C18",
      "role": "encoder_b"
    },
    {
      "id": "E19",
      "from": "POSITION_OK",
      "to": "TASK_DONE",
      "component": "C19",
      "role": "gripper_actuation"
    }
  ]
}
```

## 4. 任务剖面（阶段时长）
| 阶段 | duration_h |
|---|---:|
| Pick | 0.010 |
| Lift | 0.020 |
| TravelLoaded | 0.100 |
| Place | 0.015 |
| ReturnEmpty | 0.080 |

## 5. 单元件参数、可靠度与可用度
| 编号 | 元件 | λ(1/h) | μ(1/h) | duty | λ_eff(1/h) | R(T) | A_ss |
|---|---|---:|---:|---:|---:|---:|---:|
| C1 | 断路器 | 2.00e-05 | 0.50 | 1.000 | 2.00e-05 | 0.999730 | 0.999960 |
| C2 | EMI滤波器 | 1.00e-05 | 0.67 | 1.000 | 1.00e-05 | 0.999865 | 0.999985 |
| C3 | 整流模块A | 8.00e-05 | 0.33 | 1.000 | 8.00e-05 | 0.998921 | 0.999758 |
| C4 | 整流模块B | 8.00e-05 | 0.33 | 0.200 | 1.60e-05 | 0.999784 | 0.999952 |
| C5 | DC母线电容 | 3.00e-05 | 0.25 | 0.200 | 6.00e-06 | 0.999919 | 0.999976 |
| C6 | PLC控制器 | 5.00e-05 | 0.50 | 0.800 | 4.00e-05 | 0.999460 | 0.999920 |
| C7 | 安全继电器 | 4.00e-05 | 0.50 | 0.800 | 3.20e-05 | 0.999568 | 0.999936 |
| C8 | 起升变频器 | 1.20e-04 | 0.25 | 0.200 | 2.40e-05 | 0.999676 | 0.999904 |
| C9 | 起升电机 | 6.00e-05 | 0.20 | 0.200 | 1.20e-05 | 0.999838 | 0.999940 |
| C10 | 起升制动器 | 4.00e-05 | 0.33 | 0.200 | 8.00e-06 | 0.999892 | 0.999976 |
| C11 | 钢丝绳/卷筒 | 3.50e-05 | 0.17 | 0.444 | 1.56e-05 | 0.999790 | 0.999909 |
| C12 | 小车变频器 | 1.00e-04 | 0.25 | 1.000 | 1.00e-04 | 0.998651 | 0.999600 |
| C13 | 小车电机 | 5.00e-05 | 0.20 | 1.000 | 5.00e-05 | 0.999325 | 0.999750 |
| C14 | 车轮/轨道啮合子系统 | 2.50e-05 | 0.14 | 1.000 | 2.50e-05 | 0.999663 | 0.999821 |
| C15 | 起升上限位A | 7.00e-05 | 1.00 | 1.000 | 7.00e-05 | 0.999055 | 0.999930 |
| C16 | 起升上限位B | 7.00e-05 | 1.00 | 1.000 | 7.00e-05 | 0.999055 | 0.999930 |
| C17 | 小车编码器A | 6.00e-05 | 1.00 | 1.000 | 6.00e-05 | 0.999190 | 0.999940 |
| C18 | 小车编码器B | 6.00e-05 | 1.00 | 1.000 | 6.00e-05 | 0.999190 | 0.999940 |
| C19 | 夹具执行器 | 6.00e-05 | 0.50 | 1.000 | 6.00e-05 | 0.999190 | 0.999880 |

## 6. 最小路集（Minimal Path Sets）
- 最小路集数量：32
| 路集编号 | 边组合 | 对应元件 | 路集可靠度 |
|---|---|---|---:|
| P1 | E1, E2, E4, E5, E6, E7, E12, E13, E16, E18, E19 | C1, C2, C4, C5, C6, C7, C12, C13, C16, C18, C19 | 0.993756 |
| P2 | E1, E2, E4, E5, E6, E7, E12, E13, E16, E17, E19 | C1, C2, C4, C5, C6, C7, C12, C13, C16, C17, C19 | 0.993756 |
| P3 | E1, E2, E4, E5, E6, E7, E12, E13, E15, E18, E19 | C1, C2, C4, C5, C6, C7, C12, C13, C15, C18, C19 | 0.993756 |
| P4 | E1, E2, E4, E5, E6, E7, E12, E13, E15, E17, E19 | C1, C2, C4, C5, C6, C7, C12, C13, C15, C17, C19 | 0.993756 |
| P5 | E1, E2, E4, E5, E6, E7, E8, E9, E16, E18, E19 | C1, C2, C4, C5, C6, C7, C8, C9, C16, C18, C19 | 0.995286 |
| P6 | E1, E2, E4, E5, E6, E7, E8, E9, E16, E17, E19 | C1, C2, C4, C5, C6, C7, C8, C9, C16, C17, C19 | 0.995286 |
| P7 | E1, E2, E4, E5, E6, E7, E8, E9, E15, E18, E19 | C1, C2, C4, C5, C6, C7, C8, C9, C15, C18, C19 | 0.995286 |
| P8 | E1, E2, E4, E5, E6, E7, E8, E9, E15, E17, E19 | C1, C2, C4, C5, C6, C7, C8, C9, C15, C17, C19 | 0.995286 |
| P9 | E1, E2, E3, E5, E6, E7, E12, E13, E16, E18, E19 | C1, C2, C3, C5, C6, C7, C12, C13, C16, C18, C19 | 0.992897 |
| P10 | E1, E2, E3, E5, E6, E7, E12, E13, E16, E17, E19 | C1, C2, C3, C5, C6, C7, C12, C13, C16, C17, C19 | 0.992897 |
| P11 | E1, E2, E3, E5, E6, E7, E12, E13, E15, E18, E19 | C1, C2, C3, C5, C6, C7, C12, C13, C15, C18, C19 | 0.992897 |
| P12 | E1, E2, E3, E5, E6, E7, E12, E13, E15, E17, E19 | C1, C2, C3, C5, C6, C7, C12, C13, C15, C17, C19 | 0.992897 |
| P13 | E1, E2, E3, E5, E6, E7, E8, E9, E16, E18, E19 | C1, C2, C3, C5, C6, C7, C8, C9, C16, C18, C19 | 0.994427 |
| P14 | E1, E2, E3, E5, E6, E7, E8, E9, E16, E17, E19 | C1, C2, C3, C5, C6, C7, C8, C9, C16, C17, C19 | 0.994427 |
| P15 | E1, E2, E3, E5, E6, E7, E8, E9, E15, E18, E19 | C1, C2, C3, C5, C6, C7, C8, C9, C15, C18, C19 | 0.994427 |
| P16 | E1, E2, E3, E5, E6, E7, E8, E9, E15, E17, E19 | C1, C2, C3, C5, C6, C7, C8, C9, C15, C17, C19 | 0.994427 |
| P17 | E1, E2, E4, E5, E6, E7, E12, E14, E11, E16, E18, E19 | C1, C2, C4, C5, C6, C7, C12, C14, C11, C16, C18, C19 | 0.993882 |
| P18 | E1, E2, E4, E5, E6, E7, E12, E14, E11, E16, E17, E19 | C1, C2, C4, C5, C6, C7, C12, C14, C11, C16, C17, C19 | 0.993882 |
| P19 | E1, E2, E4, E5, E6, E7, E12, E14, E11, E15, E18, E19 | C1, C2, C4, C5, C6, C7, C12, C14, C11, C15, C18, C19 | 0.993882 |
| P20 | E1, E2, E4, E5, E6, E7, E12, E14, E11, E15, E17, E19 | C1, C2, C4, C5, C6, C7, C12, C14, C11, C15, C17, C19 | 0.993882 |
| P21 | E1, E2, E4, E5, E6, E7, E8, E10, E11, E16, E18, E19 | C1, C2, C4, C5, C6, C7, C8, C10, C11, C16, C18, C19 | 0.995131 |
| P22 | E1, E2, E4, E5, E6, E7, E8, E10, E11, E16, E17, E19 | C1, C2, C4, C5, C6, C7, C8, C10, C11, C16, C17, C19 | 0.995131 |
| P23 | E1, E2, E4, E5, E6, E7, E8, E10, E11, E15, E18, E19 | C1, C2, C4, C5, C6, C7, C8, C10, C11, C15, C18, C19 | 0.995131 |
| P24 | E1, E2, E4, E5, E6, E7, E8, E10, E11, E15, E17, E19 | C1, C2, C4, C5, C6, C7, C8, C10, C11, C15, C17, C19 | 0.995131 |
| P25 | E1, E2, E3, E5, E6, E7, E12, E14, E11, E16, E18, E19 | C1, C2, C3, C5, C6, C7, C12, C14, C11, C16, C18, C19 | 0.993024 |
| P26 | E1, E2, E3, E5, E6, E7, E12, E14, E11, E16, E17, E19 | C1, C2, C3, C5, C6, C7, C12, C14, C11, C16, C17, C19 | 0.993024 |
| P27 | E1, E2, E3, E5, E6, E7, E12, E14, E11, E15, E18, E19 | C1, C2, C3, C5, C6, C7, C12, C14, C11, C15, C18, C19 | 0.993024 |
| P28 | E1, E2, E3, E5, E6, E7, E12, E14, E11, E15, E17, E19 | C1, C2, C3, C5, C6, C7, C12, C14, C11, C15, C17, C19 | 0.993024 |
| P29 | E1, E2, E3, E5, E6, E7, E8, E10, E11, E16, E18, E19 | C1, C2, C3, C5, C6, C7, C8, C10, C11, C16, C18, C19 | 0.994271 |
| P30 | E1, E2, E3, E5, E6, E7, E8, E10, E11, E16, E17, E19 | C1, C2, C3, C5, C6, C7, C8, C10, C11, C16, C17, C19 | 0.994271 |
| P31 | E1, E2, E3, E5, E6, E7, E8, E10, E11, E15, E18, E19 | C1, C2, C3, C5, C6, C7, C8, C10, C11, C15, C18, C19 | 0.994271 |
| P32 | E1, E2, E3, E5, E6, E7, E8, E10, E11, E15, E17, E19 | C1, C2, C3, C5, C6, C7, C8, C10, C11, C15, C17, C19 | 0.994271 |

## 7. 最小割集（Minimal Cut Sets）
- 最小割集数量：6
| 割集编号 | 边组合 | 对应元件 | 割集失效概率 |
|---|---|---|---:|
| C1 | E1 | C1 | 0.000270 |
| C2 | E2 | C2 | 0.000135 |
| C3 | E5 | C5 | 0.000081 |
| C4 | E6 | C6 | 0.000540 |
| C5 | E7 | C7 | 0.000432 |
| C6 | E19 | C19 | 0.000810 |

## 8. 系统层结果（阿林斯法）
### 任务可靠度（Reliability）
- 可靠度下限：R_lower = 0.995286
- 可靠度上限：R_upper = 1.000000
- 阿林斯估计值：R_sys(Alims) = (R_lower + R_upper) / 2 = 0.997643
- 精确计算值：R_sys(Exact) = 0.997732
- 估计误差：|R_sys(Alims) - R_sys(Exact)| = 0.000089

### 稳态可用度（Availability）
- 可用度下限：A_lower = 0.999323
- 可用度上限：A_upper = 1.000000
- 阿林斯估计值：A_sys(Alims) = (A_lower + A_upper) / 2 = 0.999661
- 精确计算值：A_sys(Exact) = 0.999657
- 估计误差：|A_sys(Alims) - A_sys(Exact)| = 0.000004

### 可靠性达标判定
- 目标可靠度：R_target = 0.95
- 是否达标：是（R_sys(Exact) = 0.997732 ≥ R_target = 0.95）

## 9. 薄弱环节
- 最低单元可靠度：C12 小车变频器，R(T) = 0.998651，λ_eff = 1.00e-04 1/h
- 最低单元可用度：C12 小车变频器，A_ss = 0.999600，μ = 0.25 1/h

> 报告生成时间：2026-05-22 15:18:59

## 10. 学生自定义补充区（请在此区块内补充任务1/4内容，不会被自动覆盖）
### 任务1：一般网络建模与公式
（请在此处补充你的建模思路、公式推导等）

### 任务4：结果解释与工程分析（必做）
（请在此处补充你的可靠度/可用度结果解释、薄弱环节分析、改进建议等）
