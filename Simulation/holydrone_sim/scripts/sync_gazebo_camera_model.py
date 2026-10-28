#!/usr/bin/env python3

import argparse
import math
import os
import re
import sys
from dataclasses import dataclass
from typing import Optional, Tuple


R_CAM_BODY_PATTERN = re.compile(
    r"^\s*R_cam_body\s*:\s*\[([^]]*)\]\s*(?:#.*)?$"
)
IMG_WIDTH_PATTERN = re.compile(r"^\s*img_width\s*:\s*(\d+)\s*(?:#.*)?$")
IMG_HEIGHT_PATTERN = re.compile(r"^\s*img_height\s*:\s*(\d+)\s*(?:#.*)?$")
IMG_F_PATTERN = re.compile(r"^\s*img_f\s*:\s*([-+]?\d+(?:\.\d+)?)\s*(?:#.*)?$")
FX_PATTERN = re.compile(r"^\s*fx\s*:\s*([-+]?\d+(?:\.\d+)?)\s*(?:#.*)?$")
FY_PATTERN = re.compile(r"^\s*fy\s*:\s*([-+]?\d+(?:\.\d+)?)\s*(?:#.*)?$")
CX_PATTERN = re.compile(r"^\s*cx\s*:\s*([-+]?\d+(?:\.\d+)?)\s*(?:#.*)?$")
CY_PATTERN = re.compile(r"^\s*cy\s*:\s*([-+]?\d+(?:\.\d+)?)\s*(?:#.*)?$")
DISTORTION_PATTERN = re.compile(
    r"^\s*distortion_coeffs\s*:\s*\[([^]]*)\]\s*(?:#.*)?$"
)
POSITION_BODY_PATTERN = re.compile(
    r"^\s*position_body_m\s*:\s*\[([^]]*)\]\s*(?:#.*)?$"
)
FPS_PATTERN = re.compile(
    r"^\s*(?:fps|framerate)\s*:\s*([-+]?\d+(?:\.\d+)?)\s*(?:#.*)?$"
)
AIRCRAFT_SDF_PATH_PATTERN = re.compile(r"^\s*aircraft_sdf\s*:\s*['\"]?([^'\"#\n]+)['\"]?\s*(?:#.*)?$")
FPV_SDF_PATH_PATTERN = re.compile(r"^\s*fpv_cam_sdf\s*:\s*['\"]?([^'\"#\n]+)['\"]?\s*(?:#.*)?$")
LEGACY_SDF_PATH_PATTERN = re.compile(r"^\s*fpv_cam_sdf\s*:\s*['\"]?([^'\"#\n]+)['\"]?\s*(?:#.*)?$")
POSE_PATTERN = re.compile(r"(<pose>\s*)([^<]+?)(\s*</pose>)")
TAG_PATTERN_TEMPLATE = r"(<{tag}>\s*)([^<]+?)(\s*</{tag}>)"


@dataclass(frozen=True)
class CameraConfig:
    r_cam_body: Tuple[float, float, float, float, float, float, float, float, float]
    position_body_m: Optional[Tuple[float, float, float]]
    img_width: int
    img_height: int
    fx: float
    fy: float
    cx: float
    cy: float
    distortion: Tuple[float, float, float, float, float]
    fps: Optional[float]
    aircraft_sdf: Optional[str]
    fpv_cam_sdf: Optional[str]


