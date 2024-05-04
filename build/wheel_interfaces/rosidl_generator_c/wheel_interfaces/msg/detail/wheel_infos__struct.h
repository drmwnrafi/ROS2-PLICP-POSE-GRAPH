// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice

#ifndef WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__STRUCT_H_
#define WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'cmd_value'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/WheelInfos in the package wheel_interfaces.
typedef struct wheel_interfaces__msg__WheelInfos
{
  int32_t position;
  int32_t current;
  int32_t rpm;
  rosidl_runtime_c__int32__Sequence cmd_value;
} wheel_interfaces__msg__WheelInfos;

// Struct for a sequence of wheel_interfaces__msg__WheelInfos.
typedef struct wheel_interfaces__msg__WheelInfos__Sequence
{
  wheel_interfaces__msg__WheelInfos * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} wheel_interfaces__msg__WheelInfos__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__STRUCT_H_
