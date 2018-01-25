/* -*- c++ -*- */

#define CYBERRADIO_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "CyberRadio_swig_doc.i"

%{
#include "CyberRadio/NDR651_duc_sink_mk2.h"
#include "CyberRadio/vita_iq_source.h"
#include "CyberRadio/vita_iq_source_2.h"
#include "CyberRadio/vita_iq_source_mk3.h"
#include "CyberRadio/vita_multifile_iq_source.h"
#include "CyberRadio/snapshot_source_c.h"
#include "CyberRadio/vector_keep_m_in_n.h"
#include "CyberRadio/vector_nlog10_ff.h"
#include "CyberRadio/vita_udp_rx.h"
#include "CyberRadio/ndr651_sink.h"
#include "CyberRadio/snapshot_vector_source.h"
#include "CyberRadio/NDR651_sync_sink.h"
#include "CyberRadio/vector_mag_squared_log10_cf.h"
%}

%include "CyberRadio/NDR651_duc_sink_mk2.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, NDR651_duc_sink_mk2);
%include "CyberRadio/vita_iq_source.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vita_iq_source);
%include "CyberRadio/vita_iq_source_2.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vita_iq_source_2);
%include "CyberRadio/vita_iq_source_mk3.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vita_iq_source_mk3);
%include "CyberRadio/vita_multifile_iq_source.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vita_multifile_iq_source);
%include "CyberRadio/snapshot_source_c.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, snapshot_source_c);
%include "CyberRadio/vector_keep_m_in_n.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vector_keep_m_in_n);
%include "CyberRadio/vector_nlog10_ff.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vector_nlog10_ff);

%include "CyberRadio/vita_udp_rx.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vita_udp_rx);


%include "CyberRadio/ndr651_sink.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, ndr651_sink);
%include "CyberRadio/snapshot_vector_source.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, snapshot_vector_source);
%include "CyberRadio/NDR651_sync_sink.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, NDR651_sync_sink);
%include "CyberRadio/vector_mag_squared_log10_cf.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, vector_mag_squared_log10_cf);
