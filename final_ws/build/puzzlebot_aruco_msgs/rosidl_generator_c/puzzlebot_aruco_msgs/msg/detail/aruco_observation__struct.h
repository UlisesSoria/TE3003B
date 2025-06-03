// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice

#ifndef PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__STRUCT_H_
#define PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ArucoObservation in the package puzzlebot_aruco_msgs.
typedef struct puzzlebot_aruco_msgs__msg__ArucoObservation
{
  int32_t id;
  float distance;
  float angle;
} puzzlebot_aruco_msgs__msg__ArucoObservation;

// Struct for a sequence of puzzlebot_aruco_msgs__msg__ArucoObservation.
typedef struct puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence
{
  puzzlebot_aruco_msgs__msg__ArucoObservation * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__STRUCT_H_
