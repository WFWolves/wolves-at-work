; Auto-generated. Do not edit!


(cl:in-package youbot_manipulation_vision-msg)


;//! \htmlinclude DetectedObjects.msg.html

(cl:defclass <DetectedObjects> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (objects
    :reader objects
    :initarg :objects
    :type (cl:vector youbot_manipulation_vision-msg:DetectedObject)
   :initform (cl:make-array 0 :element-type 'youbot_manipulation_vision-msg:DetectedObject :initial-element (cl:make-instance 'youbot_manipulation_vision-msg:DetectedObject))))
)

(cl:defclass DetectedObjects (<DetectedObjects>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <DetectedObjects>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'DetectedObjects)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name youbot_manipulation_vision-msg:<DetectedObjects> is deprecated: use youbot_manipulation_vision-msg:DetectedObjects instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <DetectedObjects>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:header-val is deprecated.  Use youbot_manipulation_vision-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'objects-val :lambda-list '(m))
(cl:defmethod objects-val ((m <DetectedObjects>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:objects-val is deprecated.  Use youbot_manipulation_vision-msg:objects instead.")
  (objects m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <DetectedObjects>) ostream)
  "Serializes a message object of type '<DetectedObjects>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'objects))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'objects))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <DetectedObjects>) istream)
  "Deserializes a message object of type '<DetectedObjects>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'objects) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'objects)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'youbot_manipulation_vision-msg:DetectedObject))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<DetectedObjects>)))
  "Returns string type for a message object of type '<DetectedObjects>"
  "youbot_manipulation_vision/DetectedObjects")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'DetectedObjects)))
  "Returns string type for a message object of type 'DetectedObjects"
  "youbot_manipulation_vision/DetectedObjects")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<DetectedObjects>)))
  "Returns md5sum for a message object of type '<DetectedObjects>"
  "888ee09f728332ca391b50f5f6a87049")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'DetectedObjects)))
  "Returns md5sum for a message object of type 'DetectedObjects"
  "888ee09f728332ca391b50f5f6a87049")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<DetectedObjects>)))
  "Returns full string definition for message of type '<DetectedObjects>"
  (cl:format cl:nil "#The header of the source image~%Header header~%~%DetectedObject[] objects~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: youbot_manipulation_vision/DetectedObject~%#Name of the detected Object~%string object_name~%~%#Rotated Rectangle of the source image matching the detected object~%RotatedRect rrect~%BoundingBox bbox~%================================================================================~%MSG: youbot_manipulation_vision/RotatedRect~%#Center of the rotated rectangle~%geometry_msgs/Point centerPoint~%~%#The width of the rotated rectangle~%float64 width~%#The height of the rotated rectangle~%float64 height~%~%#The angle of the rotated rectangle~%float64 angle~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: youbot_manipulation_vision/BoundingBox~%#Top-left corner of the bounding box~%geometry_msgs/Point position~%~%#The width of the bounding box~%float64 width~%#The height of the bounding box~%float64 height~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'DetectedObjects)))
  "Returns full string definition for message of type 'DetectedObjects"
  (cl:format cl:nil "#The header of the source image~%Header header~%~%DetectedObject[] objects~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: youbot_manipulation_vision/DetectedObject~%#Name of the detected Object~%string object_name~%~%#Rotated Rectangle of the source image matching the detected object~%RotatedRect rrect~%BoundingBox bbox~%================================================================================~%MSG: youbot_manipulation_vision/RotatedRect~%#Center of the rotated rectangle~%geometry_msgs/Point centerPoint~%~%#The width of the rotated rectangle~%float64 width~%#The height of the rotated rectangle~%float64 height~%~%#The angle of the rotated rectangle~%float64 angle~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: youbot_manipulation_vision/BoundingBox~%#Top-left corner of the bounding box~%geometry_msgs/Point position~%~%#The width of the bounding box~%float64 width~%#The height of the bounding box~%float64 height~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <DetectedObjects>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'objects) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <DetectedObjects>))
  "Converts a ROS message object to a list"
  (cl:list 'DetectedObjects
    (cl:cons ':header (header msg))
    (cl:cons ':objects (objects msg))
))
