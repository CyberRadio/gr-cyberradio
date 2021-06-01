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

import numpy
from gnuradio import gr
from gnuradio.gr import pmt

from .generic_radio_control_block import generic_radio_control_block

class freq_msg_converter(generic_radio_control_block, gr.basic_block):
	"""
	docstring for block freq_msg_converter
	"""
	
	_portEnable_controlRx = False
	_portEnable_controlTx = False
	
	_portEnable_statusRx = False
	_portEnable_statusTx = False
	
	_portEnable_freqRx = True
	_portEnable_freqTx = True
	
	_portEnable_enableRx = False
	_portEnable_enableTx = False
	
	def __init__(self, msgKey="freq", unitsIn=1.0e6, unitsOut=1.0, offset=0.0, roundOutput=True, triggerOnChange=True, debug=False):
		self._name = "frqMsgCnv"
		self.debug = debug
		self.triggerOnChange = triggerOnChange
		self.roundOutput = roundOutput
		self.offset = numpy.float64(offset)
		self.unitsIn = numpy.float64(unitsIn)
		self.unitsOut = numpy.float64(unitsOut)
		self.msgKey = str(msgKey)
		self.freqIn = None
		gr.basic_block.__init__(self,
			name="freq_msg_converter",
			in_sig=None,
			out_sig=None, 
			 )
		generic_radio_control_block.__init__(self, radioObj=None, debug=debug)
	
	def set_unitsIn(self,arg):
		arg = numpy.float64(arg)
		if arg != self.unitsIn:
			self.unitsIn = arg
			if self.freqIn is not None and self.triggerOnChange:
				self.convertFreq()
	
	def set_unitsIn(self,arg):
		arg = numpy.float64(arg)
		if arg != self.unitsOut:
			self.unitsOut = arg
			if self.freqIn is not None and self.triggerOnChange:
				self.convertFreq()
	
	def set_offset(self,arg):
		arg = numpy.float64(arg)
		if arg != self.offset:
			self.offset = arg
			if self.freqIn is not None and self.triggerOnChange:
				self.convertFreq()
	
	def rxFreqMsg(self, msg):
		pyMsg = pmt.to_python(msg)
		self.log.debug("rxFreqMsg(%s)"%(repr(pyMsg)))
		freqIn = numpy.float64( pyMsg[-1] )
		if freqIn != self.freqIn:
			self.freqIn = freqIn
			self.convertFreq()
	
	def convertFreq(self,):
		freqOut = ((self.freqIn+self.offset)*self.unitsIn)/self.unitsOut
		if self.roundOutput:
			freqOut = numpy.round(freqOut)
		self.freqOut = freqOut
		self.log.debug("convertFreq ( ( %f + %f ) * %f ) / %f = %f"%(self.freqIn, self.offset, self.unitsIn, self.unitsOut,freqOut))
		self.txFreqMsg(self.msgKey, freqOut)
