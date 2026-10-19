# holydrone

用于无人机结构集成与气球牵引实验的 CAD 仓库，包含四种主装配体、机载模块外形模型、机架板件、改装支架和 3D 打印零件。仓库主要帮助读者查看装配关系、比较上位机安装方案、制作实验附件与打印件。

当前文件以 SolidWorks 装配/零件为主，部分附件提供 STL、STEP 或 CATPart。`Firmware/` 提供 PX4 固件文件，`Params/` 提供两份飞行参数快照；固件与参数的适配机型及实测性能仍需核实。上位机软件、接线图和经过实测确认的整机性能表尚待补充。

## 四种机型与展示

| 主装配体 | 方案 | 当前配置与区别 |
| --- | --- | --- |
| [holydrone_nx_v1.SLDASM](Hardware/holydrone_nx_v1.SLDASM) | ORIN NX 上位机版 | `默认`；启用 ORIN NX、原 NX 安装支架 |
| [holydrone_lbc4_v1.SLDASM](Hardware/holydrone_lbc4_v1.SLDASM) | 鲁班猫 4 上位机版 | `默认`；压缩 ORIN NX，启用带底板鲁班猫模型与六孔改装支架 |
| [holydrone_static_towing_v1.sldasm](Hardware/holydrone_static_towing_v1.sldasm) | 静态牵引版 | `STATIC_TOWING_NOHOST`；压缩 NX 及两件专用支架；增加竖直碳棒、衬套、顶部支架、气球托和气球包络 |
| [holydrone_towing_v1.SLDASM](Hardware/holydrone_towing_v1.SLDASM) | 可转动拖曳版 | `GROUND_0deg` / `AIRBORNE_90deg`；无上位机，含铰座、夹座、改装电池托和拖曳杆；棉线仅在空中配置启用 |

### 上位机版本

| ORIN NX 版 | 鲁班猫 4 版 |
| :---: | :---: |
| <img src="demo/holydrone_nx_v1-explode.gif" width="460" alt="ORIN NX 版分层爆炸动画"> | <img src="demo/holydrone_lbc4_v1-explode.gif" width="460" alt="鲁班猫 4 版分层爆炸动画"> |
| [装配静态预览](demo/holydrone_nx_v1-assembled.png) · [展开静态预览](demo/holydrone_nx_v1-exploded.png) | [装配静态预览](demo/holydrone_lbc4_v1-assembled.png) · [展开静态预览](demo/holydrone_lbc4_v1-exploded.png) |

两段动画分别提取对应主装配体中启用且可见的零件几何及装配变换，参照 [demo/holydrone explode.mp4](demo/holydrone%20explode.mp4) 的轴向分层展开方式制作。颜色按部件类别区分，位移仅用于结构展示，不代表拆装工艺、实际行程或配合关系；未把一份旧视频改名作为两种版本。生成方式与素材记录见 [展示素材说明](demo/README.md)。

### 牵引版本

| 静态牵引版（Static Towing） | 可转动拖曳版（Towing） |
| :---: | :---: |
| <img src="demo/holydrone_static_towing_v1-model.png" width="460" alt="静态牵引版 CAD 建模图"> | <img src="demo/holydrone_towing_v1-model.png" width="460" alt="可转动拖曳版 CAD 建模图"> |
| `STATIC_TOWING_NOHOST`：顶部碳棒与气球包络 | `AIRBORNE_90deg`：空中配置的拖曳机构与下方气球包络 |

两张静态图均从当前主装配体的可见零件网格及装配位置生成，采用英文标题和示意配色，属于 CAD 建模展示。Towing 的橙色绳索仅在展示中加粗，以便缩略图辨识；CAD 绳径仍为 0.18 mm。

静态版结构与安装说明见 [静态牵引说明](Hardware/3dp4drone/balloonstatictowing/静态牵引装配说明.txt)。模型碳棒为 **直径 4 mm、长度 300 mm**，与维护者确认的规格一致；原支架 6 mm 孔通过外径 6 mm、内径 4.2 mm 衬套适配。此核查只确认 CAD 尺寸与已提供规格一致，尚无实物测量记录。

两种牵引版均引用直径 **150 mm** 的气球包络。`11_Balloon_D50_Envelope.SLDPRT` 的旧文件名不代表当前直径；`05_Balloon50_QuickTie_Ballast` 也保留原文件名以保持引用稳定。气球包络是装配示意，不是打印件，也不构成浮力、充气介质或载荷数据。

