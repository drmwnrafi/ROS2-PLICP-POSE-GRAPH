// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice

#ifndef WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__STRUCT_HPP_
#define WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__wheel_interfaces__msg__WheelInfos __attribute__((deprecated))
#else
# define DEPRECATED__wheel_interfaces__msg__WheelInfos __declspec(deprecated)
#endif

namespace wheel_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct WheelInfos_
{
  using Type = WheelInfos_<ContainerAllocator>;

  explicit WheelInfos_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->position = 0l;
      this->current = 0l;
      this->rpm = 0l;
    }
  }

  explicit WheelInfos_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->position = 0l;
      this->current = 0l;
      this->rpm = 0l;
    }
  }

  // field types and members
  using _position_type =
    int32_t;
  _position_type position;
  using _current_type =
    int32_t;
  _current_type current;
  using _rpm_type =
    int32_t;
  _rpm_type rpm;
  using _cmd_value_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _cmd_value_type cmd_value;

  // setters for named parameter idiom
  Type & set__position(
    const int32_t & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__current(
    const int32_t & _arg)
  {
    this->current = _arg;
    return *this;
  }
  Type & set__rpm(
    const int32_t & _arg)
  {
    this->rpm = _arg;
    return *this;
  }
  Type & set__cmd_value(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->cmd_value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    wheel_interfaces::msg::WheelInfos_<ContainerAllocator> *;
  using ConstRawPtr =
    const wheel_interfaces::msg::WheelInfos_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      wheel_interfaces::msg::WheelInfos_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      wheel_interfaces::msg::WheelInfos_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__wheel_interfaces__msg__WheelInfos
    std::shared_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__wheel_interfaces__msg__WheelInfos
    std::shared_ptr<wheel_interfaces::msg::WheelInfos_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const WheelInfos_ & other) const
  {
    if (this->position != other.position) {
      return false;
    }
    if (this->current != other.current) {
      return false;
    }
    if (this->rpm != other.rpm) {
      return false;
    }
    if (this->cmd_value != other.cmd_value) {
      return false;
    }
    return true;
  }
  bool operator!=(const WheelInfos_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct WheelInfos_

// alias to use template instance with default allocator
using WheelInfos =
  wheel_interfaces::msg::WheelInfos_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace wheel_interfaces

#endif  // WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__STRUCT_HPP_
