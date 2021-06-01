#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr303 
# \brief NDR303 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import command
from CyberRadioDriver import configKeys
from CyberRadioDriver.radios.ndr304 import fif304, stat304, tstat304, \
                                           ndr304_ifSpec, ndr304_tuner, ndr304
# Imports from external modules
# Python standard library imports


##
# Tuner filter setting command specific to the NDR303.
#
class fif303(fif304):
    mnemonic = "FIF"


        
##
# Tuner component class for the NDR303.
#
class ndr303_tuner(ndr304_tuner):
    _name = "Tuner(NDR303)"
    fifCmd = fif303
    tadjCmd = None
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY, 
                                  configKeys.TUNER_ATTENUATION, 
                                  configKeys.TUNER_RF_ATTENUATION,
                                  configKeys.ENABLE, 
                                  configKeys.TUNER_FILTER,
                                  ]


##
# \brief Radio handler class for the NDR303.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR303 Connection Modes
#
# "tty"
#
# \implements CyberRadioDriver::IRadio
class ndr303(ndr304):
    _name = "NDR303"
    ifSpec = ndr304_ifSpec
    adcRate = 102.4e6
    numTuner = 6
    numWbddc = 0
    numNbddc = 0
    tunerType = ndr303_tuner
    wbddcType = None
    nbddcType = None
    statQry = stat304
    tstatQry = tstat304
    tadjCmd = command.tadj
    rbypCmd = None
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
