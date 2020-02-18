#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr301ptt 
# \brief NDR301PTT Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2018 CyberRadio Solutions, Inc.  
#     All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import nbddc, wbdp, nbdp, maybeHex, wbss
from CyberRadioDriver.components import adjustFrequency, DDC_DATA_FORMAT
from CyberRadioDriver.radio import _radio
from CyberRadioDriver.radios.ndr301 import ndr301, \
                                           ndr301_wbddc, \
                                           ndr301_nbddc
# Imports from external modules
# Python standard library imports


class ddc301ptt(nbddc):
    mnemonic = "DDC"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.DDC_RF_INDEX,        int,    False,    1        ), \
                        (configKeys.DDC_FREQUENCY_OFFSET,int,    False,    0        ), \
                        (configKeys.DDC_RATE_INDEX,        int,    False,    0        ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False,    0        ), \
                        (configKeys.ENABLE,                int,    False,    0        ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False,    0        ), \
                        (configKeys.DDC_STREAM_ID,         int,    False,    0        ), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX,                 int,    False    ), \
                        (configKeys.DDC_RF_INDEX,     int,    False    ), \
                        (configKeys.DDC_FREQUENCY_OFFSET,int,    False    ), \
                        (configKeys.DDC_RATE_INDEX,        int,    False    ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False    ), \
                        (configKeys.ENABLE,                int,    False    ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False    ), \
                        (configKeys.DDC_STREAM_ID,        int,    False    ), \
                        ]


class wbsc301ptt(nbddc):
    mnemonic = "WBSC"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False,    0        ), \
                        # (configKeys.DDC_SPECTRAL_AVERAGE_ALPHA,    int,    True,    0), \
                        (configKeys.DDC_RF_INDEX,    int,    True,    1), \
                        (configKeys.DDC_SPECTRAL_FRAME_RATE,    int,    False,    0), \
                        (configKeys.ENABLE,                int,    False,    0        ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False,    0        ), \
                        (configKeys.DDC_STREAM_ID,         int,    False,    0        ), \
                        ]
    queryParameters = [ (configKeys.INDEX,    int,    True,    None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX,                 int,    False    ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False    ), \
                        # (configKeys.DDC_SPECTRAL_AVERAGE_ALPHA,    int,    False,    0), \
                        (configKeys.DDC_RF_INDEX,    int,    False, 1    ), \
                        (configKeys.DDC_SPECTRAL_FRAME_RATE,    int,    False,    ), \
                        (configKeys.ENABLE,                int,    False    ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False    ), \
                        (configKeys.DDC_STREAM_ID,        maybeHex,    False    ), \
#                         (configKeys.DDC_RATE_INDEX,        int,    False    ), \
                        ]


