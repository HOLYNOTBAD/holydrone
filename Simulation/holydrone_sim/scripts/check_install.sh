#!/usr/bin/env bash

set -euo pipefail

PACKAGE_DIR="${HOLYDRONE_SIM_DIR:-}"
if [ -z "${PACKAGE_DIR}" ] && command -v rospack >/dev/null 2>&1; then
    PACKAGE_DIR="$(rospack find holydrone_sim 2>/dev/null || true)"
fi
PACKAGE_DIR="${PACKAGE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PX4_DIR="${PX4_DIR:-${1:-}}"
failed=0

check_file() {
    if [ -f "$1" ]; then
        printf '[ok] %s\n' "$1"
    else
        printf '[missing] %s\n' "$1" >&2
        failed=1
    fi
}

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        printf '[ok] command: %s\n' "$1"
    else
        printf '[missing] command: %s\n' "$1" >&2
        failed=1
    fi
}

check_command gzserver
check_command gz
check_command roscore
check_file "${PACKAGE_DIR}/gazebo/models/holydrone/holydrone.sdf"
check_file "${PACKAGE_DIR}/gazebo/models/holydrone/meshes/holydrone_v1.STL"
check_file "${PACKAGE_DIR}/gazebo/models/holydrone/meshes/Propeller 7inch.STL"
check_file "${PACKAGE_DIR}/gazebo/models/fpv_cam/fpv_cam.sdf"
check_file "${PACKAGE_DIR}/gazebo/models/gps/gps.sdf"
check_file "${PACKAGE_DIR}/gazebo/models/lidar/model.sdf"

if [ -z "${PX4_DIR}" ]; then
    printf '[missing] PX4_DIR is not set\n' >&2
    failed=1
else
    PX4_BUILD_DIR="${PX4_BUILD_DIR:-${PX4_DIR}/build/px4_sitl_default}"
    check_file "${PX4_DIR}/Tools/simulation/gazebo-classic/setup_gazebo.bash"
    check_file "${PX4_BUILD_DIR}/bin/px4"
    check_file "${PX4_BUILD_DIR}/build_gazebo-classic/libgazebo_mavlink_interface.so"
    check_file "${PX4_BUILD_DIR}/etc/init.d-posix/airframes/22000_gazebo-classic_holydrone"
fi

if [ "${failed}" -ne 0 ]; then
    printf '\nHolydrone simulation prerequisites are incomplete.\n' >&2
    exit 1
fi

printf '\nHolydrone simulation prerequisites are ready.\n'
