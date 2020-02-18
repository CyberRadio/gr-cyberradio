#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr551 
# \brief NDR551 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.  
#     All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _jsonCommandBase, jsonConfig
from CyberRadioDriver.components import _tuner, _wbddc, _nbddc, \
                                        adjustFrequency, adjustAttenuation, \
                                        ddc_group
from CyberRadioDriver.radio import _ifSpec, _radio, funJSON
# Imports from external modules
# Python standard library imports
import json
import traceback


class tuner551(_jsonCommandBase):
    mnemonic = "tuner"
    queryParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_PRESELECT_BYPASS: "prebypass",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_IF_FILTER: "if",
                configKeys.TUNER_FNR: "fnr",
                configKeys.TUNER_GAIN_MODE: "mode",
                configKeys.TUNER_DELAY: "delay",
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
                configKeys.TUNER_DELAY: "delay",
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
# WBDDC configuration command specific to the NDR551.
#
class wbddc551(_jsonCommandBase):
    mnemonic = "wbddc"
    queryParamMap = {
                configKeys.INDEX: "id",
                configKeys.DDC_RF_INDEX: "rfch",
                configKeys.DDC_OUTPUT_TYPE: "type",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_DECIMATION: "decimation",
                configKeys.DDC_RATE_INDEX: "filter",
                configKeys.DDC_OVERSAMPLING: "ovs",
                configKeys.ENABLE: "enable",
                configKeys.DDC_START_TIME: "start",
                configKeys.DDC_SAMPLES: "samples",
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
                configKeys.DDC_DECIMATION: "decimation",
                configKeys.DDC_RATE_INDEX: "filter",
                configKeys.DDC_OVERSAMPLING: "ovs",
                configKeys.ENABLE: "enable",
                configKeys.DDC_START_TIME: "start",
                configKeys.DDC_SAMPLES: "samples",
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
# NBDDC configuration command specific to the NDR551.
#
class nbddc551(_jsonCommandBase):
    mnemonic = "nbddc"
    queryParamMap = {
                configKeys.INDEX: "id",
                configKeys.DDC_RF_INDEX: "rfch",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_CIC0: "cic0",
                configKeys.DDC_CIC1: "cic1",
                configKeys.DDC_RATE_INDEX: "filter",
                configKeys.DDC_OVERSAMPLING: "ovs",
                configKeys.DDC_DEMOD_TYPE: "demod",
                configKeys.DDC_DEMOD_GAIN: "dmdgain",
                #configKeys.DDC_AUDIO_DECIMATION: "audiodec",
                configKeys.DDC_AUDIO_DECIMATION: "audio",
                configKeys.DDC_BEAT_FREQ_OSC: "bfo",
                configKeys.ENABLE: "enable",
                configKeys.DDC_START_TIME: "start",
                configKeys.DDC_SAMPLES: "samples",
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
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_CIC0: "cic0",
                configKeys.DDC_CIC1: "cic1",
                configKeys.DDC_RATE_INDEX: "filter",
                configKeys.DDC_OVERSAMPLING: "ovs",
                configKeys.DDC_DEMOD_TYPE: "demod",
                configKeys.DDC_DEMOD_GAIN: "dmdgain",
                #configKeys.DDC_AUDIO_DECIMATION: "audiodec",
                configKeys.DDC_AUDIO_DECIMATION: "audio",
                configKeys.DDC_BEAT_FREQ_OSC: "bfo",
                configKeys.ENABLE: "enable",
                configKeys.DDC_START_TIME: "start",
                configKeys.DDC_SAMPLES: "samples",
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
# DDC group configuration command specific to the NDR551.
#
# The NDR551 allows a DDC group to contain both WBDDCs and NBDDCs.
#
# \note The NDR551 ICD changed how groups work as of version 7.2.  
#     Group assignments are now handled by the individual WBDDC
#     and NBDDC configurations.
#
class gddc551(_jsonCommandBase):
    mnemonic = "gddc"
    queryParamMap = {
                configKeys.INDEX: "gddcid",
                configKeys.ENABLE: "enable",
                #configKeys.WBDDC_GROUP_MEMBERS: "wbddc",
                #configKeys.NBDDC_GROUP_MEMBERS: "nbddc",
                configKeys.DDC_START_TIME: "start",
                configKeys.DDC_SAMPLES: "samples",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_STREAM_ID: "vita",
                 }
    setParamMap = {
                configKeys.INDEX: "gddcid",
                configKeys.ENABLE: "enable",
                #configKeys.WBDDC_GROUP_MEMBERS: "wbddc",
                #configKeys.NBDDC_GROUP_MEMBERS: "nbddc",
                configKeys.DDC_START_TIME: "start",
                configKeys.DDC_SAMPLES: "samples",
                configKeys.DDC_FREQUENCY_OFFSET: "offset",
                configKeys.DDC_STREAM_ID: "vita",
                 }


##
# Status Query command specific to the NDR551.
#
class status551(_jsonCommandBase):
    mnemonic = "status"
    settable = False
    queryParamMap = {
                configKeys.VERINFO_MODEL: "model",
                configKeys.VERINFO_SN: "sn",
                configKeys.VERINFO_UNITREV: "unit",
                configKeys.VERINFO_SW: "sw",
                configKeys.STATUS_TUNERS: "tuners",
                configKeys.VERINFO_FW: "fw",
                #configKeys.VERINFO_HW: "hw",
                configKeys.STATUS_WBDDCS: "wbddcs",
                configKeys.STATUS_NBDDCS: "nbddcs",
                configKeys.STATUS_DEMODS: "demods",
                configKeys.STATUS_ERROR: "error",
                configKeys.STATUS_PRI_MAC: "pmac",
                configKeys.STATUS_AUX_MAC: "amac",
                configKeys.STATUS_FASTSCAN_MAC: "fmac",
                configKeys.STATUS_TEMP: "temp",
                configKeys.STATUS_10MHZ_REF: "cfg10m",
                configKeys.STATUS_10MHZ_REF_STATUS: "status10m",
                configKeys.STATUS_PPS_SOURCE: "cfg1pps",
                configKeys.STATUS_PPS: "status1pps",
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
                configKeys.STATUS_TUNER4_LO1: "tuner4lo1",
                configKeys.STATUS_TUNER4_LO2: "tuner4lo2",
                configKeys.STATUS_TUNER5_LO1: "tuner5lo1",
                configKeys.STATUS_TUNER5_LO2: "tuner5lo2",
                configKeys.STATUS_TUNER6_LO1: "tuner6lo1",
                configKeys.STATUS_TUNER6_LO2: "tuner6lo2",
                configKeys.STATUS_TUNER7_LO1: "tuner7lo1",
                configKeys.STATUS_TUNER7_LO2: "tuner7lo2",
                configKeys.STATUS_TUNERBRD0_ADC_CLOCK: "tunerbd0adcclk",
                configKeys.STATUS_TUNERBRD1_ADC_CLOCK: "tunerbd1adcclk",
                configKeys.STATUS_FSCI_PACKETS: "fscipackets",
                configKeys.STATUS_FPGA_TEMP: "fpgatemp",
                configKeys.STATUS_FASTSCAN_TUNES: "fstunes",
                configKeys.STATUS_FASTSCAN_LINK: "fslinkup",
                configKeys.STATUS_FASTSCAN_SEC: "fssec",
                configKeys.STATUS_FASTSCAN_SAMP: "fssamp",
                }
    
        
##
# Radio reset command specific to the NDR551.
#
class reset551(_jsonCommandBase):
    mnemonic = "cntrl"
    queryable = False
    setParamMap = {
                configKeys.RESET_TYPE: "reboot",
                }


##
# Reference mode command specific to the NDR551.
#
class ref551(_jsonCommandBase):
    mnemonic = "ref"
    queryParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                }
    setParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                }
    

