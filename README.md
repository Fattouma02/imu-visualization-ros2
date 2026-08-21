# imu-visualization-ros2

ROS 2 Humble workspace that subscribes to live BNO055 IMU orientation data
and visualizes it on a 3D cube in RViz2, using a TF broadcaster and a
URDF-defined mesh rendered via `robot_state_publisher`.

## Part of a larger project

This is the visualization/host-side half of an autonomous robotized vehicle
project (obstacle avoidance, perception, trajectory planning, 25 km/h
target speed). Two-board architecture:

- **STM32F401RE Nucleo** — real-time IMU reading and low-level control,
  FreeRTOS + micro-ROS
- **Jetson Nano** — high-level perception/decision-making, ROS 2 Humble
  (this package will eventually run here)

**Companion repo:** [micro-ROS-STM32-BNO055-IMU](https://github.com/Fattouma02/micro-ROS-STM32-BNO055-IMU)
— the STM32 firmware that reads the BNO055 over I2C and publishes
`sensor_msgs/msg/Imu` on `/imu/data` via micro-ROS. This workspace consumes
that topic.

## Architecture

- `tf2_broadcaster.py` — subscribes to `/imu/data`, broadcasts
  `reference_link → imu_link` transform live from the IMU quaternion
- `urdf/imu_cube.urdf.xacro` — defines the cube geometry, rendered by
  `robot_state_publisher`
- `launch/` — brings up `robot_state_publisher` + RViz2

## Status

- ✅ Full pipeline confirmed working: micro-ROS agent → `tf2_broadcaster` →
  TF → `robot_state_publisher` → RViz2. Rotating the physical IMU rotates
  the cube live in RViz2.