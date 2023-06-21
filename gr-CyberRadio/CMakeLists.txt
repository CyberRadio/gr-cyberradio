# Copyright 2011,2012,2014,2016 Free Software Foundation, Inc.
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
project(gr-CyberRadio CXX C)
enable_testing()

#install to PyBOMBS target prefix if defined
if(DEFINED ENV{PYBOMBS_PREFIX})
    set(CMAKE_INSTALL_PREFIX $ENV{PYBOMBS_PREFIX})
    message(STATUS "PyBOMBS installed GNU Radio. Setting CMAKE_INSTALL_PREFIX to $ENV{PYBOMBS_PREFIX}")
endif()

#select the release build type by default to get optimization flags
if(NOT CMAKE_BUILD_TYPE)
   set(CMAKE_BUILD_TYPE "Release")
   message(STATUS "Build type not specified: defaulting to release.")
endif(NOT CMAKE_BUILD_TYPE)
set(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "")

#make sure our local CMake Modules path comes first
list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_SOURCE_DIR}/cmake/Modules)
list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_SOURCE_DIR}/gnuradio-volk-devel/usr/lib64/cmake/volk)

# Set the version information here
set(VERSION_INFO_MAJOR_VERSION 1)
set(VERSION_INFO_API_COMPAT    0)
set(VERSION_INFO_MINOR_VERSION 0)
set(VERSION_INFO_MAINT_VERSION git)
# -- If PACKAGE_VERSION is set from an external source, such as during Debian package
#    builds, use it to set the version information.
if(DEFINED PACKAGE_VERSION)
    include(UnpackVersionInfo)
    UNPACK_VERSION_INFO(PACKAGE_VERSION VERSION_INFO_MAJOR_VERSION VERSION_INFO_API_COMPAT
                        VERSION_INFO_MINOR_VERSION VERSION_INFO_MAINT_VERSION)
    #message(STATUS "UNPACK_VERSION_INFO ${PACKAGE_VERSION} ->")
    #message(STATUS "* VERSION_INFO_MAJOR_VERSION=${VERSION_INFO_MAJOR_VERSION}")
    #message(STATUS "* VERSION_INFO_API_COMPAT=${VERSION_INFO_API_COMPAT}")
    #message(STATUS "* VERSION_INFO_MINOR_VERSION=${VERSION_INFO_MINOR_VERSION}")
    #message(STATUS "* VERSION_INFO_MAINT_VERSION=${VERSION_INFO_MAINT_VERSION}")
endif(DEFINED PACKAGE_VERSION)

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
find_package(Boost "1.53" COMPONENTS filesystem system thread)
#find_package(Boost "1.55" COMPONENTS filesystem system thread)
#find_package(Boost "1.60" COMPONENTS filesystem system thread)

if(NOT Boost_FOUND)
    message(FATAL_ERROR "Boost required to compile CyberRadio")
endif()

########################################################################
# Install directories
########################################################################
include(GrPlatform) #define LIB_SUFFIX
include(IsPackageBuild) #define IS_PACKAGE_BUILD
set(GR_RUNTIME_DIR      bin)
set(GR_LIBRARY_DIR      lib${LIB_SUFFIX})
set(GR_INCLUDE_DIR      include/CyberRadio)
set(GR_DATA_DIR         share)
set(GR_PKG_DATA_DIR     ${GR_DATA_DIR}/${CMAKE_PROJECT_NAME})
set(GR_DOC_DIR          ${GR_DATA_DIR}/doc)
set(GR_PKG_DOC_DIR      ${GR_DOC_DIR}/${CMAKE_PROJECT_NAME})
# FORCE configuration files into /etc if this is a package build
if(IS_PACKAGE_BUILD)
    set(GR_CONF_DIR         /etc)
else()
    set(GR_CONF_DIR         etc)
endif(IS_PACKAGE_BUILD)
set(GR_PKG_CONF_DIR     ${GR_CONF_DIR}/${CMAKE_PROJECT_NAME}/conf.d)
set(GR_LIBEXEC_DIR      libexec)
set(GR_PKG_LIBEXEC_DIR  ${GR_LIBEXEC_DIR}/${CMAKE_PROJECT_NAME})
set(GRC_BLOCKS_DIR      ${GR_PKG_DATA_DIR}/grc/blocks)

########################################################################
# On Apple only, set install name and use rpath correctly, if not already set
########################################################################
if(APPLE)
    if(NOT CMAKE_INSTALL_NAME_DIR)
        set(CMAKE_INSTALL_NAME_DIR
            ${CMAKE_INSTALL_PREFIX}/${GR_LIBRARY_DIR} CACHE
            PATH "Library Install Name Destination Directory" FORCE)
    endif(NOT CMAKE_INSTALL_NAME_DIR)
    if(NOT CMAKE_INSTALL_RPATH)
        set(CMAKE_INSTALL_RPATH
            ${CMAKE_INSTALL_PREFIX}/${GR_LIBRARY_DIR} CACHE
            PATH "Library Install RPath" FORCE)
    endif(NOT CMAKE_INSTALL_RPATH)
    if(NOT CMAKE_BUILD_WITH_INSTALL_RPATH)
        set(CMAKE_BUILD_WITH_INSTALL_RPATH ON CACHE
            BOOL "Do Build Using Library Install RPath" FORCE)
    endif(NOT CMAKE_BUILD_WITH_INSTALL_RPATH)
