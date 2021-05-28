########################################################################
# Project Setup
########################################################################
CMAKE_MINIMUM_REQUIRED(VERSION 3.8)

# Import package version if specified externally
# NOTE: Update this default package version string when there is a 
#    new library release!
IF("${PACKAGE_VERSION}" STREQUAL "")
   SET(PACKAGE_VERSION "18.06.29"
       CACHE STRING "Package version number" FORCE)
ENDIF("${PACKAGE_VERSION}" STREQUAL "")

# Set the project name and version
PROJECT(libcyberradio CXX C)
SET(PROJECT_NAME "libcyberradio"
    CACHE STRING "Project name" FORCE)
SET(PROJECT_VERSION ${PACKAGE_VERSION}
    CACHE STRING "Project version number" FORCE)

# Select the release build type by default to get optimization flags
IF(NOT CMAKE_BUILD_TYPE)
   SET(CMAKE_BUILD_TYPE "Release")
   MESSAGE(STATUS "Build type not specified: defaulting to release.")
ENDIF(NOT CMAKE_BUILD_TYPE)
SET(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "Build type")

#make sure our local CMake Modules path comes first
LIST(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_SOURCE_DIR}/cmake/Modules)

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
# Find Required Packages
########################################################################
# -- The kernel needs to be able to support TPACKET_V3 capture 
#    semantics.
INCLUDE(CheckStructHasMember)
CHECK_STRUCT_HAS_MEMBER("struct tpacket_req3" tp_retire_blk_tov "linux/if_packet.h" HAVE_TPACKET_V3)
#CHECK_CXX_SYMBOL_EXISTS("struct tpacket_req3" "linux/if_packet.h" HAVE_TPACKET_V3)
IF(NOT HAVE_TPACKET_V3)
    MESSAGE(FATAL_ERROR "Kernel must support TPACKET_V3 capture semantics to build ${PROJECT_NAME}")
ENDIF()
# -- Boost: This needs to be version 1.47 at minimum, since we rely on
#    Boost::Chrono.
IF(UNIX AND EXISTS "/usr/lib64")
    LIST(APPEND BOOST_LIBRARYDIR "/usr/lib64") #fedora 64-bit fix
    SET(Boost_USE_MULTITHREADED False) # CentOS 6 64-bit fix
ENDIF(UNIX AND EXISTS "/usr/lib64")
SET(Boost_ADDITIONAL_VERSIONS
    "1.47.0" "1.47" "1.48.0" "1.48" "1.49.0" "1.49" "1.50.0" "1.50" "1.51.0" "1.51" 
    "1.52.0" "1.52" "1.53.0" "1.53" "1.54.0" "1.54" "1.55.0" "1.55" "1.56.0" "1.56" 
    "1.57.0" "1.57" "1.58.0" "1.58" "1.59.0" "1.59" "1.60.0" "1.60" "1.61.0" "1.61" 
    "1.62.0" "1.62" "1.63.0" "1.63" "1.64.0" "1.64" "1.65.0" "1.65" "1.66.0" "1.66" 
    "1.67.0" "1.67" "1.68.0" "1.68" "1.69.0" "1.69"
)
FIND_PACKAGE(Boost "1.47" COMPONENTS filesystem system thread chrono)
IF(NOT Boost_FOUND)
    MESSAGE(FATAL_ERROR "Boost required to build ${PROJECT_NAME}")
ENDIF()
# -- libpcap: This package is required
FIND_PACKAGE(PCAP)
IF(PCAP_FOUND)
    GET_FILENAME_COMPONENT(PCAP_LIBRARY_DIR ${PCAP_LIBRARIES} PATH)
    MESSAGE(STATUS "Found libpcap")
    MESSAGE(STATUS "-- Includes: ${PCAP_INCLUDE_DIRS}")
    MESSAGE(STATUS "-- Libraries: ${PCAP_LIBRARY_DIR}")
ELSE()
    MESSAGE(FATAL_ERROR "libpcap required to build ${PROJECT_NAME}")
ENDIF()
INCLUDE(FindPCAP.cmake)
# -- CURL: This package is required
FIND_PACKAGE(CURL)
IF(NOT CURL_FOUND)
    MESSAGE(FATAL_ERROR "CURL required to build ${PROJECT_NAME}")
ENDIF()
# -- JsonCpp: This package is required
FIND_PACKAGE(JsonCpp)
IF(NOT JSONCPP_FOUND)
    MESSAGE(FATAL_ERROR "JsonCpp required to build ${PROJECT_NAME}")
ENDIF()
# -- Doxygen: This package is optional
FIND_PACKAGE(Doxygen)

########################################################################
# Set Up Paths
########################################################################
SET(LIBCYBERRADIO_INC_SUBDIR       LibCyberRadio)
SET(LIBCYBERRADIO_INCLUDE_DIR      include/${LIBCYBERRADIO_INC_SUBDIR})

IF(UNIX AND EXISTS "/usr/lib/x86_64-linux-gnu")
    SET(LIBCYBERRADIO_LIBRARY_DIR      lib/x86_64-linux-gnu) # new for linux with multiarch support
ELSEIF(UNIX AND EXISTS "/usr/lib64")
    SET(LIBCYBERRADIO_LIBRARY_DIR      lib64) # CentOS 64-bit fix
ELSE()
    SET(LIBCYBERRADIO_LIBRARY_DIR      lib)
ENDIF()

SET(LIBCYBERRADIO_BINARY_DIR       bin)
SET(LIBCYBERRADIO_DATA_DIR         share)
SET(LIBCYBERRADIO_PKG_DATA_DIR     ${LIBCYBERRADIO_DATA_DIR}/${PROJECT_NAME})
SET(LIBCYBERRADIO_DOC_DIR          ${LIBCYBERRADIO_DATA_DIR}/doc)
SET(LIBCYBERRADIO_PKG_DOC_DIR      ${LIBCYBERRADIO_DOC_DIR}/${PROJECT_NAME})
SET(LIBCYBERRADIO_EXAMPLES_DIR     ${LIBCYBERRADIO_PKG_DATA_DIR}/examples)
SET(LIBCYBERRADIO_CMAKE_MODS_DIR   ${LIBCYBERRADIO_LIBRARY_DIR}/cmake/${PROJECT_NAME})

########################################################################
# Set Up Include and Linker Paths
########################################################################
INCLUDE_DIRECTORIES(
    ${CMAKE_SOURCE_DIR}/lib
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/lib
    ${CMAKE_BINARY_DIR}/include
    ${Boost_INCLUDE_DIRS}
    ${PCAP_INCLUDE_DIRS}
    ${CURL_INCLUDE_DIRS}
    ${JSONCPP_INCLUDE_DIR}
)
LINK_DIRECTORIES(
    ${Boost_LIBRARY_DIRS}
    ${PCAP_LIBRARY_DIR}
    ${JSONCPP_LIB_DIR}
)

########################################################################
# Create CMake "Config" files
# NOTE: These are used to tell CMake where to find this library 
#    using the find_package() directive.
# NOTE: Depends on the files LibCyberRadioConfig.cmake.in and 
#    LibCyberRadioConfigVersion.cmake.in.
########################################################################
# -- Generate config files
CONFIGURE_FILE(
    ${CMAKE_SOURCE_DIR}/LibCyberRadioConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/LibCyberRadioConfig.cmake
@ONLY)
CONFIGURE_FILE(
    ${CMAKE_SOURCE_DIR}/LibCyberRadioConfigVersion.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/LibCyberRadioConfigVersion.cmake
@ONLY)
# -- Add make target for config files
ADD_CUSTOM_TARGET(package_config_target ALL 
                  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/LibCyberRadioConfig.cmake
                          ${CMAKE_CURRENT_BINARY_DIR}/LibCyberRadioConfigVersion.cmake)
# -- Add config files to install
INSTALL(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/LibCyberRadioConfig.cmake 
        ${CMAKE_CURRENT_BINARY_DIR}/LibCyberRadioConfigVersion.cmake 
        DESTINATION ${LIBCYBERRADIO_CMAKE_MODS_DIR})

########################################################################
# Create Uninstall Target
# NOTE: Depends on the file cmake/cmake_uninstall.cmake.in
########################################################################
CONFIGURE_FILE(
    ${CMAKE_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
@ONLY)
ADD_CUSTOM_TARGET(uninstall
    ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
)

########################################################################
# Add Subdirectories
########################################################################
ADD_SUBDIRECTORY(include)
ADD_SUBDIRECTORY(libcyberradio)
ADD_SUBDIRECTORY(examples)

########################################################################
# Doxygen Support
########################################################################
# NOTE: The Doxygen configuration file is not formatted in the standard
# manner.  Instead, it uses ${VAR} placeholders for any CMake variables 
# we need to pass into it. 
IF(DOXYGEN_FOUND)
    # -- Set documentation options
    SET(HAVE_DOT ${DOXYGEN_DOT_FOUND})
    SET(GENERATE_HTML YES)
    SET(GENERATE_HTMLHELP NO)
    SET(GENERATE_LATEX NO)
    SET(GENERATE_PDF NO)
    SET(GENERATE_RTF NO)
    SET(GENERATE_MAN NO)
    SET(GENERATE_XML NO)
    # -- Generate the "real" doxyfile
    CONFIGURE_FILE(
        ${CMAKE_SOURCE_DIR}/${PROJECT_NAME}.doxyfile
        ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        )
    # -- Define where the docs are generated
    SET(DOXYGEN_DIRS ${CMAKE_CURRENT_BINARY_DIR}/docs/html)
    # -- Add build target
    ADD_CUSTOM_COMMAND(
        OUTPUT ${DOXYGEN_DIRS}
        COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating documentation with Doxygen"
        )
    ADD_CUSTOM_TARGET(doxygen_target ALL DEPENDS ${DOXYGEN_DIRS})
    # -- Add install target
    INSTALL(DIRECTORY ${DOXYGEN_DIRS} DESTINATION ${LIBCYBERRADIO_PKG_DOC_DIR})
ENDIF(DOXYGEN_FOUND)
