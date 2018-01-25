###############################################################
# IsPackageBuild.cmake
#
# CMake module for determining if the user is executing CMake
# as part of a package building process (either Debian or RPM)
#
# Author: DA
# 
############################################################### 

STRING(COMPARE EQUAL "${CMAKE_INSTALL_PREFIX}" "/usr" IS_PACKAGE_BUILD)
MESSAGE(STATUS "Determining if this is a package build")
MESSAGE(STATUS "* CMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}")
MESSAGE(STATUS "* IS_PACKAGE_BUILD=${IS_PACKAGE_BUILD}")
MARK_AS_ADVANCED(FORCE IS_PACKAGE_BUILD)
