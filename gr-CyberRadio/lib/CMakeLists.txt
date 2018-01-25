# Copyright 2011,2012,2016 Free Software Foundation, Inc.
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

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND CyberRadio_sources
    NDR651_duc_sink_mk2_impl.cc
    vita_iq_source_impl.cc
    vita_iq_source_2_impl.cc
    vita_iq_source_mk3_impl.cc
    vita_multifile_iq_source_impl.cc
    snapshot_source_c_impl.cc
    vector_keep_m_in_n_impl.cc
    vector_nlog10_ff_impl.cc
    vita_udp_rx_impl.cc
    ndr651_sink_impl.cc
    snapshot_vector_source_impl.cc
    NDR651_sync_sink_impl.cc
    vector_mag_squared_log10_cf_impl.cc )

set(CyberRadio_sources "${CyberRadio_sources}" PARENT_SCOPE)
if(NOT CyberRadio_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT CyberRadio_sources)

add_library(gnuradio-CyberRadio SHARED ${CyberRadio_sources})
target_link_libraries(gnuradio-CyberRadio ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES} cyberradio)
set_target_properties(gnuradio-CyberRadio PROPERTIES DEFINE_SYMBOL "gnuradio_CyberRadio_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-CyberRadio PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-CyberRadio RUNTIME_COMPONENT "CyberRadio_runtime" DEVEL_COMPONENT "CyberRadio_devel")

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
  gnuradio-CyberRadio
)

GR_ADD_TEST(test_CyberRadio test-CyberRadio)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")
