import smach
import rospy
import copy
import zmq

class GetTaskspecFromRefbox(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'sendFailed', 'recieveFailed', 'connectFailed'],
                                   output_keys=['recieved_message_out'])
    def get_taskspec(self):
        server_ip = rospy.get_param('youbot_main_ai/refbox/server_ip')
        server_port = rospy.get_param('youbot_main_ai/refbox/server_port')
        team_name = "WF Wolves"
        message = None
        connection_address = "tcp://" + server_ip + ":" + server_port
        rospy.loginfo("Start connection to %s", connection_address)
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect(connection_address)
        except:
            return (message, 'connectFailed')
        rospy.loginfo("Connected.")
        try:
            socket.send(team_name)
        except:
            return (message, 'sendFailed')
        try:
            message = socket.recv()
        except:
            return (message, 'recieveFailed')
        try:
            socket.send("ACK")
            socket.close()
        except:
            return (message, 'sendFailed')
        return (message, 'succeeded')
    def get_taskspec_test(self):
        return ("BNT<(S5,S,3)(S6,N,3)(S7,N,3)(S3,S,3)(S4,N,3)(S1,S,3)(S2,S,3)>", "succeeded")
        #return ("BMT<S1,S1,S2,line(R20,F20_20_B),D1>", "succeeded")
        #return ("BTT<initialsituation(<S1,line(R20,F20_20_B)>);goalsituation(<S2,zigzag(F20_20_B,R20)>)>","succeeded")
        #return ("BTT<initialsituation(<S1,line(R20)>);goalsituation(<S2,circle(R20)>)>","succeeded")
    def execute(self, userdata):
        message, code = self.get_taskspec()
        userdata.recieved_message_out = message
        return code
