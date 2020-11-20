
FROM ros:kinetic

LABEL maintainer="Nicolai Anton Lynnerup nily@dti.dk Lærke Fabricius llfa@dti.dk & Kim Lykke Nørregaard kimn@dti.dk"

SHELL ["/bin/bash", "-c"]

################
# Dependencies #
################

RUN apt-get update && apt-get install -y --no-install-recommends \
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
		libssl-dev \
		&& updatedb

RUN pip3 install "pybind11[global]" --upgrade pip

################
# CMake 3.19.0 #
################

ARG cmake_version=3.19
ARG cmake_build=0
RUN cd /tmp/ \
	&& wget -q --show-progress --progress=bar:force https://cmake.org/files/v$cmake_version/cmake-$cmake_version.$cmake_build.tar.gz \
	&& tar -xzf cmake-$cmake_version.$cmake_build.tar.gz \
	&& cd cmake-$cmake_version.$cmake_build/ \
	&& ./bootstrap \
	&& make -j$(nproc) \
	&& make install

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

################
# ROS Packages #
################

RUN apt-get update && apt-get install -y --no-install-recommends \
		ros-${ROS_DISTRO}-opencv3

RUN pip3 install rospkg catkin_pkg

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

##############
# Franka ROS #
##############
RUN cd catkin_ws \
	&& /bin/bash -c "source ~/.bashrc" \
	&& /bin/bash -c ". /opt/ros/${ROS_DISTRO}/setup.sh; catkin_init_workspace src" \
	&& git clone --recursive https://github.com/frankaemika/franka_ros src/franka_ros \
	&& apt-get update \
	&& rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y \
	&& /bin/bash -c ". /opt/ros/${ROS_DISTRO}/setup.bash; catkin_make -DCMAKE_BUILD_TYPE=Release -DFranka_DIR:PATH=/home/workspace/libfranka/build" \
	&& /bin/bash -c "source ~/.bashrc"

##########
# MoveIt #
##########
RUN mkdir ws_moveit && cd ws_moveit \
	&& rosdep update && apt update \
	&& apt dist-upgrade -y \
	&& apt install -y \
	python-rosdep \
	python-wstool \
	python-catkin-pkg \
	python-catkin-tools \
	&& wstool init src \
	#&& wstool merge -t src https://raw.githubusercontent.com/ros-planning/moveit/${ROS_DISTRO}-devel/moveit.rosinstall \
	&& wstool merge -t src https://raw.githubusercontent.com/dti-research/learning-shifting-for-grasping/bug/new-codebase/moveit.rosinstall \
	&& wstool update -t src \
 	&& rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y \
	&& catkin config --extend /opt/ros/${ROS_DISTRO} --cmake-args -DCMAKE_BUILD_TYPE=Release \
	&& catkin build \
	&& echo "source /home/workspace/ws_moveit/devel/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"