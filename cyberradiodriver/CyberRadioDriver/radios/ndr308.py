#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr308 
# \brief NDR308 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017 G3 Technologies, Inc.  All rights
#    reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import command
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _commandBase, nbddc, stat, tstat
from CyberRadioDriver.components import _tuner, _wbddc, _nbddc, \
                                        wbddc_group, nbddc_group, \
                                        adjustFrequency, DDC_DATA_FORMAT
from CyberRadioDriver.radio import _ifSpec, _radio
# Imports from external modules
# Python standard library imports


##
# \internal
# \brief NBDDC configuration command specific to the NDR308.
#
class nbddc308(nbddc):
    ## This is a special version for the NDR308
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.DDC_FREQUENCY_OFFSET,int,False,0), \
                        (configKeys.DDC_RATE_INDEX,int,False,0), \
                        (configKeys.DDC_UDP_DESTINATION,int,False,0), \
                        (configKeys.ENABLE,int,False,0), \
                        (configKeys.DDC_VITA_ENABLE,int,True,None), \
                        (configKeys.DDC_STREAM_ID,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DDC_FREQUENCY_OFFSET, int, True), \
                        (configKeys.DDC_RATE_INDEX, int, True), \
                        (configKeys.DDC_UDP_DESTINATION, int, True), \
                        (configKeys.ENABLE, int, True), \
                        (configKeys.DDC_VITA_ENABLE, int, True), \
                        (configKeys.DDC_STREAM_ID, int, True), \
                        ]


##
# \internal
# \brief Destination IP address configuration command specific to the NDR308.
#
# Supports radios which have dedicated Gigabit Ethernet ports.
class dip308(_commandBase):
    mnemonic="DIP"
    setParameters = [ \
                        (configKeys.GIGE_PORT_INDEX, int, True, None), \
                        (configKeys.GIGE_DIP_INDEX, int, True, None), \
                        (configKeys.GIGE_IP_ADDR, str, True, None), \
                        (configKeys.GIGE_MAC_ADDR, str, True, None), \
                        (configKeys.GIGE_SOURCE_PORT, int, True, None), \
                        (configKeys.GIGE_DEST_PORT, int, True, None), \
                        ]
    queryParameters = [ (configKeys.GIGE_PORT_INDEX, int, True, None), \
                        (configKeys.GIGE_DIP_INDEX, int, True, None), \
                        ]
    queryResponseData = [ \
                        (configKeys.GIGE_PORT_INDEX, int, False), \
                        (configKeys.GIGE_DIP_INDEX, int, False), \
                        (configKeys.GIGE_IP_ADDR, str, False), \
                        (configKeys.GIGE_MAC_ADDR, str, False), \
                        (configKeys.GIGE_SOURCE_PORT, int, False), \
                        (configKeys.GIGE_DEST_PORT, int, False), \
                        ]
    

##
# \internal
# \brief Source IP address configuration command specific to the NDR308.
#
# Supports radios which have dedicated Gigabit Ethernet ports.
class sip308(_commandBase):
    mnemonic="SIP"
    setParameters = [ (configKeys.GIGE_PORT_INDEX, int, True, None), \
                      (configKeys.IP_SOURCE, str, True, None), \
                     ]
    queryParameters = [ (configKeys.GIGE_PORT_INDEX, int, True, None), \
                        ]
    queryResponseData = [ \
                        (configKeys.GIGE_PORT_INDEX, int, False), \
                        (configKeys.IP_SOURCE, str, False), \
                        ]
    

