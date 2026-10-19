# 展示素材记录

本目录沿用远端的平铺结构：GIF、PNG、参考 MP4、哈希记录和检查记录直接放在 `demo/`，生成脚本集中在 `demo/tools/`。图中文字全部为英文（ORIN NX / LubanCat 4 / Static Towing / Towing），正文说明保留中文。

2026-10-18 从当前主装配体实际零件几何生成。原始参考为 [holydrone explode.mp4](holydrone%20explode.mp4)，1920×1080，约 6.073 秒：由合拢状态沿竖向分层展开。没有用该视频冒充新机型，也没有通过生成式图像补画零件。

| 素材 | 输入 | 内容 |
| --- | --- | --- |
| `holydrone_nx_v1-explode.gif` | [`Hardware/holydrone_nx_v1.SLDASM`](../Hardware/holydrone_nx_v1.SLDASM) / 默认配置 | ORIN NX 版本，独立提取 52 个启用且可见的叶子组件实例 |
| `holydrone_lbc4_v1-explode.gif` | [`Hardware/holydrone_lbc4_v1.SLDASM`](../Hardware/holydrone_lbc4_v1.SLDASM) / 默认配置 | 鲁班猫版本，独立提取 52 个启用且可见的叶子组件实例，含实际带底板鲁班猫与改装支架 |
| `*-assembled.png` | 对应动画合拢帧 | 静态装配预览 |
| `*-exploded.png` | 对应动画最大展开帧 | 静态展开预览 |

GIF 尺寸 960×720，循环播放；72 个输入帧按 80 ms 排布，总时长 5.76 秒。重复静止帧可能被编码器合并，编码帧数以实际验证结果为准。共用调色板 128 色。类别配色、光照和展示位移由渲染器指定，整体仍来自真实 CAD 网格和部件变换；不表达物理仿真、实际运动轨迹、装配工艺或产品实拍。

生成工具见 [tools](tools/README.md)，输入/输出 SHA-256 与文件大小见 [media-manifest.json](media-manifest.json)。README 使用相对路径嵌入 GIF，静态 PNG 供无法播放动画时查看。

2026-10-19：新增两款牵引机型的 1200×1000 静态 CAD 展示图，分别读取当前保存的 `STATIC_TOWING_NOHOST` 与 `AIRBORNE_90deg` 配置。保留实际装配位置，采用示意配色与英文标题；气球包络直径 150 mm。

| 素材 | 输入配置 | 绘制的可见组件实例 |
| --- | --- | --- |
| `holydrone_static_towing_v1-model.png` | `Hardware/holydrone_static_towing_v1.sldasm` / `STATIC_TOWING_NOHOST` | 54 |
| `holydrone_towing_v1-model.png` | `Hardware/holydrone_towing_v1.SLDASM` / `AIRBORNE_90deg` | 56 |

两图来自 SolidWorks 只读提取的零件网格和装配变换；未修改 CAD，未施加爆炸位移。无可用三角网格的组件不绘制，细棉线在整机缩放下可能不明显。

2026-10-19：展示素材与生成工具统一迁移到 demo；两种机型的 GIF 和静态预览标题、状态、图例及页脚全部采用英文。

2026-10-19：修复静态牵引气球托漏绘。该导入零件的 SolidWorks 三角面提取为空，改用同目录原始 `气球托v4 4.2mm.STL`，将毫米转换为米并应用保存的组件变换；气球托采用橙色，与红色气球区分。
