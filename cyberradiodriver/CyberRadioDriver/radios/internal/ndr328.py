#!/usr/bin/env python
##################################################################
# \package CyberRadioDriver.radios.ndr328 
# \brief NDR328 Support
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
##################################################################

# Imports from other modules in this package
from CyberRadioDriver import command
from CyberRadioDriver import configKeys
from CyberRadioDriver.command import _commandBase, nbddc
from CyberRadioDriver.components import _tuner, adjustFrequency
from CyberRadioDriver.radios.ndr308 import ndr308_nbddc, ndr308
# Imports from external modules
# Python standard library imports


class ddc328(nbddc):
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


class demod328(_commandBase):
    mnemonic = "DEMOD"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.DDC_DEMOD_TYPE,        int,    False,    0        ), \
                        (configKeys.DDC_DEMOD_DC_BLOCK,    int,    False,    0        ), \
                        (configKeys.DDC_BEAT_FREQ_OSC,    int,    False,    0        ), \
                        ]
    queryParameters = [ (configKeys.INDEX,    int,    True,    None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX,                 int,    False    ), \
                        (configKeys.DDC_DEMOD_TYPE,     int,    False    ), \
                        (configKeys.DDC_DEMOD_DC_BLOCK,    int,    False,    ), \
                        (configKeys.DDC_BEAT_FREQ_OSC,int,    False    ), \
                        ]


class alc328(_commandBase):
    mnemonic = "ALC"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.DDC_DEMOD_ALC_TYPE,        int,    False,    0        ), \
                        (configKeys.DDC_DEMOD_ALC_LEVEL,    int,    False,    0        ), \
                        ]
    queryParameters = [ (configKeys.INDEX,    int,    True,    None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX,                 int,    False    ), \
                        (configKeys.DDC_DEMOD_ALC_TYPE,     int,    False    ), \
                        (configKeys.DDC_DEMOD_ALC_LEVEL,    int,    False,    ), \
                        ]


class sql328(_commandBase):
    mnemonic = "SQL"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.DDC_DEMOD_SQUELCH_LEVEL,    int,    False,    0        ), \
                        ]
    queryParameters = [ (configKeys.INDEX,    int,    True,    None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX,                 int,    False    ), \
                        (configKeys.DDC_DEMOD_SQUELCH_LEVEL,    int,    False,    ), \
                        ]


class dagc328(_commandBase):
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


class wbsc328(nbddc):
    mnemonic = "WBSC"
    setParameters = [   (configKeys.INDEX,                int,    False,    None    ), \
                        (configKeys.DDC_OUTPUT_FORMAT,    int,    False,    0        ), \
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
                        (configKeys.DDC_SPECTRAL_FRAME_RATE,    int,    False,    ), \
                        (configKeys.ENABLE,                int,    False    ), \
                        (configKeys.DDC_UDP_DESTINATION,int,    False    ), \
                        (configKeys.DDC_STREAM_ID,        int,    False    ), \
#                         (configKeys.DDC_RATE_INDEX,        int,    False    ), \
                        ]

        
##
# Tuner component class for the NDR328.
#
class ndr328_tuner(_tuner):
    _name = "Tuner(NDR328)"
    frqRange = (20e6,6e9)
    attRange = (0.0,46.0)
    fifCmd = command.fif
    ## AGP set/query command.
    agpCmd = command.agp    
    validConfigurationKeywords = [
                                  configKeys.TUNER_FREQUENCY, 
                                  configKeys.TUNER_ATTENUATION, 
                                  configKeys.TUNER_AGP, 
                                  configKeys.TUNER_RF_ATTENUATION,
                                  configKeys.ENABLE, 
                                  configKeys.TUNER_FILTER,
                                  ]


class ndr328_nbddc(ndr308_nbddc):
    _name = "NBDDC(NDR328)"
    # OVERRIDE
    selectableSource = False
    # OVERRIDE
    nbssCmd = None
    frqRange = (-20e6,20e6,)
    cfgCmd = ddc328
    frqCmd = None
    demodCmd = demod328
    otherCmdList = [alc328,
                    sql328,
                    dagc328,
                    ]
    rateSet = { 0: 250.0e3, \
                1: 125.0e3, \
                2: 62.5e3, \
                3: 25.0e3, \
                4: 12.5e3, \
                5: 6.25e3, \
                6: 6.25e3, \
                7: 2.5e3, \
                 }
    bwSet = { 0: 200.0e3, \
                1: 100.0e3, \
                2: 50.0e3, \
                3: 20.0e3, \
                4: 10.0e3, \
                5: 5.0e3, \
                6: 3.5e3, \
                7: 2.0e3, \
                 }
    validConfigurationKeywords = [
                                    configKeys.NBDDC_RF_INDEX, 
                                    configKeys.DDC_FREQUENCY_OFFSET, 
                                    configKeys.DDC_RATE_INDEX, 
                                    configKeys.DDC_OUTPUT_FORMAT, 
                                    configKeys.DDC_UDP_DESTINATION, 
                                    configKeys.ENABLE, 
                                    configKeys.DDC_STREAM_ID, 
                                    configKeys.DDC_DATA_PORT, 
                                    configKeys.DDC_DEMOD_TYPE, 
                                    configKeys.DDC_BEAT_FREQ_OSC, 
                                    configKeys.DDC_DEMOD_DC_BLOCK, 
                                    configKeys.DDC_DEMOD_ALC_TYPE, 
                                    configKeys.DDC_DEMOD_ALC_LEVEL, 
                                    configKeys.DDC_DEMOD_SQUELCH_LEVEL, 
                                    configKeys.DDC_DGC_MODE, 
                                    configKeys.DDC_DGC_GAIN, 
                                  ]
    # OVERRIDE
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        for cmdObj in [self.nbssCmd,self.dportCmd,self.cfgCmd,self.demodCmd]+self.otherCmdList:
            if cmdObj is not None:
