# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_occupancy_grid_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED occupancy_grid_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(occupancy_grid_FOUND FALSE)
  elseif(NOT occupancy_grid_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(occupancy_grid_FOUND FALSE)
  endif()
  return()
endif()
set(_occupancy_grid_CONFIG_INCLUDED TRUE)

# output package information
if(NOT occupancy_grid_FIND_QUIETLY)
  message(STATUS "Found occupancy_grid: 0.0.1 (${occupancy_grid_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'occupancy_grid' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${occupancy_grid_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(occupancy_grid_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${occupancy_grid_DIR}/${_extra}")
endforeach()
