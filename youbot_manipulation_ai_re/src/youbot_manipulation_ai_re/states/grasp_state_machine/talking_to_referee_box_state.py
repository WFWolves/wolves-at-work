'''
@author: Jens Huebner
@version: 0.0.1 prealpha
@param taskspecification: List with the names of all objects, the robot has to grasp 
@note: This state communicates with the refereebox and 
       shares the task with the other states
'''
import smach
#import zmq
import sys
import re
from youbot_manipulation_ai_re.utils.task_specification import task_specification

class talking_to_referee_box(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['message received', 'Error, retry'],
                             output_keys=['task_specification_out'])

    def execute(self, userdata):
        print 'talking to RefereeBox'
        userdata.task_specification_out = self.evaluateMessage('BMT<D1,S1,S2,line(S40_40_B,F20_20_B,R20,R20,M20_100),S2>')#self.getTask())
        return 'message received'
    
    '''
    @note: Communicates with the refereebox
    @return: String with the task specification 
    '''
    def getTask(self):
        ServerIP = "192.168.2.190" 
        ServerPort = "11111"
        TeamName = "wf wolves"
        context = zmq.Context()
        connection_address = "tcp://" + ServerIP + ":" + ServerPort
        print "Start connection to " + connection_address
        print "Connecting to server..."
        socket = context.socket(zmq.REQ)
        socket.connect (connection_address)
        print "Sending request ..."
        socket.send (TeamName)
        
        message = socket.recv()
        socket.send ("ACK")
        socket.close()
        print "Received message: ", message
        return message
    
    '''
    @param message: String, containing task specification.
    @note: Evaluates the String.
    @return: class containing the task specification.
    '''
    def evaluateMessage(self,message):
        task_spec = task_specification()
        result = re.findall('[DST][0-9]',message)
        task_spec.set_initial_place(result[0])
        print 'Initial Place: ' + result[0]
        
        task_spec.set_source(result[1])
        print 'Source Place: ' + result[1]
        
        task_spec.set_destination(result[2])
        print 'Destination Place: ' + result[2]
        
        task_spec.set_final_place(result[3])
        print 'Final Place: ' + result[3]
        
        ObjectPositions = re.findall('[a-z]*[(].*[)]',message)
        result.append(re.findall('[a-z]*',ObjectPositions[0])[0])
        
        task_spec.set_formation(result[4])
        #globalData.objectsPosition = result[4]
        print 'Object Position: ' + result[4] 
        result = result + re.findall('[MSFRV][2-4][0]_?[1-4]?[0]+?_?[BG]?', ObjectPositions[0])
        print 'Objects to grasp:'
        task_spec.set_objects(re.findall('[MSFRV][2-4][0]_?[1-4]?[0]+?_?[BG]?', ObjectPositions[0]))
        print re.findall('[MSFRV][2-4][0]_?[1-4]?[0]+?_?[BG]?', ObjectPositions[0])
        return task_spec
    
