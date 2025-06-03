// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice

#ifndef PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__BUILDER_HPP_
#define PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace puzzlebot_aruco_msgs
{

namespace msg
{

namespace builder
{

class Init_ArucoObservation_angle
{
public:
  explicit Init_ArucoObservation_angle(::puzzlebot_aruco_msgs::msg::ArucoObservation & msg)
  : msg_(msg)
  {}
  ::puzzlebot_aruco_msgs::msg::ArucoObservation angle(::puzzlebot_aruco_msgs::msg::ArucoObservation::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::puzzlebot_aruco_msgs::msg::ArucoObservation msg_;
};

class Init_ArucoObservation_distance
{
public:
  explicit Init_ArucoObservation_distance(::puzzlebot_aruco_msgs::msg::ArucoObservation & msg)
  : msg_(msg)
  {}
  Init_ArucoObservation_angle distance(::puzzlebot_aruco_msgs::msg::ArucoObservation::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return Init_ArucoObservation_angle(msg_);
  }

private:
  ::puzzlebot_aruco_msgs::msg::ArucoObservation msg_;
};

class Init_ArucoObservation_id
{
public:
  Init_ArucoObservation_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArucoObservation_distance id(::puzzlebot_aruco_msgs::msg::ArucoObservation::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_ArucoObservation_distance(msg_);
  }

private:
  ::puzzlebot_aruco_msgs::msg::ArucoObservation msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::puzzlebot_aruco_msgs::msg::ArucoObservation>()
{
  return puzzlebot_aruco_msgs::msg::builder::Init_ArucoObservation_id();
}

}  // namespace puzzlebot_aruco_msgs

#endif  // PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__BUILDER_HPP_
