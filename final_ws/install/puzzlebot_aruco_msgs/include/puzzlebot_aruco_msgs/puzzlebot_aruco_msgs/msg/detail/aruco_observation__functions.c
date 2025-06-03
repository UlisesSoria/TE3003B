// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from puzzlebot_aruco_msgs:msg/ArucoObservation.idl
// generated code does not contain a copyright notice
#include "puzzlebot_aruco_msgs/msg/detail/aruco_observation__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
puzzlebot_aruco_msgs__msg__ArucoObservation__init(puzzlebot_aruco_msgs__msg__ArucoObservation * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // distance
  // angle
  return true;
}

void
puzzlebot_aruco_msgs__msg__ArucoObservation__fini(puzzlebot_aruco_msgs__msg__ArucoObservation * msg)
{
  if (!msg) {
    return;
  }
  // id
  // distance
  // angle
}

bool
puzzlebot_aruco_msgs__msg__ArucoObservation__are_equal(const puzzlebot_aruco_msgs__msg__ArucoObservation * lhs, const puzzlebot_aruco_msgs__msg__ArucoObservation * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // distance
  if (lhs->distance != rhs->distance) {
    return false;
  }
  // angle
  if (lhs->angle != rhs->angle) {
    return false;
  }
  return true;
}

bool
puzzlebot_aruco_msgs__msg__ArucoObservation__copy(
  const puzzlebot_aruco_msgs__msg__ArucoObservation * input,
  puzzlebot_aruco_msgs__msg__ArucoObservation * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // distance
  output->distance = input->distance;
  // angle
  output->angle = input->angle;
  return true;
}

puzzlebot_aruco_msgs__msg__ArucoObservation *
puzzlebot_aruco_msgs__msg__ArucoObservation__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  puzzlebot_aruco_msgs__msg__ArucoObservation * msg = (puzzlebot_aruco_msgs__msg__ArucoObservation *)allocator.allocate(sizeof(puzzlebot_aruco_msgs__msg__ArucoObservation), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(puzzlebot_aruco_msgs__msg__ArucoObservation));
  bool success = puzzlebot_aruco_msgs__msg__ArucoObservation__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
puzzlebot_aruco_msgs__msg__ArucoObservation__destroy(puzzlebot_aruco_msgs__msg__ArucoObservation * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    puzzlebot_aruco_msgs__msg__ArucoObservation__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__init(puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  puzzlebot_aruco_msgs__msg__ArucoObservation * data = NULL;

  if (size) {
    data = (puzzlebot_aruco_msgs__msg__ArucoObservation *)allocator.zero_allocate(size, sizeof(puzzlebot_aruco_msgs__msg__ArucoObservation), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = puzzlebot_aruco_msgs__msg__ArucoObservation__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        puzzlebot_aruco_msgs__msg__ArucoObservation__fini(&data[i - 1]);
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
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__fini(puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * array)
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
      puzzlebot_aruco_msgs__msg__ArucoObservation__fini(&array->data[i]);
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

puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence *
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * array = (puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence *)allocator.allocate(sizeof(puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__destroy(puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__are_equal(const puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * lhs, const puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!puzzlebot_aruco_msgs__msg__ArucoObservation__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence__copy(
  const puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * input,
  puzzlebot_aruco_msgs__msg__ArucoObservation__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(puzzlebot_aruco_msgs__msg__ArucoObservation);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    puzzlebot_aruco_msgs__msg__ArucoObservation * data =
      (puzzlebot_aruco_msgs__msg__ArucoObservation *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!puzzlebot_aruco_msgs__msg__ArucoObservation__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          puzzlebot_aruco_msgs__msg__ArucoObservation__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!puzzlebot_aruco_msgs__msg__ArucoObservation__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
