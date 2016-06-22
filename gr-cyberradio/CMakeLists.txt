# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.


########################################################################
# Project setup
########################################################################
cmake_minimum_required(VERSION 2.6)

if("${PACKAGE_VERSION}" STREQUAL "")
   set(PACKAGE_VERSION "1.0.0")
endif("${PACKAGE_VERSION}" STREQUAL "")

project(gr-cyberradio CXX C)
set(PROJECT_NAME "CyberRadio")
set(PROJECT_VERSION ${PACKAGE_VERSION})
enable_testing()

#select the release build type by default to get optimization flags
if(NOT CMAKE_BUILD_TYPE)
   set(CMAKE_BUILD_TYPE "Release")
   message(STATUS "Build type not specified: defaulting to release.")
endif(NOT CMAKE_BUILD_TYPE)
set(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "")

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/Modules)

########################################################################
# Compiler specific setup
########################################################################
if(CMAKE_COMPILER_IS_GNUCXX AND NOT WIN32)
    #http://gcc.gnu.org/wiki/Visibility
    add_definitions(-fvisibility=hidden)
endif()

########################################################################
# Find boost
########################################################################
if(UNIX AND EXISTS "/usr/lib64")
    list(APPEND BOOST_LIBRARYDIR "/usr/lib64") #fedora 64-bit fix
    set(Boost_USE_MULTITHREADED False) # CentOS 6 64-bit fix
endif(UNIX AND EXISTS "/usr/lib64")
set(Boost_ADDITIONAL_VERSIONS
    "1.35.0" "1.35" "1.36.0" "1.36" "1.37.0" "1.37" "1.38.0" "1.38" "1.39.0" "1.39"
    "1.40.0" "1.40" "1.41.0" "1.41" "1.42.0" "1.42" "1.43.0" "1.43" "1.44.0" "1.44"
    "1.45.0" "1.45" "1.46.0" "1.46" "1.47.0" "1.47" "1.48.0" "1.48" "1.49.0" "1.49"
    "1.50.0" "1.50" "1.51.0" "1.51" "1.52.0" "1.52" "1.53.0" "1.53" "1.54.0" "1.54"
    "1.55.0" "1.55" "1.56.0" "1.56" "1.57.0" "1.57" "1.58.0" "1.58" "1.59.0" "1.59"
    "1.60.0" "1.60" "1.61.0" "1.61" "1.62.0" "1.62" "1.63.0" "1.63" "1.64.0" "1.64"
    "1.65.0" "1.65" "1.66.0" "1.66" "1.67.0" "1.67" "1.68.0" "1.68" "1.69.0" "1.69"
)
# -- Make sure libboost_thread and its dependencies get linked in
find_package(Boost "1.35" COMPONENTS filesystem system thread)

if(NOT Boost_FOUND)
    message(FATAL_ERROR "Boost required to compile CyberRadio")
endif()

########################################################################
# Install directories
########################################################################
include(GrPlatform) #define LIB_SUFFIX
set(GR_RUNTIME_DIR      bin)
set(GR_LIBRARY_DIR      lib${LIB_SUFFIX})
set(GR_INCLUDE_DIR      include/${PROJECT_NAME})
set(GR_DATA_DIR         share)
set(GR_PKG_DATA_DIR     ${GR_DATA_DIR}/${PROJECT_NAME})
set(GR_DOC_DIR          ${GR_DATA_DIR}/doc)
set(GR_PKG_DOC_DIR      ${GR_DOC_DIR}/${PROJECT_NAME})
set(GR_CONF_DIR         etc)
set(GR_PKG_CONF_DIR     ${GR_CONF_DIR}/${PROJECT_NAME}/conf.d)
set(GR_LIBEXEC_DIR      libexec)
set(GR_PKG_LIBEXEC_DIR  ${GR_LIBEXEC_DIR}/${PROJECT_NAME})
set(GRC_BLOCKS_DIR      ${GR_PKG_DATA_DIR}/grc/blocks)

########################################################################
# Find gnuradio build dependencies
########################################################################
find_package(CppUnit)

# Search for GNU Radio and its components and versions. Add any
# components required to the list of GR_REQUIRED_COMPONENTS (in all
# caps such as FILTER or FFT) and change the version to the minimum
# API compatible version required.
# -- Some of these required components ensure that libvolk gets linked in
set(GR_REQUIRED_COMPONENTS RUNTIME ANALOG BLOCKS DIGITAL FFT PMT)
find_package(Gnuradio "3.7.2" REQUIRED)

