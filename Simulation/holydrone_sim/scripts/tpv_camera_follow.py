#!/usr/bin/env python3

import math

import rospy
from gazebo_msgs.msg import ModelState, ModelStates
from gazebo_msgs.srv import SetModelState
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class TpvCameraFollower:
    def __init__(self):
        self.target_model = rospy.get_param("~target_model", "holydrone")
        self.camera_model = rospy.get_param("~camera_model", "tpv_cam")
        self.offset_x = rospy.get_param("~offset_x", -4.0)
        self.offset_y = rospy.get_param("~offset_y", 0.0)
        self.offset_z = rospy.get_param("~offset_z", 2.0)
        self.look_at_z = rospy.get_param("~look_at_z", 0.0)
        self.position_alpha = rospy.get_param("~position_alpha", rospy.get_param("~alpha", 0.04))
        self.attitude_alpha = rospy.get_param("~attitude_alpha", 0.08)
        self.rate_hz = rospy.get_param("~rate", 15.0)

        self.target_pose = None
        self.camera_ready = False
        self.smoothed = None

        rospy.wait_for_service("/gazebo/set_model_state")
        self.set_model_state = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)
        self.model_states_sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.model_states_cb, queue_size=1)

    def model_states_cb(self, msg):
        try:
            idx = msg.name.index(self.target_model)
        except ValueError:
            self.target_pose = None
            self.camera_ready = self.camera_model in msg.name
            return
        self.target_pose = msg.pose[idx]
        self.camera_ready = self.camera_model in msg.name

    @staticmethod
    def lerp_angle(a, b, alpha):
        delta = math.atan2(math.sin(b - a), math.cos(b - a))
        return a + alpha * delta

    def desired_state(self):
        if self.target_pose is None:
            return None

        q = self.target_pose.orientation
        _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)

        x = self.target_pose.position.x + cos_yaw * self.offset_x - sin_yaw * self.offset_y
        y = self.target_pose.position.y + sin_yaw * self.offset_x + cos_yaw * self.offset_y
        z = self.target_pose.position.z + self.offset_z

        target_x = self.target_pose.position.x
        target_y = self.target_pose.position.y
        target_z = self.target_pose.position.z + self.look_at_z

        look_dx = target_x - x
        look_dy = target_y - y
        look_dz = target_z - z
        look_yaw = math.atan2(look_dy, look_dx)
        look_pitch = -math.atan2(look_dz, math.hypot(look_dx, look_dy))

        if self.smoothed is None:
            self.smoothed = [x, y, z, look_yaw, look_pitch]
        else:
            self.smoothed[0] += self.position_alpha * (x - self.smoothed[0])
            self.smoothed[1] += self.position_alpha * (y - self.smoothed[1])
            self.smoothed[2] += self.position_alpha * (z - self.smoothed[2])

            target_x = self.target_pose.position.x
            target_y = self.target_pose.position.y
            target_z = self.target_pose.position.z + self.look_at_z
            look_dx = target_x - self.smoothed[0]
            look_dy = target_y - self.smoothed[1]
            look_dz = target_z - self.smoothed[2]
            look_yaw = math.atan2(look_dy, look_dx)
            look_pitch = -math.atan2(look_dz, math.hypot(look_dx, look_dy))
            self.smoothed[3] = self.lerp_angle(self.smoothed[3], look_yaw, self.attitude_alpha)
            self.smoothed[4] = self.lerp_angle(self.smoothed[4], look_pitch, self.attitude_alpha)

        state = ModelState()
        state.model_name = self.camera_model
        state.reference_frame = "world"
        state.pose.position.x = self.smoothed[0]
        state.pose.position.y = self.smoothed[1]
        state.pose.position.z = self.smoothed[2]
        qx, qy, qz, qw = quaternion_from_euler(0.0, self.smoothed[4], self.smoothed[3])
        state.pose.orientation.x = qx
        state.pose.orientation.y = qy
        state.pose.orientation.z = qz
        state.pose.orientation.w = qw
        return state

    def spin(self):
        rate = rospy.Rate(self.rate_hz)
        while not rospy.is_shutdown():
            if not self.camera_ready:
                rospy.logwarn_throttle(
                    2.0,
                    "Waiting for TPV camera model '%s' in Gazebo.",
                    self.camera_model,
                )
                rate.sleep()
                continue
            state = self.desired_state()
            if state is not None:
                try:
                    self.set_model_state(state)
                except rospy.ServiceException as exc:
                    rospy.logwarn_throttle(2.0, "Failed to update TPV camera pose: %s", exc)
            rate.sleep()


if __name__ == "__main__":
    rospy.init_node("tpv_camera_follow")
    TpvCameraFollower().spin()
