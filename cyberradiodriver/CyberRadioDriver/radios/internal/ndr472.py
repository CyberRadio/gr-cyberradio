#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr472 
# \brief NDR472 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import command
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import stat, tstat
from CyberRadioDriver.components import _tuner, _wbddc, _nbddc, \
                                        wbddc_group
from CyberRadioDriver.radio import _radio
from CyberRadioDriver.radios.internal import ndr470
# Imports from external modules
# Python standard library imports


##
# \internal
# \brief Status command bitmask values for the NDR472.
#
# \copydetails CyberRadioDriver::radios::ndr308::stat308Values
class stat472Values():
    RF_TUNER_UNLOCKED = 0x01
    ADC_OVERFLOW = 0x02
    REF_UNLOCKED = 0x04
    POWER_FAILURE = 0x08
    OVER_TEMP = 0x10
    RT_TIMER = 0x20
    GPS_UNLOCK = 0x40
    text = {
            RF_TUNER_UNLOCKED: "RF Tuner LOs Unlocked (check TSTAT?)", \
            ADC_OVERFLOW: "ADC Overflow", \
            REF_UNLOCKED: "Reference not yet locked", \
            POWER_FAILURE: "Power failure", \
            OVER_TEMP: "Over-temp condition", \
            RT_TIMER: "Retune timer not timed-out", \
            GPS_UNLOCK: "GPS time & position unlocked", \
            }


##
# \internal
# \brief Status command specific to the NDR472.
#
# \copydetails CyberRadioDriver::command::stat
class stat472(stat):
    statTextValues = stat472Values.text


##
# \internal
# \brief Tuner RF status command bitmask values for the NDR472.
#
# \copydetails CyberRadioDriver::radios::ndr308::stat308Values
class tstat472Values():
    RF1_LO1_UNLOCKED = 0x1
    RF1_LO2_UNLOCKED = 0x2
    T1_64MHZ_UNLOCKED = 0x10
    
    CH1_LO1_UNLOCK = 0x100
    CH1_LO2_UNLOCK = 0x200
    CH2_LO1_UNLOCK = 0x400
    CH2_LO2_UNLOCK = 0x800
    
    text = {
        RF1_LO1_UNLOCKED: "RF Channel 1, RFMD LO Unlock", \
        RF1_LO2_UNLOCKED: "RF Channel 2, RFMD LO Unlock", \
        T1_64MHZ_UNLOCKED: "Tuner Board 1, 64MHz Ref Unlock", \
        CH1_LO1_UNLOCK: "Channel 1 uTune LO1 Unlock", \
        CH1_LO2_UNLOCK: "Channel 1 uTune LO2 Unlock", \
        CH2_LO1_UNLOCK: "Channel 2 uTune LO1 Unlock", \
        CH2_LO2_UNLOCK: "Channel 2 uTune LO2 Unlock", \
        }


##
# \internal
# \brief Tuner RF status command specific to the NDR472.
#
# \copydetails CyberRadioDriver::command::tstat
class tstat472(tstat):
    statTextValues = tstat472Values.text


##
# \internal
# \brief Tuner component class for the NDR472 (all flavors).
#
class ndr472_tuner(_tuner):
    _name = "Tuner(NDR472)"
    tadjCmd = command.tadj
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY, 
                                  configKeys.TUNER_ATTENUATION, 
                                  configKeys.TUNER_AGP, 
                                  configKeys.TUNER_RF_ATTENUATION,
                                  configKeys.ENABLE, 
                                  configKeys.TUNER_FILTER,
                                  configKeys.TUNER_TIMING_ADJ,
                                  ]


##
# \internal
# \brief WBDDC component class for the NDR472-1.
class ndr472_1_wbddc(_wbddc):
    _name = "WBDDC(NDR472-1)"
    rateSet = {     0: 16e6, \
                    1: 8e6, \
                    2: 4e6, \
                    3: 2e6, \
                    4: 1e6, \
                    5: 500e3, \
                }
    frqCmd = None


##
# \internal
# \brief WBDDC component class for the NDR472.
class ndr472_wbddc(_wbddc):
    _name = "WBDDC(NDR472)"
    rateSet = {     0: 12.8e6, \
                }
    frqCmd = None


##
# \internal
# \brief NBDDC component class for the NDR472.
class ndr472_nbddc(_nbddc):
    _name = "NBDDC(NDR472)"
    #_name = "NBDDC(NDR470)"
    rateSet = {     0: 480e3, \
                    1: 96.0e3, \
                    2: 48.0e3, \
                    3: 38.4e3, \
                    4: 28.8e3, \
                    5: 24.0e3, \
                    6: 9.6e3, \
                    7: 4.8e3, \
                }


##
# \internal
# \brief WBDDC group component class specific to the NDR472.
#
# A WBDDC group component object maintains one WBDDC group on the radio.  
#
class ndr472_wbddc_group(wbddc_group):
    _name = "WBDDCGroup(NDR472)"
    ## \brief Group member index base (what number indices start at) 
    groupMemberIndexBase = 1
    ## \brief Number of potential group members 
    numGroupMembers = 2


