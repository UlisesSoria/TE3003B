// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice

#ifndef PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__STRUCT_HPP_
#define PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__puzzlebot_aruco_msgs__msg__ArucoObservation __attribute__((deprecated))
#else
# define DEPRECATED__puzzlebot_aruco_msgs__msg__ArucoObservation __declspec(deprecated)
#endif

namespace puzzlebot_aruco_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ArucoObservation_
{
  using Type = ArucoObservation_<ContainerAllocator>;

  explicit ArucoObservation_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->distance = 0.0f;
      this->angle = 0.0f;
    }
  }

  explicit ArucoObservation_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->distance = 0.0f;
      this->angle = 0.0f;
    }
  }

  // field types and members
  using _id_type =
    int32_t;
  _id_type id;
  using _distance_type =
    float;
  _distance_type distance;
  using _angle_type =
    float;
  _angle_type angle;

  // setters for named parameter idiom
  Type & set__id(
    const int32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__distance(
    const float & _arg)
  {
    this->distance = _arg;
    return *this;
  }
  Type & set__angle(
    const float & _arg)
  {
    this->angle = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator> *;
  using ConstRawPtr =
    const puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__puzzlebot_aruco_msgs__msg__ArucoObservation
    std::shared_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__puzzlebot_aruco_msgs__msg__ArucoObservation
    std::shared_ptr<puzzlebot_aruco_msgs::msg::ArucoObservation_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ArucoObservation_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->distance != other.distance) {
      return false;
    }
    if (this->angle != other.angle) {
      return false;
    }
    return true;
  }
  bool operator!=(const ArucoObservation_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ArucoObservation_

// alias to use template instance with default allocator
using ArucoObservation =
  puzzlebot_aruco_msgs::msg::ArucoObservation_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace puzzlebot_aruco_msgs

#endif  // PUZZLEBOT_ARUCO_MSGS__MSG__DETAIL__ARUCO_OBSERVATION__STRUCT_HPP_
