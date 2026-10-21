from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    ld = []

    declare_kp_arg = DeclareLaunchArgument(
        'kp',
        default_value='1.0',
        description='Proportional gain for turtle controller'
    )

    kp_arg = LaunchConfiguration('kp')

    turtle_sim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='my_turtlesim',
        output='screen'
    )

    turtle_controller_node = Node(
        package='turtle_ctrl',
        executable='turtle_controller',
        name='turtle_controller',
        output='screen',
        parameters=[{'kp': kp_arg}]
    )
    
    ld.append(declare_kp_arg)
    ld.append(turtle_sim_node)
    ld.append(turtle_controller_node)
    return LaunchDescription(ld)