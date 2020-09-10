#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr301 
# \brief NDR301 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017-2020 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _commandBase, nbddc, idn, ver, hrev, \
                                     cfg, pps, utc, ref, fnr, gpos, temp, \
                                     adcsr, dmac, maybeHex
from CyberRadioDriver.components import _tuner, _wbddc, \
                                        adjustFrequency, adjustAttenuation, \
                                        DDC_DATA_FORMAT
from CyberRadioDriver.radio import _ifSpec, _radio
from CyberRadioDriver.radios.ndr308 import stat308, tstat308, sip308, dip308, \
                                           ndr308_wbddc, ndr308_nbddc
# Imports from external modules
# Python standard library imports


##
# \internal
# \brief VITA 49 interface specification class for the NDR301.
class ndr301_ifSpec(_ifSpec):
    headerSizeWords = 9
    payloadSizeWords = 2048
    tailSizeWords = 1
    byteOrder = "little"
    iqSwapped = True


##
# Attenuation command specific to the NDR301.
#
class att301(_commandBase):
    mnemonic = "ATT"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.TUNER_ATTENUATION,float,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_ATTENUATION, float, True), \
                        ]


##
# RF Attenuation command specific to the NDR301.
#
class atr301(_commandBase):
    mnemonic = "ATR"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.TUNER_RF_ATTENUATION, float, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_RF_ATTENUATION, float, True), \
                        ]


##
# IF Attenuation command specific to the NDR301.
#
class ati301(_commandBase):
    mnemonic = "ATI"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.TUNER_IF_ATTENUATION, float, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_IF_ATTENUATION, float, True), \
                        ]


##
# \internal
# \brief NBDDC configuration command specific to the NDR301.
#
# The NDR301 uses a floating-point frequency offset with sub-Hz
# resolution.
#
class nbddc301(nbddc):
    ## This is a special version for the NDR601
    setParameters = [   (configKeys.INDEX, int, False,None), \
                        (configKeys.DDC_FREQUENCY_OFFSET, float, False, 0), \
                        (configKeys.DDC_RATE_INDEX, int, False, 0), \
                        (configKeys.DDC_UDP_DESTINATION, int, False, 0), \
                        (configKeys.ENABLE, int, False, 0), \
                        (configKeys.DDC_VITA_ENABLE, int, True, None), \
                        (configKeys.DDC_STREAM_ID, int, True, None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DDC_FREQUENCY_OFFSET, float, True), \
                        (configKeys.DDC_RATE_INDEX, int, True), \
                        (configKeys.DDC_UDP_DESTINATION, int, True), \
                        (configKeys.ENABLE, int, True), \
                        (configKeys.DDC_VITA_ENABLE, int, True), \
                        (configKeys.DDC_STREAM_ID, int, True), \
                        ]


##
# Reference tuning voltage command specific to the NDR301.
#
class rtv301(_commandBase):
    mnemonic="RTV"
    setParameters = [ (configKeys.REF_TUNING_VOLT, int, False, 0) ]
    queryResponseData = [ (configKeys.REF_TUNING_VOLT, maybeHex, False), \
                        ]


##
# Source MAC address configuration command for the NDR301.
#
# @note The NDR301 has two source MAC addresses that can be queried
#    via this command (the 1 Gig interface and the 10 Gig interface).
#
class smac301(_commandBase):
    mnemonic="#MAC"
    settable=False
    #setParameters = [ (configKeys.MAC_SOURCE, str, True, None) ]
    queryParameters = [ (configKeys.GIGE_PORT_INDEX, int, True, None), \
                        ]
    queryResponseData = [ 
                        (configKeys.GIGE_PORT_INDEX, int, False), \
                        (configKeys.MAC_SOURCE, str, False), \
                        ]


