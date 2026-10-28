#!/usr/bin/env python3

import copy
import math

import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker


class CameraFrustumMarkerNode:
    """Draw the calibrated onboard camera frustum in the vehicle body frame."""

    def __init__(self):
        self.state_topic = rospy.get_param("~state_topic", "/nmpc/uavStateEstimate")
        self.marker_topic = rospy.get_param(
            "~marker_topic", "/rviz/camera_frustum"
        )
        self.frame_id = rospy.get_param("~frame_id", "")
        self.gazebo_model_states_topic = rospy.get_param(
            "~gazebo_model_states_topic", ""
        )
        self.gazebo_model_name = rospy.get_param(
            "~gazebo_model_name", "holydrone"
        )
        self.depth = float(rospy.get_param("~depth", 8.0))
        self.line_width = float(rospy.get_param("~line_width", 0.04))

        camera = rospy.get_param("~camera")
        self.width = self._positive(camera, "img_width")
        self.height = self._positive(camera, "img_height")
        self.fx = self._positive(camera, "fx", camera.get("img_f"))
        self.fy = self._positive(camera, "fy", camera.get("img_f"))
        self.cx = float(camera.get("cx", self.width * 0.5))
        self.cy = float(camera.get("cy", self.height * 0.5))

        rotation = camera.get("R_cam_body")
        if not isinstance(rotation, list) or len(rotation) != 9:
            raise rospy.ROSInitException(
                "~camera/R_cam_body must contain 9 row-major values"
            )
        self.rotation = [float(value) for value in rotation]
        position = camera.get("position_body_m", camera.get("p_B_C", [0, 0, 0]))
        if not isinstance(position, list) or len(position) != 3:
            raise rospy.ROSInitException(
                "~camera/position_body_m (or p_B_C) must contain 3 values"
            )
        self.origin = [float(value) for value in position]

        if self.depth <= 0.0 or self.line_width <= 0.0:
            raise rospy.ROSInitException("~depth and ~line_width must be positive")

        self.frustum_points = self._make_frustum_points()
        self.publisher = rospy.Publisher(
            self.marker_topic, Marker, queue_size=1, latch=True
        )
        if self.gazebo_model_states_topic:
            rospy.Subscriber(
                self.gazebo_model_states_topic,
                ModelStates,
                self.gazebo_state_callback,
                queue_size=1,
            )
        else:
            rospy.Subscriber(
                self.state_topic, Odometry, self.state_callback, queue_size=20
            )

    @staticmethod
    def _positive(mapping, key, fallback=None):
        value = mapping.get(key, fallback)
        try:
            result = float(value)
        except (TypeError, ValueError):
            raise rospy.ROSInitException("~camera/{} must be numeric".format(key))
        if not math.isfinite(result) or result <= 0.0:
            raise rospy.ROSInitException("~camera/{} must be positive".format(key))
        return result

    def _camera_to_body(self, point):
        x, y, z = point
        r = self.rotation
        return Point(
            self.origin[0] + r[0] * x + r[1] * y + r[2] * z,
            self.origin[1] + r[3] * x + r[4] * y + r[5] * z,
            self.origin[2] + r[6] * x + r[7] * y + r[8] * z,
        )

    def _make_frustum_points(self):
        corners = []
        for u, v in (
            (0.0, 0.0),
            (self.width, 0.0),
            (self.width, self.height),
            (0.0, self.height),
        ):
            corners.append(
                self._camera_to_body(
                    (
                        (u - self.cx) * self.depth / self.fx,
                        (v - self.cy) * self.depth / self.fy,
                        self.depth,
                    )
                )
            )

        origin = Point(*self.origin)
        points = []
        for corner in corners:
            points.extend((copy.deepcopy(origin), copy.deepcopy(corner)))
        for index in range(4):
            points.extend(
                (
                    copy.deepcopy(corners[index]),
                    copy.deepcopy(corners[(index + 1) % 4]),
                )
            )
        return points

    def publish_marker(self, pose, stamp, frame_id):
        marker = Marker()
        marker.header.stamp = stamp if stamp != rospy.Time() else rospy.Time.now()
        marker.header.frame_id = self.frame_id or frame_id or "world"
        marker.ns = "camera_frustum"
        marker.id = 0
        marker.type = Marker.LINE_LIST
        marker.action = Marker.ADD
        marker.pose = copy.deepcopy(pose)
        marker.scale.x = self.line_width
        marker.color.r = 0.0
        marker.color.g = 0.9
        marker.color.b = 1.0
        marker.color.a = 0.9
        marker.points = self.frustum_points
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
                "camera_frustum_marker: Gazebo model '%s' is unavailable"
                % self.gazebo_model_name,
            )
            return
        self.publish_marker(msg.pose[index], rospy.Time.now(), "world")


if __name__ == "__main__":
    rospy.init_node("camera_frustum_marker")
    CameraFrustumMarkerNode()
    rospy.spin()
