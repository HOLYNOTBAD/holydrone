# PX4 compatibility snapshot

The Holydrone overlay was extracted from and validated against:

- PX4-Autopilot tag: `v1.16.2`
- PX4-Autopilot commit: `54f0455ffcd755534539a7cf33a09a20bf71d29d`
- PX4-SITL_gazebo-classic submodule commit: `70683dc759cbd3ebccfa78429b564f8b1fb5d149`
- Gazebo Classic: 11
- ROS: Noetic
- Ubuntu: 20.04

The backed-up overlay contains the custom `22000` airframe. The Gazebo models,
including the PX4 lidar model, live under `gazebo/models` in this ROS package so
they can be resolved through `GAZEBO_MODEL_PATH` without modifying the PX4
Gazebo submodule.
