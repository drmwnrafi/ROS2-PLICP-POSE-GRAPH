// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice

#ifndef WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__TRAITS_HPP_
#define WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "wheel_interfaces/msg/detail/wheel_infos__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace wheel_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const WheelInfos & msg,
  std::ostream & out)
{
  out << "{";
  // member: position
  {
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << ", ";
  }

  // member: current
  {
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
    out << ", ";
  }

  // member: rpm
  {
    out << "rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.rpm, out);
    out << ", ";
  }

  // member: cmd_value
  {
    if (msg.cmd_value.size() == 0) {
      out << "cmd_value: []";
    } else {
      out << "cmd_value: [";
      size_t pending_items = msg.cmd_value.size();
      for (auto item : msg.cmd_value) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const WheelInfos & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << "\n";
  }

  // member: current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
    out << "\n";
  }

  // member: rpm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.rpm, out);
    out << "\n";
  }

  // member: cmd_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.cmd_value.size() == 0) {
      out << "cmd_value: []\n";
    } else {
      out << "cmd_value:\n";
      for (auto item : msg.cmd_value) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const WheelInfos & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace wheel_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use wheel_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const wheel_interfaces::msg::WheelInfos & msg,
  std::ostream & out, size_t indentation = 0)
{
  wheel_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use wheel_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const wheel_interfaces::msg::WheelInfos & msg)
{
  return wheel_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<wheel_interfaces::msg::WheelInfos>()
{
  return "wheel_interfaces::msg::WheelInfos";
}

template<>
inline const char * name<wheel_interfaces::msg::WheelInfos>()
{
  return "wheel_interfaces/msg/WheelInfos";
}

template<>
struct has_fixed_size<wheel_interfaces::msg::WheelInfos>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<wheel_interfaces::msg::WheelInfos>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<wheel_interfaces::msg::WheelInfos>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__TRAITS_HPP_