## 快速开始

1. 克隆或下载完整仓库。CAD 与网格格式已配置 Git LFS；使用 Git 时先安装并初始化 LFS，再执行 `git lfs pull`，确认取到实际大文件。
2. 用 SolidWorks 2024 打开 `Hardware/` 下所需主装配体，保留目录层级。本次四份总装打开均报告需要重建警告（码 32，`swFileLoadWarning_NeedsRegen`），尚未重做完整重建验证。打开后核对配置和缺失引用；`Hardware/modules/misc/` 中的模型也可能是装配依赖，不能当作无用素材删除。
3. 先阅读对应支架说明，再选择 STL 打印。STL 单位按毫米核对；源 CAD 与现有 STL 不一定同步，打印前检查版本和几何。
4. 实物装配前核对采购件尺寸、孔位、紧固方式及电气接口。调试资料见下文“设计方案、性能与调试资料”；动画生成方式见 [展示素材记录](demo/README.md)。

## 仓库结构

目录与远端保持一致：硬件资源集中在 `Hardware/`，固件和参数分别放在 `Firmware/`、`Params/`；本地制作的英文爆炸视图直接保留在 `demo/`。

```text
holydrone/
├── Hardware/                  # 四种主装配体及全部硬件资源
│   ├── holydrone_*_v1.*       # NX、LBC4、static_towing、towing
│   ├── 3dp4drone/             # 机载打印件、CAD 和 STL
│   ├── 3dp4exp/               # 地面实验附件
│   ├── modules/               # 采购模块与原始模型
│   ├── fasteners/             # 紧固件模型
│   └── plates/                # 机架板件模型
├── Firmware/                  # PX4 固件
├── Params/                    # 飞行参数快照
├── demo/                      # 展示动画、图片和参考视频
└── README.md
```

历史备份不属于发布资源，`version_backups/` 已被 Git 忽略。`~$` 开头的是 SolidWorks 会话锁文件，不是设计资产；新增忽略规则不会自动清除已跟踪的历史锁文件。

## 零件来源与 BOM

### Notion 原始采购清单

