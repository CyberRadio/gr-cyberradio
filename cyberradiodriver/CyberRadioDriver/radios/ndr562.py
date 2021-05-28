#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr562 
# \brief NDR562 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _jsonCommandBase, jsonConfig
from CyberRadioDriver.radios.ndr551 import ndr551, \
                                           ndr551_tuner, \
                                           ndr551_wbddc, \
                                           ndr551_nbddc, \
                                           ndr551_ddc_group, \
                                           ndr551_ddc_ifSpec, \
                                           ndr551_adc_ifSpec, \
                                           ndr551_demod_ifSpec

# Imports from external modules
# Python standard library imports

##
# \brief Tuner component class for the NDR562.
#
class ndr562_tuner(ndr551_tuner):
    _name = "Tuner(NDR562)"
    mnemonic = "tuner"
    frqRes = 10e6
    frqRange = (20e6,18e9)
    ifFilters = [200,320,500]
    queryParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_PRESELECT_BYPASS: "prebypass",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_IF_FILTER: "if",
                configKeys.TUNER_FNR: "fnr",
                configKeys.TUNER_GAIN_MODE: "mode",
                configKeys.ENABLE: "enable",
                configKeys.TUNER_AGC_SET_POINT: "asp",
                configKeys.TUNER_AGC_UPPER_LIMIT: "aul",
                configKeys.TUNER_AGC_LOWER_LIMIT: "aul",
                configKeys.TUNER_AGC_LOWER_LIMIT: "all",
                configKeys.TUNER_AGC_ATTACK_TIME: "aat",
                configKeys.TUNER_AGC_DECAY_TIME: "adt",
                configKeys.TUNER_AGC_ATTACK_STEP: "aas",
                configKeys.TUNER_AGC_DECAY_STEP: "ads",
                configKeys.TUNER_AGC_ATTACK_LIMIT: "aal",
                configKeys.TUNER_AGC_DECAY_LIMIT: "adl",
                }
    setParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_PRESELECT_BYPASS: "prebypass",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_IF_FILTER: "if",
                configKeys.TUNER_FNR: "fnr",
                configKeys.TUNER_GAIN_MODE: "mode",
                configKeys.ENABLE: "enable",
                configKeys.TUNER_AGC_SET_POINT: "asp",
                configKeys.TUNER_AGC_UPPER_LIMIT: "aul",
                configKeys.TUNER_AGC_LOWER_LIMIT: "aul",
                configKeys.TUNER_AGC_LOWER_LIMIT: "all",
                configKeys.TUNER_AGC_ATTACK_TIME: "aat",
                configKeys.TUNER_AGC_DECAY_TIME: "adt",
                configKeys.TUNER_AGC_ATTACK_STEP: "aas",
                configKeys.TUNER_AGC_DECAY_STEP: "ads",
                configKeys.TUNER_AGC_ATTACK_LIMIT: "aal",
                configKeys.TUNER_AGC_DECAY_LIMIT: "adl",
                }

##
# \brief WBDDC component class for the NDR562.
class ndr562_wbddc(ndr551_wbddc):
    _name = "WBDDC(NDR562)"
    rateSet = { 0 : 672.0e6, \
                1 : 448.0e6, \
                2 : 336.0e6, \
                3 : 336.0e6, \
                4 : 224.0e6, \
                5 : 112.0e6, \
                6 : 112.0e6   \
              }
    bwSet = { 0 : 500.0e6, \
              1 : 320.0e6, \
              2 : 250.0e6, \
              3 : 200.0e6, \
              4 : 160.0e6, \
              5 : 100.0e6, \
              6 : 80.0e6   \
            }
    tunable = True
    selectableSource = False
    frqRange = (-250e6,250e6,)
    frqRes = 1e3
    validConfigurationKeywords = [
                                configKeys.DDC_OUTPUT_TYPE,
                                configKeys.DDC_FREQUENCY_OFFSET,
                                configKeys.DDC_RATE_INDEX,
                                configKeys.ENABLE,
                                configKeys.DDC_GROUP_ID,
                                configKeys.DDC_STREAM_ID,
                                configKeys.DDC_LINK,
                                configKeys.DDC_UDP_DESTINATION,
                                configKeys.DDC_VITA_ENABLE
                                ]

