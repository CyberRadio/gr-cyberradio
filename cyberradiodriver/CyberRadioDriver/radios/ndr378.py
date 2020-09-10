#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr378 
# \brief NDR378 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.  
#     All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver.radios.ndr551 import ndr551, \
                                           ndr551_tuner, \
                                           ndr551_wbddc, \
                                           ndr551_nbddc, \
                                           ndr551_ddc_group, \
                                           ndr551_ddc_ifSpec, \
                                           ndr551_adc_ifSpec, \
                                           ndr551_demod_ifSpec
from CyberRadioDriver.command import _jsonCommandBase, jsonConfig
from CyberRadioDriver import configKeys
# Imports from external modules
# Python standard library imports

##
# \brief Tuner component class for the NDR378.
#
class ndr378_tuner(ndr551_tuner):
    _name = "Tuner(NDR378)"
    frqRange = (20e6,6e9)

##
# \brief WBDDC component class for the NDR378.
class ndr378_wbddc(ndr551_wbddc):
    _name = "WBDDC(NDR378)"

##
# \brief NBDDC component class for the NDR378.
class ndr378_nbddc(ndr551_nbddc):
    _name = "NBDDC(NDR378)"

##
# \brief NBDDC component class for the NDR378.
class ndr378_ddc_group(ndr551_ddc_group):
    _name = "DDCGroup(NDR378)"

##
# \internal
# \brief VITA 49 interface specification class for the NDR378's DDC format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each DDC payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the DDC payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For DDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("ddc") / 4.
class ndr378_ddc_ifSpec(ndr551_ddc_ifSpec):
    pass


##
# \internal
# \brief VITA 49 interface specification class for NDR378's ADC format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each ADC payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the ADC payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For ADC format, each 32-bit word contains two 16-bit ADC samples,
#    so the number of samples is getVitaPayloadSize("adc") / 2.
class ndr378_adc_ifSpec(ndr551_adc_ifSpec):
    pass


##
# \internal
# \brief VITA 49 interface specification class for the NDR378's demod format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each demod payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the demod payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For demod format, each 32-bit word contains two 16-bit demod samples,
#    so the number of samples is getVitaPayloadSize("demod") / 2.
class ndr378_demod_ifSpec(ndr551_demod_ifSpec):
    pass


