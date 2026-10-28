#!/usr/bin/env bash

set -euo pipefail

PACKAGE_DIR="${HOLYDRONE_SIM_DIR:-}"
if [ -z "${PACKAGE_DIR}" ] && command -v rospack >/dev/null 2>&1; then
    PACKAGE_DIR="$(rospack find holydrone_sim 2>/dev/null || true)"
fi
PACKAGE_DIR="${PACKAGE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PX4_DIR="${PX4_DIR:-${1:-}}"
BUILD_PX4="${BUILD_PX4:-1}"
EXPECTED_COMMIT="54f0455ffcd755534539a7cf33a09a20bf71d29d"

if [ -z "${PX4_DIR}" ] || [ ! -d "${PX4_DIR}/ROMFS/px4fmu_common/init.d-posix/airframes" ]; then
    echo "Usage: PX4_DIR=/path/to/PX4-Autopilot $0" >&2
    exit 2
fi

actual_commit="$(git -C "${PX4_DIR}" rev-parse HEAD 2>/dev/null || true)"
if [ "${actual_commit}" != "${EXPECTED_COMMIT}" ]; then
    echo "WARNING: this overlay was validated against PX4 v1.16.2 (${EXPECTED_COMMIT})." >&2
    echo "         Current PX4 commit: ${actual_commit:-unknown}" >&2
fi

airframe_dir="${PX4_DIR}/ROMFS/px4fmu_common/init.d-posix/airframes"
airframe_src="${PACKAGE_DIR}/px4/overlay/ROMFS/px4fmu_common/init.d-posix/airframes/22000_gazebo-classic_holydrone"
airframe_dst="${airframe_dir}/22000_gazebo-classic_holydrone"
cmake_file="${airframe_dir}/CMakeLists.txt"

install -m 0755 "${airframe_src}" "${airframe_dst}"

if ! grep -qE '^[[:space:]]*22000_gazebo-classic_holydrone[[:space:]]*$' "${cmake_file}"; then
    cp -n "${cmake_file}" "${cmake_file}.pre-holydrone-sim.bak"
    python3 - "${cmake_file}" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
anchor = "\t71001_gazebo-classic_spacecraft_dart"
entry = "\t22000_gazebo-classic_holydrone\n"
legacy = re.compile(r"^[ \t]*22000_gazebo-classic_holydrone_cam[ \t]*$", re.MULTILINE)
if legacy.search(text):
    text = legacy.sub("\t22000_gazebo-classic_holydrone", text, count=1)
elif anchor in text:
    text = text.replace(anchor, entry + anchor, 1)
else:
    raise SystemExit(f"Cannot find insertion anchor in {path}")
path.write_text(text, encoding="utf-8")
PY
fi

echo "Installed PX4 airframe 22000 and registered it in ${cmake_file}."

if [ "${BUILD_PX4}" = "1" ]; then
    git -C "${PX4_DIR}" submodule update --init --recursive
    make -C "${PX4_DIR}" px4_sitl_default
    DONT_RUN=1 make -C "${PX4_DIR}" px4_sitl gazebo-classic
    echo "PX4 SITL build completed."
else
    echo "BUILD_PX4=0: skipped rebuilding PX4."
fi
