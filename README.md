# holydrone

Contributors include: Li Hong, Linkai Liu, Dingchen Zeng, Xiangyu Ren, Chunjiang Wu, Yuchen Xiao, Yuehui He, Yujun Zhang, Shuli Lv, and Chen Min.

To everyone who has helped along the way: thank you for your time, patience, and willingness to work through the challenges together. This project would not be where it is today without you.

A Mark4 7-inch drone research platform for drone interception and low-altitude security experiments. Four variants cover ORIN NX and LubanCat 4 companion computers, static balloon towing, and pivoting balloon towing. This repository includes CAD assemblies, 3D-printable parts, PX4 firmware, parameter snapshots, and hardware demonstrations.

Contributions to the hardware and software are welcome.

## Hardware gallery

| ORIN NX | LubanCat 4 |
| :---: | :---: |
| <img src="demo/real/holydrone_nx-cutout.png" width="440" alt="ORIN NX hardware"> | <img src="demo/real/holydrone_lbc4-cutout.png" width="440" alt="LubanCat 4 hardware"> |

| Static balloon towing | Pivoting balloon towing |
| :---: | :---: |
| <img src="demo/real/holydrone_static_towing-cutout.png" height="400" alt="Static towing assembly with a balloon above the drone"> | <img src="demo/real/originals/towing_darkbg.jpg" height="400" alt="Pivoting towing drone carrying a balloon on a tether at night"> |

[Original photos and media notes](demo/real/README.md) · [ORIN NX night flight photo](demo/real/originals/holydrone_nx_darkbg.jpg)

## Flight demonstrations

| Balloon towing | Two-drone balloon experiment |
| :---: | :---: |
| <a href="demo/real/holydrone_towing.mp4"><img src="demo/real/holydrone_towing-preview.gif" height="280" alt="Balloon towing preview"></a> | <a href="demo/real/intercept_slow.mp4"><img src="demo/real/intercept_slow-preview.gif" height="280" alt="Two-drone experiment preview"></a> |
| [Watch MP4](demo/real/holydrone_towing.mp4) | [Watch MP4](demo/real/intercept_slow.mp4) |

## Variants and CAD

| Variant | Structure | Assembly |
| --- | --- | --- |
| ORIN NX | ORIN NX companion computer | [holydrone_nx_v1](Hardware/holydrone_nx_v1.SLDASM) |
| LubanCat 4 | LubanCat 4 with a six-hole mounting bracket | [holydrone_lbc4_v1](Hardware/holydrone_lbc4_v1.SLDASM) |
| Static towing | Vertical carbon rod and balloon cup; no companion computer | [holydrone_static_towing_v1](Hardware/holydrone_static_towing_v1.sldasm) |
| Pivoting towing | Hinged mechanism with ground and airborne configurations; no companion computer | [holydrone_towing_v1](Hardware/holydrone_towing_v1.SLDASM) |

<details>
<summary>CAD exploded views and towing structures</summary>

| ORIN NX | LubanCat 4 |
| :---: | :---: |
| <img src="demo/holydrone_nx_v1-explode.gif" width="440" alt="ORIN NX exploded view"> | <img src="demo/holydrone_lbc4_v1-explode.gif" width="440" alt="LubanCat 4 exploded view"> |

| Static towing | Pivoting towing |
| :---: | :---: |
| <img src="demo/holydrone_static_towing_v1-model.png" width="440" alt="Static towing CAD model"> | <img src="demo/holydrone_towing_v1-model.png" width="440" alt="Pivoting towing CAD model"> |

CAD colors are illustrative. The tether is thickened in the preview for visibility. [Rendering notes](demo/README.md)

</details>

## Getting started

Install Git LFS, then download the repository and its model files:

```bash
git lfs install
git clone https://github.com/HOLYNOTBAD/holydrone.git
cd holydrone
git lfs pull
```

Open the selected assembly in `Hardware/` with **SolidWorks 2024**. Keep the folder structure intact and check rebuild warnings and component references. Before printing, confirm the STL version and millimeter units. Before using firmware or parameters, verify the flight controller, wiring, and aircraft configuration.

## Repository guide

| Location | Contents |
| --- | --- |
| [Hardware](Hardware/) | Assemblies, module models, and frame plates |
| [Aircraft parts](Hardware/3dp4drone/) / [Experiment fixtures](Hardware/3dp4exp/) | Printable brackets, balloon mechanisms, and ground fixtures |
| [BOM notes](Hardware/BOM.md) | Variant differences and component selection notes |
| [Firmware](Firmware/) / [Params](Params/) | PX4 firmware and flight parameter snapshots |
| [demo](demo/) | Photos, videos, and CAD animations |
| [Hardware directory index](Hardware/DIRECTORIES.md) | Model and file descriptions |

