; Auto-generated. Do not edit!


(cl:in-package youbot_scanner_lines-msg)


;//! \htmlinclude DetectedLaserLines.msg.html

(cl:defclass <DetectedLaserLines> (roslisp-msg-protocol:ros-message)
  ((detectedLines
    :reader detectedLines
    :initarg :detectedLines
    :type (cl:vector youbot_scanner_lines-msg:DetectedLaserLine)
   :initform (cl:make-array 0 :element-type 'youbot_scanner_lines-msg:DetectedLaserLine :initial-element (cl:make-instance 'youbot_scanner_lines-msg:DetectedLaserLine))))
)

(cl:defclass DetectedLaserLines (<DetectedLaserLines>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <DetectedLaserLines>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'DetectedLaserLines)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name youbot_scanner_lines-msg:<DetectedLaserLines> is deprecated: use youbot_scanner_lines-msg:DetectedLaserLines instead.")))

(cl:ensure-generic-function 'detectedLines-val :lambda-list '(m))
(cl:defmethod detectedLines-val ((m <DetectedLaserLines>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader youbot_scanner_lines-msg:detectedLines-val is deprecated.  Use youbot_scanner_lines-msg:detectedLines instead.")
  (detectedLines m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <DetectedLaserLines>) ostream)
  "Serializes a message object of type '<DetectedLaserLines>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'detectedLines))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'detectedLines))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <DetectedLaserLines>) istream)
  "Deserializes a message object of type '<DetectedLaserLines>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'detectedLines) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'detectedLines)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'youbot_scanner_lines-msg:DetectedLaserLine))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<DetectedLaserLines>)))
  "Returns string type for a message object of type '<DetectedLaserLines>"
  "youbot_scanner_lines/DetectedLaserLines")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'DetectedLaserLines)))
  "Returns string type for a message object of type 'DetectedLaserLines"
  "youbot_scanner_lines/DetectedLaserLines")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<DetectedLaserLines>)))
  "Returns md5sum for a message object of type '<DetectedLaserLines>"
  "7c433a25e0a3ae395b3b8ecdca9a275d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'DetectedLaserLines)))
  "Returns md5sum for a message object of type 'DetectedLaserLines"
  "7c433a25e0a3ae395b3b8ecdca9a275d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<DetectedLaserLines>)))
  "Returns full string definition for message of type '<DetectedLaserLines>"
  (cl:format cl:nil "DetectedLaserLine[] detectedLines~%~%================================================================================~%MSG: youbot_scanner_lines/DetectedLaserLine~%#a point on the line~%float64 pointX~%float64 pointY~%float64 pointZ~%~%#the direction of the line as vector~%float64 directionX~%float64 directionY~%float64 directionZ~%~%#the number of points matched in the point cloud~%int32 pointCount~%~%#the extracted point cloud of the matched line~%sensor_msgs/PointCloud2 cloud~%~%================================================================================~%MSG: sensor_msgs/PointCloud2~%# This message holds a collection of N-dimensional points, which may~%# contain additional information such as normals, intensity, etc. The~%# point data is stored as a binary blob, its layout described by the~%# contents of the \"fields\" array.~%~%# The point cloud data may be organized 2d (image-like) or 1d~%# (unordered). Point clouds organized as 2d images may be produced by~%# camera depth sensors such as stereo or time-of-flight.~%~%# Time of sensor data acquisition, and the coordinate frame ID (for 3d~%# points).~%Header header~%~%# 2D structure of the point cloud. If the cloud is unordered, height is~%# 1 and width is the length of the point cloud.~%uint32 height~%uint32 width~%~%# Describes the channels and their layout in the binary data blob.~%PointField[] fields~%~%bool    is_bigendian # Is this data bigendian?~%uint32  point_step   # Length of a point in bytes~%uint32  row_step     # Length of a row in bytes~%uint8[] data         # Actual point data, size is (row_step*height)~%~%bool is_dense        # True if there are no invalid points~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: sensor_msgs/PointField~%# This message holds the description of one point entry in the~%# PointCloud2 message format.~%uint8 INT8    = 1~%uint8 UINT8   = 2~%uint8 INT16   = 3~%uint8 UINT16  = 4~%uint8 INT32   = 5~%uint8 UINT32  = 6~%uint8 FLOAT32 = 7~%uint8 FLOAT64 = 8~%~%string name      # Name of field~%uint32 offset    # Offset from start of point struct~%uint8  datatype  # Datatype enumeration, see above~%uint32 count     # How many elements in the field~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'DetectedLaserLines)))
  "Returns full string definition for message of type 'DetectedLaserLines"
  (cl:format cl:nil "DetectedLaserLine[] detectedLines~%~%================================================================================~%MSG: youbot_scanner_lines/DetectedLaserLine~%#a point on the line~%float64 pointX~%float64 pointY~%float64 pointZ~%~%#the direction of the line as vector~%float64 directionX~%float64 directionY~%float64 directionZ~%~%#the number of points matched in the point cloud~%int32 pointCount~%~%#the extracted point cloud of the matched line~%sensor_msgs/PointCloud2 cloud~%~%================================================================================~%MSG: sensor_msgs/PointCloud2~%# This message holds a collection of N-dimensional points, which may~%# contain additional information such as normals, intensity, etc. The~%# point data is stored as a binary blob, its layout described by the~%# contents of the \"fields\" array.~%~%# The point cloud data may be organized 2d (image-like) or 1d~%# (unordered). Point clouds organized as 2d images may be produced by~%# camera depth sensors such as stereo or time-of-flight.~%~%# Time of sensor data acquisition, and the coordinate frame ID (for 3d~%# points).~%Header header~%~%# 2D structure of the point cloud. If the cloud is unordered, height is~%# 1 and width is the length of the point cloud.~%uint32 height~%uint32 width~%~%# Describes the channels and their layout in the binary data blob.~%PointField[] fields~%~%bool    is_bigendian # Is this data bigendian?~%uint32  point_step   # Length of a point in bytes~%uint32  row_step     # Length of a row in bytes~%uint8[] data         # Actual point data, size is (row_step*height)~%~%bool is_dense        # True if there are no invalid points~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: sensor_msgs/PointField~%# This message holds the description of one point entry in the~%# PointCloud2 message format.~%uint8 INT8    = 1~%uint8 UINT8   = 2~%uint8 INT16   = 3~%uint8 UINT16  = 4~%uint8 INT32   = 5~%uint8 UINT32  = 6~%uint8 FLOAT32 = 7~%uint8 FLOAT64 = 8~%~%string name      # Name of field~%uint32 offset    # Offset from start of point struct~%uint8  datatype  # Datatype enumeration, see above~%uint32 count     # How many elements in the field~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <DetectedLaserLines>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'detectedLines) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <DetectedLaserLines>))
  "Converts a ROS message object to a list"
  (cl:list 'DetectedLaserLines
    (cl:cons ':detectedLines (detectedLines msg))
))
