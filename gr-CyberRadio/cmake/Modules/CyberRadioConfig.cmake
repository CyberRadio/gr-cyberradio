INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_CYBERRADIO CyberRadio)

FIND_PATH(
    CYBERRADIO_INCLUDE_DIRS
    NAMES CyberRadio/api.h
    HINTS $ENV{CYBERRADIO_DIR}/include
        ${PC_CYBERRADIO_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    CYBERRADIO_LIBRARIES
    NAMES gnuradio-CyberRadio
    HINTS $ENV{CYBERRADIO_DIR}/lib
        ${PC_CYBERRADIO_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/CyberRadioTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CYBERRADIO DEFAULT_MSG CYBERRADIO_LIBRARIES CYBERRADIO_INCLUDE_DIRS)
MARK_AS_ADVANCED(CYBERRADIO_LIBRARIES CYBERRADIO_INCLUDE_DIRS)
