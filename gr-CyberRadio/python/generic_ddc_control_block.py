#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
from gnuradio import gr
from gnuradio.gr import pmt
import json
import logging
import numpy

import CyberRadioDriver as crd
from .generic_radio_control_block import generic_radio_control_block


class generic_ddc_control_block(generic_radio_control_block, gr.basic_block):
	"""
	docstring for block generic_ddc_control_block
	"""
	_disableOnStop = True
	
	_portEnable_enableRx = False
	
	_portEnable_freqRx = True
	_portEnable_freqTx = True
	
	_portEnable_udpRx = True
	_portEnable_udpTx = True
	
	def __init__(self,
					radioObj,
					index=1,
					enable=True,
					wideband=True,
					rate=0,
					mode=0,
					freq=0,
					rfSource=1,
					rfFreq=0,
					radioInterface=1,
					dipIndex=None,
					localInterface=None,
					udpPort=12345,
					otherArgs={},
					debug=False,
					autoStart=True):
		self._configParams = {"enable":self.set_enable, 
						"rate": self.set_rate, 
                        "index":self.set_index,
                        "freq":self.set_freq
						 }
		
		self._name = "%sBDDC%d_ctrl"%("W" if wideband else "N",index)
		self._debug = debug
		
		generic_radio_control_block.__init__(self, radioObj=radioObj, debug=debug)
		self.log.debug("hello")
		self.freqUnits = 1
		self.arp = False
		
		self.log.debug("%s.__init__(radioObj=%r, index=%r, rate=%s)"%(self._name,radioObj,index,rate))

		self.totalRepeatPackets = None
		self.activeRepeatPackets = None
		self.phaseOffset = None
		
		self.set_index(index)
		self.set_enable(enable)
		self.set_wideband(wideband)
		self.set_rate(rate)
		self.set_mode(mode)
		self.set_freq(freq)
		self.set_rfSource(rfSource)
		self.set_rfFreq(rfFreq)
		self.set_radioInterface(radioInterface)
		self.set_dipIndex(dipIndex)
		self.set_localInterface(localInterface)
		self.set_udpPort(udpPort)
		self.set_otherArgs(otherArgs)
		# self.set_phaseOffset(0.0)
		# self.set_totalRepeatPackets(totalRepeatPackets)
		# self.set_activeRepeatPackets(activeRepeatPackets)
		
		self.updateConfig()
		self._init = False
	
	def __del__(self,):
		self.log.debug( (self._name+".__del__()").center(80,"~") )
		self.set_enable(False)
	
	def getStreamId(self):
		return (int(self.wideband)<<15)|self.index
	
	def getDipConf(self,dipIndex):
		if self.radioInterface in self.radioObj.getGigEIndexRange():
			interfaceList = [self.radioInterface,]
		else:
			interfaceList = self.radioObj.getGigEIndexRange()
		self.log.debug("getDipConf: dipIndex = %d(%d), radioInterface = %r(%r)"%(self.dipIndex,dipIndex,self.radioInterface,interfaceList))
		dipConfDict = {}
		for radioInterface in interfaceList:
			dipConfDict[radioInterface] = {
								crd.configKeys.IP_DEST: { 
									dipIndex: { 
										crd.configKeys.GIGE_SOURCE_PORT:self.index+(10000 if self.wideband else 20000),
										crd.configKeys.GIGE_DEST_PORT:self.udpPort,
										 }, 
									 },
								crd.configKeys.IP_SOURCE : {
										crd.configKeys.GIGE_SOURCE_PORT : self.udpPort,
									}
								 }
		if self.localInterface is not None and len(self.localInterface)>0:
			dmac, dip = crd.getInterfaceAddresses(self.localInterface)
			self.log.debug( "interface = {0}, dmac = {1}, dip = {2}".format(self.localInterface, dmac, dip,) )
			temp = [int(i) for i in dip.split(".")]
			temp[-1] = (~temp[-1])&0xff
			sip = ".".join(str(i) for i in temp)
			for radioInterface in interfaceList:
				#~ dipConfDict = { 
								#~ radioInterface: {
									#~ crd.configKeys.IP_SOURCE: sip, 
									#~ crd.configKeys.IP_DEST: { 
										#~ dipIndex: { 
											#~ crd.configKeys.GIGE_SOURCE_PORT:self.udpPort,
											#~ crd.configKeys.GIGE_DEST_PORT:self.udpPort,
											#~ crd.configKeys.GIGE_MAC_ADDR:dmac,
											#~ crd.configKeys.GIGE_IP_ADDR:dip,
											#~ }, 
										 #~ }, 
									 #~ }, 
								 #~ }
				dipConfDict[radioInterface][crd.configKeys.IP_DEST][dipIndex][crd.configKeys.GIGE_MAC_ADDR] = dmac
				dipConfDict[radioInterface][crd.configKeys.IP_DEST][dipIndex][crd.configKeys.GIGE_IP_ADDR] = dip
				dipConfDict[radioInterface][crd.configKeys.IP_SOURCE][crd.configKeys.GIGE_IP_ADDR] = sip	
				dipConfDict[radioInterface][crd.configKeys.IP_SOURCE][crd.configKeys.GIGE_SOURCE_PORT] = self.udpPort
		else:
			if any(i in self.radioObj.name.lower() for i in ("562","358","551","357","324")):
				self.log.debug("self.arp: {0}".format(self.arp))
				if self.arp == True:
					# since an interface was not provided, try to ARP it for the destination.
					dipConfDict[radioInterface][crd.configKeys.IP_DEST][dipIndex][crd.configKeys.GIGE_ARP] = True
		
		return dipConfDict
	
	def updateConfig(self,param=None):
		self.log.debug("%s.updateConfig( %s ), init=%s"%(self._name, param, self._init))
		if self.dipIndex<0:
			dipIndex = self.index-self.radioObj.getDdcIndexRange(self.wideband)[0] + (0 if self.wideband else self.radioObj.getNumWbddc())
		else:
			dipIndex = self.dipIndex
		sendFreqMsgFlag = False
		ddcConfDict = None
		dipConfDict = None
		#~ if self.radioInterface<0:
			#~ portIndexRange = self.radioObj.getGigEIndexRange()
			#~ numPorts = len(portIndexRange)
			#~ self.radioInterface = portIndexRange[ (self.index-1)%numPorts ]
			
		rateKey = crd.configKeys.DDC_RATE_INDEX
		
		#for gpr configurations force packet type and set spectral rate
		if self.enable and self.radioObj.name.lower() in ("ndr804","ndr328","ndr804-ptt","ndr301-ptt"):
			self.log.debug('if self.enable and self.radioObj.name.lower() in ("ndr804","ndr328","ndr804-ptt","ndr301-ptt")')
			enableVal = 2
			if self.wideband:
				rateKey = crd.configKeys.DDC_SPECTRAL_FRAME_RATE
			vitaVal = None
			udpDest = dipIndex
		else:
			enableVal = self.enable
			if any(i in self.radioObj.name.lower() for i in ("470","472","304",)):
				vitaVal = 2
				udpDest = self.udpPort
			else:
				vitaVal = 3
				udpDest = dipIndex
		if (self._init and param is None) or ((not self._init) and (param=="index")):
			ddcConfDict = { rateKey: self.rate, 
							crd.configKeys.DDC_STREAM_ID: self.getStreamId(), 
							crd.configKeys.ENABLE: enableVal, 
							crd.configKeys.DDC_OUTPUT_FORMAT: self.mode, 
							crd.configKeys.DDC_UDP_DESTINATION: udpDest, 
							crd.configKeys.DDC_DATA_PORT: self.radioInterface, 
							 }
			if "364" in self.radioObj.name.lower():
				for key,value in (
						(crd.configKeys.DDC_PHASE_OFFSET, self.phaseOffset),
						(crd.configKeys.DDC_TOTAL_REPEAT_PACKETS, self.totalRepeatPackets),
						(crd.configKeys.DDC_ACTIVE_REPEAT_PACKETS, self.activeRepeatPackets), 
						 ):
					if value is not None:
						ddcConfDict[key] = value
			if self.radioObj.isDdcSelectableSource(self.wideband):
				ddcConfDict[crd.configKeys.DDC_RF_INDEX] = self.rfSource
			if self.radioObj.isDdcTunable(self.wideband):
				ddcConfDict[crd.configKeys.DDC_FREQUENCY_OFFSET] = self.ddcFreq
			if vitaVal is not None:
				ddcConfDict[ crd.configKeys.DDC_VITA_ENABLE ] = vitaVal
			# if self.radioObj.name.lower() in ("ndr354","ndr364",):
			# 	ddcConfDict[ crd.configKeys.DDC_CLASS_ID ] = True
			dipConfDict = self.getDipConf(dipIndex)
			sendFreqMsgFlag = True
		else:
			if param in ("localInterface","radioInterface","dipIndex","udpPort"):
				dipConfDict = self.getDipConf(dipIndex)
			else:
				ddcConfDict = {}
				if param=="enable":
					ddcConfDict[ crd.configKeys.ENABLE ] = enableVal
					if enableVal:
						ddcConfDict[ crd.configKeys.DDC_STREAM_ID ] = self.getStreamId()
						ddcConfDict[ crd.configKeys.DDC_UDP_DESTINATION ] = udpDest
						# if self.radioObj.name.lower() in ("ndr354","ndr364",):
						# 	ddcConfDict[ crd.configKeys.DDC_CLASS_ID ] = True
					if vitaVal is not None:
						ddcConfDict[ crd.configKeys.DDC_VITA_ENABLE ] = vitaVal
				elif param=="rate":
					ddcConfDict[ rateKey ] = self.rate
				elif param=="mode":
					ddcConfDict[ crd.configKeys.DDC_OUTPUT_FORMAT ] = self.mode
				elif param=="rate&mode":
					ddcConfDict[ rateKey ] = self.rate
					ddcConfDict[ crd.configKeys.DDC_OUTPUT_FORMAT ] = self.mode
				elif param=="freq":
					ddcConfDict[ crd.configKeys.DDC_FREQUENCY_OFFSET ] = self.ddcFreq
					sendFreqMsgFlag = True
				elif param=="rfSource":
					if self.radioObj.isDdcSelectableSource(self.wideband):
						ddcConfDict[ crd.configKeys.DDC_RF_INDEX ] = self.rfSource
				elif param=="phaseOffset" and ("364" in self.radioObj.name.lower()) and (self.phaseOffset is not None):
					ddcConfDict[ crd.configKeys.DDC_PHASE_OFFSET ] = self.phaseOffset
				elif param=="totalRepeatPackets" and ("364" in self.radioObj.name.lower()) and (self.totalRepeatPackets is not None):
					ddcConfDict[ crd.configKeys.DDC_TOTAL_REPEAT_PACKETS ] = self.totalRepeatPackets
				elif param=="activeRepeatPackets" and ("364" in self.radioObj.name.lower()) and (self.activeRepeatPackets is not None):
					ddcConfDict[ crd.configKeys.DDC_ACTIVE_REPEAT_PACKETS ] = self.activeRepeatPackets
				#~ else:
					#~ raise Exception("Error: unknown command " + param)
		if (ddcConfDict is not None) or (dipConfDict is not None):
			ddcType = crd.configKeys.CONFIG_WBDDC if self.wideband else crd.configKeys.CONFIG_NBDDC
			confDict = {}
			if ddcConfDict is not None:
				confDict[crd.configKeys.CONFIG_DDC] = { ddcType: { self.index: ddcConfDict } }
			if dipConfDict is not None:
				confDict[crd.configKeys.CONFIG_IP] = dipConfDict
			self.log.debug( json.dumps(confDict, sort_keys=True) )
			if self.radioObj.isConnected():
				self.radioObj.setConfiguration(confDict)
				errorMsg = self.radioObj.cmdErrorInfo
				if (len(errorMsg) > 0):
					self.txStatusMsg("Status", "Frequency out of range")
		if sendFreqMsgFlag:
			self.txFreqMsg("nbddc_freq",self.freq)
	
	def _sendFreqMessage(self):
		pass
	
	## Setter & getter for index
	def set_index(self, index=1):
		if self._init or not hasattr(self, "index"):
			self.index = index
			self.log.debug("%s.set_index: %s -> %s"%(self._name, repr(self.index), repr(index),))
		elif index!=self.index:
			self.log.debug("%s.set_index: %s -> %s"%(self._name, repr(self.index), repr(index),))
			toggle=self.get_enable()
			if toggle:
				self.set_enable(False)
			self.index = index
			'''
			if "562" in self.radioObj.name.lower():
				self.index = 0
			'''
			self.updateConfig("index")
			if toggle:
				self.set_enable(True)
		else:
			self.log.debug("%s.set_index: %s == %s"%(self._name, repr(self.index), repr(index),))

	def get_index(self,):
		return self.index

	def get_idString(self):
		return self.idString

	def set_idString(self, idString):
		self.idString = idString
		
	## Setter & getter for enable
	def set_enable(self, enable=True):
		if self._init or not hasattr(self, "enable"):
			self.enable = enable
			self.log.debug("%s.set_enable: %s -> %s"%(self._name, repr(self.enable), repr(enable),))
		else:
			if enable!=self.enable:
				self.log.debug("%s.set_enable: %s -> %s"%(self._name, repr(self.enable), repr(enable),))
				self.enable = enable
				self.updateConfig("enable")
			else:
				self.log.debug("%s.set_enable: %s == %s"%(self._name, repr(self.enable), repr(enable),))

	def get_enable(self,):
		return self.enable

	## Setter & getter for wideband
	def set_wideband(self, wideband=True):
		if self._init or not hasattr(self, "wideband"):
			self.log.debug("%s.set_wideband: %s -> %s"%(self._name, "n/a", repr(wideband),))
			self.wideband = wideband
		elif wideband!=self.wideband:
			self.log.debug("%s.set_wideband: %s -> %s"%(self._name, repr(self.wideband), repr(wideband),))
			self.wideband = wideband
			self.updateConfig("wideband")
		else:
			self.log.debug("%s.set_wideband: %s == %s"%(self._name, repr(self.wideband), repr(wideband),))

	def get_wideband(self,):
		return self.wideband

	## Setter & getter for rate
	def set_rate(self, rate=0):
		if self._init or not hasattr(self, "rate"):
			self.rate = rate
			self.log.debug("%s.set_rate: %s -> %s"%(self._name, "n/a", repr(rate),))
		elif rate!=self.rate:
			self.log.debug("%s.set_rate: %s -> %s"%(self._name, repr(self.rate), repr(rate),))
			self.rate = rate
			self.updateConfig("rate")
		else:
			self.log.debug("%s.set_rate: %s == %s"%(self._name, repr(self.rate), repr(rate),))

	def get_rate(self,):
		return self.rate

	## Setter & getter for mode
	def set_mode(self, mode=0):
		if self._init or not hasattr(self, "mode"):
			self.mode = mode
			self.log.debug("%s.set_mode: %s -> %s"%(self._name, repr(self.mode), repr(mode),))
		elif mode!=self.mode:
			self.log.debug("%s.set_mode: %s -> %s"%(self._name, repr(self.mode), repr(mode),))
			self.mode = mode
			self.updateConfig("mode")

	def get_mode(self,):
		return self.mode
	
	def set_rate_and_mode(self, rate=0, mode=None):
		update = False
		
		if self._init or not hasattr(self, "mode"):
			self.mode = mode
			self.log.debug("%s.set_rate_and_mode: %s -> %s"%(self._name, repr(self.mode), repr(mode),))
		elif mode!=self.mode:
			self.log.debug("%s.set_rate_and_mode: %s -> %s"%(self._name, repr(self.mode), repr(mode),))
			self.mode = mode
			update = True
		else:
			self.log.debug("%s.set_rate_and_mode: %s == %s"%(self._name, repr(self.mode), repr(mode),))

		if self._init or not hasattr(self, "rate"):
			self.rate = rate
			self.log.debug("%s.set_rate_and_mode: %s -> %s"%(self._name, "n/a", repr(rate),))
		elif rate!=self.rate:
			self.log.debug("%s.set_rate_and_mode: %s -> %s"%(self._name, repr(self.rate), repr(rate),))
			self.rate = rate
			update = True
		else:
			self.log.debug("%s.set_rate_and_mode: %s == %s"%(self._name, repr(self.rate), repr(rate),))
		
		if update:
			self.updateConfig("rate&mode")


	## Setter & getter for mode
	def set_phaseOffset(self, phaseOffset=None):
		if self._init or not hasattr(self, "phaseOffset"):
			self.phaseOffset = phaseOffset
			self.log.debug("%s.set_phaseOffset: %s -> %s"%(self._name, repr(self.phaseOffset), repr(phaseOffset),))
		elif phaseOffset!=self.phaseOffset:
			self.log.debug("%s.set_phaseOffset: %s -> %s"%(self._name, repr(self.phaseOffset), repr(phaseOffset),))
			self.phaseOffset = phaseOffset
			if self.phaseOffset is not None:
				self.updateConfig("phaseOffset")
	
	def set_totalRepeatPackets(self, totalRepeatPackets=None):
		if self._init or not hasattr(self, "totalRepeatPackets"):
			self.totalRepeatPackets = totalRepeatPackets
			self.log.debug("%s.set_totalRepeatPackets: %s -> %s"%(self._name, repr(self.totalRepeatPackets), repr(totalRepeatPackets),))
		elif totalRepeatPackets!=self.totalRepeatPackets:
			self.log.debug("%s.set_totalRepeatPackets: %s -> %s"%(self._name, repr(self.totalRepeatPackets), repr(totalRepeatPackets),))
			self.totalRepeatPackets = totalRepeatPackets
			if self.totalRepeatPackets is not None:
				self.updateConfig("totalRepeatPackets")

	def set_activeRepeatPackets(self,activeRepeatPackets=1):
		if self._init or not hasattr(self, "activeRepeatPackets"):
			self.activeRepeatPackets = activeRepeatPackets
			self.log.debug("%s.set_activeRepeatPackets: %s -> %s"%(self._name, repr(self.activeRepeatPackets), repr(activeRepeatPackets),))
		elif activeRepeatPackets!=self.activeRepeatPackets:
			self.log.debug("%s.set_activeRepeatPackets: %s -> %s"%(self._name, repr(self.activeRepeatPackets), repr(activeRepeatPackets),))
			self.activeRepeatPackets = activeRepeatPackets 
			if self.activeRepeatPackets is not None:
				self.updateConfig("activeRepeatPackets")

	def get_mode(self,):
		return self.mode

	def rxFreqMsg(self, msg):
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxFreqMsg(%s)"%(repr(pyMsg)))
		if (len(pyMsg)==2) and (pyMsg[0]=="freq"):
			self.set_freq(pyMsg[1])

	## Setter & getter for freq
	def set_freq(self, freq=0):
		if hasattr(self, "rfFreq") and (self.rfFreq>0):
			ddcFreq = int( numpy.round( (freq*self.freqUnits)-(self.rfFreq*1e6) ) )
		else:
			ddcFreq = int( numpy.round( (freq*self.freqUnits) ) )
		if self._init or not hasattr(self, "freq"):
			self.freq = freq
			self.ddcFreq = ddcFreq
			self.log.debug("%s.set_freq: %s(%s) -> %s(%s)"%(self._name, repr(self.freq), repr(self.ddcFreq), repr(freq), repr(ddcFreq),))
		elif (freq!=self.freq) or (ddcFreq!=self.ddcFreq):
			self.log.debug("%s.set_freq: %s(%s) -> %s(%s)"%(self._name, repr(self.freq), repr(self.ddcFreq), repr(freq), repr(ddcFreq),))
			self.freq = freq
			self.ddcFreq = ddcFreq
			self.updateConfig("freq")
			self.updateConfig("ddcFreq")
		else:
			self.log.debug("%s.set_freq: %s(%s) == %s(%s)"%(self._name, repr(self.freq), repr(self.ddcFreq), repr(freq), repr(ddcFreq),))

	def get_freq(self,):
		return self.freq

	## Setter & getter for rfSource
	def set_rfSource(self, rfSource=1):
		if self._init or not hasattr(self, "rfSource"):
			self.rfSource = rfSource
			self.log.debug("%s.set_rfSource: %s -> %s"%(self._name, repr(self.rfSource), repr(rfSource),))
		elif rfSource!=self.rfSource:
			self.log.debug("%s.set_rfSource: %s -> %s"%(self._name, repr(self.rfSource), repr(rfSource),))
			self.rfSource = rfSource
			self.updateConfig("rfSource")
		else:
			self.log.debug("%s.set_rfSource: %s == %s"%(self._name, repr(self.rfSource), repr(rfSource),))

	def get_rfSource(self,):
		return self.rfSource

	## Setter & getter for rfFreq
	def set_rfFreq(self, rfFreq=0):
		if self._init or not hasattr(self, "rfFreq"):
			self.rfFreq = rfFreq
			self.log.debug("%s.set_rfFreq: %s -> %s"%(self._name, repr(self.rfFreq), repr(rfFreq),))
			self.set_freq(self.freq)
		elif rfFreq!=self.rfFreq:
			self.log.debug("%s.set_rfFreq: %s -> %s"%(self._name, repr(self.rfFreq), repr(rfFreq),))
			self.rfFreq = rfFreq
			self.set_freq(self.freq)
		else:
			self.log.debug("%s.set_rfFreq: %s == %s no change."%(self._name, repr(self.rfFreq), repr(rfFreq),))

	#~ def get_rfFreq(self,):
		#~ return self.rfFreq

	## Setter & getter for radioInterface
	def set_radioInterface(self, radioInterface=1):
		if self._init or not hasattr(self, "radioInterface"):
			self.radioInterface = radioInterface
			self.log.debug("%s.set_radioInterface: %s -> %s"%(self._name, repr(self.radioInterface), repr(radioInterface),))
		elif radioInterface!=self.radioInterface:
			self.log.debug("%s.set_radioInterface: %s -> %s"%(self._name, repr(self.radioInterface), repr(radioInterface),))
			self.radioInterface = radioInterface
			self.updateConfig("radioInterface")

	def get_radioInterface(self,):
		return self.radioInterface

	## Setter & getter for dipIndex
	def set_dipIndex(self, dipIndex=None):
