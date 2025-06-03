// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace puzzlebot_aruco_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ArucoObservation_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) puzzlebot_aruco_msgs::msg::ArucoObservation(_init);
}

void ArucoObservation_fini_function(void * message_memory)
{
  auto typed_message = static_cast<puzzlebot_aruco_msgs::msg::ArucoObservation *>(message_memory);
  typed_message->~ArucoObservation();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ArucoObservation_message_member_array[3] = {
  {
    "id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(puzzlebot_aruco_msgs::msg::ArucoObservation, id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "distance",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(puzzlebot_aruco_msgs::msg::ArucoObservation, distance),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "angle",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(puzzlebot_aruco_msgs::msg::ArucoObservation, angle),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ArucoObservation_message_members = {
  "puzzlebot_aruco_msgs::msg",  // message namespace
  "ArucoObservation",  // message name
  3,  // number of fields
  sizeof(puzzlebot_aruco_msgs::msg::ArucoObservation),
  ArucoObservation_message_member_array,  // message members
  ArucoObservation_init_function,  // function to initialize message memory (memory has to be allocated)
  ArucoObservation_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ArucoObservation_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ArucoObservation_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace puzzlebot_aruco_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<puzzlebot_aruco_msgs::msg::ArucoObservation>()
{
  return &::puzzlebot_aruco_msgs::msg::rosidl_typesupport_introspection_cpp::ArucoObservation_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, puzzlebot_aruco_msgs, msg, ArucoObservation)() {
  return &::puzzlebot_aruco_msgs::msg::rosidl_typesupport_introspection_cpp::ArucoObservation_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