##
# \internal
# \brief Status command bitmask values for the NDR308.
#
# Static member "text" is a dictionary where the keys are bits in 
# the status bitmask, and the values are text strings indicating what those 
# bits mean when set.
#
class stat308Values():
    RF_TUNER_UNLOCKED = 0x01
    ADC_OVERFLOW = 0x02
    REF_UNLOCKED = 0x04
    POWER_FAILURE = 0x08
    OVER_TEMP = 0x10
    RT_TIMER = 0x20
    GPS_FIX = 0x40
    TUNER_OFF_OVER_TEMP = 0x80
    REF_PIC = 0x100
    FPGA_ERR = 0x200
    MGT_REF = 0x400
    UTC_COR = 0x800
    text = {
            RF_TUNER_UNLOCKED: "RF Tuner LOs Unlocked (check TSTAT?)", \
            ADC_OVERFLOW: "ADC Overflow", \
            REF_UNLOCKED: "Reference not yet locked", \
            POWER_FAILURE: "Power failure", \
            OVER_TEMP: "Over-temp condition", \
            RT_TIMER: "Retune timer not timed-out", \
            GPS_FIX: "GPS has no valid fix", \
            TUNER_OFF_OVER_TEMP: "Tuners turned off due to high-temp condition", \
            REF_PIC: "Reference microcontroller has entered an inoperable state", \
            FPGA_ERR: "FPGA firmware is not compatible with the TunerControl software", \
            MGT_REF: "FPGA firmware and the digital board revision and MGT reference " \
                     "oscillator frequency are not compatible", \
            UTC_COR: "UTC correction value for leap seconds has not yet been received " \
                     "by the GPS module", \
            }


##
# \internal
# \brief Status command specific to the NDR308.
#
# \copydetails CyberRadioDriver::command::stat
class stat308(stat):
    statTextValues = stat308Values.text


##
# \internal
# \brief Tuner RF status command bitmask values for the NDR308.
#
# \copydetails CyberRadioDriver::radios::ndr308::stat308Values
class tstat308Values():
    RF1_LO1_UNLOCKED = 0x1
    RF1_LO2_UNLOCKED = 0x2
    RF2_LO1_UNLOCKED = 0x4
    RF2_LO2_UNLOCKED = 0x8
    RF3_LO1_UNLOCKED = 0x10
    RF3_LO2_UNLOCKED = 0x20
    RF4_LO1_UNLOCKED = 0x40
    RF4_LO2_UNLOCKED = 0x80
    TQ1_COH_LO1_UNLOCKED = 0x100
    TQ1_COH_LO2_UNLOCKED = 0x200
    TQ1_100MHZ_REF_UNLOCKED = 0x400
    
    RF5_LO1_UNLOCKED = 0x1000
    RF5_LO2_UNLOCKED = 0x2000
    RF6_LO1_UNLOCKED = 0x4000
    RF6_LO2_UNLOCKED = 0x8000
    RF7_LO1_UNLOCKED = 0x10000
    RF7_LO2_UNLOCKED = 0x20000
    RF8_LO1_UNLOCKED = 0x40000
    RF8_LO2_UNLOCKED = 0x80000
    TQ2_COH_LO1_UNLOCKED     = 0x100000
    TQ2_COH_LO2_UNLOCKED     = 0x200000
    TQ2_100MHZ_REF_UNLOCKED = 0x400000
    
    text = {
        RF1_LO1_UNLOCKED: "RF1 LO1 Unlocked", \
        RF1_LO2_UNLOCKED: "RF1 LO2 Unlocked", \
        RF2_LO1_UNLOCKED: "RF2 LO1 Unlocked", \
        RF2_LO2_UNLOCKED: "RF2 LO2 Unlocked", \
        RF3_LO1_UNLOCKED: "RF3 LO1 Unlocked", \
        RF3_LO2_UNLOCKED: "RF3 LO2 Unlocked", \
        RF4_LO1_UNLOCKED: "RF4 LO1 Unlocked", \
        RF4_LO2_UNLOCKED: "RF5 LO2 Unlocked", \
        TQ1_COH_LO1_UNLOCKED: "Tuner Quad 1 LO1 Unlocked", \
        TQ1_COH_LO2_UNLOCKED: "Tuner Quad 1 LO2 Unlocked", \
        TQ1_100MHZ_REF_UNLOCKED: "Tuner Quad 1 100MHz Unlocked", \
        RF5_LO1_UNLOCKED: "RF5 LO1 Unlocked", \
        RF5_LO2_UNLOCKED: "RF5 LO2 Unlocked", \
        RF6_LO1_UNLOCKED: "RF6 LO1 Unlocked", \
        RF6_LO2_UNLOCKED: "RF6 LO2 Unlocked", \
        RF7_LO1_UNLOCKED: "RF7 LO1 Unlocked", \
        RF7_LO2_UNLOCKED: "RF7 LO2 Unlocked", \
        RF8_LO1_UNLOCKED: "RF8 LO1 Unlocked", \
        RF8_LO2_UNLOCKED: "RF8 LO2 Unlocked", \
        TQ2_COH_LO1_UNLOCKED: "Tuner Quad 2 LO1 Unlocked", \
        TQ2_COH_LO2_UNLOCKED: "Tuner Quad 2 LO2 Unlocked", \
        TQ2_100MHZ_REF_UNLOCKED: "Tuner Quad 1 100MHz Unlocked", \
        }