##
# \internal
# \brief VITA 49 interface specification class for the NDR472-1.
class ndr472_1_ifSpec(ndr470.ndr470_ifSpec):
    payloadSizeWords = 289
    byteOrder = "big"

##
# \internal
# \brief VITA 49 interface specification class for the NDR472.
class ndr472_ifSpec(ndr470.ndr470_ifSpec):
    byteOrder = "little"


##
# \brief Radio handler class for the NDR472-1.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR472-1 Connection Modes
#
# "tty"
#
# \section RadioConfig_NDR472-1 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#            },
#         ...2 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5],
#                 "udpDest": [port],
#                 "vitaEnable": [0, 1, 2],
#                 "streamId": [stream ID],
#              },
#           ...2 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-8000000.0-8000000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6, 7],
#                 "udpDest": [port],
#                 "vitaEnable": [0, 1, 2],
#                 "streamId": [stream ID],
#                 "rfIndex": [1, 2],
#              },
#           ...4 (repeat for each NBDDC)
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
# \section WbddcRates_NDR472-1 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>16000000.0</td></tr>
# <tr><td>1</td><td>8000000.0</td></tr>
# <tr><td>2</td><td>4000000.0</td></tr>
# <tr><td>3</td><td>2000000.0</td></tr>
# <tr><td>4</td><td>1000000.0</td></tr>
# <tr><td>5</td><td>500000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR472-1 NBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>NBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>480000.0</td></tr>
# <tr><td>1</td><td>96000.0</td></tr>
# <tr><td>2</td><td>48000.0</td></tr>
# <tr><td>3</td><td>38400.0</td></tr>
# <tr><td>4</td><td>28800.0</td></tr>
# <tr><td>5</td><td>24000.0</td></tr>
# <tr><td>6</td><td>9600.0</td></tr>
# <tr><td>7</td><td>4800.0</td></tr>
# </table>
#
# \section VitaEnable_NDR472-1 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>Vita49 and Vita49.1 disabled</td></tr>
# <tr><td>1</td><td>Vita49 enabled and Vita 49.1 disabled</td></tr>
# <tr><td>2</td><td>Vita 49 and Vita 49.1 enabled</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr472_1(_radio):
    _name = "NDR472-1"
    ifSpec = ndr472_1_ifSpec
    adcRate = 64e6
    numTuner = 2
    numWbddc = 2
    numNbddc = 4
    tunerType = ndr472_tuner
    wbddcType = ndr472_1_wbddc
    nbddcType = ndr472_nbddc
    refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz",}
    udpDestInfo = "port"
    vitaEnableOptions = {0: "Vita49 and Vita49.1 disabled",
                         1: "Vita49 enabled and Vita 49.1 disabled",
                         2: "Vita 49 and Vita 49.1 enabled",
                         }


##
# \brief Radio handler class for the NDR472.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR472 Connection Modes
#
# "tty"
#
# \section RadioConfig_NDR472 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#               "timingAdjustment": [-32768 - 32767, step 1],
#            },
#         ...2 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0],
#                 "udpDest": [port],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#              },
#           ...2 (repeat for each WBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...2 (repeat for each WBDDC group)
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
# \section WbddcRates_NDR472 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>12800000.0</td></tr>
# </table>
#
# \section VitaEnable_NDR472 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>VITA-49 header disabled</td></tr>
# <tr><td>1</td><td>VITA-49 header enabled, fractional timestamp in picoseconds</td></tr>
# <tr><td>2</td><td>VITA-49 header disabled</td></tr>
# <tr><td>3</td><td>VITA-49 header enabled, fractional timestamp in sample counts with resolution of 128Msps</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr472(ndr472_1):
    _name = "NDR472"
    ifSpec = ndr472_ifSpec
    adcRate = 128e6
    numNbddc = 0
    wbddcType = ndr472_wbddc
    nbddcType = None
    numWbddcGroups = 2
    wbddcGroupIndexBase = 1
    wbddcGroupType = ndr472_wbddc_group
    numNbddcGroups = 0
    nbddcGroupIndexBase = 1
    nbddcGroupType = None
    ppsCmd = command.pps
    utcCmd = command.utc
    statQry = stat472
    tstatQry = tstat472
    tadjCmd = command.tadj
    refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz",3:"External 1PPS",4:"External 1PPS with jitter-optimized control loop"}
    vitaEnableOptions = {0: "VITA-49 header disabled",
                         1: "VITA-49 header enabled, fractional timestamp in picoseconds",
                         2: "VITA-49 header disabled",
                         3: "VITA-49 header enabled, fractional timestamp in sample counts with resolution of 128Msps",
                         }
    tunerBandwithSettable = False
    tunerBandwidthConstant = 10e6


        
if __name__ == '__main__':
    pass
