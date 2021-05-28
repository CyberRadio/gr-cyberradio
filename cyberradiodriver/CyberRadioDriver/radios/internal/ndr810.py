#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr810
# \brief NDR810 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver.radios.ndr308 import ndr308_tuner, \
                                           ndr308_wbddc, \
                                           ndr308_nbddc, \
                                           ndr308_wbddc_group, \
                                           ndr308_nbddc_group, \
                                           ndr308
# Imports from external modules
# Python standard library imports


class ndr810_tuner(ndr308_tuner):
    _name = "Tuner(NDR810)"


class ndr810_wbddc(ndr308_wbddc):
    _name = "WBDDC(NDR810)"


class ndr810_nbddc(ndr308_nbddc):
    _name = "NBDDC(NDR810)"


class ndr810_wbddc_group(ndr308_wbddc_group):
    _name = "WBDDCGroup(NDR810)"


class ndr810_nbddc_group(ndr308_nbddc_group):
    _name = "NBDDCGroup(NDR810)"


##
# \brief Radio handler class for the NDR810.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR810 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR810 Radio Configuration Options
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
# \section WbddcRates_NDR810 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>61440000.0</td></tr>
# <tr><td>1</td><td>30720000.0</td></tr>
# <tr><td>2</td><td>15360000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR810 NBDDC Rate Settings
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
# \section VitaEnable_NDR810 VITA 49 Enabling Options
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
class ndr810(ndr308):
    _name = "NDR810"

