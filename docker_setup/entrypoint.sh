#!/bin/bash
# entrypoint.sh
#
# This is the script that runs when the container starts.
# For this basic tutorial, we just print a message and then
# keep the container alive forever so you can exec into it,
# poke around, and see how things work.

echo "Container is up and running!"
echo "Try: docker exec -it ros_test_container bash"

cd /home/marsrover/ros_ws
source /opt/ros/humble/setup.bash
colcon build

# 'tail -f /dev/null' watches an empty, never-ending file.
# Since /dev/null never produces new data and never closes,
# this command never exits — which keeps the container alive.
tail -f /dev/null