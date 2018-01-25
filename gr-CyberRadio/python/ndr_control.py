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

import random
import numpy
from gnuradio import gr

import CyberRadio
import CyberRadioDriver as crd
import CyberRadioDriver.configKeys as cfgKeys
#~ import TestSupportTools
import json

def printJson(obj):
    print json.dumps(obj, indent=4, sort_keys=True)

class ndr_control(gr.hier_block2):
    configuring = False
    radio_cmd = None
    radio_rsp = ""
    
    radioType = None
    hostname = None
    verbose = None
    interface = None
    dataPort = None
    tunerFreq = None
    tunerAtten = None
    tunerFilter = None
    tunerIndex = None
    calFrequency = None
    wbddcEnable = None
    wbddcVitaLevel = None
    wbddcRate = None
    wbddcFormat = None
    wbddcFreq = None
    wbddcPort = None
    wbddcIndex = None
    specAlpha = None
    specRate = None
    nbddcEnable = None
    nbddcVitaLevel = None
    nbddcRate = None
    nbddcFormat = 0
    nbddcDemodType = None
    nbddcDemodBfo = None
    nbddcDemodDcBlock = None
    nbddcDemodAlcType = None
    nbddcDemodAlcLevel = None
    nbddcDemodSquelchLevel = None
    nbddcDagcType = None
    nbddcDagcLevel = None
    nbddcFreq = None
    nbddcPort = None
    nbddcIndex = None
    otherNbddcEnable = None
    otherNbddcPort = None
    
    radio = None
    dipIndex = None
    sourceIp = None
    destIp = None
    destMac = None
    wbddcDipIndex = 100
    spectralDipIndex = wbddcDipIndex+4
    nbddcDipIndex = wbddcDipIndex+1
    otherNbddcDipIndex = wbddcDipIndex+2
    demodDipIndex = wbddcDipIndex+5
    
    """
    docstring for block ndr_control
    """
    def __init__(self, radioType="ndr804", 
                        hostname="ndr308", 
                        verbose=True,
                        interface="eth6",
                        dataPort = 1,
                        tunerFreq=1000, 
                        tunerAtten=0,
                        tunerFilter=1, 
                        tunerIndex=1,
                        calFrequency = 0,
                        wbddcEnable=True, 
                        wbddcVitaLevel=3,
                        wbddcRate=0, 
                        wbddcFormat=1,
                        wbddcFreq=0.0, 
                        wbddcPort=10100,
                        wbddcIndex=1, 
                        specRate = 1, 
                        nbddcEnable=True, 
                        nbddcVitaLevel=3,
                        nbddcRate=0.0, 
                        #~ nbddcFormat=0,
                        nbddcDemodType=0,
                        nbddcDemodBfo=0,
                        nbddcDemodDcBlock=0,
                        nbddcDemodAlcType=0,
                        nbddcDemodAlcLevel=0,
                        nbddcDemodSquelchLevel=0,
                        nbddcDagcType=0,
                        nbddcDagcLevel=0,
                        nbddcFreq=0.0,
                        nbddcPort=10101,
                        nbddcIndex=46,
                        otherNbddcEnable=False,
                        otherNbddcPort=10102,
                    ):
        gr.hier_block2.__init__(self, "CyberRadio/NDR_demo_control",
                                gr.io_signature(0, 0, 0),
                                gr.io_signature(1, 1, gr.sizeof_char*1),
                                 )
        self.fileLikeObjectSource = CyberRadio.file_like_object_source()
        self.connect((self.fileLikeObjectSource, 0), (self, 0))
        
        print("radioType = %r (%s)"%(radioType,type(radioType)))
        print("hostname = %r (%s)"%(hostname,type(hostname)))
        print("verbose = %r (%s)"%(verbose,type(verbose)))
        print("interface = %r (%s)"%(interface,type(interface)))
        print("dataPort = %r (%s)"%(dataPort,type(dataPort)))
        print("tunerFreq = %r (%s)"%(tunerFreq,type(tunerFreq)))
        print("tunerAtten = %r (%s)"%(tunerAtten,type(tunerAtten)))
        print("tunerIndex = %r (%s)"%(tunerIndex,type(tunerIndex)))
        print("calFrequency = %r (%s)"%(calFrequency,type(calFrequency)))
        print("wbddcEnable = %r (%s)"%(wbddcEnable,type(wbddcEnable)))
        print("wbddcVitaLevel = %r (%s)"%(wbddcVitaLevel,type(wbddcVitaLevel)))
        print("wbddcRate = %r (%s)"%(wbddcRate,type(wbddcRate)))
        print("wbddcFormat = %r (%s)"%(wbddcFormat,type(wbddcFormat)))
        print("wbddcFreq = %r (%s)"%(wbddcFreq,type(wbddcFreq)))
        print("wbddcPort = %r (%s)"%(wbddcPort,type(wbddcPort)))
        print("wbddcIndex = %r (%s)"%(wbddcIndex,type(wbddcIndex)))
        print("specRate = %r (%s)"%(specRate,type(specRate)))
        print("nbddcEnable = %r (%s)"%(nbddcEnable,type(nbddcEnable)))
        print("nbddcVitaLevel = %r (%s)"%(nbddcVitaLevel,type(nbddcVitaLevel)))
        print("nbddcRate = %r (%s)"%(nbddcRate,type(nbddcRate)))
        print("nbddcFreq = %r (%s)"%(nbddcFreq,type(nbddcFreq)))
        print("nbddcPort = %r (%s)"%(nbddcPort,type(nbddcPort)))
        print("nbddcIndex = %r (%s)"%(nbddcIndex,type(nbddcIndex)))
        print("otherNbddcEnable = %r (%s)"%(otherNbddcEnable,type(otherNbddcEnable)))
        print("otherNbddcPort = %r (%s)"%(otherNbddcPort,type(otherNbddcPort)))
        
        self.init = True
        self.set_radioType( radioType )
        self.set_hostname( hostname )
        self.set_verbose( verbose )
        #~ self.set_interface( interface )
        #~ self.set_dataPort( dataPort )
        self.set_tunerFreq( tunerFreq )
        self.set_tunerAtten( tunerAtten )
        self.set_tunerFilter( tunerFilter )
        self.set_tunerIndex( tunerIndex )
        self.set_calFrequency( calFrequency )
        self.set_wbddcEnable( wbddcEnable )
        self.set_wbddcVitaLevel( wbddcVitaLevel )
        self.set_wbddcRate( wbddcRate )
        self.set_wbddcFormat( wbddcFormat )
        self.set_wbddcFreq( wbddcFreq )
        self.set_wbddcPort( wbddcPort )
        self.set_wbddcIndex( wbddcIndex )
        self.set_specRate( specRate )
        self.set_nbddcEnable( nbddcEnable )
        self.set_nbddcVitaLevel( nbddcVitaLevel )
        self.set_nbddcRate( nbddcRate )
        #~ self.set_nbddcFormat( nbddcFormat )
        self.set_nbddcDemodType( nbddcDemodType )
        self.set_nbddcDemodBfo( nbddcDemodBfo )
        self.set_nbddcDemodDcBlock( nbddcDemodDcBlock )
        self.set_nbddcDemodAlcType( nbddcDemodAlcType )
        self.set_nbddcDemodAlcLevel( nbddcDemodAlcLevel )
        self.set_nbddcDemodSquelchLevel( nbddcDemodSquelchLevel )
        self.set_nbddcDagcType( nbddcDagcType )
        self.set_nbddcDagcLevel( nbddcDagcLevel )
        self.set_nbddcFreq( nbddcFreq )
        self.set_nbddcPort( nbddcPort )
        self.set_nbddcIndex( nbddcIndex )
        self.set_otherNbddcEnable( otherNbddcEnable )
        self.set_otherNbddcPort( otherNbddcPort )
        
        self.init = False
        self.radio = crd.getRadioObject(self.radioType, 
                                        verbose=self.verbose, 
                                        logFile=self.fileLikeObjectSource, 
                                         )
        self.radio.connect("tcp", self.hostname, 8617)
        self.set_dataPort(interface, dataPort)
        for dipIndex,udpPort in ((self.wbddcDipIndex,self.wbddcPort),
                                    (self.nbddcDipIndex,self.nbddcPort),
                                    (self.otherNbddcDipIndex,self.otherNbddcPort),
                                    (self.spectralDipIndex,self.wbddcPort+4),
                                    (self.demodDipIndex,self.wbddcPort+5),
                                     ):
            self.setDipEntry(dipIndex,udpPort)
        self.disableWbddc(True)
        self.disableNbddc(True)
        self.updateWbddc()
        self.updateNbddc()
        self.updateTuner()
        self.updateCal()
    
    def stop(self,):
        print "STOP"
        self.disableNbddc(True)
        self.disableWbddc(True)

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        output_items[0][:] = input_items[0]
        consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
    
    def set_radioType(self, radioType):
        if radioType != self.radioType:
            print "Changing radioType from %r -> %r"%(self.radioType,radioType)
            self.radioType = radioType

    def set_hostname(self, hostname):
        if hostname != self.hostname:
            print "Changing hostname from %r -> %r"%(self.hostname,hostname)
            self.hostname = hostname

    def set_verbose(self, verbose):
        if verbose != self.verbose:
            print "Changing verbose from %r -> %r"%(self.verbose,verbose)
            self.verbose = verbose

    #~ def set_interface(self, interface):
        #~ if interface != self.interface:
            #~ print "Changing interface from %r -> %r"%(self.interface,interface)
            #~ self.interface = interface
