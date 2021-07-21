######################################################################
# LibCyberRadioConfig.cmake
#
# Configures the package location information for CMake.
#
# Based on the GnuradioConfig.cmake file distributed with
# GNU Radio 3.7.11.
#
# Sets the following CMake cache variables:
# * LIBCYBERRADIO_FOUND (Boolean) -- Whether LibCyberRadio was found
#      using this module
# * LIBCYBERRADIO_INCLUDE_DIR (String) -- LibCyberRadio include file 
#      directory
# * LIBCYBERRADIO_LIB_DIR (String) -- Directory where LibCyberRadio 
#      library was found 
# * LIBCYBERRADIO_LIB (String) -- LibCyberRadio shared library file
# 
######################################################################

INCLUDE(FindPkgConfig)
INCLUDE(FindPackageHandleStandardArgs)

# Allows us to use all .cmake files in this directory
LIST(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_CURRENT_LIST_DIR}")

# look for include files
# NOTE: This uses paths relative to the CMAKE_SOURCE_DIR in order
#    to support automated builds through Jenkins without needing
#    to install libcyberradio on the slave units.
FIND_PATH(
    LIBCYBERRADIO_INCLUDE_DIR
    NAMES LibCyberRadio/Common/BasicList.h
    PATHS ${CMAKE_SOURCE_DIR}/../tmp-libcyberradio/usr/include
          ${CMAKE_SOURCE_DIR}/../tmp/usr/include
          ${CMAKE_SOURCE_DIR}/../libcyberradio/include
          /usr/local/include
          /usr/include
          "/usr/include"
          "/usr/include"
)

# look for library
# NOTE: This uses paths relative to the CMAKE_SOURCE_DIR in order
#    to support automated builds through Jenkins without needing
#    to install libcyberradio on the slave units.
FIND_LIBRARY(
    LIBCYBERRADIO_LIB
    NAMES libcyberradio.so
    PATHS ${CMAKE_SOURCE_DIR}/../tmp-libcyberradio/usr/lib
          ${CMAKE_SOURCE_DIR}/../tmp-libcyberradio/usr/lib64
          ${CMAKE_SOURCE_DIR}/../tmp-libcyberradio/usr/lib/x86_64-linux-gnu # multiarch support
          ${CMAKE_SOURCE_DIR}/../tmp/usr/lib
          ${CMAKE_SOURCE_DIR}/../tmp/usr/lib64
          ${CMAKE_SOURCE_DIR}/../tmp/usr/lib/x86_64-linux-gnu # multiarch support
          ${CMAKE_SOURCE_DIR}/../libcyberradio/.libs
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          /usr/lib/x86_64-linux-gnu # multiarch support
          "/usr/lib"
          "/usr/lib64"
          "/usr/lib/x86_64-linux-gnu" # multiarch support
)
GET_FILENAME_COMPONENT(LIBCYBERRADIO_LIB_DIR ${LIBCYBERRADIO_LIB} PATH)

# For FIND_PACKAGE_HANDLE_STANDARD_ARGS, the FOUND_VAR argument was introduced
# in CMake 2.8.11.  We need to do version-checking to get the right syntax.
IF(${CMAKE_VERSION} VERSION_LESS "2.8.11")
    FIND_PACKAGE_HANDLE_STANDARD_ARGS(LibCyberRadio
                                      REQUIRED_VARS LIBCYBERRADIO_INCLUDE_DIR LIBCYBERRADIO_LIB_DIR
                                                    LIBCYBERRADIO_LIB
                                      )
ELSE()
    FIND_PACKAGE_HANDLE_STANDARD_ARGS(LibCyberRadio
                                      FOUND_VAR LIBCYBERRADIO_FOUND
                                      REQUIRED_VARS LIBCYBERRADIO_INCLUDE_DIR LIBCYBERRADIO_LIB_DIR
                                                    LIBCYBERRADIO_LIB
                                      )
ENDIF()

SET(LIBCYBERRADIO_FOUND ${LIBCYBERRADIO_FOUND} CACHE BOOL "LibCyberRadio found")
SET(LIBCYBERRADIO_INCLUDE_DIR ${LIBCYBERRADIO_INCLUDE_DIR} CACHE STRING "LibCyberRadio include directory")
SET(LIBCYBERRADIO_LIB_DIR ${LIBCYBERRADIO_LIB_DIR} CACHE STRING "LibCyberRadio library directory")
SET(LIBCYBERRADIO_LIB ${LIBCYBERRADIO_LIB} CACHE STRING "LibCyberRadio shared library")

# show results
MESSAGE("LibCyberRadio Config Results")
MESSAGE(" * FOUND=${LIBCYBERRADIO_FOUND}")
MESSAGE(" * INCLUDE_DIR=${LIBCYBERRADIO_INCLUDE_DIR}")
MESSAGE(" * LIB_DIR=${LIBCYBERRADIO_LIB_DIR}")
MESSAGE(" * LIB=${LIBCYBERRADIO_LIB}")

MARK_AS_ADVANCED(LIBCYBERRADIO_INCLUDE_DIR LIBCYBERRADIO_LIB_DIR LIBCYBERRADIO_LIB
                 LIBCYBERRADIO_FOUND)