def parse_camera_config(config_path: str) -> CameraConfig:
    r_cam_body = None
    img_width = None
    img_height = None
    img_f = None
    fx = None
    fy = None
    cx = None
    cy = None
    distortion = None
    position_body_m = None
    fps = None
    aircraft_sdf = None
    fpv_cam_sdf = None

    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            m_rotation = R_CAM_BODY_PATTERN.match(line)
            if m_rotation:
                values = [
                    float(value.strip())
                    for value in m_rotation.group(1).split(",")
                    if value.strip()
                ]
                if len(values) != 9:
                    raise RuntimeError(
                        f"R_cam_body must contain 9 values in {config_path}"
                    )
                r_cam_body = tuple(values)
                continue
            m_width = IMG_WIDTH_PATTERN.match(line)
            if m_width:
                img_width = int(m_width.group(1))
                continue
            m_height = IMG_HEIGHT_PATTERN.match(line)
            if m_height:
                img_height = int(m_height.group(1))
                continue
            m_f = IMG_F_PATTERN.match(line)
            if m_f:
                img_f = float(m_f.group(1))
                continue
            m_fx = FX_PATTERN.match(line)
            if m_fx:
                fx = float(m_fx.group(1))
                continue
            m_fy = FY_PATTERN.match(line)
            if m_fy:
                fy = float(m_fy.group(1))
                continue
            m_cx = CX_PATTERN.match(line)
            if m_cx:
                cx = float(m_cx.group(1))
                continue
            m_cy = CY_PATTERN.match(line)
            if m_cy:
                cy = float(m_cy.group(1))
                continue
            m_distortion = DISTORTION_PATTERN.match(line)
            if m_distortion:
                values = [
                    float(value.strip())
                    for value in m_distortion.group(1).split(",")
                    if value.strip()
                ]
                if len(values) not in (4, 5):
                    raise RuntimeError(
                        f"distortion_coeffs must contain 4 or 5 values in {config_path}"
                    )
                if len(values) == 4:
                    values.append(0.0)
                distortion = tuple(values)
                continue
            m_position = POSITION_BODY_PATTERN.match(line)
            if m_position:
                values = [
                    float(value.strip())
                    for value in m_position.group(1).split(",")
                    if value.strip()
                ]
                if len(values) != 3:
                    raise RuntimeError(
                        f"position_body_m must contain 3 values in {config_path}"
                    )
                position_body_m = tuple(values)
                continue
            m_fps = FPS_PATTERN.match(line)
            if m_fps:
                fps = float(m_fps.group(1))
                continue
            m_path = AIRCRAFT_SDF_PATH_PATTERN.match(line)
            if m_path:
                aircraft_sdf = m_path.group(1).strip()
                continue
            m_fpv_path = FPV_SDF_PATH_PATTERN.match(line)
            if m_fpv_path:
                fpv_cam_sdf = m_fpv_path.group(1).strip()
                continue
            # Backward compatibility with early config key.
            m_legacy_path = LEGACY_SDF_PATH_PATTERN.match(line)
            if m_legacy_path and fpv_cam_sdf is None:
                fpv_cam_sdf = m_legacy_path.group(1).strip()

    if r_cam_body is None:
        raise RuntimeError(f"R_cam_body not found in {config_path}")
    if img_width is None or img_height is None or (img_f is None and fx is None):
        raise RuntimeError(f"img_width/img_height/fx or img_f not fully found in {config_path}")

    effective_fx = fx if fx is not None else img_f
    effective_fy = fy if fy is not None else effective_fx
    effective_cx = cx if cx is not None else 0.5 * img_width
    effective_cy = cy if cy is not None else 0.5 * img_height
    effective_distortion = (
        distortion if distortion is not None else (0.0, 0.0, 0.0, 0.0, 0.0)
    )
    return CameraConfig(
        r_cam_body=r_cam_body,
        position_body_m=position_body_m,
        img_width=img_width,
        img_height=img_height,
        fx=effective_fx,
        fy=effective_fy,
        cx=effective_cx,
        cy=effective_cy,
        distortion=effective_distortion,
        fps=fps,
        aircraft_sdf=aircraft_sdf,
        fpv_cam_sdf=fpv_cam_sdf,
    )


def params_root() -> str:
    env_root = os.environ.get("HOLYDRONE_SIM_DIR")
    if env_root:
        return os.path.realpath(env_root)
    try:
        import rospkg
    except ImportError:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    try:
        return os.path.realpath(rospkg.RosPack().get_path("holydrone_sim"))
    except rospkg.ResourceNotFound:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))


def resolve_aircraft_sdf_path(cli_sdf: Optional[str], yaml_sdf: Optional[str]) -> Optional[str]:
    candidates = []
    if cli_sdf:
        candidates.append(cli_sdf)
    env_sdf = os.environ.get("GAZEBO_AIRCRAFT_SDF") or os.environ.get("GAZEBO_FPV_CAM_SDF")
    if env_sdf:
        candidates.append(env_sdf)
    if yaml_sdf:
        candidates.append(yaml_sdf)

    candidates.append(
        os.path.join(
            params_root(),
            "gazebo/models/holydrone/holydrone.sdf",
        )
    )

    seen = set()
    for path in candidates:
        if not path:
            continue
        expanded = os.path.expanduser(path)
        if not os.path.isabs(expanded):
            expanded = os.path.join(params_root(), expanded)
        if expanded in seen:
            continue
        seen.add(expanded)
        if os.path.isfile(expanded):
            return expanded
    return None


