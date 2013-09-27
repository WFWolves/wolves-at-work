#!/usr/bin/env python
"""SimpleIkSolverConsole module
Provides easy python access to the IKSolver and Arm control.
Includes Console arm control.
@Author: Alexander Gabel
"""
import roslib; roslib.load_manifest('youbot_manipulation_scripts')

import rospy
import threading
import tf
import time
import math
import geometry_msgs.msg
import kinematics_msgs.srv
import kinematics_msgs.msg
import sensor_msgs.msg
import arm_navigation_msgs.msg
import arm_navigation_msgs.srv
import brics_actuator.msg
import sys, select, termios, tty, signal
import copy
from youbot_generic_scripts.StubMaker import create_methods_stub

from youbot_manipulation_scripts.youbot_arm_change import ArmChanger

class TimeoutException(Exception): 
    """Raised when a operation timed out."""
    pass 

class TerminalKeyboardManager:
    def __init__(self):
        self.settings = termios.tcgetattr(sys.stdin)
    def get_key(self):
        """gets a key pressed in terminal"""
        def cb_timeout_handler(signum, frame):
            """executed if the timeout for reading a key is reached"""
            raise TimeoutException()
        
        old_handler = signal.signal(signal.SIGALRM, cb_timeout_handler)
        signal.alarm(1) #this is the watchdog timing
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        try:
            key = sys.stdin.read(1)
            #print "Read key"
        except TimeoutException:
            #print "Timeout"
            return None
        finally:
            signal.signal(signal.SIGALRM, old_handler)

        signal.alarm(0)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

class SimpleIkSolver:
    """Provides python access to the ik solver"""
    def __init__(self):
        self.joint_names = ["arm_joint_1", "arm_joint_2", "arm_joint_3", "arm_joint_4", "arm_joint_5"]
        self.configuration = [0, 0, 0, 0, 0]
        self.received_state = False
        
        rospy.Subscriber('/joint_states', sensor_msgs.msg.JointState, self.joint_states_callback)
        
        rospy.loginfo("Waiting for 'get_constraint_aware_ik' service")
        rospy.wait_for_service('/youbot_arm_kinematics/get_constraint_aware_ik')
        self.ciks = rospy.ServiceProxy('/youbot_arm_kinematics/get_constraint_aware_ik',
                                        kinematics_msgs.srv.GetConstraintAwarePositionIK)
        rospy.loginfo("Service 'get_constraint_aware_ik' is ready")
        
        rospy.loginfo("Waiting for 'set_planning_scene_diff' service")
        rospy.wait_for_service('/environment_server/set_planning_scene_diff')
        self.planning_scene = rospy.ServiceProxy('/environment_server/set_planning_scene_diff',
                                                  arm_navigation_msgs.srv.SetPlanningSceneDiff)
        rospy.loginfo("Service 'set_planning_scene_diff'")
        
        # a planning scene must be set before using the constraint-aware ik!
        self.send_planning_scene()


    #callback function: when a joint_states message arrives, save the values
    def joint_states_callback(self, msg):
        """callback function: when a joint_states message arrives, save the values"""
        for k in range(5):
            for i in range(len(msg.name)):
                joint_name = "arm_joint_" + str(k + 1)
                if(msg.name[i] == joint_name):
                    self.configuration[k] = msg.position[i]
        self.received_state = True


    def send_planning_scene(self):
        """Sends planning scene"""
        rospy.loginfo("Sending planning scene")
        
        req = arm_navigation_msgs.srv.SetPlanningSceneDiffRequest()
        res = self.planning_scene.call(req)


    def call_constraint_aware_ik_solver(self, goal_pose):
        """Calls the constraint aware ik solver service and returns the solution or None"""
        while (not self.received_state):
            time.sleep(0.1)
        req = kinematics_msgs.srv.GetConstraintAwarePositionIKRequest()
        req.timeout = rospy.Duration(0.5)
        req.ik_request.ik_link_name = "arm_link_5"
        req.ik_request.ik_seed_state.joint_state.name = self.joint_names
        req.ik_request.ik_seed_state.joint_state.position = self.configuration
        req.ik_request.pose_stamped = goal_pose
        try:
            resp = self.ciks(req)
        except rospy.ServiceException, exc:
            rospy.logerr("Service did not process request: %s", str(exc))
        
        if (resp.error_code.val == arm_navigation_msgs.msg.ArmNavigationErrorCodes.SUCCESS):
            return resp.solution.joint_state.position
        else:
            return None


    def create_pose(self, x_coord, y_coord, z_coord, roll, pitch, yaw):
        """Creates and returns a stamped pose from coordinates and rpy angles"""
        pose = geometry_msgs.msg.PoseStamped()
        pose.pose.position.x = x_coord
        pose.pose.position.y = y_coord
        pose.pose.position.z = z_coord
        quat = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
        pose.pose.orientation.x = quat[0]
        pose.pose.orientation.y = quat[1]
        pose.pose.orientation.z = quat[2]
        pose.pose.orientation.w = quat[3]
        pose.header.frame_id = "/arm_link_0"
        pose.header.stamp = rospy.Time.now()
        
        return pose
        
