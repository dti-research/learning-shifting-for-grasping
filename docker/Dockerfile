
#FROM dtiresearch/ros-melodic-py3
#FROM ros:melodic-ros-base
#FROM dtiresearch/ros-kinetic-py3
FROM ros:kinetic as base

LABEL maintainer="Nicolai Anton Lynnerup nily@dti.dk Lærke Fabricius llfa@dti.dk & Kim Lykke Nørregaard kimn@dti.dk"

SHELL ["/bin/bash", "-c"]

################
# Dependencies #
################

RUN apt update && apt install -y --no-install-recommends \
		iproute2 \
		iputils-ping \
		mlocate \
		nano \
		net-tools \
        python3-dev \
	    python3-pip \
	    python3-yaml \
        wget \
		build-essential \
		libpoco-dev \
		libeigen3-dev \
		&& updatedb \
		&& apt remove "*libfranka*"

RUN pip3 install "pybind11[global]" --upgrade pip

################
# CMake 3.18.4 #
################

RUN apt update \
	&& apt install -y apt-transport-https ca-certificates gnupg software-properties-common \
	&& wget --no-check-certificate -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null \
	&& apt-add-repository 'deb https://apt.kitware.com/ubuntu/ xenial main' \
	&& apt update \
	&& apt install kitware-archive-keyring \
	&& rm /etc/apt/trusted.gpg.d/kitware.gpg \
	&& apt install -y cmake

################
# ROS Packages #
################

RUN apt update && apt install -y --no-install-recommends \
#		ros-${ROS_DISTRO}-moveit-commander \
		ros-${ROS_DISTRO}-desktop-full \
#       ros-${ROS_DISTRO}-franka-ros \
#	    ros-${ROS_DISTRO}-libfranka \
#		ros-${ROS_DISTRO}-moveit \
		ros-${ROS_DISTRO}-opencv3 \
		ros-${ROS_DISTRO}-joint-state-controller \
		ros-${ROS_DISTRO}-joint-trajectory-controller \
		ros-${ROS_DISTRO}-effort-controllers \
		ros-${ROS_DISTRO}-position-controllers

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

# Setup .bashrc
RUN echo "source /home/workspace/catkin_ws/devel/setup.bash" >> ~/.bashrc \
	&& echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"


#################################################################################################################################
FROM base as libfranka_and_frankaros

#########################
### INSTALL LIBFRANKA ###
#########################
RUN git clone --recursive https://github.com/frankaemika/libfranka.git \
	&& cd libfranka \
	&& git submodule update \
	&& mkdir build && cd build \
	&& cmake -DCMAKE_BUILD_TYPE=Release .. \
	&& cmake --build .

###################################
### INSTALL FRANKA ROS PACKAGES ###
###################################
RUN cd catkin_ws \
	&& /bin/bash -c "source ~/.bashrc" \
	&& /bin/bash -c ". /opt/ros/${ROS_DISTRO}/setup.sh; catkin_init_workspace src" \
	&& git clone --recursive https://github.com/frankaemika/franka_ros src/franka_ros \
	&& apt update \
	&& rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y \
	&& /bin/bash -c ". /opt/ros/${ROS_DISTRO}/setup.bash; catkin_make -DCMAKE_BUILD_TYPE=Release -DFranka_DIR:PATH=/home/workspace/libfranka/build" \
	&& /bin/bash -c "source ~/.bashrc"


#################################################################################################################################
FROM libfranka_and_frankaros as complete_build

######################
### INSTALL MOVEIT ###
######################
RUN mkdir ws_moveit && cd ws_moveit \
	&& rosdep update && apt update \
	&& apt dist-upgrade -y \
	&& apt install -y \
	python-rosdep \
#	ros-${ROS_DISTRO}-catkin \
	python-wstool \
	python-catkin-pkg \
	python-catkin-tools \
	&& wstool init src \
#	&& wstool merge -t src https://raw.githubusercontent.com/ros-planning/moveit/master/moveit.rosinstall \
	&& wstool merge -t src https://raw.githubusercontent.com/ros-planning/moveit/${ROS_DISTRO}-devel/moveit.rosinstall \
	&& wstool update -t src \
 	&& rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y \
	&& catkin config --extend /opt/ros/${ROS_DISTRO} --cmake-args -DCMAKE_BUILD_TYPE=Release \
	&& catkin build \
	&& echo "source /home/workspace/ws_moveit/devel/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"