##
# \internal
# \brief Tuner RF status command specific to the NDR308.
#
# \copydetails CyberRadioDriver::command::tstat
class tstat308(tstat):
    statTextValues = tstat308Values.text


##
# \internal
# \brief Tuner component class for the NDR308 (all flavors).
#
class ndr308_tuner(_tuner):
    _name = "Tuner(NDR308)"
    frqRange = (20e6,6e9)
    attRange = (0.0,46.0)
    fifCmd = command.fif
    tadjCmd = command.tadj
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY, 
                                  configKeys.TUNER_ATTENUATION, 
                                  configKeys.TUNER_RF_ATTENUATION,
                                  configKeys.ENABLE, 
                                  configKeys.TUNER_FILTER,
                                  configKeys.TUNER_TIMING_ADJ,
                                  ]


##
# \internal
# \brief WBDDC component class for the NDR308.
class ndr308_wbddc(_wbddc):
    _name = "WBDDC(NDR308)"
    rateSet = { 0: 51.2e6, 
                1: 25.6e6, 
                2: 12.8e6, 
                3: 102.4e6, 
                4: 6.4e6, 
                5: 3.2e6, 
                 }
    bwSet = { 0: 40e6, \
                1: 0.8*25.6e6, 
                2: 0.8*12.8e6, 
                3: 40e6, 
                4: 0.8*6.4e6, 
                5: 0.8*3.2e6, 
                 }
    dataFormat = { 3:DDC_DATA_FORMAT.REAL }
#    cfgCmd = command.wbddc308
    frqCmd = None
    # OVERRIDE
    dportCmd = command.wbdp
    # OVERRIDE
    validConfigurationKeywords = [
                                  configKeys.ENABLE, 
                                  configKeys.DDC_RATE_INDEX, 
                                  configKeys.DDC_UDP_DESTINATION, 
                                  configKeys.DDC_VITA_ENABLE, 
                                  configKeys.DDC_STREAM_ID, 
                                  configKeys.DDC_DATA_PORT,
                                  ]

##
# \internal
# \brief WBDDC component class for the NDR308-TS.
class ndr308ts_wbddc(ndr308_wbddc):
    _name = "WBDDC(NDR308)"
    rateSet = { 0: 1.2*51.2e6, \
                1: 1.2*25.6e6, \
                2: 1.2*12.8e6, \
#                3: 1.2*102.4e6, \
                 }
#     dataFormat = { 3:"real" }
#    cfgCmd = command.wbddc308
    frqCmd = None


