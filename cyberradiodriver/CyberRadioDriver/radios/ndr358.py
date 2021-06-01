#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr358 
# \brief NDR358 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#     All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver.radios.ndr551 import  ndr551, \
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
# \brief Tuner component class for the NDR358.
#
class ndr358_tuner(ndr551_tuner):
    _name = "Tuner(NDR358)"
    frqRange = (20e6,6e9)

##
# \brief WBDDC component class for the NDR358.
class ndr358_wbddc(ndr551_wbddc):
    _name = "WBDDC(NDR358)"

##
# \brief NBDDC component class for the NDR358.
class ndr358_nbddc(ndr551_nbddc):
    _name = "NBDDC(NDR358)"

##
# \brief NBDDC component class for the NDR358.
class ndr358_ddc_group(ndr551_ddc_group):
    _name = "DDCGroup(NDR358)"

##
# \internal
# \brief VITA 49 interface specification class for the NDR358's DDC format.
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
class ndr358_ddc_ifSpec(ndr551_ddc_ifSpec):
    pass


##
# \internal
# \brief VITA 49 interface specification class for NDR358's ADC format.
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
class ndr358_adc_ifSpec(ndr551_adc_ifSpec):
    pass


##
# \internal
# \brief VITA 49 interface specification class for the NDR358's demod format.
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
class ndr358_demod_ifSpec(ndr551_demod_ifSpec):
    pass


##
# \brief Radio handler class for the NDR358.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR358 Connection Modes
#
# "udp"
#
# \section RadioConfig_NDR358 Radio Configuration Options
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
#      "ddcGroupConfiguration": {
#            "combined": {
#                0: {
#                   "enable": [True, False],
#                   "startTime": [ISO 8601 time string],
#                   "samples": [number of samples],
#                   "frequency": [-40e6-40e6, step 1e3],
#                   "streamId": [stream ID],
#                },
#             ...15 (repeat for each DDC group)
#            },
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
# \section VITA_Notes_NDR358 VITA 49 Notes
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
class ndr358(ndr551):
    _name = "NDR358"
    ifSpec = ndr358_ddc_ifSpec
    ifSpecMap = {
            "ddc":   ndr358_ddc_ifSpec,
            "adc":   ndr358_adc_ifSpec,
            "demod": ndr358_demod_ifSpec,
        }
    tunerType = ndr358_tuner
    numTuner = 8
    wbddcType = ndr358_wbddc
    numWbddc = 8
    nbddcType = ndr358_nbddc
    cddcGroupType = ndr358_ddc_group


class ndr358_coherent(ndr358):
    _name = "NDR358-Coherent"
    numWbddc = 16


##
# \brief WBDDC configuration command specific to the NDR358 
#     Recorder variant.
#
class wbddc358_recorder(_jsonCommandBase):
    mnemonic = "wbddc"
    queryParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_OUTPUT_TYPE: "type",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_LINK: "link",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }
    setParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_OUTPUT_TYPE: "type",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_LINK: "link",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }


##
# \brief NBDDC configuration command specific to the NDR358 
#     Recorder variant.
#
class nbddc358_recorder(_jsonCommandBase):
    mnemonic = "nbddc"
    queryParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.DDC_OVERSAMPLING: "ovs",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_LINK: "link",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }
    setParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.DDC_OVERSAMPLING: "ovs",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_LINK: "link",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }


##
# \brief FFT streaming configuration command specific to the NDR358
#    Recorder variant.
#
class fft358_recorder(_jsonCommandBase):
    mnemonic = "fft"
    queryParamMap = {
            configKeys.INDEX: "id",
            configKeys.ENABLE: "enable",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.FFT_DEST_MAC_ADDR: "mac",
            configKeys.FFT_DEST_IP_ADDR: "ip",
            configKeys.FFT_DEST_PORT: "port",
        }
    setParamMap = {
            configKeys.INDEX: "id",
            configKeys.ENABLE: "enable",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.FFT_DEST_MAC_ADDR: "mac",
            configKeys.FFT_DEST_IP_ADDR: "ip",
            configKeys.FFT_DEST_PORT: "port",
        }