##
# Gigabit Ethernet configuration command specific to the NDR551.
#
# \note Used to configure IP information with respect to the 
#    destination.
#
class e10g551(_jsonCommandBase):
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
# Data IP configuration command specific to the NDR551.
#
# \note Used to configure IP information with respect to the 
#    source.
#
class cfge10g551(_jsonCommandBase):
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
                configKeys.GIGE_MAC_ADDR: "mac",
                configKeys.GIGE_IP_ADDR: "ip",
                configKeys.GIGE_NETMASK: "netmask",
                configKeys.GIGE_SOURCE_PORT: "port",
                }
    
                        
##
# loadEnvData JSON command.
#                        
class loadEnvData551(_jsonCommandBase):
    mnemonic = "loadenv"
    timeout = 5
        
    def getCmdString(self,*args,**kwargs):
        self.logIfVerbose(str("command.py - getCmdString for loadEnvData551"))
        name = kwargs.get("name")
        fileName = kwargs.get("fileName")
        loadEnvObject = {'msg':jsonConfig.msgIdVal, 'cmd':'loadenv', 'params':{'name':name, 'filename':fileName}}
        self.logIfVerbose(str(loadEnvObject))
        jsonCmdString = json.dumps(loadEnvObject, separators=(',', ':'))
        jsonConfig.msgIdVal +=1
        self.logIfVerbose(str(jsonCmdString))    
        return jsonCmdString

    def parseResponse(self):
        if self.verbose:
            self.logIfVerbose(str("Parsing %s response"%self.mnemonic))
        loadEnvDataResult = False
        try:
            if self.query:
                if self.verbose:
                    self.logIfVerbose(str("Response is ", self.rsp))
                queryRespStringOrig = self.rsp
                queryRespString = (queryRespStringOrig.lower())
                queryRespDict = json.loads(queryRespString)
        
                if 'success' in queryRespDict:
                    loadEnvDataResult = queryRespDict['success']    
        except:
            self.responseInfo = None
            traceback.print_exc()
        self.logIfVerbose(str(loadEnvDataResult))
        self.responseInfo = loadEnvDataResult
        return loadEnvDataResult