##
# \internal
# \brief NBDDC component class for the NDR308-1.
class ndr308_1_nbddc(_nbddc):
    _name = "NBDDC(NDR308-1)"
    rateSet = { 0: 1.6e6, \
                1: 800e3, \
                2: 400e3, \
                3: 200e3, \
                4: 100e3, \
                5: 50e3, \
                6: 25e3, \
                7: 12.5e3, \
                 }
    bwSet = { 0: 0.8*1.6e6, \
                1: 0.8*800e3, \
                2: 0.8*400e3, \
                3: 0.8*200e3, \
                4: 0.8*100e3, \
                5: 0.8*50e3, \
                6: 0.8*25e3, \
                7: 0.8*12.5e3, \
                 }
    frqRange = (-25.6e6,25.6e6,)
    cfgCmd = nbddc308
    frqCmd = None
    # OVERRIDE
    validConfigurationKeywords = [
                                  configKeys.ENABLE, 
                                  configKeys.DDC_FREQUENCY_OFFSET, 
                                  configKeys.DDC_RATE_INDEX, 
                                  configKeys.DDC_UDP_DESTINATION, 
                                  configKeys.DDC_VITA_ENABLE, 
                                  configKeys.DDC_STREAM_ID, 
                                  ]

    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
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
                for key in [configKeys.ENABLE, 
                            configKeys.DDC_RATE_INDEX, 
                            configKeys.DDC_UDP_DESTINATION, 
                            configKeys.DDC_VITA_ENABLE, 
                            configKeys.DDC_STREAM_ID]:
                    self.configuration[key] = rspInfo.get(key, None)
                freq = rspInfo.get(configKeys.DDC_FREQUENCY_OFFSET, 0)
                self.configuration[configKeys.DDC_FREQUENCY_OFFSET] = None if freq is None else \
                                                                      freq * self.frqUnits
        pass

    # OVERRIDE
    ##
    # \protected
    # Sets the component's current configuration.  
    def _setConfiguration(self, confDict):
        ret = True
        keys = [configKeys.ENABLE, 
                configKeys.DDC_RATE_INDEX, 
                configKeys.DDC_UDP_DESTINATION, 
                configKeys.DDC_VITA_ENABLE, 
                configKeys.DDC_STREAM_ID, 
                configKeys.DDC_FREQUENCY_OFFSET]
        if any([q in confDict for q in keys]):
            if self.cfgCmd is not None:
                cDict = {}
                if confDict.has_key(configKeys.DDC_FREQUENCY_OFFSET):
                    confDict[configKeys.DDC_FREQUENCY_OFFSET] = adjustFrequency(
                                          float(confDict[configKeys.DDC_FREQUENCY_OFFSET]), 
                                          self.frqRange, 
                                          self.frqRes, 
                                          self.frqUnits)
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
# \internal
# \brief NBDDC component class for the NDR308.
class ndr308_nbddc(ndr308_1_nbddc):
    _name = "NBDDC(NDR308)"
    # OVERRIDE
    selectableSource = True
    # OVERRIDE
    nbssCmd = command.nbss
    # OVERRIDE
    dportCmd = command.nbdp
    # OVERRIDE
    validConfigurationKeywords = [
                                  configKeys.ENABLE, 
                                  configKeys.DDC_FREQUENCY_OFFSET, 
                                  configKeys.DDC_RATE_INDEX, 
                                  configKeys.DDC_UDP_DESTINATION, 
                                  configKeys.DDC_VITA_ENABLE, 
                                  configKeys.DDC_STREAM_ID, 
                                  configKeys.NBDDC_RF_INDEX,
                                  configKeys.DDC_DATA_PORT,
                                  ]

    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
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
#                 for key in [configKeys.ENABLE, 
#                             configKeys.DDC_RATE_INDEX, 
#                             configKeys.DDC_UDP_DESTINATION, 
#                             configKeys.DDC_VITA_ENABLE, 
#                             configKeys.DDC_STREAM_ID]:
                keys = [i[0] for i in self.cfgCmd.queryResponseData]
                for key in keys:
                    self.configuration[key] = rspInfo.get(key, None)
                freq = rspInfo.get(configKeys.DDC_FREQUENCY_OFFSET, 0)
                self.configuration[configKeys.DDC_FREQUENCY_OFFSET] = None if freq is None else \
                                                                      freq * self.frqUnits
        if self.nbssCmd is not None:
            cmd = self.nbssCmd(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
            cmd.send( self.callback, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            #self.logIfVerbose("rspInfo =", rspInfo)
            if rspInfo is not None:
                for key in [configKeys.NBDDC_RF_INDEX, 
                            ]:
                    self.configuration[key] = rspInfo.get(key, None)
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
    # Sets the component's current configuration.  
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
                             "logFile": self.logFile })
            cmd = self.dportCmd(**cDict)
            ret &= cmd.send( self.callback, )
            ret &= cmd.success
            self._addLastCommandErrorInfo(cmd)
            if ret:
                self.configuration[configKeys.DDC_DATA_PORT] = getattr(cmd, configKeys.DDC_DATA_PORT)
            pass
        if self.cfgCmd is not None:
            keys = [ i[0] for i in self.cfgCmd.setParameters ]
            #print repr(self),"setParameters =",keys
            #print repr(self),"self.configuration =",self.configuration
            #print repr(self),"confDict =",confDict
        else:
            keys = [configKeys.ENABLE, 
                configKeys.DDC_RATE_INDEX, 
                configKeys.DDC_UDP_DESTINATION, 
                configKeys.DDC_VITA_ENABLE, 
                configKeys.DDC_STREAM_ID, 
                configKeys.DDC_FREQUENCY_OFFSET,
                ]
        if any([q in confDict for q in keys]):
            if self.cfgCmd is not None:
                cDict = {}
                if confDict.has_key(configKeys.DDC_FREQUENCY_OFFSET):
                    confDict[configKeys.DDC_FREQUENCY_OFFSET] = adjustFrequency(
                                          float(confDict[configKeys.DDC_FREQUENCY_OFFSET]), 
                                          self.frqRange, 
                                          self.frqRes, 
                                          self.frqUnits)
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
        if self.nbssCmd is not None and \
           configKeys.NBDDC_RF_INDEX in confDict:
            cDict = {}
            self._dictUpdate(cDict, confDict, self.configuration, 
                             [configKeys.NBDDC_RF_INDEX])
            cDict.update({ "parent": self, 
                            configKeys.INDEX: self.index,
                             "verbose": self.verbose, 
                             "logFile": self.logFile })
            cmd = self.nbssCmd(**cDict)
            ret &= cmd.send( self.callback, )
            ret &= cmd.success
            self._addLastCommandErrorInfo(cmd)
            if ret:
                self.configuration[configKeys.NBDDC_RF_INDEX] = getattr(cmd, configKeys.NBDDC_RF_INDEX)
            pass
        return ret


