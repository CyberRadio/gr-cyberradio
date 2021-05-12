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
import CyberRadio
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


class NDR_demo_control(gr.hier_block2):
    """
    docstring for block CyberRadio/NDR_demo_control
    """
    radio_cmd = None
    radio_rsp = ""
    
    radio_type = None
    radio_hostname = None
    radio_port = None
    tuner1_index = None
    tuner1_freq = None
    tuner1_atten = None
    tuner2_index = None
    tuner2_freq = None
    tuner2_atten = None
    ddc1_index = None
    ddc1_wideband = None
    ddc1_enable = None
    ddc1_vita49_level = None
    ddc1_rate_index = None
    ddc1_freq = None
    ddc1_udp_port = None
    ddc1_rf_source = None
    ddc2_index = None
    ddc2_wideband = None
    ddc2_enable = None
    ddc2_vita49_level = None
    ddc2_rate_index = None
    ddc2_freq = None
    ddc2_udp_port = None
    ddc2_rf_source = None
    cal_freq = None
    interface_dict = None
    verbose = None
    other_args = None
    
    ten_gbe_radio = False
    ddc1_data_port = 1
    ddc1_dip_index = 0
    ddc2_data_port = 1
    ddc2_dip_index = ddc1_dip_index+1
    
    def __init__(self, 
                    radio_type="ndr304", 
                    radio_hostname="/dev/ndr47x", 
                    radio_port=921600, 
                    tuner1_index=-1, 
                    tuner1_freq=1e9, 
                    tuner1_atten=0, 
                    tuner2_index=-1, 
                    tuner2_freq=1e9, 
                    tuner2_atten=0, 
                    ddc1_index=-1, 
                    ddc1_wideband=True, 
                    ddc1_enable=True, 
                    ddc1_vita49_level=3, 
                    ddc1_rate_index=0, 
                    ddc1_freq=0.0, 
                    ddc1_udp_port=40001, 
                    ddc1_rf_source=-1, 
                    ddc1_data_port=1, 
                    ddc2_index=-1, 
                    ddc2_wideband=True, 
                    ddc2_enable=True, 
                    ddc2_vita49_level=3, 
                    ddc2_rate_index=0, 
                    ddc2_freq=0.0, 
                    ddc2_udp_port=40002, 
                    ddc2_rf_source=-1, 
                    ddc2_data_port=1, 
                    cal_freq=0.0, 
                    interface_dict={1: 'eth0'}, 
                    verbose=True, 
                    other_args={}, 
                     ):
        gr.hier_block2.__init__(self, "CyberRadio/NDR_demo_control",
                                gr.io_signature(0, 0, 0),
                                gr.io_signature(1, 1, gr.sizeof_char*1),
                                 )
        self.fileLikeObjectSource = CyberRadio.file_like_object_source()
        self.connect((self.fileLikeObjectSource, 0), (self, 0))
        
        self.init = True
        self.set_radio_type( radio_type )
        self.set_radio_hostname( radio_hostname )
        self.set_radio_port( radio_port )
        self.set_tuner1_index( tuner1_index )
        self.set_tuner1_freq( tuner1_freq )
        self.set_tuner1_atten( tuner1_atten )
        self.set_tuner2_index( tuner2_index )
        self.set_tuner2_freq( tuner2_freq )
        self.set_tuner2_atten( tuner2_atten )
        self.set_ddc1_index( ddc1_index )
        self.set_ddc1_wideband( ddc1_wideband )
        self.set_ddc1_enable( ddc1_enable )
        self.set_ddc1_vita49_level( ddc1_vita49_level )
        self.set_ddc1_rate_index( ddc1_rate_index )
        self.set_ddc1_freq( ddc1_freq )
        self.set_ddc1_udp_port( ddc1_udp_port )
        self.set_ddc1_rf_source( ddc1_rf_source )
        self.set_ddc1_data_port( ddc1_data_port )
        self.set_ddc2_index( ddc2_index )
        self.set_ddc2_wideband( ddc2_wideband )
        self.set_ddc2_enable( ddc2_enable )
        self.set_ddc2_vita49_level( ddc2_vita49_level )
        self.set_ddc2_rate_index( ddc2_rate_index )
        self.set_ddc2_freq( ddc2_freq )
        self.set_ddc2_udp_port( ddc2_udp_port )
        self.set_ddc2_rf_source( ddc2_rf_source )
        self.set_ddc2_data_port( ddc2_data_port )
        self.set_cal_freq( cal_freq )
        self.set_interface_dict( interface_dict )
        self.set_verbose( verbose )
        self.set_other_args( other_args )
        
        self.init = False
        self.update_radio()
        self.update_tuner1()
        self.update_tuner2()
        self.update_ddc1()
        self.update_ddc2()
        self.update_cal()
        self.update_interface()
        self.update_verbose()
        self.update_other()



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
    
    def _disable_all_ddcs(self,):
        conf = { crd.configKeys.CONFIG_DDC: 
                    { crd.configKeys.CONFIG_WBDDC: 
                        { crd.configKeys.ALL: 
                            { crd.configKeys.ENABLE: False,
#                             crd.configKeys.DDC_RATE_INDEX: 0, 
#                             crd.configKeys.DDC_FREQUENCY_OFFSET: 0, 
#                             crd.configKeys.DDC_VITA_ENABLE: 0, 
#                             crd.configKeys.DDC_UDP_DESTINATION: 0, 
                            crd.configKeys.DDC_STREAM_ID: 0xDEAD, 
                             },
                         }, 
                    crd.configKeys.CONFIG_NBDDC: 
                        { crd.configKeys.ALL: 
                            { crd.configKeys.ENABLE: False,
#                             crd.configKeys.DDC_RATE_INDEX: 0, 
#                             crd.configKeys.DDC_FREQUENCY_OFFSET: 0, 
#                             crd.configKeys.DDC_VITA_ENABLE: 0, 
#                             crd.configKeys.DDC_UDP_DESTINATION: 0, 
                            crd.configKeys.DDC_STREAM_ID: 0xDEAD, 
                             },
                         },
                    }, 
                }
        self._set_configuration(conf)
    
    def _set_ddc_configuration(self, index, wideband, enable=False, rateIndex=0, freq=0.0, vitaLevel=0, rfSource=1, udpPort=0, dipIndex=0, dataPort=1):
        print(((" _set_ddc_configuration ").center(80,'~')))
        if self.radio_type in ["ndr354", "ndr364"]:
            conf = { crd.configKeys.CONFIG_DDC: 
                        { crd.configKeys.CONFIG_WBDDC if wideband else crd.configKeys.CONFIG_NBDDC: 
                            { index: 
                                { 
                                crd.configKeys.ENABLE: enable, 
                                crd.configKeys.DDC_RATE_INDEX: rateIndex, 
                                crd.configKeys.DDC_FREQUENCY_OFFSET: freq, 
                                crd.configKeys.DDC_VITA_ENABLE: vitaLevel, 
                                crd.configKeys.DDC_UDP_DESTINATION: dipIndex if self.ten_gbe_radio else udpPort, 
                                crd.configKeys.DDC_DATA_PORT: dataPort if self.ten_gbe_radio else None, 
                                crd.configKeys.DDC_STREAM_ID: index|(0x8000 if wideband else 0x0000), 
                                 }, 
                            }
                         }, 
                     }
        else:
            conf = { crd.configKeys.CONFIG_DDC: 
                        { crd.configKeys.CONFIG_WBDDC if wideband else crd.configKeys.CONFIG_NBDDC: 
                            { index: 
                                { 
                                crd.configKeys.ENABLE: enable, 
                                crd.configKeys.DDC_RATE_INDEX: rateIndex, 
                                crd.configKeys.DDC_FREQUENCY_OFFSET: freq, 
                                crd.configKeys.DDC_VITA_ENABLE: vitaLevel, 
                                crd.configKeys.DDC_UDP_DESTINATION: dipIndex if self.ten_gbe_radio else udpPort, 
                                crd.configKeys.DDC_DATA_PORT: dataPort if self.ten_gbe_radio else None, 
                                crd.configKeys.DDC_STREAM_ID: index|(0x8000 if wideband else 0x0000), 
                                crd.configKeys.DDC_RF_INDEX: None if wideband else rfSource, 
                                 }, 
                            }
                         }, 
                     }
        self._set_configuration(conf)
    
    def _set_interface_configuration(self,):
        print(((" _set_interface_configuration ").center(80,'~')))
        if self.radio_type.strip().lower() in ("ndr304","ndr470","ndr472",):
            for ind,iface in self.interface_dict.items():
                print(ind,iface)
                dmac,dip,mask = GetInterfaceAddress(iface)
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
                break
        else:
            for data_port,dip_index,udp_port in ((self.ddc1_data_port, self.ddc1_dip_index, self.ddc1_udp_port), 
                                                    (self.ddc2_data_port, self.ddc2_dip_index, self.ddc2_udp_port), 
                                                     ):
                if data_port in self.interface_dict:
                    iface = self.interface_dict.get(data_port)
                    dmac,dip,mask = GetInterfaceAddress(iface)
                    temp = [int(i) for i in dip.split(".")]
                    temp[-1]+=10
                    sip = ".".join( str(i) for i in temp )
                    if self.radio_type in ["ndr354", "ndr364"]:
                        conf = { crd.configKeys.CONFIG_IP: 
                                    { data_port: 
                                        { crd.configKeys.IP_SOURCE: 
                                            {
                                                crd.configKeys.GIGE_SOURCE_PORT: udp_port^0xffff,
                                                crd.configKeys.GIGE_IP_ADDR: sip,
                                                crd.configKeys.GIGE_NETMASK: "255.255.255.0",
                                            }, 
                                        crd.configKeys.IP_DEST: 
                                            { dip_index: 
                                                { 
                                                crd.configKeys.GIGE_DEST_PORT: udp_port,
                                                crd.configKeys.GIGE_MAC_ADDR: dmac, 
                                                crd.configKeys.GIGE_IP_ADDR: dip,
                                                 },
                                            }, 
                                        }, 
                                    }, 
                                }
                    else:
                        conf = { crd.configKeys.CONFIG_IP: 
                                    { data_port: 
                                        { crd.configKeys.IP_SOURCE: sip, 
                                        crd.configKeys.IP_DEST: 
                                            { dip_index: 
                                                { crd.configKeys.GIGE_SOURCE_PORT: udp_port^0xffff,
                                                crd.configKeys.GIGE_DEST_PORT: udp_port,
                                                crd.configKeys.GIGE_MAC_ADDR: dmac, 
                                                crd.configKeys.GIGE_IP_ADDR: dip,
                                                 },
                                            }, 
                                        }, 
                                    }, 
                                }
                    self._set_configuration(conf)

##############################  radio Parameters  ##############################
    def update_radio(self, disable=False,):
        print(((" update_radio(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            self.ten_gbe_radio = not any(i in self.radio_type for i in ("304","470","472"))
            self.radio = crd.getRadioObject(self.radio_type, verbose=self.verbose, logFile=self.fileLikeObjectSource)
            self.radio.connect(self.radio.getConnectionModeList()[0],self.radio_hostname,self.radio_port)
            self._disable_all_ddcs()

    def set_radio_type(self, radio_type):
        print(((" set_radio_type ").center(80,'~')))
        if self.radio_type != radio_type:
            print(("radio_type: %r -> %r"%(self.radio_type, radio_type)))
            self.radio_type = radio_type
            self.update_radio()

    def set_radio_hostname(self, radio_hostname):
        print(((" set_radio_hostname ").center(80,'~')))
        if self.radio_hostname != radio_hostname:
            print(("radio_hostname: %r -> %r"%(self.radio_hostname, radio_hostname)))
            self.radio_hostname = radio_hostname
            self.update_radio()

    def set_radio_port(self, radio_port):
        print(((" set_radio_port ").center(80,'~')))
        if self.radio_port != radio_port:
            print(("radio_port: %r -> %r"%(self.radio_port, radio_port)))
            self.radio_port = radio_port
            self.update_radio()

############################## tuner1 Parameters  ##############################
    def update_tuner1(self, disable=False,):
        print(((" update_tuner1(disable=%s) "%(disable)).center(80,'~')))
        if not self.init and self.tuner1_index>=0:
            self._set_tuner_configuration(self.tuner1_index, self.tuner1_freq, self.tuner1_atten)

    def set_tuner1_index(self, tuner1_index):
        print(((" set_tuner1_index ").center(80,'~')))
        if self.tuner1_index != tuner1_index:
            print(("tuner1_index: %r -> %r"%(self.tuner1_index, tuner1_index)))
            self.tuner1_index = tuner1_index
            self.update_tuner1()

    def set_tuner1_freq(self, tuner1_freq):
        print(((" set_tuner1_freq ").center(80,'~')))
        if self.tuner1_freq != tuner1_freq:
            print(("tuner1_freq: %r -> %r"%(self.tuner1_freq, tuner1_freq)))
            self.tuner1_freq = tuner1_freq
            self.update_tuner1()

    def set_tuner1_atten(self, tuner1_atten):
        print(((" set_tuner1_atten ").center(80,'~')))
        if self.tuner1_atten != tuner1_atten:
            print(("tuner1_atten: %r -> %r"%(self.tuner1_atten, tuner1_atten)))
            self.tuner1_atten = tuner1_atten
            self.update_tuner1()

############################## tuner2 Parameters  ##############################
    def update_tuner2(self, disable=False,):
        print(((" update_tuner2(disable=%s) "%(disable)).center(80,'~')))
        if not self.init and self.tuner2_index>=0:
            self._set_tuner_configuration(self.tuner2_index, self.tuner2_freq, self.tuner2_atten)

    def set_tuner2_index(self, tuner2_index):
        print(((" set_tuner2_index ").center(80,'~')))
        if self.tuner2_index != tuner2_index:
            print(("tuner2_index: %r -> %r"%(self.tuner2_index, tuner2_index)))
            self.tuner2_index = tuner2_index
            self.update_tuner2()

    def set_tuner2_freq(self, tuner2_freq):
        print(((" set_tuner2_freq ").center(80,'~')))
        if self.tuner2_freq != tuner2_freq:
            print(("tuner2_freq: %r -> %r"%(self.tuner2_freq, tuner2_freq)))
            self.tuner2_freq = tuner2_freq
            self.update_tuner2()

    def set_tuner2_atten(self, tuner2_atten):
        print(((" set_tuner2_atten ").center(80,'~')))
        if self.tuner2_atten != tuner2_atten:
            print(("tuner2_atten: %r -> %r"%(self.tuner2_atten, tuner2_atten)))
            self.tuner2_atten = tuner2_atten
            self.update_tuner2()

##############################  ddc1 Parameters   ##############################
    def update_ddc1(self, disable=False,):
        print(((" update_ddc1(disable=%s) "%(disable)).center(80,'~')))
        if not self.init and self.ddc1_index>=0:
            #~ _set_ddc_configuration(self, index, wideband, enable=False, rateIndex=0, freq=0.0, vitaLevel=0, rfSource=1, udpPort=0, dipIndex=0, dataPort=1)
            self._set_ddc_configuration(self.ddc1_index, 
                                        self.ddc1_wideband, 
                                        self.ddc1_enable and not disable, 
                                        self.ddc1_rate_index, 
                                        self.ddc1_freq, 
                                        self.ddc1_vita49_level, 
                                        self.ddc1_rf_source, 
                                        self.ddc1_udp_port,
                                        self.ddc1_dip_index, 
                                        self.ddc1_data_port,
                                         )

    def set_ddc1_index(self, ddc1_index):
        print(((" set_ddc1_index ").center(80,'~')))
        if self.ddc1_index != ddc1_index:
            print(("ddc1_index: %r -> %r"%(self.ddc1_index, ddc1_index)))
            self.update_ddc1(True)
            self.ddc1_index = ddc1_index
            self.update_ddc1()

    def set_ddc1_wideband(self, ddc1_wideband):
        print(((" set_ddc1_wideband ").center(80,'~')))
        if self.ddc1_wideband != ddc1_wideband:
            print(("ddc1_wideband: %r -> %r"%(self.ddc1_wideband, ddc1_wideband)))
            self.ddc1_wideband = ddc1_wideband
            self.update_ddc1()

    def set_ddc1_enable(self, ddc1_enable):
        print(((" set_ddc1_enable ").center(80,'~')))
        if self.ddc1_enable != ddc1_enable:
            print(("ddc1_enable: %r -> %r"%(self.ddc1_enable, ddc1_enable)))
            self.ddc1_enable = ddc1_enable
            self.update_ddc1()

    def set_ddc1_vita49_level(self, ddc1_vita49_level):
        print(((" set_ddc1_vita49_level ").center(80,'~')))
        if self.ddc1_vita49_level != ddc1_vita49_level:
            print(("ddc1_vita49_level: %r -> %r"%(self.ddc1_vita49_level, ddc1_vita49_level)))
            self.ddc1_vita49_level = ddc1_vita49_level
            self.update_ddc1()

    def set_ddc1_rate_index(self, ddc1_rate_index):
        print(((" set_ddc1_rate_index ").center(80,'~')))
        if self.ddc1_rate_index != ddc1_rate_index:
            print(("ddc1_rate_index: %r -> %r"%(self.ddc1_rate_index, ddc1_rate_index)))
            self.ddc1_rate_index = ddc1_rate_index
            self.update_ddc1()

    def set_ddc1_freq(self, ddc1_freq):
        print(((" set_ddc1_freq ").center(80,'~')))
        if self.ddc1_freq != ddc1_freq:
            print(("ddc1_freq: %r -> %r"%(self.ddc1_freq, ddc1_freq)))
            self.ddc1_freq = ddc1_freq
            self.update_ddc1()

    def set_ddc1_udp_port(self, ddc1_udp_port):
        print(((" set_ddc1_udp_port ").center(80,'~')))
        if self.ddc1_udp_port != ddc1_udp_port:
            print(("ddc1_udp_port: %r -> %r"%(self.ddc1_udp_port, ddc1_udp_port)))
            self.ddc1_udp_port = ddc1_udp_port
            self.update_ddc1()

    def set_ddc1_rf_source(self, ddc1_rf_source):
        print(((" set_ddc1_rf_source ").center(80,'~')))
        if self.ddc1_rf_source != ddc1_rf_source:
            print(("ddc1_rf_source: %r -> %r"%(self.ddc1_rf_source, ddc1_rf_source)))
            self.ddc1_rf_source = ddc1_rf_source
            self.update_ddc1()

    def set_ddc1_data_port(self, ddc1_data_port):
        print(((" set_ddc1_data_port ").center(80,'~')))
        if self.ddc1_data_port != ddc1_data_port:
            print(("ddc1_data_port: %r -> %r"%(self.ddc1_data_port, ddc1_data_port)))
            self.ddc1_data_port = ddc1_data_port
            self.update_ddc1()

##############################  ddc2 Parameters   ##############################
    def update_ddc2(self, disable=False,):
        print(((" update_ddc2(disable=%s) "%(disable)).center(80,'~')))
        if not self.init and self.ddc2_index>=0:
            #~ _set_ddc_configuration(self, index, wideband, enable=False, rateIndex=0, freq=0.0, vitaLevel=0, udpPort=0):
            self._set_ddc_configuration(self.ddc2_index, 
                                        self.ddc2_wideband, 
                                        self.ddc2_enable and not disable, 
                                        self.ddc2_rate_index, 
                                        self.ddc2_freq, 
                                        self.ddc2_vita49_level, 
                                        self.ddc2_rf_source, 
                                        self.ddc2_udp_port, 
                                        self.ddc2_dip_index, 
                                        self.ddc2_data_port,
                                         )

    def set_ddc2_index(self, ddc2_index):
        print(((" set_ddc2_index ").center(80,'~')))
        if self.ddc2_index != ddc2_index:
            print(("ddc2_index: %r -> %r"%(self.ddc2_index, ddc2_index)))
            self.update_ddc2(True)
            self.ddc2_index = ddc2_index
            self.update_ddc2()

    def set_ddc2_wideband(self, ddc2_wideband):
        print(((" set_ddc2_wideband ").center(80,'~')))
        if self.ddc2_wideband != ddc2_wideband:
            print(("ddc2_wideband: %r -> %r"%(self.ddc2_wideband, ddc2_wideband)))
            self.ddc2_wideband = ddc2_wideband
            self.update_ddc2()

    def set_ddc2_enable(self, ddc2_enable):
        print(((" set_ddc2_enable ").center(80,'~')))
        if self.ddc2_enable != ddc2_enable:
            print(("ddc2_enable: %r -> %r"%(self.ddc2_enable, ddc2_enable)))
            self.ddc2_enable = ddc2_enable
            self.update_ddc2()

    def set_ddc2_vita49_level(self, ddc2_vita49_level):
        print(((" set_ddc2_vita49_level ").center(80,'~')))
        if self.ddc2_vita49_level != ddc2_vita49_level:
            print(("ddc2_vita49_level: %r -> %r"%(self.ddc2_vita49_level, ddc2_vita49_level)))
            self.ddc2_vita49_level = ddc2_vita49_level
            self.update_ddc2()

    def set_ddc2_rate_index(self, ddc2_rate_index):
        print(((" set_ddc2_rate_index ").center(80,'~')))
        if self.ddc2_rate_index != ddc2_rate_index:
            print(("ddc2_rate_index: %r -> %r"%(self.ddc2_rate_index, ddc2_rate_index)))
            self.ddc2_rate_index = ddc2_rate_index
            self.update_ddc2()

    def set_ddc2_freq(self, ddc2_freq):
        print(((" set_ddc2_freq ").center(80,'~')))
        if self.ddc2_freq != ddc2_freq:
            print(("ddc2_freq: %r -> %r"%(self.ddc2_freq, ddc2_freq)))
            self.ddc2_freq = ddc2_freq
            self.update_ddc2()

    def set_ddc2_udp_port(self, ddc2_udp_port):
        print(((" set_ddc2_udp_port ").center(80,'~')))
        if self.ddc2_udp_port != ddc2_udp_port:
            print(("ddc2_udp_port: %r -> %r"%(self.ddc2_udp_port, ddc2_udp_port)))
            self.ddc2_udp_port = ddc2_udp_port
            self.update_ddc2()

    def set_ddc2_rf_source(self, ddc2_rf_source):
        print(((" set_ddc2_rf_source ").center(80,'~')))
        if self.ddc2_rf_source != ddc2_rf_source:
            print(("ddc2_rf_source: %r -> %r"%(self.ddc2_rf_source, ddc2_rf_source)))
            self.ddc2_rf_source = ddc2_rf_source
            self.update_ddc2()

    def set_ddc2_data_port(self, ddc2_data_port):
        print(((" set_ddc2_data_port ").center(80,'~')))
        if self.ddc2_data_port != ddc2_data_port:
            print(("ddc2_data_port: %r -> %r"%(self.ddc2_data_port, ddc2_data_port)))
            self.ddc2_data_port = ddc2_data_port
            self.update_ddc2()

##############################   cal Parameters   ##############################
    def update_cal(self, disable=False,):
        print(((" update_cal(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            pass

    def set_cal_freq(self, cal_freq):
        print(((" set_cal_freq ").center(80,'~')))
        if self.cal_freq != cal_freq:
            print(("cal_freq: %r -> %r"%(self.cal_freq, cal_freq)))
            self.cal_freq = cal_freq
            self.update_cal()

##############################interface Parameters##############################
    def update_interface(self, disable=False,):
        print(((" update_interface(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            self._set_interface_configuration()

    def set_interface_dict(self, interface_dict):
        print(((" set_interface_dict ").center(80,'~')))
        if self.interface_dict != interface_dict:
            print(("interface_dict: %r -> %r"%(self.interface_dict, interface_dict)))
            self.interface_dict = interface_dict
            self.update_interface()

############################## verbose Parameters ##############################
    def update_verbose(self, disable=False,):
        print(((" update_verbose(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            pass

    def set_verbose(self, verbose):
        print(((" set_verbose ").center(80,'~')))
        if self.verbose != verbose:
            print(("verbose: %r -> %r"%(self.verbose, verbose)))
            self.verbose = verbose
            self.update_verbose()

##############################  other Parameters  ##############################
    def update_other(self, disable=False,):
        print(((" update_other(disable=%s) "%(disable)).center(80,'~')))
        if not self.init:
            pass

    def set_other_args(self, other_args):
        print(((" set_other_args ").center(80,'~')))
        if self.other_args != other_args:
            print(("other_args: %r -> %r"%(self.other_args, other_args)))
            self.other_args = other_args
            self.update_other()

##############################  special  ##############################
    def set_radio_cmd(self, radio_cmd):
        print(((" set_radio_cmd ").center(80,'~')))
        if radio_cmd is not None:
            print(("ddc2_rate_index: %r -> %r"%(self.radio_cmd, radio_cmd)))
            self.radio_cmd = radio_cmd.strip()
            if not self.init:
                self.radio_rsp = "; ".join( self.radio.sendCommand("%s\n"%self.radio_cmd) )
            return self.radio_rsp
    
    def get_radio_rsp(self,):
        return self.radio_rsp