##
# Tuner component class for the NDR301 (all flavors).
#
# The NDR301 supports configuring RF attenuation and IF attenuation
# separately
#
class ndr301_tuner(_tuner):
    _name = "Tuner(NDR301)"
    frqRange = (30e6,3200e6)
    frqRes = 1e6
    frqUnits = 1e6
    attRange = (0.0,49.5)
    attRes = 0.5
    attCmd = att301
    atrCmd = atr301
    atiCmd = ati301
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY, 
                                  configKeys.TUNER_ATTENUATION, 
                                  configKeys.TUNER_RF_ATTENUATION, 
                                  configKeys.TUNER_IF_ATTENUATION, 
                                  configKeys.ENABLE, 
                                  ]

    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call base-class query
        _tuner._queryConfiguration(self)
        # Then our custom commands
        if self.atrCmd is not None:
            cmd = self.atrCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.configuration[configKeys.TUNER_RF_ATTENUATION] = rspInfo.get(configKeys.TUNER_RF_ATTENUATION, None)
        if self.atiCmd is not None:
            cmd = self.atiCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.configuration[configKeys.TUNER_IF_ATTENUATION] = rspInfo.get(configKeys.TUNER_IF_ATTENUATION, None)
        pass

    ##
    # \protected
    # Queries current overall attenuation.  
    def _queryAttenuation(self):
        if self.attCmd is not None:
            cmd = self.attCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.configuration[configKeys.TUNER_ATTENUATION] = rspInfo.get(configKeys.TUNER_ATTENUATION, None)

    ##
    # \protected
    # Queries current RF attenuation.  
    def _queryRfAttenuation(self):
        if self.atrCmd is not None:
            cmd = self.atrCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.configuration[configKeys.TUNER_RF_ATTENUATION] = rspInfo.get(configKeys.TUNER_RF_ATTENUATION, None)
        pass

    ##
    # \protected
    # Queries current IF attenuation.  
    def _queryIfAttenuation(self):
        if self.atiCmd is not None:
            cmd = self.atiCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.configuration[configKeys.TUNER_IF_ATTENUATION] = rspInfo.get(configKeys.TUNER_IF_ATTENUATION, None)
        pass

    # OVERRIDE
    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.  
    # \note We are doing a full override here due to how the NDR301 handles attenuation
    #    settings (overall, RF-specific, IF-specific).
    def _setConfiguration(self, confDict):
        ret = True
        if configKeys.ENABLE in confDict:
            if self.tpwrCmd is not None:
                cmd = self.tpwrCmd(**{ "parent": self, 
                                       configKeys.INDEX: self.index,
                                       configKeys.ENABLE: confDict.get(configKeys.ENABLE, 0),
                                        "verbose": self.verbose, 
                                        "logFile": self.logFile })
                ret &= cmd.send( self.callback, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    self.configuration[configKeys.ENABLE] = getattr(cmd, configKeys.ENABLE)
                pass
        if configKeys.TUNER_FREQUENCY in confDict:
            if self.frqCmd is not None:
                freqIn = float(confDict.get(configKeys.TUNER_FREQUENCY, 0)) 
                freqAdj = adjustFrequency(freqIn, self.frqRange, 
                                          self.frqRes, self.frqUnits)
                cmd = self.frqCmd(**{ "parent": self, 
                                       configKeys.INDEX: self.index,
                                       configKeys.TUNER_FREQUENCY: freqAdj,
                                        "verbose": self.verbose, 
                                        "logFile": self.logFile })
                ret &= cmd.send( self.callback, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    self.configuration[configKeys.TUNER_FREQUENCY] = freqAdj * self.frqUnits
                pass
        if configKeys.TUNER_ATTENUATION in confDict:
            if self.attCmd is not None:
                rfAttIn = float(confDict.get(configKeys.TUNER_ATTENUATION, 0)) 
                rfAttAdj = adjustAttenuation(rfAttIn, self.attRange, 
                                            self.attRes, 1)
                cmd = self.attCmd(**{ "parent": self, 
                                       configKeys.INDEX: self.index,
                                       configKeys.TUNER_ATTENUATION: rfAttAdj,
                                        "verbose": self.verbose, 
                                        "logFile": self.logFile })
                ret &= cmd.send( self.callback, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    self.configuration[configKeys.TUNER_ATTENUATION] = rfAttAdj
                pass
        if configKeys.TUNER_RF_ATTENUATION in confDict:
            if self.atrCmd is not None:
                rfAttIn = float(confDict.get(configKeys.TUNER_RF_ATTENUATION, 0)) 
                rfAttAdj = adjustAttenuation(rfAttIn, self.attRange, 
                                            self.attRes, 1)
                cmd = self.atrCmd(**{ "parent": self, 
                                       configKeys.INDEX: self.index,
                                       configKeys.TUNER_RF_ATTENUATION: rfAttAdj,
                                        "verbose": self.verbose, 
                                        "logFile": self.logFile })
                ret &= cmd.send( self.callback, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    self.configuration[configKeys.TUNER_RF_ATTENUATION] = rfAttAdj
                pass
        if configKeys.TUNER_IF_ATTENUATION in confDict:
            if self.atiCmd is not None:
                rfAttIn = float(confDict.get(configKeys.TUNER_IF_ATTENUATION, 0)) 
                rfAttAdj = adjustAttenuation(rfAttIn, self.attRange, 
                                            self.attRes, 1)
                cmd = self.atiCmd(**{ "parent": self, 
                                       configKeys.INDEX: self.index,
                                       configKeys.TUNER_IF_ATTENUATION: rfAttAdj,
                                        "verbose": self.verbose, 
                                        "logFile": self.logFile })
                ret &= cmd.send( self.callback, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    self.configuration[configKeys.TUNER_IF_ATTENUATION] = rfAttAdj
                pass
        # If setting overall attenuation, the NDR301 splits that value into individual
        # RF and IF components, so we need to query the individual RF and IF attenuations
        if configKeys.TUNER_ATTENUATION in confDict:
            self._queryRfAttenuation()
            self._queryIfAttenuation()
        # If setting either RF or IF attenuation, the NDR301 adjusts the overall
        # attenuation accordingly, so we need to query the overall attenuation
        if configKeys.TUNER_RF_ATTENUATION in confDict or \
           configKeys.TUNER_IF_ATTENUATION in confDict:
            self._queryAttenuation()
        return ret


##
# WBDDC component class for the NDR301.
class ndr301_wbddc(ndr308_wbddc):
    _name = "WBDDC(NDR301)"
    # Rate set here is based on ADC rate mode 0, but will change by instance
    rateSet = { 
#                 0: 245.76e6, 
                1: 122.88e6, 
                2: 61.44e6, 
                3: 30.72e6, 
                4: 15.36e6, 
                5: 7.68e6, 
                 }
    bwSet = {   
#                 0: 75e6, 
                1: 75e6, 
                2: 0.65*61.44e6, 
                3: 0.65*30.72e6, 
                4: 0.65*15.36e6, 
                5: 0.65*7.68e6, 
            }
    # Data format here defaults to complex I/Q, but will change by instance
    dataFormat = {0: DDC_DATA_FORMAT.REAL}
    frqCmd = None
    
    ##
    # \protected
    # \brief Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call base-class
        ndr308_wbddc._queryConfiguration(self)
        # Then our custom stuff
        # Set DDC rate/data format sets based on ADC rate mode
        # -- Data format is complex I/Q for rate indexes 2-6
        # -- Data format is real for rate index 7
        if len(self.cmdErrorInfo) == 0:
            rate_index = self.configuration[configKeys.DDC_RATE_INDEX]
#             self.dataFormat = { 1: "real" if rate_index == 7 else "iq" } ## what does this do?

    ##
    # \protected
    # \brief Issues hardware commands to set the object's current configuration.  
    def _setConfiguration(self, confDict):
        # Call base-class
        ret = ndr308_wbddc._setConfiguration(self, confDict)
        # Then our custom stuff
        # Set DDC rate/data format sets based on ADC rate mode
        # -- Data format is complex I/Q for rate indexes 2-6
        # -- Data format is real for rate index 7
        if len(self.cmdErrorInfo) == 0:
            rate_index = self.configuration[configKeys.DDC_RATE_INDEX]
#             self.dataFormat = { 1: "real" if rate_index == 7 else "iq" }
        return ret

    ##
    # \brief Update sets for this component, based on ADC sample rate.
    #
    # Used for radios which allow the ADC sample rate to be changed.
    #
    def updateSets(self):
        adc_rate = self.parent.getAdcRate()
#         self.rateSet[0] = adc_rate
        for rindex in self.rateSet.keys():
            self.rateSet[rindex] = adc_rate / (2**rindex)
            self.bwSet[rindex] = 0.65 * self.rateSet[rindex]


# NBDDC component class for the NDR301.
class ndr301_nbddc(ndr308_nbddc):
    _name = "NBDDC(NDR301)"
    # Rate set here is based on ADC rate mode 0, but will change by instance
    rateSet = {   1: 245.76e6/(64*1), # 3.84Msps
                  2: 245.76e6/(64*2), # 1.92Msps
                  3: 245.76e6/(64*3), # 1.28Msps
                  4: 245.76e6/(64*4), # 960ksps
                  5: 245.76e6/(64*5), # 768ksps
                  6: 245.76e6/(64*6), # 640ksps
                  7: 245.76e6/(64*7), # 548.571ksps
                  8: 245.76e6/(64*8), # 480ksps
                  9: 245.76e6/(64*9), # 426.667ksps
                 10: 245.76e6/(64*10), # 384ksps
                 11: 245.76e6/(64*11), # 349.091ksps
                 12: 245.76e6/(64*12), # 320ksps
                 13: 245.76e6/(64*13), # 295.385ksps
                 14: 245.76e6/(64*14), # 274.286ksps
                 15: 245.76e6/(64*15), # 256ksps
                 16: 245.76e6/(64*16), # 240ksps
                 17: 245.76e6/(64*17), # 225.882ksps
                 18: 245.76e6/(64*18), # 213.333ksps
                 19: 245.76e6/(64*19), # 202.105ksps
                 20: 245.76e6/(64*20), # 192ksps
                 21: 245.76e6/(64*21), # 182.857ksps
                 22: 245.76e6/(64*22), # 174.545ksps
                 23: 245.76e6/(64*23), # 166.957ksps
                 24: 245.76e6/(64*24), # 160ksps
                 25: 245.76e6/(64*25), # 153.6ksps
                 26: 245.76e6/(64*26), # 147.692ksps
                 27: 245.76e6/(64*27), # 142.222ksps
                 28: 245.76e6/(64*28), # 137.143ksps
                 29: 245.76e6/(64*29), # 132.414ksps
                 30: 245.76e6/(64*30), # 128ksps
                 31: 245.76e6/(64*31), # 123.871ksps
                 32: 245.76e6/(64*32), # 120ksps
                 33: 245.76e6/(64*33), # 116.364ksps
                 34: 245.76e6/(64*34), # 112.941ksps
                 35: 245.76e6/(64*35), # 109.714ksps
                 36: 245.76e6/(64*36), # 106.667ksps
                 37: 245.76e6/(64*37), # 103.784ksps
                 38: 245.76e6/(64*38), # 101.053ksps
                 39: 245.76e6/(64*39), # 98.4615ksps
                 40: 245.76e6/(64*40), # 96ksps
                 41: 245.76e6/(64*41), # 93.6585ksps
                 42: 245.76e6/(64*42), # 91.4286ksps
                 43: 245.76e6/(64*43), # 89.3023ksps
                 44: 245.76e6/(64*44), # 87.2727ksps
                 45: 245.76e6/(64*45), # 85.3333ksps
                 46: 245.76e6/(64*46), # 83.4783ksps
                 47: 245.76e6/(64*47), # 81.7021ksps
                 48: 245.76e6/(64*48), # 80ksps
                 49: 245.76e6/(64*49), # 78.3673ksps
                 50: 245.76e6/(64*50), # 76.8ksps
                 51: 245.76e6/(64*51), # 75.2941ksps
                 52: 245.76e6/(64*52), # 73.8462ksps
                 53: 245.76e6/(64*53), # 72.4528ksps
                 54: 245.76e6/(64*54), # 71.1111ksps
                 55: 245.76e6/(64*55), # 69.8182ksps
                 56: 245.76e6/(64*56), # 68.5714ksps
                 57: 245.76e6/(64*57), # 67.3684ksps
                 58: 245.76e6/(64*58), # 66.2069ksps
                 59: 245.76e6/(64*59), # 65.0847ksps
                 60: 245.76e6/(64*60), # 64ksps
                 61: 245.76e6/(64*61), # 62.9508ksps
                 62: 245.76e6/(64*62), # 61.9355ksps
                 63: 245.76e6/(64*63), # 60.9524ksps
                 64: 245.76e6/(64*64), # 60ksps
                 65: 245.76e6/(64*65), # 59.0769ksps
                 66: 245.76e6/(64*66), # 58.1818ksps
                 67: 245.76e6/(64*67), # 57.3134ksps
                 68: 245.76e6/(64*68), # 56.4706ksps
                 69: 245.76e6/(64*69), # 55.6522ksps
                 70: 245.76e6/(64*70), # 54.8571ksps
                 71: 245.76e6/(64*71), # 54.0845ksps
                 72: 245.76e6/(64*72), # 53.3333ksps
                 73: 245.76e6/(64*73), # 52.6027ksps
                 74: 245.76e6/(64*74), # 51.8919ksps
                 75: 245.76e6/(64*75), # 51.2ksps
                 76: 245.76e6/(64*76), # 50.5263ksps
                 77: 245.76e6/(64*77), # 49.8701ksps
                 78: 245.76e6/(64*78), # 49.2308ksps
                 79: 245.76e6/(64*79), # 48.6076ksps
                 80: 245.76e6/(64*80), # 48ksps
                 81: 245.76e6/(64*81), # 47.4074ksps
                 82: 245.76e6/(64*82), # 46.8293ksps
                 83: 245.76e6/(64*83), # 46.2651ksps
                 84: 245.76e6/(64*84), # 45.7143ksps
                 85: 245.76e6/(64*85), # 45.1765ksps
                 86: 245.76e6/(64*86), # 44.6512ksps
                 87: 245.76e6/(64*87), # 44.1379ksps
                 88: 245.76e6/(64*88), # 43.6364ksps
                 89: 245.76e6/(64*89), # 43.1461ksps
                 90: 245.76e6/(64*90), # 42.6667ksps
                 91: 245.76e6/(64*91), # 42.1978ksps
                 92: 245.76e6/(64*92), # 41.7391ksps
                 93: 245.76e6/(64*93), # 41.2903ksps
                 94: 245.76e6/(64*94), # 40.8511ksps
                 95: 245.76e6/(64*95), # 40.4211ksps
                 96: 245.76e6/(64*96), # 40ksps
                 97: 245.76e6/(64*97), # 39.5876ksps
                 98: 245.76e6/(64*98), # 39.1837ksps
                 99: 245.76e6/(64*99), # 38.7879ksps
                100: 245.76e6/(64*100), # 38.4ksps
                101: 245.76e6/(64*101), # 38.0198ksps
                102: 245.76e6/(64*102), # 37.6471ksps
                103: 245.76e6/(64*103), # 37.2816ksps
                104: 245.76e6/(64*104), # 36.9231ksps
                105: 245.76e6/(64*105), # 36.5714ksps
                106: 245.76e6/(64*106), # 36.2264ksps
                107: 245.76e6/(64*107), # 35.8879ksps
                108: 245.76e6/(64*108), # 35.5556ksps
                109: 245.76e6/(64*109), # 35.2294ksps
                110: 245.76e6/(64*110), # 34.9091ksps
                111: 245.76e6/(64*111), # 34.5946ksps
                112: 245.76e6/(64*112), # 34.2857ksps
                113: 245.76e6/(64*113), # 33.9823ksps
                114: 245.76e6/(64*114), # 33.6842ksps
                115: 245.76e6/(64*115), # 33.3913ksps
                116: 245.76e6/(64*116), # 33.1034ksps
                117: 245.76e6/(64*117), # 32.8205ksps
                118: 245.76e6/(64*118), # 32.5424ksps
                119: 245.76e6/(64*119), # 32.2689ksps
                120: 245.76e6/(64*120), # 32ksps
                121: 245.76e6/(64*121), # 31.7355ksps
                122: 245.76e6/(64*122), # 31.4754ksps
                123: 245.76e6/(64*123), # 31.2195ksps
                124: 245.76e6/(64*124), # 30.9677ksps
                125: 245.76e6/(64*125), # 30.72ksps
                126: 245.76e6/(64*126), # 30.4762ksps
                127: 245.76e6/(64*127), # 30.2362ksps
                128: 245.76e6/(64*128), # 30ksps
                }
    bwSet   = {   1: 0.75*245.76e6/(64*1), # 2.88MHz
                2: 0.75*245.76e6/(64*2), # 1.44MHz
                3: 0.75*245.76e6/(64*3), # 960kHz
                4: 0.75*245.76e6/(64*4), # 720kHz
                5: 0.75*245.76e6/(64*5), # 576kHz
                6: 0.75*245.76e6/(64*6), # 480kHz
                7: 0.75*245.76e6/(64*7), # 411.429kHz
                8: 0.75*245.76e6/(64*8), # 360kHz
                9: 0.75*245.76e6/(64*9), # 320kHz
                10: 0.75*245.76e6/(64*10), # 288kHz
                11: 0.75*245.76e6/(64*11), # 261.818kHz
                12: 0.75*245.76e6/(64*12), # 240kHz
                13: 0.75*245.76e6/(64*13), # 221.538kHz
                14: 0.75*245.76e6/(64*14), # 205.714kHz
                15: 0.75*245.76e6/(64*15), # 192kHz
                16: 0.75*245.76e6/(64*16), # 180kHz
                17: 0.75*245.76e6/(64*17), # 169.412kHz
                18: 0.75*245.76e6/(64*18), # 160kHz
                19: 0.75*245.76e6/(64*19), # 151.579kHz
                20: 0.75*245.76e6/(64*20), # 144kHz
                21: 0.75*245.76e6/(64*21), # 137.143kHz
                22: 0.75*245.76e6/(64*22), # 130.909kHz
                23: 0.75*245.76e6/(64*23), # 125.217kHz
                24: 0.75*245.76e6/(64*24), # 120kHz
                25: 0.75*245.76e6/(64*25), # 115.2kHz
                26: 0.75*245.76e6/(64*26), # 110.769kHz
                27: 0.75*245.76e6/(64*27), # 106.667kHz
                28: 0.75*245.76e6/(64*28), # 102.857kHz
                29: 0.75*245.76e6/(64*29), # 99.3103kHz
                30: 0.75*245.76e6/(64*30), # 96kHz
                31: 0.75*245.76e6/(64*31), # 92.9032kHz
                32: 0.75*245.76e6/(64*32), # 90kHz
                33: 0.75*245.76e6/(64*33), # 87.2727kHz
                34: 0.75*245.76e6/(64*34), # 84.7059kHz
                35: 0.75*245.76e6/(64*35), # 82.2857kHz
                36: 0.75*245.76e6/(64*36), # 80kHz
                37: 0.75*245.76e6/(64*37), # 77.8378kHz
                38: 0.75*245.76e6/(64*38), # 75.7895kHz
                39: 0.75*245.76e6/(64*39), # 73.8462kHz
                40: 0.75*245.76e6/(64*40), # 72kHz
                41: 0.75*245.76e6/(64*41), # 70.2439kHz
                42: 0.75*245.76e6/(64*42), # 68.5714kHz
                43: 0.75*245.76e6/(64*43), # 66.9767kHz
                44: 0.75*245.76e6/(64*44), # 65.4545kHz
                45: 0.75*245.76e6/(64*45), # 64kHz
                46: 0.75*245.76e6/(64*46), # 62.6087kHz
                47: 0.75*245.76e6/(64*47), # 61.2766kHz
                48: 0.75*245.76e6/(64*48), # 60kHz
                49: 0.75*245.76e6/(64*49), # 58.7755kHz
                50: 0.75*245.76e6/(64*50), # 57.6kHz
                51: 0.75*245.76e6/(64*51), # 56.4706kHz
                52: 0.75*245.76e6/(64*52), # 55.3846kHz
                53: 0.75*245.76e6/(64*53), # 54.3396kHz
                54: 0.75*245.76e6/(64*54), # 53.3333kHz
                55: 0.75*245.76e6/(64*55), # 52.3636kHz
                56: 0.75*245.76e6/(64*56), # 51.4286kHz
                57: 0.75*245.76e6/(64*57), # 50.5263kHz
                58: 0.75*245.76e6/(64*58), # 49.6552kHz
                59: 0.75*245.76e6/(64*59), # 48.8136kHz
                60: 0.75*245.76e6/(64*60), # 48kHz
                61: 0.75*245.76e6/(64*61), # 47.2131kHz
                62: 0.75*245.76e6/(64*62), # 46.4516kHz
                63: 0.75*245.76e6/(64*63), # 45.7143kHz
                64: 0.75*245.76e6/(64*64), # 45kHz
                65: 0.75*245.76e6/(64*65), # 44.3077kHz
                66: 0.75*245.76e6/(64*66), # 43.6364kHz
                67: 0.75*245.76e6/(64*67), # 42.9851kHz
                68: 0.75*245.76e6/(64*68), # 42.3529kHz
                69: 0.75*245.76e6/(64*69), # 41.7391kHz
                70: 0.75*245.76e6/(64*70), # 41.1429kHz
                71: 0.75*245.76e6/(64*71), # 40.5634kHz
                72: 0.75*245.76e6/(64*72), # 40kHz
                73: 0.75*245.76e6/(64*73), # 39.4521kHz
                74: 0.75*245.76e6/(64*74), # 38.9189kHz
                75: 0.75*245.76e6/(64*75), # 38.4kHz
                76: 0.75*245.76e6/(64*76), # 37.8947kHz
                77: 0.75*245.76e6/(64*77), # 37.4026kHz
                78: 0.75*245.76e6/(64*78), # 36.9231kHz
                79: 0.75*245.76e6/(64*79), # 36.4557kHz
                80: 0.75*245.76e6/(64*80), # 36kHz
                81: 0.75*245.76e6/(64*81), # 35.5556kHz
                82: 0.75*245.76e6/(64*82), # 35.122kHz
                83: 0.75*245.76e6/(64*83), # 34.6988kHz
                84: 0.75*245.76e6/(64*84), # 34.2857kHz
                85: 0.75*245.76e6/(64*85), # 33.8824kHz
                86: 0.75*245.76e6/(64*86), # 33.4884kHz
                87: 0.75*245.76e6/(64*87), # 33.1034kHz
                88: 0.75*245.76e6/(64*88), # 32.7273kHz
                89: 0.75*245.76e6/(64*89), # 32.3596kHz
                90: 0.75*245.76e6/(64*90), # 32kHz
                91: 0.75*245.76e6/(64*91), # 31.6484kHz
                92: 0.75*245.76e6/(64*92), # 31.3043kHz
                93: 0.75*245.76e6/(64*93), # 30.9677kHz
                94: 0.75*245.76e6/(64*94), # 30.6383kHz
                95: 0.75*245.76e6/(64*95), # 30.3158kHz
                96: 0.75*245.76e6/(64*96), # 30kHz
                97: 0.75*245.76e6/(64*97), # 29.6907kHz
                98: 0.75*245.76e6/(64*98), # 29.3878kHz
                99: 0.75*245.76e6/(64*99), # 29.0909kHz
                100: 0.75*245.76e6/(64*100), # 28.8kHz
                101: 0.75*245.76e6/(64*101), # 28.5149kHz
                102: 0.75*245.76e6/(64*102), # 28.2353kHz
                103: 0.75*245.76e6/(64*103), # 27.9612kHz
                104: 0.75*245.76e6/(64*104), # 27.6923kHz
                105: 0.75*245.76e6/(64*105), # 27.4286kHz
                106: 0.75*245.76e6/(64*106), # 27.1698kHz
                107: 0.75*245.76e6/(64*107), # 26.9159kHz
                108: 0.75*245.76e6/(64*108), # 26.6667kHz
                109: 0.75*245.76e6/(64*109), # 26.422kHz
                110: 0.75*245.76e6/(64*110), # 26.1818kHz
                111: 0.75*245.76e6/(64*111), # 25.9459kHz
                112: 0.75*245.76e6/(64*112), # 25.7143kHz
                113: 0.75*245.76e6/(64*113), # 25.4867kHz
                114: 0.75*245.76e6/(64*114), # 25.2632kHz
                115: 0.75*245.76e6/(64*115), # 25.0435kHz
                116: 0.75*245.76e6/(64*116), # 24.8276kHz
                117: 0.75*245.76e6/(64*117), # 24.6154kHz
                118: 0.75*245.76e6/(64*118), # 24.4068kHz
                119: 0.75*245.76e6/(64*119), # 24.2017kHz
                120: 0.75*245.76e6/(64*120), # 24kHz
                121: 0.75*245.76e6/(64*121), # 23.8017kHz
                122: 0.75*245.76e6/(64*122), # 23.6066kHz
                123: 0.75*245.76e6/(64*123), # 23.4146kHz
                124: 0.75*245.76e6/(64*124), # 23.2258kHz
                125: 0.75*245.76e6/(64*125), # 23.04kHz
                126: 0.75*245.76e6/(64*126), # 22.8571kHz
                127: 0.75*245.76e6/(64*127), # 22.6772kHz
                128: 0.75*245.76e6/(64*128), # 22.5kHz
                 }
    # Frequency range here is based on ADC rate mode 0, but will change by instance
    frqRange = (-61.44e6, 61.44e6,)
    cfgCmd = nbddc301

    ##
    # \brief Update sets for this component, based on ADC sample rate.
    #
    # Used for radios which allow the ADC sample rate to be changed.
    #
    def updateSets(self):
        adc_rate = self.parent.getAdcRate()
        # Frequency range
        self.frqRange = (-adc_rate / 4.0, adc_rate / 4.0)
        # Rate set and BW set
        for rindex in self.rateSet.keys():
            self.rateSet[rindex] = adc_rate / (rindex * 64.0)
            self.bwSet[rindex] = 0.75 * self.rateSet[rindex]


##
# \brief Radio handler class for the NDR301.
#
# The NDR301 allows users to use either a TCP link or a serial link for its 
# command and control communications.  The TCP link uses a different port number 
# than the NDR308-class radios use (10301 rather than 8617).
#
# The NDR301 also provides both 1 Gig and 10 Gig data outputs.  However, 
# the 301's command set treats the 1 Gig and 10 Gig interfaces identically.
# For driver purposes, the 1 Gig interface is treated as a 10 Gig interface with
# index 1.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR301 Connection Modes
#
# "tcp", "tty"
#
# \implements CyberRadioDriver.IRadio    
class ndr301(_radio):
    _name = "NDR301"
    ifSpec = ndr301_ifSpec
    json = False
    numTuner = 2
    tunerType = ndr301_tuner
    tunerIndexBase = 1
    numWbddc = 2
    wbddcType = ndr301_wbddc
    wbddcIndexBase = 1
    numNbddc = 8
    nbddcType = ndr301_nbddc
    nbddcIndexBase = 1
    # GigE interfaces: Index 1 is the 1Gig output, 2 is the 10Gig output
    # They are treated the same way in the driver.
    numGigE = 2
    gigEIndexBase = 1
    numGigEDipEntries = 16
    gigEDipEntryIndexBase = 0
    idnQry = idn
    verQry = ver
    hrevQry = hrev
    statQry = stat308
    tstatQry = tstat308
    tadjCmd = None
    resetCmd = None
    cfgCmd = cfg
    ppsCmd = pps
    utcCmd = utc
    refCmd = ref
    rbypCmd = None
    sipCmd = sip308
    dipCmd = dip308
    smacCmd = smac301
    dmacCmd = dmac
    calfCmd = None
    nbssCmd = None
    fnrCmd = fnr
    gpsCmd = None
    gposCmd = gpos
    rtvCmd = rtv301
    tempCmd = temp
    gpioStaticCmd = None
    gpioSeqCmd = None
    tgfcCmd = None
    adcsrCmd = adcsr
    refModes = { 0: "Internal 10MHz", 
                 1: "External 10MHz", 
                 2: "Internal GPSDO 10MHz",
                 3: "External 1PPS", 
                 4: "External 1PPS pass-through",
                 5: "External 10MHz and 1PPS",
                 }
    # This ADC rate assumes ADC rate mode 0, but this will change by instance
    adcRate = 245.76e6
    adcRateModes = { 0: 245.76e6,
                     1: 122.88e6 }
    rbypModes = {}
    connectionModes = ["tcp", "tty"]
    defaultPort = 10301
    udpDestInfo = "Destination index"
    vitaEnableOptions = {0: "VITA-49 header disabled",
                         1: "VITA-49 header enabled, fractional timestamp in picoseconds",
                         2: "VITA-49 header disabled",
                         3: "VITA-49 header enabled, fractional timestamp in sample counts",
                         }
    ## \brief Does this radio support setting the tuner bandwidth?
    tunerBandwithSettable = False
    tunerBandwidthConstant = 75e6
    validConfigurationKeywords = [configKeys.CONFIG_MODE, \
                                  configKeys.REFERENCE_MODE, \
                                  configKeys.FNR_MODE, \
                                  configKeys.REF_TUNING_VOLT, \
                                  configKeys.ADC_RATE_MODE, \
                                 ]

    ##
    # \protected
    # \brief Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call base-class
        _radio._queryConfiguration(self)
        # Then our custom stuff
        for cmdClass, configKey in [ \
                                (self.adcsrCmd, configKeys.ADC_RATE_MODE), \
                              ]:
            if cmdClass is not None:
                cmd = cmdClass(parent=self, 
                               query=True,
                                verbose=self.verbose, logFile=self.logFile)
                cmd.send( self.sendCommand, )
                self._addLastCommandErrorInfo(cmd)
                rspInfo = cmd.getResponseInfo()
                #self.logIfVerbose("DEBUG:", cmd.mnemonic, "rspInfo=", rspInfo)
                if rspInfo is not None:
                    self.configuration[configKey] = rspInfo.get(configKey, 0)
        # Set DDC rate/data format sets based on ADC rate mode
        if len(self.cmdErrorInfo) == 0:
            self.adcRate = self.adcRateModes.get(self.configuration[configKeys.ADC_RATE_MODE], 0)
            for wbddc in self.wbddcDict.values():
                wbddc.updateSets()
            for nbddc in self.nbddcDict.values():
                nbddc.updateSets()

    ##
    # \protected
    # \brief Issues hardware commands to set the object's current configuration.  
    def _setConfiguration(self, confDict):
        # Call base-class
        ret = _radio._setConfiguration(self, confDict)
        # Then our custom stuff
        for cmdClass, configKey in [ \
                                (self.adcsrCmd, configKeys.ADC_RATE_MODE), \
                              ]:
            cDict = { "parent": self, \
                      "verbose": self.verbose, \
                      "logFile": self.logFile, \
                      configKey: confDict.get(configKey, 0)
                     }
            if configKey in confDict and cmdClass is not None and \
               cmdClass.settable:
                cmd = cmdClass(**cDict)
                ret &= cmd.send( self.sendCommand, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    self.configuration[configKey] = getattr(cmd, configKey)
                pass
        # Set DDC rate/data format sets based on new ADC rate mode
        if ret and configKeys.ADC_RATE_MODE in confDict:
            self.adcRate = self.adcRateModes.get(self.configuration[configKeys.ADC_RATE_MODE], 0)
            for wbddc in self.wbddcDict.values():
                wbddc.updateSets()
            for nbddc in self.nbddcDict.values():
                nbddc.updateSets()
        return ret

    # The following methods override the similarly named class methods so that they 
    # operate on local instance variables.
    # REMOVING THESE OVERRIDES WILL BREAK EXPECTED FUNCTIONALITY! -- DA
    
    # OVERRIDE
    def getAdcRate(self):
        return self.adcRate

    # OVERRIDE
    def getWbddcRateSet(self, index=None):
        ret = []
        if self.numWbddc > 0:
            wbddcIndices = sorted(self.wbddcDict.keys())
            if index is None:
                ret = self.wbddcDict[wbddcIndices[0]].rateSet
            elif index in wbddcIndices:
                ret = self.wbddcDict[wbddcIndices[index]].rateSet
        return ret
      
    # OVERRIDE
    def getWbddcRateList(self, index=None):
        rateSet = self.getWbddcRateSet(index)
        return [rateSet[q] for q in sorted(rateSet.keys())]
      
    # OVERRIDE
    def getNbddcRateSet(self, index=None):
        ret = []
        if self.numNbddc > 0:
            nbddcIndices = sorted(self.nbddcDict.keys())
            if index is None:
                ret = self.nbddcDict[nbddcIndices[0]].rateSet
            elif index in nbddcIndices:
                ret = self.nbddcDict[nbddcIndices[index]].rateSet
        return ret
      
    # OVERRIDE
    def getNbddcRateList(self, index=None):
        rateSet = self.getNbddcRateSet(index)
        return [rateSet[q] for q in sorted(rateSet.keys())]
    



        
if __name__ == '__main__':
    pass
