#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.radio
# 
# \brief Defines basic functionality for radio handler objects.
#
# \note This module defines basic behavior only.  To customize
#     a radio handler class for a particular radio, derive a new
#     class from the appropriate base class.  It is recommended
#     that behavior specific to a given radio be placed in the
#     module that supports that radio.
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.  
#    All rights reserved.
#
###############################################################

# Imports from other modules in this package
from . import command
from . import components
from . import configKeys
from . import log
from . import transport
# Imports from external modules
# Python standard library imports
import ast
import copy
import datetime
import json
import math
import sys
import time
import traceback
import threading

##
# \internal
# \brief Returns the MAC address and IP address for a given Ethernet interface.
#
# \param ifname The name of t# \author DA
# \param ifname The Ethernet system interface ("eth0", for example).
# \returns A 2-tuple: (MAC Address, IP Address).
def getInterfaceAddresses(ifname):
    import socket,fcntl,struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    mac = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
    ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])
    return mac,ip


##
# \internal
# \brief VITA 49 interface specification class.
#
# The _ifSpec class describes how the VITA 49 interface is set up for 
# a particular radio.  Each radio should have its own interface 
# specification, implemented as a subclass of _ifSpec.
#
# Radio handler classes need to set static member "ifSpec" to the interface 
# specification class that the radio uses.
class _ifSpec():
    ## Whether Vita 49.1 is used
    vita49_1 = True
    ## Whether Vita 49.0 is used
    vita49_0 = True
    ## Size of the VITA 49 header, in 32-byte words
    headerSizeWords = 0
    ## Size of the payload, in 32-byte words
    payloadSizeWords = 0
    ## Size of the VITA 49 "tail", in 32-byte words
    tailSizeWords = 0
    ## Byte order used by the radio.
    byteOrder = "little"
    ## Whether the I/Q data in the payload are swapped
    iqSwapped = False
    
    @classmethod
    def getFrameInfoDict(cls, self):
        return {
                "headerWords": cls.headerSizeWords, 
                "payloadWords": cls.payloadSizeWords, 
                "tailWords": cls.tailSizeWords, 
                "frameSize": (cls.headerSizeWords+cls.payloadSizeWords+cls.tailSizeWords)*4, 
                "v49.1": cls.vita49_1, 
                "v49.0": cls.vita49_0, 
                "byteSwap": cls.byteOrder!=sys.byteorder, 
                "iqSwap": cls.iqSwapped, 
                 }

#-- Radio Handler Objects ---------------------------------------------#

