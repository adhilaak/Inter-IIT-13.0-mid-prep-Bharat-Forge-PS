Start a docker container with the osrf/ros-noetic-desktop-full image.
```bash
sudo apt install ros-noetic-desktop-full ros-noetic-move-base ros-noetic-slam-gmapping ros-noetic-turtlebot3 ros-noetic-turtlebot3-gazebo ros-noetic-multirobot-map-merge ros-noetic-explore-lite ros-noetic-dwa-local-planner python3-pip python-is-python3 ros-noetic-amcl ros-noetic-base-local-planner ros-noetic-map-server ros-noetic-navfn libgoogle-glog-dev python3.9
mkdir -p ~/catkin_ws/src
cd ~
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
cd ~/catkin_ws/src/Task_Allocation
python3.9 -m pip install -r requirements.txt
cd ~/catkin_ws
catkin_make
roslaunch ~/catkin_ws/src/multiple_turtlebot3/launch/frontier_exploration/main.launch
```

After frontier exploration is done and you are satisfied with map generated in rviz, open another terminal and enter
```bash
cd ~/catkin_ws/multiple_turtlebot3/map
rosrun map_server map_saver
```

To merge the results of YOLO use
```bash
cd ~/catkin_ws/multiple_turtlebot3
python script/merge_db.py
```

After that, close the previous windows and enter
``` bash
roslaunch multiple_turtlebot3 multiple_turtlebot3.launch
```

and this uses D\*, DWA for global, local planning


You can start the LLM Interface with
```bash
cd ~/catkin_ws/Task_Allocation
python3.9 Interface.py
```
