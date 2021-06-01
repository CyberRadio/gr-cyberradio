#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
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
import threading

import numpy
from gnuradio import gr

class py_peak_hold(gr.sync_block):
	"""
	docstring for block py_peak_hold
	"""
	def __init__(self, vecLen, clearEnable=False, otherArgs={}, debug=False):
		self.vecLen = vecLen
		gr.sync_block.__init__(self,
				name="py_peak_hold",
				in_sig=[(numpy.float32,vecLen),], 
				out_sig=[(numpy.float32,vecLen),],
				 )
		self._lock = threading.RLock()
	
	def start(self,):
		self.clearMax()
		return True
	
	def stop(self,):
		return True
	
	def clearMax(self, clearEnable=True):
		print(("clearMax( %r )"%(clearEnable,)))
		if clearEnable:
			with self._lock:
				self.maxVec = -numpy.inf*numpy.ones(self.vecLen)
				self.minVec = numpy.inf*numpy.ones(self.vecLen)
	
	def work(self, input_items, output_items):
		numOut = 0
		with self._lock:
			for i in range(len(input_items[0])):
				numOut += 1
				self.maxVec = numpy.maximum(input_items[0][i], self.maxVec)
				output_items[0][i] = self.maxVec.copy()
				#~ self.minVec = numpy.minimum(input_items[0][i], self.maxVec)
				#~ output_items[1][i] = self.minVec.copy()
		return numOut

