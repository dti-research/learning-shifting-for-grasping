
#FROM dtiresearch/ros-melodic-py3
#FROM ros:melodic-ros-base
#FROM dtiresearch/ros-kinetic-py3
FROM ros:kinetic

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
		gedit \ 
		python3-empy \
		python3-tk \
		libglfw3 \
		libglfw3-dev \
		libvtk6.2 \
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

RUN pip3 install "pybind11[global]" --upgrade pip \
	&& pip install matplotlib \
	opencv-python \
	pyrealsense2 \
	&& pip install --upgrade tensorflow


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
ENV ROS_MASTER_URI=http://10.224.55.100:11311
ENV ROS_IP=10.224.60.100

# Setup .bashrc
RUN echo "source /home/workspace/catkin_ws/devel/setup.bash" >> ~/.bashrc \
	&& echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"


#################################################################################################################################


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
	&& /bin/bash -c ". /opt/ros/${ROS_DISTRO}/setup.bash; catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3 -DCMAKE_BUILD_TYPE=Release -DFranka_DIR:PATH=/home/workspace/libfranka/build" \
	&& /bin/bash -c "source ~/.bashrc"

#Rename opencv 
RUN cd /opt/ros/kinetic/lib/python2.7/dist-packages/ \
	&& mv cv2.so cv2_ros.so

#################################################################################################################################


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
	&& wstool merge -t src https://raw.githubusercontent.com/dti-research/learning-shifting-for-grasping/bug/new-codebase/moveit.rosinstall \
	&& wstool update -t src \
 	&& rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y \
	&& catkin config --extend /opt/ros/${ROS_DISTRO} --cmake-args -DCMAKE_BUILD_TYPE=Release \
	&& catkin build \
	&& echo "source /home/workspace/ws_moveit/devel/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"

# RUN cp /home/workspace/ws_moveit/src/panda_moveit_config/config/panda_arm.xacro /opt/ros/${ROS_DISTRO}/share/panda_moveit_config/config/
#########################
### INSTALL CV_BRIDGE ###
#########################

RUN mkdir -p cv_ws/src \
	&& cd cv_ws \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make" 

RUN apt-get install -y python-catkin-tools \
	python3-dev \
	python3-catkin-pkg-modules \
	python3-numpy \
	python3-yaml \
	ros-kinetic-cv-bridge

RUN cd cv_ws \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin init" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.5m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.5m.so" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin config --install" 

# Clone the repo and change the one line 
RUN cd cv_ws \
	&& git clone https://github.com/ros-perception/vision_opencv.git src/vision_opencv \
	&& cd src/vision_opencv/ \ 
	&& git checkout 1.12.8 \ 
	&& sed -i 's/python3/python-py35/' cv_bridge/CMakeLists.txt

# Build Cv_Bridge 
RUN cd cv_ws \ 
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin clean -y" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin build cv_bridge" \
	&& /bin/bash -c "source install/setup.bash --extend" 

#########################
### INSTALL REALSENSE ###
#########################
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update \
	# Get lisence key
	&& apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE \
	&& apt-get install -y software-properties-common \
	# Add the repository 
	&& add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main" -u \
	# Install the librealsense, Development packages & and other needed packages
	&& apt-get install -y \
	librealsense2-dkms \
	librealsense2-utils \
	librealsense2-dev  \
	librealsense2-dbg \
	# Upgrade the local packages 
	&& apt-get update && apt-get --only-upgrade install -y librealsense2-utils librealsense2-dkms

# Create catkin workspace and clone realsense git repository
#RUN echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc \
#RUN	/bin/bash -c "source ~/.bashrc" \
RUN cd catkin_ws/src \
	&& git clone https://github.com/IntelRealSense/realsense-ros.git \
	&& git clone https://github.com/pal-robotics/ddynamic_reconfigure.git \
	&& cd realsense-ros \
	# The latest tag using ROS - and not ROS2
	&& git checkout tags/2.2.17

# Build the workspace from the repository
RUN /bin/bash -c "source ~/.bashrc" \
	&& cd catkin_ws \
	&& rosdep update \
	&& rosdep install -r --from-paths src --ignore-src --rosdistro=kinetic -y \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make clean" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make install" 
	

