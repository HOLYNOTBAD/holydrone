# Bill of materials and variant notes

The illustrated [bill of materials](../README.md#bill-of-materials) includes purchase links. It is based on the [original assembly notes](https://app.notion.com/p/3573520427fd8005840cdcc12764cd68) and [15-entry BOM](https://app.notion.com/p/3853520427fd805ebc13d6384a617ec7). The Notion sources require access permission. Quantities follow the source list; verify current product options before ordering.

## Component selection

| # | Component / specification | Quantity | Selection notes |
| --- | --- | --- | --- |
| 1 | Mark4 7-inch frame | 1 set | 7-inch version. |
| 2 | EMAX ECO II 2807 1700KV motor | 4 | Final motor selection in the source BOM. |
| 3 | MicoAir743 V2 + 70A 32-bit 4-in-1 ESC stack | 1 set | Distinguish the 743 V2 from the 743. |
| 4 | Amov Lab Allspark2-Orin companion computer | 1 | NX variant only; towing variants omit the companion computer. |
| 5 | CUAV P9 telemetry radio | 1 pair | One pair includes the air and ground units. |
| 6 | 2.4 GHz ELRS receiver | 1 | EP1 2400RX and RP4TD-M appear in the source; confirm the installed version. |
| 7 | Yahboom 2 MP USB camera | 1 | 2 MP specification from the source hardware notes. |
| 8 | Unidentified item | 1 | The source entry has no name or description; identity and use remain unconfirmed. |
| 9 | HQProp 7040 7-inch three-blade propellers | Multiple sets | The source lists multiple sets and also mentions x2; confirm package contents and order quantity. |
| 10 | 12 V DC-DC converter (NX) | 1 | Same product listing as the 5 V converter, with a different SKU. |
| 11 | 5 V DC-DC converter | 1 | Shared generic product image; verify the 5 V option. |
| 12 | Micro-HDMI display emulator | 1 | Check the connector specification. |
| 13 | RGB LED strip + quick-connect board | 1 | The source does not itemize the contents of the set. |
| 14 | Parachute | 1 | Confirm size, trigger mechanism and suitability for the selected variant. |
| 15 | CUAV C-RTK 9Ps RTK module | 1 | Confirm the allocation between base and rover units. |

The final motor selection is 2807 1700KV, although another source passage recommends lower KV for a 7-inch / 6S setup. Battery cell count and capacity, motor–propeller–battery compatibility, and the quantities of wiring, fasteners, straps, and printing materials still need confirmation. Item 8 should not be treated as a battery.

The source hardware notes also mention an MicoAir MTF-02P optical-flow/range module and a [5G module](https://detail.tmall.com/item.htm?id=807650545092&skuId=5487563908572), which are not separate entries in the 15-item list. Their quantities and variant compatibility remain unconfirmed.

## Variant differences

| Variant | Additional or different hardware | CAD location |
| --- | --- | --- |
| ORIN NX | Allspark2-Orin, 12 V converter, and NX brackets | `Hardware/modules/ORIN NX.SLDPRT`, `Hardware/3dp4drone/nxholder/` |
| LubanCat 4 | LubanCat 4 and a six-hole bracket; the source RK3588 section has no detailed purchase list | `Hardware/modules/LubanCat4/`, `nxholder_Part2-rk3588lbc4` |
| Static towing | No companion computer; 4 mm × 300 mm carbon rod, top bracket, balloon cup, and 6 mm OD / 4.2 mm ID sleeve | `Hardware/3dp4drone/balloonstatictowing/` |
| Pivoting towing | No companion computer; carbon tube, pivot sleeve, tether, and printable parts 05/30/31/32 | `Hardware/3dp4drone/balloontowing/` |

Towing accessory quantities and suppliers are not included in the source BOM. Dimensions in filenames such as `BoreAssumed` are modeling labels, not confirmed purchase specifications.

## CAD and hardware differences

The CAD library contains Emax ECO II **2306**, SpeedyBee F405 Mini BLS **35A**, GXIVISION S2M06, and C-RTK**2Hp** models. These differ from the **2807 / MicoAir743 V2 70A / Yahboom USB camera / C-RTK 9Ps** selection in the source notes. Check mounting holes and interfaces against the actual components.

See the [directory index](DIRECTORIES.md) for model locations and the [image source list](../demo/bom/README.md) for product illustrations. CAD instance counts are not purchase quantities.
