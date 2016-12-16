########################################################################
# Project Setup
########################################################################
cmake_minimum_required(VERSION 2.6)

# Import package version if specified externally
# NOTE: Update this default package version string when there is a 
#    new library release!
if("${PACKAGE_VERSION}" STREQUAL "")
   set(PACKAGE_VERSION "16.06.20"
       CACHE STRING "Package version number" FORCE)
endif("${PACKAGE_VERSION}" STREQUAL "")

# Set the project name and version
project(libcyberradio CXX C)
set(PROJECT_NAME "libcyberradio"
    CACHE STRING "Project name" FORCE)
set(PROJECT_VERSION ${PACKAGE_VERSION}
    CACHE STRING "Project version number" FORCE)

# Select the release build type by default to get optimization flags
if(NOT CMAKE_BUILD_TYPE)
   set(CMAKE_BUILD_TYPE "Release")
   message(STATUS "Build type not specified: defaulting to release.")
endif(NOT CMAKE_BUILD_TYPE)
set(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "Build type")

########################################################################
# Find Required Packages
########################################################################
# -- Boost: This needs to be version 1.47 at minimum, since we rely on
#    Boost::Chrono.
if(UNIX AND EXISTS "/usr/lib64")
    list(APPEND BOOST_LIBRARYDIR "/usr/lib64") #fedora 64-bit fix
    set(Boost_USE_MULTITHREADED False) # CentOS 6 64-bit fix
endif(UNIX AND EXISTS "/usr/lib64")
set(Boost_ADDITIONAL_VERSIONS
    "1.47.0" "1.47" "1.48.0" "1.48" "1.49.0" "1.49" "1.50.0" "1.50" "1.51.0" "1.51" 
    "1.52.0" "1.52" "1.53.0" "1.53" "1.54.0" "1.54" "1.55.0" "1.55" "1.56.0" "1.56" 
    "1.57.0" "1.57" "1.58.0" "1.58" "1.59.0" "1.59" "1.60.0" "1.60" "1.61.0" "1.61" 
    "1.62.0" "1.62" "1.63.0" "1.63" "1.64.0" "1.64" "1.65.0" "1.65" "1.66.0" "1.66" 
    "1.67.0" "1.67" "1.68.0" "1.68" "1.69.0" "1.69"
)
find_package(Boost "1.47" COMPONENTS filesystem system thread chrono)
if(NOT Boost_FOUND)
    message(FATAL_ERROR "Boost 1.47 or newer required to build ${PROJECT_NAME}")
endif()
# -- Doxygen: This package is optional
find_package(Doxygen)

########################################################################
# Set Up Paths
########################################################################
set(LIBCYBERRADIO_INC_SUBDIR       LibCyberRadio)
set(LIBCYBERRADIO_INCLUDE_DIR      include/${LIBCYBERRADIO_INC_SUBDIR})
set(LIBCYBERRADIO_LIBRARY_DIR      lib)
set(LIBCYBERRADIO_BINARY_DIR       bin)
set(LIBCYBERRADIO_DATA_DIR         share)
set(LIBCYBERRADIO_PKG_DATA_DIR     ${LIBCYBERRADIO_DATA_DIR}/${PROJECT_NAME})
set(LIBCYBERRADIO_DOC_DIR          ${LIBCYBERRADIO_DATA_DIR}/doc)
set(LIBCYBERRADIO_PKG_DOC_DIR      ${LIBCYBERRADIO_DOC_DIR}/${PROJECT_NAME})
set(LIBCYBERRADIO_EXAMPLES_DIR     ${LIBCYBERRADIO_PKG_DATA_DIR}/examples)

########################################################################
# Set Up Include and Linker Paths
########################################################################
include_directories(
    ${CMAKE_SOURCE_DIR}/lib
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/lib
    ${CMAKE_BINARY_DIR}/include
    ${Boost_INCLUDE_DIRS}
)
link_directories(
    ${Boost_LIBRARY_DIRS}
)

########################################################################
# Create Uninstall Target
# NOTE: Depends on the file cmake/cmake_uninstall.cmake.in
########################################################################
configure_file(
    ${CMAKE_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
@ONLY)
add_custom_target(uninstall
    ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
)

########################################################################
# Add Subdirectories
########################################################################
add_subdirectory(include)
add_subdirectory(libcyberradio)
add_subdirectory(examples)

########################################################################
# Doxygen Support
########################################################################
# NOTE: The Doxygen configuration file is not formatted in the standard
# manner.  Instead, it uses ${VAR} placeholders for any CMake variables 
# we need to pass into it. 
if(DOXYGEN_FOUND)
    # -- Set documentation options
    set(HAVE_DOT ${DOXYGEN_DOT_FOUND})
    set(GENERATE_HTML YES)
    set(GENERATE_HTMLHELP NO)
    set(GENERATE_LATEX NO)
    set(GENERATE_PDF NO)
    set(GENERATE_RTF NO)
    set(GENERATE_MAN NO)
    set(GENERATE_XML NO)
    # -- Generate the "real" doxyfile
    configure_file(
        ${CMAKE_SOURCE_DIR}/${PROJECT_NAME}.doxyfile
        ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        )
    # -- Define where the docs are generated
    set(DOXYGEN_DIRS ${CMAKE_CURRENT_BINARY_DIR}/docs/html)
    # -- Add build target
    add_custom_command(
        OUTPUT ${DOXYGEN_DIRS}
        COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating documentation with Doxygen"
        )
    add_custom_target(doxygen_target ALL DEPENDS ${DOXYGEN_DIRS})
    # -- Add install target
    install(DIRECTORY ${DOXYGEN_DIRS} DESTINATION ${LIBCYBERRADIO_PKG_DOC_DIR})
endif(DOXYGEN_FOUND)
