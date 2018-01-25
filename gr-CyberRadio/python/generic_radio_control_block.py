#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
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
import traceback

import CyberRadioDriver as crd


class generic_radio_control_block(gr.basic_block):
	"""
	docstring for block generic_radio_control_block
	"""
	_name = "genRadioCtrl"
	
	_disableOnStop = False
	
	_portEnable_controlRx = True
	_portEnable_controlTx = False
	
	_portEnable_statusRx = False
	_portEnable_statusTx = True
	
	_portEnable_freqRx = False
	_portEnable_freqTx = False
	
	_portEnable_enableRx = False
	_portEnable_enableTx = False
	
	_portEnable_udpRx = False
	_portEnable_udpTx = False
	
	_configParams = {}
	
	def __init__(self, radioObj, debug=False, **kwargs):
		self._init = True
		self._started = False
		self._stopped = False
		
		gr.basic_block.__init__(self,
			name=self._name,
			in_sig=None,
			out_sig=None)
		
		self.log = logging.getLogger(self._name)
		self.log.setLevel(logging.DEBUG if debug else logging.INFO)
		handler = logging.StreamHandler()
		handler.setLevel(logging.DEBUG)
		handler.setFormatter(logging.Formatter('%(asctime)s :: %(name)s(%(levelname)s) :: %(message)s'))
		self.log.addHandler( handler )
		self.log.debug("__init__")
		
		self.radioObj = radioObj
		self.log.debug("Radio Object = %r"%(self.radioObj,))
		
		## Setup ports for control messaging
		self.msgPort_control = pmt.intern("control")
		if self._portEnable_controlRx:
			self.log.debug("Enabling control message reception")
			self.message_port_register_in(self.msgPort_control)
			self.set_msg_handler(self.msgPort_control, self.rxControlMsg)
		if self._portEnable_controlTx:
			self.log.debug("Enabling control message transmission")
			self.message_port_register_out(self.msgPort_control)
		
		## Setup ports for status messaging
		self.msgPort_status = pmt.intern("status")
		if self._portEnable_statusRx:
			self.log.debug("Enabling status message reception")
			self.message_port_register_in(self.msgPort_status)
			self.set_msg_handler(self.msgPort_status, self.rxStatusMsg)
		if self._portEnable_statusTx:
			self.log.debug("Enabling status message transmission")
			self.message_port_register_out(self.msgPort_status)
		
		## Setup ports for enable messaging
		self.msgPort_enable = pmt.intern("enable")
		if self._portEnable_enableRx:
			self.log.debug("Enabling enable message reception")
			self.message_port_register_in(self.msgPort_enable)
			self.set_msg_handler(self.msgPort_enable, self.rxEnableMsg)
		if self._portEnable_enableTx:
			self.log.debug("Enabling enable message reception")
			self.message_port_register_out(self.msgPort_enable)
		
		## Setup ports for frequency messaging
		self.msgPort_freq = pmt.intern("freq")
		if self._portEnable_freqRx:
			self.log.debug("Enabling freq message reception")
			self.message_port_register_in(self.msgPort_freq)
			self.set_msg_handler(self.msgPort_freq, self.rxFreqMsg)
		if self._portEnable_freqTx:
			self.log.debug("Enabling freq message reception")
			self.message_port_register_out(self.msgPort_freq)
		
		## Setup ports for UDP block messaging
		self.msgPort_udp = pmt.intern("udp")
		if self._portEnable_udpRx:
			self.log.debug("Enabling UDP message reception")
			self.message_port_register_in(self.msgPort_udp)
			self.set_msg_handler(self.msgPort_udp, self.rxUdpMsg)
		if self._portEnable_udpTx:
			self.log.debug("Enabling UDP message reception")
			self.message_port_register_out(self.msgPort_udp)
	
	def __del__(self,):
		if self._disableOnStop:
			self.set_enable(False)
	
	def initRadioConnection(self,):
		self.log.debug("initRadioConnection")
		self.radioObj = self.radioParam.get("obj",None)
		if self.radioObj is None:
			self.log.debug("Creating radio object")
			self.radioObj = crd.getRadioObject(self.radioParam["type"])
		if not self.radioObj.isConnected():
			self.log.debug("Connecting to radio...")
			if all( self.radioParam.has_key(i) for i in ("host","port") ):
				self.radioObj.connect( "tcp", self.radioParam["host"], self.radioParam["port"] )
			elif all( self.radioParam.has_key(i) for i in ("device","baudrate") ):
				self.radioObj.connect( "tty", self.radioParam["device"], self.radioParam["baudrate"] )
			else:
				raise Exception("%s :: Can't connect to radio"%(self._name))
		if self.radioObj.isConnected():
			self.log.info("Connected to radio!")
	
	def start(self):
		if not self._started:
			self.log.debug("start")
			self._started = True
		return True
	
	def stop(self):
		self.log.debug("stop")
		if self._disableOnStop:
			self.set_enable(False)
		self._stopped = True
		return True
	
	def updateConfig(self,param=None):
		self.log.debug("updateConfig not implemented")
	
		## Setter & getter for radioParam
	def set_radioParam(self, radioParam={"type":"ndr308","host":"ndr308","port":8617,"obj":None}):
		if self._init or not hasattr(self, "radioParam"):
			self.radioParam = radioParam
			self.radioType = self.radioParam.get("type")
			print("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
		elif radioParam!=self.radioParam:
			print("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
			self.radioParam = radioParam
			self.updateConfig("radioParam")

	def get_radioParam(self,):
		return self.radioParam
	
	def setConfiguration(self,confDict):
		return self.radioObj.setConfiguration(confDict)

	def forecast(self, noutput_items, ninput_items_required):
		#setup size of input_items[i] for work call
		for i in range(len(ninput_items_required)):
			ninput_items_required[i] = noutput_items

	def general_work(self, input_items, output_items):
		output_items[0][:] = input_items[0]
		consume(0, len(input_items[0]))
		#self.consume_each(len(input_items[0]))
		return len(output_items[0])
	
	def _sendPmtPair(self, port, key, value):
		a = pmt.intern(key)
		b = pmt.to_pmt(value)
		msg = pmt.cons(a, b)
		self.message_port_pub(port, msg)
	
	def txControlMsg(self, label, content):
		self.log.debug("txControlMsg(%r, %r)"%(label,content))
		self._sendPmtPair(self.msgPort_control, label, content)
	
	def rxControlMsg(self, msg):
		confDict = None
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxControlMsg(%s)"%(repr(pyMsg)))
		msgId = pyMsg[0]
		if isinstance(pyMsg[1],str):
			content = json.loads(pyMsg[1])
		elif isinstance(pyMsg[1],dict):
			content = pyMsg[1]
		else:
			content = {}
		
		setList = []
		for k,v in content.get("config",{}).iteritems():
			k = str(k)
			try:
				self.log.debug("Can I use parameter %r (%r)?"%(k,v,))
				if self._configParams.has_key(k):
					self.log.debug("Yes I can!")
					self._configParams[k](v)
					setList.append(k)
			except:
				self.log.debug("ERROR using config parameter %r"%(k,))
				traceback.print_exc()
		
		if len(setList):
			info = {"block": self._name, 
					"parameters": setList, 
					"controlMsg": pyMsg
					 }
			self._sendPmtPair(self.msgPort_status, msgId, json.dumps(info))
	
	def txStatusMsg(self, label, content):
		self.log.debug("txStatusMsg(%r, %r)"%(label,content))
		self._sendPmtPair(self.msgPort_status, label, content)
	
	def rxStatusMsg(self, msg):
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxStatusMsg(%s)"%(repr(pyMsg)))
	
	def txEnableMsg(self, label, content):
		self.log.debug("txEnableMsg(%r, %r)"%(label,content))
		self._sendPmtPair(self.msgPort_enable, label, content)
	
	def rxEnableMsg(self, msg):
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxEnableMsg(%s)"%(repr(pyMsg)))
	
	def txFreqMsg(self, label, content):
		self.log.debug("txFreqMsg(%r, %r)"%(label,content))
		self._sendPmtPair(self.msgPort_freq, label, content)
	
	def rxFreqMsg(self, msg):
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxFreqMsg(%s)"%(repr(pyMsg)))
	
	def txUdpMsg(self, label, content):
		self.log.debug("txUdpMsg(%r, %r)"%(label,content))
		self._sendPmtPair(self.msgPort_freq, label, content)
	
	def rxUdpMsg(self, msg):
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxUdpMsg(%s)"%(repr(pyMsg)))
	
	def set_attenuation(self, attenuation=0):
		self.log.debug("set_attenuation not implemented")
	def set_ddcList(self, ddcList=12345):
		self.log.debug("set_ddcList not implemented")
	def set_dipIndex(self, dipIndex=None):
		self.log.debug("set_dipIndex not implemented")
	def set_enable(self, enable=True):
		self.log.debug("set_enable not implemented")
	def set_filter(self, filter=1):
		self.log.debug("set_filter not implemented")
	def set_freq(self, freq=0):
		self.log.debug("set_freq not implemented")
	def set_freq(self, freq=[0,0]):
		self.log.debug("set_freq not implemented")
	def set_idString(self, idString):
		self.log.debug("set_idString not implemented")
	def set_index(self, index=1):
		self.log.debug("set_index not implemented")
	def set_localInterface(self, localInterface=None):
		self.log.debug("set_localInterface not implemented")
	def set_mode(self, mode=0):
		self.log.debug("set_mode not implemented")
	def set_otherArgs(self, otherArgs={}):
		self.log.debug("set_otherArgs not implemented")
	def set_radioInterface(self, radioInterface=1):
		self.log.debug("set_radioInterface not implemented")
	def set_radioParam(self, radioParam={"type":"ndr308","host":"ndr308","port":8617,"obj":None}):
		self.log.debug("set_radioParam")
		if self._init or not hasattr(self, "radioParam"):
			self.radioParam = radioParam
			self.radioType = self.radioParam.get("type")
			print("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
		elif radioParam!=self.radioParam:
			print("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
			self.radioParam = radioParam
			self.updateConfig("radioParam")
	def set_rate(self, rate=0):
		self.log.debug("set_rate not implemented")
	def set_rfFreq(self, rfFreq=1):
		self.log.debug("set_rfFreq not implemented")
	def set_rfSource(self, rfSource=1):
		self.log.debug("set_rfSource not implemented")
	def set_udpPort(self, udpPort=12345):
		self.log.debug("set_udpPort not implemented")
	def set_wideband(self, wideband=True):
		self.log.debug("set_wideband not implemented")

	
