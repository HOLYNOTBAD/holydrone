#!/usr/bin/env python3

import copy
import math

import rospy
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker


class UavMeshMarkerNode:
    def __init__(self):
        self.state_topic = rospy.get_param("~state_topic", "/nmpc/uavStateEstimate")
        self.marker_topic = rospy.get_param("~marker_topic", "/rviz/uav_mesh")
        self.mesh_resource = rospy.get_param(
            "~mesh_resource",
            "package://holydrone_sim/gazebo/models/holydrone/meshes/holydrone_v1.STL",
        )
        self.frame_id = rospy.get_param("~frame_id", "")
        self.gazebo_model_states_topic = rospy.get_param(
            "~gazebo_model_states_topic", ""
        )
        self.gazebo_model_name = rospy.get_param("~gazebo_model_name", "holydrone")
        self.scale = float(rospy.get_param("~scale", 0.001))
        self.alpha = float(rospy.get_param("~alpha", 1.0))
        mesh_roll = float(rospy.get_param("~mesh_roll", 0.0))
        mesh_pitch = float(rospy.get_param("~mesh_pitch", 0.0))
        mesh_yaw = float(rospy.get_param("~mesh_yaw", 0.0))
        self.mesh_rotation = self.quaternion_from_rpy(
            mesh_roll, mesh_pitch, mesh_yaw
        )

        self.publisher = rospy.Publisher(self.marker_topic, Marker, queue_size=1)
        if self.gazebo_model_states_topic:
            rospy.Subscriber(
                self.gazebo_model_states_topic,
                ModelStates,
                self.gazebo_state_callback,
                queue_size=1,
            )
        else:
            rospy.Subscriber(self.state_topic, Odometry, self.state_callback, queue_size=20)

    @staticmethod
    def quaternion_from_rpy(roll, pitch, yaw):
        cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
        cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
        cy, sy = math.cos(yaw * 0.5), math.sin(yaw * 0.5)
        return (
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy,
        )

    @staticmethod
    def multiply_quaternions(left, right):
        lx, ly, lz, lw = left
        rx, ry, rz, rw = right
        return (
            lw * rx + lx * rw + ly * rz - lz * ry,
            lw * ry - lx * rz + ly * rw + lz * rx,
            lw * rz + lx * ry - ly * rx + lz * rw,
            lw * rw - lx * rx - ly * ry - lz * rz,
        )

    def publish_marker(self, pose, stamp, frame_id):
        marker = Marker()
        marker.header.stamp = stamp if stamp != rospy.Time() else rospy.Time.now()
        marker.header.frame_id = self.frame_id or frame_id or "world"
        marker.ns = "uav"
        marker.id = 0
        marker.type = Marker.MESH_RESOURCE
        marker.action = Marker.ADD
        marker.pose = copy.deepcopy(pose)
        vehicle_rotation = (
            pose.orientation.x,
            pose.orientation.y,
            pose.orientation.z,
            pose.orientation.w,
        )
        rotation = self.multiply_quaternions(
            vehicle_rotation, self.mesh_rotation
        )
        marker.pose.orientation.x = rotation[0]
        marker.pose.orientation.y = rotation[1]
        marker.pose.orientation.z = rotation[2]
        marker.pose.orientation.w = rotation[3]
        marker.scale.x = self.scale
        marker.scale.y = self.scale
        marker.scale.z = self.scale
        marker.color.r = 0.1
        marker.color.g = 0.35
        marker.color.b = 1.0
        marker.color.a = self.alpha
        marker.mesh_resource = self.mesh_resource
        marker.mesh_use_embedded_materials = False
        marker.lifetime = rospy.Duration(0.25)
        self.publisher.publish(marker)

    def state_callback(self, msg):
        self.publish_marker(msg.pose.pose, msg.header.stamp, msg.header.frame_id)

    def gazebo_state_callback(self, msg):
        try:
            index = msg.name.index(self.gazebo_model_name)
        except ValueError:
            rospy.logwarn_throttle(
                2.0,
                "uav_mesh_marker: Gazebo model '%s' is unavailable"
                % self.gazebo_model_name,
            )
            return
        self.publish_marker(msg.pose[index], rospy.Time.now(), "world")


if __name__ == "__main__":
    rospy.init_node("uav_mesh_marker")
    UavMeshMarkerNode()
    rospy.spin()