##
# \brief Base radio handler class.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# To add a supported radio to this driver, derive a class from 
# _radio and change the static members of the new class to describe the
# capabilities of that particular radio.  Each supported radio should
# have its own module under the CyberRadioDriver.radios package tree.
#
# A radio handler object maintains a series of component objects, one
# per component of each type (tuner, WBDDC, NBDDC, etc.).  Each component 
# object is responsible for managing the hardware object that it represents.
# Each component object is also responsible for querying the component's 
# current configuration and for maintaining the object's configuration
# as it changes during radio operation.
#
# A radio handler object also maintains its own configuration, for settings
# that occur at the radio level and are not managed by a component object.
#
# \note Several static members of this class have no function within the 
# code, but instead help CyberRadioDriver.getRadioObjectDocstring() generate 
# appropriate documentation for derived radio handler classes.
#
# \implements CyberRadioDriver::IRadio
class _radio(log._logger, configKeys.Configurable):
    _name = "NDRgeneric"
    ## \brief Radio uses JSON command/response interface?
    json = False
    ## \brief VITA 49 interface specification class name (see _ifSpec class).
    ifSpec = _ifSpec
    ## \brief Dictionary of VITA 49 interface specification classes, keyed by 
    #     payload type strings, for those radios that support more than one VITA 
    #     packet format.
    ifSpecMap = {}
    ## \brief Analog-to-digital Converter clock rate
    adcRate = 1.0
    # Tuner settings
    ## \brief Number of tuners
    numTuner = 0
    ## \brief Number of tuner boards
    numTunerBoards = 1
    ## \brief Tuner index base (what number indices start at) 
    tunerIndexBase = 0
    ## \brief Tuner component type 
    tunerType = components._tuner
    ## \brief Tuner index overrides.  Used for radios with 
    # WBDDC settings
    ## \brief Number of WBDDCs available
    numWbddc = numTuner
    ## \brief WBDDC index base (what number indices start at) 
    wbddcIndexBase = 1
    ## \brief WBDDC component type 
    wbddcType = components._wbddc
    # NBDDC settings
    ## \brief Number of NBDDCs
    numNbddc = 0
    ## \brief NBDDC index base (what number indices start at) 
    nbddcIndexBase = 1
    ## \brief NBDDC component type 
    nbddcType = components._nbddc
    ## \brief NBDDC index list override.  This is a list of discrete indices 
    #     for radios where the indices are a subset of the full index list.  
    #     This should be set to None otherwise.
    nbddcIndexOverride = None
    # FFT Processor Settings
    ## \brief Number of FFT Channels
    numFftStream = 0
    ## \brief FFT stream index base (what number indices start at) 
    fftStreamIndexBase = 0
    ## \brief FFT stream component type 
    fftStreamType = None
    # Transmitter settings
    ## \brief Number of transmitters
    numTxs = 0
    ## \brief Transmitter index base (what number indices start at) 
    txIndexBase = 1
    ## \brief Transmitter component type 
    txType = None
    # WBDUC Settings
    ## \brief Number of WBDUC
    numWbduc = 0
    ## \brief WBDUC index base (what number indices start at)
    wbducIndexBase = 1
    ## \brief WBDUC component type
    wbducType = None
    # NBDUC Settings
    ## \brief Number of NBDUC
    numNbduc = 0
    ## \brief NBDUC index base (what number indices start at)
    nbducIndexBase = 1
    ## \brief NBDUC component type
    nbducType = None
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
    # Combined DDC Group settings
    ## \brief Number of combined DDC groups available
    numCddcGroups = 0
    ## \brief Combined DDC group index base (what number indices start at) 
    cddcGroupIndexBase = 1
    ## \brief Combined DDC Group component type 
    cddcGroupType = None
    # WBDUC Group settings
    ## \brief Number of WBDUC groups available
    numWbducGroups = 0
    ## \brief WBDUC group index base (what number indices start at) 
    wbducGroupIndexBase = 1
    ## \brief WBDUC Group component type 
    wbducGroupType = None
    # Tuner Group settings
    ## \brief Number of tuner groups available
    numTunerGroups = 0
    ## \brief Tuner group index base (what number indices start at) 
    tunerGroupIndexBase = 1
    ## \brief Tuner Group component type 
    tunerGroupType = None
    # UDP destination information
    ## \brief What the UDP destination setting represents for this radio
    udpDestInfo = ""
    ## \brief Number of Gigabit Ethernet ports
    numGigE = 0
    ## \brief Gigabit Ethernet port index base (what number indices start at) 
    gigEIndexBase = 1
    ## \brief Number of destination IP table entries for each Gigabit Ethernet port
    numGigEDipEntries = 0
    ## \brief Gigabit Ethernet destination IP table index base (what number indices start at) 
    gigEDipEntryIndexBase = 0
    # Supported command set.  Each member listed here is either a 
    # command class (one derived from command._commandBase) or None 
    # if the command is not supported for a given radio.
    ## \brief Command: Identity query 
    idnQry = command.idn
    ## \brief Command: Version query 
    verQry = command.ver
    ## Command: Hardware revision query 
    hrevQry = command.hrev
    ## \brief Command: Status query 
    statQry = command.stat
    ## \brief Command: Tuner status query 
    tstatQry = command.tstat
    ## \brief Command: Time adjustment set/query
    tadjCmd = None
    ## \brief Command: Reset 
    resetCmd = command.reset
    ## \brief Command: Configuration mode set/query
    cfgCmd = command.cfg
    ## \brief Command: Pulse-per-second (PPS) set/query
    ppsCmd = None
    ## \brief Command: UTC time set/query 
    utcCmd = None
    ## \brief Command: Reference mode set/query 
    refCmd = command.ref
    ## \brief Command: Reference bypass mode set/query 
    rbypCmd = None
    ## \brief Command: Source IP address set/query
    sipCmd = command.sip
    ## \brief Command: Destination IP address set/query
    dipCmd = command.dip
    ## \brief Command: Source MAC address set/query
    #
    # \note Most radios support \e querying the source MAC address, but few
    # support \e setting it.
    smacCmd = command.smac
    ## \brief Command: Destination MAC address set/query
    dmacCmd = command.dmac
    ## \brief Command: Calibration frequency set/query
    calfCmd = None
    ## \brief Command: Narrowband source selection set/query
    nbssCmd = None
    ## \brief Command: Frequency normalization mode set/query
    fnrCmd = None
    ## \brief Command: GPS receiver enable set/query
    gpsCmd = None
    ## \brief Command: GPS position query
    gposCmd = None
    ## \brief Command: Reference tuning voltage set/query
    rtvCmd = None
    ## \brief Command: Radio temperature query
    tempCmd = None
    ## \brief Command: GPIO output (static) set/query
    gpioStaticCmd = None
    ## \brief Command: GPIO output (sequence) set/query
    gpioSeqCmd = None
    ## \brief Command: Gigabit Ethernet interface flow control set/query
    tgfcCmd = None
    ## \brief Coherent tuning command
    cohTuneCmd = None
    ## \brief FPGA state selection command
    fpgaStateCmd = None
    ## \brief Radio function (mode) selection command
    funCmd = None
    ## \brief Radio Cntrl command
    cntrlCmd = None
    # Mode settings
    ## \brief Supported reference modes 
    refModes = {}
    ## \brief Supported reference bypass modes 
    rbypModes = {}
    ## \brief Supported VITA 49 enabling options 
    vitaEnableOptions = {}
    ## \brief Supported connection modes
    connectionModes = ["tty"]
    ## \brief Default baud rate (has no effect if radio does not use TTY)
    defaultBaudrate = 921600
    ## \brief Default port number (has no effect if radio does not use network connections)
    defaultPort = 8617
    ## \brief Default timeout for communications over the radio transport
    defaultTimeout = transport.radio_transport.defaultTimeout
    ## \brief Does this radio support setting the tuner bandwidth?
    tunerBandwithSettable = False
    ## \brief Tuner bandwidth (Hz) for radios that do not support setting it
    tunerBandwidthConstant = 40e6
    
    ##
    # \brief The list of valid configuration keywords supported by this
    # object.  Override in derived classes as needed.
    validConfigurationKeywords = [configKeys.CONFIG_MODE,
                                  configKeys.REFERENCE_MODE,
                                  configKeys.BYPASS_MODE,
                                  configKeys.CALIB_FREQUENCY,
                                  configKeys.FNR_MODE,
                                  configKeys.GPS_ENABLE,
                                  configKeys.REF_TUNING_VOLT,
                                  configKeys.GIGE_FLOW_CONTROL,
                                 ]
    ## \brief Default "set time" value
    setTimeDefault = False

    ##
    # \brief Constructs a radio handler object.
    #
    # \copydetails CyberRadioDriver::IRadio::\_\_init\_\_()
    def __init__(self, *args, **kwargs):
        self._setConfigLock = threading.RLock()
        # Set up configuration capability
        configKeys.Configurable.__init__(self)
        # Consume keyword arguments "verbose" and "logFile" for logging support
        log._logger.__init__(self, *args, **kwargs)
        # Now consume our own
        self.setTime = kwargs.get("setTime",self.setTimeDefault)
        self.logCtrl = kwargs.get("logCtrl",None)
        self.transportTimeout = kwargs.get("timeout", None)
        self.clientId = kwargs.get("clientId", None)
        if self.transportTimeout is None:
            self.transportTimeout = self.defaultTimeout
        self.name = "%s%s"%(self._name,"-%s"%kwargs.get("name") if "name" in kwargs else "",)
        self.logIfVerbose("Verbose mode!")
        # Communication transport in use 
        self.transport = None
        self.tunerDict = {}
        self.wbddcDict = {}
        self.nbddcDict = {}
        self.fftStreamDict = {}
        self.txDict = {}
        self.wbducDict = {}
        self.nbducDict = {}
        self.wbddcGroupDict = {}
        self.nbddcGroupDict = {}
        self.cddcGroupDict = {}
        self.wbducGroupDict = {}
        self.tunerGroupDict = {}
        self.componentList = []
        # Little hack to ensure numWbddc is always set (we didn't always have this attribute).
        if self.numWbddc is None:
            self.numWbddc = self.numTuner
        # Form the actual index lists for the different components.  Now that certain components
        # have discrete index values rather than a full sequence, we need to store these for
        # later use.
        self.tunerIndexList = list(range(self.tunerIndexBase, self.tunerIndexBase + self.numTuner))
        self.wbddcIndexList = list(range(self.wbddcIndexBase, self.wbddcIndexBase + self.numWbddc))
        self.nbddcIndexList = self.nbddcIndexOverride if self.nbddcIndexOverride is not None else \
                              list(range(self.nbddcIndexBase, self.nbddcIndexBase + self.numNbddc))
        self.fftStreamIndexList = list(range(self.fftStreamIndexBase, self.fftStreamIndexBase + self.numFftStream))
        self.txIndexList = list(range(self.txIndexBase, self.txIndexBase + self.numTxs))
        self.wbducIndexList = list(range(self.wbducIndexBase, self.wbddcIndexBase + self.numWbduc))
        self.nbducIndexList = list(range(self.nbducIndexBase, self.nbddcIndexBase + self.numNbduc))
        self.wbddcGroupIndexList = list(range(self.wbddcGroupIndexBase, self.wbddcGroupIndexBase + self.numWbddcGroups))
        self.nbddcGroupIndexList = list(range(self.nbddcGroupIndexBase, self.nbddcGroupIndexBase + self.numNbddcGroups))
        self.cddcGroupIndexList = list(range(self.cddcGroupIndexBase, self.cddcGroupIndexBase + self.numCddcGroups))
        self.wbducGroupIndexList = list(range(self.wbducGroupIndexBase, self.wbducGroupIndexBase + self.numWbducGroups))
        self.tunerGroupIndexList = list(range(self.tunerGroupIndexBase, self.tunerGroupIndexBase + self.numTunerGroups))
        self.gigEIndexList = list(range(self.gigEIndexBase, self.gigEIndexBase + self.numGigE))
        self.gigEDipEntryIndexList = list(range(self.gigEDipEntryIndexBase, self.gigEDipEntryIndexBase + self.numGigEDipEntries))
        self.txToneGenIndexList = [] if self.numTxs == 0 else \
                                  list(range(self.txType.toneGenIndexBase, self.txType.toneGenIndexBase + self.txType.numToneGen))
        # Make component objects
        for objRange,objType,objDict in ( \
                                        (self.tunerIndexList,self.tunerType,self.tunerDict), \
                                        (self.wbddcIndexList,self.wbddcType,self.wbddcDict), \
                                        (self.nbddcIndexList,self.nbddcType,self.nbddcDict), \
                                        (self.fftStreamIndexList,self.fftStreamType,self.fftStreamDict), \
                                        (self.txIndexList,self.txType,self.txDict), \
                                        (self.wbducIndexList,self.wbducType,self.wbducDict), \
                                        (self.nbducIndexList,self.nbducType,self.nbducDict), \
                                        (self.wbddcGroupIndexList,self.wbddcGroupType,self.wbddcGroupDict), \
                                        (self.nbddcGroupIndexList,self.nbddcGroupType,self.nbddcGroupDict), \
                                        (self.cddcGroupIndexList,self.cddcGroupType,self.cddcGroupDict), \
                                        (self.wbducGroupIndexList,self.wbducGroupType,self.wbducGroupDict), \
                                        (self.tunerGroupIndexList,self.tunerGroupType,self.tunerGroupDict), \
                                         ):
            if objType is not None:
                for objInd in objRange:
                    objDict[objInd] = objType(parent=self, transport=None, 
                                              index=objInd, verbose=self.verbose, 
                                              logFile=self.logFile)
                    self.componentList.append( objDict[objInd] )
        self.sipTable = {}
        self.dipTable = {}
        self.versionInfo = {}
        # State variables
        # -- is the radio connected through crdd?
        self.isCrddConnection = False
        # -- crdd command prefix, which tells crdd that this isn't a pass-through
        #    radio command.  Set this to four vertical bars, because no NDR-class
        #    radio uses them.
        self.crddCommandPrefix = "||||"
        # Set the time on the radio 
        self.setTime = False
        self.connectError = ""
    
    ##
    # \brief Destroys a radio handler object.
    #
    # \copydetails CyberRadioDriver::IRadio::\_\_del\_\_()
    def __del__(self):
        if self.isConnected():
            self.disconnect()

    ##
    # \brief Indicates whether the radio is connected.
    #
    # \copydetails CyberRadioDriver::IRadio::isConnected()
    def isConnected(self,):
        return (self.transport is not None and self.transport.connected)
    
    ##
    # \brief Returns version information for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getVersionInfo()
    def getVersionInfo(self):
        # If this is a crdd connection, try to get the version info from
        # crdd's radio handler rather than through direct radio commands
        if self.isCrddConnection:
            # Get the radio's version information from crdd
            rsp = self._crddSendCommand(cmd="GETVERINFO")
            if rsp is not None:
                # Set the version info by running the first response string (the
                # version info dict) through ast.literal_eval().
                self.versionInfo = ast.literal_eval(rsp[0])
        # Query hardware for details if we don't have them already
        if not all([key in self.versionInfo for key in \
                      [configKeys.VERINFO_MODEL, configKeys.VERINFO_SN]]):
            cmd = self.idnQry(parent=self, 
                              query=True,
                              verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.versionInfo.update(rspInfo)
        if not all([key in self.versionInfo for key in [configKeys.VERINFO_SW, 
                                                              configKeys.VERINFO_FW,
                                                              configKeys.VERINFO_REF]]):
            cmd = self.verQry(parent=self, 
                              query=True,
                              verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self.versionInfo.update(rspInfo)
        if not all([key in self.versionInfo for key in [configKeys.VERINFO_MODEL, 
                                                              configKeys.VERINFO_SN,
                                                              configKeys.VERINFO_UNITREV, 
                                                              configKeys.VERINFO_HW]]):
            cmd = self.hrevQry(parent=self, 
                               query=True,
                               verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                # Don't mask previously determined model and S/N information!
                for key in [configKeys.VERINFO_MODEL, configKeys.VERINFO_SN]:
                    if key in self.versionInfo and key in rspInfo:
                        del rspInfo[key]
                self.versionInfo.update(rspInfo)
        for key in [configKeys.VERINFO_MODEL, configKeys.VERINFO_SN, 
                    configKeys.VERINFO_SW, configKeys.VERINFO_FW, 
                    configKeys.VERINFO_REF, configKeys.VERINFO_UNITREV, 
                    configKeys.VERINFO_HW]:
            if key not in self.versionInfo:
                self.versionInfo[key] = "N/A"
        return self.versionInfo
        
    ##
    # \brief Returns connection information for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getConnectionInfo()
    def getConnectionInfo(self):
        connectionInfo = {}
        # Connection information
        connectionInfo["mode"] = self.mode
        if self.mode in ("tcp","udp","https"):
            connectionInfo["hostname"] = self.host_or_dev
            connectionInfo["port"] = "%d" % self.port_or_baudrate
        elif self.mode == "tty":
            connectionInfo["device"] = self.host_or_dev
            connectionInfo["baudrate"] = "%d" % self.port_or_baudrate
        return connectionInfo
        
    ##
    # \brief Connects to a given radio.
    #
    # \copydetails CyberRadioDriver::IRadio::connect()
    def connect(self,mode,host_or_dev,port_or_baudrate=None,setTime=False,initDdc=False,
                reset=False, fcState=None):
        if mode in self.connectionModes:
            self.mode = mode
            self.host_or_dev = host_or_dev
            self.port_or_baudrate = port_or_baudrate
            if self.port_or_baudrate is None:
                self.port_or_baudrate = self.defaultBaudrate if mode == "tty" else \
                                        self.defaultPort
                self.logIfVerbose("USING PORT %r"%(self.port_or_baudrate))
            if self.transport is not None:
                self.transport.disconnect()
                self.transport = None
            self.transport = transport.radio_transport(parent=self,verbose=self.verbose,
                                                       logFile=self.logFile, 
                                                       logCtrl=self.logCtrl,
                                                       json=self.json,
                                                       timeout=self.transportTimeout)
            if self.transport.connect(mode, self.host_or_dev, self.port_or_baudrate):
                if self.isCrddConnection:
                    self._crddInitialize()
                # Query the configuration if we didn't already have it
                if self.configuration == {}:
                    self._queryConfiguration()
                for obj in self.componentList:
                    obj.addTransport(self.transport, self.sendCommand,
                                     not self.isCrddConnection)
                self.getVersionInfo()
                if reset:
                    self.sendReset()
                if setTime:
                    self.setTimeNextPps()
                if initDdc:
                    self.setDdcConfiguration(wideband=True,)
                    self.setDdcConfiguration(wideband=False,)
                if fcState is not None:
                    try:
                        self.setTenGigFlowControlStatus(fcState)
                    except:
                        pass
                return True
            else:
                self.connectError = self.transport.connectError
                self.disconnect()
                return False
        else:
            self.log("Unsupported connection mode: %s", str(mode))
            return False
            
    ##
    # \brief Disconnects from the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::disconnect()
    def disconnect(self):
        try:
            self.transport.disconnect()
        except:
            self.logIfVerbose(traceback.format_exc())
            #traceback.print_exc()
        for obj in self.componentList:
            obj.delTransport()
        self.configuration = {}
    
    ##
    # \brief Sends a command to the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::sendCommand()
    def sendCommand(self,cmdString,timeout=None):
        # Sanity-check: Don't bother trying if we don't have a 
        # transport object, or if it's disconnected
        if self.transport is None or not self.transport.isConnected():
            return None
        # Check if this is an outgoing crdd command.  These commands don't
        # use JSON framing, so we want to avoid trying to run it through
        # the JSON layer (which won't work).
        isCrddCommand = cmdString.startswith(self.crddCommandPrefix)
        try:
            if not isCrddCommand and self.json:
                if isinstance(cmdString, str):
                    jsonCmd = json.loads(cmdString)
                elif isinstance(cmdString, dict):
                    jsonCmd = cmdString
                jsonCmd["msg"] = command.jsonConfig.newMessageId()
                x = self.transport.sendCommandAndReceive(json.dumps(jsonCmd),timeout)
            else:
                x = self.transport.sendCommandAndReceive(cmdString, timeout, useJson=False)
            if not self.transport.connected:
                self.transport.disconnect()
                return None
            else:
                return x
        except:
            self.logIfVerbose(traceback.format_exc())
            #traceback.print_exc()
            self.transport.disconnect()
            return None
    
    ##
    # \brief Sets the radio configuration.
    #
    # \copydetails CyberRadioDriver::IRadio::setConfiguration()
    def setConfiguration(self, configDict={}):
        if self.isCrddConnection:
            return self._crddSetConfiguration(configDict)
        else:
            with self._setConfigLock:
                self.cmdErrorInfo = []
                # Normalize the incoming configuration dictionary before trying to process it.
                configDict2 = self._normalizeConfigDict(configDict)
                success = configKeys.Configurable.setConfiguration(self, **configDict2)
                # Tuner configuration
                tunerConfDict = configDict2.get(configKeys.CONFIG_TUNER,{})
                for index in self.tunerIndexList:
                    if index in tunerConfDict:
                        confDict = tunerConfDict[index]
                        confDict[configKeys.TUNER_INDEX] = index
                        success &= self.setTunerConfigurationNew(**confDict)
                # DDC configuration
                for ddcType in [configKeys.CONFIG_WBDDC, configKeys.CONFIG_NBDDC]:
                    isWideband = (ddcType == configKeys.CONFIG_WBDDC)
                    ddcConfDict = configDict2.get(configKeys.CONFIG_DDC,{}).get(ddcType,{})
                    ddcIndexRange = self.wbddcIndexList if isWideband else self.nbddcIndexList
                    for index in ddcIndexRange:
                        if index in ddcConfDict:
                            confDict = ddcConfDict[index]
                            confDict[configKeys.DDC_INDEX] = index
                            success &= self.setDdcConfigurationNew(wideband=isWideband, **confDict)
                # IP configuration
                success &= self.setIpConfigurationNew(configDict2.get(configKeys.CONFIG_IP, {}))
                # Transmitter configuration
                txConfDict = configDict2.get(configKeys.CONFIG_TX,{})
                for index in self.getTransmitterIndexRange():
                    if index in txConfDict:
                        confDict = txConfDict[index]
                        confDict[configKeys.TX_INDEX] = index
                        success &= self.setTxConfigurationNew(**confDict)
                for ducType in [configKeys.CONFIG_WBDUC, configKeys.CONFIG_NBDUC]:
                    isWideband = (ducType == configKeys.CONFIG_WBDUC)
                    ducConfDict = configDict2.get(configKeys.CONFIG_DUC,{}).get(ducType,{})
                    ducIndexRange = self.wbducIndexList if isWideband else self.nbducIndexList
                    for index in ducIndexRange:
                        if index in ducConfDict:
                            confDict = ducConfDict[index]
                            confDict[configKeys.DUC_INDEX] = index
                            success &= self.setDucConfigurationNew(wideband=isWideband, **confDict)
                # DDC group configuration
                for ddcType in [configKeys.CONFIG_WBDDC_GROUP, configKeys.CONFIG_NBDDC_GROUP]:
                    # Flag for forcing the driver to query DDCs for status information
                    forceDdcQuery = False
                    isWideband = (ddcType == configKeys.CONFIG_WBDDC_GROUP)
                    ddcGroupConfDict = configDict2.get(configKeys.CONFIG_DDC_GROUP,{}).get(ddcType,{})
                    ddcGroupIndexRange = self.wbddcGroupIndexList if isWideband else self.nbddcGroupIndexList
                    for index in ddcGroupIndexRange:
                        if index in ddcGroupConfDict:
                            confDict = ddcGroupConfDict[index]
                            confDict[configKeys.INDEX] = index
                            success &= self.setDdcGroupConfigurationNew(wideband=isWideband, **confDict)
                            # Force DDC query if DDC grouping configuration gets changed
                            forceDdcQuery = True
                    # This section forces hardware queries to update the corresponding DDC
                    # and DDC group configurations.
                    if forceDdcQuery:
                        ddcDict = self.wbddcDict if isWideband else self.nbddcDict
                        for i in self._getIndexList(None, ddcDict):
                            ddcDict[i]._queryConfiguration()
                        ddcGroupDict = self.wbddcGroupDict if isWideband else self.nbddcGroupDict
                        for i in self._getIndexList(None, ddcGroupDict):
                            ddcGroupDict[i]._queryConfiguration()
                # Combined DDC group configuration
                for ddcType in [configKeys.CONFIG_COMBINED_DDC_GROUP]:
                    #self.logIfVerbose("[ndr551][setConfiguration()] Configure combined DDCs")
                    # Flag for forcing the driver to query DDCs for status information
                    forceDdcQuery = False
                    ddcGroupConfDict = configDict2.get(configKeys.CONFIG_DDC_GROUP,{}).get(ddcType,{})
                    ddcGroupIndexRange = self.cddcGroupIndexList
                    for index in ddcGroupIndexRange:
                        if index in ddcGroupConfDict:
                            confDict = ddcGroupConfDict[index]
                            confDict[configKeys.INDEX] = index
                            #self.logIfVerbose("[ndr551][setConfiguration()] Combined DDC", index)
                            #self.logIfVerbose("[ndr551][setConfiguration()] %s" % confDict)
                            success &= self.setCombinedDdcGroupConfigurationNew(**confDict)
                            # Force DDC query if DDC grouping configuration gets changed
                            forceDdcQuery = True
                    # This section forces hardware queries to update the corresponding DDC
                    # and DDC group configurations.
                    if forceDdcQuery:
                        for isWideband in [True, False]:
                            ddcDict = self.wbddcDict if isWideband else self.nbddcDict
                            for i in self._getIndexList(None, ddcDict):
                                ddcDict[i]._queryConfiguration()
                        ddcGroupDict = self.cddcGroupDict
                        for i in self._getIndexList(None, ddcGroupDict):
                            ddcGroupDict[i]._queryConfiguration()
                # DUC configuration
                for ducType in [configKeys.CONFIG_WBDUC_GROUP]:
                    # Flag for forcing the driver to query DUCs for status information
                    forceDucQuery = False
                    isWideband = (ducType == configKeys.CONFIG_WBDUC_GROUP)
                    ducGroupConfDict = configDict2.get(configKeys.CONFIG_DUC_GROUP,{}).get(ducType,{})
                    ducGroupIndexRange = self.wbducGroupIndexList if isWideband else self.nbducGroupIndexList
                    for index in ducGroupIndexRange:
                        if index in ducGroupConfDict:
                            confDict = ducGroupConfDict[index]
                            confDict[configKeys.INDEX] = index
                            success &= self.setDucGroupConfigurationNew(wideband=isWideband, **confDict)
                            # Force DUC query if DUC grouping configuration gets changed
                            forceDucQuery = True
                    # This section forces hardware queries to update the corresponding DUC
                    # and DUC group configurations.
                    if forceDucQuery:
                        ducDict = self.wbducDict if isWideband else self.nbducDict
                        for i in self._getIndexList(None, ducDict):
                            ducDict[i]._queryConfiguration()
                        ducGroupDict = self.wbducGroupDict if isWideband else self.nbducGroupDict
                        for i in self._getIndexList(None, ducGroupDict):
                            ducGroupDict[i]._queryConfiguration()
                # FFT streaming configuration
                fftStreamConfDict = configDict2.get(configKeys.CONFIG_FFT,{})
                for index in self.fftStreamIndexList:
                    if index in fftStreamConfDict:
                        confDict = fftStreamConfDict[index]
                        confDict[configKeys.FFT_INDEX] = index
                        success &= self.setFftStreamConfiguration(**confDict)
                # Tuner group configuration
                forceTunerQuery = False
                tunerGroupConfDict = configDict2.get(configKeys.CONFIG_TUNER_GROUP,{})
                tunerGroupIndexRange = self.tunerGroupIndexList
                for index in tunerGroupIndexRange:
                    if index in tunerGroupConfDict:
                        confDict = tunerGroupConfDict[index]
                        confDict[configKeys.INDEX] = index
                        success &= self.setTunerGroupConfigurationNew(**confDict)
                        # Force tuner query if tuner grouping configuration gets changed
                        forceTunerQuery = True
                if forceTunerQuery:
                    for i in self._getIndexList(None, self.tunerDict):
                        self.tunerDict[i]._queryConfiguration()
                    for i in self._getIndexList(None, self.tunerGroupDict):
                        self.tunerGroupDict[i]._queryConfiguration()
                return success
    
    ##
    # \brief Sets the radio configuration based on a sequence of configuration
    #    dictionary keys.
    #
    # \copydetails CyberRadioDriver::IRadio::setConfigurationByKeys()
    def setConfigurationByKeys(self, value=None, *keys):
        configDict = {}
        self._dictEnsureEntrySet(configDict, value, *keys)
        return self.setConfiguration(configDict)
    
    ##
    # \brief Gets the radio configuration.
    #
    # \copydetails CyberRadioDriver::IRadio::getConfiguration()
    def getConfiguration(self):
        ret = None
        if self.isCrddConnection:
            ret = self._crddGetConfiguration()
        else:
            self.cmdErrorInfo = []
            ret = configKeys.Configurable.getConfiguration(self)
            # Get tuner configuration
            if self.numTuner > 0:
                ret[configKeys.CONFIG_TUNER] = self.getTunerConfigurationNew()
            # Get DDC configuration
            if self.numWbddc > 0:
                ret[configKeys.CONFIG_DDC] = {}
                # -- Wideband
                ret[configKeys.CONFIG_DDC][configKeys.CONFIG_WBDDC] = self.getDdcConfigurationNew(wideband=True)
                if self.numNbddc > 0:
                    # -- Narrowband
                    ret[configKeys.CONFIG_DDC][configKeys.CONFIG_NBDDC] = self.getDdcConfigurationNew(wideband=False)
            if self.numFftStream > 0:
                ret[configKeys.CONFIG_FFT] = self.getFftStreamConfiguration()
            # Get transmitter configuration
            if self.numTxs > 0:
                ret[configKeys.CONFIG_TX] = self.getTxConfigurationNew()
            # Get DUC configuration
            if self.numTxs > 0:
                ret[configKeys.CONFIG_DUC] = {}
                # -- Wideband
                ret[configKeys.CONFIG_DUC][configKeys.CONFIG_WBDUC] = self.getDucConfigurationNew(wideband=True)
                if self.numNbduc > 0:
                    # -- Narrowband
                    ret[configKeys.CONFIG_DDC][configKeys.CONFIG_NBDUC] = self.getDucConfigurationNew(wideband=False)
            # Get DDC group configuration
            if self.numWbddcGroups > 0:
                ret[configKeys.CONFIG_DDC_GROUP] = {}
                # -- Wideband
                ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_WBDDC_GROUP] = \
                          self.getDdcGroupConfigurationNew(wideband=True)
                if self.numNbddcGroups > 0:
                    # -- Narrowband
                    ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_NBDDC_GROUP] = \
                          self.getDdcGroupConfigurationNew(wideband=False)
            elif self.numCddcGroups > 0:
                ret[configKeys.CONFIG_DDC_GROUP] = {}
                ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_COMBINED_DDC_GROUP] = \
                          self.getCombinedDdcGroupConfigurationNew()
            # Get DUC group configuration
            if self.numWbducGroups > 0:
                ret[configKeys.CONFIG_DUC_GROUP] = {}
                # -- Wideband
                ret[configKeys.CONFIG_DUC_GROUP][configKeys.CONFIG_WBDUC_GROUP] = \
                          self.getDucGroupConfigurationNew(wideband=True)
    #             if self.numNbducGroups > 0:
    #                 # -- Narrowband
    #                 ret[configKeys.CONFIG_DUC_GROUP][configKeys.CONFIG_NBDUC_GROUP] = \
    #                       self.getDucGroupConfigurationNew(wideband=False)
            # Get tuner group configuration
            if self.numTunerGroups > 0:
                ret[configKeys.CONFIG_TUNER_GROUP] = \
                          self.getTunerGroupConfigurationNew()
        return ret 
    
    ##
    # \brief Gets radio configuration information based on a sequence of configuration
    #    dictionary keys.
    #
    # \copydetails CyberRadioDriver::IRadio::getConfigurationByKeys()
    def getConfigurationByKeys(self, *keys):
        return self._dictSafeGet(self.getConfiguration(), None, *keys)

    ##
    # \brief Queries the radio hardware to get its configuration.
    #
    # \copydetails CyberRadioDriver::IRadio::queryConfiguration()
    def queryConfiguration(self):
        return self.queryConfigurationByKeys()
    
    ##
    # \brief Queries the radio hardware to get a subset of configuration information, 
    #    based on a sequence of configuration dictionary keys.
    #
    # \copydetails CyberRadioDriver::IRadio::queryConfigurationByKeys()
    def queryConfigurationByKeys(self, *keys):
        self.cmdErrorInfo = []
        ret = {}
        if self.isCrddConnection:
            ret = self._crddQueryConfigurationByKeys(*keys)
        else:
            if len(keys) == 0:
                ret = configKeys.Configurable.queryConfiguration(self)
            # Get tuner configuration
            if self.numTuner > 0:
                if len(keys) == 0:
                    ret[configKeys.CONFIG_TUNER] = self.queryTunerConfigurationNew(tunerIndex=None)
                elif len(keys) > 0 and keys[0] == configKeys.CONFIG_TUNER:
                    tunerIndex = None if len(keys) == 1 else int(keys[1])
                    ret[configKeys.CONFIG_TUNER] = self.queryTunerConfigurationNew(tunerIndex=tunerIndex)
            # Get DDC configuration
            if self.numWbddc > 0:
                if len(keys) == 0 or keys[0] == configKeys.CONFIG_DDC:
                    ret[configKeys.CONFIG_DDC] = {}
                    # -- Wideband
                    if len(keys) < 2:
                        ret[configKeys.CONFIG_DDC][configKeys.CONFIG_WBDDC] = self.queryDdcConfigurationNew(
                                wideband=True, ddcIndex=None)
                    elif keys[1] == configKeys.CONFIG_WBDDC:
                        ddcIndex = None if len(keys) == 2 else int(keys[2])
                        ret[configKeys.CONFIG_DDC][configKeys.CONFIG_WBDDC] = self.queryDdcConfigurationNew(
                                    wideband=True, ddcIndex=ddcIndex)
                    # -- Narrowband
                    if self.numNbddc > 0:
                        if len(keys) < 2:
                            ret[configKeys.CONFIG_DDC][configKeys.CONFIG_NBDDC] = self.queryDdcConfigurationNew(
                                    wideband=False, ddcIndex=None)
                        elif keys[1] == configKeys.CONFIG_NBDDC:
                            ddcIndex = None if len(keys) == 2 else int(keys[2])
                            ret[configKeys.CONFIG_DDC][configKeys.CONFIG_NBDDC] = self.queryDdcConfigurationNew(
                                        wideband=False, ddcIndex=ddcIndex)
            # Get FFT Stream configuration
            if self.numFftStream > 0:
                if len(keys) == 0:
                    ret[configKeys.CONFIG_FFT] = self.queryFftStreamConfiguration(fftStreamIndex=None)
                elif len(keys) > 0 and keys[0] == configKeys.CONFIG_FFT:
                    fftStreamIndex = None if len(keys) == 1 else int(keys[1])
                    ret[configKeys.CONFIG_FFT] = self.queryFftStreamConfiguration(fftStreamIndex=fftStreamIndex)
            # Get transmitter configuration
            if self.numTxs > 0:
                if len(keys) == 0:
                    ret[configKeys.CONFIG_TX] = self.queryTxConfigurationNew(txIndex=None)
                elif len(keys) > 0 and keys[0] == configKeys.CONFIG_TX:
                    txIndex = None if len(keys) == 1 else int(keys[1])
                    ret[configKeys.CONFIG_TX] = self.queryTxConfigurationNew(txIndex=txIndex)
            # Get DUC configuration
            if self.numTxs > 0:
                if len(keys) == 0 or keys[0] == configKeys.CONFIG_DUC:
                    ret[configKeys.CONFIG_DUC] = {}
                    # -- Wideband
                    if len(keys) < 2:
                        ret[configKeys.CONFIG_DUC][configKeys.CONFIG_WBDUC] = self.queryDucConfigurationNew(
                                wideband=True, ducIndex=None)
                    elif keys[1] == configKeys.CONFIG_WBDUC:
                        ducIndex = None if len(keys) == 2 else int(keys[2])
                        ret[configKeys.CONFIG_DUC][configKeys.CONFIG_WBDUC] = self.queryDucConfigurationNew(
                                    wideband=True, ducIndex=ducIndex)
                    # -- Narrowband
                    if self.numNbduc > 0:
                        if len(keys) < 2:
                            ret[configKeys.CONFIG_DUC][configKeys.CONFIG_NBDUC] = self.queryDucConfigurationNew(
                                    wideband=False, ducIndex=None)
                        elif keys[1] == configKeys.CONFIG_NBDUC:
                            ducIndex = None if len(keys) == 2 else int(keys[2])
                            ret[configKeys.CONFIG_DUC][configKeys.CONFIG_NBDUC] = self.queryDucConfigurationNew(
                                        wideband=False, ducIndex=ducIndex)
            # Get DDC group configuration
            if any( [self.numWbddcGroups > 0, self.numNbddcGroups > 0, self.numCddcGroups > 0] ):
                if len(keys) == 0 or keys[0] == configKeys.CONFIG_DDC_GROUP:
                    ret[configKeys.CONFIG_DDC_GROUP] = {}
                    # -- Wideband
                    if self.numWbddcGroups > 0:
                        if len(keys) < 2:
                            ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_WBDDC_GROUP] = \
                                    self.queryDdcGroupConfigurationNew(wideband=True, ddcGroupIndex=None)
                        elif keys[1] == configKeys.CONFIG_WBDDC_GROUP:
                            ddcGroupIndex = None if len(keys) == 2 else int(keys[2])
                            ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_WBDDC_GROUP] = \
                                    self.queryDdcGroupConfigurationNew(wideband=True, ddcGroupIndex=ddcGroupIndex)
                    # -- Narrowband
                    if self.numNbddcGroups > 0:
                        if len(keys) < 2:
                            ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_NBDDC_GROUP] = \
                                    self.queryDdcGroupConfigurationNew(wideband=False, ddcGroupIndex=None)
                        elif keys[1] == configKeys.CONFIG_NBDDC_GROUP:
                            ddcGroupIndex = None if len(keys) == 2 else int(keys[2])
                            ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_NBDDC_GROUP] = \
                                    self.queryDdcGroupConfigurationNew(wideband=False, ddcGroupIndex=ddcGroupIndex)
                    # -- Combined (wideband + narrowband)
                    if self.numCddcGroups > 0:
                        if len(keys) < 2:
                            ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_COMBINED_DDC_GROUP] = \
                                    self.queryCombinedDdcGroupConfigurationNew(ddcGroupIndex=None)
                        elif keys[1] == configKeys.CONFIG_COMBINED_DDC_GROUP:
                            ddcGroupIndex = None if len(keys) == 2 else int(keys[2])
                            ret[configKeys.CONFIG_DDC_GROUP][configKeys.CONFIG_COMBINED_DDC_GROUP] = \
                                    self.queryCombinedDdcGroupConfigurationNew(ddcGroupIndex=ddcGroupIndex)
            # Get DUC group configuration
            if any( [self.numWbducGroups > 0] ):
                if len(keys) == 0 or keys[0] == configKeys.CONFIG_DUC_GROUP:
                    ret[configKeys.CONFIG_DUC_GROUP] = {}
                    # -- Wideband
                    if self.numWbducGroups > 0:
                        if len(keys) < 2:
                            ret[configKeys.CONFIG_DUC_GROUP][configKeys.CONFIG_WBDUC_GROUP] = \
                                    self.queryDucGroupConfigurationNew(wideband=True, ducGroupIndex=None)
                        elif keys[1] == configKeys.CONFIG_WBDUC_GROUP:
                            ducGroupIndex = None if len(keys) == 2 else int(keys[2])
                            ret[configKeys.CONFIG_DUC_GROUP][configKeys.CONFIG_WBDUC_GROUP] = \
                                    self.queryDucGroupConfigurationNew(wideband=True, ducGroupIndex=ducGroupIndex)
            # Get tuner group configuration
            if self.numTunerGroups > 0:
                if len(keys) == 0:
                    ret[configKeys.CONFIG_TUNER_GROUP] = self.queryTunerGroupConfigurationNew(
                            tunerGroupIndex=None)
                elif len(keys) > 0 and keys[0] == configKeys.CONFIG_TUNER_GROUP:
                    tunerGroupIndex = None if len(keys) == 1 else int(keys[1])
                    ret[configKeys.CONFIG_TUNER_GROUP] = self.queryTunerGroupConfigurationNew(
                            tunerGroupIndex=tunerGroupIndex)
            # Query IP configuration
            if len(keys) == 0 or keys[0] == configKeys.CONFIG_IP:
                if len(keys) == 0:
                    ret[configKeys.CONFIG_IP] = self.queryIpConfigurationNew(gigEPortIndex=None)
                elif len(keys) > 0 and keys[0] == configKeys.CONFIG_IP:
                    gigEPortIndex = None if len(keys) == 1 else int(keys[1])
                    ret[configKeys.CONFIG_IP] = self.queryIpConfigurationNew(gigEPortIndex=gigEPortIndex)
        # Update the internal configuration dictionary based on query results
        self.configuration.update(ret)
        # Return the result
        return ret 

    ##
    # \protected
    # \brief Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # Override
        for cmdClass, configKey in [ \
                                (self.cfgCmd, configKeys.CONFIG_MODE), \
                                (self.refCmd, configKeys.REFERENCE_MODE), \
                                (self.rbypCmd, configKeys.BYPASS_MODE), \
                                (self.calfCmd, configKeys.CALIB_FREQUENCY), \
                                (self.fnrCmd, configKeys.FNR_MODE), \
                                (self.gpsCmd, configKeys.GPS_ENABLE), \
                                (self.rtvCmd, configKeys.REF_TUNING_VOLT), \
                                (self.fpgaStateCmd, configKeys.FPGA_STATE), \
                                (self.funCmd, configKeys.RADIO_FUNCTION), \
                                (self.refCmd, configKeys.STATUS_PPS_SOURCE), \
                                # (self.cntrlCmd, configKeys.CNTRL_IF_OUT), \
                              ]:
            if cmdClass is not None:
                cmd = cmdClass(parent=self, 
                               query=True,
                                verbose=self.verbose, logFile=self.logFile)
                cmd.send( self.sendCommand, )
                self._addLastCommandErrorInfo(cmd)
                rspInfo = cmd.getResponseInfo()
                #self.logIfVerbose("DEBUG:", cmd.mnemonic, "rspInfo=", rspInfo)
                if rspInfo is not None:
                    self.configuration[configKey] = rspInfo.get(configKey, 0)
        # IP configuration query -- The format of this section depends on whether
        # the radio has Gigabit Ethernet ports on it or not.
        if configKeys.CONFIG_IP not in self.configuration:
            self.configuration[configKeys.CONFIG_IP] = {}
        self.configuration[configKeys.CONFIG_IP].update( self.queryIpConfigurationNew() )

    ##
    # \protected
    # \brief Issues hardware commands to set the object's current configuration.  
    def _setConfiguration(self, confDict):
        ret = True
        for cmdClass, configKey in [ \
                                (self.cfgCmd, configKeys.CONFIG_MODE), \
                                (self.refCmd, configKeys.REFERENCE_MODE), \
                                (self.rbypCmd, configKeys.BYPASS_MODE), \
                                (self.calfCmd, configKeys.CALIB_FREQUENCY), \
                                (self.fnrCmd, configKeys.FNR_MODE), \
                                (self.gpsCmd, configKeys.GPS_ENABLE), \
                                (self.rtvCmd, configKeys.REF_TUNING_VOLT), \
                                (self.fpgaStateCmd, configKeys.FPGA_STATE), \
                                (self.refCmd, configKeys.STATUS_PPS_SOURCE), \
                                (self.cntrlCmd, configKeys.CNTRL_IF_OUT), \
                              ]:
            cDict = { "parent": self, \
                      "verbose": self.verbose, \
                      "logFile": self.logFile, \
                      configKey: confDict.get(configKey, 0)
                     }
            if configKey in confDict and cmdClass is not None and \
               cmdClass.settable:
                cmd = cmdClass(**cDict)
                ret &= cmd.send( self.sendCommand, )
                ret &= cmd.success
                self._addLastCommandErrorInfo(cmd)
                if ret:
                    self.configuration[configKey] = getattr(cmd, configKey)
                pass
        return ret

    ##
    # \protected
    # \brief Gets whether or not the given (nested) dictionary has an entry for the given keys.
    #
    # \param dicty The dictionary to search.
    # \param keys A number of comma-separated search keys, each pointing to a deeper level
    #    of the dictionary hierarchy.
    # \return True if the dictionary has the entry, False otherwise.
    def _dictHasEntry(self, dicty, *keys):
        ret = True
        keysOk = [ q != "" for q in keys ]
        if all(keysOk):
            tmp = dicty
            for key in keys:
                if key not in tmp:
                    ret = False
                    break
                else:
                    tmp = tmp[key]
        else:
            ret = False
        return ret
    
    ##
    # \protected
    # \brief Ensures that we make an entry in the given dictionary with the specified keys, using
    #    the provided default for the entry.
    #
    # @param dicty The dictionary to manipulate.
    # @param default The default value to use for the entry if it does not already exist.
    # @param keys A number of comma-separated search keys, each pointing to a deeper level
    #    of the dictionary hierarchy.
    def _dictEnsureEntry(self, dicty, default, *keys):
        tmp = dicty
        # Create intermediate sub-dicts if needed
        for i, key in enumerate(keys):
            if i < len(keys)-1:
                if key not in tmp:
                    #print "[DBG] sub-dict key", key, "not present"
                    tmp[key] = {}
                else:
                    #print "[DBG] sub-dict key", key, "present"
                    pass
                tmp = tmp[key]
            else:
                if key not in tmp:
                    #print "[DBG] value key", key, "not present"
                    tmp[key] = default
                else:
                    #print "[DBG] value key", key, "present"
                    pass
        pass
    
    ##
    # \protected
    # \brief Ensures that a given nested dictionary item is set to the provided value, 
    #    even if the item does not already exist.
    # \param dicty The dictionary to manipulate.
    # \param value The value to set the entry to.
    # \param keys A number of comma-separated search keys, each pointing to a deeper level
    #    of the dictionary hierarchy.
    def _dictEnsureEntrySet(self, dicty, value, *keys):
        self._dictEnsureEntry(dicty, value, *keys)
        tmp = dicty
        for i, key in enumerate(keys):
            if i < len(keys)-1:
                tmp = tmp[key]
            else:
                try:
                    tmp[key] = copy.deepcopy(value)
                except:
                    tmp[key] = value

    ##
    # \protected
    # \brief Gets a value from a dictionary in a "safe" way, using a default in case there is
    #    no entry for the given set of keys.
    #
    # \param dicty The dictionary to query.
    # \param default The default value to use if the keys do not point to a valid entry.
    # \param keys A number of comma-separated search keys, each pointing to a deeper level
    #    of the dictionary hierarchy.
    # \return The entry from the dictionary, or the default if the entry does not exist.
    def _dictSafeGet(self, dicty, default, *keys):
        ret = default if len(keys) > 0 else dicty
        if self._dictHasEntry(dicty, *keys):
            tmp = dicty
            for i, key in enumerate(keys):
                if i < len(keys)-1:
                    tmp = tmp[key]
                else:
                    ret = tmp[key]
        return ret
    
    ##
    # \internal
    # \brief Initializes the radio handler object after connecting to crdd.
    #
    def _crddInitialize(self):
        # Optionally, send crdd our client ID
        if self.clientId is not None:
            rsp = self._crddSendCommand(cmd="CLIENTID", data=self.clientId)
        # Get the radio's current configuration from crdd
        self._crddGetConfiguration()
        pass
    
    ##
    # \internal
    # \brief Sends a command to crdd.
    # \note This capability does not depend on whether the radio is JSON or not. 
    # \param cmd Command mnemonic
    # \param data Data to send as a command parameter.  What actually gets sent
    #    over the link is this object's string representation.  Can be None, in 
    #    which case only the command gets sent.
    # \returns Either a list of response strings (if the command completed
    #    successfully), or None (if it did not). 
    def _crddSendCommand(self, cmd, data=None):
        outCmd = self.crddCommandPrefix + str(cmd)
        if data is not None:
            outCmd += " " + str(data)
        outCmd += "\n"
        return self.sendCommand(outCmd)
    
    ##
    # \internal
    # \brief Unpacks the provided configuration dictionary, setting the 
    #     configuration of all components.
    # \param configuration Fully-specified configuration dictionary.
    def _crddUnpackConfiguration(self, configuration):
        # Unpack the full configuration
        fullConfiguration = copy.deepcopy(configuration)
        # -- Tuner configuration
        cDict = fullConfiguration.pop(configKeys.CONFIG_TUNER, {})
        for index in list(cDict.keys()):
            self.tunerDict[index].configuration = cDict[index]
        # -- DDC configuration
        cDict = fullConfiguration.pop(configKeys.CONFIG_DDC, {})
        for ddcType in list(cDict.keys()):
            ddcDict = self.wbddcDict 
            if ddcType == "narrowband":
                ddcDict = self.nbddcDict
            for index in list(cDict[ddcType].keys()):
                ddcDict[index].configuration = cDict[ddcType][index]
        # -- FFT streams
        cDict = fullConfiguration.pop(configKeys.CONFIG_FFT, {})
        for index in list(cDict.keys()):
            self.fftStreamDict[index].configuration = cDict[index]
        # -- TX configuration
        cDict = fullConfiguration.pop(configKeys.CONFIG_TX, {})
        for index in list(cDict.keys()):
            cDict2 = cDict[index].pop(configKeys.CONFIG_CW, {})
            for index2 in list(cDict2.keys()):
                self.txDict[index].toneGenDict[index2].configuration = cDict2[index2]
            self.txDict[index].configuration = cDict[index]
        # -- DUC configuration
        cDict = fullConfiguration.pop(configKeys.CONFIG_DUC, {})
        for ducType in list(cDict.keys()):
            ducDict = self.wbducDict 
            if ducType == "narrowband":
                ducDict = self.nbducDict
            for index in list(cDict[ducType].keys()):
                ducDict[index].configuration = cDict[ducType][index]
        # -- DDC group configuration
        cDict = fullConfiguration.pop(configKeys.CONFIG_DDC_GROUP, {})
        for ddcType in list(cDict.keys()):
            ddcDict = self.wbddcGroupDict
            if ddcType == "narrowband":
                ddcDict = self.nbddcGroupDict
            elif ddcType == "combined":
                ddcDict = self.cddcGroupDict
            for index in list(cDict[ddcType].keys()):
                ddcDict[index].configuration = cDict[ddcType][index]
        # -- WBDUC groups
        cDict = fullConfiguration.pop(configKeys.CONFIG_DUC_GROUP, {})
        for ducType in list(cDict.keys()):
            ducDict = self.wbducGroupDict 
            #if ducType == "narrowband":
            #    ducDict = self.nbducGroupDict
            for index in list(cDict[ducType].keys()):
                ducDict[index].configuration = cDict[ducType][index]
        # -- Tuner groups
        cDict = fullConfiguration.pop(configKeys.CONFIG_TUNER_GROUP, {})
        for index in list(cDict.keys()):
            self.tunerGroupDict[index].configuration = cDict[index]
        # -- What is left after all the popping are the radio-specific 
        #    config items, and the IP config
        self.configuration = fullConfiguration
        pass
    
    ##
    # \internal
    # \brief Gets the radio's current configuration from crdd.
    # \note This capability does not depend on whether the radio is JSON or not. 
    # \returns Either the returned configuration dictionary (if the command 
    #    completed successfully), or an empty dictionary (if it did not). 
    def _crddGetConfiguration(self):
        ret = {}
        # Get the radio's current configuration from crdd
        rsp = self._crddSendCommand(cmd="GETCFG", data=None)
        # Deal with out-of-bound conditions
        try:
            if all( [
                    rsp is not None,
                    rsp != "Empty Read",
                    rsp[0] != "TIMEOUT"
                ] ):
                # Get the returned full configuration by running the first response 
                # string (the config dict) through ast.literal_eval().
                ret = ast.literal_eval(rsp[0])
                # Unpack the full configuration
                self._crddUnpackConfiguration(ret)
        except:
            pass
        return ret
    
    ##
    # \internal
    # \brief Sets the radio's current configuration using crdd.
    # \note This capability does not depend on whether the radio is JSON or not. 
    # \return True if all commands completed successfully, False otherwise.
    #    Use getLastCommandErrorInfo() to retrieve any error information.
    def _crddSetConfiguration(self, configDict={}):
        ret = False
        # Get the radio's current configuration from crdd
        rsp = self._crddSendCommand(cmd="SETCFG", data=configDict)
        # Deal with out-of-bound conditions
        try:
            if all( [
                    rsp is not None,
                    rsp != "Empty Read",
                    rsp[0] != "TIMEOUT"
                ] ):
                #self.log("[DBG] rsp =", str(rsp))
                # First response string: SUCCESS or ERROR (plus error info)
                ret = ( rsp[0] == "SUCCESS" )
                if not ret:
                    # Grab the error info (serialized as a list of strings)
                    self.cmdErrorInfo = ast.literal_eval(rsp[0].replace("ERROR: ", ""))
                # Second response string: Updated configuration dictionary string.  
                # Run this through ast.literal_eval().
                configuration = ast.literal_eval(rsp[1])
                # Unpack the full configuration
                self._crddUnpackConfiguration(configuration)
        except:
            pass
        return ret
    
    ##
    # \internal
    # \brief Queries the radio's current configuration from crdd.
    # \note This capability does not depend on whether the radio is JSON or not. 
    # \param keys List of keys used to specify which configuration values to query.
    # \returns Either the returned configuration dictionary (if the command 
    #    completed successfully), or an empty dictionary (if it did not). 
    def _crddQueryConfigurationByKeys(self, *keys):
        ret = {}
        # Query the radio's current configuration from crdd
        rsp = self._crddSendCommand(cmd="QUERYCFGK", data=list(keys))
        # Deal with out-of-bound conditions
        try:
            if all( [
                    rsp is not None,
                    rsp != "Empty Read",
                    rsp[0] != "TIMEOUT"
                ] ):
                # Get the returned configuration by running the first response 
                # string (the config dict) through ast.literal_eval().
                ret = ast.literal_eval(rsp[0])
        except:
            pass
        return ret
    
    ##
    # \internal
    # \brief Gets the list of currently connected data port indices from crdd.
    # \note This capability does not depend on whether the radio is JSON or not. 
    # \returns Either the returned data port list (if the command 
    #    completed successfully), or an empty list (if it did not). 
    def _crddGetConnectedDataPortIndices(self):
        ret = []
        # Get the radio's current configuration from crdd
        rsp = self._crddSendCommand(cmd="QUERYCDPS", data=None)
        # Deal with out-of-bound conditions
        try:
            if all( [
                    rsp is not None,
                    rsp != "Empty Read",
                    rsp[0] != "TIMEOUT"
                ] ):
                # Get the returned list by running the first response 
                # string (the data port list) through ast.literal_eval().
                ret = ast.literal_eval(rsp[0])
        except:
            pass
        return ret
    
    ##
    # \internal
    # \brief Helper method for converting Unicode strings to ASCII strings
    #    during the JSON conversion process.
    #
    # The JSON-formatted string will have elements whose names 
    # correspond to the names of this entity's attributes.  
    #
    # \param data The entity being encoded as JSON.
    @staticmethod
    def encodeJsonAsAscii(data):
        def _foo(item):
            ret = item
            if isinstance(item, str):
                ret = item.encode('ascii')
            elif isinstance(item, list):
                ret = [ _foo(q) for q in item ]
            elif isinstance(item, dict):
                ret = { _foo(key): _foo(value) for key, value in item.items() }
            return ret
        adjPairs = []
        for pair in data:
            adjPairs.append( (_foo(pair[0]), _foo(pair[1])) )
        return dict(adjPairs)

    ##
    # \brief Resets the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::sendReset()
    def sendReset(self, resetType=None):
        if self.resetCmd is not None:
            cDict = { "parent": self, 
                      "verbose": self.verbose,
                      "logFile": self.logFile,
                      configKeys.RESET_TYPE: resetType,
                     }
            cmd = self.resetCmd(**cDict)
            cmd.send( self.sendCommand, )
            return cmd.success
        else:
            return False
        #time.sleep(20)
        #self.connect(self.mode,self.host_or_dev,self.port_or_baudrate)
    
    ##
    # \brief Gets the pulse-per-second (PPS) rising edge from the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getPps()
    def getPps(self):
        if self.ppsCmd is not None:
            cmd = command.pps(parent=self,query=True,
                              verbose=self.verbose, logFile=self.logFile)
            cmd.send(self.sendCommand, timeout=cmd.timeout)
            return cmd.success
        else:
            return False
    
    ##
    # \brief Sets the time for the next PPS rising edge on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::setTimeNextPps()
    def setTimeNextPps(self,checkTime=False,useGpsTime=False,newPpsTime=None):
        if self.ppsCmd is not None and self.utcCmd is not None:
            if self.getPps():
                if newPpsTime is not None:
                    nextSecond = int( _radio.timeFromString(newPpsTime, utc=True) )
                    cmd = self.utcCmd( parent=self, utcTime=str(nextSecond),
                                       verbose=self.verbose, logFile=self.logFile )
                elif useGpsTime:
                    cmd = self.utcCmd( parent=self, utcTime="g" )
                else:
                    nextSecond = int( math.floor( time.time() ) )+1
                    cmd = self.utcCmd( parent=self, utcTime=str(nextSecond),
                                       verbose=self.verbose, logFile=self.logFile )
                cmd.send( self.sendCommand, timeout=cmd.timeout )
                if checkTime:
                    radioUtc = self.getTimeNextPps()
                    self.logIfVerbose("Set time = %d & Query time = %d" % (nextSecond,radioUtc))
                    return radioUtc==nextSecond
                else:
                    return cmd.success
            else:
                self.log("ERROR, ERROR, ERROR".center(80,"!"))
                return False
        else:
            return False
            
    ##
    # \brief Gets the current radio time.
    #
    # \copydetails CyberRadioDriver::IRadio::getTimeNow()
    def getTimeNow(self):
        if self.utcCmd is not None:
            cmd = self.utcCmd( parent=self, query=True,
                               verbose=self.verbose, logFile=self.logFile  )
            cmd.send( self.sendCommand, timeout=cmd.timeout )
            return cmd.getResponseInfo().get(configKeys.TIME_UTC, None)
        else:
            return None
    
    ##
    # \brief Gets the time for the next PPS rising edge on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTimeNextPps()
    def getTimeNextPps(self):
        if self.ppsCmd is not None and self.utcCmd is not None:
            if self.getPps():
                cmd = self.utcCmd( parent=self, query=True,
                                   verbose=self.verbose, logFile=self.logFile )
                cmd.send( self.sendCommand, timeout=cmd.timeout )
                return cmd.getResponseInfo().get(configKeys.TIME_UTC, None)
            else:
                return None
        else:
            return None
    
    ##
    # \brief Gets the status from the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getStatus()
    def getStatus(self):
        if self.statQry is not None:
            cmd = self.statQry(parent=self,
                               verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand )
            return cmd.getResponseInfo()
        else:
            self.log("No status query available.")
            return None
    
    ##
    # \brief Gets the RF tuner status from the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTstatus()
    def getTstatus(self):
        if self.tstatQry is not None:
            cmd = self.tstatQry(parent=self,
                                verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand )
            return cmd.getResponseInfo()
        else:
            self.log("No tuner status query available.")
            return None
    
    ##
    # \brief Sets the reference mode on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::setReferenceMode()
    def setReferenceMode(self,mode):
        try:
            modeInt = int(mode) if int(mode) in list(self.refModes.keys()) else None
        except:
            modeInt = None
        if modeInt is not None and self.refCmd is not None:
            self.logIfVerbose("Setting reference mode %d (%s)"%(modeInt,self.refModes.get(modeInt)))
            cmd = self.refCmd(parent=self, referenceMode=modeInt,
                              verbose=self.verbose, logFile=self.logFile)
            ret = cmd.send( self.sendCommand )
            if ret and cmd.success:
                self.configuration[configKeys.REFERENCE_MODE] = getattr(cmd, configKeys.REFERENCE_MODE)
            return cmd.success
        else:
            return False
    
    ##
    # \brief Sets the reference bypass mode on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::setBypassMode()
    def setBypassMode(self,mode):
        try:
            modeInt = int(mode) if int(mode) in list(self.rbypModes.keys()) else None
        except:
            modeInt = None
        if modeInt is not None and self.rbypCmd is not None:
            self.logIfVerbose("Setting bypass mode %d (%s)"%(modeInt,self.rbypModes.get(modeInt)))
            cmd = self.rbypCmd(parent=self, bypassMode=modeInt,
                               verbose=self.verbose, logFile=self.logFile)
            ret = cmd.send( self.sendCommand )
            if ret and cmd.success:
                self.configuration[configKeys.BYPASS_MODE] = getattr(cmd, configKeys.BYPASS_MODE)
            return cmd.success
        else:
            return False
            
    ##
    # \brief Sets the time adjustment for tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::setTimeAdjustment()
    def setTimeAdjustment(self, tunerIndex=None, timeAdjustValue=0):
        if self.tadjCmd is not None:
            success = True
            for i in self._getIndexList(tunerIndex, self.tunerDict):
