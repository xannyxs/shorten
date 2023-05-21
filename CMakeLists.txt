cmake_minimum_required(VERSION 3.18)
project(shorten)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror -pedantic")

find_package(CURL REQUIRED)
if(NOT CURL_FOUND)
    message(FATAL_ERROR "CURL library not found.")
endif()

set(SOURCE_FILES
        src/main.cpp src/videoFormatting.cpp src/utils.cpp src/uploadVideo.cpp src/Livepeer/livepeer.cpp)

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

# add the Python include directories to your include path
include_directories(${MAGIC_INCLUDE_DIR})

# MAIN PROGRAM
add_executable(shorten ${SOURCE_FILES})
target_include_directories(shorten PRIVATE include ${CURL_INCLUDE_DIR})
target_link_libraries(shorten ${MAGIC_LIB} ${CURL_LIBRARIES})

# TESTER
add_subdirectory(lib/Catch2)
add_executable(tester ${TEST_FILES})
target_link_libraries(tester PRIVATE ${MAGIC_LIB} Catch2::Catch2WithMain)
target_include_directories(tester PRIVATE include)
