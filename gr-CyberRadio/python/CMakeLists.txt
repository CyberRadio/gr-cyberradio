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
GR_PYTHON_INSTALL(
    FILES
    __init__.py
    NDR304_source.py
    NDR304_coherent_control.py
    NDR308_source.py
    NDR470_source.py
    NDR472_source.py
    NDR551_source.py
    NDR651_source.py
    ndr_control.py
    NDR_demo_control.py
    generic_tuner_control_block.py
    generic_ddc_control_block.py
    generic_group_control_block.py
    generic_radio_interface_block.py
    ndr804ptt_wideband_spectral_source.py
    ndr804ptt_snapshot_fft_source.py
    ndr804ptt_narrowband_source.py
    file_like_object_source.py
    py_msg_strobe.py
    qt_freq_time_sink_iq.py
    qt_freq_time_sink_real.py
    safe_audio_sink.py
    sinad_calc_block.py
    generic_ndr_command_block.py
    generic_radio_control_block.py
    freq_msg_converter.py
    freq_msg_strobe.py
    log_mag_fft.py DESTINATION ${GR_PYTHON_DIR}/CyberRadio
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-CyberRadio)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
GR_ADD_TEST(qa_generic_radio_control_block ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_generic_radio_control_block.py)
GR_ADD_TEST(qa_ndr651_sink ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ndr651_sink.py)
GR_ADD_TEST(qa_freq_msg_converter ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_freq_msg_converter.py)
GR_ADD_TEST(qa_freq_msg_strobe ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_freq_msg_strobe.py)
GR_ADD_TEST(qa_vector_mag_squared_log10_cf ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_vector_mag_squared_log10_cf.py)
GR_ADD_TEST(qa_log_mag_fft ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_log_mag_fft.py)
