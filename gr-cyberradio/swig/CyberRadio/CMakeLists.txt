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
# Check if there is C++ code at all
########################################################################
if(NOT CyberRadio_sources)
	MESSAGE(STATUS "No C++ sources... skipping swig/")
	return()
endif(NOT CyberRadio_sources)

########################################################################
# Include swig generation macros
########################################################################
find_package(SWIG)
find_package(PythonLibs 2)
if(NOT SWIG_FOUND OR NOT PYTHONLIBS_FOUND)
    return()
endif()
include(GrSwig)
include(GrPython)

########################################################################
# Setup swig generation
########################################################################
foreach(incdir ${GNURADIO_RUNTIME_INCLUDE_DIRS})
    list(APPEND GR_SWIG_INCLUDE_DIRS ${incdir}/gnuradio/swig)
endforeach(incdir)

if(BUILD_SUBGROUP_BASE)
	set(CyberRadio_lib_name gnuradio-CyberRadio-base)
endif(BUILD_SUBGROUP_BASE)
if(BUILD_SUBGROUP_NDR651)
	set(CyberRadio_lib_name gnuradio-CyberRadio-ndr651)
endif(BUILD_SUBGROUP_NDR651)
if(BUILD_SUBGROUP_ALL)
	set(CyberRadio_lib_name gnuradio-CyberRadio)
endif(BUILD_SUBGROUP_ALL)

set(GR_SWIG_LIBRARIES ${CyberRadio_lib_name})
set(GR_SWIG_DOC_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/../include)

########################################################################
# Build and install by active subgroup
########################################################################
if(BUILD_SUBGROUP_BASE)
	#set(GR_SWIG_DOC_FILE ${CMAKE_CURRENT_BINARY_DIR}/CyberRadio_base_swig_doc.i)
	GR_SWIG_MAKE(CyberRadio_base_swig CyberRadio_base_swig.i)
	GR_SWIG_INSTALL(TARGETS CyberRadio_base_swig 
	                DESTINATION ${GR_PYTHON_DIR}/CyberRadio)
	install(
	    FILES
	    CyberRadio_base_swig.i
	    DESTINATION ${GR_INCLUDE_DIR}/CyberRadio/swig
	)
endif(BUILD_SUBGROUP_BASE)
if(BUILD_SUBGROUP_NDR651)
	#set(GR_SWIG_DOC_FILE ${CMAKE_CURRENT_BINARY_DIR}/CyberRadio_NDR651_swig_doc.i)
	GR_SWIG_MAKE(CyberRadio_NDR651_swig CyberRadio_NDR651_swig.i)
	GR_SWIG_INSTALL(TARGETS CyberRadio_NDR651_swig 
	                DESTINATION ${GR_PYTHON_DIR}/CyberRadio)
	install(
	    FILES
	    CyberRadio_NDR651_swig.i
	    DESTINATION ${GR_INCLUDE_DIR}/CyberRadio/swig
	)
endif(BUILD_SUBGROUP_NDR651)

########################################################################
# Install swig .i files for development
########################################################################
#install(
#    FILES
#    ${CMAKE_CURRENT_BINARY_DIR}/CyberRadio_swig_doc.i
#    DESTINATION ${GR_INCLUDE_DIR}/CyberRadio/swig
#)
