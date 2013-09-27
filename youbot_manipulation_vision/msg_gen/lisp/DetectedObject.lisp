; Auto-generated. Do not edit!


(cl:in-package youbot_manipulation_vision-msg)


;//! \htmlinclude DetectedObject.msg.html

(cl:defclass <DetectedObject> (roslisp-msg-protocol:ros-message)
  ((object_name
    :reader object_name
    :initarg :object_name
    :type cl:string
    :initform "")
   (rrect
    :reader rrect
    :initarg :rrect
    :type youbot_manipulation_vision-msg:RotatedRect
    :initform (cl:make-instance 'youbot_manipulation_vision-msg:RotatedRect))
   (bbox
    :reader bbox
    :initarg :bbox
    :type youbot_manipulation_vision-msg:BoundingBox
    :initform (cl:make-instance 'youbot_manipulation_vision-msg:BoundingBox)))
)

(cl:defclass DetectedObject (<DetectedObject>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <DetectedObject>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'DetectedObject)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name youbot_manipulation_vision-msg:<DetectedObject> is deprecated: use youbot_manipulation_vision-msg:DetectedObject instead.")))

(cl:ensure-generic-function 'object_name-val :lambda-list '(m))
(cl:defmethod object_name-val ((m <DetectedObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:object_name-val is deprecated.  Use youbot_manipulation_vision-msg:object_name instead.")
  (object_name m))

(cl:ensure-generic-function 'rrect-val :lambda-list '(m))
(cl:defmethod rrect-val ((m <DetectedObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:rrect-val is deprecated.  Use youbot_manipulation_vision-msg:rrect instead.")
  (rrect m))

(cl:ensure-generic-function 'bbox-val :lambda-list '(m))
(cl:defmethod bbox-val ((m <DetectedObject>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:bbox-val is deprecated.  Use youbot_manipulation_vision-msg:bbox instead.")
  (bbox m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <DetectedObject>) ostream)
  "Serializes a message object of type '<DetectedObject>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'object_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'object_name))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'rrect) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'bbox) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <DetectedObject>) istream)
  "Deserializes a message object of type '<DetectedObject>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'object_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'object_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'rrect) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'bbox) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<DetectedObject>)))
  "Returns string type for a message object of type '<DetectedObject>"
  "youbot_manipulation_vision/DetectedObject")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'DetectedObject)))
  "Returns string type for a message object of type 'DetectedObject"
  "youbot_manipulation_vision/DetectedObject")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<DetectedObject>)))
  "Returns md5sum for a message object of type '<DetectedObject>"
  "800da33f4f6e00b51df454a5259cf97d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'DetectedObject)))
  "Returns md5sum for a message object of type 'DetectedObject"
  "800da33f4f6e00b51df454a5259cf97d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<DetectedObject>)))
  "Returns full string definition for message of type '<DetectedObject>"
  (cl:format cl:nil "#Name of the detected Object~%string object_name~%~%#Rotated Rectangle of the source image matching the detected object~%RotatedRect rrect~%BoundingBox bbox~%================================================================================~%MSG: youbot_manipulation_vision/RotatedRect~%#Center of the rotated rectangle~%geometry_msgs/Point centerPoint~%~%#The width of the rotated rectangle~%float64 width~%#The height of the rotated rectangle~%float64 height~%~%#The angle of the rotated rectangle~%float64 angle~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: youbot_manipulation_vision/BoundingBox~%#Top-left corner of the bounding box~%geometry_msgs/Point position~%~%#The width of the bounding box~%float64 width~%#The height of the bounding box~%float64 height~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'DetectedObject)))
  "Returns full string definition for message of type 'DetectedObject"
  (cl:format cl:nil "#Name of the detected Object~%string object_name~%~%#Rotated Rectangle of the source image matching the detected object~%RotatedRect rrect~%BoundingBox bbox~%================================================================================~%MSG: youbot_manipulation_vision/RotatedRect~%#Center of the rotated rectangle~%geometry_msgs/Point centerPoint~%~%#The width of the rotated rectangle~%float64 width~%#The height of the rotated rectangle~%float64 height~%~%#The angle of the rotated rectangle~%float64 angle~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: youbot_manipulation_vision/BoundingBox~%#Top-left corner of the bounding box~%geometry_msgs/Point position~%~%#The width of the bounding box~%float64 width~%#The height of the bounding box~%float64 height~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <DetectedObject>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'object_name))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'rrect))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'bbox))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <DetectedObject>))
  "Converts a ROS message object to a list"
  (cl:list 'DetectedObject
    (cl:cons ':object_name (object_name msg))
    (cl:cons ':rrect (rrect msg))
    (cl:cons ':bbox (bbox msg))
))
