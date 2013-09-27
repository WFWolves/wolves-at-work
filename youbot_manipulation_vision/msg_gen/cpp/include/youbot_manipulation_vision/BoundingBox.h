/* Auto-generated by genmsg_cpp for file /home/youbot/ros_workspace/youbot_manipulation_vision/msg/BoundingBox.msg */
#ifndef YOUBOT_MANIPULATION_VISION_MESSAGE_BOUNDINGBOX_H
#define YOUBOT_MANIPULATION_VISION_MESSAGE_BOUNDINGBOX_H
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

#include "geometry_msgs/Point.h"

namespace youbot_manipulation_vision
{
template <class ContainerAllocator>
struct BoundingBox_ {
  typedef BoundingBox_<ContainerAllocator> Type;

  BoundingBox_()
  : position()
  , width(0.0)
  , height(0.0)
  {
  }

  BoundingBox_(const ContainerAllocator& _alloc)
  : position(_alloc)
  , width(0.0)
  , height(0.0)
  {
  }

  typedef  ::geometry_msgs::Point_<ContainerAllocator>  _position_type;
   ::geometry_msgs::Point_<ContainerAllocator>  position;

  typedef double _width_type;
  double width;

  typedef double _height_type;
  double height;


  typedef boost::shared_ptr< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator>  const> ConstPtr;
  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;
}; // struct BoundingBox
typedef  ::youbot_manipulation_vision::BoundingBox_<std::allocator<void> > BoundingBox;

typedef boost::shared_ptr< ::youbot_manipulation_vision::BoundingBox> BoundingBoxPtr;
typedef boost::shared_ptr< ::youbot_manipulation_vision::BoundingBox const> BoundingBoxConstPtr;


template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const  ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> & v)
{
  ros::message_operations::Printer< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> >::stream(s, "", v);
  return s;}

} // namespace youbot_manipulation_vision

namespace ros
{
namespace message_traits
{
template<class ContainerAllocator> struct IsMessage< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct IsMessage< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator>  const> : public TrueType {};
template<class ContainerAllocator>
struct MD5Sum< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> > {
  static const char* value() 
  {
    return "27ee999b462577e9eea47f8b009f88e8";
  }

  static const char* value(const  ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0x27ee999b462577e9ULL;
  static const uint64_t static_value2 = 0xeea47f8b009f88e8ULL;
};

template<class ContainerAllocator>
struct DataType< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> > {
  static const char* value() 
  {
    return "youbot_manipulation_vision/BoundingBox";
  }

  static const char* value(const  ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> > {
  static const char* value() 
  {
    return "#Top-left corner of the bounding box\n\
geometry_msgs/Point position\n\
\n\
#The width of the bounding box\n\
float64 width\n\
#The height of the bounding box\n\
float64 height\n\
================================================================================\n\
MSG: geometry_msgs/Point\n\
# This contains the position of a point in free space\n\
float64 x\n\
float64 y\n\
float64 z\n\
\n\
";
  }

  static const char* value(const  ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct IsFixedSize< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
    stream.next(m.position);
    stream.next(m.width);
    stream.next(m.height);
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct BoundingBox_
} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const  ::youbot_manipulation_vision::BoundingBox_<ContainerAllocator> & v) 
  {
    s << indent << "position: ";
s << std::endl;
    Printer< ::geometry_msgs::Point_<ContainerAllocator> >::stream(s, indent + "  ", v.position);
    s << indent << "width: ";
    Printer<double>::stream(s, indent + "  ", v.width);
    s << indent << "height: ";
    Printer<double>::stream(s, indent + "  ", v.height);
  }
};


} // namespace message_operations
} // namespace ros

#endif // YOUBOT_MANIPULATION_VISION_MESSAGE_BOUNDINGBOX_H

