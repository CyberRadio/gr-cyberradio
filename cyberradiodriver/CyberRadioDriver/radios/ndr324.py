#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr324 
# \brief NDR324 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _jsonCommandBase, fun
from CyberRadioDriver.components import _tuner, _wbddc, \
                                        wbddc_group
from CyberRadioDriver.radio import _ifSpec, _radio


##
# Status Query command specific to the NDR324.
#
class status324(_jsonCommandBase):
    mnemonic = "status"
    settable = False
    queryParamMap = {
                configKeys.VERINFO_MODEL: "model",
                configKeys.VERINFO_SN: "sn",
                configKeys.VERINFO_UNITREV: "unit",
                configKeys.VERINFO_SW: "sw",
                configKeys.VERINFO_FW: "fw",
                configKeys.STATUS_TUNERS: "tuners",
                configKeys.STATUS_WBDDCS: "wbddcs",
                configKeys.STATUS_ERROR: "error",
                configKeys.STATUS_CTL_MAC: "pmac",
                configKeys.STATUS_TEMP: "temp",
                configKeys.STATUS_10MHZ_REF: "cfg10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.STATUS_10MHZ_REF_STATUS: "status10m",
                configKeys.STATUS_PPS: "statuspps",
                configKeys.STATUS_ONTIME: "ontime",
                configKeys.STATUS_MEM: "mem",
                configKeys.STATUS_LINK0: "link0up",
                configKeys.STATUS_LINK1: "link1up",
                configKeys.STATUS_LINK2: "link2up",
                configKeys.STATUS_LINK3: "link3up",
                configKeys.STATUS_TUNER0_LO1: "tuner0lo1",
                configKeys.STATUS_TUNER0_LO2: "tuner0lo2",
                configKeys.STATUS_TUNER1_LO1: "tuner1lo1",
                configKeys.STATUS_TUNER1_LO2: "tuner1lo2",
                configKeys.STATUS_TUNER2_LO1: "tuner2lo1",
                configKeys.STATUS_TUNER2_LO2: "tuner2lo2",
                configKeys.STATUS_TUNER3_LO1: "tuner3lo1",
                configKeys.STATUS_TUNER3_LO2: "tuner3lo2",
                configKeys.STATUS_ADC_CLOCK_REF: "adcrefclk",
                configKeys.STATUS_ADC_CLOCK_INT: "internaladcclk",
                configKeys.STATUS_FPGA_TEMP: "fpgatemp",
                }
    

##
# Tuner configuration command specific to the NDR324.
#
class tuner324(_jsonCommandBase):
    mnemonic = "tuner"
    queryParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.ENABLE: "enable",
                configKeys.TUNER_FNR: "fnr",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_GAIN_MODE: "mode",
                configKeys.TUNER_PRESELECTOR_MODE: "psmode",
                configKeys.TUNER_AGC_SET_POINT: "asp",
                configKeys.TUNER_AGC_UPPER_LIMIT: "aul",
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
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.ENABLE: "enable",
                configKeys.TUNER_FNR: "fnr",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_GAIN_MODE: "mode",
                configKeys.TUNER_PRESELECTOR_MODE: "psmode",
                configKeys.TUNER_AGC_SET_POINT: "asp",
                configKeys.TUNER_AGC_UPPER_LIMIT: "aul",
                configKeys.TUNER_AGC_LOWER_LIMIT: "all",
                configKeys.TUNER_AGC_ATTACK_TIME: "aat",
                configKeys.TUNER_AGC_DECAY_TIME: "adt",
                configKeys.TUNER_AGC_ATTACK_STEP: "aas",
                configKeys.TUNER_AGC_DECAY_STEP: "ads",
                configKeys.TUNER_AGC_ATTACK_LIMIT: "aal",
                configKeys.TUNER_AGC_DECAY_LIMIT: "adl",
                }
    