# NBDDC component class for the NDR301PTT.
class ndr301ptt_nbddc(ndr301_nbddc):
    _name = "NBDDC(NDR301PTT)"
    # OVERRIDE
    selectableSource = True
    # OVERRIDE
    nbssCmd = None
    frqRange = (-30.72e6, 30.72e6,)
    cfgCmd = ddc301ptt
    frqCmd = None
    demodCmd = None
    otherCmdList = [ ]
    rateSet = {  0: 60e3, 
                 1: 36e3, 
                 2: 24e3, 
                }
    bwSet   = {  0: 48.0e3, 
                 1: 28.8e3, 
                 2: 19.2e3, 
                 }
    validConfigurationKeywords = [
                                    configKeys.DDC_RF_INDEX, 
                                    configKeys.DDC_FREQUENCY_OFFSET, 
                                    configKeys.DDC_RATE_INDEX, 
                                    configKeys.DDC_OUTPUT_FORMAT, 
                                    configKeys.DDC_UDP_DESTINATION, 
                                    configKeys.ENABLE, 
                                    configKeys.DDC_STREAM_ID, 
                                    configKeys.DDC_DATA_PORT, 
                                  ]
    # # OVERRIDE
    # ##
    # # \protected
    # # Queries hardware to determine the object's current configuration.  
    # def _queryConfiguration(self):
    #     for cmdObj in [self.nbssCmd,self.dportCmd,self.cfgCmd,self.demodCmd]+self.otherCmdList:
    #         if cmdObj is not None:
    #             cmd = cmdObj(**{ "parent": self, 
    #                                configKeys.INDEX: self.index,
    #                                "query": True,
    #                                 "verbose": self.verbose, 
    #                                 "logFile": self.logFile })
    #             cmd.send( self.callback, )
    #             self._addLastCommandErrorInfo(cmd)
    #             rspInfo = cmd.getResponseInfo()
    #             keys = [i[0] for i in cmdObj.queryResponseData if \
    #                     i[0] != configKeys.INDEX]
    #             if rspInfo is not None:
    #                 for key in keys:
    #                     self.configuration[key] = rspInfo.get(key, None)
    #     pass
    
    # # OVERRIDE
    # ##
    # # \protected
    # # Sets the component's current configuration.  
    # def _setConfiguration(self, confDict):
    #     ret = True
    #     if confDict.has_key(configKeys.DDC_FREQUENCY_OFFSET):
    #         confDict[configKeys.DDC_FREQUENCY_OFFSET] = adjustFrequency(
    #                               float(confDict[configKeys.DDC_FREQUENCY_OFFSET]), 
    #                               self.frqRange, 
    #                               self.frqRes, 
    #                               self.frqUnits)
    #     for cmdObj in [self.nbssCmd, 
    #                     self.dportCmd, 
    #                     self.cfgCmd, 
    #                     self.demodCmd, f
    #                     ]+self.otherCmdList:
    #         if cmdObj is not None:
    #             keys = [ i[0] for i in cmdObj.setParameters ]
    #             if any([q in confDict for q in keys]):
    #                 cDict = {}
    #                 self._dictUpdate(cDict, confDict, self.configuration, keys)
    #                 cDict.update({ "parent": self, 
    #                                 configKeys.INDEX: self.index,
    #                                  "verbose": self.verbose, 
    #                                  "logFile": self.logFile })
    #                 cmd = cmdObj(**cDict)
    #                 ret &= cmd.send( self.callback, )
    #                 ret &= cmd.success
    #                 self._addLastCommandErrorInfo(cmd)
    #                 if ret:
    #                     for key in keys:
    #                         self.configuration[key] = getattr(cmd, key)
    #                 pass
    #     return ret

    ##
    # \brief Update sets for this component, based on ADC sample rate.
    #
    # Used for radios which allow the ADC sample rate to be changed.
    #
    def updateSets(self):
        pass