Some CAD component models differ from the installed hardware; see the [BOM notes](Hardware/BOM.md). Complete companion-computer software and wiring documentation are not included.

## License

No repository-wide license has been specified. Third-party models remain subject to their original authors' licenses.

## Bill of materials

Select the companion computer and towing accessories for your variant. Verify specifications and quantities before ordering; batteries, wiring, and fasteners are not fully itemized.

| # | Component / specification | Image | Quantity | Purchase link |
| --- | --- | :---: | :---: | --- |
| 1 | Mark4 7-inch frame | <img src="demo/bom/01-mark4-frame.png" width="96" alt="Mark4 7-inch frame"> | 1 set | [Product](https://item.taobao.com/item.htm?id=678090972875&skuId=4871676933340) |
| 2 | EMAX ECO II 2807 1700KV motor | <img src="demo/bom/02-emax-2807-motor.png" width="96" alt="EMAX ECO II 2807 1700KV motor"> | 4 | [Product](https://item.taobao.com/item.htm?id=642731025018&skuId=5101017592191) |
| 3 | MicoAir743 V2 + 70A 32-bit 4-in-1 ESC stack | <img src="demo/bom/03-micoair743-v2-stack.png" width="96" alt="MicoAir743 V2 + 70A 32-bit 4-in-1 ESC stack"> | 1 set | [Product](https://item.taobao.com/item.htm?id=949016296353&skuId=6025215071231) |
| 4 | Amov Lab Allspark2-Orin companion computer | <img src="demo/bom/04-allspark2-orin.png" width="96" alt="Amov Lab Allspark2-Orin companion computer"> | 1 | [Product](https://item.taobao.com/item.htm?id=705748339987&skuId=5786543713974) |
| 5 | CUAV P9 telemetry radio | <img src="demo/bom/05-cuav-p9-radio.png" width="96" alt="CUAV P9 telemetry radio"> | 1 pair | [Product](https://item.taobao.com/item.htm?id=667193254604&skuId=4809453989330) |
| 6 | 2.4 GHz ELRS receiver | <img src="demo/bom/06-elrs-receiver.png" width="96" alt="2.4 GHz ELRS receiver"> | 1 | [Product](https://item.taobao.com/item.htm?id=831092464978&skuId=6055826220853) |
| 7 | Yahboom 2 MP USB camera | <img src="demo/bom/07-usb-camera.png" width="96" alt="Yahboom 2 MP USB camera"> | 1 | [Product](https://detail.tmall.com/item.htm?id=775110864301&skuId=5300422684518) |
| 8 | Unidentified item | <img src="demo/bom/08-unnamed-item.png" width="96" alt="Unidentified item"> | 1 | [Source entry](https://app.notion.com/p/39c3520427fd80ab800af4c0dd67ad9f) |
| 9 | HQProp 7040 7-inch three-blade propellers | <img src="demo/bom/09-hqprop-7040.png" width="96" alt="HQProp 7040 7-inch three-blade propellers"> | Multiple sets | [Product](https://item.taobao.com/item.htm?id=671633881954&skuId=5010241515719) |
| 10 | 12 V DC-DC converter (NX) | <img src="demo/bom/10-dc-dc-converter.png" width="96" alt="12 V DC-DC converter (NX)"> | 1 | [Product](https://item.taobao.com/item.htm?id=677122068881&skuId=6264144190644) |
| 11 | 5 V DC-DC converter | <img src="demo/bom/10-dc-dc-converter.png" width="96" alt="5 V DC-DC converter"> | 1 | [Product](https://item.taobao.com/item.htm?id=677122068881&skuId=6264144190643) |
| 12 | Micro-HDMI display emulator | <img src="demo/bom/12-display-emulator.png" width="96" alt="Micro-HDMI display emulator"> | 1 | [Product](https://item.taobao.com/item.htm?id=896020537740&skuId=5980377650344) |
| 13 | RGB LED strip + quick-connect board | — | 1 | [Product](https://item.taobao.com/item.htm?id=1039871543334&skuId=6226525563898) |
| 14 | Parachute | <img src="demo/bom/14-parachute.png" width="96" alt="Parachute"> | 1 | [Product](https://item.taobao.com/item.htm?id=707712088745&skuId=4970106592804) |
| 15 | CUAV C-RTK 9Ps RTK module | <img src="demo/bom/15-cuav-rtk.png" width="96" alt="CUAV C-RTK 9Ps RTK module"> | 1 | [Product](https://item.taobao.com/item.htm?id=672313744007&skuId=4841813280367) |
