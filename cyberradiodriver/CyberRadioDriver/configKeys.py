#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.configKeys
# 
# Provides classes and constants that define basic support for
# configurable objects.  
#
# \author NH
# \author DA
# \copyright Copyright (c) 2014 CyberRadio Solutions, Inc.  All rights 
# reserved.
#
###############################################################

import copy

#------ Configuration Key Constants ----------------------------------------#

#------ General-use configuration keys ----------------------------------------#
## Enable a component.
ENABLE = "enable"
## Component index number.
INDEX = "index"
## Denotes all available components or entries at a given level.
ALL = "all"

#------ Version information configuration keys --------------------------#
## Radio model.
VERINFO_MODEL = "model"
## Radio serial number.
VERINFO_SN = "serialNumber"
## Radio unit revision number
VERINFO_UNITREV = "unitRevision"
## Application version number.
VERINFO_SW = "softwareVersion"
## FPGA software version number.
VERINFO_FW = "firmwareVersion"
## Reference/timing version number.
VERINFO_REF = "referenceVersion"
## Hardware version information.
VERINFO_HW = "hardwareVersion"

#------ Radio configuration keys ----------------------------------------#
## Configuration mode.
CONFIG_MODE = "configMode"
## Reference mode.
REFERENCE_MODE = "referenceMode"
## Reference bypass mode.
BYPASS_MODE = "bypassMode"
## Frequency normalization mode.
FNR_MODE = "freqNormalization"
## GPS receiver enable/disable.
GPS_ENABLE = "gpsEnable"
## 10MHz reference tuning voltage.
REF_TUNING_VOLT = "referenceTuningVoltage"
## Tuner configuration sub-dictionary.
CONFIG_TUNER = "tunerConfiguration"
## Transmitter configuration sub-dictionary.
CONFIG_TX = "txConfiguration"
## CW Tone generator configuration sub-dictionary.
CONFIG_CW = "cwConfiguration"
## DDC configuration sub-dictionary.
CONFIG_DDC = "ddcConfiguration"
## IP configuration sub-dictionary.
CONFIG_IP = "ipConfiguration"
## Wideband DDC configuration sub-dictionary.
CONFIG_WBDDC = "wideband"
## Narrowband DDC configuration sub-dictionary.
CONFIG_NBDDC = "narrowband"
## DUC configuration sub-dictionary.
CONFIG_DUC = "ducConfiguration"
## Wideband DUC configuration sub-dictionary.
CONFIG_WBDUC = "wideband"
## Narrowband DUC configuration sub-dictionary.
CONFIG_NBDUC = "narrowband"
## DDC group configuration sub-dictionary.
CONFIG_DDC_GROUP = "ddcGroupConfiguration"
## Wideband DDC group configuration sub-dictionary.
CONFIG_WBDDC_GROUP = "wideband"
## Narrowband DDC group configuration sub-dictionary.
CONFIG_NBDDC_GROUP = "narrowband"

#------ Tuner Configuration Keys ----------------------------------------#
## Tuner index number.
TUNER_INDEX = "tunerIndex"
## Tuner frequency.
TUNER_FREQUENCY = "frequency"
## Tuner attenuation.
TUNER_ATTENUATION = "attenuation"
## Tuner RF attentuation.
TUNER_RF_ATTENUATION = "rfAttenuation"
## Tuner IF attentuation.
TUNER_IF_ATTENUATION = "ifAttenuation"
## Tuner IF filter setting.
TUNER_IF_FILTER = "ifFilter"
## Tuner FNR setting.
TUNER_FNR = "fnr"
## Tuner gain mode setting.
TUNER_GAIN_MODE = "gainMode"
## Tuner delay setting.
TUNER_DELAY = "delay"
## Tuner AGC set point setting.
TUNER_AGC_SET_POINT = "asp"
## Tuner AGC upper limit range setting.
TUNER_AGC_UPPER_LIMIT = "aul"
## Tuner AGC lower limit range setting.
TUNER_AGC_LOWER_LIMIT = "all"
## Tuner AGC attack time setting.
TUNER_AGC_ATTACK_TIME = "aat"
## Tuner AGC delay time setting.
TUNER_AGC_DELAY_TIME = "adt"
## Tuner AGC attack step setting.
TUNER_AGC_ATTACK_STEP = "aas"
## Tuner AGC delay step setting.
TUNER_AGC_DELAY_STEP = "ads"
## Tuner AGC attack limit range setting.
TUNER_AGC_ATTACK_LIMIT = "aal"
## Tuner AGC delay limit range setting.
TUNER_AGC_DELAY_LIMIT = "adl"
## Tuner filter setting.
TUNER_FILTER = "filter"
## Timing adjustment, in clocks.
TUNER_TIMING_ADJ = "timingAdjustment"

