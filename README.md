WF Wolves youBot stack Eindhoven 2013
=============

We used this ros stack to participate in the robocup@work world championship 2013.

License
-------

We publish all of our code and documents under the [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)](https://creativecommons.org/licenses/by-nc-sa/3.0).
For commercial interest please contact us at [wfwolves.de](http://robocup.fh-wolfenbuettel.de/index.php?option=com_content&view=article&id=57&Itemid=63)

Dependencies
-------

The following package dependencies exist. We have used ROS Fuerte and the latest released version of the packages (last update was on 5th June 2013). Python 2.7 is required.

* [smach, smach\_ros](http://wiki.ros.org/smach) -- `sudo apt-get install ros-fuerte-executive-smach` (https://github.com/ros/executive\_smach)
* [geometry\_msgs](http://wiki.ros.org/geometry\_msgs) -- `sudo apt-get install ros-fuerte-common-msgs` (https://github.com/ros/common\_msgs)
* [sensor\_msgs](http://wiki.ros.org/sensor\_msgs) -- `sudo apt-get install ros-fuerte-common-msgs` (https://github.com/ros/common\_msgs)
* [rospy](http://wiki.ros.org/rospy) -- `sudo apt-get install ros-fuerte-ros-comm` (https://github.com/ros/ros\_comm)
* [tf](http://wiki.ros.org/tf) -- `sudo apt-get install ros-fuerte-geometry` (https://kforge.ros.org/geometry/geometry)
* [rosgraph\_msgs](http://wiki.ros.org/rosgraph\_msgs) -- `sudo apt-get install ros-fuerte-ros-comm` (https://github.com/ros/ros\_comm)
* [brics\_actuator](http://wiki.ros.org/brics\_actuator) -- `sudo apt-get install ros-fuerte-cob-common`(https://github.com/ipa320/cob\_common)
* [std\_msgs](http://wiki.ros.org/std\_msgs) -- `sudo apt-get install ros-fuerte-std-msgs`(https://github.com/ros/std\_msgs)
* [actionlib](http://wiki.ros.org/actionlib) -- `sudo apt-get install ros-fuerte-actionlib` (https://github.com/ros/actionlib)
* [control\_msgs](http://wiki.ros.org/control\_msgs) -- `sudo apt-get install ros-fuerte-control` (https://bitbucket.org/sglaser/control)
* [kinematics\_msgs](http://wiki.ros.org/kinematics\_msgs) -- `sudo apt-get install ros-fuerte-arm-navigation` (https://kforge.ros.org/armnavigation/armnavigation)
* [trajectory\_msgs](http://wiki.ros.org/trajectory\_msgs) -- `sudo apt-get install ros-fuerte-common-msgs` (https://github.com/ros/common\_msgs)
* [arm\_navigation\_msgs](http://wiki.ros.org/arm\_navigation\_msgs) -- `sudo apt-get install ros-fuerte-arm-navigation` (https://kforge.ros.org/armnavigation/armnavigation)
* [trajectory\_msgs](http://wiki.ros.org/trajectory\_msgs) -- `sudo apt-get install ros-fuerte-common-msgs` (https://github.com/ros/common\_msgs)
* [image\_transport](http://wiki.ros.org/image\_transport) -- `sudo apt-get install ros-fuerte-image-common` (https://github.com/ros-perception/image\_common)
* [roscpp](http://wiki.ros.org/roscpp) -- `sudo apt-get install ros-fuerte-ros-comm` (https://github.com/ros/ros\_comm)
* [opencv2](http://wiki.ros.org/opencv2) -- `sudo apt-get install ros-fuerte-opencv2` (http://opencv.org)
* [cv\_bridge](http://wiki.ros.org/cv\_bridge) -- `sudo apt-get install ros-fuerte-vision-opencv` (https://github.com/ros-perception/vision\_opencv)
* [image\_geometry](http://wiki.ros.org/image\_geometry) -- `sudo apt-get install ros-fuerte-vision-opencv` (https://github.com/ros-perception/vision\_opencv)
* [dynamic\_reconfigure](http://wiki.ros.org/dynamic\_reconfigure) -- `sudo apt-get install ros-fuerte-dynamic-reconfigure` (https://github.com/ros/dynamic\_reconfigure)
* [image\_geometry](http://wiki.ros.org/image\_geometry) -- `sudo apt-get install ros-fuerte-vision-opencv` (https://github.com/ros-perception/vision\_opencv)
* [nav\_msgs](http://wiki.ros.org/nav\_msgs) -- `sudo apt-get install ros-fuerte-common-msgs` (https://github.com/ros/common\_msgs)
* [move\_base](http://wiki.ros.org/move\_base) -- `sudo apt-get install ros-fuerte-navigation` (https://github.com/ros-planning/navigation)
* [actionlib\_msgs](http://wiki.ros.org/actionlib\_msgs) -- `sudo apt-get install ros-fuerte-actionlib` (https://github.com/ros/actionlib)
* [pcl](http://wiki.ros.org/pcl) -- `sudo apt-get install ros-fuerte-perception-pcl` (http://svn.pointclouds.org/ros/branches/fuerte/perception\_pcl)
* [pcl\_ros](http://wiki.ros.org/pcl\_ros) -- `sudo apt-get install ros-fuerte-perception-pcl` (http://svn.pointclouds.org/ros/branches/fuerte/perception\_pcl)
* [laser\_geometry](http://wiki.ros.org/laser\_geometry) -- `sudo apt-get install ros-fuerte-laser-pipeline` (https://github.com/ros-perception/laser\_pipeline)
* [visualization\_msgs](http://wiki.ros.org/visualization\_msgs) -- `sudo apt-get install ros-fuerte-common-msgs` (https://github.com/ros/common\_msgs)/perception\_pcl)
* [youbot-ros-pkg](http://www.youbot-store.com/youbot-developers/software/frameworks/ros-wrapper-for-kuka-youbot-api) -- see website (https://github.com/youbot/youbot-ros-pkg)


Packages
-----------

* <b>youbot\_main\_ai:</b>  
    The youbot\_main\_ai is our central robot behaviour which communicates with the referee-box and launches the necessary task-behaviour(besides conveyorbelt). The `main_ai.launch` file starts the smach-state-machine and tries to connect to the referee-box.
* <b>youbot\_navigation\_ai\_re:</b>  
    The youbot\_navigation\_ai\_re is our robot behaviour for the navigation challenge and the `navigation_ai.launch` starts the smach-state-machine with a hard-coded Spec.
* <b>youbot\_conveyorbelt\_ai:</b>  
    The youbot\_conveyorbelt\_ai is our robot behaviour for the conveyorbelt challenge and the `conveyorbelt_ai.launch` starts it with the connection to the referee-box. (this was implemented one hour befor the challenge)
* <b>youbot\_manipulation\_ai\_re:</b>  
    The youbot\_manipulation\_ai\_re is our robot behaviour for the navigation challenge and the `manipulation_ai.launch` starts the smach-state-machine with a hard-coded Spec.
* <b>youbot\_transportation\_ai:</b>  
    The youbot\_transportation\_ai\_re is our robot behaviour for the navigation challenge and the `transportation_ai.launch` starts the smach-state-machine with no hard-coded Spec.
* <b>youbot\_generic\_scripts:</b>  
    The youbot\_generic\_scripts is our general toolbox package.
* <b>youbot\_ik\_solution\_modifier:</b>  
    The youbot\_ik\_solution\_modifier is an extension of our own IKControl class. We use it to handle the inverse kinematics from the youbot-ros-pkg. Due to quick fixing it is not in the youbot\_manipulation\_scripts package yet.
* <b>youbot\_manipulation\_scripts:</b>  
    The youbot\_manipulation\_scripts is a toolbox for manipulation scripts and classes.
* <b>youbot\_manipulation\_vision:</b>  
    The youbot\_manipulation\_vision is our object recognition node for the at-work objects. The `vision.launch` will start the node which tries to get a camera image on this topic: /usb\_cam/image\_raw.
* <b>youbot\_scanner\_alignment:</b>  
    The youbot\_scanner\_alignment is a ROS service that lets the robot align itself to a wall in front of it. It needs the `detected_best_laser_line_filtered` topic (published by youbot\_scanner\_lines), this will be started within the main\_ai-launch
* <b>youbot\_scanner\_lines:</b>  
    The youbot\_scanner\_lines is a RANSAC linedetection on the range finder scans. For this it subscribes to the `/base_scan` topic which is our front laser range finder.

Files
-----------

* <b>ros-pkg.patch:</b>  
    It is a patchfile for the youbot-ros-pkg to get our modificated launch files.
* <b>usb\_cam\_microsoft\_hd.launch:</b>  
    This is our camera launch file for the [usb\_cam](http://wiki.ros.org/usb\_cam) node
* <b>move\_base\_global\_dwa.launch:</b>  
    Our try to use the dwa planner.
* <b>base\_back\_hokuyo\_node.launch:</b>  
    We have two laser_range finders mounted on our robot, so this .launch is for the one in the back.

Installation
-----------

When the youBot is fresh installed you can patch the youbot-ros-pkg to get our modificated .launch files. To patch just copy the `ros-pkg.patch` file into your youbot-ros-pkg folder and execute the folowing in it:

    patch -p 3 < ./ros-pkg.patch

After that there are new .launch files which have to be moved into the corresponding folders

* `base_back_hokuyo_node.launch` into the `youbot-ros-pkg/youbot_navigation/youbot_navigation_common/launch` folder
* `move_base_global_dwa.launch` into the `youbot-ros-pkg/youbot_navigation/youbot_navigation_global/launch` folder
* `usb_cam_microsoft_hd.launch` into the `usb_cam/launch` folder

To be sure that all of our own ros_msgs are generated, build all packages:

    rosmake youbot_scanner_lines youbot_manipulation_vision youbot_conveyorbelt_ai youbot_ik_solution_modifier youbot_main_ai youbot_manipulation_scripts youbot_navigation_ai_re youbot_scanner_alignment youbot_transportation_ai

Usage
------------

To use our stuff you need to start some basic nodes:

    roslaunch youbot_manipulation_examples bringup.launch
    roslaunch youbot_navigation_common base_front_hokuyo_node.launch
    roslaunch youbot_navigation_common base_back_hokuyo_node.launch
    roslaunch usb_cam usb_cam_microsoft_hd.launch
    roslaunch youbot_manipulation_vision vision.launch
    roslaunch youbot_navigation_global amcl.launch
    roslaunch youbot_navigation_global move_base_global_dwa.launch

After this you have to make sure that the robot is localised and don't forget to calibrate the vision. For vision calibration you can use dynamic\_reconfigure.
Now your robot preperation is finished and you can connect to the referee-box and start the challenge with:

    roslaunch youbot_main_ai main_ai.launch

Now cross your fingers as we do it all the time.

Troubleshooting
------------
If you have any questions or problems regarding robot setup or installation, feel free to contact us at [wfwolves.de](http://robocup.fh-wolfenbuettel.de/index.php?option=com_content&view=article&id=57&Itemid=63).

Contributing
------------

1. Fork it.
2. Create a branch (`git checkout -b my_youbot_ai`)
3. Commit your changes (`git commit -am "Added Snarkdown"`)
4. Push to the branch (`git push origin my_youbot_ai`)
5. Open a [Pull Request][1]
6. Enjoy a refreshing Diet Coke and wait