#~ 
    #~ def set_dataPort(self, dataPort):
        #~ if dataPort != self.dataPort:
            #~ print "Changing dataPort from %r -> %r"%(self.dataPort,dataPort)
            #~ self.dataPort = dataPort



    def set_dataPort(self, interface, dataPort):
        print "set_dataPort(%s, %s)"%(interface, dataPort,)
        self.interface = interface
        self.dataPort = dataPort
        self.destMac,self.destIp = crd.getInterfaceAddresses(interface)
        self.sourceIp = ".".join(self.destIp.split(".")[:-1] + [str(int(self.destIp.split(".")[-1])+10),])
        conf = {crd.configKeys.CONFIG_IP:{
                    self.dataPort: {crd.configKeys.IP_SOURCE: self.sourceIp,
                                    #~ crd.configKeys.IP_DEST: { 0: {cfgKeys.GIGE_SOURCE_PORT:self.wbddcPort,
                                                                    #~ cfgKeys.GIGE_DEST_PORT:self.wbddcPort,
                                                                    #~ cfgKeys.GIGE_MAC_ADDR:self.destMac,
                                                                    #~ cfgKeys.GIGE_IP_ADDR:self.destIp,
                                                                    #~ },
                                                                #~ 1: {cfgKeys.GIGE_SOURCE_PORT:self.nbddcPort,
                                                                    #~ cfgKeys.GIGE_DEST_PORT:self.nbddcPort,
                                                                    #~ cfgKeys.GIGE_MAC_ADDR:self.destMac,
                                                                    #~ cfgKeys.GIGE_IP_ADDR:self.destIp,
                                                                    #~ },
                                                            #~ }
                                    }
                        }
                    }
        #~ printJson(conf)
        self.radio.setConfiguration(conf)

    def set_tunerIndex(self, tunerIndex):
        if tunerIndex != self.tunerIndex:
            print "Changing tunerIndex from %r -> %r"%(self.tunerIndex,tunerIndex)
            self.tunerIndex = tunerIndex
            self.updateTuner()
            self.updateNbddc()

    def set_tunerFreq(self, tunerFreq):
        if tunerFreq != self.tunerFreq:
            print "Changing tunerFreq from %r -> %r"%(self.tunerFreq,tunerFreq)
            self.tunerFreq = tunerFreq
            self.updateTuner(updateFreq=True)

    def set_tunerAtten(self, tunerAtten):
        if tunerAtten != self.tunerAtten:
            print "Changing tunerAtten from %r -> %r"%(self.tunerAtten,tunerAtten)
            self.tunerAtten = tunerAtten
            self.updateTuner(updateAtten=True)

    def set_tunerFilter(self, tunerFilter):
        if tunerFilter != self.tunerFilter:
            print "Changing tunerFilter from %r -> %r"%(self.tunerFilter,tunerFilter)
            self.tunerFilter = tunerFilter
            self.updateTuner(updateFilter=True)
    
    def set_calFrequency(self, calFrequency):
        if calFrequency != self.calFrequency:
            print "Changing calFrequency from %r -> %r"%(self.calFrequency,calFrequency)
            self.calFrequency = calFrequency
            self.updateCal()

    def set_wbddcIndex(self, wbddcIndex):
        if wbddcIndex != self.wbddcIndex:
            print "Changing wbddcIndex from %r -> %r"%(self.wbddcIndex,wbddcIndex)
            self.disableWbddc()
            self.wbddcIndex = wbddcIndex
            self.updateWbddc()

    def set_wbddcEnable(self, wbddcEnable):
        if wbddcEnable != self.wbddcEnable:
            print "Changing wbddcEnable from %r -> %r"%(self.wbddcEnable,wbddcEnable)
            self.wbddcEnable = wbddcEnable
            self.updateWbddc()

    def set_wbddcVitaLevel(self, wbddcVitaLevel):
        if wbddcVitaLevel != self.wbddcVitaLevel:
            print "Changing wbddcVitaLevel from %r -> %r"%(self.wbddcVitaLevel,wbddcVitaLevel)
            self.wbddcVitaLevel = wbddcVitaLevel
            self.updateWbddc()

    def set_wbddcRate(self, wbddcRate):
        if wbddcRate != self.wbddcRate:
            print "Changing wbddcRate from %r -> %r"%(self.wbddcRate,wbddcRate)
            self.wbddcRate = wbddcRate
            self.updateWbddc()

    def set_wbddcFormat(self, wbddcFormat):
        if wbddcFormat != self.wbddcFormat:
            print "Changing wbddcFormat from %r -> %r"%(self.wbddcFormat,wbddcFormat)
            self.disableWbddc()
            self.wbddcFormat = wbddcFormat
            self.updateWbddc()

    def set_wbddcFreq(self, wbddcFreq):
        if wbddcFreq != self.wbddcFreq:
            print "Changing wbddcFreq from %r -> %r"%(self.wbddcFreq,wbddcFreq)
            self.wbddcFreq = wbddcFreq
            self.updateWbddc()

    def set_wbddcPort(self, wbddcPort):
        if wbddcPort != self.wbddcPort:
            print "Changing wbddcPort from %r -> %r"%(self.wbddcPort,wbddcPort)
            self.wbddcPort = wbddcPort
            self.setDipEntry(self.wbddcDipIndex,self.wbddcPort)
            self.setDipEntry(self.wbddcDipIndex+4,self.wbddcPort+4)
            self.updateWbddc()

    def set_specAlpha(self, specAlpha):
        if specAlpha != self.specAlpha:
            print "Changing specAlpha from %r -> %r"%(self.specAlpha,specAlpha)
            self.specAlpha = specAlpha
            self.updateWbddc()

    def set_specRate(self, specRate):
        if specRate != self.specRate:
            print "Changing specRate from %r -> %r"%(self.specRate,specRate)
            self.specRate = specRate
            self.updateWbddc()


    def set_nbddcIndex(self, nbddcIndex):
        if nbddcIndex != self.nbddcIndex:
            print "Changing nbddcIndex from %r -> %r"%(self.nbddcIndex,nbddcIndex)
            self.disableNbddc()
            self.nbddcIndex = nbddcIndex
            self.updateNbddc()

    def set_nbddcEnable(self, nbddcEnable):
        if nbddcEnable != self.nbddcEnable:
            print "Changing nbddcEnable from %r -> %r"%(self.nbddcEnable,nbddcEnable)
            self.nbddcEnable = nbddcEnable
            self.updateNbddc(updateDdc=True)

    def set_nbddcVitaLevel(self, nbddcVitaLevel):
        if nbddcVitaLevel != self.nbddcVitaLevel:
            print "Changing nbddcVitaLevel from %r -> %r"%(self.nbddcVitaLevel,nbddcVitaLevel)
            self.nbddcVitaLevel = nbddcVitaLevel
            self.updateNbddc(updateDdc=True)

    def set_nbddcRate(self, nbddcRate):
        if nbddcRate != self.nbddcRate:
            print "Changing nbddcRate from %r -> %r"%(self.nbddcRate,nbddcRate)
            self.nbddcRate = nbddcRate
            self.updateNbddc(updateDdc=True,updateDemod=(self.nbddcFormat==1))

    #~ def set_nbddcFormat(self, nbddcFormat):
        #~ if nbddcFormat != self.nbddcFormat:
            #~ print "Changing nbddcFormat from %r -> %r"%(self.nbddcFormat,nbddcFormat)
            #~ self.nbddcFormat = nbddcFormat
            #~ self.updateNbddc()

    def set_nbddcDemodType(self, nbddcDemodType):
        if nbddcDemodType != self.nbddcDemodType and self.radioType=="ndr328":
            print "Changing nbddcDemodType from %r -> %r"%(self.nbddcDemodType,nbddcDemodType)
            self.nbddcFormat = 0 if nbddcDemodType<0 else 1
            self.nbddcDemodType = nbddcDemodType
            self.updateNbddc(updateDemod=True, updateAlc=True)

    def set_nbddcDemodBfo(self, nbddcDemodBfo):
        if nbddcDemodBfo != self.nbddcDemodBfo and self.radioType=="ndr328":
            print "Changing nbddcDemodBfo from %r -> %r"%(self.nbddcDemodBfo,nbddcDemodBfo)
            self.nbddcDemodBfo = nbddcDemodBfo
            #~ self.updateNbddc()
            if (not self.init) and (self.nbddcFormat==1):
                print self.radio.sendCommand("BFO %d, %d\n"%(self.nbddcIndex,self.nbddcDemodBfo))

    def set_nbddcDemodDcBlock(self, nbddcDemodDcBlock):
        if nbddcDemodDcBlock != self.nbddcDemodDcBlock and self.radioType=="ndr328":
            print "Changing nbddcDemodDcBlock from %r -> %r"%(self.nbddcDemodDcBlock,nbddcDemodDcBlock)
            self.nbddcDemodDcBlock = nbddcDemodDcBlock
            self.updateNbddc(updateDemod=True)

    def set_nbddcDemodAlcType(self, nbddcDemodAlcType):
        if nbddcDemodAlcType != self.nbddcDemodAlcType and self.radioType=="ndr328":
            print "Changing nbddcDemodAlcType from %r -> %r"%(self.nbddcDemodAlcType,nbddcDemodAlcType)
            self.nbddcDemodAlcType = nbddcDemodAlcType
            self.updateNbddc(updateAlc=True)

    def set_nbddcDemodAlcLevel(self, nbddcDemodAlcLevel):
        if nbddcDemodAlcLevel != self.nbddcDemodAlcLevel and self.radioType=="ndr328":
            print "Changing nbddcDemodAlcLevel from %r -> %r"%(self.nbddcDemodAlcLevel,nbddcDemodAlcLevel)
            self.nbddcDemodAlcLevel = nbddcDemodAlcLevel
            self.updateNbddc(updateAlc=True)

    def set_nbddcDemodSquelchLevel(self, nbddcDemodSquelchLevel):
        if nbddcDemodSquelchLevel != self.nbddcDemodSquelchLevel and self.radioType=="ndr328":
            print "Changing nbddcDemodSquelchLevel from %r -> %r"%(self.nbddcDemodSquelchLevel,nbddcDemodSquelchLevel)
            self.nbddcDemodSquelchLevel = nbddcDemodSquelchLevel
            self.updateNbddc(updateAlc=True)

    def set_nbddcDagcType(self, nbddcDagcType):
        if nbddcDagcType != self.nbddcDagcType and self.radioType=="ndr328":
            print "Changing nbddcDagcType from %r -> %r"%(self.nbddcDagcType,nbddcDagcType)
            self.nbddcDagcType = nbddcDagcType
            self.updateNbddc(updateAlc=True)

    def set_nbddcDagcLevel(self, nbddcDagcLevel):
        if nbddcDagcLevel != self.nbddcDagcLevel and self.radioType=="ndr328":
            print "Changing nbddcDagcLevel from %r -> %r"%(self.nbddcDagcLevel,nbddcDagcLevel)
            self.nbddcDagcLevel = nbddcDagcLevel
            self.updateNbddc(updateAlc=True)

    def set_nbddcFreq(self, nbddcFreq):
        if nbddcFreq != self.nbddcFreq:
            print "Changing nbddcFreq from %r -> %r"%(self.nbddcFreq,nbddcFreq)
            self.nbddcFreq = nbddcFreq
            self.updateNbddc(updateDdc=True)

    def set_nbddcPort(self, nbddcPort):
        if nbddcPort != self.nbddcPort:
            print "Changing nbddcPort from %r -> %r"%(self.nbddcPort,nbddcPort)
            self.nbddcPort = nbddcPort
            self.setDipEntry(self.nbddcDipIndex,self.nbddcPort)
            self.updateNbddc()
    
    def set_otherNbddcPort(self, otherNbddcPort):
        if otherNbddcPort != self.otherNbddcPort:
            print "Changing nbddcPort from %r -> %r"%(self.otherNbddcPort,otherNbddcPort)
            self.otherNbddcPort = otherNbddcPort
            self.setDipEntry(self.otherNbddcDipIndex, self.otherNbddcPort)
            self.updateNbddc()
    
    def set_otherNbddcEnable(self, otherNbddcEnable):
        if otherNbddcEnable != self.otherNbddcEnable:
            print "Changing otherNbddcEnable from %r -> %r"%(self.otherNbddcEnable,otherNbddcEnable)
            self.otherNbddcEnable = otherNbddcEnable
            self.disableNbddc(True)
            self.updateNbddc()
    
    def disableWbddc(self,allddc=False):
        self.configuring = True#False
        if self.radio is not None and (allddc or self.wbddcIndex is not None):
            conf = { crd.configKeys.CONFIG_DDC: { 
                        crd.configKeys.CONFIG_WBDDC: { 
                            crd.configKeys.ALL if allddc else self.wbddcIndex: { 
                                            crd.configKeys.ENABLE: 0,
                                            crd.configKeys.DDC_STREAM_ID: 0,
                                        }
                            }
                        }
                    }
            printJson(conf)
            self.radio.setConfiguration(conf)
        self.configuring = False
    
    def updateWbddc(self,):
        self.configuring = True#False
        print "updateWbddc!",self.wbddcIndex, self.wbddcFreq, self.wbddcRate
        if (self.radio is not None) and (not self.init) and (self.wbddcIndex is not None and self.wbddcIndex>0):
            conf = { crd.configKeys.CONFIG_DDC: { 
                        crd.configKeys.CONFIG_WBDDC: { 
                            #~ crd.configKeys.ALL:{ 
                                                #~ crd.configKeys.ENABLE: False,
                                                 #~ },
                            self.wbddcIndex: { 
                                            crd.configKeys.NBDDC_RF_INDEX: self.tunerIndex, 
                                            crd.configKeys.DDC_FREQUENCY_OFFSET: self.wbddcFreq, 
                                            crd.configKeys.DDC_RATE_INDEX: self.wbddcRate, 
                                            crd.configKeys.DDC_OUTPUT_FORMAT: self.wbddcFormat, 
                                            crd.configKeys.DDC_UDP_DESTINATION: self.wbddcDipIndex if (self.wbddcFormat==1) else self.wbddcDipIndex+4,
                                            #~ crd.configKeys.ENABLE: (self.wbddcVitaLevel if (self.wbddcFormat==1) else 1) if self.wbddcEnable else 0,
                                            crd.configKeys.ENABLE: self.wbddcVitaLevel if self.wbddcEnable else 0,
                                            crd.configKeys.DDC_SPECTRAL_FRAME_RATE: self.specRate,
                                            crd.configKeys.DDC_VITA_ENABLE: self.wbddcVitaLevel,
                                            crd.configKeys.DDC_STREAM_ID: 0x8000|((self.wbddcRate&0xf)<<8)|(self.wbddcIndex&0x00ff),
                                            crd.configKeys.DDC_DATA_PORT: self.dataPort, 
                                        }
                            }
                        }
                    }
            printJson(conf)
            self.radio.setConfiguration(conf)
        self.configuring = False
    
    def disableNbddc(self,allddc=False):
        self.configuring = True#False
        if self.radio is not None and (allddc or self.nbddcIndex is not None):
            conf = { crd.configKeys.CONFIG_DDC: { 
                        crd.configKeys.CONFIG_NBDDC: { 
                            #~ crd.configKeys.ALL if allddc else self.nbddcIndex: { 
                                            #~ crd.configKeys.DDC_FREQUENCY_OFFSET: 0, 
                                            #~ crd.configKeys.DDC_RATE_INDEX: 0, 
                                            #~ crd.configKeys.ENABLE: 0,
                                            #~ crd.configKeys.DDC_VITA_ENABLE: 0,
                                            #~ crd.configKeys.DDC_STREAM_ID: 0,
                                            #~ crd.configKeys.DDC_UDP_DESTINATION: self.wbddcDipIndex,
                                        #~ }
                            }
                        }
                    }
            if allddc:
                for nbddcIndex in self.radio.getNbddcIndexRange():
                    if nbddcIndex != self.nbddcIndex:
                        rate = random.choice( self.radio.getNbddcRateSet(nbddcIndex).keys() )
                        conf[crd.configKeys.CONFIG_DDC][crd.configKeys.CONFIG_NBDDC][nbddcIndex] = { 
                                                crd.configKeys.DDC_FREQUENCY_OFFSET: random.randint(-20000000,20000000) if self.otherNbddcEnable else 0, 
                                                #~ crd.configKeys.DDC_FREQUENCY_OFFSET: nbddcIndex*100e3 if self.otherNbddcEnable else 0, 
                                                #~ crd.configKeys.DDC_FREQUENCY_OFFSET: 0.0 if self.otherNbddcEnable else 0, 
                                                crd.configKeys.DDC_RATE_INDEX: rate if self.otherNbddcEnable else 0, 
                                                crd.configKeys.ENABLE: self.nbddcVitaLevel if self.otherNbddcEnable else 0,
                                                crd.configKeys.DDC_VITA_ENABLE: self.nbddcVitaLevel if self.otherNbddcEnable else 0,
                                                crd.configKeys.DDC_STREAM_ID: ((rate&0xf)<<8)|(nbddcIndex&0x00ff) if self.otherNbddcEnable else 0,
                                                crd.configKeys.DDC_UDP_DESTINATION: self.otherNbddcDipIndex if self.otherNbddcEnable else 0,
                                                crd.configKeys.DDC_DATA_PORT: self.dataPort, 
                                                crd.configKeys.DDC_OUTPUT_FORMAT: 0, 
                                                crd.configKeys.DDC_DEMOD_TYPE: 0, 
                                                crd.configKeys.DDC_BEAT_FREQ_OSC: 0, 
                                                }
            else:
                rate = random.choice( self.radio.getNbddcRateSet(self.nbddcIndex).keys() )
                conf[crd.configKeys.CONFIG_DDC][crd.configKeys.CONFIG_NBDDC][self.nbddcIndex] = { 
                                            #~ crd.configKeys.DDC_FREQUENCY_OFFSET: random.randint(-20000000,20000000) if self.otherNbddcEnable else 0, 
                                            #~ crd.configKeys.DDC_FREQUENCY_OFFSET: self.nbddcIndex*100e3 if self.otherNbddcEnable else 0, 
                                            crd.configKeys.DDC_FREQUENCY_OFFSET: 0.0 if self.otherNbddcEnable else 0, 
                                            crd.configKeys.DDC_RATE_INDEX: rate if self.otherNbddcEnable else 0, 
                                            crd.configKeys.ENABLE: self.nbddcVitaLevel if self.otherNbddcEnable else 0,
                                            crd.configKeys.DDC_VITA_ENABLE: self.nbddcVitaLevel if self.otherNbddcEnable else 0,
                                            crd.configKeys.DDC_STREAM_ID: ((rate&0xf)<<8)|(self.nbddcIndex&0x00ff) if self.otherNbddcEnable else 0,
                                            crd.configKeys.DDC_UDP_DESTINATION: self.nbddcDipIndex+1 if self.otherNbddcEnable else 0,
                                            crd.configKeys.DDC_DATA_PORT: self.dataPort, 
                                            crd.configKeys.DDC_OUTPUT_FORMAT: 0, 
                                            crd.configKeys.DDC_DEMOD_TYPE: 0, 
                                            crd.configKeys.DDC_BEAT_FREQ_OSC: 0, 
                                            }
                printJson(conf)
            self.radio.setConfiguration(conf)
        self.configuring = False
    
    def updateNbddc(self,updateDdc=False,updateDemod=False,updateAlc=False):
        self.configuring = True
        if (self.radio is not None) and (not self.init) and (self.nbddcIndex is not None):
            confDict = {}
            updateAll = all(not(i) for i in (updateDdc,updateDemod,updateAlc))
            if updateAll:
                confDict.update( { 
                                    #~ crd.configKeys.NBDDC_RF_INDEX: self.tunerIndex, 
                                    #~ crd.configKeys.DDC_FREQUENCY_OFFSET: self.nbddcFreq, 
                                    #~ crd.configKeys.DDC_RATE_INDEX: self.nbddcRate, 
                                    #~ crd.configKeys.DDC_OUTPUT_FORMAT: self.nbddcFormat, 
                                    #~ crd.configKeys.DDC_UDP_DESTINATION: self.nbddcDipIndex if self.nbddcFormat==0 else self.demodDipIndex,
                                    #~ crd.configKeys.ENABLE: self.nbddcVitaLevel if self.nbddcEnable else 0,
                                    #~ crd.configKeys.DDC_VITA_ENABLE: self.nbddcVitaLevel,
                                    #~ crd.configKeys.DDC_STREAM_ID: ((self.nbddcRate&0xf)<<8)|(self.nbddcIndex&0x00ff),
                                    crd.configKeys.DDC_DATA_PORT: self.dataPort, 
                                    #~ crd.configKeys.DDC_DEMOD_TYPE: self.nbddcDemodType, 
                                    #~ crd.configKeys.DDC_BEAT_FREQ_OSC: self.nbddcDemodBfo, 
                                    #~ crd.configKeys.DDC_DEMOD_DC_BLOCK: self.nbddcDemodDcBlock, 
                                    #~ crd.configKeys.DDC_DEMOD_ALC_LEVEL: self.nbddcDemodAlcLevel, 
                                    #~ crd.configKeys.DDC_DEMOD_ALC_TYPE: self.nbddcDemodAlcType, 
                                     } )
            if updateAll or updateDdc:
                confDict.update( { 
                                    crd.configKeys.NBDDC_RF_INDEX: self.tunerIndex, 
                                    crd.configKeys.DDC_FREQUENCY_OFFSET: self.nbddcFreq, 
                                    crd.configKeys.DDC_RATE_INDEX: self.nbddcRate, 
                                    crd.configKeys.DDC_OUTPUT_FORMAT: self.nbddcFormat, 
                                    crd.configKeys.DDC_UDP_DESTINATION: self.nbddcDipIndex if self.nbddcFormat==0 else self.demodDipIndex,
                                    crd.configKeys.ENABLE: self.nbddcVitaLevel if self.nbddcEnable else 0,
                                    crd.configKeys.DDC_VITA_ENABLE: self.nbddcVitaLevel,
                                    crd.configKeys.DDC_STREAM_ID: ((self.nbddcRate&0xf)<<8)|(self.nbddcIndex&0x00ff),
                                    #~ crd.configKeys.DDC_DATA_PORT: self.dataPort, 
                                    #~ crd.configKeys.DDC_DEMOD_TYPE: self.nbddcDemodType, 
                                    #~ crd.configKeys.DDC_BEAT_FREQ_OSC: self.nbddcDemodBfo, 
                                    #~ crd.configKeys.DDC_DEMOD_DC_BLOCK: self.nbddcDemodDcBlock, 
                                    #~ crd.configKeys.DDC_DEMOD_ALC_LEVEL: self.nbddcDemodAlcLevel, 
                                    #~ crd.configKeys.DDC_DEMOD_ALC_TYPE: self.nbddcDemodAlcType, 
                                     } )
            if updateAll or updateDemod:
                confDict.update( { 
                                    #~ crd.configKeys.NBDDC_RF_INDEX: self.tunerIndex, 
                                    #~ crd.configKeys.DDC_FREQUENCY_OFFSET: self.nbddcFreq, 
                                    #~ crd.configKeys.DDC_RATE_INDEX: self.nbddcRate, 
                                    crd.configKeys.DDC_OUTPUT_FORMAT: self.nbddcFormat, 
                                    crd.configKeys.DDC_UDP_DESTINATION: self.nbddcDipIndex if self.nbddcFormat==0 else self.demodDipIndex,
                                    #~ crd.configKeys.ENABLE: self.nbddcVitaLevel if self.nbddcEnable else 0,
                                    #~ crd.configKeys.DDC_VITA_ENABLE: self.nbddcVitaLevel,
                                    #~ crd.configKeys.DDC_STREAM_ID: ((self.nbddcRate&0xf)<<8)|(self.nbddcIndex&0x00ff),
                                    #~ crd.configKeys.DDC_DATA_PORT: self.dataPort, 
                                    crd.configKeys.DDC_DEMOD_TYPE: 0 if self.nbddcDemodType not in (0,1,2,3,4) else self.nbddcDemodType, 
                                    crd.configKeys.DDC_BEAT_FREQ_OSC: self.nbddcDemodBfo, 
                                    crd.configKeys.DDC_DEMOD_DC_BLOCK: self.nbddcDemodDcBlock, 
                                    #~ crd.configKeys.DDC_DEMOD_ALC_LEVEL: self.nbddcDemodAlcLevel, 
                                    #~ crd.configKeys.DDC_DEMOD_ALC_TYPE: self.nbddcDemodAlcType, 
                                     } )
            if updateAll or updateAlc:
                confDict.update( { 
                                    #~ crd.configKeys.NBDDC_RF_INDEX: self.tunerIndex, 
                                    #~ crd.configKeys.DDC_FREQUENCY_OFFSET: self.nbddcFreq, 
                                    #~ crd.configKeys.DDC_RATE_INDEX: self.nbddcRate, 
                                    #~ crd.configKeys.DDC_OUTPUT_FORMAT: self.nbddcFormat, 
                                    #~ crd.configKeys.DDC_UDP_DESTINATION: self.nbddcDipIndex if self.nbddcFormat==0 else self.demodDipIndex,
                                    #~ crd.configKeys.ENABLE: self.nbddcVitaLevel if self.nbddcEnable else 0,
                                    #~ crd.configKeys.DDC_VITA_ENABLE: self.nbddcVitaLevel,
                                    #~ crd.configKeys.DDC_STREAM_ID: ((self.nbddcRate&0xf)<<8)|(self.nbddcIndex&0x00ff),
                                    #~ crd.configKeys.DDC_DATA_PORT: self.dataPort, 
                                    #~ crd.configKeys.DDC_DEMOD_TYPE: self.nbddcDemodType, 
                                    #~ crd.configKeys.DDC_BEAT_FREQ_OSC: self.nbddcDemodBfo, 
                                    #~ crd.configKeys.DDC_DEMOD_DC_BLOCK: self.nbddcDemodDcBlock, 
                                    crd.configKeys.DDC_DEMOD_ALC_LEVEL: self.nbddcDemodAlcLevel, 
                                    crd.configKeys.DDC_DEMOD_ALC_TYPE: self.nbddcDemodAlcType, 
                                    crd.configKeys.DDC_DEMOD_SQUELCH_LEVEL: self.nbddcDemodSquelchLevel, 
                                    crd.configKeys.DDC_DGC_MODE: self.nbddcDagcType, 
                                    crd.configKeys.DDC_DGC_GAIN: self.nbddcDagcLevel, 
                                     } )
            
            conf = { crd.configKeys.CONFIG_DDC: { 
                        crd.configKeys.CONFIG_NBDDC: { 
                                                    self.nbddcIndex: confDict, 
                                                         }
                        }
                    }
            printJson(conf)
            self.radio.setConfiguration(conf)
        self.configuring = False
    
    def updateTuner(self,updateFreq=False,updateAtten=False,updateFilter=False):
        self.configuring = True
        if (self.radio is not None) and (not self.init) and (self.tunerIndex is not None):
            updateAll = all(not(i) for i in (updateFreq,updateAtten,updateFilter))
            confDict = {}
            if updateAll:
                confDict.update( { crd.configKeys.ENABLE: True, } )
            if updateAll or updateFreq:
                confDict.update( { crd.configKeys.TUNER_FREQUENCY: self.tunerFreq, } )
            if updateAll or updateAtten:
                confDict.update( { crd.configKeys.TUNER_ATTENUATION: self.tunerAtten, } )
            if updateAll or updateFilter:
                confDict.update( { crd.configKeys.TUNER_FILTER: self.tunerFilter, } )
            conf = { crd.configKeys.CONFIG_TUNER: { 
                            self.tunerIndex: confDict,
                            }
                        }
            printJson(conf)
            self.radio.setConfiguration(conf)
        self.configuring = False
    
    def updateCal(self,):
        self.configuring = True#False
        if (self.radio is not None) and (not self.init) and (self.calFrequency is not None):
            conf = { crd.configKeys.CALIB_FREQUENCY: self.calFrequency }
            printJson(conf)
            self.radio.setConfiguration(conf)
        self.configuring = False
    
    ## Specific to 10GbE radios
    def setDipEntry(self,index,port):
        self.configuring = True#False
        print "setDipEntry(%d, %d)"%(index,port)
        if self.destIp is not None:
            conf = {crd.configKeys.CONFIG_IP:{
                        self.dataPort: {crd.configKeys.IP_DEST: { index: {cfgKeys.GIGE_SOURCE_PORT:port,
                                                                        cfgKeys.GIGE_DEST_PORT:port,
                                                                        cfgKeys.GIGE_MAC_ADDR:self.destMac,
                                                                        cfgKeys.GIGE_IP_ADDR:self.destIp,
                                                                        },
                                                                }
                                        }
                            }
                        }
            printJson(conf)
            self.radio.setConfiguration(conf)
        self.configuring = False

