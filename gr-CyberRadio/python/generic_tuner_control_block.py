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
from generic_radio_control_block import generic_radio_control_block


class generic_tuner_control_block(generic_radio_control_block, gr.basic_block):
	"""
	docstring for block generic_tuner_control_block
	"""
	_portEnable_freqRx = True
	_portEnable_freqTx = True
	
	def __init__(self, 
					radioObj,
					index=1,
					enable=True,
					freq=0,
					attenuation=0,
					filter=1,
					group=None,
					otherArgs={},
					debug=False, 
					autoStart = True, 
					 ):
		self._configParams = {"freq": self.set_freq, 
						"attenuation": self.set_attenuation, 
						 }
		self._init=True
		self._name = "Tuner%d_ctrl"%(index)
		self._debug = debug
		
		generic_radio_control_block.__init__(self, radioObj=radioObj, debug=debug)
		
		self.freqUnits = int(1e6)
		
		self.set_index(index)
		self.set_enable(enable)
		self.set_freq(freq)
		self.set_attenuation(attenuation)
		self.set_filter(filter)
		self.set_group(group)
		self.set_otherArgs(otherArgs)
		
		self.updateConfig()
		self._init = False

	def updateConfig(self,param=None):
		self.log.debug("%s.updateConfig( %s ), init=%s"%(self._name, param, self._init))
		confDict=None
		sendFreqMsg = False
		if (self._init and param is None) or ((not self._init) and (param=="index")):
			confDict = { crd.configKeys.CONFIG_TUNER: { self.index: {crd.configKeys.TUNER_FREQUENCY:int(self.rfFreq*1e6), 
																			crd.configKeys.TUNER_ATTENUATION:self.attenuation, 
																			crd.configKeys.TUNER_FILTER: self.filter, 
# 																			crd.configKeys.ENABLE: self.enable, 
																			 } } }
			if ( isinstance(self.group,int) and (self.group>=0) ):
				confDict[crd.configKeys.CONFIG_TUNER][self.index][crd.configKeys.TUNER_COHERENT_GROUP] = self.group
			sendFreqMsg = True
		elif not self._init:
			if param=="freq":
				confDict = { crd.configKeys.CONFIG_TUNER: { self.index: { crd.configKeys.TUNER_FREQUENCY:int(self.rfFreq*1e6), } } }
				sendFreqMsg = True
			elif param=="attenuation":
				confDict = { crd.configKeys.CONFIG_TUNER: { self.index: { crd.configKeys.TUNER_ATTENUATION:self.attenuation, } } }
			elif param=="filter":
				confDict = { crd.configKeys.CONFIG_TUNER: { self.index: { crd.configKeys.TUNER_FILTER: self.filter, } } }
			elif param=="group":
				confDict = { crd.configKeys.CONFIG_TUNER: { self.index: { crd.configKeys.TUNER_COHERENT_GROUP: self.group, } } }
			elif param=="enable":
				confDict = { crd.configKeys.CONFIG_TUNER: { self.index: { crd.configKeys.ENABLE: self.enable, } } }
		if confDict is not None:
			self.log.debug( json.dumps(confDict, sort_keys=True) )
			self.radioObj.setConfiguration(confDict)
		if sendFreqMsg:
			self.txFreqMsg("freq",self.freq*self.freqUnits)
	

	## Setter & getter for radioParam
	def set_radioParam(self, radioParam={"type":"ndr308","host":"ndr308","port":8617,"obj":None}):
		if self._init or not hasattr(self, "radioParam"):
			self.radioParam = radioParam
			self.log.debug("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
		elif radioParam!=self.radioParam:
			self.log.debug("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
			self.radioParam = radioParam
			self.updateConfig("radioParam")

	def get_radioParam(self,):
		return self.radioParam

	## Setter & getter for index
	def set_index(self, index=1):
		if self._init or not hasattr(self, "index"):
			self.index = index
			self.log.debug("%s.set_index: %s -> %s"%(self._name, repr(self.index), repr(index),))
		elif index!=self.index:
			self.log.debug("%s.set_index: %s -> %s"%(self._name, repr(self.index), repr(index),))
			self.index = index
			self.updateConfig("index")

	def get_index(self,):
		return self.index

	## Setter & getter for enable
	def set_enable(self, enable=True):
		if self._init or not hasattr(self, "enable"):
			self.enable = enable
			self.log.debug("%s.set_enable: %s -> %s"%(self._name, repr(self.enable), repr(enable),))
		elif enable!=self.enable:
			self.log.debug("%s.set_enable: %s -> %s"%(self._name, repr(self.enable), repr(enable),))
			self.enable = enable
			self.updateConfig("enable")

	def get_enable(self,):
		return self.enable

	## Setter & getter for freq
	def set_freq(self, freq=0):
		if self._init or not hasattr(self, "freq"):
			self.freq = freq
			self.rfFreq = self.freq*self.freqUnits/int(1e6)
			self.log.debug("%s.set_freq: %s -> %s"%(self._name, repr(self.freq), repr(freq),))
		elif freq!=self.freq:
			self.log.debug("%s.set_freq: %s -> %s"%(self._name, repr(self.freq), repr(freq),))
			self.freq = freq
			self.rfFreq = self.freq*self.freqUnits/int(1e6)
			self.updateConfig("freq")
	
	def get_freq(self,):
		return self.freq

	## Setter & getter for attenuation
	def set_attenuation(self, attenuation=0):
		print "set_attenuation( {0} )".format(attenuation)
		if self._init or not hasattr(self, "attenuation"):
			self.attenuation = attenuation
			self.log.debug("%s.set_attenuation: %s -> %s"%(self._name, repr(self.attenuation), repr(attenuation),))
		elif attenuation!=self.attenuation:
			self.log.debug("%s.set_attenuation: %s -> %s"%(self._name, repr(self.attenuation), repr(attenuation),))
			self.attenuation = attenuation
			self.updateConfig("attenuation")

	def get_attenuation(self,):
		return self.attenuation

	## Setter & getter for filter
	def set_filter(self, filter=1):
		if self._init or not hasattr(self, "filter"):
			self.filter = filter
			self.log.debug("%s.set_filter: %s -> %s"%(self._name, repr(self.filter), repr(filter),))
		elif filter!=self.filter:
			self.log.debug("%s.set_filter: %s -> %s"%(self._name, repr(self.filter), repr(filter),))
			self.filter = filter
			self.updateConfig("filter")

	def get_filter(self,):
		return self.filter

	## Setter & getter for otherArgs
	def set_otherArgs(self, otherArgs={}):
		self.freqUnits = otherArgs.get("freqUnits", self.freqUnits)
		self.tunerGroup = otherArgs.get("group", None)

	def get_otherArgs(self,):
		return self.otherArgs
	
	def set_group(self, group):
		if self._init or not hasattr(self, "group"):
			self.group = group
			self.log.debug("%s.set_group: %s -> %s"%(self._name, repr(self.group), repr(group),))
		elif group!=self.group:
			self.log.debug("%s.set_group: %s -> %s"%(self._name, repr(self.group), repr(group),))
			self.filter = filter
			self.updateConfig("group")
	
	def rxFreqMsg(self, msg):
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxFreqMsg(%s)"%(repr(pyMsg)))
		if (len(pyMsg)==2) and (pyMsg[0]=="freq"):
			self.set_freq(pyMsg[1]/self.freqUnits)

#   def forecast(self, noutput_items, ninput_items_required):
#	   #setup size of input_items[i] for work call
#	   for i in range(len(ninput_items_required)):
#		   ninput_items_required[i] = noutput_items
# 
#   def general_work(self, input_items, output_items):
#	   output_items[0][:] = input_items[0]
#	   consume(0, len(input_items[0]))
#	   #self.consume_each(len(input_items[0]))
#	   return len(output_items[0])
