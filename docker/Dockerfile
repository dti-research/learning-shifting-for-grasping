
FROM dtiresearch/frankr

LABEL maintainer="Nicolai Anton Lynnerup nily@dti.dk Lærke Fabricius llfa@dti.dk & Kim Lykke Nørregaard kimn@dti.dk"

SHELL ["/bin/bash", "-c"]

################
# Dependencies #
################

RUN apt-get update && apt-get install -y --no-install-recommends \
		python3-empy \
		python3-tk \
		libglfw3 \
		libglfw3-dev \
		libvtk6.2 \
		&& updatedb

RUN pip3 install "pybind11[global]" --upgrade pip \
	&& pip install matplotlib \
	opencv-python \
	pyrealsense2 \
	&& pip install --upgrade tensorflow

################
# ROS Packages #
################

RUN apt-get update && apt-get install -y --no-install-recommends \
		ros-${ROS_DISTRO}-desktop-full \
		ros-${ROS_DISTRO}-opencv3

#############
# Workspace #
#############

# Set environment variables
ENV ROS_MASTER_URI=http://10.224.60.100:11311
ENV ROS_IP=10.224.60.100

#################################################################################################################################

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
	