def resolve_fpv_sdf_path(yaml_sdf: Optional[str]) -> Optional[str]:
    candidates = []
    env_sdf = os.environ.get("GAZEBO_FPV_SENSOR_SDF")
    if env_sdf:
        candidates.append(env_sdf)
    if yaml_sdf:
        candidates.append(yaml_sdf)

    candidates.extend([
        os.path.join(
            params_root(),
            "gazebo/models/fpv_cam/fpv_cam.sdf",
        ),
    ])

    seen = set()
    for path in candidates:
        if not path:
            continue
        expanded = os.path.expanduser(path)
        if not os.path.isabs(expanded):
            expanded = os.path.join(params_root(), expanded)
        if expanded in seen:
            continue
        seen.add(expanded)
        if os.path.isfile(expanded):
            return expanded
    return None


def update_aircraft_camera_pose(
    sdf_path: str,
    r_cam_body: Tuple[float, float, float, float, float, float, float, float, float],
    position_body_m: Optional[Tuple[float, float, float]]
) -> bool:
    with open(sdf_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    include_idx = None
    for i, line in enumerate(lines):
        if re.search(r"<uri>\s*model://[^<]*fpv_cam\s*</uri>", line):
            include_idx = i
            break
    if include_idx is None:
        raise RuntimeError(f"cannot find an FPV camera <include> in {sdf_path}")

    pose_idx = None
    for i in range(include_idx + 1, min(include_idx + 20, len(lines))):
        if "<pose>" in lines[i] and "</pose>" in lines[i]:
            pose_idx = i
            break
    if pose_idx is None:
        raise RuntimeError(f"cannot find include-level <pose> after model://fpv_cam in {sdf_path}")

    original = lines[pose_idx]
    m = POSE_PATTERN.search(original)
    if not m:
        raise RuntimeError(f"failed to parse pose line: {original.strip()}")

    pose_values = m.group(2).split()
    if len(pose_values) != 6:
        raise RuntimeError(f"pose needs 6 values, got {len(pose_values)} in: {original.strip()}")

    if position_body_m is None:
        x, y, z = pose_values[0], pose_values[1], pose_values[2]
    else:
        x, y, z = (f"{value:.6f}" for value in position_body_m)
    # Gazebo's camera link uses FLU-like X-forward/Y-left/Z-up axes. The
    # optical frame is RDF, so remove the fixed RDF->FLU basis change from
    # the complete camera RDF -> body FLU extrinsic to obtain body<-link.
    r0 = (
        (0.0, 0.0, 1.0),
        (-1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
    )
    r_bc = tuple(tuple(r_cam_body[3*row + col] for col in range(3))
                 for row in range(3))
    r_bl = tuple(
        tuple(sum(r_bc[row][k] * r0[col][k] for k in range(3))
              for col in range(3))
        for row in range(3)
    )
    # ZYX Euler angles used by SDF <pose>: R = Rz(yaw) Ry(pitch) Rx(roll).
    pitch = math.asin(max(-1.0, min(1.0, -r_bl[2][0])))
    if abs(math.cos(pitch)) > 1e-8:
        roll = math.atan2(r_bl[2][1], r_bl[2][2])
        yaw = math.atan2(r_bl[1][0], r_bl[0][0])
    else:
        roll = 0.0
        yaw = math.atan2(-r_bl[0][1], r_bl[1][1])
    replacement_pose = (
        f"{x} {y} {z} {roll:.6f} {pitch:.6f} {yaw:.6f}")
    new_line = POSE_PATTERN.sub(
        lambda m: f"{m.group(1)}{replacement_pose}{m.group(3)}",
        original,
        count=1,
    )

    if new_line == original:
        return False

    lines[pose_idx] = new_line
    with open(sdf_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return True


def replace_tag(text: str, tag: str, value: str) -> Tuple[str, bool]:
    pattern = re.compile(TAG_PATTERN_TEMPLATE.format(tag=tag))
    new_text, count = pattern.subn(
        lambda m: f"{m.group(1)}{value}{m.group(3)}",
        text,
        count=1,
    )
    if count == 0:
        raise RuntimeError(f"cannot find <{tag}> in fpv_cam.sdf")
    return new_text, new_text != text


def update_fpv_camera_model(
    sdf_path: str, config: CameraConfig
) -> bool:
    with open(sdf_path, "r", encoding="utf-8") as f:
        text = f.read()

    changed = False
    hfov = 2.0 * math.atan(float(config.img_width) / (2.0 * config.fx))
    k1, k2, p1, p2, k3 = config.distortion

    for tag, value in [
        ("width", str(int(config.img_width))),
        ("height", str(int(config.img_height))),
        ("horizontal_fov", f"{hfov:.9f}"),
        ("CxPrime", f"{config.cx:.6f}"),
        ("Cx", f"{config.cx:.6f}"),
        ("Cy", f"{config.cy:.6f}"),
        ("focalLength", f"{config.fx:.6f}"),
        ("distortionK1", f"{k1:.12f}"),
        ("distortionK2", f"{k2:.12f}"),
        ("distortionK3", f"{k3:.12f}"),
        ("distortionT1", f"{p1:.12f}"),
        ("distortionT2", f"{p2:.12f}"),
    ]:
        updated_text, tag_changed = replace_tag(text, tag, value)
        text = updated_text
        changed = changed or tag_changed

    if config.fps is not None:
        for tag, value in [
            ("update_rate", f"{config.fps:.6f}"),
            # The Gazebo sensor already owns the configured frame rate.  A
            # second equal-rate gate in gazebo_ros_camera can skip frames when
            # sensor timestamps straddle its floating-point period boundary.
            # Zero disables the plugin-side throttle so every sensor frame is
            # forwarded to ROS.
            ("updateRate", "0.000000"),
        ]:
            updated_text, tag_changed = replace_tag(text, tag, value)
            text = updated_text
            changed = changed or tag_changed

    if changed:
        with open(sdf_path, "w", encoding="utf-8") as f:
            f.write(text)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync aircraft FPV camera pose and fpv_cam intrinsics from a camera YAML file"
    )
    parser.add_argument(
        "--config",
        default=os.path.join(params_root(), "camera/camera_params_usb_imx577_30degree.yaml"),
        help="Path to the shared camera YAML file",
    )
    parser.add_argument("--sdf", default=None, help="Optional explicit aircraft SDF path.")
    args = parser.parse_args()

    config = parse_camera_config(args.config)
    aircraft_sdf_path = resolve_aircraft_sdf_path(args.sdf, config.aircraft_sdf)
    if aircraft_sdf_path is None:
        print(
            "[sync_gazebo_camera_model] ERROR: cannot locate aircraft SDF. "
            "Install holydrone_sim or set camera.gazebo.aircraft_sdf.",
            file=sys.stderr,
        )
        return 2
    fpv_sdf_path = resolve_fpv_sdf_path(config.fpv_cam_sdf)
    if fpv_sdf_path is None:
        print(
            "[sync_gazebo_camera_model] ERROR: cannot locate fpv_cam.sdf. "
            "Install holydrone_sim or set camera.gazebo.fpv_cam_sdf.",
            file=sys.stderr,
        )
        return 2

    pose_changed = update_aircraft_camera_pose(
        aircraft_sdf_path, config.r_cam_body, config.position_body_m
    )
    camera_changed = update_fpv_camera_model(fpv_sdf_path, config)
    if pose_changed or camera_changed:
        print(
            f"[sync_gazebo_camera_model] updated aircraft pose + fpv camera model: "
            f"position_body_m={config.position_body_m if config.position_body_m is not None else 'keep'} "
            f"img={config.img_width}x{config.img_height} "
            f"fx={config.fx:.6f} fy={config.fy:.6f} "
            f"cx={config.cx:.6f} cy={config.cy:.6f} "
            f"fps={config.fps if config.fps is not None else 'keep'}\n"
            f"  aircraft.sdf: {aircraft_sdf_path}\n"
            f"  fpv_cam.sdf: {fpv_sdf_path}"
        )
    else:
        print(
            f"[sync_gazebo_camera_model] already up-to-date:\n"
            f"  aircraft.sdf: {aircraft_sdf_path}\n"
            f"  fpv_cam.sdf: {fpv_sdf_path}\n"
            f"position_body_m={config.position_body_m if config.position_body_m is not None else 'keep'} "
            f"img={config.img_width}x{config.img_height} "
            f"fx={config.fx:.6f} fy={config.fy:.6f} "
            f"cx={config.cx:.6f} cy={config.cy:.6f} "
            f"fps={config.fps if config.fps is not None else 'keep'}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