##
# \brief FFT IP configuration command specific to the NDR358
#    Recorder variant.
#
# \note Used to configure IP information with respect to the
#    source.
#
class cfge1gfft358_recorder(_jsonCommandBase):
    mnemonic = "cfge1gfft"
    queryParamMap = {
            configKeys.FFT_LINK: "link",
            configKeys.FFT_SOURCE_MAC_ADDR: "mac",
            configKeys.FFT_SOURCE_IP_ADDR: "ip",
            configKeys.FFT_SOURCE_NETMASK: "netmask",
            configKeys.FFT_SOURCE_PORT: "port",
        }
    setParamMap = {
            configKeys.FFT_LINK: "link",
            configKeys.FFT_SOURCE_IP_ADDR: "ip",
            configKeys.FFT_SOURCE_NETMASK: "netmask",
            configKeys.FFT_SOURCE_PORT: "port",
        }


##
# \brief WBDDC component class for the NDR358 Recorder variant.
class ndr358_recorder_wbddc(ndr358_wbddc):
    _name = "WBDDC(NDR358-Recorder)"
    # OVERRIDES
    rateSet = {
            50: 102.4e6,
            49: 51.2e6,
            48: 51.2e6,
            47: 25.6e6,
            46: 25.6e6,
            45: 12.8e6,
            44: 12.8e6,
            43: 6.4e6,
            42: 6.4e6,
        }
    bwSet = {
            50: 80e6,
            49: 40e6,
            48: 25e6,
            47: 20e6,
            46: 12.5e6,
            45: 10e6,
            44: 8e6,
            43: 5e6,
            42: 4e6,
        }
    # sample size in 4 byte words
    ssSet = {
            50: 1024,
            49: 1024,
            48: 1024,
            47: 1024,
            46: 1024,
            45: 1024,
            44: 1024,
            43: 1024,
            42: 1024,
        }
    cfgCmd = wbddc358_recorder
    validConfigurationKeywords = [
            configKeys.DDC_RF_INDEX,
            configKeys.DDC_OUTPUT_TYPE,
            configKeys.DDC_FREQUENCY_OFFSET,
            configKeys.DDC_RATE_INDEX,
            configKeys.ENABLE,
            configKeys.DDC_GROUP_ID,
            configKeys.DDC_STREAM_ID,
            configKeys.DDC_LINK,
            configKeys.DDC_UDP_DESTINATION,
            configKeys.DDC_DGC_MODE,
            configKeys.DDC_DGC_GAIN,
            configKeys.DDC_DGC_UPPER_LIMIT,
            configKeys.DDC_DGC_LOWER_LIMIT,
            configKeys.DDC_DGC_TARGET_RANGE,
            configKeys.DDC_DGC_ATTACK_LIMIT,
            configKeys.DDC_DGC_DECAY_LIMIT,
            configKeys.DDC_DGC_ATTACK_OFFSET,
            configKeys.DDC_DGC_DECAY_OFFSET,
            configKeys.DDC_DGC_ATTACK_TIME,
            configKeys.DDC_DGC_DECAY_TIME,
            configKeys.DDC_DGC_ATTACK_TRIGGER,
            configKeys.DDC_DGC_DECAY_TRIGGER,
        ]


##
# \brief NBDDC component class for the NDR358 Recorder variant.
class ndr358_recorder_nbddc(ndr358_nbddc):
    _name = "NBDDC(NDR358-Recorder)"
    # OVERRIDES
    rateSet = {
            16: 2000e3,
            15: 4000e3,
            14: 3200e3,
            13: 1280e3,
            12: 400e3,
            11: 256e3,
            10: 200e3,
             9: 128e3,
             8: 64e3,
             7: 32e3,
             6: 16e3,
             5: 8e3,
             4: 4e3,
             3: 2e3,
             2: 1e3,
             1: 0.5e3,
             0: 0.25e3,
        }
    bwSet = {
            16: 1500e3,
            15: 3200e3,
            14: 2500e3,
            13: 1000e3,
            12: 300e3,
            11: 200e3,
            10: 150e3,
             9: 100e3,
             8: 50e3,
             7: 25e3,
             6: 12.5e3,
             5: 6.4e3,
             4: 3.2e3,
             3: 1.6e3,
             2: 0.8e3,
             1: 0.4e3,
             0: 0.2e3,
        }
    # sample size in 4 byte words
    ssSet = {
            16: 1280,
            15: 1280,
            14: 1280,
            13: 1280,
            12: 1280,
            11: 1280,
            10: 1280,
             9: 1280,
             8: 1280,
             7: 1280,
             6: 1280,
             5: 1280,
             4: 1280,
             3: 1280,
             2: 1280,
             1: 1280,
             0: 1280,
        }
    cfgCmd = nbddc358_recorder
    validConfigurationKeywords = [
            configKeys.DDC_RF_INDEX,
            configKeys.DDC_OUTPUT_TYPE,
            configKeys.DDC_FREQUENCY_OFFSET,
            configKeys.DDC_RATE_INDEX,
            configKeys.DDC_OVERSAMPLING,
            configKeys.ENABLE,
            configKeys.DDC_GROUP_ID,
            configKeys.DDC_STREAM_ID,
            configKeys.DDC_LINK,
            configKeys.DDC_UDP_DESTINATION,
            configKeys.DDC_DGC_MODE,
            configKeys.DDC_DGC_GAIN,
            configKeys.DDC_DGC_UPPER_LIMIT,
            configKeys.DDC_DGC_LOWER_LIMIT,
            configKeys.DDC_DGC_TARGET_RANGE,
            configKeys.DDC_DGC_ATTACK_LIMIT,
            configKeys.DDC_DGC_DECAY_LIMIT,
            configKeys.DDC_DGC_ATTACK_OFFSET,
            configKeys.DDC_DGC_DECAY_OFFSET,
            configKeys.DDC_DGC_ATTACK_TIME,
            configKeys.DDC_DGC_DECAY_TIME,
            configKeys.DDC_DGC_ATTACK_TRIGGER,
            configKeys.DDC_DGC_DECAY_TRIGGER,
        ]


