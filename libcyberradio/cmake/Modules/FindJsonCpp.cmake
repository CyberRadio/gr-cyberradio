######################################################################
# FindJsonCpp.cmake
#
# Finds the JsonCpp package for CMake.
#
# Sets the following CMake cache variables:
# * JSONCPP_FOUND (Boolean) -- Whether JsonCpp was found
#      using this module
# * JSONCPP_INCLUDE_DIR (String) -- JsonCpp include file 
#      directory
# * JSONCPP_LIB_DIR (String) -- Directory where JsonCpp 
#      library was found 
# * JSONCPP_LIB (String) -- JsonCpp shared library file
# 
######################################################################

FIND_PATH( JSONCPP_INCLUDE_DIR
           NAMES json/json.h json.h
           HINTS "${JSONCPP_HINTS}/include"
           PATHS /usr/include/jsoncpp
)

FIND_LIBRARY( JSONCPP_LIB
              NAMES jsoncpp
              HINTS "${JSONCPP_HINTS}/lib"
)
GET_FILENAME_COMPONENT(JSONCPP_LIB_DIR ${JSONCPP_LIB} PATH)

INCLUDE( FindPackageHandleStandardArgs )
FIND_PACKAGE_HANDLE_STANDARD_ARGS(JsonCpp
                                  REQUIRED_VARS JSONCPP_INCLUDE_DIR JSONCPP_LIB_DIR
                                                JSONCPP_LIB
                                  )

MARK_AS_ADVANCED(JSONCPP_INCLUDE_DIR JSONCPP_LIB_DIR JSONCPP_LIB
                 JSONCPP_FOUND)
