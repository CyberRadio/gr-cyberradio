##################################################################
# \package CyberRadioDriver.radios.ndr511
# \brief NDR511 Support
# \author BS
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#     All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _jsonCommandBase, jsonConfig
from CyberRadioDriver.components import _tuner, adjustFrequency, adjustAttenuation
from CyberRadioDriver.radio import _ifSpec, _radio, funJSON

# Imports from external modules
# Python standard library imports
import json
import math
import time, datetime
import traceback



class tuner511(_jsonCommandBase):
    mnemonic = "tuner"
    queryParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_BAND: "band",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.ENABLE: "enable"
                }
    setParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_BAND: "band",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.ENABLE: "enable"
                }
##
# Status Query command specific to the NDR551.
#
class status511(_jsonCommandBase):
    mnemonic = "status"
    settable = False
    queryParamMap = {
                configKeys.VERINFO_MODEL: "model",
                configKeys.VERINFO_SN: "sn",
                configKeys.VERINFO_UNITREV: "unit",
                configKeys.VERINFO_SW: "sw",
                configKeys.STATUS_TUNERS: "tuners",
                configKeys.VERINFO_FW: "fw",
                configKeys.STATUS_ERROR: "error",
                configKeys.STATUS_PRI_MAC: "pmac",
                configKeys.STATUS_TEMP: "temp",
                configKeys.STATUS_10MHZ_REF: "cfg10m",
                configKeys.STATUS_10MHZ_REF_STATUS: "status10m",
                configKeys.STATUS_ONTIME: "ontime",
                configKeys.STATUS_MEM: "mem",
                configKeys.STATUS_LINK0: "link0up",
                configKeys.STATUS_TUNER0_LO1: "ch1lo",
                configKeys.STATUS_TUNER1_LO1: "ch2lo",
                configKeys.STATUS_FPGA_TEMP: "fpgatemp",
                }
    
##
# Reference mode command specific to the NDR562.
#
class ref511(_jsonCommandBase):
    mnemonic = "ref"
    queryParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m"
                }
    setParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m"
                }

##
# \brief Tuner component class for the NDR562.
#

class ndr511_tuner(_tuner):
    _name = "Tuner(NDR511)"
    frqRange = (17e9,42e9)
    frqRes = 10e6
    attRange = (0.0,40.0)
    attRes = 1.0
    frqCmd = tuner511
    attCmd = tuner511
    agc = False
    defaultPort = 19091

    validConfigurationKeywords = [
                                  configKeys.TUNER_BAND, 
                                  configKeys.TUNER_ATTENUATION, 
                                  configKeys.ENABLE,
                                  configKeys.TUNER_FNR,
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
                        configKeys.TUNER_FNR,
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
                            configKeys.TUNER_FNR,
                            ]:
                    if key in confDict:
                        self.configuration[key] = confDict[key]
            pass
        return ret

##
# \brief Radio handler class for the NDR562.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR562_2 Connection Modes
#
# "udp"
#
# \section RadioConfig_NDR562_2 Radio Configuration Options
#
# \code
# configDict = {
#      "referenceMode": [0, 1],
#      "tunerConfiguration": {
#            0: {
#               "band": [0-5],
#               "attenuation": [0.0-40.0, step 0.5],
#               "enable": [True, False],
#            },
#            1: {
#               "band": [0-5],
#               "attenuation": [0.0-40.0, step 0.5],
#               "enable": [True, False],
#            }
#      },
# }
# \endcode
#
# \implements CyberRadioDriver.IRadio                    
class ndr511(_radio):
    _name = "NDR511"
    json = True
    ifSpec = None
    ifSpecMap = {}
    tunerType = ndr511_tuner
    wbddcType = None
    nbddcType = None
    cddcGroupType = None
    statQry = status511
    refCmd = ref511
    sipCmd = None
    dipCmd = None
    numGigE = 0
    numTuner = 2
    numNbddc = 0
    numWbddc = 0
    numCddcGroups = 0
    connectionModes = ["udp"]
    defaultPort = 19091

    idnQry = None
    verQry = None
    hrevQry = None
    cfgCmd = None
    rbypCmd = None
    sipCmd = None
    dipCmd = None
    smacCmd = None
    dmacCmd = None
    calfCmd = None


    refModes = {0:"Internal 10MHz",1:"External 10MHz"}
    ##
    # \brief The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [configKeys.REFERENCE_MODE]
    
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


if __name__ == '__main__':
    pass
