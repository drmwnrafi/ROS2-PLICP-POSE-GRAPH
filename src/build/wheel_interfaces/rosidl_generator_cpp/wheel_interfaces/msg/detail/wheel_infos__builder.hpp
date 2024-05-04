// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice

#ifndef WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__BUILDER_HPP_
#define WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "wheel_interfaces/msg/detail/wheel_infos__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace wheel_interfaces
{

namespace msg
{

namespace builder
{

class Init_WheelInfos_cmd_value
{
public:
  explicit Init_WheelInfos_cmd_value(::wheel_interfaces::msg::WheelInfos & msg)
  : msg_(msg)
  {}
  ::wheel_interfaces::msg::WheelInfos cmd_value(::wheel_interfaces::msg::WheelInfos::_cmd_value_type arg)
  {
    msg_.cmd_value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::wheel_interfaces::msg::WheelInfos msg_;
};

class Init_WheelInfos_rpm
{
public:
  explicit Init_WheelInfos_rpm(::wheel_interfaces::msg::WheelInfos & msg)
  : msg_(msg)
  {}
  Init_WheelInfos_cmd_value rpm(::wheel_interfaces::msg::WheelInfos::_rpm_type arg)
  {
    msg_.rpm = std::move(arg);
    return Init_WheelInfos_cmd_value(msg_);
  }

private:
  ::wheel_interfaces::msg::WheelInfos msg_;
};

class Init_WheelInfos_current
{
public:
  explicit Init_WheelInfos_current(::wheel_interfaces::msg::WheelInfos & msg)
  : msg_(msg)
  {}
  Init_WheelInfos_rpm current(::wheel_interfaces::msg::WheelInfos::_current_type arg)
  {
    msg_.current = std::move(arg);
    return Init_WheelInfos_rpm(msg_);
  }

private:
  ::wheel_interfaces::msg::WheelInfos msg_;
};

class Init_WheelInfos_position
{
public:
  Init_WheelInfos_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_WheelInfos_current position(::wheel_interfaces::msg::WheelInfos::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_WheelInfos_current(msg_);
  }

private:
  ::wheel_interfaces::msg::WheelInfos msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::wheel_interfaces::msg::WheelInfos>()
{
  return wheel_interfaces::msg::builder::Init_WheelInfos_position();
}

}  // namespace wheel_interfaces

#endif  // WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__BUILDER_HPP_
