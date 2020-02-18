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
# Install example programs
########################################################################
set(EXAMPLE_DESTINATION ${GR_DATA_DIR}/CyberRadio/examples)

#GR_PYTHON_INSTALL(
#    FILES
#    ndr_qt_demo_gui.py
#    ndrGuiLauncher
#    testRadioConnection
#    ndr804_display.py
#    DESTINATION ${EXAMPLE_DESTINATION}
#)
install(
	FILES
	ndr_qt_demo_gui.grc
	ndr651_txrx_gui.grc
	ndr804_display.grc
	continuous_fft_demo.grc
	ndr_click2tune_test.grc
	DESTINATION ${EXAMPLE_DESTINATION}
)

set(EXAMPLE_DESTINATION ${GR_DATA_DIR}/CyberRadio/)

install(
	FILES
	cyberradio.qss
	DESTINATION ${EXAMPLE_DESTINATION}
)
