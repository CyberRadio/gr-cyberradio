#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr651 
# \brief NDR651 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import command
from CyberRadioDriver.components import wbddc_group, nbddc_group, \
                                        wbduc_group, \
                                        DDC_DATA_FORMAT, _cwToneGen, \
                                        _tx, _wbduc
from CyberRadioDriver.radios.ndr308 import ndr308_tuner, ndr308_wbddc, \
                                           ndr308_nbddc, ndr308
# Imports from external modules
# Python standard library imports


##
# Tuner component class for the NDR651.
#
class ndr651_tuner(ndr308_tuner):
    _name = "Tuner(NDR651)"

        
##
# WBDDC component class for the NDR651.
class ndr651_wbddc(ndr308_wbddc):
    _name = "WBDDC(NDR651)"
    rateSet = { 0: 51.2e6, \
                1: 25.6e6, \
                2: 12.8e6, \
                3: 102.4e6, \
                4: 6.4e6, \
                5: 3.2e6, \
                 }
    dataFormat = { 3:DDC_DATA_FORMAT.REAL }
    bwSet = { 0: 40e6, \
                1: 0.8*25.6e6, \
                2: 0.8*12.8e6, \
                4: 0.8*6.4e6, \
                5: 0.8*3.2e6, \
                 }


##
# NBDDC component class for the NDR651.
class ndr651_nbddc(ndr308_nbddc):
    _name = "NBDDC(NDR651)"


##
# Continuous-wave (CW) tone generator component class for the NDR651.
#
class ndr651_cwToneGen(_cwToneGen):
    _name = "CWToneGen(NDR651)"


##
# Transmitter component class for the NDR651.
class ndr651_tx(_tx):
    _name = "TX(NDR651)"
    numToneGen = 2
    toneGenType = ndr651_cwToneGen
    attRange = (0.0,16.0)
    attRes = 0.5

##
# WBDUC component class for the NDR651.
class ndr651_wbduc(_wbduc):
    _name = "WBDUC(NDR651)"
    snapshotLoadCmd = command.lwf
    #snapshotTxCmd = command.txsd
    snapshotTxCmd = command.pwf


##
# WBDDC group component class specific to the NDR651.
#
# A WBDDC group component object maintains one WBDDC group on the radio.  
#
class ndr651_wbddc_group(wbddc_group):
    _name = "WBDDCGroup(NDR651)"
    ## \brief Group member index base (what number indices start at) 
    groupMemberIndexBase = 1
    ## \brief Number of potential group members 
    numGroupMembers = 2


##
# NBDDC group component class specific to the NDR651.
#
# A NBDDC group component object maintains one NBDDC group on the radio.  
#
class ndr651_nbddc_group(nbddc_group):
    _name = "NBDDCGroup(NDR651)"
    ## \brief Group member index base (what number indices start at) 
    groupMemberIndexBase = 1
    ## \brief Number of potential group members 
    numGroupMembers = 16


##
# WBDUC group component class specific to the NDR651.
#
# A WBDUC group component object maintains one WBDUC group on the radio.  
#
class ndr651_wbduc_group(wbduc_group):
    _name = "WBDUCGroup(NDR651)"
    ## \brief Group member index base (what number indices start at) 
    groupMemberIndexBase = 1
    ## \brief Number of potential group members 
    numGroupMembers = 4


