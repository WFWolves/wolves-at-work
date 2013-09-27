import roslib
roslib.load_manifest("youbot_generic_scripts")
import rospy
from rosgraph_msgs.msg import Log as LogMsg

class DoFunction:
    def __init__(self):
        pass
    def do_function(self, msg):
        pass

class FilterFunction:
    def __init__(self):
        pass
    def filter_function(self, msg):
        pass

class SimplePrintLogMsg(DoFunction):
    def __init__(self, prefix_node_name = False):
        DoFunction.__init__(self)
        self.prefix_node_name = prefix_node_name
    def do_function(self, msg):
        print_str = "[%s]: %s"
        prefix = "LogSubscriber"
        msg_str = msg.msg
        if self.prefix_node_name:
            prefix = msg.name
        print print_str % (prefix, msg_str)

class FilterByNodeName(FilterFunction):
    def __init__(self, node_names = None):
        FilterFunction.__init__(self)
        self.node_names = node_names
    def filter_function(self, msg):
        if msg.name in self.node_names:
            return True
        else:
            return False

class LogSubscriber:
    def __init__(self, filter_function, do_function):
        """LogSubscriber constructor
        filter_function: If filter_function.filter_function returns true 
            for a given rosgraph/Log message, then this instance will send 
            the message to do_function
        do_function:  do_function.do_function recieves the log message if filter_function returns true"""
        self.filter_function = filter_function
        self.do_function = do_function
        self.sub_rosout = rospy.Subscriber('/rosout', LogMsg, self.cb_roslog)
    def cb_roslog(self, msg):
        if self.filter_function.filter_function(msg):
            self.do_function.do_function(msg)