##
# \internal
# \brief Client command class specific to the NDR551.
#
# \note The client command on the NDR551 is intended for internal
# diagnostic purposes.  It is not part of the publicly available
# ICD.
#
class cli551(_jsonCommandBase):
    mnemonic = "cli"
    queryable = False
    setParamMap = {
                "input": "input",
                }


##
# Tuner component class for the NDR551.
#
class ndr551_tuner(_tuner):
    _name = "Tuner(NDR551)"
    frqRange = (20e6,18e9)
    frqRes = 1e6
    frqUnits = 1
    attRange = (0.0,40.0)
    attRes = 1.0
    ifFilter = [3, 10, 40, 80]
    agc = False
    # The NDR551 has one tuner command that sets all tuner parameters.
    frqCmd = tuner551
    attCmd = tuner551
    tpwrCmd = None
    # Override default port
    defaultPort = 19091
    # OVERRIDE
    ##
    # The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY, 
                                  configKeys.TUNER_ATTENUATION, 
                                  configKeys.ENABLE, 
                                  configKeys.TUNER_IF_FILTER,
                                  configKeys.TUNER_FNR,
                                  configKeys.TUNER_GAIN_MODE,
                                  configKeys.TUNER_DELAY,
                                  configKeys.TUNER_AGC_SET_POINT,
                                  configKeys.TUNER_AGC_UPPER_LIMIT,
                                  configKeys.TUNER_AGC_LOWER_LIMIT,
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
        if self.frqCmd is not None:
            cDict = { "parent": self, 
                      configKeys.TUNER_INDEX: self.index,
                      "verbose": self.verbose, 
                      "logFile": self.logFile }
            for key in [configKeys.ENABLE, 
                        configKeys.TUNER_IF_FILTER,
                        configKeys.TUNER_FNR,
                        configKeys.TUNER_GAIN_MODE,
                        configKeys.TUNER_DELAY,
                        configKeys.TUNER_AGC_SET_POINT,
                        configKeys.TUNER_AGC_UPPER_LIMIT,
                        configKeys.TUNER_AGC_LOWER_LIMIT,
                        configKeys.TUNER_AGC_LOWER_LIMIT,
                        configKeys.TUNER_AGC_ATTACK_TIME,
                        configKeys.TUNER_AGC_DECAY_TIME,
                        configKeys.TUNER_AGC_ATTACK_STEP,
                        configKeys.TUNER_AGC_DECAY_STEP,
                        configKeys.TUNER_AGC_ATTACK_LIMIT,
                        configKeys.TUNER_AGC_DECAY_LIMIT,
                        ]:
                if key in confDict:
                    cDict[key] = confDict[key]
            if configKeys.TUNER_FREQUENCY in confDict:
                freqIn = float(confDict.get(configKeys.TUNER_FREQUENCY, 0)) 
                freqAdj = adjustFrequency(freqIn, self.frqRange, 
                                          self.frqRes, self.frqUnits)
                cDict[configKeys.TUNER_FREQUENCY] = freqAdj
            if configKeys.TUNER_ATTENUATION in confDict or configKeys.TUNER_RF_ATTENUATION in confDict:
                rfAttIn = float(confDict.get(configKeys.TUNER_RF_ATTENUATION, 
                                confDict.get(configKeys.TUNER_ATTENUATION, 0))) 
                rfAttAdj = adjustAttenuation(rfAttIn, self.attRange, 
                                            self.attRes, 1)
                cDict[configKeys.TUNER_ATTENUATION] = rfAttAdj
            cmd = self.frqCmd(**cDict)
            ret &= cmd.send( self.callback, )
            ret &= cmd.success
            self._addLastCommandErrorInfo(cmd)
            if ret:
                if configKeys.TUNER_FREQUENCY in confDict:
                    self.configuration[configKeys.TUNER_FREQUENCY] = freqAdj * self.frqUnits
                if configKeys.TUNER_ATTENUATION in confDict or configKeys.TUNER_RF_ATTENUATION in confDict:
                    self.configuration[configKeys.TUNER_ATTENUATION] = rfAttAdj
                    self.configuration[configKeys.TUNER_RF_ATTENUATION] = rfAttAdj
                for key in [configKeys.ENABLE, 
                            configKeys.TUNER_IF_FILTER,
                            configKeys.TUNER_FNR,
                            configKeys.TUNER_GAIN_MODE,
                            configKeys.TUNER_DELAY,
                            configKeys.TUNER_AGC_SET_POINT,
                            configKeys.TUNER_AGC_UPPER_LIMIT,
                            configKeys.TUNER_AGC_LOWER_LIMIT,
                            configKeys.TUNER_AGC_LOWER_LIMIT,
                            configKeys.TUNER_AGC_ATTACK_TIME,
                            configKeys.TUNER_AGC_DECAY_TIME,
                            configKeys.TUNER_AGC_ATTACK_STEP,
                            configKeys.TUNER_AGC_DECAY_STEP,
                            configKeys.TUNER_AGC_ATTACK_LIMIT,
                            configKeys.TUNER_AGC_DECAY_LIMIT,
                            ]:
                    if key in confDict:
                        self.configuration[key] = confDict[key]
            pass
        return ret


