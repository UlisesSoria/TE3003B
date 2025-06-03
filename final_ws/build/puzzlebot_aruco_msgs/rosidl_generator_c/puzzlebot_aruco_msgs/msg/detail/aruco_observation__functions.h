// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice

#ifndef PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__FUNCTIONS_H_
#define PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "puzzlebot_aruco_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__struct.h"

/// Initialize msg/ArucoObservation message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * puzzlebot_aruco_msgs__msg__ArucoObservation
 * )) before or use
 * puzzlebot_aruco_msgs__msg__ArucoObservation__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
bool
puzzlebot_aruco_msgs__msg__ArucoObservation__init(puzzlebot_aruco_msgs__msg__ArucoObservation * msg);

/// Finalize msg/ArucoObservation message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
void
puzzlebot_aruco_msgs__msg__ArucoObservation__fini(puzzlebot_aruco_msgs__msg__ArucoObservation * msg);

/// Create msg/ArucoObservation message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * puzzlebot_aruco_msgs__msg__ArucoObservation__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
puzzlebot_aruco_msgs__msg__ArucoObservation *
puzzlebot_aruco_msgs__msg__ArucoObservation__create();

/// Destroy msg/ArucoObservation message.
/**
 * It calls
 * puzzlebot_aruco_msgs__msg__ArucoObservation__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
void
puzzlebot_aruco_msgs__msg__ArucoObservation__destroy(puzzlebot_aruco_msgs__msg__ArucoObservation * msg);

/// Check for msg/ArucoObservation message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
bool
puzzlebot_aruco_msgs__msg__ArucoObservation__are_equal(const puzzlebot_aruco_msgs__msg__ArucoObservation * lhs, const puzzlebot_aruco_msgs__msg__ArucoObservation * rhs);

/// Copy a msg/ArucoObservation message.
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
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
bool
puzzlebot_aruco_msgs__msg__ArucoObservation__copy(
  const puzzlebot_aruco_msgs__msg__ArucoObservation * input,
  puzzlebot_aruco_msgs__msg__ArucoObservation * output);

/// Initialize array of msg/ArucoObservation messages.
/**
 * It allocates the memory for the number of elements and calls
 * puzzlebot_aruco_msgs__msg__ArucoObservation__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
bool
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__init(puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * array, size_t size);

/// Finalize array of msg/ArucoObservation messages.
/**
 * It calls
 * puzzlebot_aruco_msgs__msg__ArucoObservation__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
void
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__fini(puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * array);

/// Create array of msg/ArucoObservation messages.
/**
 * It allocates the memory for the array and calls
 * puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence *
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__create(size_t size);

/// Destroy array of msg/ArucoObservation messages.
/**
 * It calls
 * puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
void
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__destroy(puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * array);

/// Check for msg/ArucoObservation message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
bool
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__are_equal(const puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * lhs, const puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * rhs);

/// Copy an array of msg/ArucoObservation messages.
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
ROSIDL_GENERATOR_C_PUBLIC_puzzlebot_aruco_msgs
bool
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__copy(
  const puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * input,
  puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__FUNCTIONS_H_
