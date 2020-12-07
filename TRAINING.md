# Running the Training Phase (on multiple PCs)

As we're using ROS for this project we are able to run different parts of the complete system on different machines, e.g. one running all related to robot control and another for camera communication and processing of the neural network. For this case we would choose one of our machines to be the master and the others will connect to this by specifying both the master IP and the slave's own IP: 

```
# Set environment variables
export ROS_MASTER_URI=http://10.224.60.100:11311
export ROS_IP=10.224.60.60
```

## Robot PC

Then on the PC connected to the Franka Emika Panda robot open two (2) terminals and start the docker container in the first terminal by:

```bash
docker run -it --rm --net=host --privileged \
           dtiresearch/frankr
```

Next, in the remaining terminal connect to the container by running:

```bash
docker exec -it NAME_OF_CONTAINER bash
```

Now we want to run all robot related ROS nodes in these terminals:

```bash
# Terminal 1
roslaunch franka_control franka_control.launch robot_ip:=172.16.0.2 # FCI_IP

# Terminal 2
roslaunch panda_moveit_config panda_moveit.launch
```

## NN + Camera PC

```
git clone https://github.com/dti-research/learning-shifting-for-grasping.git
cd learning-shifting-for-grasping
docker run -it --rm --net=host --privileged \
           -v $(pwd):/home/workspace/catkin_ws/src/learning-shifting-for-grasping \
           -w /home/workspace/catkin_ws \
           dtiresearch/learning-shifting-for-grasping
```

TODO
