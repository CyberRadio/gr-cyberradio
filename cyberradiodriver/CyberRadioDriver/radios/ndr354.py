#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr354
# \brief NDR354 Support
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
# Status Query command specific to the NDR354.
#
class status354(_jsonCommandBase):
    mnemonic = "status"
    settable = False
    queryParamMap = {
                configKeys.VERINFO_MODEL: "model",
                configKeys.VERINFO_SN: "unitserial",
                configKeys.VERINFO_UNITREV: "unit",
                configKeys.VERINFO_SW: "sw",
                configKeys.VERINFO_FW: "fw",
                configKeys.VERINFO_HW: "hw",
                configKeys.STATUS_TUNERS: "tuners",
                configKeys.STATUS_DIGBRD_SN: "digserial",
                configKeys.STATUS_TUNERBRD1_SN: "tb1serial",
                configKeys.STATUS_TUNERBRD2_SN: "tb2serial",
                configKeys.STATUS_ERROR: "error",
                configKeys.STATUS_10MHZ_REF: "cfg10m",
                configKeys.STATUS_10MHZ_REF_STATUS: "status10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.STATUS_NTP: "ntp",
                configKeys.STATUS_ONTIME: "ontime",
                configKeys.STATUS_LINK0: "link0up",
                configKeys.STATUS_LINK1: "link1up",
                configKeys.STATUS_CLOCK_TIME: "clktime",
                configKeys.STATUS_FAN: "fan",
                configKeys.STATUS_AVG_POWER: "avgpwr",
                configKeys.STATUS_BATTERY_LEVEL: "battery",
                configKeys.STATUS_HOSTNAME: "hostname",
                configKeys.STATUS_WBDDCS: "wbddcs",
                # Keys that should be present according to ICD, but aren't yet
                #configKeys.STATUS_CTL_MAC: "ctlmac",
                #configKeys.STATUS_DATA0_MAC: "data0mac",
                #configKeys.STATUS_DATA1_MAC: "data1mac",
                #configKeys.STATUS_PPS: "status1pps",
                #configKeys.STATUS_VOLTS: "volts",
                #configKeys.STATUS_LOCKS: "locks",
                #configKeys.STATUS_TEMPS: "temps",
                # Keys that are present but should not be according to ICD
                configKeys.STATUS_CTL_MAC: "pmac",
                configKeys.STATUS_DATA0_MAC: "e10g0mac",
                configKeys.STATUS_DATA1_MAC: "e10g1mac",
                configKeys.STATUS_PPS: "statuspps",
                configKeys.STATUS_ADC_CLOCK1: "adcclk1",
                configKeys.STATUS_ADC_CLOCK2: "adcclk2",
                configKeys.STATUS_DIGBRD_TEMP: "digtemp",
                configKeys.STATUS_FPGA_TEMP: "fpgatemp",
                configKeys.STATUS_LO11: "lo11",
                configKeys.STATUS_LO12: "lo12",
                configKeys.STATUS_LO13: "lo13",
                configKeys.STATUS_LO12: "lo14",
                configKeys.STATUS_LO21: "lo21",
                configKeys.STATUS_LO22: "lo22",
                configKeys.STATUS_LO23: "lo23",
                configKeys.STATUS_LO22: "lo24",
                configKeys.STATUS_MEM: "mem",
                configKeys.STATUS_MODE: "mode",
                configKeys.STATUS_TUNERBRD1_JESD: "tb1jesd",
                configKeys.STATUS_TUNERBRD2_JESD: "tb2jesd",
                configKeys.STATUS_TUNERBRD1_TEMP: "tb1temp",
                configKeys.STATUS_TUNERBRD2_TEMP: "tb2temp",
                configKeys.STATUS_TUNER_POWER: "tunerpower",
                configKeys.STATUS_VOLTS1: "volts1",
                configKeys.STATUS_VOLTS2: "volts2",
                configKeys.STATUS_VOLTS3: "volts3",
                configKeys.STATUS_VOLTS4: "volts4",
                configKeys.STATUS_VOLTS5: "volts5",
                }


##
# Tuner configuration command specific to the NDR354.
#
class tuner354(_jsonCommandBase):
    mnemonic = "tuner"
    queryParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_RF_ATTENUATION: "rfatten",
                configKeys.TUNER_IF_ATTENUATION: "ifatten",
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
                configKeys.TUNER_RF_INPUT_POWER: "inppwr",
                configKeys.TUNER_ADC_OVERLOAD: "ovrld",
                configKeys.TUNER_PRESELECT_BYPASS: "prebypass",
                configKeys.TUNER_COHERENT_GROUP: "cgroup",
                }
    setParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_RF_ATTENUATION: "rfatten",
                configKeys.TUNER_IF_ATTENUATION: "ifatten",
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
                configKeys.TUNER_PRESELECT_BYPASS: "prebypass",
                configKeys.TUNER_COHERENT_GROUP: "cgroup",
                }