##
# DGS configuration command specific to the NDR324.
#
class dgs324(_jsonCommandBase):
    mnemonic = "dgs"
    queryParamMap = {
                configKeys.DGS_INDEX: "dgsid",
                configKeys.DGS_RF_INDEX: "rfch",
                configKeys.DGS_STREAM_ID: "vita",
                configKeys.DGS_LINK: "link",
                }
    setParamMap = {
                configKeys.DGS_INDEX: "id",
                configKeys.DGS_RF_INDEX: "rfch",
                configKeys.DGS_STREAM_ID: "vita",
                configKeys.DGS_LINK: "link",
                }
    
##
# WBDDC configuration command specific to the NDR324.
#
class wbddc324(_jsonCommandBase):
    mnemonic = "wbddc"
    queryParamMap = {
                configKeys.INDEX: "id",
                configKeys.DGS_INDEX: "dgsid",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_RATE_INDEX: "filter",
                configKeys.ENABLE: "enable",
                configKeys.DDC_GROUP_ID: "gddcid",
                configKeys.DDC_UDP_DESTINATION: "dest",
                }
    setParamMap = {
                configKeys.INDEX: "id",
                configKeys.DGS_INDEX: "dgsid",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_RATE_INDEX: "filter",
                configKeys.ENABLE: "enable",
                configKeys.DDC_GROUP_ID: "gddcid",
                configKeys.DDC_UDP_DESTINATION: "dest",
                }
    

##
# Gigabit Ethernet configuration command specific to the NDR324.
#
class e10g324(_jsonCommandBase):
    mnemonic = "e10g"
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
# Data IP configuration command specific to the NDR324.
#
# \note Used to configure IP information with respect to the 
#    source.
#
class cfge10g324(_jsonCommandBase):
    mnemonic = "cfge10g"
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
# WBDDC group configuration command specific to the NDR324.
#
class gddc324(_jsonCommandBase):
    mnemonic = "gddc"
    queryParamMap = {
                configKeys.INDEX: "gddcid",
                configKeys.ENABLE: "enable",
                configKeys.DDC_FREQUENCY_OFFSET: "offset", 
                configKeys.DDC_STREAM_ID: "vita", 
                 }
    setParamMap = {
                configKeys.INDEX: "gddcid",
                configKeys.ENABLE: "enable",
                configKeys.DDC_FREQUENCY_OFFSET: "offset", 
                configKeys.DDC_STREAM_ID: "vita", 
                 }


##
# FFT streaming configuration command specific to the NDR324.
#
class fft324(_jsonCommandBase):
    mnemonic = "fft"
    queryParamMap = {
                configKeys.INDEX: "id",
                configKeys.DGS_INDEX: "dgsid",
                configKeys.ENABLE: "enable",
                configKeys.DDC_UDP_DESTINATION: "dest",
                 }
    setParamMap = {
                configKeys.INDEX: "id",
                configKeys.DGS_INDEX: "dgsid",
                configKeys.ENABLE: "enable",
                configKeys.DDC_UDP_DESTINATION: "dest",
                 }


##
# Digital Link configuration command specific to the NDR324.
#
class dglink324(_jsonCommandBase):
    mnemonic = "dglink"
    queryParamMap = {
                configKeys.LINK: "link",
                configKeys.DGLINK_TYPE: "type",
                 }
    setParamMap = {
                configKeys.LINK: "link",
                configKeys.DGLINK_TYPE: "type",
                 }

##
# Reference configuration command specific to the NDR324.
#
class ref324(_jsonCommandBase):
    mnemonic = "ref"
    queryable = True
    queryParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.TIME_UTC: "timeset",
                configKeys.NOISE_GENERATOR: "noise",
                configKeys.NOISE_STATE: "nstate",
                 }
    setParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.TIME_UTC: "timeset",
                configKeys.NOISE_GENERATOR: "noise",
                configKeys.NOISE_STATE: "nstate",
                 }

