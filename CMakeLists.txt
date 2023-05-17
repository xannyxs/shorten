cmake_minimum_required(VERSION 3.25)
project(shorten)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror -pedantic")

set(SOURCE_FILES
        src/main.cpp src/videoFormatting.cpp src/utils.cpp src/uploadVideo.cpp)

set(TEST_FILES
        src/videoFormatting.cpp tests/videoFormatting_tests.cpp src/uploadVideo.cpp)

find_library(MAGIC_LIB magic)
if (NOT MAGIC_LIB)
    message(FATAL_ERROR "Library libmagic not found")
endif()

find_path(MAGIC_INCLUDE_DIR magic.h)
if (NOT MAGIC_INCLUDE_DIR)
    message(FATAL_ERROR "magic.h not found")
endif()

# specify the path to your venv
set(PYTHON_VENV_PATH "${CMAKE_SOURCE_DIR}/.venv")

# find the Python interpreter and libraries in the venv
set(Python3_ROOT_DIR "${PYTHON_VENV_PATH}")
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# add the Python include directories to your include path
include_directories(${MAGIC_INCLUDE_DIR} ${Python3_INCLUDE_DIRS})

# MAIN PROGRAM
add_executable(shorten ${SOURCE_FILES})
target_include_directories(shorten PRIVATE include)
target_link_libraries(shorten ${MAGIC_LIB} Python3::Python)

# TESTER
add_subdirectory(lib/Catch2)
add_executable(tester ${TEST_FILES})
target_link_libraries(tester PRIVATE Catch2::Catch2WithMain ${MAGIC_LIB} Python3::Python)
target_include_directories(tester PRIVATE include)