#------ Transmitter Configuration Keys --------------------------------#
TX_INDEX = "txIndex"
TX_FREQUENCY = "frequency"
TX_ATTENUATION = "attenuation"

#------ CW Tone Generator Configuration Keys --------------------------#
CW_INDEX = "cwIndex"
CW_FREQUENCY = "cwFrequency"
CW_AMPLITUDE = "cwAmplitude"
CW_PHASE = "cwPhase"
CW_SWEEP_START = "cwSweepStart"
CW_SWEEP_STOP = "cwSweepStop"
CW_SWEEP_STEP = "cwSweepStep"
CW_SWEEP_DWELL = "cwSweepDwell"

#------ DDC Configuration Keys ----------------------------------------#
## DDC index.
DDC_INDEX = "ddcIndex"
## Whether the DDC is a wideband DDC.
DDC_WIDEBAND = "wideband"
## DDC rate index (that is, index into the allowed rates table).
DDC_RATE_INDEX = "rateIndex"
## DDC frequency offset.
DDC_FREQUENCY_OFFSET = "frequency"
## DDC UDP destination.
DDC_UDP_DESTINATION = "udpDest"
## DDC VITA 49 enabling option.
DDC_VITA_ENABLE = "vitaEnable" 
## DDC VITA 49 stream ID.
DDC_STREAM_ID = "streamId"
## DDC RF index.
DDC_RF_INDEX = "rfIndex"
## DDC output type.
DDC_OUTPUT_TYPE = "outputType"
## DDC decimation factor.
DDC_DECIMATION = "decimation"
## DDC filter index.
DDC_FILTER_INDEX = "filterIndex"
## DDC oversampling parameter.
DDC_OVERSAMPLING = "oversampling"
## DDC start time.
DDC_START_TIME = "startTime"
## DDC number of samples.
DDC_SAMPLES = "samples"
## DDC link (10GigE interface) number.
DDC_LINK = "link"
## DDC gain.
DDC_GAIN = "gain"
## DDC CIC0 value.
DDC_CIC0 = "cic0"
## DDC CIC1 value.
DDC_CIC1 = "cic1"
## DDC demodulation type.
DDC_DEMOD_TYPE = "demod"
## DDC Beat Frequency Oscillator (BFO) value.
DDC_BEAT_FREQ_OSC = "bfo"
## DDC Digital Gain Control (DGC) gain mode.
DDC_DGC_MODE = "gainMode"
## DDC Digital Gain Control (DGC) manual gain.
DDC_DGC_GAIN = "dgv"
## DDC Digital Gain Control (DGC) upper limit range.
DDC_DGC_UPPER_LIMIT = "dul"
## DDC Digital Gain Control (DGC) lower limit range.
DDC_DGC_LOWER_LIMIT = "dll"
## DDC Digital Gain Control (DGC) target level range.
DDC_DGC_TARGET_RANGE = "dtl"
## DDC Digital Gain Control (DGC) attack limit range.
DDC_DGC_ATTACK_LIMIT = "dal"
## DDC Digital Gain Control (DGC) decay limit range.
DDC_DGC_DECAY_LIMIT = "ddl"
## DDC Digital Gain Control (DGC) attack offset range.
DDC_DGC_ATTACK_OFFSET = "dao"
## DDC Digital Gain Control (DGC) decay offset range.
DDC_DGC_DECAY_OFFSET = "ddo"
## DDC Digital Gain Control (DGC) attack time constant range.
DDC_DGC_ATTACK_TIME = "datc"
## DDC Digital Gain Control (DGC) decay time constant range.
DDC_DGC_DECAY_TIME = "ddtc"
## DDC Digital Gain Control (DGC) attack trigger range.
DDC_DGC_ATTACK_TRIGGER = "dat"
## DDC Digital Gain Control (DGC) decay trigger range.
DDC_DGC_DECAY_TRIGGER = "ddt"
## DDC data port (that is, 10GigE interface number).
DDC_DATA_PORT = "dataPort"