##############################  special  ##############################
    def set_radio_cmd(self, radio_cmd):
        print((" set_radio_cmd ").center(80,'~'))
        if not self.configuring:
            if radio_cmd is not None:
                print("radio_cmd: %r -> %r"%(self.radio_cmd, radio_cmd))
                self.radio_cmd = radio_cmd.strip()
                if (not self.init) and self.radio_cmd:
                    self.radio_rsp = self.radio.sendCommand("%s\n"%self.radio_cmd)
                return self.radio_rsp
    
    def send_radio_rsp(self, trigger=False):
        print((" send_radio_rsp ").center(80,'~'))
        if trigger and not self.configuring:
            print("trigger = %r, self.radio_rsp = %r"%(trigger,self.radio_rsp))
            if self.radio_rsp:
                for cmd in (self.radio_rsp[0],self.radio_cmd):
                    self.radio_rsp = self.radio.sendCommand("%s\n"%cmd)
    
    def get_radio_rsp(self,):
        return "; ".join( self.radio_rsp )

    def query_rssi(self,*args,**kwargs):
        if self.configuring:
            return "CONFIGURING"
        else:
            try:
                if self.nbddcIndex>0:
                    rsp = self.radio.sendCommand("RSSI? %d\n"%self.nbddcIndex)
                    print "RSSI Rsp = %r"%rsp
                    return rsp[0] if rsp is not None else "error"
                else:
                    return "n/a"
            except:
                traceback.print_exc()
                return "RSSI QUERY ERROR"
        