#      if dipIndex is None:
#          dipIndex = self.index-1
#          if not self.wideband:
#              dipIndex += self.radioObj.getNumWbddc()
		if self._init or not hasattr(self, "dipIndex"):
			self.dipIndex = dipIndex
			self.log.debug("%s.set_dipIndex: %s -> %s"%(self._name, repr(self.dipIndex), repr(dipIndex),))
		elif dipIndex!=self.dipIndex:
			self.log.debug("%s.set_dipIndex: %s -> %s"%(self._name, repr(self.dipIndex), repr(dipIndex),))
			self.dipIndex = dipIndex
			self.updateConfig("dipIndex")

	def get_dipIndex(self,):
		return self.dipIndex

	## Setter & getter for localInterface
	def set_localInterface(self, localInterface=None):
		if self._init or not hasattr(self, "localInterface"):
			self.localInterface = localInterface
			self.log.debug("%s.set_localInterface: %s -> %s"%(self._name, repr(self.localInterface), repr(localInterface),))
		elif localInterface!=self.localInterface:
			self.log.debug("%s.set_localInterface: %s -> %s"%(self._name, repr(self.localInterface), repr(localInterface),))
			self.localInterface = localInterface
			self.updateConfig("localInterface")

	def get_localInterface(self,):
		return self.localInterface

	## Setter & getter for udpPort
	def set_udpPort(self, udpPort=12345):
		if self._init or not hasattr(self, "udpPort"):
			self.udpPort = udpPort
			self.log.debug("%s.set_udpPort: %s -> %s"%(self._name, repr(self.udpPort), repr(udpPort),))
		elif udpPort!=self.udpPort:
			self.log.debug("%s.set_udpPort: %s -> %s"%(self._name, repr(self.udpPort), repr(udpPort),))
			self.udpPort = udpPort
			self.updateConfig("udpPort")

	def get_udpPort(self,):
		return self.udpPort

	## Setter & getter for otherArgs
	def set_otherArgs(self, otherArgs={}):
		self.freqUnits = otherArgs.get("freqUnits", self.freqUnits)
		self.arp = otherArgs.get("arp", self.arp)

	def get_otherArgs(self,):
		return self.otherArgs
	
	def setSampleRate(self,):
		self.fs = self.radioObject.getDdcRateSet(self.wideband,self.index).get(self.rate,1.0)
	
	def getSampleRate(self,):
		self.log.debug("%s.getSampleRate"%(self.blockName,))
		return self.fs

#   def forecast(self, noutput_items, ninput_items_required):
#      #setup size of input_items[i] for work call
#      for i in range(len(ninput_items_required)):
#          ninput_items_required[i] = noutput_items
# 
#   def general_work(self, input_items, output_items):
#      output_items[0][:] = input_items[0]
#      consume(0, len(input_items[0]))
#      #self.consume_each(len(input_items[0]))
#      return len(output_items[0])