#------ DUC Configuration Keys ----------------------------------------#
## DUC index.
DUC_INDEX = "ducIndex"
## Whether the DUC is a wideband DUC.
DUC_WIDEBAND = "wideband"
## DUC rate index (that is, index into the allowed rates table).
DUC_RATE_INDEX = "rateIndex"
## DUC TX channels (bitmap).
DUC_TX_CHANNELS = "txChannels"
## DUC VITA 49 stream ID.
DUC_STREAM_ID = "streamId"
## DUC snapshot filename.
DUC_FILENAME = "filename"
## DUC snapshot start sample number.
DUC_START_SAMPLE = "startSample"
## DUC snapshot number of samples.
DUC_SAMPLES = "samples"
## DUC snapshot start block.
DUC_START_BLOCK = "startBlock"
## DUC snapshot end block.
DUC_END_BLOCK = "endBlock"

#------ NBDDC Configuration Keys ----------------------------------------# 
## NBDDC RF index.
NBDDC_RF_INDEX = "rfIndex"

#------ DDC Group Configuration Keys ----------------------------------------#
DDC_GROUP_MEMBER = "member"
DDC_GROUP_MEMBERS = "members"

#------ Time Configuration Keys ----------------------------------------#
## UTC time, in seconds past the Epoch.
TIME_UTC = "utcTime"

#------ IP Configuration Keys ------------------------------------------#
## Source IP address.
IP_SOURCE = "sourceIP"
## Destination IP address (if radio has no Gigabit Ethernet ports) or 
# destination IP address table (if radio does have them).
IP_DEST = "destIP"
## Source MAC address.
MAC_SOURCE = "sourceMAC"
## Destination MAC address.
MAC_DEST = "destMAC"
# For radios with Gigabit Ethernet ports
## Gigabit Ethernet port index number.
GIGE_PORT_INDEX = "gigEIndex"
## Gigabit Ethernet destination IP table index number.
GIGE_DIP_INDEX = "gigEDipIndex"
## Gigabit Ethernet destination IP address.
GIGE_IP_ADDR = "ipAddr"
## Gigabit Ethernet destination MAC address.
GIGE_MAC_ADDR = "macAddr"
## Gigabit Ethernet source port.
GIGE_SOURCE_PORT = "sourcePort"
## Gigabit Ethernet destination port.
GIGE_DEST_PORT = "destPort"
## Gigabit Ethernet Address Resolution Protocol (ARP) enabled.
GIGE_ARP = "arp"

#--  Calibration Frequency Keys  ---------------------------------------#
## Calibration frequency.
CALIB_FREQUENCY = "calibFrequency"

#--  GPS Keys  ---------------------------------------#
## GPS latitude.
GPS_LATITUDE = "latitude"
## GPS longitude.
GPS_LONGITUDE = "longitude"

#--  Temperature Keys  ---------------------------------------#
## Temperature.
TEMPERATURE = "temperature"

#--  GPIO Keys  ---------------------------------------#
## GPIO output pin value (bitmap).
GPIO_VALUE = "value"
## Duration.
GPIO_DURATION = "duration"
## Loop indicator.
GPIO_LOOP = "loop"
## Go indicator.
GPIO_GO = "go"

#--  Status Keys  ------------------------------------------------------#
## MAC address of auxiliary 1GigE port.
STATUS_AMAC = "amac"
## 10MHz reference source.
STATUS_CFG10M = "cfg10m"
## Error state.
STATUS_ERROR = "error"
## 10GigE Link 0 state.
STATUS_LINK0 = "link0up"
## 10GigE Link 1 state.
STATUS_LINK1 = "link1up"
## 10GigE Link 2 state.
STATUS_LINK2 = "link2up"
## 10GigE Link 3 state.
STATUS_LINK3 = "link3up"
## Available memory space for user-defined filters.
STATUS_MEM = "mem"
## Accumulated powered-on time.
STATUS_ONTIME = "ontime"
## MAC address of primary 1GigE port.
STATUS_PMAC = "pmac"
## 10MHz reference status.
STATUS_10M = "status10m"
## Pulse-per-second (PPS) status.
STATUS_PPS = "statuspps"
## Unit internal temperature (degrees Celsius).
STATUS_TEMP = "temp"

