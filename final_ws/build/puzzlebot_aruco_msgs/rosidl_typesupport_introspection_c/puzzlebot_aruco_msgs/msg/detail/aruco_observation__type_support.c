// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__rosidl_typesupport_introspection_c.h"
#include "puzzlebot_aruco_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__functions.h"
#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  puzzlebot_aruco_msgs__msg__ArucoObservation__init(message_memory);
}

void puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_fini_function(void * message_memory)
{
  puzzlebot_aruco_msgs__msg__ArucoObservation__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_member_array[3] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(puzzlebot_aruco_msgs__msg__ArucoObservation, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "distance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(puzzlebot_aruco_msgs__msg__ArucoObservation, distance),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(puzzlebot_aruco_msgs__msg__ArucoObservation, angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_members = {
  "puzzlebot_aruco_msgs__msg",  // message namespace
  "ArucoObservation",  // message name
  3,  // number of fields
  sizeof(puzzlebot_aruco_msgs__msg__ArucoObservation),
  puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_member_array,  // message members
  puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_init_function,  // function to initialize message memory (memory has to be allocated)
  puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_type_support_handle = {
  0,
  &puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_puzzlebot_aruco_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, puzzlebot_aruco_msgs, msg, ArucoObservation)() {
  if (!puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_type_support_handle.typesupport_identifier) {
    puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &puzzlebot_aruco_msgs__msg__ArucoObservation__rosidl_typesupport_introspection_c__ArucoObservation_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
