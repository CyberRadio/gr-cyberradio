/* -*- c++ -*- */

#define CYBERRADIO_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
#%include "CyberRadio_swig_doc.i"

%{
#include "CyberRadio/NDR651_duc_sink.h"
#include "CyberRadio/NDR651_duc_sink_mk2.h"
%}

%include "CyberRadio/NDR651_duc_sink.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, NDR651_duc_sink);
%include "CyberRadio/NDR651_duc_sink_mk2.h"
GR_SWIG_BLOCK_MAGIC2(CyberRadio, NDR651_duc_sink_mk2);
