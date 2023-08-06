cmake_minimum_required(VERSION 2.8.3)

project(dynamic-fba)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-Wno-deprecated-register" )

################### Find pybind11

set(PYBIND11_PYTHON_VERSION 3)
find_package(pybind11 REQUIRED)

################### Set path for custom FindModules

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

################### Find glpk packages

FIND_PACKAGE(GLPK REQUIRED)
message(STATUS "GLPK_LIBRARIES = ${GLPK_LIBRARIES}")
message(STATUS "GLPK_INCLUDE_DIRS = ${GLPK_INCLUDE_DIRS}")

################### Find sundials packages

FIND_PACKAGE(SUNDIALS REQUIRED)
message(STATUS "SUNDIALS_LIBRARIES = ${SUNDIALS_LIBRARIES}")
message(STATUS "SUNDIALS_INCLUDE_DIR = ${SUNDIALS_INCLUDE_DIR}")

################### Include directories and libraries

INCLUDE_DIRECTORIES(${GLPK_INCLUDE_DIRS} ${SUNDIALS_INCLUDE_DIR})
LINK_LIBRARIES(${GLPK_LIBRARIES} ${SUNDIALS_LIBRARIES})

################### Source files

set(SRC ./src/extension/)
AUX_SOURCE_DIRECTORY(${SRC}/emblp/ EMBLP_FILES)
AUX_SOURCE_DIRECTORY(${SRC}/methods/ METHOD_FILES)
set(MODULE_FILES ${SRC}dfba_utils.cpp ${EMBLP_FILES} ${METHOD_FILES})

################### Build module

pybind11_add_module(dfba_utils ${MODULE_FILES})