##
# \brief Radio handler class for the NDR378.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR378 Connection Modes
#
# "udp"
#
# \section RadioConfig_NDR378 Radio Configuration Options
#
# \code
# configDict = {
#      "referenceMode": [0, 1],
#      "function": [integer (meaning is radio-dependent],
#      "tunerConfiguration": {
#            0: {
#               "preselectorBypass": [True, False], 
#               "frequency": [20000000.0-6000000000.0, step 1000000.0],
#               "attenuation": [0.0-40.0, step 1.0],
#               "enable": [True, False],
#               "ifFilter": [3, 10, 40, 80],
#               "delay": [0.0-1.0, step 8e-6],
#               "fnr": [True, False],
#               "gainMode": ["auto", "manual", "freeze"],
#               "asp": [-40.0-0.0, step 1.0],
#               "aul": [-40.0-0.0, step 1.0],
#               "all": [-40.0-0.0, step 1.0],
#               "aat": [1.0-128.0, step 1.0],
#               "adt": [1.0-128.0, step 1.0],
#               "aas": [0.0-40.0, step 1.0],
#               "ads": [0.0-40.0, step 1.0],
#               "aal": [1.0-30.0, step 1.0],
#               "adl": [1.0-30.0, step 1.0],
#            },
#         ...7 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              0: {
#                 "enable": [True, False],
#                 "rfIndex": ["0", "1", "2", "3"],
#                 "outputType": ["iq", "raw"],
#                 "frequency": [-40e6-40e6, step 1e3],
#                 "decimation": [1, 2, 4, 8, 16],
#                 "filterIndex": [32-63, step 1],
#                 "oversampling": [1, 2, 4],
#                 "startTime": [start time],
#                 "samples": [samples],
#                 "udpDest": [UDP destination table index],
#                 "groupId": [0-15, step 1],
#                 "streamId": [stream ID],
#                 "link": [0, 1, 2, 3],
#                 "gainMode": ["auto", "manual", "freeze"],
#                 "dgv": [0.0-96.0, step 1.0],
#                 "dul": [0.0-96.0, step 1.0],
#                 "dll": [0.0-96.0, step 1.0],
#                 "dtl": [-96.0-0.0, step 0.5],
#                 "dal": [0.0-30.0, step 0.5],
#                 "ddl": [0.0-30.0, step 0.5],
#                 "dao": [0.0-24.0, step 0.5],
#                 "ddo": [0.0-24.0, step 0.5],
#                 "datc": [10-3000, step 10],
#                 "ddtc": [10-3000, step 10],
#                 "dat": [1-100, step 1],
#                 "ddt": [1-100, step 1],
#              },
#           ...7 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              0: {
#                 "enable": [True, False],
#                 "frequency": [-40e6-40e6, step 1e3],
#                 "rfIndex": ["0", "1", "2", "3"],
#                 "filterIndex": [0-31 step 1, 64-4095 step 1],
#                 "cic0": [4-500, step 1],
#                 "cic1": [1, 4-500, step 1],
#                 "oversampling": [1, 2, 4, 8, 16],
#                 "demod": ["none", "cw", "fm", "am", "usb", "lsb"],
#                 "demodGain": [gain],
#                 "audioDecimation": [True, False],
#                 "bfo": [-12e3-12e3, step 1],
#                 "startTime": [ISO 8601 time string],
#                 "samples": [number of samples],
#                 "udpDest": [UDP destination table index],
#                 "groupId": [0-15, step 1],
#                 "streamId": [stream ID],
#                 "gainMode": ["auto", "manual", "freeze"],
#                 "dgv": [0.0-96.0, step 1.0],
#                 "dul": [0.0-96.0, step 1.0],
#                 "dll": [0.0-96.0, step 1.0],
#                 "dtl": [-96.0-0.0, step 0.5],
#                 "dal": [0.0-30.0, step 0.5],
#                 "ddl": [0.0-30.0, step 0.5],
#                 "dao": [0.0-24.0, step 0.5],
#                 "ddo": [0.0-24.0, step 0.5],
#                 "datc": [10-3000, step 10],
#                 "ddtc": [10-3000, step 10],
#                 "dat": [1-100, step 1],
#                 "ddt": [1-100, step 1],
#              },
#           ...63 (repeat for each NBDDC)
#         },
#      },
#      "ipConfiguration": {
#            0: {
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "destPort": [port],
#                      "arp": [True, False],
#                   },
#                ...63 (repeat for each UDP destination index)
#               },
#               "sourceIP": {
#                   "ipAddr": [IP address],
#                   "macAddr": [MAC address],
#                   "netmask": [netmask],
#                   "sourcePort": [port],
#               },
#            },
#         ...3 (repeat for each 10-Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \section VITA_Notes_NDR378 VITA 49 Notes
#
# When dealing with VITA 49 payloads, we have historically relied on the 
# following convention:
# * getVitaHeaderSize() provides how many bytes contain metadata information 
#   at the beginning of the packet
# * getVitaPayloadSize() provides how many bytes contain data samples
# * getVitaTailSize() provides how many bytes contain metadata information 
#   at the end of the packet
#
# For NDR551-class radios, this convention requires us to deviate, not only
# from the VITA 49 standard, but also from the NDR551 ICD itself.
# * The getVitaHeaderSize(), getVitaPayloadSize(), and getVitaTailSize() 
#   methods use the payloadType argument to differentiate between the 
#   three supported payload formats.
#   * DDC format: "ddc"
#   * ADC format: "adc"
#   * Demod format: "demod"
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For ADC format, each 32-bit word contains two 16-bit ADC samples,
#    so the number of samples is getVitaPayloadSize("adc") / 2.
# ** For DDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("ddc") / 4.
# ** For demod format, each 32-bit word contains two 16-bit demod samples,
#    so the number of samples is getVitaPayloadSize("demod") / 2.
#
# \implements CyberRadioDriver.IRadio    
class ndr378(ndr551):
    _name = "NDR378"
    ifSpec = ndr378_ddc_ifSpec
    ifSpecMap = {
            "ddc":   ndr378_ddc_ifSpec,
            "adc":   ndr378_adc_ifSpec,
            "demod": ndr378_demod_ifSpec,
        }
    tunerType = ndr378_tuner
    numTuner = 8
    wbddcType = ndr378_wbddc
    numWbddc = 8
    nbddcType = ndr378_nbddc
    cddcGroupType = None


            
