#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr804 
# \brief NDR804 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017-2020 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import nbddc, _commandBase
from CyberRadioDriver.radios.ndr308 import ndr308_tuner, ndr308_nbddc, \
                                           ndr308_nbddc_group, ndr308
from CyberRadioDriver.radios.internal.ndr328 import ndr328_wbddc, \
                                                    ndr328_nbddc, \
                                                    dagc328

# Imports from external modules
# Python standard library imports


class ddc804(nbddc):
    mnemonic = "DDC"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.NBDDC_RF_INDEX,        int,    False,    1        ), \
                        (configKeys.DDC_FREQUENCY_OFFSET,int,    False,    0        ), \
                        (configKeys.DDC_RATE_INDEX,        int,    False,    0        ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False,    0        ), \
                        (configKeys.ENABLE,                int,    False,    0        ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False,    0        ), \
                        (configKeys.DDC_STREAM_ID,         int,    False,    0        ), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX,                 int,    False    ), \
                        (configKeys.NBDDC_RF_INDEX,     int,    False    ), \
                        (configKeys.DDC_FREQUENCY_OFFSET,int,    False    ), \
                        (configKeys.DDC_RATE_INDEX,        int,    False    ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False    ), \
                        (configKeys.ENABLE,                int,    False    ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False    ), \
                        (configKeys.DDC_STREAM_ID,        int,    False    ), \
                        ]


class wbsc804(nbddc):
    mnemonic = "WBSC"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False,    0        ), \
                        (configKeys.DDC_SPECTRAL_AVERAGE_ALPHA,    int,    False,    0), \
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
                        (configKeys.DDC_SPECTRAL_AVERAGE_ALPHA,    int,    False,    0), \
                        (configKeys.DDC_SPECTRAL_FRAME_RATE,    int,    False,    ), \
                        (configKeys.ENABLE,                int,    False    ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False    ), \
                        (configKeys.DDC_STREAM_ID,        int,    False    ), \
#                         (configKeys.DDC_RATE_INDEX,        int,    False    ), \
                        ]

# Implements the DAGC command for the NDR804-PTT
class dagc804ptt(_commandBase):
    mnemonic = "DAGC"
    setParameters = [   (configKeys.INDEX,            int,    False,    None    ), \
                        (configKeys.DDC_DGC_MODE,    int,    False,    0        ), \
                        (configKeys.DDC_DGC_GAIN,    int,    False,    0        ), \
                        ]
    queryParameters = [ (configKeys.INDEX,    int,    True,    None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX,             int,    False    ), \
                        (configKeys.DDC_DGC_MODE,    int,    False,    ), \
                        (configKeys.DDC_DGC_GAIN,    int,    False,    ), \
                        ]


class ndr804_wbddc(ndr328_wbddc):
    _name = "WidebandChannel(NDR804)"
    cfgCmd = wbsc804


class ndr804_nbddc(ndr328_nbddc):
    _name = "NBDDC(NDR804)"
    # OVERRIDE
    selectableSource = True
    # OVERRIDE
    nbssCmd = None
    
    frqRange = (-20e6,20e6,)
    cfgCmd = ddc804
    demodCmd = None
    otherCmdList = []
    rateSet = { 0: 25e3*1.25, \
                1: 50e3*1.25, \
                2: 100e3*1.25, \
                3: 200e3*1.25, \
                 }
    bwSet = { 0: 25e3, \
                1: 25e3, \
                2: 25e3, \
                3: 25e3, \
                }
    rateSets = [ { 0: 25e3*1.25, \
                    1: 25e3*2*1.25, \
                    2: 25e3*4*1.25, \
                    3: 25e3*8*1.25, \
                     },
                 { 0: 5e3*1.25, \
                    1: 5e3*2*1.25, \
                    2: 5e3*4*1.25, \
                    3: 5e3*8*1.25, \
                     },
                 ]
    bwSets = [{ 0: 25e3, \
                1: 25e3, \
                2: 25e3, \
                3: 25e3, \
                 },
                 { 0: 5e3, \
                    1: 5e3, \
                    2: 5e3, \
                    3: 5e3, \
                     },]
    
    validConfigurationKeywords = [
                                    configKeys.NBDDC_RF_INDEX, 
                                    configKeys.DDC_FREQUENCY_OFFSET, 
                                    configKeys.DDC_RATE_INDEX, 
                                    configKeys.DDC_OUTPUT_FORMAT, 
                                    configKeys.DDC_UDP_DESTINATION, 
                                    configKeys.ENABLE, 
                                    configKeys.DDC_STREAM_ID, 
                                    configKeys.DDC_DATA_PORT, 
                                  ]
    
    def __init__(self,*args,**kwargs):
        ndr308_nbddc.__init__(self,*args,**kwargs)
        if self.index<46:
            self.rateSet = self.rateSets[0]
        else:
            self.rateSet = self.rateSets[1]
