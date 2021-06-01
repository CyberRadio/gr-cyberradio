#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr3585 
# \brief ndr3585 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver.radios.ndr551 import ndr551, \
                                           ndr551_tuner, \
                                           ndr551_wbddc, \
                                           ndr551_nbddc, \
                                           ndr551_ddc_group, \
                                           ndr551_ddc_ifSpec
# Imports from external modules
# Python standard library imports

##
# \brief Tuner component class for the ndr3585.
#
class ndr3585_tuner(ndr551_tuner):
    _name = "Tuner(ndr3585)"
    frqRange = (20e6,6e9)

##
# \brief WBDDC component class for the ndr3585.
class ndr3585_wbddc(ndr551_wbddc):
    _name = "WBDDC(ndr3585)"
    rateSet = { 41 : 125e6 }
    bwSet = { 41 : 80e6 }

##
# \brief NBDDC component class for the ndr3585.
class ndr3585_nbddc(ndr551_nbddc):
    _name = "NBDDC(ndr3585)"
    rateSet = { 19 : 25e6,
                18 : 12.5e6,
                17 : 6.25e6 }
    bwSet = { 19 : 25e6,
              18 : 10e6,
              17 : 5e6 }

##
# \brief NBDDC component class for the ndr3585.
class ndr3585_ddc_group(ndr551_ddc_group):
    _name = "DDCGroup(ndr3585)"

##
# \internal
# \brief VITA 49 interface specification class for the ndr3585.
class ndr3585_ifSpec(ndr551_ddc_ifSpec):
    pass 

##
# \brief Radio handler class for the ndr3585.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_ndr3585 Connection Modes
#
# "udp"
#
# \section RadioConfig_ndr3585 Radio Configuration Options
#
# \code
# configDict = {
#      "referenceMode": [0, 1],
#      "function": [integer (meaning is radio-dependent],
#      "tunerConfiguration": {
#            0: {
#               "preselectorBypass": [True, False], 
#               "frequency": [20000000.0-6000000000.0, step 1000000.0],
#               "attenuation": [0.0-40.0, step 1.0],
#               "enable": [True, False],
#               "ifFilter": [3, 10, 40, 80],
#               "delay": [0.0-1.0, step 8e-6],
#               "fnr": [True, False],
#               "gainMode": ["auto", "manual", "freeze"],
#               "asp": [-40.0-0.0, step 1.0],
#               "aul": [-40.0-0.0, step 1.0],
#               "all": [-40.0-0.0, step 1.0],
#               "aat": [1.0-128.0, step 1.0],
#               "adt": [1.0-128.0, step 1.0],
#               "aas": [0.0-40.0, step 1.0],
#               "ads": [0.0-40.0, step 1.0],
#               "aal": [1.0-30.0, step 1.0],
#               "adl": [1.0-30.0, step 1.0],
#            },
#         ...7 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              0: {
#                 "enable": [True, False],
#                 "rfIndex": ["0", "1", "2", "3"],
#                 "outputType": ["iq", "raw"],
#                 "frequency": [-40e6-40e6, step 1e3],
#                 "decimation": [1, 2, 4, 8, 16],
#                 "filterIndex": [32-63, step 1],
#                 "oversampling": [1, 2, 4],
#                 "startTime": [start time],
#                 "samples": [samples],
#                 "udpDest": [UDP destination table index],
#                 "streamId": [stream ID],
#                 "link": [0, 1, 2, 3],
#                 "gainMode": ["auto", "manual", "freeze"],
#                 "dgv": [0.0-96.0, step 1.0],
#                 "dul": [0.0-96.0, step 1.0],
#                 "dll": [0.0-96.0, step 1.0],
#                 "dtl": [-96.0-0.0, step 0.5],
#                 "dal": [0.0-30.0, step 0.5],
#                 "ddl": [0.0-30.0, step 0.5],
#                 "dao": [0.0-24.0, step 0.5],
#                 "ddo": [0.0-24.0, step 0.5],
#                 "datc": [10-3000, step 10],
#                 "ddtc": [10-3000, step 10],
#                 "dat": [1-100, step 1],
#                 "ddt": [1-100, step 1],
#              },
#           ...7 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              0: {
#                 "enable": [True, False],
#                 "frequency": [-40e6-40e6, step 1e3],
#                 "rfIndex": ["0", "1", "2", "3"],
#                 "filterIndex": [0-31 step 1, 64-4095 step 1],
#                 "cic0": [4-500, step 1],
#                 "cic1": [1, 4-500, step 1],
#                 "oversampling": [1, 2, 4, 8, 16],
#                 "demod": ["none", "cw", "fm", "am", "usb", "lsb"],
#                 "demodGain": [gain],
#                 "audioDecimation": [True, False],
#                 "bfo": [-12e3-12e3, step 1],
#                 "startTime": [ISO 8601 time string],
#                 "samples": [number of samples],
#                 "udpDest": [UDP destination table index],
#                 "streamId": [stream ID],
#                 "gainMode": ["auto", "manual", "freeze"],
#                 "dgv": [0.0-96.0, step 1.0],
#                 "dul": [0.0-96.0, step 1.0],
#                 "dll": [0.0-96.0, step 1.0],
#                 "dtl": [-96.0-0.0, step 0.5],
#                 "dal": [0.0-30.0, step 0.5],
#                 "ddl": [0.0-30.0, step 0.5],
#                 "dao": [0.0-24.0, step 0.5],
#                 "ddo": [0.0-24.0, step 0.5],
#                 "datc": [10-3000, step 10],
#                 "ddtc": [10-3000, step 10],
#                 "dat": [1-100, step 1],
#                 "ddt": [1-100, step 1],
#              },
#           ...63 (repeat for each NBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#            "combined": {
#                0: {
#                   "enable": [True, False],
#                   "wbddcMembers": [None, a single WBDDC, or a Python list of WBDDCs],
#                   "nbddcMembers": [None, a single NBDDC, or a Python list of NBDDCs],
#                },
#             ...15 (repeat for each DDC group)
#            },
#      },
#      "ipConfiguration": {
#            0: {
#               "destIP": {
#                   0: {
#                      "ipAddr": [IP address],
#                      "macAddr": [MAC address],
#                      "destPort": [port],
#                      "arp": [True, False],
#                   },
#                ...63 (repeat for each UDP destination index)
#               },
#               "sourceIP": {
#                   "ipAddr": [IP address],
#                   "macAddr": [MAC address],
#                   "netmask": [netmask],
#                   "sourcePort": [port],
#               },
#            },
#         ...3 (repeat for each 10-Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \implements CyberRadioDriver.IRadio    
class ndr3585(ndr551):
    _name = "ndr3585"
    ifSpec = ndr3585_ifSpec
    tunerType = ndr3585_tuner
    numTuner = 8
    wbddcType = ndr3585_wbddc
    numWbddc = 8
    nbddcType = ndr3585_nbddc
    cddcGroupType = ndr3585_ddc_group

class ndr3585_coherent(ndr3585):
    _name = "ndr3585-Coherent"
    numWbddc = 16

if __name__ == '__main__':
    pass
