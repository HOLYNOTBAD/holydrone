# 展示动画生成工具

`ExportReview.cs` 从实际四种主装配体读取启用/可见零件的三角网格、部件变换和包围盒；仅对 NX 和鲁班猫版输出网格。`SwRot.cs` 按 PID 查找会话，避免默认 COM 连接到其他进程。`export-meshes.ps1` 是入口；`render.py` 使用这些真实几何制作按类别着色、轴向展开的 GIF，不生成或修改配合/爆炸配置。

要求：Windows、SolidWorks 2024、Windows PowerShell/.NET Framework、Python 3.12（本次环境）、`numpy`、`Pillow`、`moderngl`、`glcontext`，以及可用 OpenGL 上下文。英文标注字体使用 Windows Segoe UI。依赖安装应使用独立虚拟环境。

1. 启动专用空白 SolidWorks 会话并记下 PID。导出器若发现会话已有文档会拒绝，避免使用正在编辑的会话。
2. 设置实际路径执行下面命令。缓存目录应在仓库外，以免将约 200 MB 的中间网格提交。
3. 运行渲染后检查装配/展开图片和 GIF，再决定替换发布素材。

```powershell
powershell.exe -NoProfile -File .\demo\tools\export-meshes.ps1 -SolidWorksPid 12345 -Repository 'D:\holydrone' -Cache 'D:\holydrone-cache' -SolidWorksDirectory 'G:\App\sw2024\SOLIDWORKS'
python .\demo\tools\render.py --work 'D:\holydrone-cache' --out '.\demo'
```

导出器使用只读打开选项，不调用 CAD 保存接口。它会解析轻化组件，缓存对应零件并保持文档打开，方便排查；请结束后关闭此专用会话。不要将其改接到含未保存文档的用户会话。失败时先检查日志/输出与 PID，不通过强制结束 SolidWorks 进程处理。

导出清单是当前保存配置的几何快照。旧组件清单属于迁移前的历史审计；需要当前状态时请针对 `Hardware/` 中的装配体重新导出。子装配变换来自 `IComponent2.Transform2`，单位为米；渲染颜色为类别示意，不是原 CAD 外观还原。展示位移不写回 CAD，不作为实际拆装顺序。