endif(APPLE)

########################################################################
# Find gnuradio build dependencies
########################################################################
find_package(CppUnit)
find_package(Doxygen)
# LibCyberRadio supports automatic package detection as of version 
# 17.11.13.
find_package(LibCyberRadio)
#message(STATUS "LIBCYBERRADIO_FOUND=${LIBCYBERRADIO_FOUND}")
#message(STATUS "LIBCYBERRADIO_INCLUDE_DIR=${LIBCYBERRADIO_INCLUDE_DIR}")
#message(STATUS "LIBCYBERRADIO_LIB_DIR=${LIBCYBERRADIO_LIB_DIR}")

# Search for GNU Radio and its components and versions. Add any
# components required to the list of GR_REQUIRED_COMPONENTS (in all
# caps such as FILTER or FFT) and change the version to the minimum
# API compatible version required.
# -- Some of these required components ensure that libvolk gets linked in
set(GR_REQUIRED_COMPONENTS RUNTIME ANALOG BLOCKS DIGITAL FFT PMT)
find_package(Gnuradio "3.7.2" REQUIRED)
list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_SOURCE_DIR}/cmake/Modules)
include(GrVersion)

if(NOT CPPUNIT_FOUND)
    message(FATAL_ERROR "CppUnit required to compile CyberRadio")
endif()

########################################################################
# Setup doxygen option
########################################################################
if(DOXYGEN_FOUND)
	option(ENABLE_DOXYGEN "Build docs using Doxygen" ON)
else(DOXYGEN_FOUND)
	option(ENABLE_DOXYGEN "Build docs using Doxygen" OFF)
endif(DOXYGEN_FOUND)

########################################################################
# Setup the include and linker paths
#
# Include and linker paths have been expanded to include the following:
# (1) The libcyberradio library tree extracted from the Debian installer 
#     (this is intended to support automated builds through Jenkins)
# (2) The libcyberradio library build tree (if the libcyberradio package
#     was built from source)
########################################################################
if(LIBCYBERRADIO_FOUND)
    include_directories(
        ${LIBCYBERRADIO_INCLUDE_DIR}
        ${CMAKE_SOURCE_DIR}/gnuradio-volk-devel/usr/include
        ${CMAKE_SOURCE_DIR}/lib
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_BINARY_DIR}/lib
        ${CMAKE_BINARY_DIR}/include
        ${Boost_INCLUDE_DIRS}
        ${CPPUNIT_INCLUDE_DIRS}
        ${GNURADIO_ALL_INCLUDE_DIRS}
    )
    link_directories(
        ${LIBCYBERRADIO_LIB_DIR}
        ${CMAKE_SOURCE_DIR}/gnuradio-volk-devel/usr/lib64
        ${Boost_LIBRARY_DIRS}
        ${CPPUNIT_LIBRARY_DIRS}
        ${GNURADIO_RUNTIME_LIBRARY_DIRS}
    )
else(LIBCYBERRADIO_FOUND)
    include_directories(
        ${CMAKE_SOURCE_DIR}/../tmp-libcyberradio/usr/include
        ${CMAKE_SOURCE_DIR}/../tmp/usr/include
        ${CMAKE_SOURCE_DIR}/../libcyberradio/include
        ${CMAKE_SOURCE_DIR}/gnuradio-volk-devel/usr/include
        ${CMAKE_SOURCE_DIR}/lib
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_BINARY_DIR}/lib
        ${CMAKE_BINARY_DIR}/include
        ${Boost_INCLUDE_DIRS}
        ${CPPUNIT_INCLUDE_DIRS}
        ${GNURADIO_ALL_INCLUDE_DIRS}
    )
    link_directories(
        ${CMAKE_SOURCE_DIR}/../tmp-libcyberradio/usr/lib
        ${CMAKE_SOURCE_DIR}/../tmp/usr/lib
        ${CMAKE_SOURCE_DIR}/../libcyberradio/.libs
        ${CMAKE_SOURCE_DIR}/gnuradio-volk-devel/usr/lib64
        ${Boost_LIBRARY_DIRS}
        ${CPPUNIT_LIBRARY_DIRS}
        ${GNURADIO_RUNTIME_LIBRARY_DIRS}
    )
endif(LIBCYBERRADIO_FOUND)

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
# Add subdirectories
########################################################################
add_subdirectory(include/CyberRadio)
add_subdirectory(lib)
add_subdirectory(swig)
add_subdirectory(python)
add_subdirectory(grc)
add_subdirectory(apps)
add_subdirectory(examples)
add_subdirectory(docs)
add_subdirectory(etc)

########################################################################
# Install cmake search helper for this library
########################################################################
if(NOT CMAKE_MODULES_DIR)
  set(CMAKE_MODULES_DIR lib${LIB_SUFFIX}/cmake)
endif(NOT CMAKE_MODULES_DIR)

install(FILES cmake/Modules/CyberRadioConfig.cmake
    DESTINATION ${CMAKE_MODULES_DIR}/CyberRadio
)
