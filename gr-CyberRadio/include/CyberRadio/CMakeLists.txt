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
# Install public header files
########################################################################
install(FILES
    api.h
    NDR651_duc_sink_mk2.h
    vita_iq_source.h
    vita_iq_source_2.h
    vita_iq_source_mk3.h
    vita_multifile_iq_source.h
    snapshot_source_c.h
    vector_keep_m_in_n.h
    vector_nlog10_ff.h
    vita_udp_rx.h
    ndr651_sink.h
    snapshot_vector_source.h
    NDR651_sync_sink.h
    vector_mag_squared_log10_cf.h
    single_pole_iir_filter_ff.h
    snapshot_vector_source_mk2.h
    snapshot_fft_vector_source.h
    mux.h DESTINATION include/CyberRadio
)
