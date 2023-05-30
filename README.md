# TP-1 Note : Turtle Regulation Package-INFO-2
### Written by:
#### Lingachetti Paavalen
#### Surjoo Yogheshwar

# Installation
Place the package: Turtle_regulation_Paavalen_Lingachetti_Yogheshwar_Surjoo in a catkin workspace

Build the package
```sh
catkin build
```
Source the setup.bash
```sh
source devel/setup.bash             #This command works from the workspace
```
Open src/Turtle_regulation_Paavalen_Lingachetti_Yogheshwar_Surjoo/src
```sh
cd src/Turtle_regulation_Paavalen_Lingachetti_Yogheshwar_Surjoo/src
```

Give execution right to set_way_point.py and service_client.py
```sh
chmod +x set_way_point.py
chmod +x service_client.py
```

Open a terminal and type
```sh
roscore
```

Open another terminal and type 
```sh
rosrun turtlesim turtlesim_node
```
Open another terminal
Type this command to launch the script
```sh
roslaunch turtle_regulation_paavalen_lingachetti_yogheshwar_surjoo way_point.launch
```

Enter the first coordinates  
Watch and wait for the turtle to move
Enter the second coordinates and do the same for the third one.