##
# \internal
# \brief Cli command class specific to the NDR324.
#
#
# \note The cli command on the NDR324 is intended for internal
# diagnostic purposes.  It is not part of the publicly available
# ICD.
#
class cli324(_jsonCommandBase):
    mnemonic = "cli"
    queryable = False
    setParamMap = {
                "input": "input",
                 }

##
# Tuner component class for the NDR324.
#
class ndr324_tuner(_tuner):
    _name = "Tuner(NDR324)"
    frqRange = (20e6,6e9)
    frqRes = 10e6
    frqUnits = 1
    attRange = (0.0,40.0)
    attRes = 1.0
    agc = False
    # The NDR324 has one tuner command that sets all tuner parameters.
    frqCmd = tuner324
    attCmd = tuner324
    attCmd = None
    tpwrCmd = None
    # OVERRIDE
    ##
    # The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY, 
                                  configKeys.TUNER_ATTENUATION,
                                  configKeys.ENABLE, 
                                  configKeys.TUNER_FNR,
                                  configKeys.TUNER_GAIN_MODE,
                                  configKeys.TUNER_PRESELECTOR_MODE,
                                  configKeys.TUNER_AGC_SET_POINT,
                                  configKeys.TUNER_AGC_UPPER_LIMIT,
                                  configKeys.TUNER_AGC_LOWER_LIMIT,
                                  configKeys.TUNER_AGC_ATTACK_TIME,
                                  configKeys.TUNER_AGC_DECAY_TIME,
                                  configKeys.TUNER_AGC_ATTACK_STEP,
                                  configKeys.TUNER_AGC_DECAY_STEP,
                                  configKeys.TUNER_AGC_ATTACK_LIMIT,
                                  configKeys.TUNER_AGC_DECAY_LIMIT,
                                  ]
    
    def __init__(self,*args,**kwargs):
        _tuner.__init__(self,*args,**kwargs)
        
    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # Override
        if self.frqCmd is not None:
            cmd = self.frqCmd(**{ "parent": self, 
                                   configKeys.TUNER_INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                for key in self.validConfigurationKeywords:
                    val = rspInfo.get(key, None)
                    if val is not None:
                        self.configuration[key] = val
        pass

    # OVERRIDE
    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.  
    def _setConfiguration(self, confDict):
        ret = True
        keys = self.validConfigurationKeywords
        if any([q in confDict for q in keys]):
            if self.frqCmd is not None:
                cDict = {}
                self._dictUpdate(cDict, confDict, {}, keys)
                cDict.update({ "parent": self, 
                                configKeys.TUNER_INDEX: self.index,
                                 "verbose": self.verbose, 
                                 "logFile": self.logFile })
                cmd = self.frqCmd(**cDict)
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
# WBDDC component class for the NDR324.
class ndr324_wbddc(_wbddc):
    _name = "WBDDC(NDR324)"
    tunable = True
    selectableSource = True
    frqRange = (-250e6,250e6,)
    frqRes = 1e3
    rateSet = { 0: 225.28e6, \
                1: 168.96e6, \
                2: 42.24e6, \
                3: 21.12e6, \
                4: 10.56e6, \
              }
    bwSet = { 0: 200e6, \
                1: 125e6, \
                2: 20e6, \
                3: 10e6, \
                4: 5e6, \
            }

    dataFormat = { 1:"iq" }
    cfgCmd = wbddc324
    frqCmd = None
    nbssCmd = None
    # OVERRIDE
    validConfigurationKeywords = [
                                 configKeys.DGS_INDEX,
                                 configKeys.DDC_FREQUENCY_OFFSET,
                                 configKeys.DDC_RATE_INDEX,
                                 configKeys.ENABLE,
                                 configKeys.DDC_GROUP_ID,
                                 configKeys.DDC_UDP_DESTINATION,
                                  ]
    
    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # Override
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
                for key in self.validConfigurationKeywords:
                    if key in rspInfo:
                        self.configuration[key] = rspInfo.get(key, None)
        pass

    # OVERRIDE
    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.  
    def _setConfiguration(self, confDict):
        ret = True
        keys = self.validConfigurationKeywords
        if any([q in confDict for q in keys]):
            if self.cfgCmd is not None:
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
# FFT stream component for the NDR324.
#
class ndr324_fftStream(ndr324_wbddc):
    _name = "FFTStream(NDR324)"
    dataFormat = { 1:"iq" }
    cfgCmd = fft324
    frqCmd = None
    nbssCmd = None
    rateSet = { }
    bwSet = { }
    
    validConfigurationKeywords = [
                                configKeys.DGS_INDEX, 
                                configKeys.ENABLE, 
                                configKeys.DDC_UDP_DESTINATION, 
                                  ]
    
##
# WBDDC group component for the NDR324.
#
class ndr324_wbddc_group(wbddc_group):
    _name = "WBDDCGroup(NDR324)"
    groupMemberIndexBase = 0
    numGroupMembers = 4
    groupMemberCmd = gddc324
    groupEnableCmd = gddc324
    
    validConfigurationKeywords = [
                                  configKeys.ENABLE, 
                                  configKeys.DDC_GROUP_MEMBERS,
                                  configKeys.FFT_GROUP_MEMBERS,
                                  ]

    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    #
    # Overrides the base-class method because the 324 uses a single command to 
    # query all group members and whether the group is enabled. 
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # Override
        if self.groupMemberCmd is not None:
            cmd = self.groupMemberCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.configuration[configKeys.ENABLE] = rspInfo.get(configKeys.ENABLE, False)
                self.configuration[configKeys.DDC_GROUP_MEMBERS] = rspInfo.get(configKeys.DDC_GROUP_MEMBERS, [])
                self.configuration[configKeys.FFT_GROUP_MEMBERS] = rspInfo.get(configKeys.FFT_GROUP_MEMBERS, [])
        pass

    # OVERRIDE
    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.  
    #
    # Overrides the base-class method because the 324 uses a single command to 
    # set all group members and enable/disable the group. 
    def _setConfiguration(self, confDict):
        ret = True
        if self.groupMemberCmd is not None:
            #~ print "\n_setConfiguration",confDict,self.configuration
            members = self.configuration.get(configKeys.DDC_GROUP_MEMBERS, [])
            fftMembers = self.configuration.get(configKeys.FFT_GROUP_MEMBERS, [])
            enabled = self.configuration.get(configKeys.ENABLE,False)
            cDict = { "parent": self, 
                      configKeys.INDEX: self.index,
                      #~ configKeys.DDC_GROUP_MEMBERS: members,
                      #~ configKeys.FFT_GROUP_MEMBERS: fftMembers,
                      #~ configKeys.ENABLE: enabled,
                       "verbose": self.verbose, 
                       "logFile": self.logFile }
            if configKeys.DDC_GROUP_MEMBERS in confDict:
                if confDict[configKeys.DDC_GROUP_MEMBERS] is None:
                    cDict[configKeys.DDC_GROUP_MEMBERS] = members = []
                elif isinstance(confDict[configKeys.DDC_GROUP_MEMBERS], int):
                    cDict[configKeys.DDC_GROUP_MEMBERS] = members = [confDict[configKeys.DDC_GROUP_MEMBERS],]
                else:
                    cDict[configKeys.DDC_GROUP_MEMBERS] = members = confDict[configKeys.DDC_GROUP_MEMBERS]
            if configKeys.FFT_GROUP_MEMBERS in confDict:
                if confDict[configKeys.FFT_GROUP_MEMBERS] is None:
                    cDict[configKeys.FFT_GROUP_MEMBERS] = fftMembers = []
                elif isinstance(confDict[configKeys.FFT_GROUP_MEMBERS], int):
                    cDict[configKeys.FFT_GROUP_MEMBERS] = fftMembers =[confDict[configKeys.FFT_GROUP_MEMBERS],]
                else:
                    cDict[configKeys.FFT_GROUP_MEMBERS] = fftMembers = confDict[configKeys.FFT_GROUP_MEMBERS]
            if configKeys.ENABLE in confDict:
                cDict[configKeys.ENABLE] = enabled = confDict.get(configKeys.ENABLE, self.configuration.get(configKeys.ENABLE,False))
            #~ print "_setConfiguration",cDict
            cmd = self.groupMemberCmd(**cDict)
            ret &= cmd.send( self.callback, )
            ret &= cmd.success
            self._addLastCommandErrorInfo(cmd)
            if ret:
                self.configuration[configKeys.DDC_GROUP_MEMBERS] = members
                self.configuration[configKeys.FFT_GROUP_MEMBERS] = fftMembers
                self.configuration[configKeys.ENABLE] = enabled
            pass
        return ret


##
# \internal
# \brief VITA 49 interface specification class for the NDR324.
class ndr324_ifSpec(_ifSpec):
    headerSizeWords = 7
    payloadSizeWords = 2048
    tailSizeWords = 1
    byteOrder = "big"

##
# \internal
# \brief VITA 49 interface specification class for the NDR324.
class ndr324_fft_ifSpec(ndr324_ifSpec):
    headerSizeWords = 9


##
# \brief Radio handler for the NDR324.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR324 Connection Modes
#
# "https"
#
# \section RadioConfig_NDR324 Radio Configuration Options
#
# \code
# configDict = {
#      "fpgaState": [0, 1, 2, 3],
#      "referenceMode": [0, 1],
#      "tunerConfiguration": {
#            0: {
#               "preselectorBypass": [True, False], 
#               "frequency": [20000000.0-6000000000.0, step 1000000.0],
#               "attenuation": [0.0-40.0, step 0.25],
#               "rfAttenuation": [0.0-20.0, step 0.25],
#               "ifAttenuation": [0.0-20.0, step 0.25],
#               "enable": [True, False],
#               "cohGroup": [0, 1, 2, 3],
#               "fnr": [True, False],
#               "gainMode": ["auto", "manual", "freeze"],
#               "asp": [-40.0-0.0, step 0.25],
#               "aul": [-50.0-0.0, step 1.0],
#               "all": [-40.0-0.0, step 1.0],
#               "aat": [1-4095],
#               "adt": [1-4095],
#               "aas": [0.0-40.0, step 0.25],
#               "ads": [0.0-40.0, step 0.25],
#               "aal": [0.0-30.0, step 0.25],
#               "adl": [0.0-30.0, step 0.25],
#               "adcOverload": [True, False] [READ ONLY],
#               "rfInputPower": [-128-127] [READ ONLY]
#            },
#         ...3 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              0: {
#                 "activeRepeatPackets": [1-65536], 
#                 "classId": [True, False], 
#                 "dataPort": [0, 1, 2, 3] [READ ONLY], 
#                 "enable": [True, False], 
#                 "frequency": [-62e6-62e6, step 1e3], 
#                 "groupEnable": [True, False] [READ ONLY], 
#                 "phase": [-180-180], 
#                 "rateIndex": [1, 2, 4, 8], 
#                 "rfIndex": ["0", "1", "2", "3"], 
#                 "streamId": [stream ID], 
#                 "totalRepeatPackets": [1-65536], 
#                 "udpDest": [UDP destination table index]
#              },
#           ...3 (repeat for each WBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#            "wideband": {
#                0: {
#                   "enable": [True, False],
#                   "members": [None, a single WBDDC, or a Python list of WBDDCs],
#                },
#             ...3 (repeat for each WBDDC group)
#            },
#      },
#      "fftStream": {
#          0: {
#              "activeRepeatPackets": [1-65536], 
#              "enable": [True, False], 
#              "rate": [500, 1000, 1600, 2000], 
#              "size": [128, 256, 512, 1024, 2048], 
#              "streamId": [stream ID], 
#              "totalRepeatPackets": [1-65536], 
#              "udpDest": [UDP destination index], 
#              "window": ["hamming", "hann", "flat", "gaussian"]
#          },
#       ...3 (repeat for each FFT stream)
#      }, 
#      "ipConfiguration": {
#            0: {
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "destPort": [port],
#                   },
#                ...63 (repeat for each UDP destination index)
#               },
#               "sourceIP": {
#                   "ipAddr": [IP address],
#                   "macAddr": [MAC address] [READ ONLY],
#                   "netmask": [netmask],
#                   "sourcePort": [port],
#               },
#            },
#         ...1 (repeat for each 10-Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \note Setting the "fpgaState" item (or executing the setFpgaState() 
#    method, which is functionally identical) may disconnect the radio 
#    handler object.
#
# \implements CyberRadioDriver.IRadio    
class ndr324(_radio):
    _name = "NDR324"
    ifSpec = ndr324_ifSpec
    json = True
    numTuner = 4
    numWbddc = 4
    tunerType = ndr324_tuner
    tunerIndexBase = 0
    wbddcType = ndr324_wbddc
    wbddcIndexBase = 0
    numNbddc = 0
    nbddcType = None
    nbddcIndexBase = 0
    numFftStream = 4
    fftStreamType = ndr324_fftStream
    fftStreamIndexBase = 0
    numWbddcGroups = 4
    wbddcGroupIndexBase = 0
    wbddcGroupType = ndr324_wbddc_group
    numGigE = 4
    gigEIndexBase = 0
    numGigEDipEntries = 64
    gigEDipEntryIndexBase = 0
    idnQry = None
    verQry = None
    hrevQry = None
    statQry = status324
    cfgCmd = None
    refCmd = ref324
    rbypCmd = None
    sipCmd = cfge10g324
    dipCmd = e10g324
    smacCmd = None
    dmacCmd = None
    calfCmd = None
    resetCmd = None
    cohTuneCmd = None
    fpgaStateCmd = fun
    refModes = {0:"Internal 10MHz",1:"External 10MHz"}
    rbypModes = {}
    connectionModes = ["udp"]
    defaultPort = 19091
    udpDestInfo = "Destination index"
    tunerBandwithSettable = False
    tunerBandwidthConstant = 1351.68e6
    ##
    # \brief The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [
            configKeys.REFERENCE_MODE,
        ]

    # OVERRIDE
    ##
    # \brief Returns version information for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getVersionInfo()
    def getVersionInfo(self):
        # Query hardware for details if we don't have them already
        keys = [configKeys.VERINFO_MODEL, configKeys.VERINFO_SN, 
                configKeys.VERINFO_SW, configKeys.VERINFO_FW, 
                configKeys.VERINFO_REF, configKeys.VERINFO_UNITREV, 
                configKeys.VERINFO_HW]
        rspInfo = None
        if not all([key in self.versionInfo for key in keys]):
            cmd = self.statQry(parent=self, 
                               query=True,
                               verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self._dictUpdate(self.versionInfo, rspInfo, {}, keys)
        for key in keys:
            if key not in self.versionInfo:
                self.versionInfo[key] = "N/A"
        return self.versionInfo
    
    # OVERRIDE
    ##
    # \brief Gets the status from the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getStatus()
    def getStatus(self):
        if self.statQry is not None:
            cmd = self.statQry(parent=self,
                               verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand )
            # Parse response info from the command and return a dictionary
            # that mirrors the returns from NDR308-class STAT commands
            errMsg = ""
            if configKeys.STATUS_ERROR in cmd.getResponseInfo():
                errMsg = cmd.getResponseInfo()[configKeys.STATUS_ERROR]
            return {
                    "int": 0x0001 if errMsg != "" else 0x0000,
                    "statValues": [1] if errMsg != "" else [],
                    "statText": [errMsg] if errMsg != "" else [],
                }
        else:
            self.log("No status query available.")
            return None
    
if __name__ == '__main__':
	pass