##
# \internal
# \brief NBDDC component class for the NDR308-TS.
class ndr308ts_nbddc(ndr308_nbddc):
    _name = "NBDDC(NDR308-TS)"
    # OVERRIDE
    selectableSource = False
    # OVERRIDE
    nbssCmd = None
    rateSet = { 0: 1.2*1.6e6, \
                1: 1.2*800e3, \
                2: 1.2*400e3, \
                3: 1.2*150e3, \
                4: 1.2*50e3, \
                5: 1.2*25e3, \
                6: 1.2*12.5e3, \
                 }


##
# \internal
# \brief WBDDC group component class specific to the NDR308.
#
# A WBDDC group component object maintains one WBDDC group on the radio.  
#
class ndr308_wbddc_group(wbddc_group):
    _name = "WBDDCGroup(NDR308)"
    ## \brief Group member index base (what number indices start at) 
    groupMemberIndexBase = 1
    ## \brief Number of potential group members 
    numGroupMembers = 8


##
# \internal
# \brief NBDDC group component class specific to the NDR308.
#
# A NBDDC group component object maintains one NBDDC group on the radio.  
#
class ndr308_nbddc_group(nbddc_group):
    _name = "NBDDCGroup(NDR308)"
    ## \brief Group member index base (what number indices start at) 
    groupMemberIndexBase = 1
    ## \brief Number of potential group members 
    numGroupMembers = 32


##
# \internal
# \brief VITA 49 interface specification class for the NDR308.
class ndr308_ifSpec(_ifSpec):
    headerSizeWords = 9
    payloadSizeWords = 1024
    tailSizeWords = 1
    byteOrder = "little"