#--  Reset Type Keys  --------------------------------------------------#
## Reset type.
RESET_TYPE = "resetType"


#------ Configurable Object --------------------------------------------#

##
# Defines basic functionality for an object that can be configured.
#
class Configurable(object):

    ##
    # The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = []

    ##
    # Constructs a Configurable object.
    def __init__(self):
        self.configuration = {}
        # Command error information
        self.cmdErrorInfo = []

    ##
    # Queries hardware to get the object's current configuration.
    #
    # \note Derived classes must override helper method _queryConfiguration(),
    # which performs the actual queries to the hardware managed by the
    # object.
    #
    # \return The object's configuration, as a dictionary.
    def queryConfiguration(self):
        self.cmdErrorInfo = []
        self._queryConfiguration()
        return self.configuration
    
    ##
    # Gets the object's current configuration.  
    #
    # This method retrieves the current configuration from a cache 
    # instead of performing hardware queries.
    #
    # \return The object's configuration, as a dictionary.
    def getConfiguration(self):
        if len(self.configuration.keys()) == 0:
            self._queryConfiguration()
        return self.configuration
    
    ##
    # Sets the object's current configuration.  
    #
    # This method uses keyword arguments to set configuration
    # parameters.  Member validConfigurationKeywords defines
    # which configuration keywords are supported; this set will
    # vary depending on the hardware being managed by this object.
    #
    # \note Derived classes must override helper method 
    # _setConfiguration(), which issues the actual configuration
    # commands to the hardware managed by the object.
    #
    # \param args Variable-length list of positional arguments.  Positional
    #     arguments are ignored.
    # \param kwargs Dictionary of keyword arguments.  Keyword arguments that 
    #     are not supported by this object will be ignored.
    # \return True if successful, False otherwise.
    def setConfiguration(self, *args, **kwargs):
        self.cmdErrorInfo = []
        confDict = {}
        confKeys = [q for q in kwargs.keys() if q in self.validConfigurationKeywords]
        for key in confKeys:
            confDict[key] = kwargs[key]
        return self._setConfiguration(confDict)

    ##
    # Gets the last set of error information returned by commands 
    # issued to the radio.
    #
    # The error information set is reset on each call to getConfiguration()
    # or setConfiguration().
    #
    # \return A list of error information strings.  This list will 
    # be empty if all commands completed successfully.
    def getLastCommandErrorInfo(self):
        return self.cmdErrorInfo
    
    ##
    # \protected
    # Queries hardware to determine the object's current configuration.  
    #
    # The base-class implementation of this method does nothing.  Override
    # this method in derived classes to set elements in the configuration
    # dictionary as appropriate for the object.
    def _queryConfiguration(self):
        pass

    ##
    # \protected
    # Issues hardware commands to set the object's current configuration.  
    #
    # The base-class implementation of this method does nothing and returns
    # True.  Override this method in derived classes to set elements in the 
    # configuration dictionary as appropriate for the object.
    def _setConfiguration(self, confDict):
        ret = True
        return ret
    
    ##
    # \internal
    # Helper method that selectively updates one dictionary with values
    # from other dictionaries.
    #
    # \param dicty The dictionary being updated.
    # \param srcDict The source dictionary supplying new values.
    # \param defDict The default dictionary to pull values from if the values 
    #    cannot be found in the source dictionary.
    # \param keys A list of keys to update.
    def _dictUpdate(self, dicty, srcDict, defDict, keys):
        for key in keys:
            if key in srcDict:
                dicty[key] = copy.deepcopy(srcDict[key])
            elif key in defDict:
                dicty[key] = copy.deepcopy(defDict[key])
        pass

    ##
    # \internal
    # Adds info to the last set of error information.
    #
    def _addLastCommandErrorInfo(self, cmd):
        self.cmdErrorInfo.extend(cmd.errorInfo if cmd.errorInfo is not None else [])
    

