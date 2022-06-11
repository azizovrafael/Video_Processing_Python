cmake_minimum_required(VERSION 3.1.0)

project(zerhacken)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

if(CMAKE_VERSION VERSION_LESS "3.7.0")
  set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()

find_package(Qt5 COMPONENTS Widgets WebEngineWidgets QuickWidgets REQUIRED)

add_executable(zerhacken main.cpp)

target_link_libraries(zerhacken Qt5::Widgets Qt5::WebEngineWidgets Qt5::QuickWidgets)
