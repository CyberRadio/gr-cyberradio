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
import time

from gnuradio import gr
from gnuradio.gr import pmt
import threading

from .generic_radio_control_block import generic_radio_control_block


class freq_msg_strobe(generic_radio_control_block,gr.basic_block):
	"""
	docstring for block freq_msg_strobe
	"""
	
	_portEnable_controlRx = False
	_portEnable_controlTx = False
	
	_portEnable_statusRx = False
	_portEnable_statusTx = False
	
	_portEnable_freqRx = True
	_portEnable_freqTx = True
	
	_portEnable_enableRx = False
	_portEnable_enableTx = False

	
	def __init__(self, pause, f1, f2, step, dwell, wrap, fManual, msgUnits, msgRes, debug):
		
		self._name = "FrqScanMsg"
		generic_radio_control_block.__init__(self, radioObj=None, debug=debug)
		
		self.msgThread = None
		self._keepScanning = False
		self._scanning = False
		
		self.pause = pause
		self.f1 = f1
		self.f2 = f2
		self.step = step
		self.dwell = dwell
		self.fManual = fManual
		self.msgUnits = msgUnits
		self.msgRes = msgRes
		self.wrap = wrap
		
		self.setFreqList()
	
	def setFreqList(self,):
		self.log.debug("setFreqList")
		self._freqList = numpy.arange(self.f1, self.f2, self.step).tolist()
		self._currentFreq = None

	def start(self,):
		self.log.debug("start")
		self.startScanThread()
		if self.pause and self.fManual is not None:
			self.log.debug("self.pause (%r) and self.fManual is not None (%r) = %r"%(self.pause, self.fManual is not None,self.pause and self.fManual is not None))
			self.sendFreqMsg(self.fManual)
		return True
	
	def stop(self,):
		self.log.debug("stop")
		self.stopScanThread()
		return True
	
	def set_f1(self, arg):
		if self.f1 != arg:
			self.log.debug("set_f1: %r -> %r"%(self.f1,arg))
			self.f1 = arg
			self.restartScanThread()
	
	def set_f2(self, arg):
		if self.f2 != arg:
			self.log.debug("set_f2: %r -> %r"%(self.f2,arg))
			self.f2 = arg
			self.restartScanThread()
	
	def set_fManual(self, arg):
		if self.fManual != arg:
			self.log.debug("set_fManual: %r -> %r"%(self.fManual,arg))
			self.fManual = arg
			if self.fManual is not None and self.pause:
				self.sendFreqMsg(self.fManual)
	
	def set_step(self, arg):
		if self.step != arg:
			self.log.debug("set_step: %r -> %r"%(self.step,arg))
			self.step = arg
			self.restartScanThread()
	
	def set_dwell(self, arg):
		if self.dwell != arg:
			self.log.debug("set_dwell: %r -> %r"%(self.dwell,arg))
			self.dwell = arg
	
	def set_pause(self, arg):
		if self.pause != arg:
			self.log.debug("set_pause: %r -> %r"%(self.pause,arg))
			self.pause = arg
			if not self._scanning:
				if self.pause:
					if self.fManual is not None:
						self.sendFreqMsg(self.fManual)
				else:
					self.restartScanThread()
	
	def startScanThread(self,):
		self.log.debug("startScanThread")
		self._keepScanning = True
		self.msgThread = threading.Thread(target=self.scanThread)
		self.msgThread.start()
	
	def stopScanThread(self,):
		self.log.debug("stopScanThread")
		self._keepScanning = False
		if self.msgThread is not None:
			self.log.debug("Joining msg thread...")
			self.msgThread.join()
	
	def restartScanThread(self,):
		self.log.debug("restartScanThread")
		self.stopScanThread()
		self.setFreqList()
		self.startScanThread()
	
	def scanThread(self,):
		self.log.debug("scan thread starting")
		self._scanning = True
		while self._keepScanning and ( len(self._freqList)>0 ):
			self.log.debug("_keepScanning")
			## interruptible pause
			while self._keepScanning and self.pause:
				time.sleep(0.001)
			## exit after pause
			if not self._keepScanning:
				break
			## reload frequency list if it's empty
			self.log.debug("next freq")
			self._currentFreq = self._freqList.pop(0)
			self.sendFreqMsg(self._currentFreq)
			numSleeps = int( numpy.round( float(self.dwell)/0.001 ) )
			for i in range(numSleeps):
				time.sleep(0.001)
				if not self._keepScanning:
					break
			
			if len(self._freqList)==0 and self.wrap:
				self.setFreqList()
		self._scanning = False
		self.log.debug("scan thread finished")
	
	def sendFreqMsg(self,freqVal):
		self.log.debug("sendFreqMsg %r"%(freqVal))
		freq = numpy.round( freqVal*1e6 )
		self.log.debug("sendFreqMsg %r"%(freq))
		freq = numpy.round( (freqVal*1e6), -int(numpy.floor(numpy.log10(self.msgRes))) )/self.msgUnits
		self.log.debug("sendFreqMsg %r"%(freq))
		self.txFreqMsg("freq",freq)















