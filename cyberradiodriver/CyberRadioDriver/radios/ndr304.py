#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr304 
# \brief NDR304 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.  
#     All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import command
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _commandBase, stat, tstat
from CyberRadioDriver.components import _tuner, _wbddc, wbddc_group
from CyberRadioDriver.radio import _ifSpec, _radio
# Imports from external modules
# Python standard library imports


##
# \internal
# \brief Tuner filter setting command specific to the NDR304.
#
class fif304(_commandBase):
    mnemonic = "FIF"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.TUNER_FILTER,int,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.TUNER_FILTER, int, True), \
                        ]
    

##
# \internal
# \brief Status command bitmask values for the NDR304.
#
# \copydetails CyberRadioDriver::radios::ndr308::stat308Values
class stat304Values():
    RF_TUNER_UNLOCKED = 0x01
    ADC_OVERFLOW = 0x02
    REF_UNLOCKED = 0x04
    POWER_FAILURE = 0x08
    OVER_TEMP = 0x10
    RT_TIMER = 0x20
#    GPS_UNLOCK = 0x40
    text = {
            RF_TUNER_UNLOCKED: "RF Tuner LOs Unlocked (check TSTAT?)", \
            ADC_OVERFLOW: "ADC Overflow", \
            REF_UNLOCKED: "Reference not yet locked", \
            POWER_FAILURE: "Power failure", \
            OVER_TEMP: "Over-temp condition", \
            RT_TIMER: "Retune timer not timed-out", \
#            GPS_UNLOCK: "GPS time & position unlocked", \
            }


##
# \internal
# \brief Status command specific to the NDR304.
#
# \copydetails CyberRadioDriver::command::stat
class stat304(stat):
    statTextValues = stat304Values.text


##
# \internal
# \brief Tuner RF status command bitmask values for the NDR304.
#
# \copydetails CyberRadioDriver::radios::ndr308::stat308Values
class tstat304Values():
    REFERENCE_UNLOCK = 0x4000
    COHERENT_LO2_UNLOCK = 0x2000
    COHERENT_LO1_UNLOCK = 0x1000
    RF_CHANNEL_6_LO1_UNLOCK = 0x800
    RF_CHANNEL_6_LO2_UNLOCK = 0x400
    RF_CHANNEL_5_LO1_UNLOCK = 0x200
    RF_CHANNEL_5_LO2_UNLOCK = 0x100
    RF_CHANNEL_4_LO1_UNLOCK = 0x80
    RF_CHANNEL_4_LO2_UNLOCK = 0x40
    RF_CHANNEL_3_LO1_UNLOCK = 0x20
    RF_CHANNEL_3_LO2_UNLOCK = 0x10
    RF_CHANNEL_2_LO1_UNLOCK = 0x8
    RF_CHANNEL_2_LO2_UNLOCK = 0x4
    RF_CHANNEL_1_LO1_UNLOCK = 0x2
    RF_CHANNEL_1_LO2_UNLOCK = 0x1
    
    text = {
        REFERENCE_UNLOCK: "100MHz Reference unlock", \
        COHERENT_LO2_UNLOCK: "Coherent LO2 unlock", \
        COHERENT_LO1_UNLOCK: "Coherent LO1 unlock", \
        RF_CHANNEL_6_LO1_UNLOCK: "RF Channel 6, LO1 unlock", \
        RF_CHANNEL_6_LO2_UNLOCK: "RF Channel 6, LO2 unlock", \
        RF_CHANNEL_5_LO1_UNLOCK: "RF Channel 5, LO1 unlock", \
        RF_CHANNEL_5_LO2_UNLOCK: "RF Channel 5, LO2 unlock", \
        RF_CHANNEL_4_LO1_UNLOCK: "RF Channel 4, LO1 unlock", \
        RF_CHANNEL_4_LO2_UNLOCK: "RF Channel 4, LO2 unlock", \
        RF_CHANNEL_3_LO1_UNLOCK: "RF Channel 3, LO1 unlock", \
        RF_CHANNEL_3_LO2_UNLOCK: "RF Channel 3, LO2 unlock", \
        RF_CHANNEL_2_LO1_UNLOCK: "RF Channel 2, LO1 unlock", \
        RF_CHANNEL_2_LO2_UNLOCK: "RF Channel 2, LO2 unlock", \
        RF_CHANNEL_1_LO1_UNLOCK: "RF Channel 1, LO1 unlock", \
        RF_CHANNEL_1_LO2_UNLOCK: "RF Channel 1, LO2 unlock", \
        }