# WBDDC component class for the NDR301PTT.
class ndr301ptt_wbddc(ndr301_wbddc):
    _name = "WidebandChannel(NDR301PTT)"
    selectableSource = True
    # nbssCmd = wbss
    cfgCmd = wbsc301ptt
    dportCmd = wbdp
    demodCmd = None
    otherCmdList = []
    validConfigurationKeywords = [
        configKeys.DDC_OUTPUT_FORMAT,
        configKeys.DDC_SPECTRAL_FRAME_RATE,
        configKeys.ENABLE, 
        configKeys.DDC_UDP_DESTINATION, 
        configKeys.DDC_STREAM_ID, 
        configKeys.DDC_DATA_PORT,
        configKeys.DDC_RF_INDEX, 
     ]
    rateSet = {
        0: 0.0, 
        1: 122.88e6/2, 
        2: 122.88e6/4, 
        3: 122.88e6/8, 
        4: 122.88e6/16, 
        5: 122.88e6/32, 
        6: 122.88e6, 
    }
    bwSet = {
        0: 40.0e6, 
        1: 40.0e6, 
        2: 20.0e6, 
        3: 10.0e6, 
        4:  5.0e6, 
        5:  2.5e6, 
        6: 40.0e6, 
    }
    dataFormat = {
        0: DDC_DATA_FORMAT.FFT, 
        6: DDC_DATA_FORMAT.REAL, 
    }


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
                for key in [configKeys.DDC_UDP_DESTINATION,
                            configKeys.ENABLE,
                            configKeys.DDC_STREAM_ID,
                            configKeys.DDC_OUTPUT_FORMAT,
                            configKeys.DDC_SPECTRAL_FRAME_RATE]:
                    self.configuration[key] = rspInfo.get(key, None)
        # if self.nbssCmd is not None:
        #     cmd = self.nbssCmd(**{ "parent": self, 
        #                            configKeys.INDEX: self.index,
        #                            "query": True,
        #                             "verbose": self.verbose, 
        #                             "logFile": self.logFile })
        #     cmd.send( self.callback, )
        #     self._addLastCommandErrorInfo(cmd)
        #     rspInfo = cmd.getResponseInfo()
        #     #self.logIfVerbose("rspInfo =", rspInfo)
        #     if rspInfo is not None:
        #         for key in [configKeys.DDC_RF_INDEX, 
        #                     ]:
        #             self.configuration[key] = rspInfo.get(key, None)
        if self.dportCmd is not None:
            cmd = self.dportCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            #self.logIfVerbose("rspInfo =", rspInfo)
            if rspInfo is not None:
                for key in [configKeys.DDC_DATA_PORT, 
                            ]:
                    self.configuration[key] = rspInfo.get(key, None)
        pass

    # OVERRIDE
    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.  
    def _setConfiguration(self, confDict):
        ret = True
        if self.dportCmd is not None and \
           configKeys.DDC_DATA_PORT in confDict:
            cDict = {}
            self._dictUpdate(cDict, confDict, self.configuration, 
                             [configKeys.DDC_DATA_PORT])
            cDict.update({ "parent": self, 
                            configKeys.INDEX: self.index,
                            "verbose": self.verbose, 
                            "logFile": self.logFile, })
            cmd = self.dportCmd(**cDict)
            ret &= cmd.send( self.callback, )
            ret &= cmd.success
            self._addLastCommandErrorInfo(cmd)
            if ret:
                self.configuration[configKeys.DDC_DATA_PORT] = getattr(cmd, configKeys.DDC_DATA_PORT)
            pass
        
        # if (self.nbssCmd is not None) and (configKeys.DDC_RF_INDEX in confDict):
        #     cDict = {}
        #     self._dictUpdate(cDict, confDict, self.configuration, [configKeys.DDC_RF_INDEX,])
        #     cDict.update({ "parent": self, 
        #                     configKeys.INDEX: self.index,
        #                      "verbose": self.verbose, 
        #                      "logFile": self.logFile })
        #     cmd = self.nbssCmd(**cDict)
        #     ret &= cmd.send( self.callback, )
        #     ret &= cmd.success
        #     self._addLastCommandErrorInfo(cmd)
        #     if ret:
        #         self.configuration[configKeys.DDC_RF_INDEX] = getattr(cmd, configKeys.DDC_RF_INDEX)

        keys = [configKeys.ENABLE,
                configKeys.DDC_UDP_DESTINATION, 
                configKeys.DDC_STREAM_ID,
                configKeys.DDC_OUTPUT_FORMAT,
                configKeys.DDC_SPECTRAL_FRAME_RATE,
                configKeys.DDC_RF_INDEX, 
                 ]
        if any([q in confDict for q in keys]):
            if self.cfgCmd is not None:
                cDict = {}
                self._dictUpdate(cDict, confDict, self.configuration, keys)
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
                        self.configuration[key] = getattr(cmd, key)
                pass
        return ret

    ##
    # \brief Update sets for this component, based on ADC sample rate.
    #
    # Used for radios which allow the ADC sample rate to be changed.
    #
    def updateSets(self):
        pass


