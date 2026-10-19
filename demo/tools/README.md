# CAD preview generation tools

`ExportReview.cs` reads enabled, visible component meshes, transforms, and bounding boxes from the four main assemblies, exporting meshes for the NX and LubanCat variants. `SwRot.cs` selects a SolidWorks session by PID. `export-meshes.ps1` is the entry point, and `render.py` creates category-colored, vertically exploded GIFs from the exported geometry.

## Requirements

Windows, SolidWorks 2024, Windows PowerShell/.NET Framework, Python 3.12 (the version used for these previews), `numpy`, `Pillow`, `moderngl`, `glcontext`, and an available OpenGL context. Labels use Windows Segoe UI. Install Python dependencies in a dedicated virtual environment.

## Workflow

1. Start a dedicated, empty SolidWorks session and note its PID. The exporter refuses sessions that already have documents open.
2. Run the commands below with your local paths. Keep the cache outside the repository; intermediate meshes can total approximately 200 MB.
3. Inspect the assembled images, exploded images, and GIFs before replacing published assets.

```powershell
powershell.exe -NoProfile -File .\demo\tools\export-meshes.ps1 -SolidWorksPid 12345 -Repository 'D:\holydrone' -Cache 'D:\holydrone-cache' -SolidWorksDirectory 'G:\App\sw2024\SOLIDWORKS'
python .\demo\tools\render.py --work 'D:\holydrone-cache' --out '.\demo'
```

The exporter opens CAD documents read-only and does not save them. It resolves lightweight components, caches parts, and leaves documents open for inspection; close the dedicated session afterward. Do not attach it to a session containing unsaved work. On failure, inspect the logs and PID instead of force-terminating SolidWorks.

Exports capture the saved configurations. Re-export the assemblies under `Hardware/` when current geometry is needed. Subassembly transforms come from `IComponent2.Transform2`, with distances in meters. Rendering colors and exploded-view offsets are illustrative and are not written back to CAD.
