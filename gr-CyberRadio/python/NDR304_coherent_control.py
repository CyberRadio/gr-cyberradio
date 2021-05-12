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

import numpy
from gnuradio import gr
import json
import CyberRadioDriver as crd
import netifaces

def GetInterfaceAddress(ifname):
    mac = ip = netmask = None
    ifList = netifaces.interfaces()
    if ifname in ifList:
        addrDict = netifaces.ifaddresses(ifname)
        mac = addrDict.get(netifaces.AF_LINK,[{},])[0].get("addr",None)
        ip = addrDict.get(netifaces.AF_INET,[{},])[0].get("addr",None)
        netmask = addrDict.get(netifaces.AF_INET,[{},])[0].get("netmask",None)
    return mac,ip,netmask

class NDR304_coherent_control(gr.basic_block):
    radio = None
    
    radio_device = None
    radio_baudrate = None
    radio_verbose = None
    radio_interface = None
    tuner_freq = None
    tuner_atten_dict = None
    tuner_coherent = None
    ddc_enable = None
    ddc_vita49_level = None
    ddc_freq = None
    ddc_udp_port = None
    ddc_coherent = None
    ddc_group = None

    """
    docstring for block ndr304_coherent_control
    """
    def __init__(self, radio_device="/dev/ndr47x", radio_baudrate=921600, radio_verbose=True, radio_interface="eth2", tuner_freq=[1e9,1e9,1e9,1e9,1e9,1e9,], tuner_atten_dict=[0, 0, 0, 0, 0, 0], tuner_coherent=False, ddc_enable=[1, 1, 1, 1, 1, 1], ddc_vita49_level=3, ddc_freq=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ddc_udp_port=[40000, 40001, 40002, 40003, 40004, 40005], ddc_coherent=False, ddc_group=True):
        gr.basic_block.__init__(self,
            name="ndr304_coherent_control",
            in_sig=None,
            out_sig=None,
            )
        
        self.init = True
        self.set_radio_device( radio_device )
        self.set_radio_baudrate( radio_baudrate )
        self.set_radio_verbose( radio_verbose )
        self.set_radio_interface( radio_interface )
        self.set_tuner_freq( tuner_freq )
        self.set_tuner_atten_dict( tuner_atten_dict )
        self.set_tuner_coherent( tuner_coherent )
        self.set_ddc_enable( ddc_enable )
        self.set_ddc_vita49_level( ddc_vita49_level )
        self.set_ddc_freq( ddc_freq )
        self.set_ddc_udp_port( ddc_udp_port )
        self.set_ddc_coherent( ddc_coherent )
        self.set_ddc_group( ddc_group )
        
        self.init = False
        self.update_radio()
        self._set_coh_mode()
        self.update_tuner()
        self.update_ddc()


    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        output_items[0][:] = input_items[0]
        consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
    
    def _set_configuration(self, confDict, printJson=True):
        print(((" _set_configuration ").center(80,'~')))
        if printJson:
            print(( json.dumps(confDict, sort_keys=True, indent=4) ))
        self.radio.setConfiguration(confDict)
    
    def _set_radio_configuration(self,):
        print(((" _set_radio_configuration ").center(80,'~')))
        self.radio = crd.ndr304(verbose=self.radio_verbose)
        self.radio.connect("tty",self.radio_device,self.radio_baudrate)
        
        dmac,dip,mask = GetInterfaceAddress(self.radio_interface)
        temp = [int(i) for i in dip.split(".")]
        temp[-1]+=10
        sip = ".".join( str(i) for i in temp )
        conf = { crd.configKeys.CONFIG_IP:
                    { crd.configKeys.IP_SOURCE: sip, 
                    crd.configKeys.IP_DEST: dip, 
                    crd.configKeys.MAC_DEST: dmac, 
                     },
                 }
        self._set_configuration(conf)
    
    def _set_tuner_configuration(self, index, freq, atten):
        print(((" _set_tuner_configuration ").center(80,'~')))
        conf = { crd.configKeys.CONFIG_TUNER: 
                    { index: 
                        { crd.configKeys.TUNER_FREQUENCY:freq, 
                        crd.configKeys.TUNER_ATTENUATION:atten, 
                         }, 
                     }, 
                 }
        self._set_configuration(conf)
    
    def _set_coh_mode(self,):
        if (self.radio is not None) and not self.init:
            mode = 0
            if self.tuner_coherent:
                mode |= 0x1
            if self.ddc_coherent:
                mode |= 0x2
            self.radio.sendCommand("COH %d\n"%mode)
    
    def _set_ddc_configuration(self, index, enable=False, rateIndex=0, freq=0.0, vitaLevel=0, udpPort=0):
        print(((" _set_ddc_configuration ").center(80,'~')))
        conf = { crd.configKeys.CONFIG_DDC: 
                    { crd.configKeys.CONFIG_WBDDC: 
                        { index: 
                            { 
                            crd.configKeys.ENABLE: enable, 
                            crd.configKeys.DDC_RATE_INDEX: rateIndex, 
                            crd.configKeys.DDC_FREQUENCY_OFFSET: freq, 
                            crd.configKeys.DDC_VITA_ENABLE: vitaLevel, 
                            crd.configKeys.DDC_UDP_DESTINATION: udpPort, 
                            crd.configKeys.DDC_STREAM_ID: index, 
                             }, 
                        }
                     }, 
                 }
        self._set_configuration(conf)
    
    def _disable_all_ddcs(self,):
        conf = { crd.configKeys.CONFIG_DDC: 
                    { crd.configKeys.CONFIG_WBDDC: 
                        { crd.configKeys.ALL: 
                            { crd.configKeys.ENABLE: False,
                            crd.configKeys.DDC_RATE_INDEX: 0, 
                            crd.configKeys.DDC_FREQUENCY_OFFSET: 0, 
                            crd.configKeys.DDC_VITA_ENABLE: 0, 
                            crd.configKeys.DDC_UDP_DESTINATION: 0, 
                            crd.configKeys.DDC_STREAM_ID: 0, 
                             },
                         }, 
                    crd.configKeys.CONFIG_NBDDC: 
                        { crd.configKeys.ALL: 
                            { crd.configKeys.ENABLE: False,
                            crd.configKeys.DDC_RATE_INDEX: 0, 
                            crd.configKeys.DDC_FREQUENCY_OFFSET: 0, 
                            crd.configKeys.DDC_VITA_ENABLE: 0, 
                            crd.configKeys.DDC_UDP_DESTINATION: 0, 
                            crd.configKeys.DDC_STREAM_ID: 0, 
                             },
                         },
                    }, 
                }
        self._set_configuration(conf)


