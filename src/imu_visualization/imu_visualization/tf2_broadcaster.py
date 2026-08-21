#!/usr/bin/env python3
"""
tf2_broadcaster.py

Subscribes to /imu/data (sensor_msgs/msg/Imu) and broadcasts a live
TransformStamped from 'reference_link' to 'imu_link', using the IMU's
orientation quaternion directly as the transform's rotation.

This is an orientation-only demo: translation is always zero. The cube
geometry itself (visual box) is defined separately in the package's URDF
(urdf/imu_cube.urdf.xacro) and rendered by robot_state_publisher; this node
only supplies the live rotation on top of it via TF.
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Imu
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class ImuTf2Broadcaster(Node):
    """
    Listens to /imu/data and re-publishes the orientation as a TF transform
    from reference_link (fixed) to imu_link (moving), once per received
    IMU message.
    """

    def __init__(self):
        super().__init__('imu_tf2_broadcaster')

        # Standard QoS for a typical sensor_msgs/Imu publisher: reliable
        # delivery, volatile durability (no need to replay old samples to
        # late subscribers), small queue depth since this is a live stream.
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )

        # TransformBroadcaster handles publishing to /tf under the hood —
        # no need to manually create a publisher for it.
        self.tf_broadcaster = TransformBroadcaster(self)

        self.subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            qos_profile,
        )

        self.get_logger().info(
            'imu_tf2_broadcaster started: /imu/data -> TF(reference_link -> imu_link)'
        )

    def imu_callback(self, msg: Imu):
        """
        Called once per incoming IMU message. Builds and broadcasts a
        TransformStamped representing the current orientation of imu_link
        relative to reference_link.
        """
        t = TransformStamped()

        # Use the current wall/ROS time for the stamp rather than
        # msg.header.stamp. The upstream micro-ROS -> STM32 timestamp isn't
        # guaranteed to be properly synced with the host clock yet, so
        # trusting it here could cause TF extrapolation warnings or stale
        # lookups in RViz2. Stamping with now() guarantees a monotonically
        # increasing, host-consistent time for every broadcast.
        t.header.stamp = self.get_clock().now().to_msg()

        # Fixed parent frame (reference_link) -> moving child frame
        # (imu_link). This must match the link names used in
        # urdf/imu_cube.urdf.xacro exactly, or RViz2/TF won't connect them.
        t.header.frame_id = 'reference_link'
        t.child_frame_id = 'imu_link'

        # Translation is fixed at the origin: this demo only visualizes
        # orientation, not position. Integrating linear_acceleration into a
        # position estimate would drift almost immediately (open-loop
        # double integration) and is out of scope here.
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        # Rotation copied directly from the IMU's orientation quaternion,
        # with no normalization or axis remapping applied here. Any
        # correction for frame-convention mismatches (BNO055 axis mapping
        # vs. REP-103) will be handled as a separate, explicit step after
        # visually verifying rotation behavior in RViz2 — not silently
        # baked into this node.
        t.transform.rotation.x = msg.orientation.x
        t.transform.rotation.y = msg.orientation.y
        t.transform.rotation.z = msg.orientation.z
        t.transform.rotation.w = msg.orientation.w

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = ImuTf2Broadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