##
# \brief Radio handler class for the NDR308-1.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308-1 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308-1 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4],
#      "bypassMode": [0, 1],
#      "calibFrequency": [0, 25.0-3000.0],
#      "freqNormalization": [0, 1],
#      "gpsEnable": [0, 1],
#      "referenceTuningVoltage": [0-65535],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#               "filter": [0, 1],
#               "timingAdjustment": [-200000 - 200000, step 1],
#            },
#         ...8 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0, 1, 2],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#              },
#           ...8 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6, 7],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#              },
#           ...16 (repeat for each NBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...4 (repeat for each WBDDC group)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...8 (repeat for each NBDDC group)
#         },
#      },
#      "ipConfiguration": {
#            1: {
#               "sourceIP": [IP address],
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "sourcePort": [port],
#                      "destPort": [port],
#                   },
#                ...31 (repeat for each DIP table entry)
#               },
#            },
#         ...2 (repeat for each Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \section WbddcRates_NDR308-1 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>51200000.0</td></tr>
# <tr><td>1</td><td>25600000.0</td></tr>
# <tr><td>2</td><td>12800000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308-1 NBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>NBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>1600000.0</td></tr>
# <tr><td>1</td><td>800000.0</td></tr>
# <tr><td>2</td><td>400000.0</td></tr>
# <tr><td>3</td><td>200000.0</td></tr>
# <tr><td>4</td><td>100000.0</td></tr>
# <tr><td>5</td><td>50000.0</td></tr>
# <tr><td>6</td><td>25000.0</td></tr>
# <tr><td>7</td><td>12500.0</td></tr>
# </table>
#
# \section VitaEnable_NDR308-1 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>VITA-49 header disabled</td></tr>
# <tr><td>1</td><td>VITA-49 header enabled, fractional timestamp in picoseconds</td></tr>
# <tr><td>2</td><td>VITA-49 header disabled</td></tr>
# <tr><td>3</td><td>VITA-49 header enabled, fractional timestamp in sample counts</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr308_1(_radio):
    _name = "NDR308-1"
    ifSpec = ndr308_ifSpec
    adcRate = 102.4e6
    numTuner = 8
    numTunerBoards = 2
    numWbddc = 8
    numNbddc = 16
    numGigE = 2
    numGigEDipEntries = 64
    tunerType = ndr308_tuner
    wbddcType = ndr308_wbddc
    nbddcType = ndr308_1_nbddc
    numWbddcGroups = 4
    wbddcGroupIndexBase = 1
    wbddcGroupType = ndr308_wbddc_group
    numNbddcGroups = 8
    nbddcGroupIndexBase = 1
    nbddcGroupType = ndr308_nbddc_group
    statQry = stat308
    tstatQry = tstat308
    tadjCmd = command.tadj
    ppsCmd = command.pps
    utcCmd = command.utc
    rbypCmd = command.rbyp
    sipCmd = sip308
    dipCmd = dip308
    smacCmd = None
    dmacCmd = None
    calfCmd = command.calf
    fnrCmd = command.fnr
    gpsCmd = command.gps
    gposCmd = command.gpos
    rtvCmd = command.rtv
    tempCmd = command.temp
    gpioStaticCmd = command.gpio_static
    gpioSeqCmd = command.gpio_sequence
    resetCmd = None
    refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz",3:"External 1PPS",4:"External 1PPS"}
    rbypModes = {0:"Internal 102.4MHz",1:"External 102.4MHz"}
    connectionModes = ["tcp"]
    defaultPort = 8617
    udpDestInfo = "DIP table index"
    vitaEnableOptions = {0: "VITA-49 header disabled",
                         1: "VITA-49 header enabled, fractional timestamp in picoseconds",
                         2: "VITA-49 header disabled",
                         3: "VITA-49 header enabled, fractional timestamp in sample counts",
                         }
    
    def configureDipTable(self,index,sip,dip,dmac,udpBase):
        success = True
        x = [ int(i) for i in dip.split(".") ]
        x[-1]+=10
        sipCmd = command.radio_command( parent=self, cmdString="SIP %d,%s"%(index,sip) )
        success &= sipCmd.send( self.sendCommand )
        if success:
            self.sipTable[index] = sip
        self.dipTable[index] = {}
        for i in range(32):
            args = ", ".join( [str(i) for i in (index,i,dip,dmac,udpBase+i,udpBase+i)] )
            dipCmd = command.radio_command( parent=self, cmdString="DIP %s"%args )
            success &= dipCmd.send( self.sendCommand )
            if success:
                self.dipTable[index][i] = {"dip":dip,"dport":udpBase+i,"sport":udpBase+i,"sip":self.sipTable.get(index,None),}
        return success
    
    def getDipTableEntry(self,ifIndex=None,dipIndex=None):
        if ifIndex is None:
            return self.dipTable
        elif dipIndex is None:
            return self.dipTable.get(ifIndex,{})
        else:
            return self.dipTable.get(ifIndex,{}).get(dipIndex,{})

    def disableTenGigFlowControl(self,):
        return self.setTenGigFlowControlStatus(False)
    
    def enableTenGigFlowControl(self,):
        return self.setTenGigFlowControlStatus(True)
    
    def setTenGigFlowControlStatus(self,enable=False):
        success = False
        if self.tgfcCmd is not None and self.tgfcCmd.settable:
            confDict = {
                    configKeys.CONFIG_IP: {
                        }
                }
            for gigEPortNum in xrange(self.gigEIndexBase, 
                                      self.gigEIndexBase + self.numGigE, 1):
                confDict[configKeys.CONFIG_IP][gigEPortNum] = {
                        configKeys.GIGE_FLOW_CONTROL: 1 if enable else 0,
                    }
            success = self.setConfiguration(confDict)
        return success
    
    def getTenGigFlowControlStatus(self,):
        status = {}
        if self.tgfcCmd is not None:
            confDict = self.getConfiguration()[configKeys.CONFIG_IP]
            for gigEPortNum in xrange(self.gigEIndexBase, 
                                      self.gigEIndexBase + self.numGigE, 1):
                if configKeys.GIGE_FLOW_CONTROL in confDict[gigEPortNum]:
                    status |= (confDict[gigEPortNum][configKeys.GIGE_FLOW_CONTROL]    == 1)
        return status

