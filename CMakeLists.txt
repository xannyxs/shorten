cmake_minimum_required(VERSION 3.18)
project(shorten)

set(CMAKE_CXX_STANDARD 20)

find_package(CURL REQUIRED)
if(NOT CURL_FOUND)
    message(FATAL_ERROR "CURL library not found.")
endif()

set(SOURCE_FILES
        src/main.cpp src/videoFormatting.cpp src/utils.cpp src/uploadVideo.cpp src/Livepeer/Livepeer.cpp)

set(TEST_FILES
        src/videoFormatting.cpp tests/videoFormatting_tests.cpp src/uploadVideo.cpp tests/LivepeerTests.cpp src/Livepeer/Livepeer.cpp)

if(CMAKE_BUILD_TYPE MATCHES Debug)
    add_compile_definitions(DEBUG=1)
else()
    add_compile_definitions(DEBUG=0)
endif()

find_library(MAGIC_LIB magic)
if (NOT MAGIC_LIB)
    message(FATAL_ERROR "Library libmagic not found")
endif()

find_path(MAGIC_INCLUDE_DIR magic.h)
if (NOT MAGIC_INCLUDE_DIR)
    message(FATAL_ERROR "magic.h not found")
endif()

# MAIN PROGRAM
add_executable(shorten ${SOURCE_FILES})
target_include_directories(shorten PRIVATE include ${CURL_INCLUDE_DIR} ${MAGIC_INCLUDE_DIR})
target_link_libraries(shorten ${MAGIC_LIB} ${CURL_LIBRARIES})
target_compile_options(shorten PRIVATE -Wall -Wextra -Werror -pedantic)

# TESTER
add_subdirectory(lib/Catch2)
add_subdirectory(lib/trompeloeil)
add_executable(tester ${TEST_FILES})
target_link_libraries(tester PRIVATE ${MAGIC_LIB} Catch2::Catch2WithMain trompeloeil ${CURL_LIBRARIES})
target_include_directories(tester PRIVATE include src/Livepeer ${MAGIC_INCLUDE_DIR})
target_compile_options(tester PRIVATE -Wall -Wextra -Werror -pedantic)
