// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice
#include "wheel_interfaces/msg/detail/wheel_infos__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `cmd_value`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
wheel_interfaces__msg__WheelInfos__init(wheel_interfaces__msg__WheelInfos * msg)
{
  if (!msg) {
    return false;
  }
  // position
  // current
  // rpm
  // cmd_value
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->cmd_value, 0)) {
    wheel_interfaces__msg__WheelInfos__fini(msg);
    return false;
  }
  return true;
}

void
wheel_interfaces__msg__WheelInfos__fini(wheel_interfaces__msg__WheelInfos * msg)
{
  if (!msg) {
    return;
  }
  // position
  // current
  // rpm
  // cmd_value
  rosidl_runtime_c__int32__Sequence__fini(&msg->cmd_value);
}

bool
wheel_interfaces__msg__WheelInfos__are_equal(const wheel_interfaces__msg__WheelInfos * lhs, const wheel_interfaces__msg__WheelInfos * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // position
  if (lhs->position != rhs->position) {
    return false;
  }
  // current
  if (lhs->current != rhs->current) {
    return false;
  }
  // rpm
  if (lhs->rpm != rhs->rpm) {
    return false;
  }
  // cmd_value
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->cmd_value), &(rhs->cmd_value)))
  {
    return false;
  }
  return true;
}

bool
wheel_interfaces__msg__WheelInfos__copy(
  const wheel_interfaces__msg__WheelInfos * input,
  wheel_interfaces__msg__WheelInfos * output)
{
  if (!input || !output) {
    return false;
  }
  // position
  output->position = input->position;
  // current
  output->current = input->current;
  // rpm
  output->rpm = input->rpm;
  // cmd_value
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->cmd_value), &(output->cmd_value)))
  {
    return false;
  }
  return true;
}

wheel_interfaces__msg__WheelInfos *
wheel_interfaces__msg__WheelInfos__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  wheel_interfaces__msg__WheelInfos * msg = (wheel_interfaces__msg__WheelInfos *)allocator.allocate(sizeof(wheel_interfaces__msg__WheelInfos), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(wheel_interfaces__msg__WheelInfos));
  bool success = wheel_interfaces__msg__WheelInfos__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
wheel_interfaces__msg__WheelInfos__destroy(wheel_interfaces__msg__WheelInfos * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    wheel_interfaces__msg__WheelInfos__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
wheel_interfaces__msg__WheelInfos__Sequence__init(wheel_interfaces__msg__WheelInfos__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  wheel_interfaces__msg__WheelInfos * data = NULL;

  if (size) {
    data = (wheel_interfaces__msg__WheelInfos *)allocator.zero_allocate(size, sizeof(wheel_interfaces__msg__WheelInfos), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = wheel_interfaces__msg__WheelInfos__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        wheel_interfaces__msg__WheelInfos__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
wheel_interfaces__msg__WheelInfos__Sequence__fini(wheel_interfaces__msg__WheelInfos__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      wheel_interfaces__msg__WheelInfos__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

wheel_interfaces__msg__WheelInfos__Sequence *
wheel_interfaces__msg__WheelInfos__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  wheel_interfaces__msg__WheelInfos__Sequence * array = (wheel_interfaces__msg__WheelInfos__Sequence *)allocator.allocate(sizeof(wheel_interfaces__msg__WheelInfos__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = wheel_interfaces__msg__WheelInfos__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
wheel_interfaces__msg__WheelInfos__Sequence__destroy(wheel_interfaces__msg__WheelInfos__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    wheel_interfaces__msg__WheelInfos__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
wheel_interfaces__msg__WheelInfos__Sequence__are_equal(const wheel_interfaces__msg__WheelInfos__Sequence * lhs, const wheel_interfaces__msg__WheelInfos__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!wheel_interfaces__msg__WheelInfos__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
wheel_interfaces__msg__WheelInfos__Sequence__copy(
  const wheel_interfaces__msg__WheelInfos__Sequence * input,
  wheel_interfaces__msg__WheelInfos__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(wheel_interfaces__msg__WheelInfos);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    wheel_interfaces__msg__WheelInfos * data =
      (wheel_interfaces__msg__WheelInfos *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!wheel_interfaces__msg__WheelInfos__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          wheel_interfaces__msg__WheelInfos__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!wheel_interfaces__msg__WheelInfos__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
