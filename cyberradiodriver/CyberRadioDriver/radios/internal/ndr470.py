#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr470 
# \brief NDR470 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import stat, tstat
from CyberRadioDriver.components import _tuner, _wbddc, _nbddc
from CyberRadioDriver.radio import _ifSpec, _radio
# Imports from external modules
# Python standard library imports


##
# \internal
# \brief Status command bitmask values for the NDR470.
#
# \copydetails CyberRadioDriver::radios::ndr308::stat308Values
class stat470Values():
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
# \brief Status command specific to the NDR470.
#
# \copydetails CyberRadioDriver::command::stat
class stat470(stat):
    statTextValues = stat470Values.text
    
    
##
# \internal
# \brief Tuner RF status command bitmask values for the NDR470.
#
# \copydetails CyberRadioDriver::radios::ndr308::stat308Values
class tstat470Values():
    RF1_LO1_UNLOCKED = 0x1
    RF1_LO2_UNLOCKED = 0x2
    RF1_LO3_UNLOCKED = 0x4
    RF1_LO4_UNLOCKED = 0x8
    T1_64MHZ_UNLOCKED = 0x10
    T2_64MHZ_UNLOCKED = 0x20
    CH1_LO1_UNLOCK = 0x100
    CH1_LO2_UNLOCK = 0x200
    CH2_LO1_UNLOCK = 0x400
    CH2_LO2_UNLOCK = 0x800
    CH3_LO1_UNLOCK = 0x1000
    CH3_LO2_UNLOCK = 0x2000
    CH4_LO1_UNLOCK = 0x4000
    CH4_LO2_UNLOCK = 0x8000
    
    text = {
        RF1_LO1_UNLOCKED: "RF Channel 1, RFMD LO Unlock", \
        RF1_LO2_UNLOCKED: "RF Channel 2, RFMD LO Unlock", \
        RF1_LO3_UNLOCKED: "RF Channel 3, RFMD LO Unlock", \
        RF1_LO4_UNLOCKED: "RF Channel 4, RFMD LO Unlock", \
        T1_64MHZ_UNLOCKED: "Tuner Board 1, 64MHz Ref Unlock", \
        T2_64MHZ_UNLOCKED: "Tuner Board 2, 64MHz Ref Unlock", \
        CH1_LO1_UNLOCK: "Channel 1 uTune LO1 Unlock", \
        CH1_LO2_UNLOCK: "Channel 1 uTune LO2 Unlock", \
        CH2_LO1_UNLOCK: "Channel 2 uTune LO1 Unlock", \
        CH2_LO2_UNLOCK: "Channel 2 uTune LO2 Unlock", \
        CH3_LO1_UNLOCK: "Channel 3 uTune LO1 Unlock", \
        CH3_LO2_UNLOCK: "Channel 3 uTune LO2 Unlock", \
        CH4_LO1_UNLOCK: "Channel 4 uTune LO1 Unlock", \
        CH4_LO2_UNLOCK: "Channel 4 uTune LO2 Unlock", \
        }


##
# \internal
# \brief Tuner RF status command specific to the NDR470.
#
# \copydetails CyberRadioDriver::command::tstat
class tstat470(tstat):
    statTextValues = tstat470Values.text


##
# \internal
# \brief Tuner component class for the NDR470.
#
class ndr470_tuner(_tuner):
    _name = "Tuner(NDR470)"


##
# \internal
# \brief WBDDC component class for the NDR470.
class ndr470_wbddc(_wbddc):
    _name = "WBDDC(NDR470)"
    rateSet = {     0: 16e6, \
                    1: 8e6, \
                    2: 4e6, \
                    3: 2e6, \
                    4: 1e6, \
                    5: 500e3, \
                }
    bwSet = {     0: 10e6, \
                    1: 0.8*8e6, \
                    2: 0.8*4e6, \
                    3: 0.8*2e6, \
                    4: 0.8*1e6, \
                    5: 0.8*500e3, \
                }
    tunable = True
    frqRange = (-25.6e6,25.6e6,)
    frqRes = 100e3
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
# \brief NBDDC component class for the NDR470.
class ndr470_nbddc(_nbddc):
    _name = "NBDDC(NDR470)"
    rateSet = {     0: 480e3, \
                    1: 96.0e3, \
                    2: 48.0e3, \
                    3: 38.4e3, \
                    4: 28.8e3, \
                    5: 24.0e3, \
                    6: 9.6e3, \
                    7: 4.8e3, \
                }
    bwSet = {     0: 0.8*480e3, \
                    1: 0.8*96.0e3, \
                    2: 0.8*48.0e3, \
                    3: 0.8*38.4e3, \
                    4: 0.8*28.8e3, \
                    5: 0.8*24.0e3, \
                    6: 0.8*9.6e3, \
                    7: 0.8*4.8e3, \
                }
    tunable = True
    frqRange = (-25.6e6,25.6e6,)
    frqRes = 100e3


##
# \internal
# \brief VITA 49 interface specification class for the NDR470.
class ndr470_ifSpec(_ifSpec):
    headerSizeWords = 7
    payloadSizeWords = 288
    tailSizeWords = 1
    byteOrder = "big"


##
# \brief Radio handler class for the NDR470.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR470 Connection Modes
#
# "tty"
#
# \section RadioConfig_NDR470 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#            },
#         ...4 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5],
#                 "udpDest": [port],
#                 "vitaEnable": [0, 1, 2],
#                 "streamId": [stream ID],
#                 "frequency": [-8000.0-8000.0, step 100],
#              },
#           ...4 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-8000000.0-8000000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6, 7],
#                 "udpDest": [port],
#                 "vitaEnable": [0, 1, 2],
#                 "streamId": [stream ID],
#                 "rfIndex": [1, 2, 3, 4],
#              },
#           ...32 (repeat for each NBDDC)
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
# \section WbddcRates_NDR470 WBDDC Rate Settings
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
# \section NbddcRates_NDR470 NBDDC Rate Settings
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
# \section VitaEnable_NDR470 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>Vita49 and Vita49.1 disabled</td></tr>
# <tr><td>1</td><td>Vita49 enabled and Vita 49.1 disabled</td></tr>
# <tr><td>2</td><td>Vita 49 and Vita 49.1 enabled</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr470(_radio):
    _name = "NDR470"
    ifSpec = ndr470_ifSpec
    adcRate = 64e6
    numTuner = 4
    numWbddc = 4
    numNbddc = 32
    tunerType = ndr470_tuner
    wbddcType = ndr470_wbddc
    nbddcType = ndr470_nbddc
    statQry = stat470
    tstatQry = tstat470
    refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz",3:"External 1PPS",}    
    udpDestInfo = "port"
    connectionModes = ["tty","tcp"]
    vitaEnableOptions = {0: "Vita49 and Vita49.1 disabled",
                         1: "Vita49 enabled and Vita 49.1 disabled",
                         2: "Vita 49 and Vita 49.1 enabled",
                         }
    tunerBandwithSettable = False
    tunerBandwidthConstant = 10e6


        
if __name__ == '__main__':
    pass
