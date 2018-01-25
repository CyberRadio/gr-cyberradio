#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes

from generic_ddc_control_block import generic_ddc_control_block
from generic_tuner_control_block import generic_tuner_control_block


class ndr804ptt_wideband_spectral_source(gr.hier_block2):
    """
    docstring for block ndr804ptt_wideband_spectral_source
    """
    def __init__(self, 
                    radioParam={"type":"ndr804-ptt", "host":"ndr308", "port":8617, "obj":None}, 
                    index=1, 
                    enable=True, 
                    rate=2, 
                    rfFreq=1000, 
                    rfAtten=0, 
                    rfFilter=1, 
                    radioInterface=1, 
                    dipIndex=-1, 
                    localInterface="eth6", 
                    udpPort=11000, 
                    iirAvgGain=5, 
                    otherDdcArgs={}, 
                    otherTunerArgs={}, 
                     ):
        gr.hier_block2.__init__(
            self, "NDR804-PTT Wideband Spectral Source",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev(2, 2, [gr.sizeof_float*3200, gr.sizeof_float*3200]),
        )
        self.message_port_register_hier_out("rfFreq")
        self.message_port_register_hier_in("rfFreq")

        ##################################################
        # Parameters
        ##################################################
        self.enable = enable
        self.dipIndex = dipIndex
        self.iirAvgGain = iirAvgGain
        self.index = index
        self.localInterface = localInterface
        self.otherDdcArgs = otherDdcArgs
        self.otherTunerArgs = otherTunerArgs
        self.radioInterface = radioInterface
        self.radioParam = radioParam
        self.rate = rate
        self.rfAtten = rfAtten
        self.rfFilter = rfFilter
        self.rfFreq = rfFreq
        self.udpPort = udpPort

        ##################################################
        # Blocks
        ##################################################
        self.tunerControl = generic_tuner_control_block(
                    radioParam, 
                    index, 
                    True, 
                    rfFreq, 
                    rfAtten, 
                    rfFilter, 
                    otherTunerArgs, 
                    False
                     )
        self.streamToVec = blocks.stream_to_vector(gr.sizeof_char*1, 3200)
        self.spectralUdpSource = blocks.udp_source(gr.sizeof_char*1, "0.0.0.0", udpPort, 4136, True)
        self.iirFilter = filter.single_pole_iir_filter_ff(2.0**-iirAvgGain, 3200)
        self.extractPacketPayload = blocks.keep_m_in_n(gr.sizeof_char, 3200, 4096+40, 36 + (4096-3200)/2)
        self.ddcControl = generic_ddc_control_block( 
                    radioParam, 
                    index, 
                    "", #idString
                    enable, 
                    True, 
                    rate, 
                    0, 
                    0, 
                    index, 
                    0, 
                    radioInterface, 
                    dipIndex, 
                    localInterface, 
                    udpPort, 
                    otherDdcArgs, 
                    False
                     )
        self.charToFloat = blocks.char_to_float(3200, 1.0)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*3200)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self, 'rfFreq'), (self.tunerControl, 'rfFreq'))   
        self.msg_connect((self.tunerControl, 'rfFreq'), (self, 'rfFreq'))   
        self.connect((self.charToFloat, 0), (self.iirFilter, 0))    
        self.connect((self.charToFloat, 0), (self, 0))  
        self.connect((self.extractPacketPayload, 0), (self.streamToVec, 0)) 
        self.connect((self.iirFilter, 0), (self.blocks_null_sink_0_0, 0))   
        self.connect((self.iirFilter, 0), (self, 1))    
        self.connect((self.spectralUdpSource, 0), (self.extractPacketPayload, 0))   
        self.connect((self.streamToVec, 0), (self.charToFloat, 0))      
    
    def stop(self):
        print self,"STOP"
        self.set_enable(False)
        self.disconnect_all()

    def get_dipIndex(self):
        return self.dipIndex

    def set_dipIndex(self, dipIndex):
        self.dipIndex = dipIndex
        self.ddcControl.set_dipIndex(self.dipIndex)

    def get_iirAvgGain(self):
        return self.iirAvgGain

    def set_iirAvgGain(self, iirAvgGain):
        self.iirAvgGain = iirAvgGain
        self.iirFilter.set_taps(2.0**-self.iirAvgGain)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        self.ddcControl.set_index(self.index)
        self.ddcControl.set_rfSource(self.index)
        self.tunerControl.set_index(self.index)

    def get_enable(self):
        return self.enable

    def set_enable(self, enable):
        self.enable = enable
        self.ddcControl.set_enable(self.enable)

    def get_localInterface(self):
        return self.localInterface

    def set_localInterface(self, localInterface):
        self.localInterface = localInterface
        self.ddcControl.set_localInterface(self.localInterface)

    def get_otherDdcArgs(self):
        return self.otherDdcArgs

    def set_otherDdcArgs(self, otherDdcArgs):
        self.otherDdcArgs = otherDdcArgs
        self.ddcControl.set_otherArgs(self.otherDdcArgs)

    def get_otherTunerArgs(self):
        return self.otherTunerArgs

    def set_otherTunerArgs(self, otherTunerArgs):
        self.otherTunerArgs = otherTunerArgs
        self.tunerControl.set_otherArgs(self.otherTunerArgs)

    def get_radioInterface(self):
        return self.radioInterface

    def set_radioInterface(self, radioInterface):
        self.radioInterface = radioInterface
        self.ddcControl.set_radioInterface(self.radioInterface)

    def get_radioParam(self):
        return self.radioParam

    def set_radioParam(self, radioParam):
        self.radioParam = radioParam

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.ddcControl.set_rate(self.rate)

    def get_rfAtten(self):
        return self.rfAtten

    def set_rfAtten(self, rfAtten):
        self.rfAtten = rfAtten
        self.tunerControl.set_attenuation(self.rfAtten)

    def get_rfFilter(self):
        return self.rfFilter

    def set_rfFilter(self, rfFilter):
        self.rfFilter = rfFilter
        self.tunerControl.set_filter(self.rfFilter)

    def get_rfFreq(self):
        return self.rfFreq

    def set_rfFreq(self, rfFreq):
        self.rfFreq = rfFreq
        self.tunerControl.set_freq(self.rfFreq)

    def get_udpPort(self):
        return self.udpPort

    def set_udpPort(self, udpPort):
        self.udpPort = udpPort
        self.ddcControl.set_udpPort(self.udpPort)

