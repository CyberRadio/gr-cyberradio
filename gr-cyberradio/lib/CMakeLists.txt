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
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR} CyberRadio)
link_directories(${Boost_LIBRARY_DIRS})

if(BUILD_SUBGROUP_BASE)
	list(APPEND CyberRadio_sources
	    vita_iq_source_impl.cpp
	    CyberRadio/Vita49Packet.cpp
	)
	set(CyberRadio_lib_name gnuradio-CyberRadio-base)
endif(BUILD_SUBGROUP_BASE)
if(BUILD_SUBGROUP_NDR651)
	list(APPEND CyberRadio_sources
	    NDR651_duc_sink_impl.cpp
	    CyberRadio/Pythonesque.cpp
	    CyberRadio/Thread.cpp
	    CyberRadio/NDR651/ClientSocket.cpp
	    CyberRadio/NDR651/FlowControlClient.cpp
	    CyberRadio/NDR651/TransmitPacketizer.cpp
	    CyberRadio/NDR651/TransmitSocket.cpp
	    CyberRadio/NDR651/Transmitter.cpp
	)
	set(CyberRadio_lib_name gnuradio-CyberRadio-ndr651)
endif(BUILD_SUBGROUP_NDR651)
if(BUILD_SUBGROUP_ALL)
	set(CyberRadio_lib_name gnuradio-CyberRadio)
endif(BUILD_SUBGROUP_ALL)

set(CyberRadio_sources "${CyberRadio_sources}" PARENT_SCOPE)
if(NOT CyberRadio_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT CyberRadio_sources)

add_library(${CyberRadio_lib_name} SHARED ${CyberRadio_sources})
target_link_libraries(${CyberRadio_lib_name} ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(${CyberRadio_lib_name} PROPERTIES DEFINE_SYMBOL "gnuradio_CyberRadio_EXPORTS")

if(APPLE)
    set_target_properties(${CyberRadio_lib_name} PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS ${CyberRadio_lib_name}
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_CyberRadio_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_CyberRadio.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_CyberRadio.cc
)

add_executable(test-CyberRadio ${test_CyberRadio_sources})

target_link_libraries(
  test-CyberRadio
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  ${CyberRadio_lib_name}
)

GR_ADD_TEST(test_CyberRadio test-CyberRadio)
