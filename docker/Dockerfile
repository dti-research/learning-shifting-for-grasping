
#FROM dtiresearch/ros-melodic-py3
#FROM ros:melodic-ros-base
#FROM dtiresearch/ros-kinetic-py3
FROM ros:kinetic

LABEL maintainer="Nicolai Anton Lynnerup nily@dti.dk Lærke Fabricius llfa@dti.dk & Kim Lykke Nørregaard kimn@dti.dk"

SHELL ["/bin/bash", "-c"]

################
# Dependencies #
################

RUN apt-get update && apt-get install -y --no-install-recommends \
		iputils-ping \
		mlocate \
		nano \
		net-tools \
        python3-dev \
	    python3-pip \
	    python3-yaml \
        wget \
		&& updatedb

RUN pip3 install "pybind11[global]" --upgrade pip

################
# CMake 3.18.4 #
################

RUN apt-get update \
	&& apt-get install -y apt-transport-https ca-certificates gnupg software-properties-common \
	&& wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null \
	&& apt-add-repository 'deb https://apt.kitware.com/ubuntu/ xenial main' \
	&& apt-get update \
	&& apt-get install kitware-archive-keyring \
	&& rm /etc/apt/trusted.gpg.d/kitware.gpg \
	&& apt-get install -y cmake

################
# ROS Packages #
################

RUN apt-get update && apt-get install -y --no-install-recommends \
		ros-${ROS_DISTRO}-moveit-commander \
		ros-${ROS_DISTRO}-desktop-full \
        ros-${ROS_DISTRO}-franka-ros \
	    ros-${ROS_DISTRO}-libfranka \
		ros-${ROS_DISTRO}-opencv3

RUN pip3 install rospkg catkin_pkg

###############
# Eigen 3.3.7 #
###############

RUN cd /tmp/ \
    && wget -q --show-progress --progress=bar:force https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz \
	&& tar -xzf eigen-3.3.7.tar.gz \
	&& cd eigen-3.3.7 \
	&& mkdir build && cd build \
	&& cmake .. && make install \
    && cd /tmp/ && rm eigen-3.3.7.tar.gz

#############
# Workspace #
#############

RUN mkdir -p /home/workspace/
WORKDIR /home/workspace

# Create Catkin WS
RUN mkdir -p catkin_ws/src/learning-shifting-for-grasping 

# Set environment variables
ENV PYTHONPATH=$PYTHONPATH:/home/workspace/catkin_ws/devel/lib
ENV ROS_MASTER_URI=http://10.224.60.66:11311
ENV ROS_IP=10.224.60.60

# Setup .bashrc
RUN echo "source /home/workspace/catkin_ws/devel/setup.bash" >> ~/.bashrc \
	&& echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc