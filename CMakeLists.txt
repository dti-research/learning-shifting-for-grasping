cmake_minimum_required(VERSION 3.12)
project(learning_shifting VERSION 1.0.0 LANGUAGES CXX)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

set(Eigen3_DIRS "/usr/local/include/eigen3")

# Cache variables so pybind11_add_module can be used in parent projects
set(PYTHON_EXECUTABLE python3.5)
set(PYTHON_INCLUDE_DIR "/usr/include/python3.5m")
set(PYTHON_LIBRARY "/usr/lib/python3.5/config-3.5m-x86_64-linux-gnu/libpython3.5m.so")
set(PYBIND11_PYTHON_VERSION 3.5)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(Eigen3 REQUIRED)
if(Eigen3_FOUND)
  message(STATUS "Found Eigen3: ${EIGEN3_INCLUDE_DIR}")
endif()

find_package(realsense2 REQUIRED)

find_package(OpenGL REQUIRED)

find_package(Franka 0.8.0 REQUIRED)
if(Franka_FOUND)
  message(STATUS "Found libfranka (${Franka_VERSION}): ${Franka_INCLUDE_DIRS}")
endif()

find_package(OpenCV 3.3 REQUIRED)
find_package(pybind11 REQUIRED)
find_package(Python3 3.5 REQUIRED)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
    roscpp
    actionlib
    message_generation
    std_msgs
    sensor_msgs
    geometry_msgs
    franka_control
    franka_msgs
    interactive_markers
    image_transport
    cv_bridge
    moveit_core
    moveit_ros_planning
    moveit_ros_planning_interface
)

## System dependencies are found with CMake's conventions

include_directories(include ${catkin_INCLUDE_DIRS})

# Generate messages in the 'msg' folder
add_message_files(
  FILES
  OrthographicImage.msg
)

# Generate services in the 'srv' folder
add_service_files(
  FILES
  GetOrthographicImages.srv
)

# Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
  sensor_msgs
)

################################################
## Declare ROS dynamic reconfigure parameters ##
################################################

## To declare and build dynamic reconfigure parameters within this
## package, follow these steps:
## * In the file package.xml:
##   * add a build_depend and a exec_depend tag for "dynamic_reconfigure"
## * In this file (CMakeLists.txt):
##   * add "dynamic_reconfigure" to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * uncomment the "generate_dynamic_reconfigure_options" section below
##     and list every .cfg file to be processed

## Generate dynamic reconfigure parameters in the 'cfg' folder
# generate_dynamic_reconfigure_options(
#   cfg/DynReconf1.cfg
#   cfg/DynReconf2.cfg
# )

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
  INCLUDE_DIRS include
#  LIBRARIES learning-shifting-for-grasping
  CATKIN_DEPENDS
    roscpp
    message_runtime
    std_msgs
    sensor_msgs
    geometry_msgs
    interactive_markers
    franka_msgs
    moveit_core
    moveit_ros_planning
    moveit_ros_planning_interface
#  DEPENDS system_lib
)

###########
## Build ##
###########

add_library(ros INTERFACE)
target_include_directories(ros INTERFACE ${catkin_INCLUDE_DIRS})
target_link_libraries(ros INTERFACE ${catkin_LIBRARIES})
add_dependencies(ros ${catkin_EXPORTED_TARGETS})


add_library(realsense src/realsense/realsense.cpp)
target_include_directories(realsense PUBLIC ${Eigen3_DIRS} ${GLFW_INCLUDE_DIRS} ${OPENGL_INCLUDE_DIR} ${realsense_INCLUDE_DIR})
target_link_libraries(realsense PUBLIC glfw ${GLFW_LIBRARIES} ${OpenCV_LIBS} ${OPENGL_LIBRARIES} ${realsense2_LIBRARY} ros)

pybind11_add_module(orthographical src/orthographic_image/python.cpp)
target_include_directories(orthographical PRIVATE ${Eigen3_DIRS})
target_link_libraries(orthographical PRIVATE ${OpenCV_LIBS})

add_executable(realsense_node src/realsense/realsense_node.cpp)
target_link_libraries(realsense_node PRIVATE
  ros
  ${OpenCV_LIBS}
  yaml-cpp
  realsense
)

## Specify additional locations of header files
## Your package locations should be listed before other locations
#include_directories(
# include
# ${catkin_INCLUDE_DIRS}
#)

## Declare a C++ library
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/learning-shifting-for-grasping.cpp
# )

## Add cmake target dependencies of the library
## as an example, code may need to be generated before libraries
## either from message generation or dynamic reconfigure
# add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide
# add_executable(${PROJECT_NAME}_node src/learning-shifting-for-grasping_node.cpp)

## Rename C++ executable without prefix
## The above recommended prefix causes long target names, the following renames the
## target back to the shorter version for ease of user use
## e.g. "rosrun someones_pkg node" instead of "rosrun someones_pkg someones_pkg_node"
# set_target_properties(${PROJECT_NAME}_node PROPERTIES OUTPUT_NAME node PREFIX "")

## Add cmake target dependencies of the executable
## same as for the library above
# add_dependencies(${PROJECT_NAME}_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Specify libraries to link a library or executable target against
# target_link_libraries(${PROJECT_NAME}_node
#   ${catkin_LIBRARIES}
# )

#############
## Install ##
#############

# all install targets should use catkin DESTINATION variables
# See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
# catkin_install_python(PROGRAMS
#   scripts/my_python_script
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark executables for installation
## See http://docs.ros.org/melodic/api/catkin/html/howto/format1/building_executables.html
# install(TARGETS ${PROJECT_NAME}_node
#   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark libraries for installation
## See http://docs.ros.org/melodic/api/catkin/html/howto/format1/building_libraries.html
# install(TARGETS ${PROJECT_NAME}
#   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
# )

## Mark cpp header files for installation
# install(DIRECTORY include/${PROJECT_NAME}/
#   DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
#   FILES_MATCHING PATTERN "*.h"
#   PATTERN ".svn" EXCLUDE
# )

## Mark other files for installation (e.g. launch and bag files, etc.)
# install(FILES
#   # myfile1
#   # myfile2
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
# )

#############
## Testing ##
#############

## Add gtest based cpp test target and link libraries
# catkin_add_gtest(${PROJECT_NAME}-test test/test_learning-shifting-for-grasping.cpp)
# if(TARGET ${PROJECT_NAME}-test)
#   target_link_libraries(${PROJECT_NAME}-test ${PROJECT_NAME})
# endif()

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)