#                 print (cmdObj.mnemonic).center(20,).center(80,"?")
                cmd = cmdObj(**{ "parent": self, 
                                   configKeys.INDEX: self.index,
                                   "query": True,
                                    "verbose": self.verbose, 
                                    "logFile": self.logFile })
                cmd.send( self.callback, )
                self._addLastCommandErrorInfo(cmd)
                rspInfo = cmd.getResponseInfo()
                keys = [i[0] for i in cmdObj.queryResponseData]
                if rspInfo is not None:
                    for key in keys:
                        self.configuration[key] = rspInfo.get(key, None)
        pass
    
    # OVERRIDE
    ##
    # \protected
    # Sets the component's current configuration.  
    def _setConfiguration(self, confDict):
        ret = True
        if configKeys.DDC_FREQUENCY_OFFSET in confDict:
            confDict[configKeys.DDC_FREQUENCY_OFFSET] = adjustFrequency(
                                  float(confDict[configKeys.DDC_FREQUENCY_OFFSET]), 
                                  self.frqRange, 
                                  self.frqRes, 
                                  self.frqUnits)
        for cmdObj in [self.nbssCmd, 
                        self.dportCmd, 
                        self.cfgCmd, 
                        self.demodCmd, 
                        ]+self.otherCmdList:
            if cmdObj is not None:
#                 print (cmdObj.mnemonic).center(20,).center(80,"!")
                keys = [ i[0] for i in cmdObj.setParameters ]
                if any([q in confDict for q in keys]):
                    cDict = {}
                    self._dictUpdate(cDict, confDict, self.configuration, keys)
                    cDict.update({ "parent": self, 
                                    configKeys.INDEX: self.index,
                                     "verbose": self.verbose, 
                                     "logFile": self.logFile })
                    cmd = cmdObj(**cDict)
                    ret &= cmd.send( self.callback, )
                    ret &= cmd.success
                    self._addLastCommandErrorInfo(cmd)
                    if ret:
                        for key in keys:
                            self.configuration[key] = getattr(cmd, key)
                    pass
        return ret


# NBDDC component class for the NDR308-TS.
class ndr328_wbddc(ndr328_nbddc):
    _name = "WidebandChannel(NDR328)"
    selectableSource = False
    rateSet = { 0: 51.2e6, }
    bwSet = { 0: 40e6, }
    cfgCmd = wbsc328
    dportCmd = command.wbdp
    demodCmd = None
    otherCmdList = []
    validConfigurationKeywords = [
                                    configKeys.DDC_OUTPUT_FORMAT,
                                    configKeys.DDC_SPECTRAL_FRAME_RATE,
                                    configKeys.ENABLE, 
                                    configKeys.DDC_UDP_DESTINATION, 
                                    configKeys.DDC_STREAM_ID, 
                                    configKeys.DDC_DATA_PORT,
                                  ]


##
# \brief Radio handler class for the NDR328.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR328 Connection Modes
#
# "tcp"
#
# \implements CyberRadioDriver::IRadio
class ndr328(ndr308):
    _name = "NDR328"
    # Tuner settings
    ## \brief Number of tuners
    numTuner = 8
    ## \brief Tuner index base (what number indices start at) 
    tunerIndexBase = 1
    ## \brief Tuner component type 
    tunerType = ndr328_tuner
    # WBDDC settings
    numWbddc = 8
    ## \brief WBDDC index base (what number indices start at) 
    wbddcIndexBase = 1
    ## \brief WBDDC component type 
    wbddcType = ndr328_wbddc
    # NBDDC settings
    ## \brief Number of NBDDCs
    numNbddc = 64
    ## \brief NBDDC index base (what number indices start at) 
    nbddcIndexBase = 1
    ## \brief NBDDC component type 
    nbddcType = ndr328_nbddc
    # WBDDC Group settings
    ## \brief Number of WBDDC groups available
    numWbddcGroups = 0
    ## \brief WBDDC group index base (what number indices start at) 
    wbddcGroupIndexBase = 1
    ## \brief WBDDC Group component type 
    wbddcGroupType = None
    # NBDDC Group settings
    ## \brief Number of NBDDC groups available
    numNbddcGroups = 0
    ## \brief NBDDC group index base (what number indices start at) 
    nbddcGroupIndexBase = 1
    ## \brief NBDDC Group component type 
    nbddcGroupType = None
    numGigE = 2
    numGigEDipEntries = 128


if __name__ == '__main__':
    pass