#         print self._name,self.index,self.rateSet
    
    # OVERRIDE
    ##
    # Gets the list of available DDC rates.
    #
    # \return A list of DDC rates.
    @classmethod
    def getDdcRateSet(cls,index=None):
        if index is None or index<46:
            return cls.rateSets[0]
        else:
            return cls.rateSets[1]
    
    # OVERRIDE
    ##
    # Gets the list of available DDC rates.
    #
    # \return A list of DDC rates.
    @classmethod
    def getDdcBwSet(cls,index=None):
        if index is None or index<46:
            return cls.bwSets[0]
        else:
            return cls.bwSets[1]


class ndr804_ptt_nbddc(ndr328_nbddc):
    _name = "NBDDC(NDR804-PTT)"
    # OVERRIDE
    selectableSource = False
    # OVERRIDE
    nbssCmd = None
    cfgCmd = ddc804
    demodCmd = None
    rateSet = { 0: 25e3*1.25, \
                1: 50e3*1.25, \
                2: 100e3*1.25, \
                3: 200e3*1.25, \
                 }
    bwSet = { 0: 25e3, \
                1: 25e3, \
                2: 25e3, \
                3: 25e3, \
                }
    otherCmdList = [
            dagc804ptt
        ]
    validConfigurationKeywords = ndr804_nbddc.validConfigurationKeywords + [
            configKeys.DDC_DGC_MODE, 
            configKeys.DDC_DGC_GAIN, 
        ]

        
##
# \brief Radio handler class for the NDR804.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR804 Connection Modes
#
# "tcp"
#
# \implements CyberRadioDriver::IRadio
class ndr804(ndr308):
    _name = "NDR804"
    # Tuner settings
    ## \brief Number of tuners
    numTuner = 1
    ## \brief Tuner index base (what number indices start at) 
    tunerIndexBase = 1
    ## \brief Tuner component type 
    tunerType = ndr308_tuner
    # WBDDC settings
    numWbddc = 1
    ## \brief WBDDC index base (what number indices start at) 
    wbddcIndexBase = 1
    ## \brief WBDDC component type 
    wbddcType = ndr804_wbddc
    # NBDDC settings
    ## \brief Number of NBDDCs
    numNbddc = 90
    ## \brief NBDDC index base (what number indices start at) 
    nbddcIndexBase = 1
    ## \brief NBDDC component type 
    nbddcType = ndr804_nbddc
    # WBDDC Group settings
    ## \brief Number of WBDDC groups available
    numWbddcGroups = 0
    ## \brief WBDDC group index base (what number indices start at) 
    wbddcGroupIndexBase = 1
    ## \brief WBDDC Group component type 
    wbddcGroupType = None
    # NBDDC Group settings
    ## \brief Number of NBDDC groups available
    numNbddcGroups = 45
    ## \brief NBDDC group index base (what number indices start at) 
    nbddcGroupIndexBase = 1
    ## \brief NBDDC Group component type 
    nbddcGroupType = ndr308_nbddc_group
    numGigE = 2
    numGigEDipEntries = 128
    vitaEnableOptions = {0: "DDC Stream Disabled", 
                         1: "VITA-49 header disabled",
                         2: "VITA-49 header enabled, fractional timestamp in picoseconds",
                         3: "VITA-49 header enabled, fractional timestamp in sample counts",
                         }


class ndr804_ptt(ndr804):
    _name = "NDR804-PTT"
    numTuner = 8
    numWbddc = 8
    numNbddc = 100
    nbddcType = ndr804_ptt_nbddc


if __name__ == '__main__':
    pass
