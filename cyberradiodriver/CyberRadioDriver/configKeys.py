#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.configKeys
# 
# \brief Provides classes and constants that define basic 
#     support for configurable objects.  
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.  
#     All rights reserved.
#
###############################################################

# Imports from other modules in this package
# Imports from external modules
# Python standard library imports
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
## FFT Stream DDC configuration sub-dictionary.
CONFIG_FFT = "fftStream"
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
## Combined wideband/narrowband DDC group configuration sub-dictionary.
CONFIG_COMBINED_DDC_GROUP = "combined"
## DUC group configuration sub-dictionary.
CONFIG_DUC_GROUP = "ducGroupConfiguration"
## Wideband DUC group configuration sub-dictionary.
CONFIG_WBDUC_GROUP = "wideband"
## Tuner group configuration sub-dictionary.
CONFIG_TUNER_GROUP = "tunerGroupConfiguration"
## ADC sample rate mode.
ADC_RATE_MODE = "adcRateMode"

#------ Tuner Configuration Keys ----------------------------------------#
## Tuner index number.
TUNER_INDEX = "tunerIndex"
## Tuner frequency.
TUNER_FREQUENCY = "frequency"
## Tuner attenuation.
TUNER_ATTENUATION = "attenuation"
## Tuner agp.
TUNER_AGP = "agp"
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
TUNER_AGC_DECAY_TIME = "adt"
## Tuner AGC attack step setting.
TUNER_AGC_ATTACK_STEP = "aas"
## Tuner AGC delay step setting.
TUNER_AGC_DECAY_STEP = "ads"
## Tuner AGC attack limit range setting.
TUNER_AGC_ATTACK_LIMIT = "aal"
## Tuner AGC delay limit range setting.
TUNER_AGC_DECAY_LIMIT = "adl"
## Tuner filter setting.
TUNER_FILTER = "filter"
## Timing adjustment, in clocks.
TUNER_TIMING_ADJ = "timingAdjustment"
## Tuner Coherent Group
TUNER_COHERENT_GROUP = "cohGroup"
## RF input power
TUNER_RF_INPUT_POWER = "rfInputPower"
## ADC Overload
TUNER_ADC_OVERLOAD = "adcOverload"
## Preselector bypass
TUNER_PRESELECT_BYPASS = "preselectorBypass"
## IF
TUNER_IF = "if"
## LO sync indicator
TUNER_LO_SYNC = "loSync"

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
## DDC audio decimation factor.
DDC_AUDIO_DECIMATION = "audioDecimation"
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
## DDC demodulation gain.
DDC_DEMOD_GAIN = "demodGain"
## DDC demod Audio DC block.
DDC_DEMOD_DC_BLOCK = "dcBlock"
## DDC demod Audio Level Control type.
DDC_DEMOD_ALC_TYPE = "alcType"
## DDC demod Audio Level Control setpoint.
DDC_DEMOD_ALC_LEVEL = "alcLevel"
## DDC demod Squelch Level.
DDC_DEMOD_SQUELCH_LEVEL = "squelchLevel"
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
## DDC Output Format (complex I&Q, demod output, etc.)
DDC_OUTPUT_FORMAT = "streamFormat"
DDC_SPECTRAL_AVERAGE_ALPHA = "avgAlpha"
DDC_SPECTRAL_FRAME_RATE = "frameRate"
## DDC class ID
DDC_CLASS_ID = "classId"
## DDC phase offset
DDC_PHASE_OFFSET = "phase"
## DDC group enable
DDC_GROUP_ENABLE = "groupEnable"
## DDC mode
DDC_MODE = "mode"
## DDC samples
DDC_SAMPLES = "samples"
## DDC start block.
DDC_START_BLOCK = "startBlock"
## DDC type
DDC_TYPE = "type"
## DDC total repeat packets
DDC_TOTAL_REPEAT_PACKETS = "totalRepeatPackets"
## DDC active repeat packets
DDC_ACTIVE_REPEAT_PACKETS = "activeRepeatPackets"

