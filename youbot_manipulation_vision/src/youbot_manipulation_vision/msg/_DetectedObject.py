"""autogenerated by genpy from youbot_manipulation_vision/DetectedObject.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import youbot_manipulation_vision.msg
import geometry_msgs.msg

class DetectedObject(genpy.Message):
  _md5sum = "800da33f4f6e00b51df454a5259cf97d"
  _type = "youbot_manipulation_vision/DetectedObject"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """#Name of the detected Object
string object_name

#Rotated Rectangle of the source image matching the detected object
RotatedRect rrect
BoundingBox bbox
================================================================================
MSG: youbot_manipulation_vision/RotatedRect
#Center of the rotated rectangle
geometry_msgs/Point centerPoint

#The width of the rotated rectangle
float64 width
#The height of the rotated rectangle
float64 height

#The angle of the rotated rectangle
float64 angle
================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: youbot_manipulation_vision/BoundingBox
#Top-left corner of the bounding box
geometry_msgs/Point position

#The width of the bounding box
float64 width
#The height of the bounding box
float64 height
"""
  __slots__ = ['object_name','rrect','bbox']
  _slot_types = ['string','youbot_manipulation_vision/RotatedRect','youbot_manipulation_vision/BoundingBox']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       object_name,rrect,bbox

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(DetectedObject, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.object_name is None:
        self.object_name = ''
      if self.rrect is None:
        self.rrect = youbot_manipulation_vision.msg.RotatedRect()
      if self.bbox is None:
        self.bbox = youbot_manipulation_vision.msg.BoundingBox()
    else:
      self.object_name = ''
      self.rrect = youbot_manipulation_vision.msg.RotatedRect()
      self.bbox = youbot_manipulation_vision.msg.BoundingBox()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self.object_name
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_11d.pack(_x.rrect.centerPoint.x, _x.rrect.centerPoint.y, _x.rrect.centerPoint.z, _x.rrect.width, _x.rrect.height, _x.rrect.angle, _x.bbox.position.x, _x.bbox.position.y, _x.bbox.position.z, _x.bbox.width, _x.bbox.height))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.rrect is None:
        self.rrect = youbot_manipulation_vision.msg.RotatedRect()
      if self.bbox is None:
        self.bbox = youbot_manipulation_vision.msg.BoundingBox()
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.object_name = str[start:end].decode('utf-8')
      else:
        self.object_name = str[start:end]
      _x = self
      start = end
      end += 88
      (_x.rrect.centerPoint.x, _x.rrect.centerPoint.y, _x.rrect.centerPoint.z, _x.rrect.width, _x.rrect.height, _x.rrect.angle, _x.bbox.position.x, _x.bbox.position.y, _x.bbox.position.z, _x.bbox.width, _x.bbox.height,) = _struct_11d.unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self.object_name
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_11d.pack(_x.rrect.centerPoint.x, _x.rrect.centerPoint.y, _x.rrect.centerPoint.z, _x.rrect.width, _x.rrect.height, _x.rrect.angle, _x.bbox.position.x, _x.bbox.position.y, _x.bbox.position.z, _x.bbox.width, _x.bbox.height))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.rrect is None:
        self.rrect = youbot_manipulation_vision.msg.RotatedRect()
      if self.bbox is None:
        self.bbox = youbot_manipulation_vision.msg.BoundingBox()
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.object_name = str[start:end].decode('utf-8')
      else:
        self.object_name = str[start:end]
      _x = self
      start = end
      end += 88
      (_x.rrect.centerPoint.x, _x.rrect.centerPoint.y, _x.rrect.centerPoint.z, _x.rrect.width, _x.rrect.height, _x.rrect.angle, _x.bbox.position.x, _x.bbox.position.y, _x.bbox.position.z, _x.bbox.width, _x.bbox.height,) = _struct_11d.unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
_struct_11d = struct.Struct("<11d")
