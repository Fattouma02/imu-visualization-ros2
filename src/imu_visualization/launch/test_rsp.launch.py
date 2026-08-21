"""
test_rsp.launch.py

Minimal launch file to start robot_state_publisher, loading
urdf/imu_cube.urdf.xacro via Python (xacro.process_file), avoiding the
shell-quoting/newline issues that break passing raw XML through a
'-p robot_description:=...' command-line override.

This is a standalone diagnostic step: it only starts robot_state_publisher.
Run your tf2_broadcaster node and rviz2 separately alongside this, same as
before. Once this is confirmed working, this will be folded into the full
display.launch.py that brings up everything in one command.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg_share = get_package_share_directory('imu_visualization')
    xacro_file = os.path.join(pkg_share, 'urdf', 'imu_cube.urdf.xacro')

    # Process the xacro file directly in Python and extract the resulting
    # URDF as a plain string. This is passed to robot_state_publisher as a
    # normal Python dict value -- no shell involved, so no quoting or
    # newline-handling issues like the CLI approach had.
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = robot_description_config.toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

    return LaunchDescription([
        robot_state_publisher_node,
    ])