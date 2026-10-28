#!/usr/bin/env bash

# Source this file before using Gazebo directly. A catkin workspace that
# contains holydrone_sim exposes the same package path through rospack.
_HOLYDRONE_SETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export HOLYDRONE_SIM_DIR="${_HOLYDRONE_SETUP_DIR}"
export GAZEBO_MODEL_PATH="${HOLYDRONE_SIM_DIR}/gazebo/models:${GAZEBO_MODEL_PATH:-}"
export HOLYDRONE_PX4_BASE_COMMIT="54f0455ffcd755534539a7cf33a09a20bf71d29d"
unset _HOLYDRONE_SETUP_DIR
