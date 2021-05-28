#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr559 
# \brief NDR559 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _jsonCommandBase
from CyberRadioDriver.components import _tuner, \
                                        adjustFrequency, adjustAttenuation
from CyberRadioDriver.radio import _radio
# Imports from external modules
# Python standard library imports


class tuner559(_jsonCommandBase):
    mnemonic = "tuner"
    queryParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_IF_FILTER: "if",
                configKeys.TUNER_FNR: "fnr",
                configKeys.ENABLE: "enable",
                }
    setParamMap = {
                configKeys.TUNER_INDEX: "id",
                configKeys.TUNER_FREQUENCY: "freq",
                configKeys.TUNER_ATTENUATION: "atten",
                configKeys.TUNER_IF_FILTER: "if",
                configKeys.TUNER_FNR: "fnr",
                configKeys.ENABLE: "enable",
                }
    
                        
##
# Status Query command specific to the NDR559.
#
class status559(_jsonCommandBase):
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
                configKeys.STATUS_AUX_MAC: "amac",
                configKeys.STATUS_TEMP: "temp",
                configKeys.STATUS_10MHZ_REF: "cfg10m",
                configKeys.STATUS_10MHZ_REF_STATUS: "status10m",
                configKeys.STATUS_ONTIME: "ontime",
                configKeys.STATUS_MEM: "mem",
                configKeys.STATUS_TUNER0_LO1: "tuner0lo1",
                configKeys.STATUS_TUNER1_LO1: "tuner1lo1",
                configKeys.STATUS_MW0_LO1: "mw0lo1",
                configKeys.STATUS_MW1_LO1: "mw1lo1",
                configKeys.STATUS_MW_LO2: "mwlo2",
                }
    
        
##
# Radio reset command specific to the NDR559.
#
class reset559(_jsonCommandBase):
    mnemonic = "cntrl"
    queryable = False
    setParamMap = {
                configKeys.RESET_TYPE: "reboot",
                }


##
# Reference mode command specific to the NDR559.
#
class ref559(_jsonCommandBase):
    mnemonic = "ref"
    queryParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                }
    setParamMap = {
                configKeys.REFERENCE_MODE: "cfg10m",
                }
    

##
# \internal
# \brief Client command class specific to the NDR559.
#
# \note The client command on the NDR559 is intended for internal
# diagnostic purposes.  It is not part of the publicly available
# ICD.
#
class cli559(_jsonCommandBase):
    mnemonic = "input"
    queryable = False
    setParamMap = {
                "input": "input",
                }


##
# Tuner component class for the NDR559.
#
class ndr559_tuner(_tuner):
    _name = "Tuner(NDR559)"
    frqRange = (6e9,18e9)
    frqRes = 1e6
    frqUnits = 1
    attRange = (0.0,40.0)
    attRes = 1.0
    agc = False
    # The NDR559 has one tuner command that sets all tuner parameters.
    frqCmd = tuner559
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
                                  configKeys.TUNER_IF_FILTER,
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
                        configKeys.TUNER_IF_FILTER,
                        configKeys.TUNER_FNR]:
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
                            configKeys.TUNER_FNR]:
                    if key in confDict:
                        self.configuration[key] = confDict[key]
            pass
        return ret


##
# \brief Radio handler class for the NDR559.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR559 Connection Modes
#
# "udp"
#
# \section RadioConfig_NDR559 Radio Configuration Options
#
# \code
# configDict = {
#      "referenceMode": [0, 1],
#      "tunerConfiguration": {
#            0: {
#               "frequency": [6000000000.0-18000000000.0, step 1000000.0],
#               "attenuation": [0.0-40.0, step 1.0],
#               "enable": [True, False],
#               "ifFilter": [125, 200, 300, 500, "lpf", "bypass"],
#               "fnr": [True, False],
#            },
#         ...1 (repeat for each tuner)
#      },
# }
# \endcode
#
# \implements CyberRadioDriver.IRadio    
class ndr559(_radio):
    _name = "NDR559"
    ifSpec = None
    json = True
    numTuner = 2
    numWbddc = 0
    tunerType = ndr559_tuner
    tunerIndexBase = 0
    numNbddc = 0
    numCddcGroups = 0
    numGigE = 0
    idnQry = None
    verQry = None
    hrevQry = None
    statQry = status559
    cfgCmd = None
    refCmd = ref559
    rbypCmd = None
    sipCmd = None
    dipCmd = None
    smacCmd = None
    dmacCmd = None
    calfCmd = None
    resetCmd = reset559
    refModes = {0:"Internal 10MHz",1:"External 10MHz"}
    rbypModes = {}
    connectionModes = ["udp"]
    defaultPort = 19091
    udpDestInfo = "N/A (no digital outputs)"

    # OVERRIDE
    validConfigurationKeywords = []
    
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

    # OVERRIDE
    ##
    # \protected
    # \brief Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # This radio has nothing further that it can configure

    # OVERRIDE
    ##
    # \brief Sets DDC configuration (old-style).
    #
    # \note This radio has no DDCs, so this method always returns False.
    #
    # \deprecated Use setConfiguration() instead.
    #
    def setDdcConfiguration(self, wideband, ddcIndex=None, rfIndex=1, 
                            rateIndex=0, udpDest=0, frequency=0, enable=0, 
                            vitaEnable=0, streamId=0):
        success = False
        return success

    ##
    # \internal
    # \brief Sends a client command to the radio.
    #
    # \note The client command on the NDR559 is intended for internal
    # diagnostic purposes.  It is not part of the publcly available
    # ICD.
    #
    # \param cmdString The client command string to send.
    # \returns A 2-tuple: (success flag, command result string).
    #
    def sendCliInput(self, cmdString):
        cmd = cli559(parent=self, 
                     query=False,
                     input=cmdString,
                     verbose=self.verbose, logFile=self.logFile)
        cmd.send( self.sendCommand, )
        self._addLastCommandErrorInfo(cmd)
        rspInfo = cmd.getResponseInfo()
        return cmd.success, rspInfo



if __name__ == '__main__':
    pass
