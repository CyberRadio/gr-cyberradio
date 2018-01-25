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
install(FILES
    CyberRadio_NDR651_duc_sink_mk2.xml
    CyberRadio_vita_iq_source.xml
    CyberRadio_vita_iq_source_2.xml
    CyberRadio_vita_iq_source_mk3.xml
    CyberRadio_vita_multifile_iq_source.xml
    CyberRadio_NDR304_source.xml
    CyberRadio_NDR304_coherent_control.xml
    CyberRadio_NDR308_source.xml
    CyberRadio_NDR470_source.xml
    CyberRadio_NDR472_source.xml
    CyberRadio_NDR551_source.xml
    CyberRadio_NDR651_source.xml
    CyberRadio_ndr_control.xml
    CyberRadio_NDR_demo_control.xml
    CyberRadio_snapshot_source_c.xml
    CyberRadio_vector_keep_m_in_n.xml
    CyberRadio_vector_nlog10_ff.xml
    CyberRadio_generic_tuner_control_block.xml
    CyberRadio_generic_ddc_control_block.xml
    CyberRadio_generic_group_control_block.xml
#   CyberRadio_generic_radio_interface_block.xml
    CyberRadio_ndr804ptt_wideband_spectral_source.xml
    CyberRadio_ndr804ptt_snapshot_fft_source.xml
    CyberRadio_ndr804ptt_narrowband_source.xml
#   CyberRadio_file_like_object_source.xml
    CyberRadio_py_msg_strobe.xml
    CyberRadio_qt_freq_time_sink_iq.xml
    CyberRadio_qt_freq_time_sink_real.xml
    CyberRadio_safe_audio_sink.xml
    CyberRadio_sinad_calc_block.xml
    CyberRadio_vita_udp_rx.xml
    CyberRadio_generic_ndr_command_block.xml
#    CyberRadio_generic_radio_control_block.xml
    CyberRadio_ndr651_sink.xml
    CyberRadio_snapshot_vector_source.xml
    CyberRadio_NDR651_sync_sink.xml
    CyberRadio_freq_msg_converter.xml 
    variable_radio_object.xml
    CyberRadio_freq_msg_strobe.xml
    CyberRadio_vector_mag_squared_log10_cf.xml
    CyberRadio_log_mag_fft.xml DESTINATION share/gnuradio/grc/blocks
)
