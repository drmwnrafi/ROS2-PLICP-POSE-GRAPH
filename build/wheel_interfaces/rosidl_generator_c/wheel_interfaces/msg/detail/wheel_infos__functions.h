// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from wheel_interfaces:msg/WheelInfos.idl
// generated code does not contain a copyright notice

#ifndef WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__FUNCTIONS_H_
#define WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "wheel_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "wheel_interfaces/msg/detail/wheel_infos__struct.h"

/// Initialize msg/WheelInfos message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * wheel_interfaces__msg__WheelInfos
 * )) before or use
 * wheel_interfaces__msg__WheelInfos__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
bool
wheel_interfaces__msg__WheelInfos__init(wheel_interfaces__msg__WheelInfos * msg);

/// Finalize msg/WheelInfos message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
void
wheel_interfaces__msg__WheelInfos__fini(wheel_interfaces__msg__WheelInfos * msg);

/// Create msg/WheelInfos message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * wheel_interfaces__msg__WheelInfos__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
wheel_interfaces__msg__WheelInfos *
wheel_interfaces__msg__WheelInfos__create();

/// Destroy msg/WheelInfos message.
/**
 * It calls
 * wheel_interfaces__msg__WheelInfos__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
void
wheel_interfaces__msg__WheelInfos__destroy(wheel_interfaces__msg__WheelInfos * msg);

/// Check for msg/WheelInfos message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
bool
wheel_interfaces__msg__WheelInfos__are_equal(const wheel_interfaces__msg__WheelInfos * lhs, const wheel_interfaces__msg__WheelInfos * rhs);

/// Copy a msg/WheelInfos message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
bool
wheel_interfaces__msg__WheelInfos__copy(
  const wheel_interfaces__msg__WheelInfos * input,
  wheel_interfaces__msg__WheelInfos * output);

/// Initialize array of msg/WheelInfos messages.
/**
 * It allocates the memory for the number of elements and calls
 * wheel_interfaces__msg__WheelInfos__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
bool
wheel_interfaces__msg__WheelInfos__Sequence__init(wheel_interfaces__msg__WheelInfos__Sequence * array, size_t size);

/// Finalize array of msg/WheelInfos messages.
/**
 * It calls
 * wheel_interfaces__msg__WheelInfos__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
void
wheel_interfaces__msg__WheelInfos__Sequence__fini(wheel_interfaces__msg__WheelInfos__Sequence * array);

/// Create array of msg/WheelInfos messages.
/**
 * It allocates the memory for the array and calls
 * wheel_interfaces__msg__WheelInfos__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
wheel_interfaces__msg__WheelInfos__Sequence *
wheel_interfaces__msg__WheelInfos__Sequence__create(size_t size);

/// Destroy array of msg/WheelInfos messages.
/**
 * It calls
 * wheel_interfaces__msg__WheelInfos__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
void
wheel_interfaces__msg__WheelInfos__Sequence__destroy(wheel_interfaces__msg__WheelInfos__Sequence * array);

/// Check for msg/WheelInfos message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
bool
wheel_interfaces__msg__WheelInfos__Sequence__are_equal(const wheel_interfaces__msg__WheelInfos__Sequence * lhs, const wheel_interfaces__msg__WheelInfos__Sequence * rhs);

/// Copy an array of msg/WheelInfos messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_wheel_interfaces
bool
wheel_interfaces__msg__WheelInfos__Sequence__copy(
  const wheel_interfaces__msg__WheelInfos__Sequence * input,
  wheel_interfaces__msg__WheelInfos__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // WHEEL_INTERFACES__MSG__DETAIL__WHEEL_INFOS__FUNCTIONS_H_