##
# \brief Radio handler class for the NDR308.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4],
#      "bypassMode": [0, 1],
#      "freqNormalization": [0, 1],
#      "gpsEnable": [0, 1],
#      "referenceTuningVoltage": [0-65535],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#               "filter": [0, 1],
#               "timingAdjustment": [-200000 - 200000, step 1],
#            },
#         ...8 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0, 1, 2],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#                 "dataPort": [1, 2],
#              },
#           ...8 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#                 "rfIndex": [1, 2, 3, 4, 5, 6, 7, 8],
#                 "dataPort": [1, 2],
#              },
#           ...32 (repeat for each NBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...4 (repeat for each WBDDC group)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...8 (repeat for each NBDDC group)
#         },
#      },
#      "ipConfiguration": {
#            1: {
#               "sourceIP": [IP address],
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "sourcePort": [port],
#                      "destPort": [port],
#                   },
#                ...31 (repeat for each DIP table entry)
#               },
#               "flowControl": [0, 1],
#            },
#         ...2 (repeat for each Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \section WbddcRates_NDR308 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>61440000.0</td></tr>
# <tr><td>1</td><td>30720000.0</td></tr>
# <tr><td>2</td><td>15360000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308 NBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>NBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>1920000.0</td></tr>
# <tr><td>1</td><td>960000.0</td></tr>
# <tr><td>2</td><td>480000.0</td></tr>
# <tr><td>3</td><td>180000.0</td></tr>
# <tr><td>4</td><td>60000.0</td></tr>
# <tr><td>5</td><td>30000.0</td></tr>
# <tr><td>6</td><td>15000.0</td></tr>
# </table>
#
# \section VitaEnable_NDR308 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>VITA-49 header disabled</td></tr>
# <tr><td>1</td><td>VITA-49 header enabled, fractional timestamp in picoseconds</td></tr>
# <tr><td>2</td><td>VITA-49 header disabled</td></tr>
# <tr><td>3</td><td>VITA-49 header enabled, fractional timestamp in sample counts</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr308(ndr308_1):
    _name = "NDR308"
    numGigEDipEntries = 128
    numNbddc = 32
    wbddcType = ndr308_wbddc
    nbddcType = ndr308_nbddc
    tgfcCmd = command.tgfc
    resetCmd = None


