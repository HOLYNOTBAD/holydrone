#!/usr/bin/env bash

set -euo pipefail

PACKAGE_DIR="${HOLYDRONE_SIM_DIR:-}"
if [ -z "${PACKAGE_DIR}" ] && command -v rospack >/dev/null 2>&1; then
    PACKAGE_DIR="$(rospack find holydrone_sim 2>/dev/null || true)"
fi
PACKAGE_DIR="${PACKAGE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PX4_DIR="${PX4_DIR:-${1:-}}"

if [ -z "${PX4_DIR}" ]; then
    echo "Usage: PX4_DIR=/path/to/PX4-Autopilot $0" >&2
    exit 2
fi

PX4_BUILD_DIR="${PX4_BUILD_DIR:-${PX4_DIR}/build/px4_sitl_default}"
PX4_BIN="${PX4_BUILD_DIR}/bin/px4"
PX4_RUNTIME_DIR="${PX4_RUNTIME_DIR:-${PX4_BUILD_DIR}/rootfs_holydrone}"
PX4_SYS_AUTOSTART="${PX4_SYS_AUTOSTART:-22000}"
PX4_SIM_MODEL="${PX4_SIM_MODEL:-gazebo-classic_holydrone}"
PX4_RESET_PARAMS="${PX4_RESET_PARAMS:-0}"
WORLD="${HOLYDRONE_WORLD:-${PACKAGE_DIR}/gazebo/worlds/empty.world}"
MODEL="${HOLYDRONE_MODEL:-${PACKAGE_DIR}/gazebo/models/holydrone/holydrone.sdf}"
SPAWN_X="${SPAWN_X:-0}"
SPAWN_Y="${SPAWN_Y:-0}"
SPAWN_Z="${SPAWN_Z:-0.055}"
GAZEBO_GUI="${GAZEBO_GUI:-1}"
AUTO_TAKEOFF="${AUTO_TAKEOFF:-0}"
TAKEOFF_DELAY="${TAKEOFF_DELAY:-10}"
RUN_DURATION="${RUN_DURATION:-0}"
START_ROSCORE="${START_ROSCORE:-1}"

for required in "${PX4_BIN}" "${PX4_DIR}/Tools/simulation/gazebo-classic/setup_gazebo.bash" "${WORLD}" "${MODEL}"; do
    if [ ! -e "${required}" ]; then
        echo "Required file is missing: ${required}" >&2
        exit 1
    fi
done

ROS_DISTRO="${ROS_DISTRO:-noetic}"
set +u
[ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ] && source "/opt/ros/${ROS_DISTRO}/setup.bash"
[ -f "/usr/share/gazebo/setup.sh" ] && source "/usr/share/gazebo/setup.sh"
source "${PX4_DIR}/Tools/simulation/gazebo-classic/setup_gazebo.bash" "${PX4_DIR}" "${PX4_BUILD_DIR}"
set -u

export GAZEBO_MODEL_PATH="${PACKAGE_DIR}/gazebo/models:${GAZEBO_MODEL_PATH:-}"
export GAZEBO_PLUGIN_PATH="/opt/ros/${ROS_DISTRO}/lib:${GAZEBO_PLUGIN_PATH:-}"
export LD_LIBRARY_PATH="/opt/ros/${ROS_DISTRO}/lib:${LD_LIBRARY_PATH:-}"

ROSCORE_PID=""
GZSERVER_PID=""
GZCLIENT_PID=""
PX4_STARTED=0
PX4_PID=""

cleanup() {
    status=$?
    trap - EXIT INT TERM
    if [ "${PX4_STARTED}" = "1" ] && [ -x "${PX4_BUILD_DIR}/bin/px4-shutdown" ]; then
        (cd "${PX4_RUNTIME_DIR}" && "${PX4_BUILD_DIR}/bin/px4-shutdown") >/dev/null 2>&1 || true
    fi
    [ -z "${PX4_PID}" ] || kill "${PX4_PID}" >/dev/null 2>&1 || true
    [ -z "${GZCLIENT_PID}" ] || kill "${GZCLIENT_PID}" >/dev/null 2>&1 || true
    [ -z "${GZSERVER_PID}" ] || kill "${GZSERVER_PID}" >/dev/null 2>&1 || true
    [ -z "${ROSCORE_PID}" ] || kill "${ROSCORE_PID}" >/dev/null 2>&1 || true
    exit "${status}"
}
trap cleanup EXIT INT TERM

if [ "${START_ROSCORE}" = "1" ] && ! rostopic list >/dev/null 2>&1; then
    roscore >"${TMPDIR:-/tmp}/holydrone_sim_roscore.log" 2>&1 &
    ROSCORE_PID=$!
    for _ in $(seq 1 50); do
        rostopic list >/dev/null 2>&1 && break
        sleep 0.2
    done
fi

gzserver --verbose -s libgazebo_ros_api_plugin.so "${WORLD}" &
GZSERVER_PID=$!
for _ in $(seq 1 60); do
    gz model --list >/dev/null 2>&1 && break
    sleep 0.25
done
if ! kill -0 "${GZSERVER_PID}" >/dev/null 2>&1; then
    echo "gzserver exited before the world became ready." >&2
    exit 1
fi

if [ "${GAZEBO_GUI}" = "1" ] && [ -n "${DISPLAY:-}" ]; then
    gzclient &
    GZCLIENT_PID=$!
fi

gz model --spawn-file "${MODEL}" --model-name holydrone \
    -x "${SPAWN_X}" -y "${SPAWN_Y}" -z "${SPAWN_Z}"

mkdir -p "${PX4_RUNTIME_DIR}"
if [ "${PX4_RESET_PARAMS}" = "1" ]; then
    rm -f "${PX4_RUNTIME_DIR}/parameters.bson" "${PX4_RUNTIME_DIR}/parameters_backup.bson"
fi

(cd "${PX4_RUNTIME_DIR}" && \
    env PX4_SYS_AUTOSTART="${PX4_SYS_AUTOSTART}" PX4_SIM_MODEL="${PX4_SIM_MODEL}" \
    "${PX4_BIN}" -d "${PX4_BUILD_DIR}/etc") &
PX4_PID=$!
PX4_STARTED=1
sleep 2
if ! kill -0 "${PX4_PID}" >/dev/null 2>&1; then
    echo "PX4 SITL exited during startup." >&2
    exit 1
fi

echo "Holydrone Gazebo + PX4 SITL is running."
echo "PX4_SYS_AUTOSTART=${PX4_SYS_AUTOSTART}; model=holydrone"

if [ "${AUTO_TAKEOFF}" = "1" ]; then
    sleep "${TAKEOFF_DELAY}"
    (cd "${PX4_RUNTIME_DIR}" && "${PX4_BUILD_DIR}/bin/px4-commander" arm)
    sleep 1
    (cd "${PX4_RUNTIME_DIR}" && "${PX4_BUILD_DIR}/bin/px4-commander" takeoff)
    echo "Automatic takeoff command sent."
fi

if [ "${RUN_DURATION}" != "0" ]; then
    sleep "${RUN_DURATION}"
else
    wait "${GZSERVER_PID}"
fi
