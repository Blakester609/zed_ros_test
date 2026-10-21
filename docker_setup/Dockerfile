FROM stereolabs/zed:5.5.0-devel-cuda13.0-ubuntu22.04	
ARG DEBIAN_FRONTEND=noninteractive

# Define a username for the new user
ARG NAME=marsrover

# Set up a new user
RUN useradd -ms /bin/bash $NAME && \
    usermod -aG sudo,video,dialout $NAME && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    echo "$NAME:$NAME" | chpasswd

# Set up automatic ROS 2 sourcing and colorized output
RUN echo "source /opt/ros/humble/setup.bash" >> /home/$NAME/.bashrc && \
    echo "source /home/$NAME/ros_ws/install/setup.bash" >> /home/$NAME/.bashrc && \
    echo "export RCUTILS_COLORIZED_OUTPUT=1" >> /home/$NAME/.bashrc && \
    echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> /home/$NAME/.bashrc && \
    echo "export _colcon_cd_root=/opt/ros/humble/" >> /home/$NAME/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> /home/$NAME/.bashrc && \
    touch /home/$NAME/.hushlogin

WORKDIR /ros2_ws/src
RUN git clone https://github.com/stereolabs/zed-ros2-wrapper.git

WORKDIR /ros2_ws
RUN apt-get update && rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    . /opt/ros/humble/setup.bash && \
    colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release

 # Fix the mmc_rule sudoers file syntax if it exists. This file is inconsequential if it doesn't exist, but it throws an error about improper syntax if it does.
USER root
RUN if [ -f /etc/sudoers.d/mmc_rule ]; then \
        echo "$NAME ALL=(ALL) NOPASSWD: /bin/ip" > /etc/sudoers.d/mmc_rule; \
    fi
USER $NAME

RUN echo "PS1='\[\033[1;34m\]\u@\h\[\033[0m\]:\[\033[1;37m\]\w\[\033[0m\]\\$ '" >> /home/marsrover/.bashrc

USER $NAME

WORKDIR /home/$NAME
CMD [ "tail", "-f", "/dev/null" ]
