from setuptools import find_packages, setup

package_name = 'imu_visualization'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', ['urdf/imu_cube.urdf.xacro']),
        ('share/' + package_name + '/launch', ['launch/test_rsp.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fatma',
    maintainer_email='fatma.mrabet.fatma@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tf2_broadcaster = imu_visualization.tf2_broadcaster:main',
        ],
    },
)
