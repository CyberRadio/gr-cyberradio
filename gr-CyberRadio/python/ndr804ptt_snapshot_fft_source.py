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
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
from gnuradio.filter import firdes
import numpy, scipy.signal
import CyberRadio

class ndr804ptt_snapshot_fft_source(gr.hier_block2):
    """
    docstring for block ndr804ptt_snapshot_fft_source
    """
    def __init__(self, avgGainList=[1.0/8,1.0/32,], dipIndex=-1, doLog10=True, enable=True, fftSize=int(2**17), fftWindowType='flattop', index=1, localInterface="", otherDdcArgs={}, otherTunerArgs={}, outSize=int((40.0/51.2)*(2**17)), radioInterface=1, radioParam={"type":"ndr804-ptt", "host":"ndr308", "port":8617, "obj":None}, rate=16, rfAtten=0, rfFilter=1, rfFreq=1000, udpPort=11000):
        numOut = len(avgGainList)+1
        gr.hier_block2.__init__(
            self, "Local NDR804-PTT Snapshot Source",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev(numOut, numOut, [gr.sizeof_float*outSize]*numOut),
        )
        self.message_port_register_hier_in("rfFreq")
        self.message_port_register_hier_in("clearAvg")
        self.message_port_register_hier_out("rfFreq")

        ##################################################
        # Parameters
        ##################################################
        self.avgGainList = avgGainList
        self.dipIndex = dipIndex
        self.doLog10 = doLog10 = bool(doLog10)
        self.enable = enable = bool(enable)
        self.fftSize = fftSize = int(fftSize)
        self.fftWindowType = fftWindowType
        self.index = index
        self.localInterface = localInterface
        self.otherDdcArgs = otherDdcArgs
        self.otherTunerArgs = otherTunerArgs
        self.outSize = outSize
        self.radioInterface = radioInterface
        self.radioParam = radioParam
        self.rate = rate
        self.rfAtten = rfAtten
        self.rfFilter = rfFilter
        self.rfFreq = rfFreq
        self.udpPort = udpPort

        ##################################################
        # Variables
        ##################################################
        self.fftWindow = fftWindow = scipy.signal.get_window(fftWindowType,fftSize)
        self.windowScale = windowScale = fftWindow.sum()/fftWindow.size
        
        ##################################################
        # Blocks
        ##################################################
        self.tunerControl = CyberRadio.generic_tuner_control_block(
                    radioParam, 
                    index, 
                    True, 
                    rfFreq, 
                    rfAtten, 
                    rfFilter, 
                    otherTunerArgs, 
                    False
                     )
        self.snapshotToVector = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftSize)
        self.snapshotSource = CyberRadio.snapshot_source_c('0.0.0.0', udpPort, fftSize, rate)
        if doLog10:
            self.log10_direct = CyberRadio.vector_nlog10_ff(10, outSize, 0)
            self.nullSink_direct = blocks.null_sink(gr.sizeof_float*outSize)
        else:
            self.log10_direct = None
        self.fftBlock = fft.fft_vcc(fftSize, True, (fftWindow/fftWindow.sum()), True, 1)
        self.extractPacketPayload = CyberRadio.vector_keep_m_in_n(gr.sizeof_gr_complex, outSize, fftSize, (fftSize-outSize)/2)
        self.ddcControl = CyberRadio.generic_ddc_control_block( 
                    radioParam, 
                    index, 
                    "", #idString
                    bool(enable), 
                    True, 
                    0, 
                    1, 
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
        self.compToMagSq = blocks.complex_to_mag_squared(outSize)
        self.avgFilterList = []
        self.avgNullSinkList = []
        self.avgLog10List = []
        
        for i in range(numOut-1):
            #cep test self.avgFilterList.append( filter.single_pole_iir_filter_ff(avgGainList[i], outSize) )
            self.avgFilterList.append( CyberRadio.vector_single_pole_iir_filter_ff(avgGainList[i], outSize, True) )
            self.avgNullSinkList.append( blocks.null_sink(gr.sizeof_float*outSize) )
            if doLog10:
                self.avgLog10List.append( CyberRadio.vector_nlog10_ff(10, outSize, 0) )
        
        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self, 'rfFreq'), (self.tunerControl, 'rfFreq'))   
        self.msg_connect((self.tunerControl, 'rfFreq'), (self, 'rfFreq'))   
                
        for i in range(numOut-1):
            self.connect((self.compToMagSq, 0), (self.avgFilterList[i], 0))
            #cep test self.msg_connect((self, 'clearAvg'), (self.avgFilterList[i], 'clear'))
            if doLog10:
                self.connect((self.avgFilterList[i], 0), (self.avgLog10List[i], 0))
                self.connect((self.avgLog10List[i], 0), (self.avgNullSinkList[i], 0))
                self.connect((self.avgLog10List[i], 0), (self, i+1))
            else:
                self.connect((self.avgFilterList[i], 0), (self.avgNullSinkList[i], 0))
                self.connect((self.avgFilterList[i], 0), (self, i+1))   
        if doLog10:
            self.connect((self.compToMagSq, 0), (self.log10_direct, 0)) 
            self.connect((self.log10_direct, 0), (self.nullSink_direct, 0)) 
            self.connect((self.log10_direct, 0), (self, 0)) 
        else:
            self.connect((self.compToMagSq, 0), (self, 0))  
        self.connect((self.extractPacketPayload, 0), (self.compToMagSq, 0))
        self.connect((self.fftBlock, 0), (self.extractPacketPayload, 0))
        self.connect((self.snapshotToVector, 0), (self.fftBlock, 0))
        self.connect((self.snapshotSource, 0), (self.snapshotToVector, 0))


    def get_avgGainList(self):
        return self.avgGainList

    def set_avgGainList(self, avgGainList):
        self.avgGainList = avgGainList
        for i,gain in enumerate(avgGainList):
            if len(self.avgFilterList)>=(i+1):
                self.avgFilterList[i].set_taps(gain)

    def get_dipIndex(self):
        return self.dipIndex

    def set_dipIndex(self, dipIndex):
        self.dipIndex = dipIndex
        self.ddcControl.set_dipIndex(self.dipIndex)

    def get_doLog10(self):
        return self.doLog10

    def set_doLog10(self, doLog10):
        self.doLog10 = doLog10

    def get_enable(self):
        return self.enable

    def set_enable(self, enable):
        self.enable = enable
        self.ddcControl.set_enable(bool(self.enable))

    def get_fftSize(self):
        return self.fftSize

    def set_fftSize(self, fftSize):
        self.fftSize = fftSize
        self.set_fftWindow(scipy.signal.get_window(self.fftWindowType,self.fftSize))

    def get_fftWindowType(self):
        return self.fftWindowType

    def set_fftWindowType(self, fftWindowType):
        self.fftWindowType = fftWindowType
        self.set_fftWindow(scipy.signal.get_window(self.fftWindowType,self.fftSize))

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        self.tunerControl.set_index(self.index)
        self.ddcControl.set_index(self.index)
        self.ddcControl.set_rfSource(self.index)

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

    def get_outSize(self):
        return self.outSize

    def set_outSize(self, outSize):
        self.outSize = outSize

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

    def clearAverage(self,boolInput):
        for i in self.avgFilterList:
            i.set_clear(bool(boolInput))
    
    def get_rfFreq(self):
        return self.rfFreq

    def set_rfFreq(self, rfFreq):
        self.set_enable(False)
        self.rfFreq = rfFreq
        self.tunerControl.set_freq(self.rfFreq)
        self.clearAverage(True)
        self.set_enable(True)

    def get_udpPort(self):
        return self.udpPort

    def set_udpPort(self, udpPort):
        self.udpPort = udpPort
        self.ddcControl.set_udpPort(self.udpPort)

    def get_fftWindow(self):
        return self.fftWindow

    def set_fftWindow(self, fftWindow):
        self.fftWindow = fftWindow

    def get_windowScale(self):
        return self.windowScale

    def set_windowScale(self, windowScale):
        self.windowScale = windowScale
