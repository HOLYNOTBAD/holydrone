#!/usr/bin/env python3

import pathlib
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = pathlib.Path(__file__).resolve().parents[1]


class HolydronePackageTest(unittest.TestCase):
    def test_xml_files_parse(self):
        files = [ROOT / "package.xml"]
        files += list((ROOT / "gazebo").rglob("*.sdf"))
        files += list((ROOT / "gazebo").rglob("model.config"))
        files += list((ROOT / "launch").glob("*.launch"))
        for path in files:
            with self.subTest(path=path.relative_to(ROOT)):
                ET.parse(path)

    def test_model_uri_dependencies_are_bundled(self):
        sdf = (ROOT / "gazebo/models/holydrone/holydrone.sdf").read_text()
        model_names = re.findall(r"model://([^/<]+)", sdf)
        for name in model_names:
            with self.subTest(model=name):
                self.assertTrue((ROOT / "gazebo/models" / name).is_dir())

    def test_required_assets_exist(self):
        required = [
            "gazebo/models/holydrone/meshes/holydrone_v1.STL",
            "gazebo/models/holydrone/meshes/Propeller 7inch.STL",
            "gazebo/models/lidar/model.sdf",
            "px4/overlay/ROMFS/px4fmu_common/init.d-posix/airframes/22000_gazebo-classic_holydrone",
        ]
        for relative in required:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())


if __name__ == "__main__":
    unittest.main()
