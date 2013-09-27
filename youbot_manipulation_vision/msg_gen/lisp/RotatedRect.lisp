; Auto-generated. Do not edit!


(cl:in-package youbot_manipulation_vision-msg)


;//! \htmlinclude RotatedRect.msg.html

(cl:defclass <RotatedRect> (roslisp-msg-protocol:ros-message)
  ((centerPoint
    :reader centerPoint
    :initarg :centerPoint
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (width
    :reader width
    :initarg :width
    :type cl:float
    :initform 0.0)
   (height
    :reader height
    :initarg :height
    :type cl:float
    :initform 0.0)
   (angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0))
)

(cl:defclass RotatedRect (<RotatedRect>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RotatedRect>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RotatedRect)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name youbot_manipulation_vision-msg:<RotatedRect> is deprecated: use youbot_manipulation_vision-msg:RotatedRect instead.")))

(cl:ensure-generic-function 'centerPoint-val :lambda-list '(m))
(cl:defmethod centerPoint-val ((m <RotatedRect>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:centerPoint-val is deprecated.  Use youbot_manipulation_vision-msg:centerPoint instead.")
  (centerPoint m))

(cl:ensure-generic-function 'width-val :lambda-list '(m))
(cl:defmethod width-val ((m <RotatedRect>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:width-val is deprecated.  Use youbot_manipulation_vision-msg:width instead.")
  (width m))

(cl:ensure-generic-function 'height-val :lambda-list '(m))
(cl:defmethod height-val ((m <RotatedRect>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:height-val is deprecated.  Use youbot_manipulation_vision-msg:height instead.")
  (height m))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <RotatedRect>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_manipulation_vision-msg:angle-val is deprecated.  Use youbot_manipulation_vision-msg:angle instead.")
  (angle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RotatedRect>) ostream)
  "Serializes a message object of type '<RotatedRect>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'centerPoint) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'width))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'height))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RotatedRect>) istream)
  "Deserializes a message object of type '<RotatedRect>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'centerPoint) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'width) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'height) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RotatedRect>)))
  "Returns string type for a message object of type '<RotatedRect>"
  "youbot_manipulation_vision/RotatedRect")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RotatedRect)))
  "Returns string type for a message object of type 'RotatedRect"
  "youbot_manipulation_vision/RotatedRect")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RotatedRect>)))
  "Returns md5sum for a message object of type '<RotatedRect>"
  "85ead10cf1031b0f418b5071f7763172")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RotatedRect)))
  "Returns md5sum for a message object of type 'RotatedRect"
  "85ead10cf1031b0f418b5071f7763172")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RotatedRect>)))
  "Returns full string definition for message of type '<RotatedRect>"
  (cl:format cl:nil "#Center of the rotated rectangle~%geometry_msgs/Point centerPoint~%~%#The width of the rotated rectangle~%float64 width~%#The height of the rotated rectangle~%float64 height~%~%#The angle of the rotated rectangle~%float64 angle~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RotatedRect)))
  "Returns full string definition for message of type 'RotatedRect"
  (cl:format cl:nil "#Center of the rotated rectangle~%geometry_msgs/Point centerPoint~%~%#The width of the rotated rectangle~%float64 width~%#The height of the rotated rectangle~%float64 height~%~%#The angle of the rotated rectangle~%float64 angle~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RotatedRect>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'centerPoint))
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RotatedRect>))
  "Converts a ROS message object to a list"
  (cl:list 'RotatedRect
    (cl:cons ':centerPoint (centerPoint msg))
    (cl:cons ':width (width msg))
    (cl:cons ':height (height msg))
    (cl:cons ':angle (angle msg))
))