##
# \brief Radio handler class for the NDR308 4-tuner variety.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308_4 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4],
#      "bypassMode": [0, 1],
#      "freqNormalization": [0, 1],
#      "gpsEnable": [0, 1],
#      "referenceTuningVoltage": [0-65535],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#               "filter": [0, 1],
#               "timingAdjustment": [-200000 - 200000, step 1],
#            },
#         ...4 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0, 1, 2],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#                 "dataPort": [1, 2],
#              },
#           ...4 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#                 "rfIndex": [1, 2, 3, 4],
#                 "dataPort": [1, 2],
#              },
#           ...4 (repeat for each NBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...4 (repeat for each WBDDC group)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...8 (repeat for each NBDDC group)
#         },
#      },
#      "ipConfiguration": {
#            1: {
#               "sourceIP": [IP address],
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "sourcePort": [port],
#                      "destPort": [port],
#                   },
#                ...31 (repeat for each DIP table entry)
#               },
#               "flowControl": [0, 1],
#            },
#         ...2 (repeat for each Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \section WbddcRates_NDR308_4 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>61440000.0</td></tr>
# <tr><td>1</td><td>30720000.0</td></tr>
# <tr><td>2</td><td>15360000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308_4 NBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>NBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>1920000.0</td></tr>
# <tr><td>1</td><td>960000.0</td></tr>
# <tr><td>2</td><td>480000.0</td></tr>
# <tr><td>3</td><td>180000.0</td></tr>
# <tr><td>4</td><td>60000.0</td></tr>
# <tr><td>5</td><td>30000.0</td></tr>
# <tr><td>6</td><td>15000.0</td></tr>
# </table>
#
# \section VitaEnable_NDR308_4 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>VITA-49 header disabled</td></tr>
# <tr><td>1</td><td>VITA-49 header enabled, fractional timestamp in picoseconds</td></tr>
# <tr><td>2</td><td>VITA-49 header disabled</td></tr>
# <tr><td>3</td><td>VITA-49 header enabled, fractional timestamp in sample counts</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr308_4(ndr308):
    _name = "NDR308-4"
    numTuner = 4
    numWbddc = 4
    numNbddc = 4


##
# \brief Radio handler class for the NDR308-TS.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308-TS Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308-TS Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4],
#      "bypassMode": [0, 1],
#      "freqNormalization": [0, 1],
#      "gpsEnable": [0, 1],
#      "referenceTuningVoltage": [0-65535],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-46.0, step 1.0],
#               "enable": [0, 1],
#               "filter": [0, 1],
#               "timingAdjustment": [-200000 - 200000, step 1],
#            },
#         ...8 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0, 1, 2],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#                 "dataPort": [1, 2],
#              },
#           ...8 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#                 "dataPort": [1, 2],
#              },
#           ...16 (repeat for each NBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...4 (repeat for each WBDDC group)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...8 (repeat for each NBDDC group)
#         },
#      },
#      "ipConfiguration": {
#            1: {
#               "sourceIP": [IP address],
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "sourcePort": [port],
#                      "destPort": [port],
#                   },
#                ...31 (repeat for each DIP table entry)
#               },
#               "flowControl": [0, 1],
#            },
#         ...2 (repeat for each Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \section WbddcRates_NDR308-TS WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>61440000.0</td></tr>
# <tr><td>1</td><td>30720000.0</td></tr>
# <tr><td>2</td><td>15360000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308-TS NBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>NBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>1920000.0</td></tr>
# <tr><td>1</td><td>960000.0</td></tr>
# <tr><td>2</td><td>480000.0</td></tr>
# <tr><td>3</td><td>180000.0</td></tr>
# <tr><td>4</td><td>60000.0</td></tr>
# <tr><td>5</td><td>30000.0</td></tr>
# <tr><td>6</td><td>15000.0</td></tr>
# </table>
#
# \section VitaEnable_NDR308-TS VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>VITA-49 header disabled</td></tr>
# <tr><td>1</td><td>VITA-49 header enabled, fractional timestamp in picoseconds</td></tr>
# <tr><td>2</td><td>VITA-49 header disabled</td></tr>
# <tr><td>3</td><td>VITA-49 header enabled, fractional timestamp in sample counts</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr308_ts(ndr308):
    _name = "NDR308-TS"
    adcRate = 122.88e6
    wbddcType = ndr308ts_wbddc
    nbddcType = ndr308ts_nbddc


if __name__ == '__main__':
    pass