##
# WBDDC configuration command specific to the NDR354.
#
class wbddc354(_jsonCommandBase):
    mnemonic = "wbddc"
    queryParamMap = {
                configKeys.INDEX: "id",
                configKeys.DDC_RATE_INDEX: "decimation",
                configKeys.DDC_STREAM_ID: "vita",
                configKeys.DDC_UDP_DESTINATION: "dest",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_RF_INDEX: "rfch",
                configKeys.DDC_CLASS_ID: "cid",
                configKeys.DDC_PHASE_OFFSET: "poffset",
                configKeys.ENABLE: "enable",
                configKeys.DDC_TOTAL_REPEAT_PACKETS: "total",
                configKeys.DDC_ACTIVE_REPEAT_PACKETS: "active",
                configKeys.DDC_GROUP_ENABLE: "groupenable",
                configKeys.DDC_DATA_PORT: "link",
                }
    setParamMap = {
                configKeys.INDEX: "id",
                configKeys.DDC_RATE_INDEX: "decimation",
                configKeys.DDC_STREAM_ID: "vita",
                configKeys.DDC_UDP_DESTINATION: "dest",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_RF_INDEX: "rfch",
                configKeys.DDC_CLASS_ID: "cid",
                configKeys.DDC_PHASE_OFFSET: "poffset",
                configKeys.ENABLE: "enable",
                configKeys.DDC_TOTAL_REPEAT_PACKETS: "total",
                configKeys.DDC_ACTIVE_REPEAT_PACKETS: "active",
                }


##
# Gigabit Ethernet configuration command specific to the NDR354.
#
class e10g354(_jsonCommandBase):
    mnemonic = "e10g"
    queryParamMap = {
                configKeys.GIGE_PORT_INDEX: "link",
                configKeys.GIGE_DIP_INDEX: "dest",
                configKeys.GIGE_IP_ADDR: "ip",
                configKeys.GIGE_MAC_ADDR: "mac",
                configKeys.GIGE_DEST_PORT: "port",
                }
    setParamMap = {
                configKeys.GIGE_PORT_INDEX: "link",
                configKeys.GIGE_DIP_INDEX: "dest",
                configKeys.GIGE_IP_ADDR: "ip",
                configKeys.GIGE_MAC_ADDR: "mac",
                configKeys.GIGE_DEST_PORT: "port",
                }


##
# Data IP configuration command specific to the NDR354.
#
# \note Used to configure IP information with respect to the
#    source.
#
class cfge10g354(_jsonCommandBase):
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
# WBDDC group configuration command specific to the NDR354.
#
class gddc354(_jsonCommandBase):
    mnemonic = "gddc"
    queryParamMap = {
                configKeys.INDEX: "group",
                configKeys.ENABLE: "enable",
                configKeys.DDC_GROUP_MEMBERS: "wbddc",
                configKeys.FFT_GROUP_MEMBERS: "fft",
                 }
    setParamMap = {
                configKeys.INDEX: "group",
                configKeys.ENABLE: "enable",
                configKeys.DDC_GROUP_MEMBERS: "wbddc",
                configKeys.FFT_GROUP_MEMBERS: "fft",
                 }


##
# FFT streaming configuration command specific to the NDR354.
#
class strmfftctl354(_jsonCommandBase):
    mnemonic = "strmfftctl"
    queryParamMap = {
                configKeys.INDEX: "id",
                configKeys.ENABLE: "enable",
                configKeys.DDC_STREAM_ID: "vita",
                configKeys.DDC_UDP_DESTINATION: "dest",
                configKeys.FFT_RATE: "rate",
                configKeys.FFT_WINDOW: "window",
                configKeys.FFT_SIZE: "size",
                configKeys.DDC_CLASS_ID: "cid",
                configKeys.DDC_TOTAL_REPEAT_PACKETS: "total",
                configKeys.DDC_ACTIVE_REPEAT_PACKETS: "active",
                 }
    setParamMap = {
                configKeys.INDEX: "id",
                configKeys.ENABLE: "enable",
                configKeys.DDC_STREAM_ID: "vita",
                configKeys.DDC_UDP_DESTINATION: "dest",
                configKeys.FFT_RATE: "rate",
                configKeys.FFT_WINDOW: "window",
                configKeys.FFT_SIZE: "size",
                configKeys.DDC_CLASS_ID: "cid",
                configKeys.DDC_TOTAL_REPEAT_PACKETS: "total",
                configKeys.DDC_ACTIVE_REPEAT_PACKETS: "active",
                 }