##
# WBDDC component class for the NDR551.
class ndr551_wbddc(_wbddc):
    _name = "WBDDC(NDR551)"
    tunable = True
    selectableSource = True
    frqRange = (-40e6,40e6,)
    frqRes = 1e3
    rateSet = { 40: 128.0e6, \
                39: 64.0e6, \
                38: 32.0e6, \
                37: 32.0e6, \
                36: 16.0e6, \
                35: 16.0e6, \
                34: 16.0e6, \
                33: 8.0e6, \
                32: 8.0e6, \
                #6: 256.0e6, \
                 }
    bwSet = { 40: 80.0e6, \
              39: 40.0e6, \
              38: 25.0e6, \
              37: 20.0e6, \
              36: 12.5e6, \
              35: 10.0e6, \
              34:  8.0e6, \
              33:  5.0e6, \
              32:  4.0e6, \
              }
    dataFormat = { 1:"iq" }
    cfgCmd = wbddc551
    frqCmd = None
    nbssCmd = None
    # OVERRIDE
    validConfigurationKeywords = [
                                configKeys.DDC_RF_INDEX,
                                configKeys.DDC_OUTPUT_TYPE,
                                configKeys.DDC_FREQUENCY_OFFSET,
                                configKeys.DDC_DECIMATION,                               
                                configKeys.DDC_RATE_INDEX,
                                configKeys.DDC_OVERSAMPLING,
                                configKeys.ENABLE,
                                configKeys.DDC_START_TIME,
                                configKeys.DDC_SAMPLES,
                                configKeys.DDC_GROUP_ID,
                                configKeys.DDC_STREAM_ID,
                                configKeys.DDC_LINK,
                                configKeys.DDC_UDP_DESTINATION,
                                configKeys.DDC_GAIN,
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
                    if rspInfo.has_key(key):
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
# NBDDC component class for the NDR551.
class ndr551_nbddc(_nbddc):
    _name = "NBDDC(NDR551)"
    tunable = True
    selectableSource = True
    frqRange = (-40e6,40e6)
    frqRes = 1
    rateSet = {     
                    #~ 16: 2.0e6, 
                    15: 4.0e6, 
                    14: 3.2e6, 
                    13: 1.28e6, 
                    12: 400e3, 
                    11: 256e3, 
                    10: 200e3, 
                    9: 128e3, 
                    8: 64e3, 
                    7: 32e3, 
                    6: 16e3, 
                    5: 8.0e3, 
                    4: 4.0e3, 
                    3: 2.0e3, 
                    2: 1.0e3, 
                    1: 0.5e3, 
                    0: 0.25e3, 
            }
    bwSet = {       
                    #~ 16: 1.5e6, 
                    15:  3.2e6, 
                    14:  2.5e6, 
                    13:  1.0e6, 
                    12:  300e3, 
                    11:  200e3, 
                    10:  150e3, 
                    9:  100e3, 
                    8:   50e3, 
                    7:   25e3, 
                    6: 12.5e3, 
                    5: 6.4e3, 
                    4: 3.2e3, 
                    3: 1.6e3, 
                    2: 0.8e3, 
                    1: 0.4e3, 
                    0: 0.2e3, 
            }
    dataFormat = { 1:"iq" }
    cfgCmd = nbddc551
    frqCmd = None
    nbssCmd = None
    # OVERRIDE
    validConfigurationKeywords = [
                                configKeys.DDC_RF_INDEX,
                                configKeys.DDC_FREQUENCY_OFFSET,
                                configKeys.DDC_CIC0,
                                configKeys.DDC_CIC1,
                                configKeys.DDC_RATE_INDEX,
                                configKeys.DDC_OVERSAMPLING,
                                configKeys.DDC_DEMOD_TYPE,
                                configKeys.DDC_DEMOD_GAIN,
                                configKeys.DDC_AUDIO_DECIMATION,
                                configKeys.DDC_BEAT_FREQ_OSC,
                                configKeys.ENABLE,
                                configKeys.DDC_START_TIME,
                                configKeys.DDC_SAMPLES,
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
                    if rspInfo.has_key(key):
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
# Combined DDC group component for the NDR551.
#
class ndr551_ddc_group(ddc_group):
    _name = "DDCGroup(NDR551)"
    groupMemberIndexBase = 0
    numGroupMembers = 16
    #groupMemberCmd = gddc551
    groupMemberCmd = None
    groupEnableCmd = gddc551

    # OVERRIDE
    ##
    # The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [
                                  configKeys.ENABLE, 
                                  #configKeys.WBDDC_GROUP_MEMBERS,
                                  #configKeys.NBDDC_GROUP_MEMBERS,
                                  configKeys.DDC_START_TIME,
                                  configKeys.DDC_SAMPLES,
                                  configKeys.DDC_FREQUENCY_OFFSET,
                                  configKeys.DDC_STREAM_ID,
                                  ]
    
    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    #
    # Overrides the base-class method because the 551 uses a single command to 
    # query all group members and whether the group is enabled. 
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # Override
#         if self.groupMemberCmd is not None:
#             cmd = self.groupMemberCmd(**{ "parent": self, 
        if self.groupEnableCmd is not None:
            cmd = self.groupEnableCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.configuration[configKeys.ENABLE] = rspInfo.get(configKeys.ENABLE, False)
                #self.configuration[configKeys.WBDDC_GROUP_MEMBERS] = rspInfo.get(configKeys.WBDDC_GROUP_MEMBERS, [])
                #self.configuration[configKeys.NBDDC_GROUP_MEMBERS] = rspInfo.get(configKeys.NBDDC_GROUP_MEMBERS, [])
                self.configuration[configKeys.DDC_START_TIME] = rspInfo.get(configKeys.DDC_START_TIME, False)
                self.configuration[configKeys.DDC_SAMPLES] = rspInfo.get(configKeys.DDC_SAMPLES, 0)
                self.configuration[configKeys.DDC_FREQUENCY_OFFSET] = rspInfo.get(configKeys.DDC_FREQUENCY_OFFSET, 0)
                self.configuration[configKeys.DDC_STREAM_ID] = rspInfo.get(configKeys.DDC_STREAM_ID, 0)
        pass

    # OVERRIDE
    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.  
    #
    # Overrides the base-class method because the 364 uses a single command to 
    # set all group members and enable/disable the group. 
    def _setConfiguration(self, confDict):
        ret = True
#         self.logIfVerbose("[ndr551_ddc_group][%d][_setConfiguration()]" % self.index, 
#                           "confDict = %s" % str(confDict))
#        if self.groupMemberCmd is not None:
        if self.groupEnableCmd is not None:
            cDict = { "parent": self, 
                      configKeys.INDEX: self.index,
                      "verbose": self.verbose, 
                      "logFile": self.logFile }
#             if configKeys.WBDDC_GROUP_MEMBERS in confDict:
#                 wmembers = []
#                 if confDict[configKeys.WBDDC_GROUP_MEMBERS] is None:
#                     wmembers = []
#                 elif isinstance(confDict[configKeys.WBDDC_GROUP_MEMBERS], int):
#                     wmembers = [confDict[configKeys.WBDDC_GROUP_MEMBERS]]
#                 else:
#                     wmembers = confDict[configKeys.WBDDC_GROUP_MEMBERS]
#                 cDict[configKeys.WBDDC_GROUP_MEMBERS] = wmembers
#             if configKeys.NBDDC_GROUP_MEMBERS in confDict:
#                 nmembers = []
#                 if confDict[configKeys.NBDDC_GROUP_MEMBERS] is None:
#                     nmembers = []
#                 elif isinstance(confDict[configKeys.NBDDC_GROUP_MEMBERS], int):
#                     nmembers = [confDict[configKeys.NBDDC_GROUP_MEMBERS]]
#                 else:
#                     nmembers = confDict[configKeys.NBDDC_GROUP_MEMBERS]
#                 cDict[configKeys.NBDDC_GROUP_MEMBERS] = nmembers
            if configKeys.ENABLE in confDict:
                cDict[configKeys.ENABLE] = confDict[configKeys.ENABLE]
#             self.logIfVerbose("[ndr551_ddc_group][%d][_setConfiguration()]" % self.index, 
#                               "cDict = %s" % str(cDict))
            if configKeys.DDC_START_TIME in confDict:
                cDict[configKeys.DDC_START_TIME] = confDict[configKeys.DDC_START_TIME]
            if configKeys.DDC_SAMPLES in confDict:
                cDict[configKeys.DDC_SAMPLES] = confDict[configKeys.DDC_SAMPLES]
            if configKeys.DDC_FREQUENCY_OFFSET in confDict:
                cDict[configKeys.DDC_FREQUENCY_OFFSET] = confDict[configKeys.DDC_FREQUENCY_OFFSET]
            if configKeys.DDC_STREAM_ID in confDict:
                cDict[configKeys.DDC_STREAM_ID] = confDict[configKeys.DDC_STREAM_ID]
            #cmd = self.groupMemberCmd(**cDict)
            cmd = self.groupEnableCmd(**cDict)
            ret &= cmd.send( self.callback, )
            ret &= cmd.success
            self._addLastCommandErrorInfo(cmd)
            if ret:
#                 if configKeys.WBDDC_GROUP_MEMBERS in confDict:
#                     self.configuration[configKeys.WBDDC_GROUP_MEMBERS] = wmembers
#                 if configKeys.NBDDC_GROUP_MEMBERS in confDict:
#                     self.configuration[configKeys.NBDDC_GROUP_MEMBERS] = nmembers
                if configKeys.ENABLE in confDict:
                    self.configuration[configKeys.ENABLE] = confDict[configKeys.ENABLE]
                if configKeys.DDC_START_TIME in confDict:
                    self.configuration[configKeys.DDC_START_TIME] = confDict[configKeys.DDC_START_TIME]
                if configKeys.DDC_SAMPLES in confDict:
                    self.configuration[configKeys.DDC_SAMPLES] = confDict[configKeys.DDC_SAMPLES]
                if configKeys.DDC_FREQUENCY_OFFSET in confDict:
                    self.configuration[configKeys.DDC_FREQUENCY_OFFSET] = confDict[configKeys.DDC_FREQUENCY_OFFSET]
                if configKeys.DDC_STREAM_ID in confDict:
                    self.configuration[configKeys.DDC_STREAM_ID] = confDict[configKeys.DDC_STREAM_ID]
            pass
        return ret


##
# \internal
# \brief VITA 49 interface specification class for the NDR551's DDC format.
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
class ndr551_ddc_ifSpec(_ifSpec):
    headerSizeWords = 12 
    payloadSizeWords = 1024
    tailSizeWords = 2
    byteOrder = "big"


##
# \internal
# \brief VITA 49 interface specification class for NDR551's ADC format.
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
class ndr551_adc_ifSpec(_ifSpec):
    headerSizeWords = 12 
    payloadSizeWords = 1024
    tailSizeWords = 2
    byteOrder = "big"


##
# \internal
# \brief VITA 49 interface specification class for the NDR551's demod format.
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
class ndr551_demod_ifSpec(_ifSpec):
    headerSizeWords = 12
    payloadSizeWords = 128
    tailSizeWords = 2
    byteOrder = "big"


##
# \brief Radio handler class for the NDR551.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR551 Connection Modes
#
# "udp"
#
# \section RadioConfig_NDR551 Radio Configuration Options
#
# \code
# configDict = {
#      "referenceMode": [0, 1],
#      "function": [integer (meaning is radio-dependent],
#      "tunerConfiguration": {
#            0: {
#               "preselectorBypass": [True, False], 
#               "frequency": [20000000.0-18000000000.0, step 1000000.0],
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
#         ...3 (repeat for each tuner)
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
#           ...3 (repeat for each WBDDC)
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
# \section VITA_Notes_NDR551 VITA 49 Notes
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
class ndr551(_radio):
    _name = "NDR551"
    ifSpec = ndr551_ddc_ifSpec
    ifSpecMap = {
            "ddc":   ndr551_ddc_ifSpec,
            "adc":   ndr551_adc_ifSpec,
            "demod": ndr551_demod_ifSpec,
        }
    json = True
    adcRate = 256e6
    numTuner = 4
    numWbddc = 4
    tunerType = ndr551_tuner
    tunerIndexBase = 0
    wbddcType = ndr551_wbddc
    wbddcIndexBase = 0
    numNbddc = 64
    nbddcType = ndr551_nbddc
    nbddcIndexBase = 0
    numCddcGroups = 16
    cddcGroupIndexBase = 0
    cddcGroupType = ndr551_ddc_group
    numGigE = 4
    gigEIndexBase = 0
    numGigEDipEntries = 64
    gigEDipEntryIndexBase = 0
    idnQry = None
    verQry = None
    hrevQry = None
    statQry = status551
    cfgCmd = None
    refCmd = ref551
    rbypCmd = None
    sipCmd = cfge10g551
    dipCmd = e10g551
    smacCmd = None
    dmacCmd = None
    calfCmd = None
    resetCmd = reset551
    funCmd = funJSON
    refModes = {0:"Internal 10MHz",1:"External 10MHz"}
    ppsModes = {0:"Internal 1PPS", 1:"External 1PPS"}
    rbypModes = {}
    connectionModes = ["udp"]
    defaultPort = 19091
    udpDestInfo = "Destination index"

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
        if not all([self.versionInfo.has_key(key) for key in keys]):
            cmd = self.statQry(parent=self, 
                               query=True,
                               verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self._dictUpdate(self.versionInfo, rspInfo, {}, keys)
        for key in keys:
            if not self.versionInfo.has_key(key):
                self.versionInfo[key] = "N/A"
        return self.versionInfo

    # OVERRIDE
    ##
    # \brief Sets DDC configuration (old-style).
    #
    # \deprecated Use setConfiguration() instead.
    #
    def setDdcConfiguration(self, wideband, ddcIndex=None, enable=False, rfch=0,
                            ddctype="iq", offset=0, decimation=1, 
                             cic0=8, cic1=1, ddcfilter=64, ovs=1, gain=0, vita=0, link=0, 
                             destination=0):
        success = True
        ddcDict = self.wbddcDict if wideband else self.nbddcDict
        for i in self._getIndexList(ddcIndex,ddcDict):
            success &= ddcDict[i].setConfiguration( **{ 
                                                        configKeys.INDEX: i,
                                                        configKeys.ENABLE: enable,
                                                        configKeys.DDC_RF_INDEX: rfch,
                                                        configKeys.DDC_OUTPUT_TYPE: ddctype,
                                                        configKeys.DDC_FREQUENCY_OFFSET: offset,
                                                        configKeys.DDC_DECIMATION: decimation,
                                                        configKeys.DDC_CIC0: cic0,
                                                        configKeys.DDC_CIC1: cic1,
                                                        configKeys.DDC_RATE_INDEX: ddcfilter,
                                                        #configKeys.DDC_FILTER_INDEX: ddcfilter,
                                                        configKeys.DDC_OVERSAMPLING: ovs,
                                                        configKeys.DDC_GAIN: gain,
                                                        configKeys.DDC_STREAM_ID: vita,
                                                        configKeys.DDC_LINK: link,
                                                        configKeys.DDC_UDP_DESTINATION: destination,
                                                        } )
        return success

    ##
    # \internal
    # \brief Sends a client command to the radio.
    #
    # \note The client command on the NDR551 is intended for internal
    # diagnostic purposes.  It is not part of the publcly available
    # ICD.
    #
    # \param cmdString The client command string to send.
    # \returns A 2-tuple: (success flag, command result string).
    #
    def sendCliInput(self, cmdString):
        cmd = cli551(parent=self, 
                     query=False,
                     input=cmdString,
                     verbose=self.verbose, logFile=self.logFile)
        cmd.send( self.sendCommand, )
        self._addLastCommandErrorInfo(cmd)
        rspInfo = cmd.getResponseInfo()
        return cmd.success, rspInfo

    

if __name__ == '__main__':
    pass