##
# \brief Radio handler class for the NDR301PTT.
#
# The NDR301PTT allows users to use either a TCP link or a serial link for its 
# command and control communications.  The TCP link uses a different port number 
# than the NDR308-class radios use (10301 rather than 8617).
#
# The NDR301PTT also provides both 1 Gig and 10 Gig data outputs.  However, 
# the 301's command set treats the 1 Gig and 10 Gig interfaces identically.
# For driver purposes, the 1 Gig interface is treated as a 10 Gig interface with
# index 1.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR301PTT Connection Modes
#
# "tcp", "tty"
#
# \section RadioConfig_NDR301PTT Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4, 5],
#      "freqNormalization": [0, 1],
#      "referenceTuningVoltage": [0-65535],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [100000000.0-3200000000.0, step 1000000.0],
#               "attenuation": [0.0-49.5, step 0.5],
#               "enable": [0, 1],
#               "rfAttenuation": [0, 6, 12, 18],
#               "ifAttenuation": [0.0-31.5, step 0.5], 
#            },
#         ...2 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1, 2, 3, 4, 5],
#                 "streamFormat": [0, 1, 2, 3, 4, 5, 6], 
#                 "frameRate": [0, 1, 2], 
#                 "avgAlpha": [0], 
#                 "udpDest": [DIP table index],
#                 "streamId": [stream ID],
#                 "dataPort": [1, 2],
#              },
#           ...4 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-30720000.0-30720000.0, step 1],
#                 "rfIndex": [1, 2], 
#                 "rateIndex": [0, 1, 2],
#                 "streamFormat": [0], 
#                 "udpDest": [DIP table index],
#                 "streamId": [stream ID],
#                 "dataPort": [1, 2],
#              },
#           ...50 (repeat for each NBDDC)
#         },
#      },
#      "ipConfiguration": {
#            2: {
#               "sourceIP": [IP address],
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "sourcePort": [port],
#                      "destPort": [port],
#                   },
#                ...15 (repeat for each DIP table entry)
#               },
#            },
#      },
# }
# \endcode
#
# \section StreamVitaEnable_NDR301PTT Stream and VITA 49 Enabling Options
#
# These options apply to the "enable" parameter of both WBDDCs and NBDDCs.
#
# <table>
# <tr><th>Enable Option</th><th>Stream Enabled</th><th>VITA 49 Format</th></tr>
# <tr><td>0</td><td>No</td><td>N/A</td></tr>
# <tr><td>1</td><td>Yes</td><td>None (raw I/Q samples)</td></tr>
# <tr><td>2</td><td>Yes</td><td>Sample fractional time format</td></tr>
# <tr><td>3</td><td>Yes</td><td>Picosecond fractional time format</td></tr>
# <tr><td>4</td><td>No</td><td>Sample fractional time format</td></tr>
# <tr><td>4</td><td>No</td><td>Sample fractional time format</td></tr>
# </table>
#
# \section WbddcStreamFormats_NDR301PTT WBDDC Stream Formats
#
# These options apply to the "streamFormat" parameter of WBDDCs.
#
# <table>
# <tr><th>Stream Format</th><th>Data Format</th><th>Rate</th></tr>
# <tr><td>0</td><td>Spectral</td><td>As set by "frameRate" parameter</td></tr>
# <tr><td>1</td><td>Complex</td><td>FS/2</td></tr>
# <tr><td>2</td><td>Complex</td><td>FS/4</td></tr>
# <tr><td>3</td><td>Complex</td><td>FS/8</td></tr>
# <tr><td>4</td><td>Complex</td><td>FS/16</td></tr>
# <tr><td>5</td><td>Complex</td><td>FS/32</td></tr>
# <tr><td>6</td><td>Real</td><td>FS</td></tr>
# </table>
#
# \section WbddcSpectralFrameRates_NDR301PTT WBDDC Spectral Frame Rates
#
# These options apply to the "frameRate" parameter of WBDDCs.
#
# <table>
# <tr><th>Frame Rate</th><th>Rate</th></tr>
# <tr><td>0</td><td>Full rate</td></tr>
# <tr><td>1</td><td>10 outputs per second</td></tr>
# <tr><td>2</td><td>100 outputs per second</td></tr>
# </table>
#
# \section NbddcRates_NDR301PTT NBDDC Rate Settings
#
# These options apply to the "rateIndex" parameter of NBDDCs.
#
# <table>
# <tr><th>Rate Index</th><th>Bandwidth</th></tr>
# <tr><td>0</td><td>48.0 kHz BW</td></tr>
# <tr><td>1</td><td>28.8 kHz BW</td></tr>
# <tr><td>2</td><td>19.2 kHz BW</td></tr>
# </table>
#
# \section NbddcStreamFormats_NDR301PTT NBDDC Stream Formats
#
# These options apply to the "streamFormat" parameter of NBDDCs.
#
# <table>
# <tr><th>Stream Format</th><th>Data Format</th><th>Rate</th></tr>
# <tr><td>0</td><td>Complex</td><td>As set by "rateIndex" parameter</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr301_ptt(ndr301):
    _name = "NDR301-PTT"
    # ADCSR command doesn't exist for the PTT variant.  The ADC rate 
    # for this variant is locked to 122.88 MHz.
    adcsrCmd = None
    adcRate = 122.88e6
    adcRateModes = { 1: 122.88e6 }
    validConfigurationKeywords = [configKeys.CONFIG_MODE,
                                  configKeys.REFERENCE_MODE,
                                  configKeys.FNR_MODE,
                                  configKeys.REF_TUNING_VOLT,
                                 ]
    # 4 WBDDCs
    numWbddc = 2
    wbddcType = ndr301ptt_wbddc
    wbddcIndexBase = 1
    # 50 NBDDCs
    numNbddc = 50
    nbddcType = ndr301ptt_nbddc
    nbddcIndexBase = 1
    # For now, only enable port 2 (the 19-Gig output) on the PTT variant, as
    # port 1 (the 1-Gig output) is malfunctioning on the prototype.
    numGigE = 1
    gigEIndexBase = 2
    numGigEDipEntries = 64
    
    ##
    # \protected
    # \brief Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call base-class
        _radio._queryConfiguration(self)
        # Then our custom stuff (if applicable)
        # -- NOTE: commenting this out for now, as it is a lot of code that
        #    basically does a no-op. -- DA