来源：[holydrone——7 寸穿越机装配](https://app.notion.com/p/3573520427fd8005840cdcc12764cd68) 中的 [1.1 BOM](https://app.notion.com/p/3853520427fd805ebc13d6384a617ec7)。2026-10-19 通过授权连接读取全部 **15 条记录**，数量沿用原表，型号补充来自同页硬件说明。采购链接保留商品 ID 与 SKU，去除分享追踪参数；商品在售状态、价格和选项变更尚未核验。Notion 原记录为私有页面，访问需要相应权限。

| 序号 | 物料 / 规格 | 图片 | 原表数量 | 采购来源 | 核对说明 |
| --- | --- | --- | --- | --- | --- |
| 1 | Mark4 7 寸机架 | <img src="demo/bom/01-mark4-frame.png" width="120" alt="Mark4 7 寸机架"> | 1套 | [商品链接](https://item.taobao.com/item.htm?id=678090972875&skuId=4871676933340) | 7 寸版本 |
| 2 | EMAX ECO II 2807 1700KV 电机 | <img src="demo/bom/02-emax-2807-motor.png" width="120" alt="EMAX ECO II 2807 1700KV 电机"> | 4个 | [商品链接](https://item.taobao.com/item.htm?id=642731025018&skuId=5101017592191) | BOM 与正文最终选型一致 |
| 3 | MicoAir743 V2 + 70A 32bit 四合一电调飞塔 | <img src="demo/bom/03-micoair743-v2-stack.png" width="120" alt="MicoAir743 V2 + 70A 32bit 四合一电调飞塔"> | 1套 | [商品链接](https://item.taobao.com/item.htm?id=949016296353&skuId=6025215071231) | 型号依据正文 §1.4；743 V2 与 743 应区分 |
| 4 | 阿木实验室 Allspark2-Orin 上位机 | <img src="demo/bom/04-allspark2-orin.png" width="120" alt="阿木实验室 Allspark2-Orin 上位机"> | 1个 | [商品链接](https://item.taobao.com/item.htm?id=705748339987&skuId=5786543713974) | NX 版；牵引版不安装上位机 |
| 5 | CUAV P9 数传电台 | <img src="demo/bom/05-cuav-p9-radio.png" width="120" alt="CUAV P9 数传电台"> | 1对 | [商品链接](https://item.taobao.com/item.htm?id=667193254604&skuId=4809453989330) | 1 对为空中端/地面端配套 |
| 6 | 2.4 GHz ELRS 接收机 | <img src="demo/bom/06-elrs-receiver.png" width="120" alt="2.4 GHz ELRS 接收机"> | 1个 | [商品链接](https://item.taobao.com/item.htm?id=831092464978&skuId=6055826220853) | 正文记录 EP1 2400RX 与 RP4TD-M，具体版本待确认 |
| 7 | 亚博智能 USB 相机（200 万像素） | <img src="demo/bom/07-usb-camera.png" width="120" alt="亚博智能 USB 相机（200 万像素）"> | 1个 | [商品链接](https://detail.tmall.com/item.htm?id=775110864301&skuId=5300422684518) | 规格依据正文 §1.8 |
| 8 | 未命名物料 | <img src="demo/bom/08-unnamed-item.png" width="120" alt="未命名物料"> | 1个 | [原始条目](https://app.notion.com/p/39c3520427fd80ab800af4c0dd67ad9f) | 原始名称为空，子页面正文也为空；用途待确认 |
| 9 | HQProp 7040 7 寸三叶桨 | <img src="demo/bom/09-hqprop-7040.png" width="120" alt="HQProp 7040 7 寸三叶桨"> | 多套 | [商品链接](https://item.taobao.com/item.htm?id=671633881954&skuId=5010241515719) | 数量为“多套”，原名称另含“x2”；包装/采购数量待确认 |
| 10 | DC-DC 降压模块（12 V，NX 用） | <img src="demo/bom/10-dc-dc-converter.png" width="120" alt="DC-DC 降压模块（12 V，NX 用）"> | 1个 | [商品链接](https://item.taobao.com/item.htm?id=677122068881&skuId=6264144190644) | 与 5 V 模块为同一商品不同 SKU |
| 11 | DC-DC 降压模块（5 V） | <img src="demo/bom/10-dc-dc-converter.png" width="120" alt="DC-DC 降压模块（5 V）"><br>同商品通用示意图 | 1 | [商品链接](https://item.taobao.com/item.htm?id=677122068881&skuId=6264144190643) | 原表数量为“1” |
| 12 | microHDMI 显示器模拟器 | <img src="demo/bom/12-display-emulator.png" width="120" alt="microHDMI 显示器模拟器"> | 1个 | [商品链接](https://item.taobao.com/item.htm?id=896020537740&skuId=5980377650344) | 原文“显卡欺骗器”；接口规格需核对 |
| 13 | RGB 灯带 + 快接板 | 待补图（Notion 原表无图片） | 1个 | [商品链接](https://item.taobao.com/item.htm?id=1039871543334&skuId=6226525563898) | 原表未拆分套内数量 |
| 14 | 降落伞 | <img src="demo/bom/14-parachute.png" width="120" alt="降落伞"> | 1个 | [商品链接](https://item.taobao.com/item.htm?id=707712088745&skuId=4970106592804) | 规格、触发方式与适配机型待确认 |
| 15 | RTK（正文指定 CUAV C-RTK 9Ps） | <img src="demo/bom/15-cuav-rtk.png" width="120" alt="RTK（正文指定 CUAV C-RTK 9Ps）"> | 1个 | [商品链接](https://item.taobao.com/item.htm?id=672313744007&skuId=4841813280367) | 型号依据正文 §1.9；基站/移动端数量分配待确认 |

图片取自 Notion 原条目，已保存为仓库内文件，点击仓库中的原图可放大查看。[配图来源记录](demo/bom/README.md) 列出对应条目。5 V 降压模块引用同商品的通用示意图（原图展示多种输出电压），不代表已核实 5 V 实物；RGB 灯带 + 快接板的原条目没有图片，待补充。未命名物料保持原名称状态，图片不作为型号确认依据。

**选型冲突与缺项：** Notion 最终选型是 2807 1700KV，但正文另一处对 7 寸 / 6S 方案建议更低 KV。BOM 没有明确电池串数、容量及电机—桨—电池配套，仍需实物确认；不能将未命名条目直接视为电池。完整线束、紧固件、绑带和打印材料的数量也尚未列明。

**正文补充、未单列于上述 15 条 BOM：** 微空 MTF-02P 光流测距模块及 [5G 模块商品](https://detail.tmall.com/item.htm?id=807650545092&skuId=5487563908572)。数量、具体版本及各机型适配待确认。

### 四种机型的差异与 CAD 来源

| 机型 | 采购 / 自制差异 | 仓库依据 |
| --- | --- | --- |
| ORIN NX 版 | Allspark2-Orin、12 V 降压模块与 NX 支架 | `Hardware/modules/ORIN NX.SLDPRT`、`Hardware/3dp4drone/nxholder/` |
| 鲁班猫 4 版 | 鲁班猫 4 与六孔改装支架；Notion 的 RK3588 小节尚无具体采购清单 | `Hardware/modules/LubanCat4/`、`nxholder_Part2-rk3588lbc4` |
| 静态牵引版 | 无上位机；用户确认的 Φ4 × 300 mm 碳棒、顶部支架、气球托和 6→4.2 mm 衬套 | `Hardware/3dp4drone/balloonstatictowing/`；附件数量和供应商不在 Notion 原表中 |
| 可转动拖曳版 | 无上位机；碳管、转轴套筒、棉线和 05/30/31/32 四种打印件 | `Hardware/3dp4drone/balloontowing/`；`BoreAssumed` 等文件名尺寸属于建模标识 |

**CAD 与实物选型差异：** 仓库仍保留 Emax ECO II **2306**、SpeedyBee F405 Mini BLS **35A**、GXIVISION S2M06 和 C-RTK**2Hp** 外形文件，与 Notion 的 **2807 / MicoAir743 V2 70A / 亚博 USB 相机 / C-RTK 9Ps** 不完全一致。本次更新 BOM 文档，CAD 外形、安装孔位及接口兼容性尚未据此重新验证。

逐目录说明见 [目录索引](Hardware/DIRECTORIES.md)。模型实例数不能直接作为采购数量；第三方模型的来源及再分发许可仍需追溯。


## 设计方案、性能与调试资料

**设计方案（仓库内已核对）：** NX 与鲁班猫版共用基础机架，改变上位机和安装支架；鲁班猫保留底板、散热器和风扇，USB 朝向摄像头一侧，通过底板六孔安装。安装接口和既有验证记录见 [鲁班猫支架说明](Hardware/3dp4drone/nxholder/鲁班猫支架安装说明.txt) 与 [孔位验证](Hardware/3dp4drone/nxholder/tray6_validation.txt)。牵引版均停用 NX；静态版采用竖直碳棒与衬套，可转动版使用铰接机构的地面/空中两种配置。

**性能：** 尚无可核验的整机重量、推重比、有效载荷、续航、航速、定位精度、抗风能力或牵引能力的实测记录。7 英寸桨叶模型、150 mm 气球几何或板卡名称均不足以推算整机指标，因此不提供猜测数值。

**调试：** 仓库现有说明涉及 CAD 孔位、安装方向、组件引用和部分配合修复；现有 [PX4 固件](Firmware/micoair_h743-v2_default.px4)、[0924 参数](Params/0924.params) 和 [0929 fix mag 参数](Params/0929%20fix%20mag.params) 可作为调试资料；固件版本、目标飞控、参数对应机型、PID 与串口映射仍需核验，Notion 另有接线图片和通讯配置记录，其完整内容与当前实物的一致性尚待核对；仓库内可复现的标定流程和飞行日志仍待补充。已有 CAD 核查不能视为完成整机干涉、强度、振动或飞行验证。需补充上述资料后，才能形成具体调试步骤。

**Notion 核对范围：** 已通过授权连接读取原页面及完整的 BOM 数据库，用于上述采购清单与型号差异说明。主页面返回截断提示及 1 个未识别块，本次读取不构成接线、调试和性能内容的完整核验。正文另有 MAVROS、P9 与接收机配置记录，需结合固件版本及实际接线单独核对；本次更新重点为 BOM。

## 模型来源与许可

当前仓库未发现明确许可证文件；本次未擅自指定开源许可证。公开仓库与第三方下载快照不自动授予模型再分发、修改或商业使用权。外部模型的原作者、原始下载链接和许可需要逐项补齐；已有 STEP 头部与目录名只作为线索，不当作授权证明。第三方模型的来源证据及授权情况仍需逐项补充确认。
