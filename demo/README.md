# Media guide

[Hardware photos and flight videos](real/README.md) are in `real/`. CAD previews are stored directly in this directory; generation scripts are in [tools](tools/README.md).

## CAD previews

| Asset | Assembly / configuration | Visible component instances |
| --- | --- | --- |
| `holydrone_nx_v1-explode.gif` | [ORIN NX](../Hardware/holydrone_nx_v1.SLDASM) / default | 52 |
| `holydrone_lbc4_v1-explode.gif` | [LubanCat 4](../Hardware/holydrone_lbc4_v1.SLDASM) / default | 52 |
| `holydrone_static_towing_v1-model.png` | [Static towing](../Hardware/holydrone_static_towing_v1.sldasm) / `STATIC_TOWING_NOHOST` | 54 |
| `holydrone_towing_v1-model.png` | [Pivoting towing](../Hardware/holydrone_towing_v1.SLDASM) / `AIRBORNE_90deg` | 56 |

`*-assembled.png` and `*-exploded.png` provide still views of the two companion-computer variants. The GIFs are 960 × 720, loop continuously, and use 72 input frames at 80 ms per frame (5.76 seconds). Identical frames may be merged by the encoder. The static towing previews are 1200 × 1000.

The previews use actual CAD meshes and component transforms. Colors and exploded-view offsets are illustrative; they do not represent physical simulation, disassembly instructions, or hardware photographs. The [reference video](holydrone%20explode.mp4), 1920 × 1080 and approximately 6.073 seconds long, informed the vertical exploded-view layout.

## Rendering details

- The two towing previews preserve the saved assembly positions without exploded-view offsets. Their balloon envelopes are 150 mm in diameter.
- The static balloon cup uses its source STL because SolidWorks returned no triangles for the imported part. Millimeters are converted to meters before applying the saved component transform.
- The pivoting towing tether is radially enlarged from 0.18 mm to an equivalent 6 mm in the preview and colored orange for visibility. Its centerline, length, and position are preserved; CAD files are unchanged.
- Components without usable triangle meshes are omitted unless a source mesh fallback is specified.

CAD previews were prepared on October 18–19, 2026. See [media-manifest.json](media-manifest.json) for recorded input/output hashes and sizes, and [tools](tools/README.md) for the export workflow. Product illustrations and their sources are in [bom](bom/README.md).