##
# Coherent tuning command specific to the NDR354.
#
class ctune354(_jsonCommandBase):
    mnemonic = "ctune"
    queryable = False
    setParamMap = {
                configKeys.TUNER_COHERENT_GROUP: "cgroup",
                configKeys.TUNER_FREQUENCY: "freq",
                 }


##
# Reference configuration command specific to the NDR354.
#
class cfg10m354(_jsonCommandBase):
    mnemonic = "ref"
    queryable = True
    queryParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                 }
    setParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                 }


##
# Tuner component class for the NDR354.
#
class ndr354_tuner(_tuner):
    _name = "Tuner(NDR354)"
    frqRange = (20e6,6e9)
    frqRes = 1e6
    frqUnits = 1
    attRange = (0.0,20.0)
    attRes = 1.0
    agc = False
    # The NDR354 has one tuner command that sets all tuner parameters.
    frqCmd = tuner354
    attCmd = None
    tpwrCmd = None
    # OVERRIDE
    ##
    # The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY,
                                  configKeys.TUNER_ATTENUATION,
                                  configKeys.TUNER_RF_ATTENUATION,
                                  configKeys.TUNER_IF_ATTENUATION,
                                  configKeys.ENABLE,
                                  configKeys.TUNER_FNR,
                                  configKeys.TUNER_GAIN_MODE,
                                  configKeys.TUNER_AGC_SET_POINT,
                                  configKeys.TUNER_AGC_UPPER_LIMIT,
                                  configKeys.TUNER_AGC_LOWER_LIMIT,
                                  configKeys.TUNER_AGC_ATTACK_TIME,
                                  configKeys.TUNER_AGC_DECAY_TIME,
                                  configKeys.TUNER_AGC_ATTACK_STEP,
                                  configKeys.TUNER_AGC_DECAY_STEP,
                                  configKeys.TUNER_AGC_ATTACK_LIMIT,
                                  configKeys.TUNER_AGC_DECAY_LIMIT,
                                  configKeys.TUNER_PRESELECT_BYPASS,
                                  configKeys.TUNER_COHERENT_GROUP,
                                  configKeys.TUNER_RF_INPUT_POWER,
                                  configKeys.TUNER_ADC_OVERLOAD
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
# WBDDC component class for the NDR354.
class ndr354_wbddc(_wbddc):
    _name = "WBDDC(NDR354)"
    tunable = True
    frqRange = (-62.5e6,62.5e6,)
    frqRes = 1e3
    rateSet = { 1: 147.2e6, \
                2: 73.6e6, \
                4: 36.8e6, \
                8: 18.4e6, \
                 }
    bwSet = { 1: 125e6, \
                2: 62.5e6, \
                4: 31.25e6, \
                8: 15.625e6, \
                 }
    dataFormat = { 1:"iq" }
    cfgCmd = wbddc354
    frqCmd = None
    nbssCmd = None
    # OVERRIDE
    validConfigurationKeywords = [
                                 configKeys.DDC_RF_INDEX,
                                 configKeys.DDC_FREQUENCY_OFFSET,
                                 configKeys.DDC_RATE_INDEX,
                                 configKeys.ENABLE,
                                 configKeys.DDC_STREAM_ID,
                                 configKeys.DDC_UDP_DESTINATION,
                                 configKeys.DDC_CLASS_ID,
                                 configKeys.DDC_PHASE_OFFSET,
                                 configKeys.ENABLE,
                                 configKeys.DDC_GROUP_ENABLE,
                                 configKeys.DDC_TOTAL_REPEAT_PACKETS,
                                 configKeys.DDC_ACTIVE_REPEAT_PACKETS,
                                 configKeys.DDC_DATA_PORT,
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
# FFT stream component for the NDR354.
#
class ndr354_fftStream(ndr354_wbddc):
    _name = "FFTStream(NDR354)"
    dataFormat = { 1:"iq" }
    cfgCmd = strmfftctl354
    frqCmd = None
    nbssCmd = None
    rateSet = { 500: 500,
                1000: 1000,
                1600: 1600,
                2000: 2000,
                 }
    windowSet = { "gaussian": "Gaussian",
                    "flat": "Flattop",
                    "hann": "Hann",
                    "hamming": "Hamming",
                     }
    sizeSet = {128:128, 256:256, 512:512, 1024:1024, 2048:2048,}

    validConfigurationKeywords = [
                                configKeys.ENABLE,
                                configKeys.DDC_STREAM_ID,
                                configKeys.DDC_UDP_DESTINATION,
                                configKeys.FFT_RATE,
                                configKeys.FFT_SIZE,
                                configKeys.FFT_WINDOW,
                                configKeys.DDC_TOTAL_REPEAT_PACKETS,
                                configKeys.DDC_ACTIVE_REPEAT_PACKETS
                                  ]

    def getWindowSet(self,):
        return self.windowSet()

    def getSizeSet(self,):
        return self.sizeSet()

##
# WBDDC group component for the NDR354.
#
class ndr354_wbddc_group(wbddc_group):
    _name = "WBDDCGroup(NDR354)"
    groupMemberIndexBase = 0
    numGroupMembers = 4
    groupMemberCmd = gddc354
    groupEnableCmd = gddc354

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
    # Overrides the base-class method because the 354 uses a single command to
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
    # Overrides the base-class method because the 354 uses a single command to
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
# \brief VITA 49 interface specification class for the NDR354.
class ndr354_ifSpec(_ifSpec):
    vita49_1 = False
    vita49_0 = True
    headerSizeWords = 5
    payloadSizeWords = 1024
    tailSizeWords = 1
    byteOrder = "big"

##
# \internal
# \brief VITA 49 interface specification class for the NDR354.
class ndr354_ccf_ifSpec(ndr354_ifSpec):
    payloadSizeWords = 2048


##
# \brief Radio handler for the NDR354.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR354 Connection Modes
#
# "https"
#
# \section RadioConfig_NDR354 Radio Configuration Options
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
class ndr354(_radio):
    _name = "NDR354"
    ifSpec = ndr354_ifSpec
    json = True
    numTuner = 4
    numWbddc = 4
    tunerType = ndr354_tuner
    tunerIndexBase = 0
    wbddcType = ndr354_wbddc
    wbddcIndexBase = 0
    numNbddc = 0
    nbddcType = None
    nbddcIndexBase = 0
    numFftStream = 4
    fftStreamType = ndr354_fftStream
    fftStreamIndexBase = 0
    numWbddcGroups = 4
    wbddcGroupIndexBase = 0
    wbddcGroupType = ndr354_wbddc_group
    numGigE = 2
    gigEIndexBase = 0
    numGigEDipEntries = 64
    gigEDipEntryIndexBase = 0
    idnQry = status354
    verQry = None
    hrevQry = None
    statQry = status354
    cfgCmd = None
    refCmd = cfg10m354
    rbypCmd = None
    sipCmd = cfge10g354
    dipCmd = e10g354
    smacCmd = None
    dmacCmd = None
    calfCmd = None
    resetCmd = None
    cohTuneCmd = ctune354
    fpgaStateCmd = fun
    refModes = {0:"Internal 10MHz",1:"External 10MHz"}
    rbypModes = {}
    connectionModes = ["https"]
    defaultPort = 443
    udpDestInfo = "Destination index"
    tunerBandwithSettable = False
    tunerBandwidthConstant = 125e6
    ##
    # \brief The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [
            configKeys.REFERENCE_MODE,
            configKeys.FPGA_STATE,
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
            cmd = self.idnQry(parent=self,
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
        # Since the 354 does not produce a single key with all hardware info,
        # construct hardware info from other response keys
        if rspInfo is not None:
            hwInfo = []
            if configKeys.STATUS_DIGBRD_SN in rspInfo:
                hwInfo.append("Digital Board S/N: %s" % rspInfo[configKeys.STATUS_DIGBRD_SN])
            if configKeys.STATUS_TUNERBRD1_SN in rspInfo:
                hwInfo.append("Tuner Board 1 S/N: %s" % rspInfo[configKeys.STATUS_TUNERBRD1_SN])
            if configKeys.STATUS_TUNERBRD2_SN in rspInfo:
                hwInfo.append("Tuner Board 2 S/N: %s" % rspInfo[configKeys.STATUS_TUNERBRD2_SN])
            self.versionInfo[configKeys.VERINFO_HW] = ", ".join(hwInfo)
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



class ndr354_wbddc_radio(ndr354):
    _name = "NDR354-WBDDC"

class ndr354_nbddc_radio(ndr354):
    _name = "NDR354-NBDDC"

class ndr354_ccf_radio(ndr354):
    _name = "NDR354-CCF"
    ifSpec = ndr354_ccf_ifSpec