##
# \internal
# \brief VITA 49 interface specification class for NDR562.
class ndr562_ifSpec(ndr551_ddc_ifSpec):
    headerSizeWords = 12
    payloadSizeWords = 2048
    tailSizeWords = 2
    byteOrder = "big"
    pass 

##
# \internal
# \brief Use to configure the IP information for the 40GbE
#
class e40g562(_jsonCommandBase):
    mnemonic = "e40g"
    queryParamMap = {
                configKeys.GIGE_PORT_INDEX: "link",
                configKeys.GIGE_DIP_INDEX: "dest",
                configKeys.GIGE_IP_ADDR: "ip",
                configKeys.GIGE_MAC_ADDR: "mac",
                configKeys.GIGE_DEST_PORT: "port",
                configKeys.GIGE_ARP: "arp",
                }
    setParamMap = {
                configKeys.GIGE_PORT_INDEX: "link",
                configKeys.GIGE_DIP_INDEX: "dest",
                configKeys.GIGE_IP_ADDR: "ip",
                configKeys.GIGE_MAC_ADDR: "mac",
                configKeys.GIGE_DEST_PORT: "port",
                configKeys.GIGE_ARP: "arp",
                }

##
# Data IP configuration command specific to the NDR562.
#
# \note Used to configure IP information with respect to the 
#    source.
#
class cfge40g562(_jsonCommandBase):
    mnemonic = "cfge40g"
    queryParamMap = {
                configKeys.GIGE_PORT_INDEX: "link",
                configKeys.GIGE_MAC_ADDR: "mac",
                configKeys.GIGE_IP_ADDR: "ip",
                configKeys.GIGE_NETMASK: "netmask",
                configKeys.GIGE_SOURCE_PORT: "port",
                }
    setParamMap = {
                configKeys.GIGE_PORT_INDEX: "link",
                configKeys.GIGE_IP_ADDR: "ip",
                configKeys.GIGE_NETMASK: "netmask",
                configKeys.GIGE_SOURCE_PORT: "port",
                }

##
# Status Query command specific to the NDR551.
#
class status562(_jsonCommandBase):
    mnemonic = "status"
    settable = False
    queryParamMap = {
                configKeys.VERINFO_MODEL: "model",
                configKeys.VERINFO_SN: "sn",
                configKeys.VERINFO_UNITREV: "unit",
                configKeys.VERINFO_SW: "sw",
                configKeys.STATUS_TUNERS: "tuners",
                configKeys.VERINFO_FW: "fw",
                configKeys.STATUS_WBDDCS: "wbddcs",
                configKeys.STATUS_ERROR: "error",
                configKeys.STATUS_PRI_MAC: "pmac",
                configKeys.STATUS_AUX_MAC: "amac",
                configKeys.STATUS_TEMP: "temp",
                configKeys.STATUS_10MHZ_REF: "cfg10m",
                configKeys.STATUS_10MHZ_REF_STATUS: "status10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                #configKeys.STATUS_PPS: "status1pps",
                configKeys.STATUS_PPS: "statuspps",
                configKeys.STATUS_ONTIME: "ontime",
                configKeys.STATUS_MEM: "mem",
                configKeys.STATUS_LINK0: "link0up",
                configKeys.STATUS_MICRO_LO1_LOCK: "micro1stlo",
                configKeys.STATUS_MICRO_LO2_LOCK: "micro2ndlo",
                configKeys.STATUS_ADC_1344MHZ_CLK_LOCK: "adcclk",
                configKeys.STATUS_FINAL_IF_LOCK: "finaliflo",
                configKeys.STATUS_FPGA_TEMP: "fpgatemp",
                configKeys.STATUS_LOW_RF_LOCK: "lowrflo"
                }
    
##
# Reference mode command specific to the NDR562.
#
class ref562(_jsonCommandBase):
    mnemonic = "ref"
    queryParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.TIME_UTC: "timeset",
                configKeys.NOISE_STATE: "nstate"
                }
    setParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.TIME_UTC: "timeset",
                configKeys.NOISE_STATE: "nstate"
                }

class pps562(_jsonCommandBase):
    mnemonic = "ref"
    queryParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.TIME_UTC: "timeset",
                configKeys.NOISE_STATE: "nstate"
                }
    setParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.TIME_UTC: "timeset",
                configKeys.NOISE_STATE: "nstate"
                }

class ifout562(_jsonCommandBase):
    mnemonic = "cntrl"
    queryParamMap = {
                configKeys.CNTRL_IF_OUT: "ifout",
                }
    setParamMap = {
                configKeys.CNTRL_IF_OUT: "ifout",
                }

##
# \brief Radio handler class for the NDR562.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR562 Connection Modes
#
# "udp"
#
# \section RadioConfig_NDR562 Radio Configuration Options
#
# \code
# configDict = {
#      "referenceMode": [0, 1],
#      "ppsSource": [0, 1],
#      "function": [integer (meaning is radio-dependent],
#      "tunerConfiguration": {
#            0: {
#               "frequency": [20000000.0, 250000000.0],
#               "attenuation": [0.0-40.0, step 0.5],
#               "enable": [True, False],
#               "ifFilter": [500, 320, 200],
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
#            1: {
#               "frequency": [500000000.0-18000000000.0, step 1000000.0],
#               "attenuation": [0.0-40.0, step 1.0],
#               "enable": [True, False],
#               "ifFilter": [500, 320, 200],
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
#            }
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              0: {
#                 "enable": [True, False],
#                 "outputType": ["iq", "raw"],
#                 "frequency": [-250e6-250e6, step 1e3],
#                 "filterIndex": [4],
#                 "udpDest": [UDP destination table index],
#                 "streamId": [stream ID],
#                 "link": [0, 1, 2, 3],
#              }
#         }
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
#            }
#      },
# }
# \endcode
#
# \section VITA_Notes_NDR562 VITA 49 Notes
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
# * The "header" includes not only the 7 words of the standard VITA
#   packet header, but also the 5 words of the metadata included in
#   each ADC/DDC payload.
# * The "tail" includes not only the standard VITA packet trailer, 
#   but also the trailer word within the ADC/DDC payload.
# * The definition of "payload" deviates from the ICD here, as we
#   want the "payload" to be only the part of the packet that 
#   contains data samples.  
# ** For ADC format, each 32-bit word contains two 16-bit ADC samples,
#    so the number of samples is getVitaPayloadSize() / 2.
# ** For DDC format, each 32-bit word contains one 16-bit I/16-bit Q 
#    sample, so the number of samples is getVitaPayloadSize() / 4.
#
# \note The values returned by getVitaHeaderSize(), getVitaPayloadSize(), 
#    and getVitaTailSize() assume that the data stream is using either the 
#    ADC format or the DDC format.  The demod format uses a completely 
#    different packet size and data format.
#
# \implements CyberRadioDriver.IRadio    
class ndr562(ndr551):
    _name = "NDR562"
    ifSpec = ndr562_ifSpec
    ifSpecMap = {}
    tunerType = ndr562_tuner
    wbddcType = ndr562_wbddc
    nbddcType = None
    cddcGroupType = None
    statQry = status562
    refCmd = ref562
    sipCmd = cfge40g562
    dipCmd = e40g562
    cntrlCmd = ifout562
    funCmd = None
    #ppsCmd = pps562
    numGigE = 1
    numTuner = 2
    numNbddc = 0
    numWbddc = 1
    numCddcGroups = 0
    ##
    # \brief The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [configKeys.REFERENCE_MODE, \
                                  configKeys.TIME_UTC, \
                                  configKeys.STATUS_PPS_SOURCE, \
                                  configKeys.CNTRL_IF_OUT
                                 ]
    

if __name__ == '__main__':
    pass
