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
import json
import numpy

import CyberRadioDriver as crd
from .generic_radio_control_block import generic_radio_control_block


class generic_group_control_block(generic_radio_control_block, gr.basic_block):
	"""
	docstring for block generic_group_control_block
	"""
	_disableOnStop = True
	
	def __init__(self,
					radioObj, 
					index=-1, 
					enable=True, 
					wideband=True, 
					ddcList=[], 
# 					rate=0, 
# 					mode=0, 
# 					freq=0, 
# 					rfSource=1, 
# 					rfFreq=0,
# 					radioInterface=1, 
# 					dipIndex=None, 
# 					localInterface=None, 
# 					udpPortList=[], 
					otherArgs={}, 
					debug=False, 
					autoStart=True, 
					):
		self._configParams = {"enable":self.set_enable, 
						 }
		self._init = True
		self._name = "%sBGRP%d_ctrl"%("W" if wideband else "N",index)
		self._debug = debug
		
		generic_radio_control_block.__init__(self, radioObj=radioObj, debug=debug)
		self.log.debug("hello")
		self.freqUnits = 1
		
		self.set_index(index)
		self.set_enable(enable)
		self.set_wideband(wideband)
		self.set_ddcList(ddcList)
		self.set_otherArgs(otherArgs)
		
		self.updateConfig()
		self._init = False

	def updateConfig(self,param=None):
		groupConf = {}
		groupType = crd.configKeys.CONFIG_WBDDC_GROUP if self.wideband else crd.configKeys.CONFIG_NBDDC_GROUP
		remDict = None
		if self._init or param=="enable":
			groupConf[ crd.configKeys.ENABLE ] = self.enable
		if self._init or param=="ddcList":
			groupConf[ crd.configKeys.DDC_GROUP_MEMBERS ] = self.ddcList
		if len(groupConf)>0:
			confDict = {crd.configKeys.CONFIG_DDC_GROUP:{ groupType: { self.index: groupConf } } }
			self.log.debug( json.dumps(confDict, sort_keys=True) )
			if self.radioObj.isConnected():
				self.radioObj.setConfiguration(confDict)

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
			self.updateConfig("index")
			if toggle:
				self.set_enable(True)

	def get_index(self,):
		return self.index

	## Setter & getter for enable
	def set_enable(self, enable=True):
		if self._init or not hasattr(self, "enable"):
			self.enable = enable
			self.log.debug("%s.set_enable: %s -> %s"%(self._name, repr(self.enable), repr(enable),))
		else:
			self.log.debug("%s.set_enable: %s -> %s"%(self._name, repr(self.enable), repr(enable),))
			if enable!=self.enable:
				self.log.debug("%s.set_enable: %s -> %s"%(self._name, repr(self.enable), repr(enable),))
				self.enable = enable
				self.updateConfig("enable")

	def get_enable(self,):
		return self.enable

	## Setter & getter for wideband
	def set_wideband(self, wideband=True):
		if self._init or not hasattr(self, "wideband"):
			self.wideband = wideband
			self.log.debug("%s.set_wideband: %s -> %s"%(self._name, repr(self.wideband), repr(wideband),))
		elif wideband!=self.wideband:
			self.log.debug("%s.set_wideband: %s -> %s"%(self._name, repr(self.wideband), repr(wideband),))
			self.wideband = wideband
			self.updateConfig("wideband")

	def get_wideband(self,):
		return self.wideband

		## Setter & getter for ddcList
	def set_ddcList(self, ddcList=12345):
		if self._init or not hasattr(self, "ddcList"):
			self.ddcList = ddcList
			self.log.debug("%s.set_ddcList: %s -> %s"%(self._name, repr(self.ddcList), repr(ddcList),))
		elif ddcList!=self.ddcList:
			self.log.debug("%s.set_ddcList: %s -> %s"%(self._name, repr(self.ddcList), repr(ddcList),))
			self.ddcList = ddcList
			self.updateConfig("ddcList")

	def get_ddcList(self,):
		return self.ddcList

	## Setter & getter for otherArgs
	def set_otherArgs(self, otherArgs={}):
		pass
