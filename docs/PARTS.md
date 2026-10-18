# 四种主机型零件来源

核查日期：2026-10-18。以主装配体在当前配置中启用的组件为依据，文件级记录见 [组件清单](data/assembly-components.tsv)。采购型号、数量与许可在无证据时保持待确认。

## 采购件与原始外形模型

| 模型标识 / 部件 | 适用机型 | 仓库输入与装配路径 | 来源与采购状态 |
| --- | --- | --- | --- |
| Emax ECO II 2306 | 全部，每机 4 个组件实例 | `modules/Emax ECO II 2306.SLDPRT` | 电机外形；KV、绕组/轴规格、供应商、模型作者与许可待确认 |
| Propeller 7inch | 全部，每机 4 个组件实例 | `modules/Propeller 7inch.SLDPRT`；输入 `modules/misc/propeller.step` 与 `propeller-622.snapshot.2/` | 原始 STEP 可追溯；桨距、旋向组合、实际采购规格待确认 |
| SpeedyBee F405 Mini BLS 35A | 全部 | `modules/SpeedyBee F405 Mini BLS 35A.sldprt`；`modules/misc/speedybee-f405-mini-bls-35a-1.snapshot.4/` | 飞控/电调叠层模型；不据名称断言实物电气配置或固件 |
| GXIVISION S2M06 | 全部 | `modules/Câmera GXIVISION S2M06.sldprt`；`modules/misc/gxivision-s2m06-1.snapshot.6/` | 相机原始模型包含 STEP、SLDPRT、X_T、截图；采购与模型原作者待确认 |
| C-RTK2Hp | 全部 | 实际引用 `modules/misc/C-RTK 2hp/C-RTK2Hp.SLDPRT`；同目录 STEP | 根目录 `modules/C-RTK2Hp.SLDPRT` 也存在；不能用重复文件数计数；采购与连接关系待确认 |
| CUAV P9 数传及天线 | 全部 | `modules/CUAV P9 Radio.SLDASM`，叶子零件位于 `modules/misc/` | 两个叶子模型不是两套电台；频段、地面端、天线与当地使用配置待实物记录确认 |
| 电池及 XT60 外形 | 全部 | `modules/misc/lipo-battery-2.snapshot.2/Bateria Lipo.SLDASM` 与其叶子零件 | 配图/贴图中标签不能证明本机实际电池；容量、串数、倍率、尺寸、重量待确认 |
| 机架板件 | 全部 | `plates/GEPRC Mk4 7in Arms.SLDPRT`、`BottomPlate`、`Top Plate`、`ArmPlate`、`ChinPlate` | 文件名指向机架外形；采购套件与板厚/材料要以实物或加工图核对，不能默认为自制打印件 |
| 螺钉、嵌件、隔柱等 | 全部 | `fasteners/` 与 `Hardware.SLDASM` | 原始紧固件示意；镜像实例及 x4/x8 组合件需按几何/实物统计，不按文件数下单 |
| ORIN NX | 仅 NX 版启用 | `modules/misc/ORIN NX.stp` → `modules/ORIN NX.SLDPRT` | 原始 STEP 的 author 字段为 `INVENTOR`，并非可验证的作者/授权；具体载板、整机厂商和 SKU 待确认 |
| 鲁班猫 4 | 仅鲁班猫版启用 | `modules/LubanCat4/LubanCat 4.STEP` → `LubanCat4_with_bottom_tray.SLDPRT` | 保留底板/散热器/风扇的派生模型；原始下载地址、版本及许可待确认；`no_bottom_tray` 不是当前装配选型 |
| 碳棒、碳管、套筒、棉线、气球 | 两种牵引方案按需 | 静态版 `static_carbon_rod_D4_L300_assumed`；拖曳版 `03_`、`06_`、`12_`；共享 `11_` 气球包络 | 静态碳棒规格获维护者确认且 CAD 一致；其余采购规格需核实。文件中 `assumed`/`BoreAssumed` 保留为建模历史，不是尺寸合格证明 |

## 改装件与自制打印件

| 部件 | 机型与当前用法 | 原始 / 派生关系与制造入口 |
| --- | --- | --- |
| `batteryholder v9` | NX、鲁班猫、静态牵引版 | 共用电池托；已有 SLDPRT 与 STL。旧说明记有 CAD 引用修复，不能据此保证 STL 与 CAD 同步 |
| `camholder30deg` | 四种机型当前均启用 | `camholder/` 保留 0/30/90°与 v2 STL，当前装配使用 30° CAD；打印时需对照具体 STL，不能混选 |
| `receiver_Part1_org` | 四种机型当前均启用 | `receiver/` 保留 `Part1_org.CATPart`、`Part1.CATPart` 与两个 SLDPRT；`receiver_Part1.SLDPRT` 也存在但不是本次清单中的生效模型；作者和改装差异待补记录 |
| `nxholder_Part1`、`nxholder_Part2` | NX 版两件启用 | 目录保留原始 CATPart/STL；没有转换日志证明每一份 CATPart/STL 与同名 SLDPRT 完全等价，打印前复核 |
| `nxholder_Part1` + `nxholder_Part2-rk3588lbc4` | 鲁班猫版 | 共用 Part1，改装 Part2；当前支架提供 SLDPRT/STEP/STL。`*_original.SLDPRT` 为旧稿，不属于当前生产选型 |
| 鲁班猫六孔安装结构 | 鲁班猫版 | 六孔两排间距 55 mm，每排孔距 7.5 mm；底板孔 3.3 mm，支架孔 3.4 mm。机架接口沿用 60×40 mm 四孔，USB 朝前。依据支架说明与既有验证记录；螺钉长度按实物叠层选定 |
| `bolloon holder`、气球托、衬套 | 静态牵引版 | 顶部支架现位于 `balloonstatictowing/`；`气球托v4 4.2mm.STL` 导入成 `balloon_cup_v4_4p2_imported.SLDPRT`；衬套为 `static_adapter_OD6_ID4p2_L71p5.SLDPRT`，目前无独立 STL。不能把碳棒几何也列为打印件 |
| 05 气球快拆托 | 拖曳版 | `05_Balloon50_QuickTie_Ballast.SLDPRT` / 同名 STL |
| 30 铰座 | 拖曳版 | `30_Hinge_RootFillets.SLDPRT` / 同名 STL |
| 31 碳管夹座 | 拖曳版 | `31_Clamp_Rounded.SLDPRT` / 同名 STL |
| 32 改装电池托 | 拖曳版，替换共用电池托 | `32_BatteryHolder_MountReady.SLDPRT` / 同名 STL；属于基于原电池托的改装结构 |
| RTK 天线托、侧板、NX Part3 等 | 目录内可选/历史附件 | 不能把目录内所有模型自动列入四种主机型 BOM；以 [组件清单](data/assembly-components.tsv) 的启用状态为准 |

拖曳版可打印 STL 入口只在 `3dp4drone/balloontowing/STL_打印件/`，共四件。04 导线嘴、21 地面支撑和拖曳紧固件示意均不在当前拖曳装配体中；共用机架紧固件仍存在，不能理解成整机无需紧固件。碳管、套筒、气球包络和棉线不列入该打印目录。

静态牵引支架及衬套的实际固定、打印材料、层高、壁厚、填充、方向与装配公差还没有完整生产记录。仓库中的 PLA 材料库与“可打印网格”只表示模型数据，不证明载荷适用性。
