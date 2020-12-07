# Robot Learning of Shifting Objects for Grasping in Cluttered Environments

<div align="center">
  <img width="500" src="https://raw.githubusercontent.com/dti-research/learning-shifting-for-grasping/bug/new-codebase/resources/IMG_1829.jpeg">
</div>

This repository contains a *replication* of the paper *Robot Learning of Shifting Objects for Grasping in Cluttered Environments* presented at IROS 2019 in Macau. The code is inspired by the original work and procedings hereof but is **not** the original codebase. All dependencies are contained in a Docker image available from Docker Hub: [dtiresearch/learning-shifting-for-grasping](https://hub.docker.com/repository/docker/dtiresearch/learning-shifting-for-grasping) to allow for easy reproduction.

## Installation

Only prerequisite is that you have Docker installed *and* that you have followed [Franka Emika's guide](https://frankaemika.github.io/docs/installation_linux.html#setting-up-the-real-time-kernel) on patching your Linux kernel to run real time.

- Pull down our Docker image

```
docker pull dtiresearch/learning-shifting-for-grasping
```

## Running the Demo

```
git clone https://github.com/dti-research/learning-shifting-for-grasping.git
cd learning-shifting-for-grasping
docker run -it --rm --net=host --privileged \
           -v $(pwd):/home/workspace/catkin_ws/src/learning-shifting-for-grasping \
           -w /home/workspace/catkin_ws \
           dtiresearch/learning-shifting-for-grasping
```

The docker container requires priveleged rights in order to set the real time capabilities of the container, otherwise the robot is not able to be controlled by the external PC as it is acting as full controller with a 1kHz control loop. If you experience communication issues please have a look at the [troubleshooting](https://frankaemika.github.io/docs/troubleshooting.html) page.


## Inside the container

```
# TODO when learning has finished and model is uploaded
```

### Running the Training Phase (on multiple PCs)

See [TRAINING.md](TRAINING.md) for an in-depth guide on how to run the training phase on your own system.

## Models

- The trained models is available in the `models` directory
- CAD-models of the gripper fingers, camera mount, and box mounts are located in the `cad-models` directory

## Software Environment Details

Below is a chosen list of libraries with versions, more details on the installation process of each library can be found in the [Dockerfile](docker/Dockerfile).

- ROS Kinetic (Ubuntu 16.04)
- Franka Control Interface (FCI) v4.0.4 ([robot firmware](https://support.franka.de/))
- libfranka [v0.8.0](https://frankaemika.github.io/docs/libfranka_changelog.html#id1)
- Franka ROS [v0.6.0](https://frankaemika.github.io/docs/franka_ros_changelog.html#id3)