class IKControlStub():
    """Stub replacement for IKControl"""
    def __init__(self, goto_start=True):
        self.armpub = None
        self.gripperpub = None
        self.iks = None
        if goto_start:
            self.reset_to_start()
        self.log_stub("IKControl initialized!")
    def log_stub(self, text):
        """Prefixed logging for this class"""
        rospy.loginfo("[IKControlStub]: %s" % text)
    def reset_to_start(self, wait = True):
        """Closes gripper and drives to front"""
        self.close_gripper()
        self.drive_to_front(wait)
    def drive_to_front(self, wait = True):
        """Drives the arm to the front position"""
        pos_dict = { "x": 0.024 + 0.033 + 0.4,
                   "y": 0.0,
                   "z": 0.115,
                   "roll": 0.3,
                   "pitch": math.pi / 2.0,
                   "yaw": 0.0}
        if wait:
            self.log_stub("Warning! Driving to front position...")
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_back(self, wait = True):
        """Drives the arm to the back position"""
        pos_dict = { "x": -0.22,
                   "y": -0.02,
                   "z": 0.19,
                   "roll": 0.3,
                   "pitch": -2.6,
                   "yaw": 0.0}
        if wait:
            self.log_stub("Warning! Driving to back position...")
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_right(self, wait = True):
        """Drives the arm to the right position"""
        pos_dict = { "x": 0.03,
                   "y": -0.28,
                   "z": 0.15,
                   "roll": 0.3,
                   "pitch":-1.6,
                   "yaw": 0.0}
        if wait:
            self.log_stub("Warning! Driving to right position...")
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_left(self, wait = True):
        """Drives the arm to the left position"""
        pos_dict = { "x": 0.03,
                   "y": 0.22,
                   "z": 0.14,
                   "roll": 0.3,
                   "pitch":1.63,
                   "yaw": 0.0}
        if wait:
            self.log_stub("Warning! Driving to left position...")
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_top(self, wait = True):
        """Drives the arm to the top position"""
        pos_dict = {'yaw': 0.378, 'pitch': 1.387, 'y': -0.0459, 'x': 0.029, 'z': 0.528, 'roll': 0.29}
        if wait:
            self.log_stub("Warning! Driving to top position...")
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def change_pos(self, pos_dict):
        """Changes the arm position to the position specified in pos_dict"""
        return self.__change_pos(self.iks, pos_dict)
    def change_gripper(self, gripper_dict):
        """Changes the gripper position to the position specified in gripper_dict"""
        self.log_stub("Gripper change: %s" % str(gripper_dict))
        return True
    def __change_pos(self, iks, pos_dict, fail = False):
        """Changes the position using the ik solver to the position specified in gripper_dict.
        If fail is true the methods emulates failing of this method by return (False, None).
        """
        if not fail:
            self.log_stub("ChangePos: %s using %s" % (str(pos_dict), str(iks)))
            return (True, pos_dict)
        else:
            self.log_stub("IK solver stub didn't find a solution")
            return (False, None)

    closed_gripper = {"fingerLeft":0.0, "fingerRight":0.0}
    opened_gripper = {"fingerLeft":0.01, "fingerRight":0.01}

    def open_gripper(self):
        """Opens the gripper"""
        self.log_stub("OpenGripper")
        return self.change_gripper(IKControl.opened_gripper)
    def close_gripper(self):
        """Closes the gripper"""
        self.log_stub("CloseGripper")
        return self.change_gripper(IKControl.closed_gripper)
    