#------ FFT Stream Configuration Keys ---------------------------------#
## FFT Stream index
FFT_INDEX = "fftIndex"
## FFT Rate (number of FFTs per second)
FFT_RATE = "rate"
## FFT window type
FFT_WINDOW = "window"
## FFT size
FFT_SIZE = "size"
## FFT source DDC
FFT_SOURCE = "source"

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
## DUC data port (that is, 10GigE interface number).
DUC_DATA_PORT = "dataPort"
## DUC frequency offset.
DUC_FREQUENCY = "frequency"
## DUC attenuation.
DUC_ATTENUATION = "attenuation"
## DUC mode.
DUC_MODE = "mode"
## DUC Single playback mode
DUC_SINGLE_PLAYBACK = "singlePlayback"

#------ NBDDC Configuration Keys ----------------------------------------# 
## NBDDC RF index.
NBDDC_RF_INDEX = "rfIndex"

#------ DDC Group Configuration Keys ----------------------------------------#
DDC_GROUP_MEMBER = "member"
DDC_GROUP_MEMBERS = "members"
WBDDC_GROUP_MEMBERS = "wbddcMembers"
NBDDC_GROUP_MEMBERS = "nbddcMembers"

#------ DUC Group Configuration Keys ----------------------------------------#
DUC_GROUP_MEMBER = "member"
DUC_GROUP_MEMBERS = "members"

#------ Tuner Group Configuration Keys ----------------------------------------#
TUNER_GROUP_MEMBER = "member"
TUNER_GROUP_MEMBERS = "members"

