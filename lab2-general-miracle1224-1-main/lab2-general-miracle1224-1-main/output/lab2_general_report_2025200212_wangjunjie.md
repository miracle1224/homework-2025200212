# 实验2：一般网络与可修系统可靠性分析（lab2-general）
2025200212，wangjunjie

## 1. 任务与剖面参数
- 单循环时长：t_cyc = 0.225 h
- 循环次数：N = 60
- 班次任务时间：T = N * t_cyc = 13.500 h
- 可修系统口径：use_effective_lambda = True

## 2. 一般网络模型摘要
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

## 3. 任务剖面（阶段时长）
| 阶段 | duration_h |
|---|---:|
| Pick | 0.010 |
| Lift | 0.020 |
| TravelLoaded | 0.100 |
| Place | 0.015 |
| ReturnEmpty | 0.080 |

## 4. 单元件参数、可靠度与可用度
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

## 5. 系统层结果
- 一般网络任务可靠度：R_sys(T) = 0.997732
- 可修系统稳态可用度：A_sys = 0.999657

## 6. 薄弱环节
- 最低单元可靠度：C12 小车变频器，R(T) = 0.998651，λ_eff = 1.00e-04 1/h
- 最低单元可用度：C12 小车变频器，A_ss = 0.999600，μ = 0.25 1/h

## 7. Sanity checks
- 去冗余应变差（可靠度）：PASS（R_noRed=0.994910 <= R=0.997732）
- 缩短任务时间应变好（可靠度）：PASS（R_halfT=0.998866 >= R=0.997732）
- 去冗余应变差（可用度）：PASS（A_noRed=0.999285 <= A=0.999657）
- 降低维修率应变差（可用度）：PASS（A_halfMu=0.999314 <= A=0.999657）

> 报告生成时间：2026-04-03 10:21:37

## 8. 学生自定义补充区（请在此区块内补充任务1/4内容，不会被自动覆盖）

### 任务1：一般网络建模与公式
- 1.选择当前的source与target是因为这种边界定义符合桥式起重机从启动到完成搬运任务的完整流程
- 2.供电路径：C1-C2-C3/C4-C5   控制路径：C6-C7   执行路径：C8-C9/C12-C13   反馈路径：C15/C16-C17/C18   执行终端：C19

### 任务4：结果解释与工程分析（必做）
（请在此处补充你的可靠度/可用度结果解释、薄弱环节分析、改进建议等）