class IKControl():
    """Provides easy python access to arm control using the IKSolver"""
    def __init__(self, goto_start = True):
        self.armpub = rospy.Publisher("/arm_1/arm_controller/position_command", brics_actuator.msg.JointPositions)
        self.gripperpub = rospy.Publisher("arm_1/gripper_controller/position_command",
                                           brics_actuator.msg.JointPositions)
        self.iks = SimpleIkSolver()
        if goto_start:
            self.reset_to_start()
        rospy.loginfo("IKControl initialized!")
    def reset_to_start(self, wait = True):
        """Closes gripper and drives to front"""
        self.close_gripper()
        self.drive_to_front(wait)
    def drive_to_front(self, wait = True):
        """Drives the arm to the front position"""
        pos_dict = { "x": 0.024 + 0.033 + 0.4,
                   "y": 0.0,
                   "z": 0.115,
                   "roll": 0.3,
                   "pitch": math.pi / 2.0,
                   "yaw": 0.0}
        if wait:
            print "Warning! Driving to front position..."
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_back(self, wait = True):
        """Drives the arm to the back position"""
        pos_dict = { "x": -0.22,
                   "y": -0.02,
                   "z": 0.19,
                   "roll": 0.3,
                   "pitch": -2.6,
                   "yaw": 0.0}
        if wait:
            print "Warning! Driving to back position..."
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_right(self, wait = True):
        """Drives the arm to the right position"""
        pos_dict = { "x": 0.03,
                   "y": -0.28,
                   "z": 0.15,
                   "roll": 0.3,
                   "pitch":-1.6,
                   "yaw": 0.0}
        if wait:
            print "Warning! Driving to right position..."
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_left(self, wait = True):
        """Drives the arm to the left position"""
        pos_dict = { "x": 0.03,
                   "y": 0.22,
                   "z": 0.14,
                   "roll": 0.3,
                   "pitch":1.63,
                   "yaw": 0.0}
        if wait:
            print "Warning! Driving to left position..."
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def drive_to_top(self, wait = True):
        """Drives the arm to the top position"""
        pos_dict = {'yaw': 0.378, 'pitch': 1.387, 'y': -0.0459, 'x': 0.029, 'z': 0.528, 'roll': 0.29}
        if wait:
            print "Warning! Driving to top position..."
            time.sleep(2.0)
        return self.__change_pos(self.iks, pos_dict)
    def change_pos(self, pos_dict):
        """Changes the arm position to the position specified in pos_dict"""
        return self.__change_pos(self.iks, pos_dict)
    def change_gripper(self, gripper_dict):
        """Changes the gripper position to the position specified in gripper_dict"""
        finger_left = gripper_dict["fingerLeft"]
        finger_right = gripper_dict["fingerRight"]
        joint_names = ["gripper_finger_joint_l", "gripper_finger_joint_r"]
        joint_values = [finger_left, finger_right]
        jpos = brics_actuator.msg.JointPositions()
        for i in range(2):
            jval = brics_actuator.msg.JointValue()
            jval.joint_uri = joint_names[i]
            jval.value = joint_values[i]
            jval.unit = "m"
            jpos.positions.append(jval)
        print "publish gripper cmd"
        self.gripperpub.publish(jpos)
        return True
    def __change_pos(self, iks, pos_dict):
        """Changes the position using the ik solver to the position specified in gripper_dict."""
        x_coord = pos_dict["x"]
        y_coord = pos_dict["y"]
        z_coord = pos_dict["z"]
        roll = pos_dict["roll"]
        pitch = pos_dict["pitch"]
        yaw = pos_dict["yaw"]
    
        pose = iks.create_pose(x_coord, y_coord, z_coord, roll, pitch, yaw)
        conf = iks.call_constraint_aware_ik_solver(pose)
        if (conf):
            # publish solution directly as joint positions
            print conf
            jpos = brics_actuator.msg.JointPositions()

            for i in range(5):
                jval = brics_actuator.msg.JointValue()
                jval.joint_uri = iks.joint_names[i]
                jval.value = conf[i]
                jval.unit = "rad"
                jpos.positions.append(jval)

            #rospy.sleep(0.5)
            print "publishing cmd"
            self.armpub.publish(jpos)
            return (True, pos_dict)
        else:
            print("IK solver didn't find a solution")
            return (False, None)

    closed_gripper = {"fingerLeft":0.0, "fingerRight":0.0}
    opened_gripper = {"fingerLeft":0.01, "fingerRight":0.01}

    def open_gripper(self):
        """Opens the gripper"""
        return self.change_gripper(IKControl.opened_gripper)
    def close_gripper(self):
        """Closes the gripper"""
        return self.change_gripper(IKControl.closed_gripper)
    