#                 cmd = self.tadjCmd(parent=self,index=i, timingAdjustment=timeAdjustValue,
#                                   verbose=self.verbose, logFile=self.logFile)
#                 success &= cmd.send( self.sendCommand )
                success &= self.setConfiguration( {
                        configKeys.CONFIG_TUNER : {
                            i: {
                                configKeys.TUNER_TIMING_ADJ: timeAdjustValue,
                            }
                        }
                    } )
            return success
        else:
            return False

    ##
    # \brief Sets the calibration frequency on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::setCalibrationFrequency()
    def setCalibrationFrequency(self, calibFrequency=0):
        if self.calfCmd is not None:
            cmd = self.calfCmd(parent=self, calibFrequency=calibFrequency,
                               verbose=self.verbose, logFile=self.logFile)
            ret = cmd.send( self.sendCommand )
            if ret and cmd.success:
                self.configuration[configKeys.CALIB_FREQUENCY] = getattr(cmd, configKeys.CALIB_FREQUENCY)
            return cmd.success
        else:
            return False

    ##
    # \brief Gets the current GPS position.
    #
    # \copydetails CyberRadioDriver::IRadio::getGpsPosition()
    def getGpsPosition(self):
        # Helper function that converts GPS coordinates from the NMEA
        # format to decimal degrees
        def degMinToDecimalDeg(coordinate):
            # Converts from [NESW](d)ddmm.mmmm(mm) format to decimal degrees
            # degDigits == number of digits used for degrees (2 for lat, 3 for lon)
            # Last (decimal places + 3) characters == Minutes
            ret = 0.0
            # -- Get the sign from the directional indicator
            sgn = (-1 if coordinate[0] in ["W", "S"] else 1)
            # -- Find the decimal point position
            coord = coordinate[1:]
            dotPos = coord.find(".")
            minLen = len(coord) - dotPos + 2
            min = float( coord[-minLen:] )
            deg = float( coord[:-minLen] )
            if deg < 0.0:
                ret = deg - min / 60.0
            else:
                ret = deg + min / 60.0
            ret = ret * sgn
            return ret

        if self.gposCmd is not None:
            cmd = self.gposCmd( parent=self, query=True,
                                verbose=self.verbose, logFile=self.logFile  )
            cmd.send( self.sendCommand, timeout=cmd.timeout )
            latStr = cmd.getResponseInfo().get(configKeys.GPS_LATITUDE, "N0000.000000")
            lonStr = cmd.getResponseInfo().get(configKeys.GPS_LONGITUDE, "E0000.000000")
            return ( degMinToDecimalDeg(latStr), degMinToDecimalDeg(lonStr) )
        else:
            return (0.0, 0.0)
    
    ##
    # \brief Gets the current radio temperature.
    #
    # \copydetails CyberRadioDriver::IRadio::getTemperature()
    def getTemperature(self):
        if self.tempCmd is not None:
            cmd = self.tempCmd( parent=self, query=True,
                                verbose=self.verbose, logFile=self.logFile  )
            cmd.send( self.sendCommand, timeout=cmd.timeout )
            return cmd.getResponseInfo().get(configKeys.TEMPERATURE, 0)
        else:
            return 0
    
    ##
    # \brief Gets the current GPIO output bits.
    #    
    # \copydetails CyberRadioDriver::IRadio::getGpioOutput()
    def getGpioOutput(self):
        if self.gpioStaticCmd is not None:
            cmd = self.gpioStaticCmd( parent=self, query=True,
                                      verbose=self.verbose, 
                                      logFile=self.logFile  )
            cmd.send( self.sendCommand, timeout=cmd.timeout )
            return cmd.getResponseInfo().get(configKeys.GPIO_VALUE, 0)
        else:
            return 0
    
    ##
    # \brief Gets the GPIO output settings for a given sequence index.
    #    
    # \copydetails CyberRadioDriver::IRadio::getGpioOutputByIndex()
    def getGpioOutputByIndex(self, index):
        if self.gpioSeqCmd is not None:
            cmd = self.gpioSeqCmd( parent=self, query=True,
                                   index=index,
                                   verbose=self.verbose, 
                                   logFile=self.logFile  )
            cmd.send( self.sendCommand, timeout=cmd.timeout )
            return ( cmd.getResponseInfo().get(configKeys.GPIO_VALUE, 0),
                     cmd.getResponseInfo().get(configKeys.GPIO_DURATION, 0),
                     cmd.getResponseInfo().get(configKeys.GPIO_LOOP, 0) )
        else:
            return (0, 0, 0)
    
    ##
    # \brief Sets the current GPIO output bits.
    #    
    # \copydetails CyberRadioDriver::IRadio::setGpioOutput()
    def setGpioOutput(self, value):
        if self.gpioStaticCmd is not None:
            cmd = self.gpioStaticCmd(parent=self, 
                                     value=value,
                                     verbose=self.verbose, logFile=self.logFile)
            ret = cmd.send( self.sendCommand )
            return cmd.success
        else:
            return False
    
    ##
    # \brief Sets the GPIO output settings for a given sequence index.
    #    
    # \copydetails CyberRadioDriver::IRadio::setGpioOutputByIndex()
    def setGpioOutputByIndex(self, index, value, duration, loop, go):
        if self.gpioSeqCmd is not None:
            cmd = self.gpioSeqCmd(parent=self,
                                  index=index, 
                                  value=value,
                                  duration=duration,
                                  loop=loop,
                                  go=go,
                                  verbose=self.verbose, logFile=self.logFile)
            ret = cmd.send( self.sendCommand )
            return cmd.success
        else:
            return False
    
    ##
    # \brief Gets the current bandwith of the given tuner.
    # \copydetails CyberRadioDriver::IRadio::getTunerBandwidth()
    def getTunerBandwidth(self, tuner):
        if tuner not in self.getTunerIndexRange():
            raise ValueError("Invalid tuner specified")
        ret = self.tunerBandwidthConstant
        if self.tunerBandwithSettable:
            ifFilter = self.getConfigurationByKeys(
                    configKeys.CONFIG_TUNER,
                    tuner,
                    configKeys.TUNER_IF_FILTER
                )
            if ifFilter is not None:
                ret = ifFilter * 1e6
        return ret
    
    ##
    # \brief Gets the name of the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getName()
    @classmethod
    def getName(cls):
        return cls._name
    
    ##
    # \brief Gets the number of tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumTuner()
    @classmethod
    def getNumTuner(cls):
        return len(cls.getTunerIndexRange())
    
    ##
    # \brief Gets the number of tuner boards on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumTunerBoards()
    @classmethod
    def getNumTunerBoards(cls):
        return cls.numTunerBoards
    
    ##
    # \brief Gets the index range for the tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTunerIndexRange()
    @classmethod
    def getTunerIndexRange(cls):
        return list(range(cls.tunerIndexBase, cls.tunerIndexBase + cls.numTuner, 1))
    
    ##
    # \brief Gets the frequency range for the tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTunerFrequencyRange()
    @classmethod
    def getTunerFrequencyRange(cls):
        return cls.tunerType.frqRange
    
    ##
    # \brief Gets the frequency resolution for tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTunerFrequencyRes()
    @classmethod
    def getTunerFrequencyRes(cls):
        return cls.tunerType.frqRes
    
    ##
    # \brief Gets the frequency unit for tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTunerFrequencyUnit()
    @classmethod
    def getTunerFrequencyUnit(cls):
        return cls.tunerType.frqUnits
    
    ##
    # \brief Gets the attenuation range for the tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTunerAttenuationRange()
    @classmethod
    def getTunerAttenuationRange(cls):
        return cls.tunerType.attRange
    
    ##
    # \brief Gets the attenuation resolution for tuners on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTunerAttenuationRes()
    @classmethod
    def getTunerAttenuationRes(cls):
        return cls.tunerType.attRes

    ##
    # \brief Gets the ifFilter list for the tuners of the radio
    #
    # \copydetails CyberRadioDriver::IRadio::getTunerIfFilterList()
    @classmethod
    def getTunerIfFilterList(cls):
        return cls.tunerType.ifFilters
    
    ##
    # \brief Gets whether or not the radio supports setting tuner
    #     bandwidth
    #
    # \copydetails CyberRadioDriver::IRadio::isTunerBandwidthSettable()
    @classmethod
    def isTunerBandwidthSettable(cls):
        return cls.tunerBandwithSettable

    ##
    # \brief Gets the number of wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumWbddc()
    @classmethod
    def getNumWbddc(cls):
        return len(cls.getWbddcIndexRange())
    
    ##
    # \brief Gets whether the DDCs on the radio have selectable sources.
    #
    # \copydetails CyberRadioDriver::IRadio::isDdcSelectableSource()
    @classmethod
    def isDdcSelectableSource(cls, wideband):
        ddcType = cls.wbddcType if wideband else cls.nbddcType
        return False if ddcType is None else ddcType.selectableSource
    
    ##
    # \brief Gets whether the wideband or narrowband DDCs on the radio are tunable.
    #
    # \copydetails CyberRadioDriver::IRadio::isNbddcTunable()
    @classmethod
    def isDdcTunable(cls, wideband):
        ddcType = cls.wbddcType if wideband else cls.nbddcType
        return False if ddcType is None else ddcType.tunable
    
    ##
    # \brief Gets the index range for the wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcIndexRange()
    @classmethod
    def getWbddcIndexRange(cls):
        return list(range(cls.wbddcIndexBase, cls.wbddcIndexBase + cls.numWbddc, 1))
    
    ##
    # \brief Gets whether the wideband DDCs on the radio are tunable.
    #
    # \copydetails CyberRadioDriver::IRadio::isWbddcSelectableSource()
    @classmethod
    def isWbddcSelectableSource(cls):
        return False if cls.wbddcType is None else cls.wbddcType.selectableSource
    
    ##
    # \brief Gets whether the wideband DDCs on the radio have selectable
    # sources.
    #
    # \copydetails CyberRadioDriver::IRadio::isWbddcTunable()
    @classmethod
    def isWbddcTunable(cls):
        return False if cls.wbddcType is None else cls.wbddcType.tunable
    
    ##
    # \brief Gets the frequency offset range for the wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcFrequencyRange()
    @classmethod
    def getWbddcFrequencyRange(cls):
        return (0.0,0.0) if cls.wbddcType is None else cls.wbddcType.frqRange
    
    ##
    # \brief Gets the frequency offset resolution for wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcFrequencyRes()
    @classmethod
    def getWbddcFrequencyRes(cls):
        return 0.0 if cls.wbddcType is None else cls.wbddcType.frqRes
    
    ##
    # \brief Gets the allowed rate set for the wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcRateSet()
    @classmethod
    def getWbddcRateSet(cls, index=None):
        return cls.getDdcRateSet(True, index)
    
    ##
    # \brief Gets the allowed rate list for the wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcRateList()
    @classmethod
    def getWbddcRateList(cls, index=None):
        return cls.getDdcRateList(True, index)
    
    ##
    # \brief Gets the allowed rate set for the wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcBwSet()
    @classmethod
    def getWbddcBwSet(cls, index=None):
        return cls.getDdcBwSet(True, index)
    
    ##
    # \brief Gets the allowed rate list for the wideband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcBwList()
    @classmethod
    def getWbddcBwList(cls, index=None):
        return cls.getDdcBwList(True, index)
        
    ##
    # \brief Gets the number of narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumNbddc()
    @classmethod
    def getNumNbddc(cls):
        return len(cls.getNbddcIndexRange())
    
    ##
    # \brief Gets the index range for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcIndexRange()
    @classmethod
    def getNbddcIndexRange(cls):
        if cls.numNbddc == 0:
            return []
        elif cls.nbddcIndexOverride is not None:
            return cls.nbddcIndexOverride
        else:
            return list(range(cls.nbddcIndexBase, cls.nbddcIndexBase + cls.numNbddc, 1))
    
    ##
    # \brief Gets whether the narrowband DDCs on the radio are tunable.
    #
    # \copydetails CyberRadioDriver::IRadio::isNbddcTunable()
    @classmethod
    def isNbddcTunable(cls):
        return False if cls.nbddcType is None else cls.nbddcType.tunable
    
    ##
    # \brief Gets whether the narrowband DDCs on the radio have selectable
    # sources.
    #
    # \copydetails CyberRadioDriver::IRadio::isNbddcSelectableSource()
    @classmethod
    def isNbddcSelectableSource(cls):
        return False if cls.nbddcType is None else cls.nbddcType.selectableSource
    
    ##
    # \brief Gets the frequency offset range for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcFrequencyRange()
    @classmethod
    def getNbddcFrequencyRange(cls):
        return (0.0,0.0) if cls.nbddcType is None else cls.nbddcType.frqRange
    
    ##
    # \brief Gets the frequency offset resolution for narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcFrequencyRes()
    @classmethod
    def getNbddcFrequencyRes(cls):
        return 0.0 if cls.nbddcType is None else cls.nbddcType.frqRes
    
    ##
    # \brief Gets the allowed rate set for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcRateSet()
    @classmethod
    def getNbddcRateSet(cls, index=None):
        return cls.getDdcRateSet(False, index)
    
    ##
    # \brief Gets the allowed rate list for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcRateList()
    @classmethod
    def getNbddcRateList(cls, index=None):
        return cls.getDdcRateList(False, index)
        
    ##
    # \brief Gets the allowed rate set for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcBwSet()
    @classmethod
    def getNbddcBwSet(cls, index=None):
        return cls.getDdcBwSet(False, index)
    
    ##
    # \brief Gets the allowed rate list for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcBwList()
    @classmethod
    def getNbddcBwList(cls, index=None):
        return cls.getDdcBwList(False, index)
        
    ##
    # \brief Gets the number of narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumFftStream()
    @classmethod
    def getNumFftStream(cls):
        return len(cls.getFftStreamIndexRange())
    
    ##
    # \brief Gets the index range for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getFftStreamIndexRange()
    @classmethod
    def getFftStreamIndexRange(cls):
        return [] if cls.numFftStream == 0 else \
               list(range(cls.fftStreamIndexBase, cls.fftStreamIndexBase + cls.numFftStream, 1))
    
    ##
    # \brief Gets the allowed rate set for the FFTs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getFftStreamRateSet()
    @classmethod
    def getFftStreamRateSet(cls,):
        return cls.fftStreamType.getDdcRateSet() if cls.fftStreamType is not None else {}
    
    ##
    # \brief Gets the allowed rate list for the FFTs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getFftStreamRateList()
    @classmethod
    def getFftStreamRateList(cls,):
        return cls.fftStreamType.getDdcRateList() if cls.fftStreamType is not None else []
    
    ##
    # \brief Gets the allowed window set for the FFTs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getFftStreamWindowSet()
    @classmethod
    def getFftStreamWindowSet(cls,):
        return cls.fftStreamType.getWindowSet() if cls.fftStreamType is not None else {}
    
    ##
    # \brief Gets the allowed window list for the FFTs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getFftStreamWindowList()
    @classmethod
    def getFftStreamWindowList(cls,):
        return sorted(cls.fftStreamType.getWindowSet().keys()) if cls.fftStreamType is not None else []
    
    ##
    # \brief Gets the allowed size set for the FFTs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getFftStreamSizeSet()
    @classmethod
    def getFftStreamSizeSet(cls,):
        return cls.fftStreamType.getSizeSet() if cls.fftStreamType is not None else {}

    ##
    # \brief Gets the allowed size list for the FFTs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getFftStreamSizeList()
    @classmethod
    def getFftStreamSizeList(cls,):
        return sorted(cls.fftStreamType.getSizeSet().keys()) if cls.fftStreamType is not None else []
    
    ##
    # \brief Gets the ADC sample rate for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getAdcRate()
    @classmethod
    def getAdcRate(cls):
        return cls.adcRate

    ##
    # \brief Gets the VITA 49 header size for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getVitaHeaderSize()
    @classmethod
    def getVitaHeaderSize(cls, payloadType=None):
        return 4 * cls.ifSpecMap.get(payloadType, cls.ifSpec).headerSizeWords
    
    ##
    # \brief Gets the VITA 49 payload size for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getVitaPayloadSize()
    @classmethod
    def getVitaPayloadSize(cls, payloadType=None):
        return 4 * cls.ifSpecMap.get(payloadType, cls.ifSpec).payloadSizeWords
    
    ##
    # \brief Gets the VITA 49 tail size for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getVitaTailSize()
    @classmethod
    def getVitaTailSize(cls, payloadType=None):
        return 4 * cls.ifSpecMap.get(payloadType, cls.ifSpec).tailSizeWords    
    ##
    # \brief Gets dictionary with information about VITA 49 framing.
    #
    # \copydetails CyberRadioDriver::IRadio::getVitaFrameInfoDict()
    @classmethod
    def getVitaFrameInfoDict(cls, payloadType=None):
        return cls.ifSpecMap.get(payloadType, cls.ifSpec).getVitaFrameInfoDict()
    
    # \brief Gets whether data coming from the radio is byte-swapped with 
    # respect to the endianness of the host operating system.
    #
    # \copydetails CyberRadioDriver::IRadio::isByteswapped()
    @classmethod
    def isByteswapped(cls, payloadType=None):
        return (cls.ifSpecMap.get(payloadType, cls.ifSpec).byteOrder != sys.byteorder)
    
    ##
    # \brief Gets whether data coming from the radio has I and Q data swapped.
    #
    # \copydetails CyberRadioDriver::IRadio::isIqSwapped()
    @classmethod
    def isIqSwapped(cls, payloadType=None):
        return cls.ifSpecMap.get(payloadType, cls.ifSpec).iqSwapped
    
    ##
    # \brief Gets the byte order for data coming from the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getByteOrder()
    @classmethod
    def getByteOrder(cls, payloadType=None):
        return cls.ifSpecMap.get(payloadType, cls.ifSpec).byteOrder
    
    ##
    # \brief Gets the number of Gigabit Ethernet interfaces on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumGigE()
    @classmethod
    def getNumGigE(cls):
        return len(cls.getGigEIndexRange())
    
    ##
    # \brief Gets the index range for the Gigabit Ethernet interfaces on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getGigEIndexRange()
    @classmethod
    def getGigEIndexRange(cls):
        return [] if cls.numGigE == 0 else \
               list(range(cls.gigEIndexBase, cls.gigEIndexBase + cls.numGigE, 1))
    
    ##
    # \brief Gets the number of destination IP address table entries available for 
    # each Gigabit Ethernet interface on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumGigEDipEntries()
    @classmethod
    def getNumGigEDipEntries(cls):
        return len(cls.getGigEDipEntryIndexRange())
    
    ##
    # \brief Gets the index range for the destination IP address table entries 
    # available for the Gigabit Ethernet interfaces on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getGigEDipEntryIndexRange()
    @classmethod
    def getGigEDipEntryIndexRange(cls):
        return [] if cls.numGigE == 0 else \
               list(range(cls.gigEDipEntryIndexBase, \
                     cls.gigEDipEntryIndexBase + cls.numGigEDipEntries, 1))
    
    ##
    # \brief Gets the list of connection modes that the radio supports.
    #
    # \copydetails CyberRadioDriver::IRadio::getConnectionModeList()
    @classmethod
    def getConnectionModeList(cls):
        return [] if cls.connectionModes is None else cls.connectionModes
    
    ##
    # \brief Gets whether the radio supports a given connection mode.
    #
    # \copydetails CyberRadioDriver::IRadio::isConnectionModeSupported()
    @classmethod
    def isConnectionModeSupported(cls, mode):
        return mode in cls.getConnectionModeList()
    
    ##
    # \brief Gets the radio's default baud rate.
    #
    # \copydetails CyberRadioDriver::IRadio::getDefaultBaudrate()
    @classmethod
    def getDefaultBaudrate(cls):
        return cls.defaultBaudrate
    
    ##
    # \brief Gets the radio's default control port.
    #
    # \copydetails CyberRadioDriver::IRadio::getDefaultControlPort()
    @classmethod
    def getDefaultControlPort(cls):
        return cls.defaultPort
    
    ##
    # \brief Gets the allowed VITA enable options set for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getVitaEnableOptionSet()
    @classmethod
    def getVitaEnableOptionSet(cls):
        return {} if cls.vitaEnableOptions is None else cls.vitaEnableOptions
    
    ##
    # \brief Gets the number of transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumTransmitters() 
    @classmethod
    def getNumTransmitters(cls):
        return len(cls.getTransmitterIndexRange())
    
    ##
    # \brief Gets the index range for the transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterIndexRange() 
    @classmethod
    def getTransmitterIndexRange(cls):
        return [] if cls.numTxs == 0 else \
               list(range(cls.txIndexBase, \
                     cls.txIndexBase + cls.numTxs, 1))
    
    ##
    # \brief Gets the frequency range for the transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterFrequencyRange()
    @classmethod
    def getTransmitterFrequencyRange(cls):
        return (0.0,0.0) if cls.numTxs == 0 else cls.txType.frqRange
    
    ##
    # \brief Gets the frequency resolution for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterFrequencyRes()
    @classmethod
    def getTransmitterFrequencyRes(cls):
        return None if cls.numTxs == 0 else cls.txType.frqRes
    
    ##
    # \brief Gets the frequency unit for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterFrequencyUnit()
    @classmethod
    def getTransmitterFrequencyUnit(cls):
        return None if cls.numTxs == 0 else cls.txType.frqUnits
    
    ##
    # \brief Gets the attenuation range for the transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterAttenuationRange()
    @classmethod
    def getTransmitterAttenuationRange(cls):
        return (0.0,0.0) if cls.numTxs == 0 else cls.txType.attRange
    
    ##
    # \brief Gets the attenuation resolution for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterAttenuationRes()
    @classmethod
    def getTransmitterAttenuationRes(cls):
        return None if cls.numTxs == 0 else cls.txType.attRes
    
    ##
    # \brief Gets whether transmitters on the radio support continuous-wave
    # (CW) tone generation.
    #
    # \copydetails CyberRadioDriver::IRadio::transmitterSupportsCW()
    @classmethod
    def transmitterSupportsCW(cls):
        return (cls.numTxs > 0 and issubclass(cls.txType.toneGenType, 
                                              components._cwToneGen))

    ##
    # \brief Gets the number of CW tone generators for each transmitter.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWNum()
    @classmethod
    def getTransmitterCWNum(cls):
        return len(cls.getTransmitterCWIndexRange())

    ##
    # \brief Gets the CW tone generator index range for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWIndexRange()
    @classmethod
    def getTransmitterCWIndexRange(cls):
        return [] if not cls.transmitterSupportsCW() else \
               list(range(cls.txType.toneGenIndexBase, \
                     cls.txType.toneGenIndexBase + cls.txType.numToneGen, 1))
    
    ##
    # \brief Gets the CW tone generator frequency range for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWFrequencyRange()
    @classmethod
    def getTransmitterCWFrequencyRange(cls):
        return (0.0,0.0) if not cls.transmitterSupportsCW() else cls.txType.toneGenType.frqRange
    
    ##
    # \brief Gets the CW tone generator frequency resolution for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWFrequencyRes()
    @classmethod
    def getTransmitterCWFrequencyRes(cls):
        return None if not cls.transmitterSupportsCW() else cls.txType.toneGenType.frqRes

    ##
    # \brief Gets the CW tone generator amplitude range for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWAmplitudeRange()
    @classmethod
    def getTransmitterCWAmplitudeRange(cls):
        return (0.0,0.0) if not cls.transmitterSupportsCW() else cls.txType.toneGenType.ampRange
    
    ##
    # \brief Gets the CW tone generator amplitude resolution for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWAmplitudeRes()
    @classmethod
    def getTransmitterCWAmplitudeRes(cls):
        return None if not cls.transmitterSupportsCW() else cls.txType.toneGenType.ampRes

    ##
    # \brief Gets the CW tone generator phase range for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWPhaseRange()
    @classmethod
    def getTransmitterCWPhaseRange(cls):
        return (0.0,0.0) if not cls.transmitterSupportsCW() else cls.txType.toneGenType.phaseRange
    
    ##
    # \brief Gets the CW tone generator phase resolution for transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWPhaseRes()
    @classmethod
    def getTransmitterCWPhaseRes(cls):
        return None if not cls.transmitterSupportsCW() else cls.txType.toneGenType.phaseRes

    ##
    # \brief Gets whether transmitters on the radio support sweep functions
    # during continuous-wave (CW) tone generation.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWPhaseRes()
    @classmethod
    def transmitterSupportsCWSweep(cls):
        return cls.transmitterSupportsCW() and cls.txType.toneGenType.sweepCmd is not None

    ##
    # \brief Gets the CW tone generator sweep start frequency range for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepStartRange()
    @classmethod
    def getTransmitterCWSweepStartRange(cls):
        return (0.0,0.0) if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.startRange
    
    ##
    # \brief Gets the CW tone generator sweep start frequency resolution for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepStartRes()
    @classmethod
    def getTransmitterCWSweepStartRes(cls):
        return None if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.startRes
    
    ##
    # \brief Gets the CW tone generator sweep stop frequency range for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepStopRange()
    @classmethod
    def getTransmitterCWSweepStopRange(cls):
        return (0.0,0.0) if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.stopRange
    
    ##
    # \brief Gets the CW tone generator sweep stop frequency resolution for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepStopRes()
    @classmethod
    def getTransmitterCWSweepStopRes(cls):
        return None if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.stopRes
    
    ##
    # \brief Gets the CW tone generator sweep step frequency range for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepStepRange()
    @classmethod
    def getTransmitterCWSweepStepRange(cls):
        return (0.0,0.0) if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.stepRange
    
    ##
    # \brief Gets the CW tone generator sweep step frequency resolution for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepStepRes()
    @classmethod
    def getTransmitterCWSweepStepRes(cls):
        return None if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.stepRes
    
    ##
    # \brief Gets the CW tone generator sweep dwell time range for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepDwellRange()
    @classmethod
    def getTransmitterCWSweepDwellRange(cls):
        return (0.0,0.0) if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.dwellRange
    
    ##
    # \brief Gets the CW tone generator sweep dwell time resolution for 
    # transmitters on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTransmitterCWSweepDwellRes()
    @classmethod
    def getTransmitterCWSweepDwellRes(cls):
        return None if not cls.transmitterSupportsCWSweep() \
               else cls.txType.toneGenType.dwellRes

    ##
    # \brief Gets the number of wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumWbduc()
    @classmethod
    def getNumWbduc(cls):
        return len(cls.getWbducIndexRange())
    
    ##
    # \brief Gets the index range for the wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducIndexRange()
    @classmethod
    def getWbducIndexRange(cls):
        return list(range(cls.wbducIndexBase, cls.wbducIndexBase + cls.numWbduc, 1))
    
    ##
    # \brief Gets the frequency offset range for the wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducFrequencyRange()
    @classmethod
    def getWbducFrequencyRange(cls):
        return (0.0,0.0) if cls.wbducType is None else cls.wbducType.frqRange
    
    ##
    # \brief Gets the frequency resolution for wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducFrequencyRes()
    @classmethod
    def getWbducFrequencyRes(cls):
        return 0.0 if cls.wbducType is None else cls.wbducType.frqRes
    
    ##
    # \brief Gets the frequency unit for wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducFrequencyUnit()
    @classmethod
    def getWbducFrequencyUnit(cls):
        return 0.0 if cls.wbducType is None else cls.wbducType.frqUnits
    
    ##
    # \brief Gets the attenuation range for the wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducAttenuationRange()
    @classmethod
    def getWbducAttenuationRange(cls):
        return (0.0,0.0) if cls.wbducType is None else cls.wbducType.attRange
    
    ##
    # \brief Gets the attenuation resolution for wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducAttenuationRes()
    @classmethod
    def getWbducAttenuationRes(cls):
        return 0.0 if cls.wbducType is None else cls.wbducType.attRes
    
    ##
    # \brief Gets the allowed rate set for the wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducRateSet()
    @classmethod
    def getWbducRateSet(cls):
        ducObj = cls.wbducType
        return ducObj.rateSet if ducObj is not None else {}
    
    ##
    # \brief Gets the allowed rate list for the wideband DUCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducRateList()
    @classmethod
    def getWbducRateList(cls):
        ducObj = cls.wbducType
        if ducObj is not None:
            return [ducObj.rateSet[k] for k in sorted(ducObj.rateSet.keys())]
        else:
            return []

    ##
    # \brief Gets whether or not the wideband DUCs on the radio support loading
    # sample snapshots.
    #
    # \copydetails CyberRadioDriver::IRadio::wbducSupportsSnapshotLoad()
    @classmethod
    def wbducSupportsSnapshotLoad(cls):
        return (cls.wbducType is not None and cls.wbducType.snapshotLoadCmd is not None)

    ##
    # \brief Gets whether or not the wideband DUCs on the radio support 
    # transmitting sample snapshots.
    #
    # \copydetails CyberRadioDriver::IRadio::wbducSupportsSnapshotTransmit()
    @classmethod
    def wbducSupportsSnapshotTransmit(cls):
        return (cls.wbducType is not None and cls.wbducType.snapshotTxCmd is not None)

    ##
    # \brief Gets the index range for the DDC groups on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcGroupIndexRange()
    @classmethod
    def getDdcGroupIndexRange(cls, wideband):
        return cls.getWbddcGroupIndexRange() if wideband else cls.getNbddcGroupIndexRange()

    ##
    # \brief Gets the number of wideband DDC groups on the radio.
    # \copydetails CyberRadioDriver::IRadio::getNumWbddcGroups()
    @classmethod
    def getNumWbddcGroups(cls):
        return len(cls.getWbddcGroupIndexRange())
    
    ##
    # \brief Gets the index range for the wideband DDC groups on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbddcGroupIndexRange()
    @classmethod
    def getWbddcGroupIndexRange(cls):
        return list(range(cls.wbddcGroupIndexBase, cls.wbddcGroupIndexBase + cls.numWbddcGroups, 1))
    
    ##
    # \brief Gets the number of narrowband DDC groups on the radio.
    # \copydetails CyberRadioDriver::IRadio::getNumNbddcGroups()
    @classmethod
    def getNumNbddcGroups(cls):
        return len(cls.getNbddcGroupIndexRange())
    
    ##
    # \brief Gets the index range for the narrowband DDC groups on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcGroupIndexRange()
    @classmethod
    def getNbddcGroupIndexRange(cls):
        return list(range(cls.nbddcGroupIndexBase, cls.nbddcGroupIndexBase + cls.numNbddcGroups, 1))
    
    ##
    # \brief Gets the number of combined DDC groups on the radio.
    # \copydetails CyberRadioDriver::IRadio::getNumCombinedDdcGroups()
    @classmethod
    def getNumCombinedDdcGroups(cls):
        return len(cls.getCombinedDdcGroupIndexRange())
    
    ##
    # \brief Gets the index range for the combined DDC groups on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getCombinedDdcGroupIndexRange()
    @classmethod
    def getCombinedDdcGroupIndexRange(cls):
        return list(range(cls.cddcGroupIndexBase, cls.cddcGroupIndexBase + cls.numCddcGroups, 1))
    
    ##
    # \brief Gets the number of wideband DUC groups on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumWbducGroups()
    @classmethod
    def getNumWbducGroups(cls):
        return len(cls.getWbducGroupIndexRange())

    ##
    # \brief Gets the index range for the wideband DUC groups on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getWbducGroupIndexRange()
    @classmethod
    def getWbducGroupIndexRange(cls):
        return list(range(cls.wbducGroupIndexBase, cls.wbducGroupIndexBase + cls.numWbducGroups, 1))
    

    # ------------- Deprecated/Helper Methods ----------------- #

    ##
    # \internal
    # \brief Define this object's string representation.
    def __str__(self):
        return self.name
    
    ##
    # \internal
    # \brief Helper function that returns an index list.
    def _getIndexList(self,objIndex,objDict):
        if objIndex is None:
            return list(objDict.keys())
        elif type(objIndex) is int:
            return [objIndex,] if objIndex in list(objDict.keys()) else []
        elif type(objIndex) is list:
            return [i for i in objIndex if i in list(objDict.keys())]
        else:
            return []
    
    ##
    # \internal
    # \brief Helper function that "normalizes" an input configuration dictionary
    # section by doing the following:
    # <ul>
    # <li> Ensuring that keys for any enumerated entries are integers  
    # <li> Expanding sub-dictionaries with the special "all" key
    # <li> Performing specialization for individual entries
    #
    # \param configDict The incoming configuration dictionary.
    # \param entryIndexList The list of entry indices (used in expanding "all" keys).
    # \return The new configuration dictionary.
    def _normalizeConfigDictSection(self, configDict, entryIndexList):
        newConfigDict = {}
        # Fix keys in config dictionary
        convertKeys = []
        invalidKeys = []
        for key in configDict:
            try:
                tmp = int(key)
                if tmp != key:
                    convertKeys.append(key)
            except:
                if key != configKeys.ALL:
                    invalidKeys.append(key)
        for key in invalidKeys:
            configDict.pop(key)
        for key in convertKeys:
            configDict[int(key)] = configDict.pop(key)
        if configKeys.ALL in configDict:
            tmpDict = configDict.pop(configKeys.ALL)
            for entryNum in entryIndexList:
                newConfigDict[entryNum] = copy.deepcopy(tmpDict)
        for entryNum in configDict:
            if entryNum in newConfigDict:
                self._dictUpdate(newConfigDict[entryNum], \
                                 configDict[entryNum], \
                                 newConfigDict[entryNum], \
                                 list(configDict[entryNum].keys()))
            else:
                newConfigDict[entryNum] = copy.deepcopy(configDict[entryNum])
        return newConfigDict

    ##
    # \internal
    # \brief Helper function that "normalizes" an input configuration dictionary
    # by doing the following:
    # <ul>
    # <li> Ensuring that keys for component enumerations are integers  
    # <li> Expanding sub-dictionaries with the special "all" key
    # <li> Performing specialization for individual components or entries
    # \param configDict The incoming configuration dictionary.
    # \return The new configuration dictionary.
    def _normalizeConfigDict(self, configDict):
        newConfigDict = {}
        for configKey in configDict:
            if configKey == configKeys.CONFIG_TUNER:
                newConfigDict[configKeys.CONFIG_TUNER] = self._normalizeConfigDictSection( \
                                                            configDict[configKeys.CONFIG_TUNER], \
                                                            self.tunerIndexList)
            elif configKey == configKeys.CONFIG_DDC:
                newConfigDict[configKeys.CONFIG_DDC] = {}
                for ddcType in [configKeys.CONFIG_WBDDC, configKeys.CONFIG_NBDDC]:
                    isWideband = (ddcType == configKeys.CONFIG_WBDDC)
                    ddcConfDict = configDict[configKeys.CONFIG_DDC].get(ddcType,{})
                    ddcIndexRange = self.wbddcIndexList if isWideband else self.nbddcIndexList
                    newConfigDict[configKeys.CONFIG_DDC][ddcType] = self._normalizeConfigDictSection(\
                            ddcConfDict, ddcIndexRange)                    
            elif self.numGigE > 0 and configKey == configKeys.CONFIG_IP:
                tmpDict = copy.deepcopy(configDict[configKeys.CONFIG_IP])
                newConfigDict[configKeys.CONFIG_IP] = self._normalizeConfigDictSection( \
                            tmpDict, self.gigEIndexList)
                for gigEPortNum in self.gigEIndexList:
                    if gigEPortNum in newConfigDict[configKeys.CONFIG_IP] and \
                       configKeys.IP_DEST in newConfigDict[configKeys.CONFIG_IP][gigEPortNum]:
                        tmpDict = copy.deepcopy(newConfigDict[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST])
                        newConfigDict[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST] = \
                              self._normalizeConfigDictSection(tmpDict, \
                                                               self.gigEDipEntryIndexList)
            elif self.numTxs > 0 and configKey == configKeys.CONFIG_TX:
                tmpDict = copy.deepcopy(configDict[configKeys.CONFIG_TX])
                newConfigDict[configKeys.CONFIG_TX] = self._normalizeConfigDictSection( \
                                                            tmpDict, \
                                                            self.txIndexList)
                for txNum in self.getTransmitterIndexRange():
                    if txNum in newConfigDict[configKeys.CONFIG_TX]:
                        if configKeys.CONFIG_CW in newConfigDict[configKeys.CONFIG_TX][txNum]:
                            newConfigDict[configKeys.CONFIG_TX][txNum][configKeys.CONFIG_CW] = \
                                 self._normalizeConfigDictSection( newConfigDict[configKeys.CONFIG_TX][txNum][configKeys.CONFIG_CW], \
                                                                   self.txToneGenIndexList)
            elif configKey == configKeys.CONFIG_DUC:
                newConfigDict[configKeys.CONFIG_DUC] = {}
                for ducType in [configKeys.CONFIG_WBDUC, configKeys.CONFIG_NBDUC]:
                    isWideband = (ducType == configKeys.CONFIG_WBDUC)
                    ducConfDict = configDict[configKeys.CONFIG_DUC].get(ducType,{})
                    ducIndexRange = self.wbducIndexList if isWideband else self.nbducIndexList
                    newConfigDict[configKeys.CONFIG_DUC][ducType] = self._normalizeConfigDictSection(\
                            ducConfDict, ducIndexRange)                    
                    pass
            elif configKey == configKeys.CONFIG_DDC_GROUP:
                newConfigDict[configKeys.CONFIG_DDC_GROUP] = {}
                for ddcType in [configKeys.CONFIG_WBDDC_GROUP, configKeys.CONFIG_NBDDC_GROUP, 
                                configKeys.CONFIG_COMBINED_DDC_GROUP]:
                    isWideband = (ddcType == configKeys.CONFIG_WBDDC_GROUP)
                    ddcGroupConfDict = configDict[configKeys.CONFIG_DDC_GROUP].get(ddcType,{})
                    ddcGroupIndexRange = self.wbddcGroupIndexList if isWideband else self.nbddcGroupIndexList
                    if ddcType == configKeys.CONFIG_COMBINED_DDC_GROUP:
                        ddcGroupIndexRange = self.cddcGroupIndexList
                    newConfigDict[configKeys.CONFIG_DDC_GROUP][ddcType] = self._normalizeConfigDictSection(\
                            ddcGroupConfDict, ddcGroupIndexRange)                    
            elif configKey == configKeys.CONFIG_FFT:
                newConfigDict[configKeys.CONFIG_FFT] = self._normalizeConfigDictSection( \
                                                            configDict[configKeys.CONFIG_FFT], \
                                                            self.fftStreamIndexList)
            else:
                newConfigDict[configKey] = copy.deepcopy(configDict[configKey])
        return newConfigDict

    ##
    # \brief Gets the radio configuration.
    #
    # \deprecated Use getConfiguration() instead.
    #
    # \return The dictionary of radio settings.
    def getAll(self):
        return self.getConfiguration()
    
    ##
    # \internal
    # \brief Helper function for setting the tuner configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setTunerConfigurationNew(self, *args, **kwargs):
        success = True
        tunerIndex = kwargs.get(configKeys.TUNER_INDEX, None)
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            success &= self.tunerDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(self.tunerDict[i].getLastCommandErrorInfo())
        return success
        
    ##
    # \internal
    # \brief Helper function for getting the tuner configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getTunerConfigurationNew(self, tunerIndex=None):
        config = {}
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            config[i] = self.tunerDict[i].getConfiguration()
            self.cmdErrorInfo.extend(self.tunerDict[i].getLastCommandErrorInfo())
        return config
    
    ##
    # \internal
    # \brief Helper function for querying the tuner configuration.
    #
    # Deprecated in favor of queryConfiguration().
    def queryTunerConfigurationNew(self, tunerIndex=None):
        config = {}
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            config[i] = self.tunerDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(self.tunerDict[i].getLastCommandErrorInfo())
        return config
    
    ##
    # \internal
    # \brief Helper function for setting the DDC configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setDdcConfigurationNew(self, wideband=True, *args, **kwargs):
        success = True
        ddcDict = self.wbddcDict if wideband else self.nbddcDict
        ddcIndex = kwargs.get(configKeys.DDC_INDEX, None)
        for i in self._getIndexList(ddcIndex, ddcDict):
            success &= ddcDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(ddcDict[i].getLastCommandErrorInfo())
        return success

    ##
    # \internal
    # \brief Helper function for getting the DDC configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getDdcConfigurationNew(self, wideband=True, ddcIndex=None):
        config = {}
        ddcDict = self.wbddcDict if wideband else self.nbddcDict
        for i in self._getIndexList(ddcIndex, ddcDict):
            config[i] = ddcDict[i].getConfiguration()
            self.cmdErrorInfo.extend(ddcDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for querying the DDC configuration.
    #
    # Deprecated in favor of queryConfiguration().
    def queryDdcConfigurationNew(self, wideband=True, ddcIndex=None):
        config = {}
        ddcDict = self.wbddcDict if wideband else self.nbddcDict
        for i in self._getIndexList(ddcIndex, ddcDict):
            config[i] = ddcDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(ddcDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for setting the IP configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setIpConfigurationNew(self, confDict):
        success = True
        # IP configuration set -- The format of the configuration dictionary 
        # depends on whether the radio has Gigabit Ethernet ports on it or not.
        # -- No GigE ports
        if self.numGigE == 0:
            for cmdClass, configKey in [ \
                                    (self.sipCmd, configKeys.IP_SOURCE), \
                                    (self.dipCmd, configKeys.IP_DEST), \
                                    (self.smacCmd, configKeys.MAC_SOURCE), \
                                    (self.dmacCmd, configKeys.MAC_DEST), \
                                  ]:
                cDict = { "parent": self, \
                          "verbose": self.verbose, \
                          "logFile": self.logFile, \
                          configKey: confDict.get(configKey, 0)
                         }
                if configKey in confDict and cmdClass is not None and \
                   cmdClass.settable:
                    cmd = cmdClass(**cDict)
                    success &= cmd.send( self.sendCommand, )
                    if success and cmd.success:
                        self.configuration[configKeys.CONFIG_IP][configKey] = \
                                getattr(cmd, configKey)
                    else:
                        self.cmdErrorInfo.extend(cmd.errorInfo)
                    pass
            pass
        # -- Has GigE ports
        else:
            for gigEPortNum in self.gigEIndexList:
                if gigEPortNum in confDict:
                    # Set source IP address for this GigE port
                    if self.sipCmd is not None and self.sipCmd.settable and \
                       configKeys.IP_SOURCE in confDict[gigEPortNum]:
                        # What we do here depends on what "sourceIP" points to --
                        # either a string (NDR308-class) or a dictionary (NDR551-class)
                        if isinstance(confDict[gigEPortNum][configKeys.IP_SOURCE], str):
                            # Do it the NDR308 way
                            cDict = { "parent": self,
                                      "verbose": self.verbose,
                                      "logFile": self.logFile,
                                      configKeys.GIGE_PORT_INDEX: gigEPortNum,
                                      configKeys.IP_SOURCE: confDict[gigEPortNum][configKeys.IP_SOURCE],
                                     }
                            cmd = self.sipCmd(**cDict)
                            success &= cmd.send( self.sendCommand, )
                            if success and cmd.success:
                                self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_SOURCE] = \
                                        getattr(cmd, configKeys.IP_SOURCE)
                            else:
                                self.cmdErrorInfo.extend(cmd.errorInfo)
                        else:
                            # Do it the NDR551 way
                            cDict = { "parent": self,
                                      "verbose": self.verbose,
                                      "logFile": self.logFile,
                                      configKeys.GIGE_PORT_INDEX: gigEPortNum,
                                     }
                            if configKeys.GIGE_MAC_ADDR in confDict[gigEPortNum][configKeys.IP_SOURCE]:
                                cDict[configKeys.GIGE_MAC_ADDR] = confDict[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_MAC_ADDR]
                            if configKeys.GIGE_IP_ADDR in confDict[gigEPortNum][configKeys.IP_SOURCE]:
                                cDict[configKeys.GIGE_IP_ADDR] = confDict[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_IP_ADDR]
                            if configKeys.GIGE_NETMASK in confDict[gigEPortNum][configKeys.IP_SOURCE]:
                                cDict[configKeys.GIGE_NETMASK] = confDict[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_NETMASK]
                            if configKeys.GIGE_SOURCE_PORT in confDict[gigEPortNum][configKeys.IP_SOURCE]:
                                cDict[configKeys.GIGE_SOURCE_PORT] = confDict[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_SOURCE_PORT]
                            cmd = self.sipCmd(**cDict)
                            success &= cmd.send( self.sendCommand, )
                            if success and cmd.success:
                                #self.logIfVerbose("[setIpConfigurationNew()] cmd attributes = %s" % \
                                #        cmd.attributeDump())
                                if configKeys.GIGE_MAC_ADDR in cmd.__dict__:
                                    self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_MAC_ADDR] = \
                                        getattr(cmd, configKeys.GIGE_MAC_ADDR)
                                if configKeys.GIGE_IP_ADDR in cmd.__dict__:
                                    self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_IP_ADDR] = \
                                        getattr(cmd, configKeys.GIGE_IP_ADDR)
                                if configKeys.GIGE_NETMASK in cmd.__dict__:
                                    self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_NETMASK] = \
                                        getattr(cmd, configKeys.GIGE_NETMASK)
                                if configKeys.GIGE_SOURCE_PORT in cmd.__dict__:
                                    self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_SOURCE_PORT] = \
                                        getattr(cmd, configKeys.GIGE_SOURCE_PORT)
                            else:
                                if cmd.errorInfo is not None:
                                    self.cmdErrorInfo.extend(cmd.errorInfo)
                    # Set destination IP table info for this GigE port
                    if self.dipCmd is not None and self.dipCmd.settable and \
                       configKeys.IP_DEST in confDict[gigEPortNum]:
                        for gigEDipEntryNum in self.gigEDipEntryIndexList:
                            if gigEDipEntryNum in confDict[gigEPortNum][configKeys.IP_DEST]:
                                cDict = { "parent": self, \
                                          "verbose": self.verbose, \
                                          "logFile": self.logFile, \
                                          configKeys.GIGE_PORT_INDEX: gigEPortNum, \
                                          configKeys.GIGE_DIP_INDEX: gigEDipEntryNum, \
                                        }
                                keys = [configKeys.GIGE_IP_ADDR, configKeys.GIGE_MAC_ADDR, \
                                        configKeys.GIGE_SOURCE_PORT, configKeys.GIGE_DEST_PORT, \
                                        configKeys.GIGE_ARP]
                                self._dictUpdate(cDict, \
                                                 confDict[gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum], \
                                                 self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum], \
                                                 keys)
                                # Don't send along MAC address if there is an ARP setting
                                # and the ARP setting is True.  This prevents errors being
                                # triggered on radios with less permissive configurations
                                # (like the NDR551).
                                if configKeys.GIGE_ARP in cDict and cDict[configKeys.GIGE_ARP]:
                                    cDict.pop(configKeys.GIGE_MAC_ADDR, None)
                                cmd = self.dipCmd(**cDict)
                                success &= cmd.send( self.sendCommand, )
                                if success and cmd.success:
                                    for key in keys:
                                        if hasattr(cmd, key):
                                            self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum][key] = \
                                               getattr(cmd, key)
                                else:
                                    if cmd.errorInfo is not None:
                                        self.cmdErrorInfo.extend(cmd.errorInfo)
                                pass
                    # Set flow control for this GigE port
                    if self.tgfcCmd is not None and self.tgfcCmd.settable and \
                       configKeys.GIGE_FLOW_CONTROL in confDict[gigEPortNum]:
                        cDict = { "parent": self, \
                                  "verbose": self.verbose, \
                                  "logFile": self.logFile, \
                                  configKeys.GIGE_PORT_INDEX: gigEPortNum, \
                                  configKeys.GIGE_FLOW_CONTROL: confDict[gigEPortNum][configKeys.GIGE_FLOW_CONTROL], \
                                 }
                        cmd = self.tgfcCmd(**cDict)
                        success &= cmd.send( self.sendCommand, )
                        if success and cmd.success:
                            self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.GIGE_FLOW_CONTROL] = \
                                    getattr(cmd, configKeys.GIGE_FLOW_CONTROL)
                        else:
                            if cmd.errorInfo is not None:
                                self.cmdErrorInfo.extend(cmd.errorInfo)
            pass
        return success

    ##
    # \internal
    # \brief Helper function for querying the IP configuration.
    # \param gigEPortIndex 10-Gig data port index, or None to query all data ports.
    def queryIpConfigurationNew(self, gigEPortIndex=None):
        # IP configuration query -- The format of this section depends on whether
        # the radio has Gigabit Ethernet ports on it or not.
        ret = {}
        # -- No GigE ports
        if self.numGigE == 0:
            ret = self._queryIpConfigurationNo10Gig()
        # -- Has GigE ports
        else:
            ret = self._queryIpConfiguration10Gig(gigEPortIndex=gigEPortIndex)
        return ret

    ##
    # \internal
    # \brief Helper function for querying the IP configuration for radios without
    #     10-Gig Ethernet interfaces.
    def _queryIpConfigurationNo10Gig(self):
        ret = {}
        for cmdClass, configKey in [ \
                                (self.sipCmd, configKeys.IP_SOURCE), \
                                (self.dipCmd, configKeys.IP_DEST), \
                                (self.smacCmd, configKeys.MAC_SOURCE), \
                                (self.dmacCmd, configKeys.MAC_DEST), \
                              ]:
            ret[configKey] = None
            if cmdClass is not None and cmdClass.queryable:
                cmd = cmdClass(parent=self, 
                               query=True,
                                verbose=self.verbose, logFile=self.logFile)
                cmd.send( self.sendCommand, )
                self._addLastCommandErrorInfo(cmd)
                rspInfo = cmd.getResponseInfo()
                if rspInfo is not None:
                    ret[configKey] = rspInfo.get(configKey, "")
        return ret
    
    ##
    # \internal
    # \brief Helper function for querying the IP configuration for radios with
    #     10-Gig Ethernet interfaces.
    # \param gigEPortIndex 10-Gig data port index, or None to query all data ports.
    def _queryIpConfiguration10Gig(self, gigEPortIndex=None):
        ret = {}
        gigEPortIndexRange = self.getGigEIndexRange() if gigEPortIndex is None else [gigEPortIndex]
        for gigEPortNum in gigEPortIndexRange:
            ret[gigEPortNum] = {}
            # Query source IP address for this GigE port   
            if self.sipCmd is not None and self.sipCmd.queryable:
                # Default source IP info
                if self.json:
                    ret[gigEPortNum][configKeys.IP_SOURCE] = {
                            configKeys.GIGE_MAC_ADDR: None,
                            configKeys.GIGE_IP_ADDR: None,
                            configKeys.GIGE_NETMASK: None,
                            configKeys.GIGE_SOURCE_PORT: None,
                         }
                else:
                    ret[gigEPortNum][configKeys.IP_SOURCE] = None
                cDict = { "parent": self, \
                          "query": True, \
                          "verbose": self.verbose, \
                          "logFile": self.logFile, \
                          configKeys.GIGE_PORT_INDEX: gigEPortNum, \
                         }
                cmd = self.sipCmd(**cDict)
                cmd.send( self.sendCommand, )
                self._addLastCommandErrorInfo(cmd)
                rspInfo = cmd.getResponseInfo()
                if rspInfo is not None:
                    # How to parse this depends on whether the radio is JSON or not
                    if self.json:
                        # Do it NDR551-style
                        ret[gigEPortNum][configKeys.IP_SOURCE] = {}
                        ret[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_MAC_ADDR] = \
                             rspInfo.get(configKeys.GIGE_MAC_ADDR, "")
                        ret[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_IP_ADDR] = \
                             rspInfo.get(configKeys.GIGE_IP_ADDR, "")
                        ret[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_NETMASK] = \
                             rspInfo.get(configKeys.GIGE_NETMASK, "")
                        ret[gigEPortNum][configKeys.IP_SOURCE][configKeys.GIGE_SOURCE_PORT] = \
                             rspInfo.get(configKeys.GIGE_SOURCE_PORT, 0)
                    else:
                        # Do it NDR308-style
                        ret[gigEPortNum][configKeys.IP_SOURCE] = \
                               rspInfo.get(configKeys.IP_SOURCE, "")
            # Query destination IP table for this GigE port
            if self.dipCmd is not None and self.dipCmd.queryable:
                ret[gigEPortNum][configKeys.IP_DEST] = {}
                for gigEDipEntryNum in self.gigEDipEntryIndexList:
                    ret[gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum] = {}
                    cmd = self.dipCmd(**{})
                    for configKey in [configKeys.GIGE_IP_ADDR, \
                                      configKeys.GIGE_MAC_ADDR, \
                                      configKeys.GIGE_SOURCE_PORT, \
                                      configKeys.GIGE_DEST_PORT, \
                                      configKeys.GIGE_ARP]:
                        if hasattr(cmd, "queryParamMap") and configKey in cmd.queryParamMap:
                            ret[gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum][configKey] = None
                        elif hasattr(cmd, "queryResponseData") and configKey in [q[0] for q in cmd.queryResponseData]:
                            ret[gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum][configKey] = None
                    cDict = { "parent": self, \
                              "query": True, \
                              "verbose": self.verbose, \
                              "logFile": self.logFile, \
                              configKeys.GIGE_PORT_INDEX: gigEPortNum, \
                              configKeys.GIGE_DIP_INDEX: gigEDipEntryNum, \
                             }
                    cmd = self.dipCmd(**cDict)
                    cmd.send( self.sendCommand, )
                    rspInfo = cmd.getResponseInfo()
                    self._addLastCommandErrorInfo(cmd)
                    if rspInfo is not None:
                        for configKey in [configKeys.GIGE_IP_ADDR, \
                                          configKeys.GIGE_MAC_ADDR, \
                                          configKeys.GIGE_SOURCE_PORT, \
                                          configKeys.GIGE_DEST_PORT, \
                                          configKeys.GIGE_ARP]:
                            if configKey in rspInfo:
                                ret[gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum][configKey] = \
                                   rspInfo[configKey]
        return ret
    
    ##
    # \internal
    # \brief Helper function for setting the transmitter configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setTxConfigurationNew(self, *args, **kwargs):
        success = True
        txIndex = kwargs.get(configKeys.TX_INDEX, None)
        for i in self._getIndexList(txIndex, self.txDict):
            success &= self.txDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(self.txDict[i].getLastCommandErrorInfo())
        return success
        
    ##
    # \internal
    # \brief Helper function for getting the transmitter configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getTxConfigurationNew(self, txIndex=None):
        config = {}
        for i in self._getIndexList(txIndex, self.txDict):
            config[i] = self.txDict[i].getConfiguration()
            self.cmdErrorInfo.extend(self.txDict[i].getLastCommandErrorInfo())
        return config
    
    ##
    # \internal
    # \brief Helper function for querying the transmitter configuration.
    #
    # Deprecated in favor of getConfiguration().
    def queryTxConfigurationNew(self, txIndex=None):
        config = {}
        for i in self._getIndexList(txIndex, self.txDict):
            config[i] = self.txDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(self.txDict[i].getLastCommandErrorInfo())
        return config
    
    ##
    # \internal
    # \brief Helper function for setting the DUC configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setDucConfigurationNew(self, wideband=True, *args, **kwargs):
        success = True
        ducDict = self.wbducDict if wideband else self.nbducDict
        ducIndex = kwargs.get(configKeys.DUC_INDEX, None)
        for i in self._getIndexList(ducIndex, ducDict):
            success &= ducDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(ducDict[i].getLastCommandErrorInfo())
        return success

    ##
    # \internal
    # \brief Helper function for getting the DUC configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getDucConfigurationNew(self, wideband=True, ducIndex=None):
        config = {}
        ducDict = self.wbducDict if wideband else self.nbducDict
        for i in self._getIndexList(ducIndex, ducDict):
            config[i] = ducDict[i].getConfiguration()
            self.cmdErrorInfo.extend(ducDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for querying the DUC configuration.
    #
    # Deprecated in favor of getConfiguration().
    def queryDucConfigurationNew(self, wideband=True, ducIndex=None):
        config = {}
        ducDict = self.wbducDict if wideband else self.nbducDict
        for i in self._getIndexList(ducIndex, ducDict):
            config[i] = ducDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(ducDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for getting the DDC group configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getDdcGroupConfigurationNew(self, wideband=True, ddcGroupIndex=None):
        config = {}
        ddcGroupDict = self.wbddcGroupDict if wideband else self.nbddcGroupDict
        for i in self._getIndexList(ddcGroupIndex, ddcGroupDict):
            config[i] = ddcGroupDict[i].getConfiguration()
            self.cmdErrorInfo.extend(ddcGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for querying the DDC group configuration.
    #
    # Deprecated in favor of queryConfiguration().
    def queryDdcGroupConfigurationNew(self, wideband=True, ddcGroupIndex=None):
        config = {}
        ddcGroupDict = self.wbddcGroupDict if wideband else self.nbddcGroupDict
        for i in self._getIndexList(ddcGroupIndex, ddcGroupDict):
            config[i] = ddcGroupDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(ddcGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for setting the DDC group configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setDdcGroupConfigurationNew(self, wideband=True, *args, **kwargs):
        success = True
        ddcGroupDict = self.wbddcGroupDict if wideband else self.nbddcGroupDict
        ddcGroupIndex = kwargs.get(configKeys.INDEX, None)
        for i in self._getIndexList(ddcGroupIndex, ddcGroupDict):
            success &= ddcGroupDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(ddcGroupDict[i].getLastCommandErrorInfo())
        return success

    ##
    # \internal
    # \brief Helper function for getting the combined DDC group configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getCombinedDdcGroupConfigurationNew(self, ddcGroupIndex=None):
        config = {}
        ddcGroupDict = self.cddcGroupDict
        for i in self._getIndexList(ddcGroupIndex, ddcGroupDict):
            config[i] = ddcGroupDict[i].getConfiguration()
            self.cmdErrorInfo.extend(ddcGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for querying the combined DDC group configuration.
    #
    # Deprecated in favor of queryConfiguration().
    def queryCombinedDdcGroupConfigurationNew(self, ddcGroupIndex=None):
        config = {}
        ddcGroupDict = self.cddcGroupDict
        for i in self._getIndexList(ddcGroupIndex, ddcGroupDict):
            config[i] = ddcGroupDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(ddcGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for setting the combined DDC group configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setCombinedDdcGroupConfigurationNew(self, *args, **kwargs):
        success = True
        #self.logIfVerbose("[ndr551][setCombinedDdcGroupConfigurationNew()] begin")
        ddcGroupDict = self.cddcGroupDict
        ddcGroupIndex = kwargs.get(configKeys.INDEX, None)
        for i in self._getIndexList(ddcGroupIndex, ddcGroupDict):
            success &= ddcGroupDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(ddcGroupDict[i].getLastCommandErrorInfo())
        #self.logIfVerbose("[ndr551][setCombinedDdcGroupConfigurationNew()] end")
        return success

    ##
    # \internal
    # \brief Helper function for getting the DUC group configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getDucGroupConfigurationNew(self, wideband=True, ducGroupIndex=None):
        config = {}
        ducGroupDict = self.wbducGroupDict if wideband else self.nbducGroupDict
        for i in self._getIndexList(ducGroupIndex, ducGroupDict):
            config[i] = ducGroupDict[i].getConfiguration()
            self.cmdErrorInfo.extend(ducGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for querying the DUC group configuration.
    #
    # Deprecated in favor of queryConfiguration().
    def queryDucGroupConfigurationNew(self, wideband=True, ducGroupIndex=None):
        config = {}
        ducGroupDict = self.wbducGroupDict if wideband else self.nbducGroupDict
        for i in self._getIndexList(ducGroupIndex, ducGroupDict):
            config[i] = ducGroupDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(ducGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for setting the DUC group configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setDucGroupConfigurationNew(self, wideband=True, *args, **kwargs):
        success = True
        ducGroupDict = self.wbducGroupDict if wideband else self.nbducGroupDict
        ducGroupIndex = kwargs.get(configKeys.INDEX, None)
        for i in self._getIndexList(ducGroupIndex, ducGroupDict):
            success &= ducGroupDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(ducGroupDict[i].getLastCommandErrorInfo())
        return success

    ##
    # \internal
    # \brief Helper function for getting the tuner group configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getTunerGroupConfigurationNew(self, tunerGroupIndex=None):
        config = {}
        for i in self._getIndexList(tunerGroupIndex, self.tunerGroupDict):
            config[i] = self.tunerGroupDict[i].getConfiguration()
            self.cmdErrorInfo.extend(self.tunerGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for querying the tuner group configuration.
    #
    # Deprecated in favor of queryConfiguration().
    def queryTunerGroupConfigurationNew(self, tunerGroupIndex=None):
        config = {}
        for i in self._getIndexList(tunerGroupIndex, self.tunerGroupDict):
            config[i] = self.tunerGroupDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(self.tunerGroupDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for setting the tuner group configuration.
    #
    # Deprecated in favor of setConfiguration().
    def setTunerGroupConfigurationNew(self, *args, **kwargs):
        success = True
        tunerGroupIndex = kwargs.get(configKeys.INDEX, None)
        for i in self._getIndexList(tunerGroupIndex, self.tunerGroupDict):
            success &= self.tunerGroupDict[i].setConfiguration(*args, **kwargs)
            self.cmdErrorInfo.extend(self.tunerGroupDict[i].getLastCommandErrorInfo())
        return success

    ##
    # \internal
    # \brief Helper function for setting the FFT stream configuration.
    #
    # Deprecated in favor of setConfiguration().
    #
    def setFftStreamConfiguration(self, *args, **kwargs):
        success = True
        index = kwargs.get(configKeys.FFT_INDEX, None)
        for i in self._getIndexList(index, self.fftStreamDict):
            success &= self.fftStreamDict[i].setConfiguration(**kwargs)
            self.cmdErrorInfo.extend(self.fftStreamDict[i].getLastCommandErrorInfo())
        return success

    ##
    # \internal
    # \brief Helper function for getting the FFT stream configuration.
    #
    # Deprecated in favor of getConfiguration().
    def getFftStreamConfiguration(self, fftStreamIndex=None):
        config = {}
        for i in self._getIndexList(fftStreamIndex, self.fftStreamDict):
            config[i] = self.fftStreamDict[i].getConfiguration()
            self.cmdErrorInfo.extend(self.fftStreamDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for querying the FFT stream configuration.
    #
    # Deprecated in favor of queryConfiguration().
    def queryFftStreamConfiguration(self, fftStreamIndex=None):
        config = {}
        for i in self._getIndexList(fftStreamIndex, self.fftStreamDict):
            config[i] = self.fftStreamDict[i].queryConfiguration()
            self.cmdErrorInfo.extend(self.fftStreamDict[i].getLastCommandErrorInfo())
        return config

    ##
    # \internal
    # \brief Helper function for configuring the IP addresses.
    def configureIp(self,iface,udpBase=41000,maxUdp=None):
        success = True
        self.logIfVerbose( "configureIP CALLED" )
        if type(iface) is list and len(iface)>1:
            self.logIfVerbose( "configuring dual interfaces %s"%repr(iface) )
            maxUdp = 32
            udpList = []
            if type(udpBase) in (int,float):
                udpBase = [udpBase,udpBase]
            elif type(udpBase) is list:
                if len(udpBase)==1:
                    udpBase.append(udpBase[0])
            for index,interface in enumerate(iface):
                udpList.append( list(range(udpBase[index]+index*100,udpBase[index]+maxUdp+index*100)) )
                mac,dip = getInterfaceAddresses(iface[index])
                x = [ int(i) for i in dip.split(".") ]
                x[-1]+=10
                sip = ".".join( [str(i) for i in x] )
                sipCmd = command.radio_command( parent=self, cmdString="SIP %d,%s"%(index+1,sip),
                          verbose=self.verbose, logFile=self.logFile )
                success &= sipCmd.send( self.sendCommand )
                for i in range(maxUdp):
                    args = ", ".join( [str(i) for i in (index+1,i,dip,mac,udpList[index][i],udpList[index][i])] )
                    dipCmd = command.radio_command( parent=self, cmdString="DIP %s"%args,
                          verbose=self.verbose, logFile=self.logFile )
                    success &= dipCmd.send( self.sendCommand )
        else:
            self.logIfVerbose("configuring single interface %s"%repr(iface))
            if type(iface) is list:
                iface = iface[0]
            if maxUdp is None:
                maxUdp = self.numWbddc+self.numNbddc
            self.udpList = [list(range(udpBase,udpBase+maxUdp)),]
            mac,dip = getInterfaceAddresses(iface)
            x = [ int(i) for i in dip.split(".") ]
            x[-1]+=10
            sip = ".".join( [str(i) for i in x] )
            for cmd in ( command.radio_command(parent=self, cmdString="SIP %s"%sip,
                          verbose=self.verbose, logFile=self.logFile), \
                        command.radio_command(parent=self, cmdString="DIP %s"%dip,
                          verbose=self.verbose, logFile=self.logFile), \
                        command.radio_command(parent=self, cmdString="TDMAC %s"%mac,
                          verbose=self.verbose, logFile=self.logFile), \
                         ):
                success &= cmd.send( self.sendCommand )
        return success
    
    ##
    # \brief Gets the number of DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNumDdc()
    @classmethod
    def getNumDdc(cls, wideband):
        return len(cls.getDdcIndexRange(wideband))
    
    ##
    # \brief Gets the allowed rate set for the DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getDdcRateSet()
    @classmethod
    def getDdcRateSet(cls, wideband, index=None):
        ddcObj = cls.wbddcType if wideband else cls.nbddcType
        return ddcObj.getDdcRateSet(index) if ddcObj is not None else {}
    
    ##
    # \brief Gets the allowed rate list for the DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getDdcRateList()
    @classmethod
    def getDdcRateList(cls, wideband, index=None):
        ddcObj = cls.wbddcType if wideband else cls.nbddcType
        return ddcObj.getDdcRateList(index) if ddcObj is not None else []
    
    ##
    # \brief Gets the allowed bandwidth set for the DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getDdcBwSet()
    @classmethod
    def getDdcBwSet(cls, wideband, index=None):
        ddcObj = cls.wbddcType if wideband else cls.nbddcType
        return ddcObj.getDdcBwSet(index) if ddcObj is not None else {}
    
    ##
    # \brief Gets the allowed bandwidth list for the DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getDdcBwList()
    @classmethod
    def getDdcBwList(cls, wideband, index=None):
        ddcObj = cls.wbddcType if wideband else cls.nbddcType
        return ddcObj.getDdcBwList(index) if ddcObj is not None else []
    
    ##
    # \brief Gets the set of available DDC data formats.
    #
    # \copydetails CyberRadioDriver::IRadio::getDdcDataFormat()
    @classmethod
    def getDdcDataFormat(cls, wideband):
        ddcObj = cls.wbddcType if wideband else cls.nbddcType
        return ddcObj.getDdcDataFormat() if ddcObj is not None else {}
    
    ##
    # \brief Gets the frequency offset range for the narrowband DDCs on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getNbddcFrequencyRange()
    @classmethod
    def getDdcFrequencyRange(cls, wideband, index=None):
        ddcType = cls.wbddcType if wideband else cls.nbddcType
        return (0.0,0.0) if ddcType is None else ddcType.frqRange
    
    ##
    # \brief Gets the list of DDC indexes for a specified type.
    #
    # \copydetails CyberRadioDriver::IRadio::getDdcIndexRange()
    @classmethod
    def getDdcIndexRange(cls, wideband):
        return cls.getWbddcIndexRange() if wideband else cls.getNbddcIndexRange()

    ##
    # \internal
    # \brief Convenience method for configuring the Ethernet addresses on a radio that does not
    # have Gigabit Ethernet ports.
    #
    # \param sip The source IP address.  If this is None, the source IP address will not
    #    be changed.
    # \param dip The destination IP address.  If this is None, the destination IP address 
    #    will not be changed.
    # \param dmac The destination MAC address.  If this is None, the destination MAC address 
    #    will not be changed.
    # \return True if the configuration succeeded, False otherwise.
    def setIpConfiguration(self, sip=None, dip=None, dmac=None):
        configDict = {
                    configKeys.CONFIG_IP: {
                } 
            }
        if sip is not None:
            configDict[configKeys.CONFIG_IP][configKeys.IP_SOURCE] = copy.deepcopy(sip)
        if dip is not None:
            configDict[configKeys.CONFIG_IP][configKeys.IP_DEST] = copy.deepcopy(dip)
        if dmac is not None:
            configDict[configKeys.CONFIG_IP][configKeys.MAC_DEST] = copy.deepcopy(dmac)
        return self._setConfiguration(configDict)
    
    ##
    # \internal
    def setDip(self,udp,dip="255.255.255.255",dmac="ff:ff:ff:ff:ff:ff",ifIndex=None,subIndex=None):
        pass
    
    ##
    # \internal
    # \brief Sets tuner configuration (old-style).
    #
    # \deprecated Use setConfiguration() instead.
    #
    # \param frequency Tuner frequency.
    # \param attenuation Tuner attenuation.
    # \param tunerIndex Either None (configure all tuners), an index number (configure
    #     a specific tuner), or a list of index numbers (configure a set of tuners).
    # \return True if successful, False otherwise.
    def setTunerConfiguration(self,frequency,attenuation,tunerIndex=None):
        success = True
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            # success &= self.tunerDict[i].setConfiguration(frequency,attenuation)
            success &= self.tunerDict[i].setConfiguration( **{ 
                                                        configKeys.TUNER_FREQUENCY: frequency,
                                                        configKeys.TUNER_ATTENUATION: attenuation,
                                                        } )
        return success
    
    ##
    # \internal
    # \brief Gets tuner configuration (old-style).
    #
    # \deprecated Use getConfiguration() instead.
    #
    # \param tunerIndex Either None (get for all tuners), an index number (get for
    #     a specific tuner), or a list of index numbers (get for a set of tuners).
    # \return A dictionary with configuration information.
    def getTunerConfiguration(self,tunerIndex=None):
        config = {}
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            config[i] = self.tunerDict[i].getConfiguration()
        return config
        
    ##
    # \internal
    # \brief Sets tuner frequency (old-style).
    #
    # \deprecated Use setConfiguration() instead.
    #
    # \param frequency Tuner frequency.
    # \param tunerIndex Either None (configure all tuners), an index number (configure
    #     a specific tuner), or a list of index numbers (configure a set of tuners).
    # \return True if successful, False otherwise.
    def setTunerFrequency(self,frequency,tunerIndex=None):
        success = True
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            # success &= self.tunerDict[i].setFrequency(frequency)
            success &= self.tunerDict[i].setConfiguration( **{ 
                                                        configKeys.TUNER_FREQUENCY: frequency,
                                                        } )
        return success
        
    ##
    # \internal
    # \brief Gets tuner frequency information (old-style).
    #
    # \deprecated Use getConfiguration() instead.
    #
    # \param tunerIndex Either None (get for all tuners), an index number (get for
    #     a specific tuner), or a list of index numbers (get for a set of tuners).
    # \return A dictionary with frequency information.
    def getTunerFrequency(self,tunerIndex=None,):
        frqDict = {}
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            #frqDict[i] = self.tunerDict[i].getFrequency()
            frqDict[i] = self.tunerDict[i].configuration.get(configKeys.TUNER_FREQUENCY, None)
        return frqDict
    
    ##
    # \internal
    # \brief Sets tuner attenuation (old-style).
    #
    # \deprecated Use setConfiguration() instead.
    #
    # \param attenuation Tuner attenuation.
    # \param tunerIndex Either None (configure all tuners), an index number (configure
    #     a specific tuner), or a list of index numbers (configure a set of tuners).
    # \return True if successful, False otherwise.
    def setTunerAttenuation(self,attenuation,tunerIndex=None):
        success = True
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            # success &= self.tunerDict[i].setAttenuation(attenuation)
            success &= self.tunerDict[i].setConfiguration( **{ 
                                                        configKeys.TUNER_ATTENUATION: attenuation,
                                                        } )
        return success
        
    ##
    # \internal
    # \brief Gets tuner attenuation information (old-style).
    #
    # \deprecated Use getConfiguration() instead.
    #
    # \param tunerIndex Either None (get for all tuners), an index number (get for
    #     a specific tuner), or a list of index numbers (get for a set of tuners).
    # \return A dictionary with attenuation information.
    def getTunerAttenuation(self,tunerIndex=None,):
        att = {}
        for i in self._getIndexList(tunerIndex, self.tunerDict):
            # att[i] = self.tunerDict[i].getAttenuation()
            att[i] = self.tunerDict[i].configuration.get(configKeys.TUNER_ATTENUATION, None)
        return att
        
    ##
    # \internal
    # \brief Sets DDC configuration (old-style).
    #
    # \deprecated Use setConfiguration() instead.
    #
    # \param wideband Whether the DDC is a wideband DDC.
    # \param ddcIndex Either None (configure all DDCs), an index number (configure
    #     a specific DDC), or a list of index numbers (configure a set of DDCs).
    # \param rfIndex DDC RF index number.
    # \param rateIndex DDC rate index number.
    # \param udpDest UDP destination.
    # \param frequency Frequency offset.
    # \param enable 1 if DDC is enabled, 0 if not.
    # \param vitaEnable VITA 49 streaming option, as appropriate for the radio.
    # \param streamId VITA 49 stream ID.
    # \return True if successful, False otherwise.
    def setDdcConfiguration(self,wideband,ddcIndex=None,rfIndex=1,rateIndex=0,udpDest=0,frequency=0,enable=0,vitaEnable=0,streamId=0):
        success = True
        ddcDict = self.wbddcDict if wideband else self.nbddcDict
        for i in self._getIndexList(ddcIndex,ddcDict):
            # ddcDict[i].setConfiguration(rfIndex=rfIndex,rateIndex=rateIndex,udpDest=udpDest,frequency=frequency,enable=enable,vitaEnable=vitaEnable,streamId=streamId)
            success &= ddcDict[i].setConfiguration( **{ 
                                                        configKeys.NBDDC_RF_INDEX: rfIndex,
                                                        configKeys.DDC_RATE_INDEX: rateIndex,
                                                        configKeys.DDC_UDP_DESTINATION: udpDest,
                                                        configKeys.DDC_FREQUENCY_OFFSET: frequency,
                                                        configKeys.ENABLE: enable,
                                                        configKeys.DDC_VITA_ENABLE: vitaEnable,
                                                        configKeys.DDC_STREAM_ID: streamId,
                                                        } )
        return success
    
    ##
    # \brief Disables ethernet flow control on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::disableTenGigFlowControl()
    def disableTenGigFlowControl(self,):
        return self.setTenGigFlowControlStatus(False)
    
    ##
    # \brief Enables ethernet flow control on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::enableTenGigFlowControl()
    def enableTenGigFlowControl(self,):
        return self.setTenGigFlowControlStatus(True)
    
    ##
    # \brief method to enable or disable ethernet flow control on the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getTenGigFlowControlStatus()
    def setTenGigFlowControlStatus(self,enable=False):
        return False
    
    ##
    # \brief Queries status of flow control handling.
    #
    # \copydetails CyberRadioDriver::IRadio::getTenGigFlowControlStatus()
    def getTenGigFlowControlStatus(self,):
        return {}

    ##
    # \brief Performs coherent tuning.
    #
    # \copydetails CyberRadioDriver::IRadio::coherentTune()
    def coherentTune(self, cohGroup, freq):
        ret = True
        if self.cohTuneCmd is not None:
            cDict = { "parent": self, \
                      "verbose": self.verbose, \
                      "logFile": self.logFile, \
                      configKeys.TUNER_COHERENT_GROUP: cohGroup,
                      configKeys.TUNER_FREQUENCY: freq,
                     }
            cmd = self.cohTuneCmd(**cDict)
            ret &= cmd.send( self.sendCommand, )
            self.logIfVerbose("coherentTune send result =", ret)
            ret &= cmd.success
            self.logIfVerbose("coherentTune success result =", ret)
            self._addLastCommandErrorInfo(cmd)
            if ret:
                self.logIfVerbose("force tuner requery")
                self.queryTunerConfigurationNew(tunerIndex=None)
            pass
        else:
            ret = False
        return ret
    ##
    # \brief Gets the current FPGA state.
    #
    # \copydetails CyberRadioDriver::IRadio::getFpgaState()
    def getFpgaState(self):
        ret = None
        if self.fpgaStateCmd is not None:
            ret = self.getConfigurationByKeys("fpgaState")
        return ret
    
    ##
    # \brief Sets the current FPGA state.
    #
    # \copydetails CyberRadioDriver::IRadio::setFpgaState()
    def setFpgaState(self, state):
        ret = False
        if self.fpgaStateCmd is not None:
            ret = self.setConfiguration({"fpgaState": state})
        return ret
    
    # OVERRIDE
    ##
    # \brief Sets whether or not the object is in verbose mode.
    #
    # \copydetails CyberRadioDriver::IRadio::setVerbose()
    def setVerbose(self, verbose):
        # Set this object's verbose mode
        log._logger.setVerbose(self, verbose)
        # Set verbose mode on all components
        for obj in self.componentList:
            obj.setVerbose(verbose)
        
    ##
    # \brief Sets the log file.
    #
    # \copydetails CyberRadioDriver::IRadio::setLogFile()
    def setLogFile(self, logFile):
        # Set this object's log file
        log._logger.setLogFile(self, logFile)
        # Set log file on all components
        for obj in self.componentList:
            obj.setLogFile(logFile)

    ##
    # \brief Gets the list of connected data port interface indices.
    #
    # \copydetails CyberRadioDriver::IRadio::getConnectedDataPorts()
    def getConnectedDataPorts(self):
        ret = []
        if self.isCrddConnection:
            ret = self._crddGetConnectedDataPortIndices()
        return ret
    
    ##
    # \internal
    # \brief Converts a user-specified time string into a number of seconds 
    #      since 1/1/70.  
    #
    # The time string can be either:
    # \li Absolute time, in any supported format
    # \li Relative time specified as now{-n}, where n is a number of seconds
    # \li Relative time specified as now{-[[H:]MM:]SS}
    # \li "begin", which is the beginning of known time (1/1/70)
    # \li "end", which is the end of trackable time and far beyond the
    #    useful life of this utility (01/18/2038)
    #
    # \throws RuntimeException if the time string format cannot be understood.
    # \param timestr The time string.
    # \param utc Whether or not the user's time string is in UTC time.
    # \return The time, in number of seconds since the Epoch
    @staticmethod
    def timeFromString(timestr, utc=True):
        ret = 0
        tm = None
        tstr = timestr.strip()
        if tstr == "":
            ret = 0
        elif tstr == "begin":
            ret = 0
        elif tstr == "end":
            ret = sys.maxsize
        else:
            if tstr.find('now') != -1:
                tm = datetime.datetime.utcnow() if utc else datetime.datetime.now()
                i = tstr.find('-')
                if i != -1:
                    tmp = tstr[i+1:]
                    tm = tm - datetime.timedelta(seconds=_radio.timeSecsFromString(tmp))
            else:
                # Replace strings "today" and "yesterday"
                tmToday = datetime.datetime.utcnow() if utc else datetime.datetime.now()
                tmYesterday = tmToday - datetime.timedelta(days=1)
                dateStrToday = tmToday.strftime("%Y%m%d")
                dateStrYesterday = tmYesterday.strftime("%Y%m%d")
                tstr = tstr.replace("today", dateStrToday).replace("yesterday", dateStrYesterday)
                # Try a series of known formats
                # -- Formats are 5-tuples: (format string, width, needs year, needs month, needs day)
                supportedFmts = [ \
                                 ('%Y-%m-%dT%H:%M:%S%z', 24, False, False, False), \
                                 ('%Y-%m-%dT%H:%M:%S', 19, False, False, False), \
                                 ('%Y%m%d:%H%M%S', 15, False, False, False), \
                                 ('%a %b %d %H:%M:%S %Y', 24, False, False, False), \
                                 ('%b %d %H:%M:%S', 15, True, False, False), \
                                 ('%b %d, %Y %I:%M:%S %p', 24, False, False, False), \
                                 ('%Y-%m-%d %H:%M:%S', 19, False, False, False), \
                                 ('%Y/%m/%d %H:%M:%S', 19, False, False, False), \
                                 ('%Y%m%d_%H%M%S', 15, False, False, False), \
                                 ('%m/%d/%Y %H:%M', 16, False, False, False), \
                                 ('%m/%d/%y %H:%M:%S', 17, False, False, False), \
                                 ('%Y%m%d', 8, False, False, False), \
                                 ('%Y-%m-%d', 10, False, False, False), \
                                 ('%H:%M:%S', 8, True, True, True), \
                                 ('%H%M%S', 6, True, True, True), \
                                 ]
                for fmt in supportedFmts:
                    try:
                        tmp = tstr[:fmt[1]].strip()
                        #print "[DBG][timeFromString] Convert"
                        #print "[DBG][timeFromString] -- string:", tmp
                        #print "[DBG][timeFromString] -- format:", fmt[0]
                        tm = datetime.datetime.strptime(tmp, fmt[0])
                        #print "[DBG][timeFromString] -- SUCCESS"
                        # Replace date items from today's date as needed by the format
                        # -- Day
                        if fmt[4]:
                            tm = tm.replace(day=tmToday.day)
                        # -- Month
                        if fmt[3]:
                            tm = tm.replace(month=tmToday.month)
                        # -- Year
                        if fmt[2]:
                            tm = tm.replace(year=tmToday.year)
                            # But if the resulting date is in the future, then we need to dial it
                            # back a year
                            if tm > tmToday:
                                tm = tm.replace(year=tmToday.year-1)
                        break
                    except:
                        #print "[DBG][timeFromString] -- FAILURE"
                        tm = None
            if tm is not None:
                ret = time.mktime(tm.timetuple())
            else:
                raise RuntimeError("Improperly formatted time: \"" + tstr + "\"")
        return ret
        
    ##
    # Converts a time string ([+-][[H:]M:]S) to a time in seconds.  
    #
    # \note Hours and minutes are not bounded in any way.  These strings provide the 
    #    same result:
    # \li "7200"
    # \li "120:00"
    # \li "2:00:00"
    #
    # \throws RuntimeError if the time is formatted improperly.
    # \param timeStr The time string.
    # \return The number of seconds.
    @staticmethod
    def timeSecsFromString(timeStr):
        hrs = 0
        mins = 0
        secs = 0
        sgn = 1
        try:
            if "-" in timeStr:
                sgn = -1
            tmp = timeStr.strip().translate(None, " +-")
            if tmp != "":
                vec = tmp.split(":")
                if vec[-1] != "":
                    secs = int(vec[-1])
                else:
                    raise RuntimeError("Improperly formatted time: \"" + timeStr + "\"")
                if len(vec) > 1:
                    if vec[-2] != "":
                        mins = int(vec[-2])
                    else:
                        raise RuntimeError("Improperly formatted time: \"" + timeStr + "\"")
                if len(vec) > 2:
                    if vec[-3] != "":
                        hrs = int(vec[-3])
                    else:
                        raise RuntimeError("Improperly formatted time: \"" + timeStr + "\"")
        except:
            raise RuntimeError("Improperly formatted time: \"" + timeStr + "\"")
        return ( sgn * (hrs * 3600 + mins * 60 + secs) )
            

##
# \internal
# \brief Radio handler class that supports nothing more complicated than 
#     identifying a connected radio.
#
# Used internally to support radio auto-detection.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
class _radio_identifier(_radio):
    _name = "Radio Identifier"
    json = False
    ifSpec = _ifSpec
    adcRate = 1.0
    numTuner = 0
    numTunerBoards = 0
    tunerType = None
    numWbddc = 0
    wbddcType = None
    numNbddc = 0
    nbddcType = None
    numTxs = 0
    txType = None
    numWbduc = 0
    wbducType = None
    numNbduc = 0
    nbducType = None
    numWbddcGroups = 0
    wbddcGroupType = None
    numNbddcGroups = 0
    nbddcGroupType = None
    numTunerGroups = 0
    tunerGroupType = None
    numGigE = 0
    numGigEDipEntries = 0
    idnQry = command.idn
    verQry = command.ver
    hrevQry = command.hrev
    statQry = None
    tstatQry = None
    tadjCmd = None
    resetCmd = None
    cfgCmd = None
    ppsCmd = None
    utcCmd = None
    refCmd = None
    rbypCmd = None
    sipCmd = None
    dipCmd = None
    smacCmd = None
    dmacCmd = None
    calfCmd = None
    nbssCmd = None
    fnrCmd = None
    gpsCmd = None
    gposCmd = None
    rtvCmd = None
    tempCmd = None
    gpioStaticCmd = None
    gpioSeqCmd = None
    tgfcCmd = None
    refModes = {}
    rbypModes = {}
    vitaEnableOptions = {}
    connectionModes = ["https", "tcp", "udp", "tty"]
    validConfigurationKeywords = []
    setTimeDefault = False

    # OVERRIDE
    ##
    # \protected
    # \brief Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # This radio has nothing further that it can configure


##
# \brief Radio function (mode) command used by JSON-based radios.
#
class funJSON(command._jsonCommandBase):
    mnemonic = "fun"
    queryParamMap = {
            configKeys.RADIO_FUNCTION: "state",
        }
    setParamMap = {
            configKeys.RADIO_FUNCTION: "state",
        }


##
# \internal
# \brief Radio handler class that supports nothing more complicated than 
#     identifying a connected radio.
#
# Used internally to support radio auto-detection.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
class _radio_identifier_json(_radio):
    _name = "Radio Identifier"
    json = True
    ifSpec = _ifSpec
    adcRate = 1.0
    numTuner = 0
    numTunerBoards = 0
    tunerType = None
    numWbddc = 0
    wbddcType = None
    numNbddc = 0
    nbddcType = None
    numTxs = 0
    txType = None
    numWbduc = 0
    wbducType = None
    numNbduc = 0
    nbducType = None
    numWbddcGroups = 0
    wbddcGroupType = None
    numNbddcGroups = 0
    nbddcGroupType = None
    numTunerGroups = 0
    tunerGroupType = None
    numGigE = 0
    numGigEDipEntries = 0
    idnQry = None
    verQry = None
    hrevQry = None
    statQry = command.status_json
    tstatQry = None
    tadjCmd = None
    resetCmd = None
    cfgCmd = None
    ppsCmd = None
    utcCmd = None
    refCmd = None
    rbypCmd = None
    sipCmd = None
    dipCmd = None
    smacCmd = None
    dmacCmd = None
    calfCmd = None
    nbssCmd = None
    fnrCmd = None
    gpsCmd = None
    gposCmd = None
    rtvCmd = None
    tempCmd = None
    gpioStaticCmd = None
    gpioSeqCmd = None
    tgfcCmd = None
    funCmd = funJSON
    refModes = {}
    rbypModes = {}
    vitaEnableOptions = {}
    connectionModes = ["https", "tcp", "udp", "tty"]
    validConfigurationKeywords = [
            configKeys.RADIO_FUNCTION
        ]
    setTimeDefault = False

    # OVERRIDE
    ##
    # \brief Returns version information for the radio.
    #
    # \copydetails CyberRadioDriver::IRadio::getVersionInfo()
    def getVersionInfo(self):
        # Query hardware for details if we don't have them already
        keys = [configKeys.VERINFO_MODEL, configKeys.VERINFO_SN, 
                configKeys.VERINFO_SW, configKeys.VERINFO_FW, 
                configKeys.VERINFO_REF, configKeys.VERINFO_UNITREV, 
                configKeys.VERINFO_HW]
        if not all([key in self.versionInfo for key in keys]):
            cmd = self.statQry(parent=self, 
                               query=True,
                               verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                self._dictUpdate(self.versionInfo, rspInfo, {}, keys)
        for key in keys:
            if key not in self.versionInfo:
                self.versionInfo[key] = "N/A"
        return self.versionInfo

    # OVERRIDE
    ##
    # \protected
    # \brief Queries hardware to determine the object's current configuration.  
    def _queryConfiguration(self):
        # Call the base-class implementation
        configKeys.Configurable._queryConfiguration(self)
        # Call the radio function command
        if self.funCmd is not None:
            cmd = self.funCmd(parent=self, 
                              query=True,
                              verbose=self.verbose, logFile=self.logFile)
            cmd.send( self.sendCommand, )
            self._addLastCommandErrorInfo(cmd)
            rspInfo = cmd.getResponseInfo()
            if rspInfo is not None:
                for key in self.validConfigurationKeywords:
                    val = rspInfo.get(key, None)
                    if val is not None:
                        self.configuration[key] = val
        # This radio has nothing further that it can configure


#-- End Radio Handler Objects --------------------------------------------------#
#-- NOTE: Radio handler objects for supporting specific radios need to be
#   implemented under the CyberRadioDriver.radios package tree. 
