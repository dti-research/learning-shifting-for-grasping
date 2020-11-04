# Robot Learning of Shifting Objects for Grasping in Cluttered Environments

<div align="center">
  <img width="500" src="https://raw.githubusercontent.com/dti-research/learning-shifting-for-grasping/bug/new-codebase/resources/IMG_1829.jpeg">
</div>

This repository contains a *replication* of the paper *Robot Learning of Shifting Objects for Grasping in Cluttered Environments* presented at IROS 2019 in Macau. The code is inspired by the original work and procedings hereof but is **not** the original codebase. All dependencies are contained in a Docker image available from Docker Hub: [dtiresearch/learning-shifting-for-grasping](https://hub.docker.com/repository/docker/dtiresearch/learning-shifting-for-grasping) to allow for easy reproduction.

## Installation

Only prerequisite is that you have Docker installed.

- Pull down our Docker image

```
docker pull dtiresearch/learning-shifting-for-grasping
```

## Running the Demo

> to come!

## Models

- The trained models is available in the `models` directory
- CAD-models of the gripper fingers, camera mount, and box mounts are located in the `cad-models` directory

## Software Environment Details

While upgrading the codebase we decided to upgrade to the newest ROS 1 version that Franka supports which is currently ROS Melodic. More details on the installation process of each library can be found in the [Dockerfile](docker/Dockerfile).

- ROS Melodic
- Franka Control Interface (FCI) v4.0.4 ([robot firmware](https://support.franka.de/))
- libfranka [v0.8.0](https://frankaemika.github.io/docs/libfranka_changelog.html#id1)
- Franka ROS [v0.6.0](https://frankaemika.github.io/docs/franka_ros_changelog.html#id3)