if __name__ == "__main__":

    def posDictControl():
        tempInput = raw_input("Werte fuer Position eingeben (x,y,z,r,p,y oder x,y,z,o): ")
        pos_lst = [float(x) for x in tempInput.split(',')]
        if len(pos_lst) == 4:
            pos_dict_key = ("x", "y", "z", "pitch")
            pos_dict = {}        
            pos_dict = { "x": pos_lst[0],
                "y": pos_lst[1],
                "z": pos_lst[2],
                "roll": 0.3,
                "pitch": pos_lst[3],
                "yaw": 0.0}
            changed_pos = True
            return (changed_pos, pos_dict)
        elif len(pos_dict) == 6:
            pos_dict_key = ("x", "y", "z", "roll", "pitch", "yaw")
            pos_dict = {}        
            pos_dict = { "x": pos_lst[0],
                "y": pos_lst[1],
                "z": pos_lst[2],
                "roll": pos_lst[3],
                "pitch": pos_lst[4],
                "yaw": pos_lst[5]}
            changed_pos = True
            return (changed_pos, pos_dict)
        else:
            print "Ungueltige Anzahl an parametern"
            return (False, {})                   
    
    def directControl(key_pressed, pos_dict, mov_dist, ikc):
        changed_pos = False
        if key_pressed in "bfrlt":
            driven = (False, None)
            if key_pressed == "b":
                driven = ikc.drive_to_back(False)
            elif key_pressed == "f":
                driven = ikc.drive_to_front(False)
            elif key_pressed == "r":
                driven = ikc.drive_to_right(False)
            elif key_pressed == "l":
                driven = ikc.drive_to_left(False)
            elif key_pressed == "t":
                driven = ikc.drive_to_top(False)
            if driven[0]:
                pos_dict = driven[1]
        if key_pressed in "wasd82467913":
            if key_pressed == "w":
                pos_dict["z"] += mov_dist
            elif key_pressed == "s":
                pos_dict["z"] -= mov_dist
            elif key_pressed == "a":
                pos_dict["y"] += mov_dist
            elif key_pressed == "d":
                pos_dict["y"] -= mov_dist
            elif key_pressed == "8":
                pos_dict["x"] += mov_dist
            elif key_pressed == "2":
                pos_dict["x"] -= mov_dist
            elif key_pressed == "4":
                pos_dict["pitch"] -= mov_dist
            elif key_pressed == "6":
                pos_dict["pitch"] += mov_dist
            elif key_pressed == "7":
                pos_dict["roll"] -= mov_dist
            elif key_pressed == "9":
                pos_dict["roll"] += mov_dist
            elif key_pressed == "1":
                pos_dict["yaw"] -= mov_dist
            elif key_pressed == "3":
                pos_dict["yaw"] += mov_dist
            changed_pos = True
            print pos_dict
        elif key_pressed in ",0":
            if key_pressed == ",":
                ikc.close_gripper()
                gripper_dict = IKControl.closed_gripper
            elif key_pressed == "0":
                ikc.open_gripper()
                gripper_dict = IKControl.opened_gripper
        elif key_pressed in "+-*/":
            print mov_dist
            if key_pressed == "+":
                mov_dist += 0.001
            elif key_pressed == "-":
                mov_dist -= 0.001
            elif key_pressed == "*":
                mov_dist *= 10.0
            elif key_pressed == "/":
                mov_dist /= 10.0     
        return (changed_pos, pos_dict, mov_dist)
    
    def armChangeControl(self):
        
        test =  kinematics_msgs.srv.GetPositionFK()
        return

    def main():
        """Main method - Enables arm control using IKControl via keyboard input in terminal"""
        rospy.init_node("simple_ik_solver")
        time.sleep(0.5)
    
        ikc = IKControl()
        pos_dict = { "x": 0.024 + 0.033 + 0.4,
                "y": 0.0,
                "z": 0.115,
                "roll": 0.3,
                "pitch": math.pi / 2.0,
                "yaw": 0.0 }
        term = TerminalKeyboardManager()
    
        mov_dist = 0.001
    
        armc = ArmChanger()
        while not armc.received_state:
            rospy.sleep(.1)
        rospy.loginfo("Initial joint_state recieved!")
        rospy.sleep(.5)
        
        mode = 0
        print "Keyboard input ready!"
        while 1:
            last_pos_dict = copy.deepcopy(pos_dict)
            key_pressed = term.get_key()
            #print "key:",hex(ord(key)),key
            changed_pos = False
            changed_gripper = False
            if key_pressed is not None:
                if key_pressed == "q":
                        exit(0)
                elif key_pressed == "t":
                    rospy.wait_for_service('youbot_arm_kinematics/get_ik_solver_info')
                    req = kinematics_msgs.srv.GetPositionFKRequest
                    resp = kinematics_msgs.srv.GetPositionFKResponse
                elif key_pressed == "m":
                    mode = (mode + 1) % 3
                    if (mode == 0):
                        print "Direct Control"
                    elif (mode == 1):
                        print "Pos-Dict Control"
                    elif (mode == 2):
                        print "ArmChanger"
                else:
                    if mode == 0:
                        directControlList = directControl(key_pressed, pos_dict, mov_dist, ikc)
                        mov_dist = directControlList[2]
                        changed_pos = directControlList[0]
                        if (changed_pos):
                            pos_dict = directControlList[1] 
                    elif mode == 1:
                        posDictControlList = posDictControl()
                        changed_pos = posDictControlList[0]
                        if (changed_pos):
                            pos_dict = posDictControlList[1]
                    elif mode == 2:
                        joint = int(raw_input("Joint: "))
                        change = float(raw_input("Relative Joint " + str(joint) + ": "))
                        print "Updated since last cmd:",str(armc.updated_since_last_cmd)
                        armc.change_relative(joint, change)
                            
                if changed_pos:
                    ik_solved = ikc.change_pos(pos_dict)[0]
                    #if ik_solved:
                    #    print "x: " + str(pos_lst[0]) + " y: " + str(pos_lst[1]) + " z: " + str(pos_lst[2]) + " roll: " + str(pos_lst[3]) + " pitch: " + str(pos_lst[4]) + " yaw: " + str(pos_lst[5])
                    #else:
                    #    pos_dict = last_pos_dict
                        
                    if not ik_solved:
                        pos_dict = last_pos_dict
    main()
