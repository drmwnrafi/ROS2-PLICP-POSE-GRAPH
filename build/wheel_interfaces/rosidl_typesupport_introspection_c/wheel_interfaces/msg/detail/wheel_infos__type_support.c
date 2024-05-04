// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "wheel_interfaces/msg/detail/wheel_infos__rosidl_typesupport_introspection_c.h"
#include "wheel_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "wheel_interfaces/msg/detail/wheel_infos__functions.h"
#include "wheel_interfaces/msg/detail/wheel_infos__struct.h"


// Include directives for member types
// Member `cmd_value`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  wheel_interfaces__msg__WheelInfos__init(message_memory);
}

void wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_fini_function(void * message_memory)
{
  wheel_interfaces__msg__WheelInfos__fini(message_memory);
}

size_t wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__size_function__WheelInfos__cmd_value(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__get_const_function__WheelInfos__cmd_value(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__get_function__WheelInfos__cmd_value(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__fetch_function__WheelInfos__cmd_value(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__get_const_function__WheelInfos__cmd_value(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__assign_function__WheelInfos__cmd_value(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__get_function__WheelInfos__cmd_value(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__resize_function__WheelInfos__cmd_value(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_member_array[4] = {
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(wheel_interfaces__msg__WheelInfos, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "current",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(wheel_interfaces__msg__WheelInfos, current),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "rpm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(wheel_interfaces__msg__WheelInfos, rpm),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "cmd_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(wheel_interfaces__msg__WheelInfos, cmd_value),  // bytes offset in struct
    NULL,  // default value
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__size_function__WheelInfos__cmd_value,  // size() function pointer
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__get_const_function__WheelInfos__cmd_value,  // get_const(index) function pointer
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__get_function__WheelInfos__cmd_value,  // get(index) function pointer
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__fetch_function__WheelInfos__cmd_value,  // fetch(index, &value) function pointer
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__assign_function__WheelInfos__cmd_value,  // assign(index, value) function pointer
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__resize_function__WheelInfos__cmd_value  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_members = {
  "wheel_interfaces__msg",  // message namespace
  "WheelInfos",  // message name
  4,  // number of fields
  sizeof(wheel_interfaces__msg__WheelInfos),
  wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_member_array,  // message members
  wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_init_function,  // function to initialize message memory (memory has to be allocated)
  wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_type_support_handle = {
  0,
  &wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_wheel_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, wheel_interfaces, msg, WheelInfos)() {
  if (!wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_type_support_handle.typesupport_identifier) {
    wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &wheel_interfaces__msg__WheelInfos__rosidl_typesupport_introspection_c__WheelInfos_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