##
# \brief Radio handler class for the NDR651.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR651 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR651 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4],
#      "bypassMode": [0, 1],
#      "calibFrequency": [0, 25.0-6000.0],
#      "freqNormalization": [0, 1],
#      "gpsEnable": [0, 1],
#      "referenceTuningVoltage": [0-65535],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-6000000000.0, step 1000000.0],
#               "attenuation": [0.0-46.0, step 1.0],
#               "enable": [0, 1],
#               "filter": [0, 1],
#               "timingAdjustment": [-200000 - 200000, step 1],
#            },
#         ...2 (repeat for each tuner)
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
#           ...2 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6, 7],
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
#      "txConfiguration": {
#            1: {
#               "frequency": [200000000.0-6000000000.0, step 1000000.0],
#               "attenuation": [0.0-15.0, step 1.0],
#               "enable": [0, 1],
#               "cwConfiguration": {
#                     1: {
#                        "cwFrequency": [-51200000.0-51200000.0, step 1],
#                        "cwAmplitude": [0-65535, step 1],
#                        "cwPhase": [-180-180, step 1],
#                        "cwSweepStart": [-51200000.0-51200000.0, step 1],
#                        "cwSweepStop": [-51200000.0-51200000.0, step 1],
#                        "cwSweepStep": [-51200000.0-51200000.0, step 1],
#                        "cwSweepDwell": [0-4294967295, step 1],
#                     },
#                  ...2 (repeat for each tone generator)
#               },
#            },
#         ...2 (repeat for each transmitter)
#      },
#      "ducConfiguration": {
#         "wideband": {
#              1: {
#                 "dataPort": [0, 1, 2],
#                 "frequency": [-51200000.0 - 51200000.0],
#                 "attenuation": [-60.0 - 60.0, step 0.1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 20],
#                 "txChannels": [0, 1, 2, 3],
#                 "mode": [0 for streaming, 1 for snapshot],
#                 "streamId": [stream ID],
#                 "filename": [snapshot filename],
#                 "startSample": [starting sample number in snapshot],
#                 "samples": [number of samples in snapshot],
#                 "singlePlayback": [0 for no, 1 for yes],
#              },
#           ...8 (repeat for each WBDUC)
#         },
#      },
#      "ducGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DUC, or iterable with multiple DUCs],
#              },
#           ...4 (repeat for each WBDUC group)
#         },
#      },
# }
# \endcode
#
# \section WbddcRates_NDR651 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>51200000.0</td></tr>
# <tr><td>1</td><td>25600000.0</td></tr>
# <tr><td>2</td><td>12800000.0</td></tr>
# <tr><td>3</td><td>102400000.0</td></tr>
# <tr><td>4</td><td>6400000.0</td></tr>
# <tr><td>5</td><td>3200000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR651 NBDDC Rate Settings
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
# \section WbducRates_NDR651 WBDUC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDUC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>102400000.0</td></tr>
# <tr><td>1</td><td>51200000.0</td></tr>
# <tr><td>2</td><td>25600000.0</td></tr>
# <tr><td>3</td><td>12800000.0</td></tr>
# <tr><td>4</td><td>6400000.0</td></tr>
# <tr><td>5</td><td>3200000.0</td></tr>
# <tr><td>6</td><td>1600000.0</td></tr>
# <tr><td>7</td><td>800000.0</td></tr>
# <tr><td>8</td><td>400000.0</td></tr>
# <tr><td>9</td><td>200000.0</td></tr>
# <tr><td>10</td><td>100000.0</td></tr>
# <tr><td>11</td><td>50000.0</td></tr>
# <tr><td>12</td><td>25000.0</td></tr>
# <tr><td>13</td><td>12500.0</td></tr>
# <tr><td>16</td><td>270833.0</td></tr>
# <tr><td>20</td><td>5600000.0</td></tr>
# </table>
#
# \section VitaEnable_NDR651 VITA 49 Enabling Options
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
class ndr651(ndr308):
    _name = "NDR651"
    numTuner = 2
    numTunerBoards = 1
    numWbddc = 2
    tunerType = ndr651_tuner
    tunerIndexBase = 1
    numGigEDipEntries = 32
    numNbddc = 16
    wbddcType = ndr651_wbddc
    nbddcType = ndr651_nbddc
    numWbddcGroups = 4
    wbddcGroupIndexBase = 1
    wbddcGroupType = ndr651_wbddc_group
    numNbddcGroups = 8
    nbddcGroupIndexBase = 1
    nbddcGroupType = ndr651_nbddc_group
    numTxs = 2
    txType = ndr651_tx
    numWbduc = 8
    wbducType = ndr651_wbduc
    numWbducGroups = 4
    wbducGroupIndexBase = 1
    wbducGroupType = ndr651_wbduc_group
    numNbduc = 0
    nbducType = None


##
# \internal
# \brief Special version of the radio handler class for the NDR651, for Dave M.
#
class ndr651dm(ndr651):
    _name = "NDR651dm"
    numTuner = 2
    numWbddc = 4


if __name__ == '__main__':
    pass
