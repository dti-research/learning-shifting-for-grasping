FROM ros:melodic-ros-base

LABEL maintainer="Nicolai Anton Lynnerup nily@dti.dk Lærke Fabricius llfa@dti.dk & Kim Lykke Nørregaard kimn@dti.dk"

RUN apt-get update && apt-get install -y --no-install-recommends \
        cmake \
        python-catkin-tools \
        ros-melodic-franka-ros \
	    ros-melodic-libfranka \
    && rm -rf /var/lib/apt/lists/*