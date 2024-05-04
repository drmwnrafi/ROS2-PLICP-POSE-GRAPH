// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice

#ifndef WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "wheel_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "wheel_interfaces/msg/detail/wheel_infos__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace wheel_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_wheel_interfaces
cdr_serialize(
  const wheel_interfaces::msg::WheelInfos & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_wheel_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  wheel_interfaces::msg::WheelInfos & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_wheel_interfaces
get_serialized_size(
  const wheel_interfaces::msg::WheelInfos & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_wheel_interfaces
max_serialized_size_WheelInfos(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace wheel_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_wheel_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, wheel_interfaces, msg, WheelInfos)();

#ifdef __cplusplus
}
#endif

#endif  // WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