#------ Time Configuration Keys ----------------------------------------#
## UTC time, in seconds past the Epoch.
TIME_UTC = "utcTime"
## Timing adjustment, in clocks.
TIMING_ADJ = "clocks"

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
## Gigabit Ethernet flow control enabled.
GIGE_FLOW_CONTROL = "flowControl"
## Gigabit Ethernet netmask.
GIGE_NETMASK = "netmask"

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
STATUS_AUX_MAC = "auxMacAddr"
## MAC address of primary 1GigE port.
STATUS_PRI_MAC = "primaryMacAddr"
## MAC address of fast-scan 1GigE port.
STATUS_FASTSCAN_MAC = "fastScanMacAddr"
## Control port MAC address.
STATUS_CTL_MAC = "controlMacAddr"
## Data port 0 MAC address.
STATUS_DATA0_MAC = "data0MacAddr"
## Data port 1 MAC address.
STATUS_DATA1_MAC = "data1MacAddr"
## 10MHz reference source.
STATUS_10MHZ_REF = "10MHzRef"
## Error state.
STATUS_ERROR = "errorState"
## 10GigE Link 0 state.
STATUS_LINK0 = "link0State"
## 10GigE Link 1 state.
STATUS_LINK1 = "link1State"
## 10GigE Link 2 state.
STATUS_LINK2 = "link2State"
## 10GigE Link 3 state.
STATUS_LINK3 = "link3State"
## Available memory space for user-defined filters.
STATUS_MEM = "memory"
## Accumulated powered-on time.
STATUS_ONTIME = "ontime"
## 10MHz reference status.
STATUS_10MHZ_REF_STATUS = "10MHzRefStatus"
## Pulse-per-second (PPS) status.
STATUS_PPS = "ppsStatus"
## Unit internal temperature (degrees Celsius).
STATUS_TEMP = "temp"
## Radio hostname.
STATUS_HOSTNAME = "hostname"
## Digital board serial number.
STATUS_DIGBRD_SN = "digitalBoardSN"
## Tuner board 1 serial number.
STATUS_TUNERBRD1_SN = "tunerBoard1SN"
## Tuner board 2 serial number.
STATUS_TUNERBRD2_SN = "tunerBoard2SN"
## Number of tuners available.
STATUS_TUNERS = "tuners"
## Number of WBDDCs available
STATUS_WBDDCS = "wbddcs"
## Number of NBDDCs available
STATUS_NBDDCS = "nbddcs"
## Number of demods available
STATUS_DEMODS = "demods"
## Voltages and currents
STATUS_VOLTS = "volts"
## Lock information
STATUS_LOCKS = "locks"
## Temperature information
STATUS_TEMPS = "temps"
## PPS reference source
STATUS_PPS_SOURCE = "ppsSource"
## NTP status
STATUS_NTP = "ntpStatus"
## Clock time of RTC
STATUS_CLOCK_TIME = "clockTime"
## Fan status
STATUS_FAN = "fanStatus"
## Average power level (watts)
STATUS_AVG_POWER = "avgPower"
## Battery level
STATUS_BATTERY_LEVEL = "batteryLevel"
## ADC clock 1
STATUS_ADC_CLOCK1 = "adcClock1"
## ADC clock 1
STATUS_ADC_CLOCK2 = "adcClock2"
## Digital board temperature
STATUS_DIGBRD_TEMP = "digitalBoardTemp"
## FPGA temperature
STATUS_FPGA_TEMP = "fpgaTemp"
## LO 11
STATUS_LO11 = "lo11"
## LO 12
STATUS_LO12 = "lo12"
## LO 13
STATUS_LO13 = "lo13"
## LO 14
STATUS_LO12 = "lo14"
## LO 21
STATUS_LO21 = "lo21"
## LO 22
STATUS_LO22 = "lo22"
## LO 23
STATUS_LO23 = "lo23"
## LO 24
STATUS_LO22 = "lo24"
## Tuner 0 LO 1
STATUS_TUNER0_LO1 = "tuner0lo1"
## Tuner 0 LO 2
STATUS_TUNER0_LO2 = "tuner0lo2"
## Tuner 1 LO 1
STATUS_TUNER1_LO1 = "tuner1lo1"
## Tuner 1 LO 2
STATUS_TUNER1_LO2 = "tuner1lo2"
## Tuner 2 LO 1
STATUS_TUNER2_LO1 = "tuner2lo1"
## Tuner 2 LO 2
STATUS_TUNER2_LO2 = "tuner2lo2"
## Tuner 3 LO 1
STATUS_TUNER3_LO1 = "tuner3lo1"
## Tuner 3 LO 2
STATUS_TUNER3_LO2 = "tuner3lo2"
## Tuner 4 LO 1
STATUS_TUNER4_LO1 = "tuner4lo1"
## Tuner 4 LO 2
STATUS_TUNER4_LO2 = "tuner4lo2"
## Tuner 5 LO 1
STATUS_TUNER5_LO1 = "tuner5lo1"
## Tuner 5 LO 2
STATUS_TUNER5_LO2 = "tuner5lo2"
## Tuner 6 LO 1
STATUS_TUNER6_LO1 = "tuner63lo1"
## Tuner 6 LO 2
STATUS_TUNER6_LO2 = "tuner6lo2"
## Tuner 7 LO 1
STATUS_TUNER7_LO1 = "tuner7lo1"
## Tuner 7 LO 2
STATUS_TUNER7_LO2 = "tuner7lo2"
## Tuner board 0 ADC clock
STATUS_TUNERBRD0_ADC_CLOCK = "tunerBoard0AdcClk"
## Tuner board 1 ADC clock
STATUS_TUNERBRD1_ADC_CLOCK = "tunerBoard1AdcClk"
## Mode
STATUS_MODE = "mode"
## Tuner board 1 JESD
STATUS_TUNERBRD1_JESD = "tunerBoard1JESD"
## Tuner board 2 JESD
STATUS_TUNERBRD2_JESD = "tunerBoard2JESD"
## Tuner board 1 temperature
STATUS_TUNERBRD1_TEMP = "tunerBoard1Temp"
## Tuner board 2 temperature
STATUS_TUNERBRD2_TEMP = "tunerBoard2Temp"
## Tuner power
STATUS_TUNER_POWER = "tunerPower"
## Volts 1
STATUS_VOLTS1 = "volts1"
## Volts 2
STATUS_VOLTS2 = "volts2"
## Volts 3
STATUS_VOLTS3 = "volts3"
## Volts 4
STATUS_VOLTS4 = "volts4"
## Volts 5
STATUS_VOLTS5 = "volts5"
## Number of FSCI packets
STATUS_FSCI_PACKETS = "fsciPackets"
## Number of tunes in Fast Scan mode
STATUS_FASTSCAN_TUNES = "fastScanTunes"
## Link status in Fast Scan mode
STATUS_FASTSCAN_LINK = "fastScanLink"
## Number of seconds last Fast Scan needed to complete
STATUS_FASTSCAN_SEC = "fastScanSec"
## Number of samples last Fast Scan needed to complete
STATUS_FASTSCAN_SAMP = "fastScanSamples"

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
    # The base-class implementation of this method puts None into the 
    # configuration dictionary for each element in the valid configuration 
    # keyword list. Extend this behavior in derived classes to set elements 
    # in the configuration dictionary as appropriate for the object.
    def _queryConfiguration(self):
        for kw in self.validConfigurationKeywords:
            self.configuration[kw] = None
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
    

