# holydrone_sim

`holydrone_sim` is a ROS 1 package containing the portable Gazebo Classic
model, PX4 SITL airframe overlay, camera calibration helpers, visualization
nodes, and the ISB-NMPC Holydrone controller profiles.

## Package contents

| Path | Purpose |
| --- | --- |
| `gazebo/models/holydrone` | Airframe SDF and Git LFS-managed body/propeller meshes |
| `gazebo/models/{gps,lidar,fpv_cam}` | Sensor submodels required by the airframe SDF |
| `gazebo/models/tpv_cam` | Optional third-person Gazebo camera |
| `px4/overlay` | Backed-up PX4 `22000` airframe using the original PX4 source-tree layout |
| `camera` | Camera intrinsics/extrinsics accepted by the model synchronizer |
| `control_interception/holydrone` | Optional simulation and real-flight ISB-NMPC profiles |
| `scripts` | PX4 installer, dependency checker, SITL runner and visualization helpers |

The supported baseline is recorded in [`px4/VERSION.md`](px4/VERSION.md).
The package does not redistribute compiled PX4/Gazebo plugins because they are
ABI-dependent; they are built from the pinned PX4 source instead.

## Add to a catkin workspace

The package may be linked into any ROS Noetic workspace:

```bash
mkdir -p ~/catkin_ws/src
ln -s ~/holydrone/Simulation/holydrone_sim ~/catkin_ws/src/holydrone_sim
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
source devel/setup.bash
```

Check the package and a prepared PX4 tree with:

```bash
PX4_DIR=~/PX4-Autopilot rosrun holydrone_sim check_install.sh
```

## Utilities

Synchronize the bundled SDF camera pose and intrinsics from a calibration:

```bash
rosrun holydrone_sim sync_gazebo_camera_model.py \
  --config "$(rospack find holydrone_sim)/camera/camera_params_usb_imx577_30degree.yaml"
```

Start only Gazebo and spawn the model (PX4 is not started by this launch file):

```bash
source "$(rospack find holydrone_sim)/scripts/setup_env.sh"
roslaunch holydrone_sim spawn.launch
```

Start optional marker and third-person-camera nodes:

```bash
roslaunch holydrone_sim visualization.launch
roslaunch holydrone_sim tpv_camera.launch
```

Full PX4 deployment and automatic-takeoff instructions are intentionally kept
at the bottom of the repository root `README.md` so a fresh clone has one
authoritative procedure.