##
# \internal
# \brief Tuner RF status command specific to the NDR304.
#
# \copydetails tstat
class tstat304(tstat):
    statTextValues = tstat304Values.text


##
# \internal
# \brief Tuner component class for the NDR304.
#
class ndr304_tuner(_tuner):
    _name = "Tuner(NDR304)"
    fifCmd = fif304
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
# \brief WBDDC component class for the NDR304.
class ndr304_wbddc(_wbddc):
    _name = "WBDDC(NDR304)"
    rateSet = { 0:102.4e6/24 }
    tunable = True
    frqRange = (-8e6,8e6,)
    frqRes = 1.0
    # OVERRIDE
    validConfigurationKeywords = [
                                  configKeys.ENABLE, 
                                  configKeys.DDC_RATE_INDEX, 
                                  configKeys.DDC_UDP_DESTINATION, 
                                  configKeys.DDC_VITA_ENABLE, 
                                  configKeys.DDC_STREAM_ID,
                                  configKeys.DDC_FREQUENCY_OFFSET, 
                                  ]


##
# \internal
# \brief WBDDC group component class specific to the NDR304.
#
# A WBDDC group component object maintains one WBDDC group on the radio.  
#
class ndr304_wbddc_group(wbddc_group):
    _name = "WBDDCGroup(NDR304)"
    ## \brief Group member index base (what number indices start at) 
    groupMemberIndexBase = 1
    ## \brief Number of potential group members 
    numGroupMembers = 6


##
# \internal
# \brief VITA 49 interface specification class for the NDR304.
class ndr304_ifSpec(_ifSpec):
    headerSizeWords = 7
    tailSizeWords = 1
    payloadSizeWords = 384
    byteOrder = "little"
    iqSwapped = True


##
# \brief Radio handler class for the NDR304.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR304 Connection Modes
#
# "tty"
#
# \section RadioConfig_NDR304 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2],
#      "bypassMode": [0, 1],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#               "filter": [0, 1],
#               "timingAdjustment": [-200000 - 200000, step 1],
#            },
#         ...6 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0],
#                 "udpDest": [port],
#                 "vitaEnable": [0, 1, 2],
#                 "streamId": [stream ID],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#              },
#           ...6 (repeat for each WBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...3 (repeat for each WBDDC group)
#         },
#      },
#      "ipConfiguration": {
#         "sourceIP": [IP address],
#         "destIP": [IP address],
#         "sourceMAC": [MAC address (read-only)],
#         "destMAC": [MAC address],
#      },
# }
# \endcode
#
# \section WbddcRates_NDR304 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>4266666.66667</td></tr>
# </table>
#
# \section VitaEnable_NDR304 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>Vita49 and Vita49.1 disabled</td></tr>
# <tr><td>1</td><td>Vita49 enabled and Vita 49.1 disabled</td></tr>
# <tr><td>2</td><td>Vita 49 and Vita 49.1 enabled</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr304(_radio):
    _name = "NDR304"
    ifSpec = ndr304_ifSpec
    adcRate = 102.4e6
    numTuner = 6
    numWbddc = 6
    numNbddc = 0
    tunerType = ndr304_tuner
    wbddcType = ndr304_wbddc
    nbddcType = None
    numWbddcGroups = 3
    wbddcGroupIndexBase = 1
    wbddcGroupType = ndr304_wbddc_group
    numNbddcGroups = 0
    nbddcGroupIndexBase = 1
    nbddcGroupType = None
    statQry = stat304
    tstatQry = tstat304
    tadjCmd = command.tadj
    rbypCmd = command.rbyp
    fnrCmd = command.fnr
    #refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz",3:"External 1PPS",4:"External 1PPS with jitter-optimized control loop"}
    refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz"}
    rbypModes = {0:"Internal 102.4MHz",1:"External 102.4MHz"}
    udpDestInfo = "port"
    vitaEnableOptions = {0: "VITA-49 header disabled",
                         1: "VITA-49 header enabled, fractional timestamp in picoseconds",
                         2: "VITA-49 header disabled",
                         3: "VITA-49 header enabled, fractional timestamp in sample counts",
                         }


if __name__ == '__main__':
    pass
