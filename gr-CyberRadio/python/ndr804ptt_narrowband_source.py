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

import CyberRadio # using gr-cyberradio vita source v2
from generic_ddc_control_block import generic_ddc_control_block

class ndr804ptt_narrowband_source(gr.hier_block2):
    """
    docstring for block ndr804ptt_narrowband_source
    """
    def __init__(self, 
                    radioParam={"type":"ndr804-ptt", "host":"ndr308", "port":8617, "obj":None}, 
                    index=1, 
                    enable=True, 
                    idString="USER", 
                    rate=0, 
                    ddcFreq=0, 
                    tunerIndex=1, 
                    radioInterface=1, 
                    dipIndex=-1, 
                    localInterface="eth6", 
                    udpPort=11000,
                    testFilename="",
                    otherDdcArgs={}, 
                     ):
        gr.hier_block2.__init__(
            self, "NDR804-PTT Narrowband IQ Source",
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )
        self.message_port_register_hier_out("control")
        self.message_port_register_hier_in("control")

        ##################################################
        # Parameters
        ##################################################
        self.ddcFreq = ddcFreq
        self.dipIndex = dipIndex
        self.index = index
        self.localInterface = localInterface
        self.otherDdcArgs = otherDdcArgs
        self.radioInterface = radioInterface
        self.radioParam = radioParam
        self.rate = rate
        self.tunerIndex = tunerIndex
        self.udpPort = udpPort
        self.enable=enable
        self.idString=idString
        self.testFilename=testFilename

        ##################################################
        # Blocks
        ##################################################
        self.vitaIqSource = CyberRadio.vita_iq_source_2( 
                    3, 
                    1024*4/4, 
                    9*4, 
                    1*4, 
                    False, 
                    True, 
                    "0.0.0.0", 
                    udpPort, 
                    False, 
                    False, 
                    False, 
                     )
        self.vecToStream = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1024/4)
        self.nullSink = blocks.null_sink(gr.sizeof_int*(9+1024/4+1))
        self.ddcControl = generic_ddc_control_block(
                    radioParam, 
                    index, 
                    self.idString,
                    enable, # enable
                    False, # wideband
                    rate, 
                    0, 
                    ddcFreq, 
                    tunerIndex, 
                    0, 
                    radioInterface, 
                    dipIndex, 
                    localInterface, 
                    udpPort, 
                    dict(otherDdcArgs), 
                    False
                     )
                     
        if self.testFilename!="":
            self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, 31250,True)
            self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
            self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, self.testFilename, True)
            self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1.0/32767, ))
             
        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ddcControl, 'control'), (self, 'control'))
        self.msg_connect((self, 'control'), (self.ddcControl, 'control'))
        
        if self.testFilename!="":
            self.connect((self.blocks_multiply_const_vxx_0, 0), (self, 0))  
            self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0, 0))                        
            self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_throttle_0, 0))          
            self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))               
        else:
            self.connect((self.vecToStream, 0), (self, 0))
            self.connect((self.vitaIqSource, 0), (self.nullSink, 0))    
            self.connect((self.vitaIqSource, 1), (self.vecToStream, 0)) 
    
    def stop(self):
        print self,"STOP"
        self.disconnect_all()
#       self.set_enable(False)

    def get_ddcFreq(self):
        return self.ddcFreq

    def set_ddcFreq(self, ddcFreq):
        self.ddcFreq = ddcFreq
        self.ddcControl.set_freq(self.ddcFreq)

    def get_dipIndex(self):
        return self.dipIndex

    def set_dipIndex(self, dipIndex):
        self.dipIndex = dipIndex
        self.ddcControl.set_dipIndex(self.dipIndex)

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        self.ddcControl.set_index(self.index)

    def get_enable(self):
        return self.enable

    def set_enable(self, enable):
        print self,"set_enable(self, %r)"%enable
        self.enable = enable
        self.ddcControl.set_enable(self.enable)

    def get_idString(self):
        return self.idString

    def set_idString(self, idString):
        self.idString = idString
 
    def get_localInterface(self):
        return self.localInterface

    def set_localInterface(self, localInterface):
        self.localInterface = localInterface
        self.ddcControl.set_localInterface(self.localInterface)

    def get_otherDdcArgs(self):
        return self.otherDdcArgs

    def set_otherDdcArgs(self, otherDdcArgs):
        self.otherDdcArgs = otherDdcArgs
        self.ddcControl.set_otherArgs(dict(self.otherDdcArgs))

    def get_otherTunerArgs(self):
        return self.otherTunerArgs

    def set_otherTunerArgs(self, otherTunerArgs):
        self.otherTunerArgs = otherTunerArgs

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

    def get_tunerIndex(self):
        return self.tunerIndex

    def set_tunerIndex(self, tunerIndex):
        self.tunerIndex = tunerIndex
        self.ddcControl.set_rfSource(self.tunerIndex)

    def get_udpPort(self):
        return self.udpPort

    def set_udpPort(self, udpPort):
        self.udpPort = udpPort
        self.ddcControl.set_udpPort(self.udpPort)

