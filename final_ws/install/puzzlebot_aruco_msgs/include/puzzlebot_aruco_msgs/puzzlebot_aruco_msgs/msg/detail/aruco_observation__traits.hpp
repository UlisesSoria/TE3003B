// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice

#ifndef PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__TRAITS_HPP_
#define PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace puzzlebot_aruco_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ArucoObservation & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: distance
  {
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << ", ";
  }

  // member: angle
  {
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ArucoObservation & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << "\n";
  }

  // member: angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ArucoObservation & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace puzzlebot_aruco_msgs

namespace rosidl_generator_traits
{

[[deprecated("use puzzlebot_aruco_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const puzzlebot_aruco_msgs::msg::ArucoObservation & msg,
  std::ostream & out, size_t indentation = 0)
{
  puzzlebot_aruco_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use puzzlebot_aruco_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const puzzlebot_aruco_msgs::msg::ArucoObservation & msg)
{
  return puzzlebot_aruco_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<puzzlebot_aruco_msgs::msg::ArucoObservation>()
{
  return "puzzlebot_aruco_msgs::msg::ArucoObservation";
}

template<>
inline const char * name<puzzlebot_aruco_msgs::msg::ArucoObservation>()
{
  return "puzzlebot_aruco_msgs/msg/ArucoObservation";
}

template<>
struct has_fixed_size<puzzlebot_aruco_msgs::msg::ArucoObservation>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<puzzlebot_aruco_msgs::msg::ArucoObservation>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<puzzlebot_aruco_msgs::msg::ArucoObservation>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__TRAITS_HPP_