##
# \brief FFT stream component for the NDR358 Recorder variant.
#
class ndr358_recorder_fftStream(ndr358_wbddc):
    _name = "FFTStream(NDR358-Recorder)"
    dataFormat = { 1:"iq" }
    cfgCmd = fft358_recorder
    srcCfgCmd = cfge1gfft358_recorder
    frqCmd = None
    nbssCmd = None
    rateSet = { }
    bwSet = { }

    validConfigurationKeywords = [
            configKeys.FFT_LINK,
            configKeys.ENABLE,
            configKeys.DDC_STREAM_ID,
            configKeys.FFT_SOURCE_MAC_ADDR,
            configKeys.FFT_SOURCE_IP_ADDR,
            configKeys.FFT_SOURCE_PORT,
            configKeys.FFT_SOURCE_NETMASK,
            configKeys.FFT_DEST_MAC_ADDR,
            configKeys.FFT_DEST_IP_ADDR,
            configKeys.FFT_DEST_PORT,
        ]

    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # Override
        if self.srcCfgCmd is not None:
            cmd = self.srcCfgCmd(**{ "parent": self,
                                     "query": True,
                                     "verbose": self.verbose,
                                     "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            #self.logIfVerbose("rspInfo =", rspInfo)
            if rspInfo is not None:
                for key in [
                        configKeys.FFT_LINK,
                        configKeys.FFT_SOURCE_MAC_ADDR,
                        configKeys.FFT_SOURCE_IP_ADDR,
                        configKeys.FFT_SOURCE_PORT,
                        configKeys.FFT_SOURCE_NETMASK,
                    ]:
                    if key in rspInfo:
                        self.configuration[key] = rspInfo.get(key, None)
        if self.cfgCmd is not None:
            cmd = self.cfgCmd(**{ "parent": self,
                                  configKeys.INDEX: self.index,
                                  "query": True,
                                  "verbose": self.verbose,
                                  "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            #self.logIfVerbose("rspInfo =", rspInfo)
            if rspInfo is not None:
                for key in [
                        configKeys.ENABLE,
                        configKeys.DDC_STREAM_ID,
                        configKeys.FFT_DEST_MAC_ADDR,
                        configKeys.FFT_DEST_IP_ADDR,
                        configKeys.FFT_DEST_PORT,
                    ]:
                    if key in rspInfo:
                        self.configuration[key] = rspInfo.get(key, None)
        pass

    # OVERRIDE
    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.
    def _setConfiguration(self, confDict):
        ret = True
        if any([q in confDict for q in self.validConfigurationKeywords]):
            if self.srcCfgCmd is not None:
                keys = [
                        configKeys.FFT_LINK,
                        configKeys.FFT_SOURCE_MAC_ADDR,
                        configKeys.FFT_SOURCE_IP_ADDR,
                        configKeys.FFT_SOURCE_PORT,
                        configKeys.FFT_SOURCE_NETMASK,
                    ]
                cDict = {}
                self._dictUpdate(cDict, confDict, {}, keys)
                cDict.update({ "parent": self,
                               "verbose": self.verbose,
                               "logFile": self.logFile })
                cmd = self.srcCfgCmd(**cDict)
                ret &= cmd.send( self.callback, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    for key in keys:
                        if key in confDict:
                            self.configuration[key] = confDict[key]
                pass
            if self.cfgCmd is not None:
                keys = [
                        configKeys.ENABLE,
                        configKeys.DDC_STREAM_ID,
                        configKeys.FFT_DEST_MAC_ADDR,
                        configKeys.FFT_DEST_IP_ADDR,
                        configKeys.FFT_DEST_PORT,
                    ]
                cDict = {}
                self._dictUpdate(cDict, confDict, {}, keys)
                cDict.update({ "parent": self,
                               configKeys.INDEX: self.index,
                               "verbose": self.verbose,
                               "logFile": self.logFile })
                cmd = self.cfgCmd(**cDict)
                ret &= cmd.send( self.callback, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    for key in keys:
                        if key in confDict:
                            self.configuration[key] = confDict[key]
                pass
        return ret



##
# \internal
# \brief VITA 49 interface specification class for the NDR358 Recorder 
#    variant's WBDDC format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each WBDDC payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the WBDDC payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For WBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("wbddc") / 4.
class ndr358_recorder_wbddc_ifSpec(ndr358_ddc_ifSpec):
    headerSizeWords = 12 
    payloadSizeWords = 1024
    tailSizeWords = 2
    byteOrder = "big"


##
# \internal
# \brief VITA 49 interface specification class for the NDR358 Recorder 
#    variant's NBDDC format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each NBDDC payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the NBDDC payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For NBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("nbddc") / 4.
class ndr358_recorder_nbddc_ifSpec(ndr358_ddc_ifSpec):
    headerSizeWords = 12 
    payloadSizeWords = 1280
    tailSizeWords = 2
    byteOrder = "big"


##
# \internal
# \brief VITA 49 interface specification class for the NDR358 Recorder 
#    variant's FFT format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each FFT payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the FFT payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For FFT format, each 32-bit word contains four 8-bit FFT bin
#    values, so the number of bins is getVitaPayloadSize("fft").
class ndr358_recorder_fft_ifSpec(ndr358_ddc_ifSpec):
    headerSizeWords = 12 
    payloadSizeWords = 2048
    tailSizeWords = 2
    byteOrder = "big"


##
# \brief Radio handler class for the NDR358 Recorder variant.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR358Rec Connection Modes
#
# "udp"
#
# \section RadioConfig_NDR358Rec Radio Configuration Options
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
#                 "rfIndex": ["0", "1", "2", "3", "4", "5", "6", "7"],
#                 "outputType": ["iq"],
#                 "frequency": [-40e6-40e6, step 1e3],
#                 "filterIndex": [42-50, step 1],
#                 "groupId": [0-15, step 1],
#                 "streamId": [stream ID],
#                 "link": [0, 1, 2, 3],
#                 "udpDest": [UDP destination table index],
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
#                 "frequency": [-40e6-40e6, step 1e3],##
#                 "rfIndex": ["0", "1", "2", "3", "4", "5", "6", "7"],
#                 "filterIndex": [0-16 step 1],
#                 "oversampling": [1, 2, 4, 8, 16],
#                 "groupId": [0-15, step 1],
#                 "streamId": [stream ID],
#                 "link": [0, 1, 2, 3],
#                 "udpDest": [UDP destination table index],
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
#           ...15 (repeat for each NBDDC)
#         },
#      },
#      "fftStream": {
#          0: {
#              "enable": [True, False],
#              "link": [0],
#              "streamId": [stream ID],
#              "sourceMacAddr": [MAC address string (read-only)],
#              "sourceIpAddr": [IP address string],
#              "sourcePort": [UDP port number],
#              "sourceNetmask": [netmask string],
#              "destMacAddr": [MAC address string],
#              "destIpAddr": [IP address string],
#              "destPort": [UDP port number],
#          },
#       ...7 (repeat for each FFT stream)
#      },
#      "ddcGroupConfiguration": {
#            "combined": {
#                0: {
#                   "enable": [True, False],
#                   "startTime": [ISO 8601 time string],
#                   "samples": [number of samples],
#                   "frequency": [-40e6-40e6, step 1e3],
#                   "streamId": [stream ID],
#                },
#             ...15 (repeat for each DDC group)
#            },
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
# \section VITA_Notes_NDR358Rec VITA 49 Notes
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
#   * WBDDC format: "wbddc"
#   * NBDDC format: "nbddc"
#   * FFT format: "fft"
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For WBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("wbddc") / 4.
# ** For NBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("nbddc") / 4.
# ** For FFT format, each 32-bit word contains four 8-bit FFT bin
#    values, so the number of bins is getVitaPayloadSize("fft").
#
# \implements CyberRadioDriver.IRadio    
class ndr358_recorder(ndr358):
    _name = "NDR358-Recorder"
    wbddcType = ndr358_recorder_wbddc
    nbddcType = ndr358_recorder_nbddc
    numNbddc = 16
    nbddcIndexBase = 0
    # nbddcIndexOverride = [0, 1, 2, 3, 16, 17, 18, 19, 32, 33, 34, 35, 48, 49, 50, 51]
    ifSpec = ndr358_recorder_wbddc_ifSpec
    ifSpecMap = {
            "wbddc": ndr358_recorder_wbddc_ifSpec,
            "nbddc": ndr358_recorder_nbddc_ifSpec,
            "fft":   ndr358_recorder_fft_ifSpec,
        }
    numFftStream = 8
    fftStreamType = ndr358_recorder_fftStream
    fftStreamIndexBase = 0
    
    
##
# \brief WBDDC configuration command specific to the NDR358 
#     ALT_RX1 variant.
#
class wbddc358_altrx1(_jsonCommandBase):
    mnemonic = "wbddc"
    queryParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_OUTPUT_TYPE: "type",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_LINK: "link",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }
    setParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_OUTPUT_TYPE: "type",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_LINK: "link",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }


##
# \brief NBDDC configuration command specific to the NDR358 
#     ALT_RX1 variant.
#
class nbddc358_altrx1(_jsonCommandBase):
    mnemonic = "nbddc"
    queryParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_OUTPUT_TYPE: "type",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_DECIMATION: "decimation",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }
    setParamMap = {
            configKeys.INDEX: "id",
            configKeys.DDC_RF_INDEX: "rfch",
            configKeys.DDC_OUTPUT_TYPE: "type",
            configKeys.DDC_FREQUENCY_OFFSET: "offset",
            configKeys.DDC_DECIMATION: "decimation",
            configKeys.DDC_RATE_INDEX: "filter",
            configKeys.ENABLE: "enable",
            configKeys.DDC_GROUP_ID: "gddcid",
            configKeys.DDC_STREAM_ID: "vita",
            configKeys.DDC_UDP_DESTINATION: "dest",
            configKeys.DDC_DGC_MODE: "mode",
            configKeys.DDC_DGC_GAIN: "dgv",
            configKeys.DDC_DGC_UPPER_LIMIT: "dul",
            configKeys.DDC_DGC_LOWER_LIMIT: "dll",
            configKeys.DDC_DGC_TARGET_RANGE: "dtl",
            configKeys.DDC_DGC_ATTACK_LIMIT: "dal",
            configKeys.DDC_DGC_DECAY_LIMIT: "ddl",
            configKeys.DDC_DGC_ATTACK_OFFSET: "dao",
            configKeys.DDC_DGC_DECAY_OFFSET: "ddo",
            configKeys.DDC_DGC_ATTACK_TIME: "datc",
            configKeys.DDC_DGC_DECAY_TIME: "ddtc",
            configKeys.DDC_DGC_ATTACK_TRIGGER: "dat",
            configKeys.DDC_DGC_DECAY_TRIGGER: "ddt",
        }


##
# \brief WBDDC component class for the NDR358 ALT_RX1 variant.
class ndr358_altrx1_wbddc(ndr358_wbddc):
    _name = "WBDDC(NDR358-Altrx1)"
    # OVERRIDES
    rateSet = {
            58: 22.0e6,
            57: 20.0e6,
            56: 30.72e6,
            55: 23.04e6,
            54: 15.36e6,
            53: 7.68e6,
            52: 1.92e6,
            51: 1.2288e6,
            40: 128.0e6,
            39: 64.0e6,
            38: 32.0e6,
            37: 32.0e6,
            36: 16.0e6,
            35: 16.0e6,
            34: 16.0e6,
            33: 8.0e6,
            32: 8.0e6,
        }
    bwSet = {
            58: 22.0e6,
            57: 16.6e6,
            56: 20.0e6,
            55: 15.0e6,
            54: 10.0e6,
            53: 5.0e6,
            52: 1.4e6,
            51: 1.25e6,
            40: 80.0e6,
            39: 40.0e6,
            38: 25.0e6,
            37: 20.0e6,
            36: 12.5e6,
            35: 10.0e6,
            34: 8.0e6,
            33: 5.0e6,
            32: 4.0e6,
        }
    #sample size in 4-byte words
    ssSet = {
            58: 1375,
            57: 1250,
            56: 960,
            55: 1080,
            54: 960,
            53: 960,
            52: 960,
            51: 960,
            40: 1000,
            39: 1000,
            38: 1000,
            37: 1000,
            36: 1000,
            35: 1000,
            34: 1000,
            33: 1000,
            32: 1000,
        }
    cfgCmd = wbddc358_altrx1
    validConfigurationKeywords = [
            configKeys.DDC_RF_INDEX,
            configKeys.DDC_OUTPUT_TYPE,
            configKeys.DDC_FREQUENCY_OFFSET,
            configKeys.DDC_RATE_INDEX,
            configKeys.ENABLE,
            configKeys.DDC_GROUP_ID,
            configKeys.DDC_STREAM_ID,
            configKeys.DDC_LINK,
            configKeys.DDC_UDP_DESTINATION,
            configKeys.DDC_DGC_MODE,
            configKeys.DDC_DGC_GAIN,
            configKeys.DDC_DGC_UPPER_LIMIT,
            configKeys.DDC_DGC_LOWER_LIMIT,
            configKeys.DDC_DGC_TARGET_RANGE,
            configKeys.DDC_DGC_ATTACK_LIMIT,
            configKeys.DDC_DGC_DECAY_LIMIT,
            configKeys.DDC_DGC_ATTACK_OFFSET,
            configKeys.DDC_DGC_DECAY_OFFSET,
            configKeys.DDC_DGC_ATTACK_TIME,
            configKeys.DDC_DGC_DECAY_TIME,
            configKeys.DDC_DGC_ATTACK_TRIGGER,
            configKeys.DDC_DGC_DECAY_TRIGGER,
        ]


##
# \brief NBDDC component class for the NDR358 ALT_RX1 variant.
class ndr358_altrx1_nbddc(ndr358_nbddc):
    _name = "NBDDC(NDR358-Altrx1)"
    # OVERRIDES
    rateSet = {
            20: 250e3,
            16: 2000e3,
            15: 4000e3,
            14: 3200e3,
            13: 1280e3,
            12: 400e3,
            11: 256e3,
            10: 200e3,
             9: 128e3,
             8: 64e3,
             7: 32e3,
             6: 16e3,
             5: 8e3,
             4: 4e3,
             3: 2e3,
             2: 1e3,
             1: 0.5e3,
             0: 0.25e3,
        }
    bwSet = {
            20: 200e3,
            16: 1500e3,
            15: 3200e3,
            14: 2500e3,
            13: 1000e3,
            12: 300e3,
            11: 200e3,
            10: 150e3,
             9: 100e3,
             8: 50e3,
             7: 25e3,
             6: 12.5e3,
             5: 6.4e3,
             4: 3.2e3,
             3: 1.6e3,
             2: 0.8e3,
             1: 0.4e3,
             0: 0.2e3,
        }
    #sample size in 4-byte words
    ssSet = {
            20: 1000,
            16: 1000,
            15: 1000,
            14: 1000,
            13: 1000,
            12: 1000,
            11: 1000,
            10: 1000,
             9: 1000,
             8: 1000,
             7: 1000,
             6: 1000,
             5: 1000,
             4: 1000,
             3: 1000,
             2: 1000,
             1: 1000,
             0: 1000,
        }
    cfgCmd = nbddc358_altrx1
    validConfigurationKeywords = [
            configKeys.DDC_RF_INDEX,
            configKeys.DDC_OUTPUT_TYPE,
            configKeys.DDC_FREQUENCY_OFFSET,
            configKeys.DDC_DECIMATION,
            configKeys.DDC_RATE_INDEX,
            configKeys.ENABLE,
            configKeys.DDC_GROUP_ID,
            configKeys.DDC_STREAM_ID,
            configKeys.DDC_UDP_DESTINATION,
            configKeys.DDC_DGC_MODE,
            configKeys.DDC_DGC_GAIN,
            configKeys.DDC_DGC_UPPER_LIMIT,
            configKeys.DDC_DGC_LOWER_LIMIT,
            configKeys.DDC_DGC_TARGET_RANGE,
            configKeys.DDC_DGC_ATTACK_LIMIT,
            configKeys.DDC_DGC_DECAY_LIMIT,
            configKeys.DDC_DGC_ATTACK_OFFSET,
            configKeys.DDC_DGC_DECAY_OFFSET,
            configKeys.DDC_DGC_ATTACK_TIME,
            configKeys.DDC_DGC_DECAY_TIME,
            configKeys.DDC_DGC_ATTACK_TRIGGER,
            configKeys.DDC_DGC_DECAY_TRIGGER,
        ]


##
# \internal
# \brief VITA 49 interface specification class for the NDR358 ALT_RX1 
#    variant's WBDDC format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each WBDDC payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the WBDDC payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For WBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("wbddc") / 4.
# *** The payload size varies based on the filter. Five different 
#     payload sizes are present - 960*4, 1000*4, 1080*4, 1250*4, 1375*4. 
class ndr358_altrx1_wbddc_ifSpec(ndr358_ddc_ifSpec):
    headerSizeWords = 12 
    payloadSizeWords = 960
    tailSizeWords = 2
    byteOrder = "big"


##
# \internal
# \brief VITA 49 interface specification class for the NDR358 Recorder 
#    variant's NBDDC format.
# \note Some explanation for these values is probably in order.
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each NBDDC payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the NBDDC payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For NBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("nbddc") / 4.
class ndr358_altrx1_nbddc_ifSpec(ndr358_ddc_ifSpec):
    headerSizeWords = 12 
    payloadSizeWords = 1000
    tailSizeWords = 2
    byteOrder = "big"


##
#
# \section VITA_Notes_NDR358Rec_2 VITA 49 Notes
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
#   * WBDDC format: "wbddc"
#   * NBDDC format: "nbddc"
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For WBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("wbddc") / 4.
# ** For NBDDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize("nbddc") / 4.
#
# \implements CyberRadioDriver.IRadio    
class ndr358_altrx1(ndr358):
    _name = "NDR358-ALTRX1"
    wbddcType = ndr358_altrx1_wbddc
    nbddcType = ndr358_altrx1_nbddc
    ifSpec = ndr358_altrx1_wbddc_ifSpec
    ifSpecMap = {
            "wbddc": ndr358_altrx1_wbddc_ifSpec,
            "nbddc": ndr358_altrx1_nbddc_ifSpec,
        }
    
    
if __name__ == '__main__':
    pass