##############################  radio Parameters  ##############################
    def update_radio(self, disable=False,):
        print(((" update_radio(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            self._set_radio_configuration()

    def set_radio_device(self, radio_device):
        print(((" set_radio_device ").center(80,'~')))
        if self.radio_device != radio_device:
            print(("radio_device: %r -> %r"%(self.radio_device, radio_device)))
            self.radio_device = radio_device
            self.update_radio()

    def set_radio_baudrate(self, radio_baudrate):
        print(((" set_radio_baudrate ").center(80,'~')))
        if self.radio_baudrate != radio_baudrate:
            print(("radio_baudrate: %r -> %r"%(self.radio_baudrate, radio_baudrate)))
            self.radio_baudrate = radio_baudrate
            self.update_radio()

    def set_radio_verbose(self, radio_verbose):
        print(((" set_radio_verbose ").center(80,'~')))
        if self.radio_verbose != radio_verbose:
            print(("radio_verbose: %r -> %r"%(self.radio_verbose, radio_verbose)))
            self.radio_verbose = radio_verbose
            self.update_radio()

    def set_radio_interface(self, radio_interface):
        print(((" set_radio_interface ").center(80,'~')))
        if self.radio_interface != radio_interface:
            print(("radio_interface: %r -> %r"%(self.radio_interface, radio_interface)))
            self.radio_interface = radio_interface
            self.update_radio()

##############################  tuner Parameters  ##############################
    def update_tuner(self, disable=False,):
        print(((" update_tuner(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            for i in range(6):
                tunerIndex = i+1
                print(tunerIndex,i,self.tuner_freq,self.tuner_coherent,(len(self.tuner_freq)<tunerIndex),(self.tuner_coherent or (len(self.tuner_freq)<tunerIndex)))
                freq = self.tuner_freq[0] if (self.tuner_coherent or (len(self.tuner_freq)<tunerIndex)) else self.tuner_freq[i]
                att = self.tuner_atten_dict[i] if len(self.tuner_atten_dict)>=tunerIndex else self.tuner_atten_dict[0]
                self._set_tuner_configuration(tunerIndex, freq, att)
                

    def set_tuner_freq(self, tuner_freq):
        print(((" set_tuner_freq ").center(80,'~')))
        if self.tuner_freq != tuner_freq:
            print(("tuner_freq: %r -> %r"%(self.tuner_freq, tuner_freq)))
            self.tuner_freq = tuner_freq
            self.update_tuner()

    def set_tuner_atten_dict(self, tuner_atten_dict):
        print(((" set_tuner_atten_dict ").center(80,'~')))
        if self.tuner_atten_dict != tuner_atten_dict:
            print(("tuner_atten_dict: %r -> %r"%(self.tuner_atten_dict, tuner_atten_dict)))
            self.tuner_atten_dict = tuner_atten_dict
            self.update_tuner()

    def set_tuner_coherent(self, tuner_coherent):
        print(((" set_tuner_coherent ").center(80,'~')))
        if self.tuner_coherent != tuner_coherent:
            print(("tuner_coherent: %r -> %r"%(self.tuner_coherent, tuner_coherent)))
            self.tuner_coherent = tuner_coherent
            self._set_coh_mode()
            self.update_tuner()

##############################   ddc Parameters   ##############################
    def update_ddc(self, disable=False, index=None):
        print(((" update_ddc(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            self.radio.sendCommand("WBGE 1, 0\n")
            for i in range(6):
                ddcIndex = i+1
                self.radio.sendCommand("WBG 1, %d, %d\n"%(ddcIndex,int(self.ddc_group and self.ddc_enable[i])))
                self._set_ddc_configuration(ddcIndex, 
                                            self.ddc_enable[i] and (not self.ddc_group), 
                                            0, 
                                            self.ddc_freq[i], 
                                            self.ddc_vita49_level, 
                                            self.ddc_udp_port[i] if not self.ddc_coherent else self.ddc_udp_port[0],
                                             )
            if self.ddc_group:
                self.radio.sendCommand("WBGE 1, 1\n")

    def set_ddc_enable(self, ddc_enable):
        print(((" set_ddc_enable ").center(80,'~')))
        if self.ddc_enable != ddc_enable:
            print(("ddc_enable: %r -> %r"%(self.ddc_enable, ddc_enable)))
            self.ddc_enable = ddc_enable
            self.update_ddc()

    def set_ddc_vita49_level(self, ddc_vita49_level):
        print(((" set_ddc_vita49_level ").center(80,'~')))
        if self.ddc_vita49_level != ddc_vita49_level:
            print(("ddc_vita49_level: %r -> %r"%(self.ddc_vita49_level, ddc_vita49_level)))
            self.ddc_vita49_level = ddc_vita49_level
            self.update_ddc()

    def set_ddc_freq(self, ddc_freq):
        print(((" set_ddc_freq ").center(80,'~')))
        if self.ddc_freq != ddc_freq:
            print(("ddc_freq: %r -> %r"%(self.ddc_freq, ddc_freq)))
            self.ddc_freq = ddc_freq
            self.update_ddc()

    def set_ddc_udp_port(self, ddc_udp_port):
        print(((" set_ddc_udp_port ").center(80,'~')))
        if self.ddc_udp_port != ddc_udp_port:
            print(("ddc_udp_port: %r -> %r"%(self.ddc_udp_port, ddc_udp_port)))
            self.ddc_udp_port = ddc_udp_port
            self.update_ddc()

    def set_ddc_coherent(self, ddc_coherent):
        print(((" set_ddc_coherent ").center(80,'~')))
        if self.ddc_coherent != ddc_coherent:
            print(("ddc_coherent: %r -> %r"%(self.ddc_coherent, ddc_coherent)))
            self.ddc_coherent = ddc_coherent
            self.update_ddc()

    def set_ddc_group(self, ddc_group):
        print(((" set_ddc_group ").center(80,'~')))
        if self.ddc_group != ddc_group:
            print(("ddc_group: %r -> %r"%(self.ddc_group, ddc_group)))
            self.ddc_group = ddc_group
            self.update_ddc()

