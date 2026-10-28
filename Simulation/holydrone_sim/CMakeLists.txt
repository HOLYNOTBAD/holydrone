cmake_minimum_required(VERSION 3.0.2)
project(holydrone_sim)

find_package(catkin REQUIRED)
catkin_package()

if(CATKIN_ENABLE_TESTING)
  catkin_add_nosetests(test/test_package.py)
endif()

catkin_install_python(PROGRAMS
  scripts/camera_frustum_marker.py
  scripts/sync_gazebo_camera_model.py
  scripts/tpv_camera_follow.py
  scripts/uav_mesh_marker.py
  scripts/world_map_alignment_tf.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(PROGRAMS
  scripts/check_install.sh
  scripts/install_px4_overlay.sh
  scripts/run_sitl.sh
  scripts/setup_env.sh
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY
  aircraft
  camera
  control_interception
  gazebo
  launch
  px4
  rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(FILES README.md THIRD_PARTY.md DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
