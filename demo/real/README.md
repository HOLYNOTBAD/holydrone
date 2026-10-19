# Hardware photos and flight videos

These assets were prepared on October 20, 2026 from the supplied `paper_so3nmpc/video/holydrone demo/` folder. Variant names follow the source filenames. See the [main README](../../README.md) for the gallery and the [CAD media guide](../README.md) for rendered models.

## Photos and transparent cutouts

| Subject | Original photo | Transparent PNG |
| --- | --- | --- |
| ORIN NX | [Photo](originals/holydrone_nx.png) | [Cutout](holydrone_nx-cutout.png) |
| LubanCat 4 | [Photo](originals/holydrone_lbc4.jpg) | [Cutout](holydrone_lbc4-cutout.png) |
| Static towing assembly, rod, and balloon | [Photo](originals/holydrone_static_towing.jpg) | [Cutout](holydrone_static_towing-cutout.png) |
| ORIN NX at night | [Photo](originals/holydrone_nx_darkbg.jpg) | — |
| Pivoting towing at night | [Photo](originals/towing_darkbg.jpg) | — |

Original photos are unchanged. Transparent PNGs use AI-assisted background removal with the built-in imagegen tool. The editing instructions were to remove the desk and laboratory background while preserving the original viewpoint, proportions, propellers, wiring, camera, companion computer, and mounts. The static towing cutout also retains the foreground aircraft, thin rod, balloon cup, and balloon while excluding other aircraft in the background. No text, shadows, or missing parts were requested; a follow-up requested cleanup outside the balloon contour.

Cutouts are for visual presentation; consult the originals for fine edges and textures. The static balloon is already cropped at the top of the source photograph. The NX PNG was selected instead of its alternative JPG to avoid duplicate photos. All source files remain in the original folder, and copies of the three cutouts were saved there as well.

## Videos

| Subject | MP4 | GIF preview | Source properties |
| --- | --- | --- | --- |
| Nighttime balloon towing | [Video](holydrone_towing.mp4) | [Preview](holydrone_towing-preview.gif) | 2160 × 3840, approximately 119.724 fps, 4.260 seconds |
| Two-drone balloon experiment | [Video](intercept_slow.mp4) | [Preview](intercept_slow-preview.gif) | 3840 × 2160, 120 fps, 4.875 seconds |

Web videos use H.264, YUV420p, 30 fps, a maximum dimension of 1280 pixels, CRF 23, and faststart, without audio. GIFs use 10 fps, a maximum dimension of 640 pixels, and continuous looping. Both preserve the source playback timeline without cropping or additional speed changes. The original high-resolution videos remain in the source folder.

`intercept_slow` retains the source filename; it does not establish the capture speed or slow-motion factor. These clips illustrate visible hardware and events, rather than quantitative performance.

Videos were converted with FFmpeg. Source and output hashes, dimensions, and file sizes are recorded in [manifest.json](manifest.json).
