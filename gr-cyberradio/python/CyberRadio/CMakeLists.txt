# Copyright 2011 Free Software Foundation, Inc.
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
# Include python install macros
########################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

########################################################################
# Install python sources
########################################################################
if(BUILD_SUBGROUP_BASE)
	GR_PYTHON_INSTALL(
	    FILES
	    __init__.py
	    file_like_object_source.py
	    NDR_driver_interface.py
	    DESTINATION ${GR_PYTHON_DIR}/CyberRadio
	)
endif(BUILD_SUBGROUP_BASE)
if(BUILD_SUBGROUP_NDR304)
	GR_PYTHON_INSTALL(
	    FILES
	    NDR304_source.py
	    DESTINATION ${GR_PYTHON_DIR}/CyberRadio
	)
endif(BUILD_SUBGROUP_NDR304)
if(BUILD_SUBGROUP_NDR308)
	GR_PYTHON_INSTALL(
	    FILES
	    NDR308_source.py
	    DESTINATION ${GR_PYTHON_DIR}/CyberRadio
	)
endif(BUILD_SUBGROUP_NDR308)
if(BUILD_SUBGROUP_NDR651)
	GR_PYTHON_INSTALL(
	    FILES
	    NDR651_source.py
	    NDR651_sink.py
	    DESTINATION ${GR_PYTHON_DIR}/CyberRadio
	)
endif(BUILD_SUBGROUP_NDR651)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-CyberRadio)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
