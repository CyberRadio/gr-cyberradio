#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.radio
# 
# \brief Provides classes that define supported radios.
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014 CyberRadio Solutions, Inc.  All rights 
# reserved.
#
###############################################################

# python library imports
import traceback
import time
import math
import inspect
import sys
import copy
#	internal imports
import components
import transport
import command
import log
import configKeys


##
# \internal
# \brief Returns the MAC address and IP address for a given Ethernet interface.
#
# \param ifname The name of the Ethernet system interface ("eth0", for example).
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
	

##
# \internal
# \brief VITA 49 interface specification class for the NDR304.
class ndr304_ifSpec(_ifSpec):
	headerSizeWords = 7
	tailSizeWords = 1
	payloadSizeWords = 384
	byteOrder = "little"
	iqSwapped = True

##
# \internal
# \brief VITA 49 interface specification class for the NDR308.
class ndr308_ifSpec(_ifSpec):
	headerSizeWords = 9
	payloadSizeWords = 1024
	tailSizeWords = 1
	byteOrder = "little"


#-- Radio Handler Objects ---------------------------------------------#

##
# \brief Base radio handler class.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# To add a supported radio to this driver, derive a class from 
# _radio and change the static members of the new class to describe the
# capabilities of that particular radio.
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
	## \brief Analog-to-digital Converter clock rate
	adcRate = 1.0
	# Tuner settings
	## \brief Number of tuners
	numTuner = 0
	## \brief Number of tuner boards
	numTunerBoards = 1
	## \brief Tuner index base (what number indices start at) 
	tunerIndexBase = 1
	## \brief Tuner component type 
	tunerType = components._tuner
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
	# Mode settings
	## \brief Supported reference modes 
	refModes = {}
	## \brief Supported reference bypass modes 
	rbypModes = {}
	## \brief Supported VITA 49 enabling options 
	vitaEnableOptions = {}
	## \brief Supported connection modes
	connectionModes = ["tty"]
	##
	# \brief The list of valid configuration keywords supported by this
	# object.  Override in derived classes as needed.
	validConfigurationKeywords = [configKeys.CONFIG_MODE, \
								  configKeys.REFERENCE_MODE, \
								  configKeys.BYPASS_MODE, \
								  configKeys.CALIB_FREQUENCY, \
								  configKeys.FNR_MODE, \
								  configKeys.GPS_ENABLE, \
								  configKeys.REF_TUNING_VOLT, \
								  configKeys.GIGE_FLOW_CONTROL, \
								 ]
	## \brief Default "set time" value
	setTimeDefault = False

	##
	# \brief Constructs a radio handler object.
	#
	# \copydetails CyberRadioDriver::IRadio::__init__()
	def __init__(self, *args, **kwargs):
		# Set up configuration capability
		configKeys.Configurable.__init__(self)
		# Consume keyword arguments "verbose" and "logFile" for logging support
		log._logger.__init__(self, *args, **kwargs)
		# Now consume our own
		self.setTime = kwargs.get("setTime",self.setTimeDefault)
		self.logCtrl = kwargs.get("logCtrl",None)
		self.name = "%s%s"%(self._name,"-%s"%kwargs.get("name") if kwargs.has_key("name") else "",)
		self.logIfVerbose("Verbose mode!")
		self.tunerDict = {}
		self.wbddcDict = {}
		self.nbddcDict = {}
		self.txDict = {}
		self.wbducDict = {}
		self.nbducDict = {}
		self.wbddcGroupDict = {}
		self.nbddcGroupDict = {}
		self.componentList = []
		# Little hack to ensure numWbddc is always set (we didn't always have this attribute).
		if self.numWbddc is None:
			self.numWbddc = self.numTuner
		for objRange,objType,objDict in ( \
										(xrange(self.tunerIndexBase, self.tunerIndexBase + self.numTuner),self.tunerType,self.tunerDict), \
										(xrange(self.wbddcIndexBase, self.wbddcIndexBase + self.numWbddc),self.wbddcType,self.wbddcDict), \
										(xrange(self.nbddcIndexBase, self.nbddcIndexBase + self.numNbddc),self.nbddcType,self.nbddcDict), \
										(xrange(self.txIndexBase, self.txIndexBase + self.numTxs),self.txType,self.txDict), \
										(xrange(self.wbducIndexBase, self.wbddcIndexBase + self.numWbduc),self.wbducType,self.wbducDict), \
										(xrange(self.nbducIndexBase, self.nbddcIndexBase + self.numNbduc),self.nbducType,self.nbducDict), \
										(xrange(self.wbddcGroupIndexBase, self.wbddcGroupIndexBase + self.numWbddcGroups),self.wbddcGroupType,self.wbddcGroupDict), \
										(xrange(self.nbddcGroupIndexBase, self.nbddcGroupIndexBase + self.numNbddcGroups),self.nbddcGroupType,self.nbddcGroupDict), \
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
		# Set the time on the radio 
		self.setTime = False
		# Communication transport in use 
		self.transport = None
		self.connectError = ""
	
	##
	# \brief Destroys a radio handler object.
	#
	# \copydetails CyberRadioDriver::IRadio::__del__()
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
		# Query hardware for details if we don't have them already
		if not all([self.versionInfo.has_key(key) for key in \
				      [configKeys.VERINFO_MODEL, configKeys.VERINFO_SN]]):
			cmd = self.idnQry(parent=self, 
							  query=True,
							  verbose=self.verbose, logFile=self.logFile)
			cmd.send( self.sendCommand, )
			self._addLastCommandErrorInfo(cmd)
			rspInfo = cmd.getResponseInfo()
			if rspInfo is not None:
				self.versionInfo.update(rspInfo)
		if not all([self.versionInfo.has_key(key) for key in [configKeys.VERINFO_SW, 
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
		if not all([self.versionInfo.has_key(key) for key in [configKeys.VERINFO_MODEL, 
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
					if self.versionInfo.has_key(key) and rspInfo.has_key(key):
						del rspInfo[key]
				self.versionInfo.update(rspInfo)
		for key in [configKeys.VERINFO_MODEL, configKeys.VERINFO_SN, 
				    configKeys.VERINFO_SW, configKeys.VERINFO_FW, 
				    configKeys.VERINFO_REF, configKeys.VERINFO_UNITREV, 
				    configKeys.VERINFO_HW]:
			if not self.versionInfo.has_key(key):
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
		if self.mode in ("tcp","udp"):
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
				self.port_or_baudrate = transport.radio_transport.defaultBaudrate \
				                           if mode == "tty" else \
				                           transport.radio_transport.defaultPort
			if self.transport is not None:
				self.transport.disconnect()
				self.transport = None
			self.transport = transport.radio_transport(parent=self,verbose=self.verbose,
													   logFile=self.logFile, 
													   logCtrl=self.logCtrl,
													   json=self.json)
			if self.transport.connect(mode, host_or_dev, port_or_baudrate):
				self._queryConfiguration()
				for obj in self.componentList:
					obj.addTransport(self.transport,self.sendCommand,)
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
			self.log(traceback.format_exc())
			#traceback.print_exc()
		for obj in self.componentList:
			obj.delTransport()
	
	##
	# \brief Sends a command to the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::sendCommand()
	def sendCommand(self,cmdString,timeout=None):
		try:
			x = self.transport.sendCommandAndReceive(cmdString,timeout)
			if not self.transport.connected:
				self.transport.disconnect()
				return None
			else:
				return x
		except:
			self.log(traceback.format_exc())
			#traceback.print_exc()
			self.transport.disconnect()
			return None
	
	##
	# \brief Sets the radio configuration.
	#
	# \copydetails CyberRadioDriver::IRadio::setConfiguration()
	def setConfiguration(self, configDict={}):
		self.cmdErrorInfo = []
		# Normalize the incoming configuration dictionary before trying to process it.
		configDict2 = self._normalizeConfigDict(configDict)
		success = configKeys.Configurable.setConfiguration(self, **configDict2)
		tunerConfDict = configDict2.get(configKeys.CONFIG_TUNER,{})
		for index in xrange(self.tunerIndexBase, self.tunerIndexBase + self.numTuner):
			if tunerConfDict.has_key(index):
				confDict = tunerConfDict[index]
				confDict[configKeys.TUNER_INDEX] = index
				success &= self.setTunerConfigurationNew(**confDict)
		for ddcType in [configKeys.CONFIG_WBDDC, configKeys.CONFIG_NBDDC]:
			isWideband = (ddcType == configKeys.CONFIG_WBDDC)
			ddcConfDict = configDict2.get(configKeys.CONFIG_DDC,{}).get(ddcType,{})
			ddcIndexRange = xrange(self.wbddcIndexBase, self.wbddcIndexBase + self.numWbddc) if isWideband \
			                else xrange(self.nbddcIndexBase, self.nbddcIndexBase + self.numNbddc)
			for index in ddcIndexRange:
				if ddcConfDict.has_key(index):
					confDict = ddcConfDict[index]
					confDict[configKeys.DDC_INDEX] = index
					success &= self.setDdcConfigurationNew(wideband=isWideband, **confDict)
		success &= self.setIpConfigurationNew(configDict2.get(configKeys.CONFIG_IP, {}))
		txConfDict = configDict2.get(configKeys.CONFIG_TX,{})
		for index in self.getTransmitterIndexRange():
			if txConfDict.has_key(index):
				confDict = txConfDict[index]
				confDict[configKeys.TX_INDEX] = index
				success &= self.setTxConfigurationNew(**confDict)
		for ducType in [configKeys.CONFIG_WBDUC, configKeys.CONFIG_NBDUC]:
			isWideband = (ducType == configKeys.CONFIG_WBDUC)
			ducConfDict = configDict2.get(configKeys.CONFIG_DUC,{}).get(ducType,{})
			ducIndexRange = xrange(self.wbducIndexBase, self.wbducIndexBase + self.numWbduc) if isWideband \
			                else xrange(self.nbducIndexBase, self.nbducIndexBase + self.numNbduc)
			for index in ducIndexRange:
				if ducConfDict.has_key(index):
					confDict = ducConfDict[index]
					confDict[configKeys.DUC_INDEX] = index
					success &= self.setDucConfigurationNew(wideband=isWideband, **confDict)
		for ddcType in [configKeys.CONFIG_WBDDC_GROUP, configKeys.CONFIG_NBDDC_GROUP]:
			# Flag for forcing the driver to query DDCs for status information
			forceDdcQuery = False
			isWideband = (ddcType == configKeys.CONFIG_WBDDC_GROUP)
			ddcGroupConfDict = configDict2.get(configKeys.CONFIG_DDC_GROUP,{}).get(ddcType,{})
			ddcGroupIndexRange = xrange(self.wbddcGroupIndexBase, self.wbddcGroupIndexBase + self.numWbddcGroups) if isWideband \
			                else xrange(self.nbddcGroupIndexBase, self.nbddcGroupIndexBase + self.numNbddcGroups)
			for index in ddcGroupIndexRange:
				if ddcGroupConfDict.has_key(index):
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
		return success
	
	##
	# \brief Gets the radio configuration.
	#
	# \copydetails CyberRadioDriver::IRadio::getConfiguration()
	def getConfiguration(self):
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
		return ret 
	
	##
	# \protected
	# \brief Queries hardware to determine the object's current configuration.  
	def _queryConfiguration(self):
		for cmdClass, configKey in [ \
								(self.cfgCmd, configKeys.CONFIG_MODE), \
							    (self.refCmd, configKeys.REFERENCE_MODE), \
							    (self.rbypCmd, configKeys.BYPASS_MODE), \
							    (self.calfCmd, configKeys.CALIB_FREQUENCY), \
							    (self.fnrCmd, configKeys.FNR_MODE), \
							    (self.gpsCmd, configKeys.GPS_ENABLE), \
							    (self.rtvCmd, configKeys.REF_TUNING_VOLT), \
							  ]:
			if cmdClass is not None:
				cmd = cmdClass(parent=self, 
							   query=True,
		 					   verbose=self.verbose, logFile=self.logFile)
				cmd.send( self.sendCommand, )
				self._addLastCommandErrorInfo(cmd)
				rspInfo = cmd.getResponseInfo()
				if rspInfo is not None:
					self.configuration[configKey] = rspInfo.get(configKey, 0)
		# IP configuration query -- The format of this section depends on whether
		# the radio has Gigabit Ethernet ports on it or not.
		self.configuration[configKeys.CONFIG_IP] = {}
		# -- No GigE ports
		if self.numGigE == 0:
			for cmdClass, configKey in [ \
									(self.sipCmd, configKeys.IP_SOURCE), \
								    (self.dipCmd, configKeys.IP_DEST), \
								    (self.smacCmd, configKeys.MAC_SOURCE), \
								    (self.dmacCmd, configKeys.MAC_DEST), \
								  ]:
				if cmdClass is not None and cmdClass.queryable:
					cmd = cmdClass(parent=self, 
								   query=True,
			 					   verbose=self.verbose, logFile=self.logFile)
					cmd.send( self.sendCommand, )
					self._addLastCommandErrorInfo(cmd)
					rspInfo = cmd.getResponseInfo()
					if rspInfo is not None:
						self.configuration[configKeys.CONFIG_IP][configKey] = \
						       rspInfo.get(configKey, "")
		# -- Has GigE ports
		else:
			for gigEPortNum in xrange(self.gigEIndexBase, 
									  self.gigEIndexBase + self.numGigE, 1):
				self.configuration[configKeys.CONFIG_IP][gigEPortNum] = {}
				# Query source IP address for this GigE port
				if self.sipCmd is not None and self.sipCmd.queryable:
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
						self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_SOURCE] = \
						       rspInfo.get(configKeys.IP_SOURCE, "")
				# Query destination IP table for this GigE port
				if self.dipCmd is not None and self.dipCmd.queryable:
					self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST] = {}
					for gigEDipEntryNum in xrange(self.gigEDipEntryIndexBase, 
										          self.gigEDipEntryIndexBase + self.numGigEDipEntries, 
										          1):
						self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum] = {}
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
								if rspInfo.has_key(configKey):
									self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST][gigEDipEntryNum][configKey] = \
								       rspInfo[configKey]

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
	def setTimeNextPps(self,checkTime=False,useGpsTime=False):
		if self.ppsCmd is not None and self.utcCmd is not None:
			if self.getPps():
				if useGpsTime:
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
			modeInt = int(mode) if int(mode) in self.refModes.keys() else None
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
			modeInt = int(mode) if int(mode) in self.rbypModes.keys() else None
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
# 				cmd = self.tadjCmd(parent=self,index=i, timingAdjustment=timeAdjustValue,
# 						          verbose=self.verbose, logFile=self.logFile)
# 				success &= cmd.send( self.sendCommand )
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
		return cls.numTuner
	
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
		return range(cls.tunerIndexBase, cls.tunerIndexBase + cls.numTuner, 1)
	
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
	# \brief Gets the number of wideband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNumWbddc()
	@classmethod
	def getNumWbddc(cls):
		return cls.numWbddc
	
	##
	# \brief Gets whether the wideband or narrobwand DDCs on the radio have 
	# selectable sources.
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
		return range(cls.wbddcIndexBase, cls.wbddcIndexBase + cls.numWbddc, 1)
	
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
	# \brief Gets the allowed rate set for the narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getWbddcBwSet()
	@classmethod
	def getWbddcBwSet(cls,index=None):
		return cls.getDdcBwSet(True, index)
	
	##
	# \brief Gets the allowed rate list for the narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getWbddcBwList()
	@classmethod
	def getWbddcBwList(cls,index=None):
		return cls.getDdcBwList(True, index)
		

	##
	# \brief Gets the number of narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNumNbddc()
	@classmethod
	def getNumNbddc(cls):
		return cls.numNbddc
	
	##
	# \brief Gets the index range for the narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNbddcIndexRange()
	@classmethod
	def getNbddcIndexRange(cls):
		return [] if cls.numNbddc == 0 else \
			   range(cls.nbddcIndexBase, cls.nbddcIndexBase + cls.numNbddc, 1)
	
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
	def getNbddcRateSet(cls,index=None):
		return cls.getDdcRateSet(False, index)
	
	##
	# \brief Gets the allowed rate list for the narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNbddcRateList()
	@classmethod
	def getNbddcRateList(cls,index=None):
		return cls.getDdcRateList(False, index)
		
	##
	# \brief Gets the allowed rate set for the narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNbddcBwSet()
	@classmethod
	def getNbddcBwSet(cls,index=None):
		return cls.getDdcBwSet(False, index)
	
	##
	# \brief Gets the allowed rate list for the narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNbddcBwList()
	@classmethod
	def getNbddcBwList(cls,index=None):
		return cls.getDdcBwList(False, index)
		

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
	def getVitaHeaderSize(cls):
		return 4 * cls.ifSpec.headerSizeWords
	
	##
	# \brief Gets the VITA 49 payload size for the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getVitaPayloadSize()
	@classmethod
	def getVitaPayloadSize(cls):
		return 4 * cls.ifSpec.payloadSizeWords
	
	##
	# \brief Gets the VITA 49 tail size for the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getVitaTailSize()
	@classmethod
	def getVitaTailSize(cls):
		return 4 * cls.ifSpec.tailSizeWords
	
	##
	# \brief Gets whether data coming from the radio is byte-swapped with 
	# respect to the endianness of the host operating system.
	#
	# \copydetails CyberRadioDriver::IRadio::isByteswapped()
	@classmethod
	def isByteswapped(cls):
		return (cls.ifSpec.byteOrder != sys.byteorder)
	
	##
	# \brief Gets whether data coming from the radio has I and Q data swapped.
	#
	# \copydetails CyberRadioDriver::IRadio::isIqSwapped()
	@classmethod
	def isIqSwapped(cls):
		return cls.ifSpec.iqSwapped
	
	##
	# \brief Gets the byte order for data coming from the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getByteOrder()
	@classmethod
	def getByteOrder(cls):
		return cls.ifSpec.byteOrder
	
	##
	# \brief Gets the number of Gigabit Ethernet interfaces on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNumGigE()
	@classmethod
	def getNumGigE(cls):
		return cls.numGigE
	
	##
	# \brief Gets the index range for the Gigabit Ethernet interfaces on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getGigEIndexRange()
	@classmethod
	def getGigEIndexRange(cls):
		return [] if cls.numGigE == 0 else \
			   range(cls.gigEIndexBase, cls.gigEIndexBase + cls.numGigE, 1)
	
	##
	# \brief Gets the number of destination IP address table entries available for 
	# each Gigabit Ethernet interface on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNumGigEDipEntries()
	@classmethod
	def getNumGigEDipEntries(cls):
		return cls.numGigEDipEntries
	
	##
	# \brief Gets the index range for the destination IP address table entries 
	# available for the Gigabit Ethernet interfaces on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getGigEDipEntryIndexRange()
	@classmethod
	def getGigEDipEntryIndexRange(cls):
		return [] if cls.numGigE == 0 else \
			   range(cls.gigEDipEntryIndexBase, \
					 cls.gigEDipEntryIndexBase + cls.numGigEDipEntries, 1)
	
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
		return cls.numTxs
	
	##
	# \brief Gets the index range for the transmitters on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getTransmitterIndexRange() 
	@classmethod
	def getTransmitterIndexRange(cls):
		return [] if cls.numTxs == 0 else \
			   range(cls.txIndexBase, \
					 cls.txIndexBase + cls.numTxs, 1)
	
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
		return 0 if not cls.transmitterSupportsCW() else cls.txType.numToneGen

	##
	# \brief Gets the CW tone generator index range for transmitters on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getTransmitterCWIndexRange()
	@classmethod
	def getTransmitterCWIndexRange(cls):
		return [] if not cls.transmitterSupportsCW() else \
			   range(cls.txType.toneGenIndexBase, \
					 cls.txType.toneGenIndexBase + cls.txType.numToneGen, 1)
	
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
		return cls.numWbduc
	
	##
	# \brief Gets the index range for the wideband DUCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getWbducIndexRange()
	@classmethod
	def getWbducIndexRange(cls):
		return range(cls.wbducIndexBase, cls.wbducIndexBase + cls.numWbduc, 1)
	
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
	# \brief Gets the index range for the wideband DDC groups on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getWbddcGroupIndexRange()
	@classmethod
	def getWbddcGroupIndexRange(cls):
		return range(cls.wbddcGroupIndexBase, cls.wbddcGroupIndexBase + cls.numWbddcGroups, 1)
	
	##
	# \brief Gets the index range for the narrowband DDC groups on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNbddcGroupIndexRange()
	@classmethod
	def getNbddcGroupIndexRange(cls):
		return range(cls.nbddcGroupIndexBase, cls.nbddcGroupIndexBase + cls.numNbddcGroups, 1)
	

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
			return objDict.keys()
		elif type(objIndex) is int:
			return [objIndex,] if objIndex in objDict.keys() else []
		elif type(objIndex) is list:
			return [i for i in objIndex if i in objDict.keys()]
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
	# \param entryMin The minimum entry index (used in expanding "all" keys)
	# \param entryMax The maximum entry index (used in expanding "all" keys)
	# \return The new configuration dictionary.
	def _normalizeConfigDictSection(self, configDict, entryMin, entryMax):
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
			for entryNum in xrange(entryMin, entryMax+1, 1):
				newConfigDict[entryNum] = copy.deepcopy(tmpDict)
		for entryNum in configDict:
			if newConfigDict.has_key(entryNum):
				self._dictUpdate(newConfigDict[entryNum], \
								 configDict[entryNum], \
								 newConfigDict[entryNum], \
								 configDict[entryNum].keys())
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
															self.tunerIndexBase, \
															self.tunerIndexBase + self.numTuner - 1)
			elif configKey == configKeys.CONFIG_DDC:
				newConfigDict[configKeys.CONFIG_DDC] = {}
				for ddcType in [configKeys.CONFIG_WBDDC, configKeys.CONFIG_NBDDC]:
					isWideband = (ddcType == configKeys.CONFIG_WBDDC)
					ddcConfDict = configDict[configKeys.CONFIG_DDC].get(ddcType,{})
					ddcIndexRange = (self.wbddcIndexBase, self.wbddcIndexBase + self.numWbddc - 1) if isWideband \
					                else (self.nbddcIndexBase, self.nbddcIndexBase + self.numNbddc - 1)
					newConfigDict[configKeys.CONFIG_DDC][ddcType] = self._normalizeConfigDictSection(\
							ddcConfDict, ddcIndexRange[0], ddcIndexRange[1])					
			elif self.numGigE > 0 and configKey == configKeys.CONFIG_IP:
				tmpDict = copy.deepcopy(configDict[configKeys.CONFIG_IP])
				newConfigDict[configKeys.CONFIG_IP] = self._normalizeConfigDictSection( \
							tmpDict, self.gigEIndexBase, self.gigEIndexBase + self.numGigE - 1)
				for gigEPortNum in xrange(self.gigEIndexBase, self.gigEIndexBase + self.numGigE, 1):
					if newConfigDict[configKeys.CONFIG_IP].has_key(gigEPortNum) and \
					   newConfigDict[configKeys.CONFIG_IP][gigEPortNum].has_key(configKeys.IP_DEST):
						tmpDict = copy.deepcopy(newConfigDict[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST])
						newConfigDict[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_DEST] = \
 						     self._normalizeConfigDictSection(tmpDict, \
 															  self.gigEDipEntryIndexBase, \
 															  self.gigEDipEntryIndexBase + self.numGigEDipEntries - 1)
			elif self.numTxs > 0 and configKey == configKeys.CONFIG_TX:
				tmpDict = copy.deepcopy(configDict[configKeys.CONFIG_TX])
				newConfigDict[configKeys.CONFIG_TX] = self._normalizeConfigDictSection( \
															tmpDict, \
															self.getTransmitterIndexRange()[0], \
															self.getTransmitterIndexRange()[1])
				for txNum in self.getTransmitterIndexRange():
					if newConfigDict[configKeys.CONFIG_TX].has_key(txNum):
						if newConfigDict[configKeys.CONFIG_TX][txNum].has_key(configKeys.CONFIG_CW):
							newConfigDict[configKeys.CONFIG_TX][txNum][configKeys.CONFIG_CW] = \
						         self._normalizeConfigDictSection( newConfigDict[configKeys.CONFIG_TX][txNum][configKeys.CONFIG_CW], \
																   self.txType.toneGenIndexBase, \
																   self.txType.toneGenIndexBase + self.txType.numToneGen - 1)
			elif configKey == configKeys.CONFIG_DUC:
				newConfigDict[configKeys.CONFIG_DUC] = {}
				for ducType in [configKeys.CONFIG_WBDUC, configKeys.CONFIG_NBDUC]:
					isWideband = (ducType == configKeys.CONFIG_WBDUC)
					ducConfDict = configDict[configKeys.CONFIG_DUC].get(ducType,{})
					ducIndexRange = (self.wbducIndexBase, self.wbducIndexBase + self.numWbduc - 1) if isWideband \
					                else (self.nbducIndexBase, self.nbducIndexBase + self.numNbduc - 1)
					newConfigDict[configKeys.CONFIG_DUC][ducType] = self._normalizeConfigDictSection(\
							ducConfDict, ducIndexRange[0], ducIndexRange[1])					
					pass
			elif configKey == configKeys.CONFIG_DDC_GROUP:
				newConfigDict[configKeys.CONFIG_DDC_GROUP] = {}
				for ddcType in [configKeys.CONFIG_WBDDC_GROUP, configKeys.CONFIG_NBDDC_GROUP]:
					isWideband = (ddcType == configKeys.CONFIG_WBDDC_GROUP)
					ddcGroupConfDict = configDict[configKeys.CONFIG_DDC_GROUP].get(ddcType,{})
					ddcGroupIndexRange = (self.wbddcGroupIndexBase, self.wbddcGroupIndexBase + self.numWbddcGroups - 1) if isWideband \
					                else (self.nbddcGroupIndexBase, self.nbddcGroupIndexBase + self.numNbddcGroups - 1)
					newConfigDict[configKeys.CONFIG_DDC_GROUP][ddcType] = self._normalizeConfigDictSection(\
							ddcGroupConfDict, ddcGroupIndexRange[0], ddcGroupIndexRange[1])					
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
			for gigEPortNum in xrange(self.gigEIndexBase, 
									  self.gigEIndexBase + self.numGigE, 1):
				if gigEPortNum in confDict:
					# Set source IP address for this GigE port
					if self.sipCmd is not None and self.sipCmd.settable and \
					   configKeys.IP_SOURCE in confDict[gigEPortNum]:
						cDict = { "parent": self, \
								  "verbose": self.verbose, \
								  "logFile": self.logFile, \
								  configKeys.GIGE_PORT_INDEX: gigEPortNum, \
								  configKeys.IP_SOURCE: confDict[gigEPortNum][configKeys.IP_SOURCE], \
								 }
						cmd = self.sipCmd(**cDict)
						success &= cmd.send( self.sendCommand, )
						if success and cmd.success:
							self.configuration[configKeys.CONFIG_IP][gigEPortNum][configKeys.IP_SOURCE] = \
							        getattr(cmd, configKeys.IP_SOURCE)
						else:
							self.cmdErrorInfo.extend(cmd.errorInfo)
					# Set destination IP table info for this GigE port
					if self.dipCmd is not None and self.dipCmd.settable and \
					   configKeys.IP_DEST in confDict[gigEPortNum]:
						for gigEDipEntryNum in xrange(self.gigEDipEntryIndexBase, 
											          self.gigEDipEntryIndexBase + self.numGigEDipEntries, 
											          1):
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
								# triggered on radios with less permissive configurations.
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
							self.cmdErrorInfo.extend(cmd.errorInfo)
			pass
		return success

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
				udpList.append( range(udpBase[index]+index*100,udpBase[index]+maxUdp+index*100) )
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
			self.udpList = [range(udpBase,udpBase+maxUdp),]
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
		if wideband:
			return cls.numWbddc
		else:
			return cls.numNbddc
	
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
	# \brief Gets the allowed rate set for the DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getDdcRateSet()
	@classmethod
	def getDdcBwSet(cls, wideband, index=None):
		ddcObj = cls.wbddcType if wideband else cls.nbddcType
		return ddcObj.getDdcBwSet(index) if ddcObj is not None else {}
	
	##
	# \brief Gets the allowed rate list for the DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getDdcRateList()
	@classmethod
	def getDdcBwList(cls, wideband, index=None):
		ddcObj = cls.wbddcType if wideband else cls.nbddcType
		return ddcObj.getDdcBwList(index) if ddcObj is not None else []
	
	##
	# \brief Gets the frequency offset range for the narrowband DDCs on the radio.
	#
	# \copydetails CyberRadioDriver::IRadio::getNbddcFrequencyRange()
	@classmethod
	def getDdcFrequencyRange(cls, wideband, index=None):
		ddcType = cls.wbddcType if wideband else cls.nbddcType
		return (0.0,0.0) if ddcType is None else ddcType.frqRange

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
# \brief Radio handler class for the NDR304.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR304 Connection Modes
#
# "tty"
#
# \section RadioConfig_NDR304 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2],
#      "bypassMode": [0, 1],
#      "tunerConfiguration": {
#            1: {
#               "frequency": [20000000.0-3000000000.0, step 1000000.0],
#               "attenuation": [0.0-30.0, step 1.0],
#               "enable": [0, 1],
#               "filter": [0, 1],
#               "timingAdjustment": [-200000 - 200000, step 1],
#            },
#         ...6 (repeat for each tuner)
#      },
#      "ddcConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "rateIndex": [0],
#                 "udpDest": [port],
#                 "vitaEnable": [0, 1, 2],
#                 "streamId": [stream ID],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#              },
#           ...6 (repeat for each WBDDC)
#         },
#      },
#      "ddcGroupConfiguration": {
#         "wideband": {
#              1: {
#                 "enable": [0, 1],
#                 "members": [None, single DDC, or iterable with multiple DDCs],
#              },
#           ...3 (repeat for each WBDDC group)
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
# \section WbddcRates_NDR304 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>4266666.66667</td></tr>
# </table>
#
# \section VitaEnable_NDR304 VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
# <tr><td>0</td><td>Vita49 and Vita49.1 disabled</td></tr>
# <tr><td>1</td><td>Vita49 enabled and Vita 49.1 disabled</td></tr>
# <tr><td>2</td><td>Vita 49 and Vita 49.1 enabled</td></tr>
# </table>
#
# \implements CyberRadioDriver.IRadio
class ndr304(_radio):
	_name = "NDR304"
	ifSpec = ndr304_ifSpec
	adcRate = 102.4e6
	numTuner = 6
	numWbddc = 6
	numNbddc = 0
	tunerType = components.ndr304_tuner
	wbddcType = components.ndr304_wbddc
	nbddcType = None
	numWbddcGroups = 3
	wbddcGroupIndexBase = 1
	wbddcGroupType = components.ndr304_wbddc_group
	numNbddcGroups = 0
	nbddcGroupIndexBase = 1
	nbddcGroupType = None
	statQry = command.stat304
	tstatQry = command.tstat304
	tadjCmd = command.tadj
	rbypCmd = command.rbyp
	fnrCmd = command.fnr
	#refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz",3:"External 1PPS",4:"External 1PPS with jitter-optimized control loop"}
	refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz"}
	rbypModes = {0:"Internal 102.4MHz",1:"External 102.4MHz"}
	udpDestInfo = "port"
	vitaEnableOptions = {0: "VITA-49 header disabled",
						 1: "VITA-49 header enabled, fractional timestamp in picoseconds",
						 2: "VITA-49 header disabled",
						 3: "VITA-49 header enabled, fractional timestamp in sample counts",
						 }


##
# \brief Radio handler class for the NDR308-1.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308-1 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308-1 Radio Configuration Options
#
# \code
# configDict = {
#      "configMode": [0, 1],
#      "referenceMode": [0, 1, 2, 3, 4],
#      "bypassMode": [0, 1],
#      "calibFrequency": [0, 25.0-3000.0],
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
#              },
#           ...8 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6, 7],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
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
#            },
#         ...2 (repeat for each Gigabit Ethernet port)
#      },
# }
# \endcode
#
# \section WbddcRates_NDR308-1 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>51200000.0</td></tr>
# <tr><td>1</td><td>25600000.0</td></tr>
# <tr><td>2</td><td>12800000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308-1 NBDDC Rate Settings
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
# \section VitaEnable_NDR308-1 VITA 49 Enabling Options
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
class ndr308_1(_radio):
	_name = "NDR308-1"
	ifSpec = ndr308_ifSpec
	adcRate = 102.4e6
	numTuner = 8
	numTunerBoards = 2
	numWbddc = 8
	numNbddc = 16
	numGigE = 2
	numGigEDipEntries = 32
	tunerType = components.ndr308_tuner
	wbddcType = components.ndr308_wbddc
	nbddcType = components.ndr308_1_nbddc
	numWbddcGroups = 4
	wbddcGroupIndexBase = 1
	wbddcGroupType = components.ndr308_wbddc_group
	numNbddcGroups = 8
	nbddcGroupIndexBase = 1
	nbddcGroupType = components.ndr308_nbddc_group
	statQry = command.stat308
	tstatQry = command.tstat308
	tadjCmd = command.tadj
	ppsCmd = command.pps
	utcCmd = command.utc
	rbypCmd = command.rbyp
	sipCmd = command.sip308
	dipCmd = command.dip308
	smacCmd = None
	dmacCmd = None
	calfCmd = command.calf
	fnrCmd = command.fnr
	gpsCmd = command.gps
	gposCmd = command.gpos
	rtvCmd = command.rtv
	tempCmd = command.temp
	gpioStaticCmd = command.gpio_static
	gpioSeqCmd = command.gpio_sequence
	refModes = {0:"Internal 10MHz",1:"External 10MHz",2:"Internal GPSDO 10MHz",3:"External 1PPS",4:"External 1PPS"}
	rbypModes = {0:"Internal 102.4MHz",1:"External 102.4MHz"}
	connectionModes = ["tcp"]
	udpDestInfo = "DIP table index"
	vitaEnableOptions = {0: "VITA-49 header disabled",
						 1: "VITA-49 header enabled, fractional timestamp in picoseconds",
						 2: "VITA-49 header disabled",
						 3: "VITA-49 header enabled, fractional timestamp in sample counts",
						 }
	
	def configureDipTable(self,index,sip,dip,dmac,udpBase):
		success = True
		x = [ int(i) for i in dip.split(".") ]
		x[-1]+=10
		sipCmd = command.radio_command( parent=self, cmdString="SIP %d,%s"%(index,sip) )
		success &= sipCmd.send( self.sendCommand )
		if success:
			self.sipTable[index] = sip
		self.dipTable[index] = {}
		for i in range(32):
			args = ", ".join( [str(i) for i in (index,i,dip,dmac,udpBase+i,udpBase+i)] )
			dipCmd = command.radio_command( parent=self, cmdString="DIP %s"%args )
			success &= dipCmd.send( self.sendCommand )
			if success:
				self.dipTable[index][i] = {"dip":dip,"dport":udpBase+i,"sport":udpBase+i,"sip":self.sipTable.get(index,None),}
		return success
	
	def getDipTableEntry(self,ifIndex=None,dipIndex=None):
		if ifIndex is None:
			return self.dipTable
		elif dipIndex is None:
			return self.dipTable.get(ifIndex,{})
		else:
			return self.dipTable.get(ifIndex,{}).get(dipIndex,{})

	def disableTenGigFlowControl(self,):
		return self.setTenGigFlowControlStatus(False)
	
	def enableTenGigFlowControl(self,):
		return self.setTenGigFlowControlStatus(True)
	
	def setTenGigFlowControlStatus(self,enable=False):
		success = False
		if self.tgfcCmd is not None and self.tgfcCmd.settable:
			confDict = {
					configKeys.CONFIG_IP: {
						}
				}
			for gigEPortNum in xrange(self.gigEIndexBase, 
									  self.gigEIndexBase + self.numGigE, 1):
				confDict[configKeys.CONFIG_IP][gigEPortNum] = {
						configKeys.GIGE_FLOW_CONTROL: 1 if enable else 0,
					}
			success = self.setConfiguration(confDict)
		return success
	
	def getTenGigFlowControlStatus(self,):
		status = {}
		if self.tgfcCmd is not None:
			confDict = self.getConfiguration()[configKeys.CONFIG_IP]
			for gigEPortNum in xrange(self.gigEIndexBase, 
									  self.gigEIndexBase + self.numGigE, 1):
				if configKeys.GIGE_FLOW_CONTROL in confDict[gigEPortNum]:
					status |= (confDict[gigEPortNum][configKeys.GIGE_FLOW_CONTROL]	== 1)
		return status

##
# \brief Radio handler class for the NDR308.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308 Radio Configuration Options
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
# \section WbddcRates_NDR308 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>61440000.0</td></tr>
# <tr><td>1</td><td>30720000.0</td></tr>
# <tr><td>2</td><td>15360000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308 NBDDC Rate Settings
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
# \section VitaEnable_NDR308 VITA 49 Enabling Options
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
class ndr308(ndr308_1):
	_name = "NDR308"
	numNbddc = 32
	wbddcType = components.ndr308_wbddc
	nbddcType = components.ndr308_nbddc
	tgfcCmd = command.tgfc


##
# \brief Radio handler class for the NDR308 4-tuner variety.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308 Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308_4 Radio Configuration Options
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
#         ...4 (repeat for each tuner)
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
#           ...4 (repeat for each WBDDC)
#         },
#         "narrowband": {
#              1: {
#                 "enable": [0, 1],
#                 "frequency": [-25600000.0-25600000.0, step 1],
#                 "rateIndex": [0, 1, 2, 3, 4, 5, 6],
#                 "udpDest": [DIP table index],
#                 "vitaEnable": [0, 1, 2, 3],
#                 "streamId": [stream ID],
#                 "rfIndex": [1, 2, 3, 4],
#                 "dataPort": [1, 2],
#              },
#           ...4 (repeat for each NBDDC)
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
# \section WbddcRates_NDR308_4 WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>61440000.0</td></tr>
# <tr><td>1</td><td>30720000.0</td></tr>
# <tr><td>2</td><td>15360000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308_4 NBDDC Rate Settings
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
# \section VitaEnable_NDR308_4 VITA 49 Enabling Options
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
class ndr308_4(ndr308):
	_name = "NDR308-4"
	numTuner = 4
	numWbddc = 4
	numNbddc = 4


##
# \brief Radio handler class for the NDR308-TS.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \section ConnectionModes_NDR308-TS Connection Modes
#
# "tcp"
#
# \section RadioConfig_NDR308-TS Radio Configuration Options
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
#               "attenuation": [0.0-46.0, step 1.0],
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
# }
# \endcode
#
# \section WbddcRates_NDR308-TS WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
# <tr><td>0</td><td>61440000.0</td></tr>
# <tr><td>1</td><td>30720000.0</td></tr>
# <tr><td>2</td><td>15360000.0</td></tr>
# </table>
#
# \section NbddcRates_NDR308-TS NBDDC Rate Settings
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
# \section VitaEnable_NDR308-TS VITA 49 Enabling Options
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
class ndr308_ts(ndr308):
	_name = "NDR308-TS"
	adcRate = 122.88e6
	wbddcType = components.ndr308ts_wbddc
	nbddcType = components.ndr308ts_nbddc

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
#      "calibFrequency": [0, 25.0-3000.0],
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
#               "frequency": [20000000.0-6000000000.0, step 1000000.0],
#               "attenuation": [0.0-10.0, step 1.0],
#               "enable": [0, 1],
#               "cwConfiguration": {
#                     1: {
#                        "cwFrequency": [-51200000.0-51200000.0, step 1],
#                        "cwAmplitude": [-32767-32767, step 1],
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
	tunerType = components.ndr651_tuner
	numNbddc = 8
	wbddcType = components.ndr651_wbddc
	nbddcType = components.ndr651_nbddc
	numWbddcGroups = 4
	wbddcGroupIndexBase = 1
	wbddcGroupType = components.ndr651_wbddc_group
	numNbddcGroups = 8
	nbddcGroupIndexBase = 1
	nbddcGroupType = components.ndr651_nbddc_group
	numTxs = 2
	txType = components.ndr651_tx
	numWbduc = 8
	wbducType = components.ndr651_wbduc
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
	
	
#-- End Radio Handler Objects --------------------------------------------------#
#-- Any radio handler objects added to this module must be added ABOVE the code #
#-- snippet below. -------------------------------------------------------------# 


# This section of code inspects this module for radio handler objects (objects 
# derived from _radio, thus implementing the IRadio interface), and adds each 
# object to the radio class map.
# To support a new radio, just create a new radio handler object inside this 
# module, and this code will do the rest.  However, you will need to add the 
# new radio to the list of supported radios in the "mainpage" documentation
# section of __init__.py.  :)
# Radio class map: maps radio name strings to radio handler class names.
_radio_class_map = {}
for name, obj in inspect.getmembers(sys.modules[__name__]):
	if inspect.isclass(obj) and issubclass(obj, _radio) and "_radio" not in name:
		# Add the object to the radio class map.
		#_radio_class_map[name] = obj
		_radio_class_map[name.replace("_","-")] = obj

##
# \brief Factory method for obtaining a radio handler class from the name
# of the radio.
#
# The name string used to identify the radio can be any string returned 
# by CyberRadioDriver.getSupportedRadios(), but the check is not case-sensitive.  
# The returned radio handler class will support the CyberRadioDriver.IRadio 
# interface.
#
# \param nameString The name string for the radio of interest.
# \returns A radio handler class for the desired radio.
# \throws RuntimeError if the desired radio is not supported.
def getRadioObject(nameString):
	nameString = nameString.strip().lower().replace("_","-")
	try:
		return _radio_class_map[nameString]
	except:
		raise RuntimeError("Unsupported radio: %s" % nameString)
	

