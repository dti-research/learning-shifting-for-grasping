FROM ros:kinetic
MAINTAINER Lærke Fabricius llfa@teknologisk.dk & Kim Lykke Nørregaard kimn@teknologisk.dk

SHELL ["/bin/bash", "-c"]


########################
### INSTALL PACKAGES ###
########################
RUN apt-get update && apt-get install -y \
	software-properties-common \
	&& add-apt-repository ppa:ubuntu-toolchain-r/test \
	&& apt-get update && apt-get install -y \
	ros-kinetic-franka-ros \
	ros-kinetic-libfranka \
	autoconf \
	autogen \
	automake \
	build-essential \
	cmake \
	curl \
	g++ \
	g++-7 \
	g++-multilib \
	git \
	libeigen3-dev \
	libglfw3 \
	libglfw3-dev \
	libpoco-dev \
	libtool \
	mlocate \
	nano \
	pkg-config \
	python3-dev \
	python3-empy \
	python3-numpy \
	python3-pip \
	python3-wheel \
	unzip \
	wget \
	zlib1g-dev \
	zip \
	&& updatedb
	
RUN curl -L https://raw.githubusercontent.com/docker/compose/1.27.4/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose

RUN mkdir -p /home/Workspace

WORKDIR /home/Workspace


############################
### INSTALL BAZEL 0.16.1 ###
############################
RUN wget -q --show-progress --progress=bar:force -P /tmp https://github.com/bazelbuild/bazel/releases/download/0.16.1/bazel-0.16.1-installer-linux-x86_64.sh \
	&& chmod +x /tmp/bazel-0.16.1-installer-linux-x86_64.sh \
	&& /tmp/bazel-0.16.1-installer-linux-x86_64.sh \
	&& rm /tmp/bazel-0.16.1-installer-linux-x86_64.sh


#############################
### INSTALL TENSORFLOW_CC ###
#############################
RUN git clone https://github.com/dti-research/tensorflow_cc.git \
	&& cd tensorflow_cc/tensorflow_cc \
	&& git checkout r1.12.0 \
	&& mkdir build && cd build \
	&& cmake -DTENSORFLOW_STATIC=OFF -DTENSORFLOW_SHARED=ON .. \
	&& make && make install
	

###############################
### INSTALL TENSORFLOW 1.12 ###
###############################
# We decided to install TF 1.12 do to 
# libtensorflow_cc supports TF 1.9 and 1.12. 
# NOT 1.10 as the look of it.

RUN apt-get update \
	&& pip3 install --upgrade pip \
	&& pip3 install --user --upgrade tensorflow==1.12
	
	
#########################
### INSTALL LIBFRANKA ###
#########################
RUN git clone --recursive https://github.com/frankaemika/libfranka.git \
	&& apt-get update \
	&& cd libfranka \
	&& git checkout 0.6.0 \
	&& git submodule update \
	&& mkdir build && cd build \
	&& cmake -DCMAKE_BUILD_TYPE=Release .. \
	&& cmake --build .
	

######################################
### INSTALL LIBFRANKA ROS PACKAGES ###
######################################
RUN mkdir -p catkin_ws/src && cd catkin_ws \
	&& echo "source /opt/ros/kinetic/setup.sh" >> .bashrc \
	&& /bin/bash -c "source ~/.bashrc" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_init_workspace src" \
	&& git clone --recursive https://github.com/frankaemika/franka_ros src/franka_ros \
	&& apt-get update \
	&& cd src/franka_ros \
	&& git checkout 0.6.0 && cd ../../ \
	&& rosdep install --from-paths src --ignore-src --rosdistro kinetic -y --skip-keys libfranka \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make -DCMAKE_BUILD_TYPE=Release -DFranka_DIR:PATH=/home/Workspace/libfranka/build" \
	&& echo "source /home/Workspace/catkin_ws/devel/setup.sh" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"


