# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ziczac/dev/skripsi_code/ros2_workspace/build/serial

# Include any dependencies generated for this target.
include CMakeFiles/serial.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/serial.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/serial.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/serial.dir/flags.make

CMakeFiles/serial.dir/src/serial.cc.o: CMakeFiles/serial.dir/flags.make
CMakeFiles/serial.dir/src/serial.cc.o: /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/serial.cc
CMakeFiles/serial.dir/src/serial.cc.o: CMakeFiles/serial.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ziczac/dev/skripsi_code/ros2_workspace/build/serial/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/serial.dir/src/serial.cc.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/serial.dir/src/serial.cc.o -MF CMakeFiles/serial.dir/src/serial.cc.o.d -o CMakeFiles/serial.dir/src/serial.cc.o -c /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/serial.cc

CMakeFiles/serial.dir/src/serial.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/serial.dir/src/serial.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/serial.cc > CMakeFiles/serial.dir/src/serial.cc.i

CMakeFiles/serial.dir/src/serial.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/serial.dir/src/serial.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/serial.cc -o CMakeFiles/serial.dir/src/serial.cc.s

CMakeFiles/serial.dir/src/impl/unix.cc.o: CMakeFiles/serial.dir/flags.make
CMakeFiles/serial.dir/src/impl/unix.cc.o: /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/unix.cc
CMakeFiles/serial.dir/src/impl/unix.cc.o: CMakeFiles/serial.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ziczac/dev/skripsi_code/ros2_workspace/build/serial/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/serial.dir/src/impl/unix.cc.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/serial.dir/src/impl/unix.cc.o -MF CMakeFiles/serial.dir/src/impl/unix.cc.o.d -o CMakeFiles/serial.dir/src/impl/unix.cc.o -c /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/unix.cc

CMakeFiles/serial.dir/src/impl/unix.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/serial.dir/src/impl/unix.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/unix.cc > CMakeFiles/serial.dir/src/impl/unix.cc.i

CMakeFiles/serial.dir/src/impl/unix.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/serial.dir/src/impl/unix.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/unix.cc -o CMakeFiles/serial.dir/src/impl/unix.cc.s

CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o: CMakeFiles/serial.dir/flags.make
CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o: /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/list_ports/list_ports_linux.cc
CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o: CMakeFiles/serial.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ziczac/dev/skripsi_code/ros2_workspace/build/serial/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o -MF CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o.d -o CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o -c /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/list_ports/list_ports_linux.cc

CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/list_ports/list_ports_linux.cc > CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.i

CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2/src/impl/list_ports/list_ports_linux.cc -o CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.s

# Object files for target serial
serial_OBJECTS = \
"CMakeFiles/serial.dir/src/serial.cc.o" \
"CMakeFiles/serial.dir/src/impl/unix.cc.o" \
"CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o"

# External object files for target serial
serial_EXTERNAL_OBJECTS =

libserial.a: CMakeFiles/serial.dir/src/serial.cc.o
libserial.a: CMakeFiles/serial.dir/src/impl/unix.cc.o
libserial.a: CMakeFiles/serial.dir/src/impl/list_ports/list_ports_linux.cc.o
libserial.a: CMakeFiles/serial.dir/build.make
libserial.a: CMakeFiles/serial.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ziczac/dev/skripsi_code/ros2_workspace/build/serial/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX static library libserial.a"
	$(CMAKE_COMMAND) -P CMakeFiles/serial.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/serial.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/serial.dir/build: libserial.a
.PHONY : CMakeFiles/serial.dir/build

CMakeFiles/serial.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/serial.dir/cmake_clean.cmake
.PHONY : CMakeFiles/serial.dir/clean

CMakeFiles/serial.dir/depend:
	cd /home/ziczac/dev/skripsi_code/ros2_workspace/build/serial && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2 /home/ziczac/dev/skripsi_code/ros2_workspace/src/serial-ros2 /home/ziczac/dev/skripsi_code/ros2_workspace/build/serial /home/ziczac/dev/skripsi_code/ros2_workspace/build/serial /home/ziczac/dev/skripsi_code/ros2_workspace/build/serial/CMakeFiles/serial.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/serial.dir/depend
