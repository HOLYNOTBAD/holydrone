#!/usr/bin/env python3

"""Align the controller's map frame with the Gazebo world frame in RViz.

The transform is calibrated while the vehicle is stationary and then locked.
Recomputing it continuously from two unsynchronised pose streams makes the
fixed Gazebo scene move by the pose noise and transport delay seen between the
streams.
"""

import numpy as np
import rospy
import tf2_ros
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import PointStamped, TransformStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler


def pose_xyzyaw(pose):
    q = pose.orientation
    yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])[2]
    return np.array([pose.position.x, pose.position.y, pose.position.z]), yaw


class WorldMapAlignment:
    def __init__(self):
        self.model_name = rospy.get_param("~model_name", "holydrone")
        self.world_frame = rospy.get_param("~world_frame", "world")
        self.map_frame = rospy.get_param("~map_frame", "map")
        self.calibration_samples = max(
            1, int(rospy.get_param("~calibration_samples", 5))
        )
        self.calibration_max_speed = max(
            0.0, float(rospy.get_param("~calibration_max_speed", 0.2))
        )
        self.max_input_age = max(
            0.02, float(rospy.get_param("~max_input_age", 0.2))
        )
        self.world_uav = None
        self.map_uav = None
        self.map_speed = float("inf")
        self.world_received_at = rospy.Time(0)
        self.map_received_at = rospy.Time(0)
        self.world_sequence = 0
        self.map_sequence = 0
        self.last_sample_sequences = (-1, -1)
        self.candidates = []
        self.calibrated = False
        self.broadcaster = tf2_ros.StaticTransformBroadcaster()
        rospy.Subscriber(
            rospy.get_param("~model_states_topic", "/gazebo/model_states"),
            ModelStates,
            self.model_states_callback,
            queue_size=1,
        )
        rospy.Subscriber(
            rospy.get_param("~uav_state_topic", "/nmpc/uavStateEstimate"),
            Odometry,
            self.uav_state_callback,
            queue_size=10,
        )
        rospy.Subscriber(
            rospy.get_param("~local_origin_topic", "/local_frame/origin"),
            PointStamped,
            self.local_origin_callback,
            queue_size=1,
        )
        self.timer = rospy.Timer(rospy.Duration(0.02), self.publish_transform)

    def model_states_callback(self, msg):
        try:
            index = msg.name.index(self.model_name)
        except ValueError:
            rospy.logwarn_throttle(
                2.0, "world_map_alignment_tf: model '%s' not found" % self.model_name
            )
            return
        self.world_uav = pose_xyzyaw(msg.pose[index])
        self.world_received_at = rospy.Time.now()
        self.world_sequence += 1

    def uav_state_callback(self, msg):
        self.map_uav = pose_xyzyaw(msg.pose.pose)
        velocity = msg.twist.twist.linear
        self.map_speed = np.linalg.norm([velocity.x, velocity.y, velocity.z])
        self.map_received_at = rospy.Time.now()
        self.map_sequence += 1

    def local_origin_callback(self, _msg):
        # The FSM may redefine map when the operator confirms takeoff. Any
        # calibration made before that event is stale, even if the vehicle has
        # barely moved, so explicitly collect and publish a replacement.
        self.candidates.clear()
        self.last_sample_sequences = (self.world_sequence, self.map_sequence)
        self.calibrated = False
        rospy.loginfo("world_map_alignment_tf: local origin changed; recalibrating")

    def publish_transform(self, _event):
        if self.calibrated or self.world_uav is None or self.map_uav is None:
            return

        now = rospy.Time.now()
        if (
            (now - self.world_received_at).to_sec() > self.max_input_age
            or (now - self.map_received_at).to_sec() > self.max_input_age
            or self.map_speed > self.calibration_max_speed
        ):
            self.candidates.clear()
            return

        sequences = (self.world_sequence, self.map_sequence)
        if (
            sequences[0] <= self.last_sample_sequences[0]
            or sequences[1] <= self.last_sample_sequences[1]
        ):
            return
        self.last_sample_sequences = sequences

        # Frames differ only by a fixed ENU translation and yaw. Taking a
        # short stationary sample rejects callback skew without injecting
        # vehicle roll/pitch or estimator noise into the global RViz frame.
        world_position, world_yaw = self.world_uav
        map_position, map_yaw = self.map_uav
        yaw = world_yaw - map_yaw
        cos_yaw = np.cos(yaw)
        sin_yaw = np.sin(yaw)
        rotation = np.array(
            [[cos_yaw, -sin_yaw, 0.0], [sin_yaw, cos_yaw, 0.0], [0.0, 0.0, 1.0]]
        )
        translation = world_position - rotation @ map_position
        self.candidates.append((translation, yaw))
        if len(self.candidates) < self.calibration_samples:
            return

        translations = np.asarray([item[0] for item in self.candidates])
        translation = np.median(translations, axis=0)
        yaws = np.asarray([item[1] for item in self.candidates])
        yaw = np.arctan2(np.mean(np.sin(yaws)), np.mean(np.cos(yaws)))
        quaternion = quaternion_from_euler(0.0, 0.0, yaw)

        transform = TransformStamped()
        transform.header.stamp = now
        transform.header.frame_id = self.world_frame
        transform.child_frame_id = self.map_frame
        transform.transform.translation.x = float(translation[0])
        transform.transform.translation.y = float(translation[1])
        transform.transform.translation.z = float(translation[2])
        transform.transform.rotation.x = quaternion[0]
        transform.transform.rotation.y = quaternion[1]
        transform.transform.rotation.z = quaternion[2]
        transform.transform.rotation.w = quaternion[3]
        self.broadcaster.sendTransform(transform)
        self.calibrated = True
        rospy.loginfo(
            "world_map_alignment_tf: locked world -> map at "
            "translation [%.3f %.3f %.3f], yaw %.3f rad from %d stationary samples",
            translation[0],
            translation[1],
            translation[2],
            yaw,
            len(self.candidates),
        )


if __name__ == "__main__":
    rospy.init_node("world_map_alignment_tf")
    WorldMapAlignment()
    rospy.spin()