######################
### INSTALL MOVEIT ###
######################
RUN rosdep update && apt-get update \
	&& apt-get dist-upgrade -y \
	&& apt-get install -y \
	ros-kinetic-catkin \
	python-catkin-tools \
	&& mkdir -p moveit_ws/src && cd moveit_ws/src \
	&& git clone -b kinetic-devel https://github.com/ros-planning/moveit_tutorials.git \
	&& git clone -b kinetic-devel https://github.com/ros-planning/panda_moveit_config.git \
	&& rosdep install -y --from-paths . --ignore-src --rosdistro kinetic \
	&& cd .. && catkin config --extend /opt/ros/kinetic \
	&& catkin build \
	&& echo "source /home/Workspace/moveit_ws/devel/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"


########################
### INSTALL YAML-CPP ###
########################
RUN git clone https://github.com/jbeder/yaml-cpp.git \
	&& cd yaml-cpp \
	&& git checkout yaml-cpp-0.6.0 \
	&& mkdir build && cd build \
	&& cmake .. && make && make install


######################
### INSTALL CATCH2 ###
######################
RUN git clone https://github.com/catchorg/Catch2.git \
	&& cd Catch2 && cmake -Bbuild -H. -DBUILD_TESTING=OFF \
	&& cmake --build build/ --target install


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
	&& apt-get install -y librealsense2-dkms \
	&& apt-get install -y librealsense2-utils \
	&& apt-get install -y librealsense2-dev  \
	&& apt-get install -y librealsense2-dbg \
	# Upgrade the local packages 
	&& apt-get update && apt-get --only-upgrade install -y librealsense2-utils librealsense2-dkms

# Create catkin workspace and clone realsense git repository
RUN echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc" \
	&& cd catkin_ws/src \
	&& git clone https://github.com/IntelRealSense/realsense-ros.git \
	&& git clone https://github.com/pal-robotics/ddynamic_reconfigure.git \
	&& cd realsense-ros \
	# The latest tag using ROS - and not ROS2
	&& git checkout tags/2.2.17

# Build the workspace from the repository
RUN /bin/bash -c "source ~/.bashrc" \
	&& cd catkin_ws \
	&& rosdep update \
	&& rosdep install -y -r --from-paths src --ignore-src --rosdistro=kinetic -y \
	#&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_init_workspace" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make clean" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release" \
	&& /bin/bash -c ". /opt/ros/kinetic/setup.sh; catkin_make install" 
	
RUN echo "source /home/Workspace/catkin_ws/devel/setup.bash" >> ~/.bashrc \
	#&& echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc \
	&& /bin/bash -c "source ~/.bashrc"


###################
### INSTALL CPR ###
###################
# https://github.com/whoshuu/cpr
RUN git clone https://github.com/whoshuu/cpr.git \
	&& cd cpr && git checkout 1.4.0 \
	&& git submodule update --init \
	&& mkdir build && cd build \
	&& cmake .. && make && make install


##############################
### CLONE THE MAIN PROJECT ###
##############################
RUN cd catkin_ws/src \
	&& apt update \
	&& mkdir learning-shifting-for-grasping \
	&& pip install catkin_pkg
	

######################
### INSTALL CEREAL ###
######################
RUN git clone https://github.com/USCiLab/cereal.git \
	&& cd cereal/include \
	&& cp -r cereal/ /home/Workspace/catkin_ws/src/learning-shifting-for-grasping/include \
	&& cd .. && mkdir build && cd build \
	&& cmake .. && make && make install
	

#####################
### INSTALL EIGEN ###
#####################
RUN git clone https://gitlab.com/libeigen/eigen.git && cd eigen \
	&& cp -r unsupported/ /home/Workspace/catkin_ws/src/learning-shifting-for-grasping/include/ \
	&& cp -r Eigen/ /home/Workspace/catkin_ws/src/learning-shifting-for-grasping/include/


###################	
### EXTRA STEPS ###
###################
RUN cp -r /home/Workspace/tensorflow_cc/tensorflow_cc/build/tensorflow/bazel-genfiles/tensorflow/cc/ops/ /usr/local/include/tensorflow/tensorflow/cc/ \
	&& pip install pyyaml \
	&& cd .. && mkdir Downloads && cd Downloads \
	&& wget -q --show-progress --progress=bar:force https://download.ensenso.com/s/ensensosdk/download?files=ensenso-sdk-2.3.1536-x64.deb \
	&& dpkg -i download\?files\=ensenso-sdk-2.3.1536-x64.deb 
	
	
	
	
	
