/* Auto-generated by genmsg_cpp for file /home/youbot/ros_workspace/youbot_manipulation_vision/msg/DetectedObjects.msg */
#ifndef YOUBOT_MANIPULATION_VISION_MESSAGE_DETECTEDOBJECTS_H
#define YOUBOT_MANIPULATION_VISION_MESSAGE_DETECTEDOBJECTS_H
#include <string>
#include <vector>
#include <map>
#include <ostream>
#include "ros/serialization.h"
#include "ros/builtin_message_traits.h"
#include "ros/message_operations.h"
#include "ros/time.h"

#include "ros/macros.h"

#include "ros/assert.h"

#include "std_msgs/Header.h"
#include "youbot_manipulation_vision/DetectedObject.h"

namespace youbot_manipulation_vision
{
template <class ContainerAllocator>
struct DetectedObjects_ {
  typedef DetectedObjects_<ContainerAllocator> Type;

  DetectedObjects_()
  : header()
  , objects()
  {
  }

  DetectedObjects_(const ContainerAllocator& _alloc)
  : header(_alloc)
  , objects(_alloc)
  {
  }

  typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
   ::std_msgs::Header_<ContainerAllocator>  header;

  typedef std::vector< ::youbot_manipulation_vision::DetectedObject_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::youbot_manipulation_vision::DetectedObject_<ContainerAllocator> >::other >  _objects_type;
  std::vector< ::youbot_manipulation_vision::DetectedObject_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::youbot_manipulation_vision::DetectedObject_<ContainerAllocator> >::other >  objects;


  typedef boost::shared_ptr< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator>  const> ConstPtr;
  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;
}; // struct DetectedObjects
typedef  ::youbot_manipulation_vision::DetectedObjects_<std::allocator<void> > DetectedObjects;

typedef boost::shared_ptr< ::youbot_manipulation_vision::DetectedObjects> DetectedObjectsPtr;
typedef boost::shared_ptr< ::youbot_manipulation_vision::DetectedObjects const> DetectedObjectsConstPtr;


template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const  ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> & v)
{
  ros::message_operations::Printer< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> >::stream(s, "", v);
  return s;}

} // namespace youbot_manipulation_vision

namespace ros
{
namespace message_traits
{
template<class ContainerAllocator> struct IsMessage< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct IsMessage< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator>  const> : public TrueType {};
template<class ContainerAllocator>
struct MD5Sum< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> > {
  static const char* value() 
  {
    return "888ee09f728332ca391b50f5f6a87049";
  }

  static const char* value(const  ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0x888ee09f728332caULL;
  static const uint64_t static_value2 = 0x391b50f5f6a87049ULL;
};

template<class ContainerAllocator>
struct DataType< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> > {
  static const char* value() 
  {
    return "youbot_manipulation_vision/DetectedObjects";
  }

  static const char* value(const  ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> > {
  static const char* value() 
  {
    return "#The header of the source image\n\
Header header\n\
\n\
DetectedObject[] objects\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.secs: seconds (stamp_secs) since epoch\n\
# * stamp.nsecs: nanoseconds since stamp_secs\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
\n\
================================================================================\n\
MSG: youbot_manipulation_vision/DetectedObject\n\
#Name of the detected Object\n\
string object_name\n\
\n\
#Rotated Rectangle of the source image matching the detected object\n\
RotatedRect rrect\n\
BoundingBox bbox\n\
================================================================================\n\
MSG: youbot_manipulation_vision/RotatedRect\n\
#Center of the rotated rectangle\n\
geometry_msgs/Point centerPoint\n\
\n\
#The width of the rotated rectangle\n\
float64 width\n\
#The height of the rotated rectangle\n\
float64 height\n\
\n\
#The angle of the rotated rectangle\n\
float64 angle\n\
================================================================================\n\
MSG: geometry_msgs/Point\n\
# This contains the position of a point in free space\n\
float64 x\n\
float64 y\n\
float64 z\n\
\n\
================================================================================\n\
MSG: youbot_manipulation_vision/BoundingBox\n\
#Top-left corner of the bounding box\n\
geometry_msgs/Point position\n\
\n\
#The width of the bounding box\n\
float64 width\n\
#The height of the bounding box\n\
float64 height\n\
";
  }

  static const char* value(const  ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct HasHeader< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct HasHeader< const ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
    stream.next(m.header);
    stream.next(m.objects);
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct DetectedObjects_
} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const  ::youbot_manipulation_vision::DetectedObjects_<ContainerAllocator> & v) 
  {
    s << indent << "header: ";
s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "objects[]" << std::endl;
    for (size_t i = 0; i < v.objects.size(); ++i)
    {
      s << indent << "  objects[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::youbot_manipulation_vision::DetectedObject_<ContainerAllocator> >::stream(s, indent + "    ", v.objects[i]);
    }
  }
};


} // namespace message_operations
} // namespace ros

#endif // YOUBOT_MANIPULATION_VISION_MESSAGE_DETECTEDOBJECTS_H