if(NOT CPPUNIT_FOUND)
    message(FATAL_ERROR "CppUnit required to compile CyberRadio")
endif()

########################################################################
# Setup the include and linker paths
########################################################################
include_directories(
    ${CMAKE_SOURCE_DIR}/lib
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/lib
    ${CMAKE_BINARY_DIR}/include
    ${Boost_INCLUDE_DIRS}
    ${CPPUNIT_INCLUDE_DIRS}
    ${GNURADIO_ALL_INCLUDE_DIRS}
)

link_directories(
    ${Boost_LIBRARY_DIRS}
    ${CPPUNIT_LIBRARY_DIRS}
    ${GNURADIO_RUNTIME_LIBRARY_DIRS}
)

# Set component parameters
set(GR_CYBERRADIO_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/include CACHE INTERNAL "" FORCE)
set(GR_CYBERRADIO_SWIG_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/swig CACHE INTERNAL "" FORCE)

########################################################################
# Create uninstall target
########################################################################
configure_file(
    ${CMAKE_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
@ONLY)

add_custom_target(uninstall
    ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
)

########################################################################
# Determine which subgroup(s) to build
########################################################################
message("Checking for which subgroups to build")
message(STATUS "PACKAGE_SUBGROUP = " ${PACKAGE_SUBGROUP})
if("${PACKAGE_SUBGROUP}" STREQUAL "")
   set(PACKAGE_SUBGROUP "ALL")
endif("${PACKAGE_SUBGROUP}" STREQUAL "")
set(BUILD_SUBGROUP_ALL False)
set(BUILD_SUBGROUP_BASE False)
set(BUILD_SUBGROUP_NDR304 False)
set(BUILD_SUBGROUP_NDR308 False)
set(BUILD_SUBGROUP_NDR651 False)
set(BUILD_SUBGROUP_DOCS False)
if("${PACKAGE_SUBGROUP}" STREQUAL "ALL")
	set(BUILD_SUBGROUP_ALL True)
	set(BUILD_SUBGROUP_BASE True)
	set(BUILD_SUBGROUP_NDR304 True)
	set(BUILD_SUBGROUP_NDR308 True)
	set(BUILD_SUBGROUP_NDR651 True)
	set(BUILD_SUBGROUP_DOCS True)
elseif("${PACKAGE_SUBGROUP}" STREQUAL "BASE")
	set(BUILD_SUBGROUP_BASE True)
elseif("${PACKAGE_SUBGROUP}" STREQUAL "NDR304")
	set(BUILD_SUBGROUP_NDR304 True)
elseif("${PACKAGE_SUBGROUP}" STREQUAL "NDR308")
	set(BUILD_SUBGROUP_NDR308 True)
elseif("${PACKAGE_SUBGROUP}" STREQUAL "NDR651")
	set(BUILD_SUBGROUP_NDR651 True)
elseif("${PACKAGE_SUBGROUP}" STREQUAL "DOCS")
	set(BUILD_SUBGROUP_DOCS True)
endif("${PACKAGE_SUBGROUP}" STREQUAL "ALL")
message(STATUS "BASE = " ${BUILD_SUBGROUP_BASE})
message(STATUS "NDR304 = " ${BUILD_SUBGROUP_NDR304})
message(STATUS "NDR308 = " ${BUILD_SUBGROUP_NDR308})
message(STATUS "NDR651 = " ${BUILD_SUBGROUP_NDR651})
message(STATUS "DOCS = " ${BUILD_SUBGROUP_DOCS})

########################################################################
# Add subdirectories
########################################################################
add_subdirectory(include/CyberRadio)
add_subdirectory(lib)
add_subdirectory(swig)
add_subdirectory(python)
add_subdirectory(grc)
add_subdirectory(apps)
add_subdirectory(examples)
if(BUILD_SUBGROUP_DOCS)
	add_subdirectory(docs)
endif(BUILD_SUBGROUP_DOCS)

########################################################################
# Install cmake search helper for this library
########################################################################
if(BUILD_SUBGROUP_BASE)
	install(FILES cmake/Modules/CyberRadioConfig.cmake        
	    DESTINATION lib/cmake/CyberRadio
	)
endif(BUILD_SUBGROUP_BASE)