#         for cmdClass, configKey in [ \
#                               ]:
#             if cmdClass is not None:
#                 cmd = cmdClass(parent=self, 
#                                query=True,
#                                 verbose=self.verbose, logFile=self.logFile)
#                 cmd.send( self.sendCommand, )
#                 self._addLastCommandErrorInfo(cmd)
#                 rspInfo = cmd.getResponseInfo()
#                 #self.logIfVerbose("DEBUG:", cmd.mnemonic, "rspInfo=", rspInfo)
#                 if rspInfo is not None:
#                     self.configuration[configKey] = rspInfo.get(configKey, 0)
        # Set DDC rate/data format sets based on ADC rate mode
        # -- NOTE: ADC rate mode is locked for this radio, so no call to 
        #    updateSets() is needed. -- DA

    ##
    # \protected
    # \brief Issues hardware commands to set the object's current configuration.  
    def _setConfiguration(self, confDict):
        # Call base-class
        ret = _radio._setConfiguration(self, confDict)
        # Then our custom stuff (if applicable)
        # -- NOTE: commenting this out for now, as it is a lot of code that
        #    basically does a no-op. -- DA
#         for cmdClass, configKey in [ \
#                               ]:
#             cDict = { "parent": self, \
#                       "verbose": self.verbose, \
#                       "logFile": self.logFile, \
#                       configKey: confDict.get(configKey, 0)
#                      }
#             if configKey in confDict and cmdClass is not None and \
#                cmdClass.settable:
#                 cmd = cmdClass(**cDict)
#                 ret &= cmd.send( self.sendCommand, )
#                 ret &= cmd.success
#                 self._addLastCommandErrorInfo(cmd)
#                 if ret:
#                     self.configuration[configKey] = getattr(cmd, configKey)
#                 pass
        # Set DDC rate/data format sets based on ADC rate mode
        # -- NOTE: ADC rate mode is locked for this radio, so no call to 
        #    updateSets() is needed. -- DA
        return ret


