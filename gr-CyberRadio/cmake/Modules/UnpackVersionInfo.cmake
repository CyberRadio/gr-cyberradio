###############################################################
# UnpackVersionInfo.cmake
#
# CMake module that provides methods for getting version 
# information from a package version string
#
# Author: DA
# 
############################################################### 

##
# \brief Function that unpacks a package version info string
#    into major number, minor number, patch number, and 
#    maintenance info string.
# 
# For example, unpacking the version info string "17.08.11-foo"
# results in:
# * Major number = 17
# * Minor number = 8
# * Patch number = 11
# * Maintenance info = foo
#
# \param VERSION_INFO_STR [input] Version info string
# \param MAJOR_NUM [output] Major version number
# \param MINOR_NUM [output] Minor version number
# \param PATCH_NUM [output] Patch version number
# \param MAINT_INFO [output] Maintenance info string
#
FUNCTION(UNPACK_VERSION_INFO VERSION_INFO_STR MAJOR_NUM MINOR_NUM PATCH_NUM MAINT_INFO)
    # NOTE: "Maintenance info" starts with the first character that isn't either
    # numeric or a dot. 
    STRING(REGEX MATCH "[-a-z][-.0-9a-zA-Z]*" MAINT_INFO_LOCAL ${${VERSION_INFO_STR}})
    #MESSAGE(STATUS "[UnpackVersionInfo] MAINT_INFO = ${MAINT_INFO_LOCAL}")
    # Remove the maintenance info from the version string (if it exists)
    IF(MAINT_INFO_LOCAL STREQUAL "")
        SET(VERSION_INFO_STR_LOCAL ${${VERSION_INFO_STR}})
    ELSE()
        STRING(REPLACE "${MAINT_INFO_LOCAL}" "" VERSION_INFO_STR_LOCAL ${${VERSION_INFO_STR}})
        STRING(REPLACE "-" "" MAINT_INFO_LOCAL ${MAINT_INFO_LOCAL})
    ENDIF()
    #MESSAGE(STATUS "[UnpackVersionInfo] VERSION_INFO_STR_LOCAL = ${VERSION_INFO_STR_LOCAL}")
    # Break the rest of the version info into major, minor, and patch components
    # NOTE: The MATH() commands below strip leading zeros from version
    # components. 
    STRING(REPLACE "." ";" VERSION_INFO_LIST ${VERSION_INFO_STR_LOCAL})
    LIST(GET VERSION_INFO_LIST 0 VERSION_INFO_MAJOR)
    LIST(GET VERSION_INFO_LIST 1 VERSION_INFO_MINOR)
    LIST(GET VERSION_INFO_LIST 2 VERSION_INFO_PATCH)
    MATH(EXPR MAJOR_NUM_LOCAL ${VERSION_INFO_MAJOR}+0)
    SET(${MAJOR_NUM} ${MAJOR_NUM_LOCAL} PARENT_SCOPE)
    MATH(EXPR MINOR_NUM_LOCAL ${VERSION_INFO_MINOR}+0)
    SET(${MINOR_NUM} ${MINOR_NUM_LOCAL} PARENT_SCOPE)
    # NOTE: The "patch" version needs to strip anything non-numeric prior to
    # evaluation.
    STRING(REGEX MATCH "[0-9]+" PATCH_STRIPPED ${VERSION_INFO_PATCH})
    MATH(EXPR PATCH_NUM_LOCAL ${PATCH_STRIPPED}+0)
    SET(${PATCH_NUM} ${PATCH_NUM_LOCAL} PARENT_SCOPE)
    # NOTE: If "maintenance info" is an empty string, then set it to "0" so
    # that GNU Radio versioning sets the library name appropriately.
    IF(MAINT_INFO_LOCAL STREQUAL "")
        SET(${MAINT_INFO} "0" PARENT_SCOPE)
    ELSE()
        SET(${MAINT_INFO} ${MAINT_INFO_LOCAL} PARENT_SCOPE)
    ENDIF()
ENDFUNCTION(UNPACK_VERSION_INFO)

