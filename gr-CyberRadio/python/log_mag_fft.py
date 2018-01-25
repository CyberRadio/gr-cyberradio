#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
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

from gnuradio import blocks
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
from gnuradio.filter import firdes
import CyberRadio
import numpy, scipy.signal

class log_mag_fft(gr.hier_block2):
    """
    docstring for block log_mag_fft
    """
    def __init__(self, fftSize=1024, windowType="blackmanharris", iirAlpha=2.0**-3):
        gr.hier_block2.__init__(
            self, "LogMagFFT",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*fftSize),
            gr.io_signaturev(2, 2, [gr.sizeof_float*fftSize, gr.sizeof_gr_complex*fftSize]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.fftSize = fftSize
        self.iirAlpha = iirAlpha
        self.windowType = windowType

        ##################################################
        # Variables
        ##################################################
        self.fftWindow = fftWindow = scipy.signal.get_window(windowType, fftSize)

        ##################################################
        # Blocks
        ##################################################
        self.singlePoleIIR = filter.single_pole_iir_filter_ff(iirAlpha, fftSize)
        self.nLog10 = CyberRadio.vector_nlog10_ff(10, fftSize, 0)

        self.fwdFFT = fft.fft_vcc(fftSize, True, (fftWindow/numpy.sum(fftWindow)), True, 1)
        self.compToMagSq = blocks.complex_to_mag_squared(fftSize)

        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.fwdFFT, 0))
        self.connect((self.fwdFFT, 0), (self, 1))
        self.connect((self.fwdFFT, 0), (self.compToMagSq, 0))
        self.connect((self.compToMagSq, 0), (self.singlePoleIIR, 0))
        self.connect((self.singlePoleIIR, 0), (self.nLog10, 0))
        self.connect((self.nLog10, 0), (self, 0))

    def get_fftSize(self):
        return self.fftSize

#     def set_fftSize(self, fftSize):
#         self.fftSize = fftSize
#         self.set_fftWindow(scipy.signal.get_window(self.windowType, self.fftSize))

    def get_iirAlpha(self):
        return self.iirAlpha

    def set_iirAlpha(self, iirAlpha):
        self.iirAlpha = iirAlpha
        self.singlePoleIIR.set_taps(self.iirAlpha)

    def get_windowType(self):
        return self.windowType

#     def set_windowType(self, windowType):
#         self.windowType = windowType
#         self.set_fftWindow(scipy.signal.get_window(self.windowType, self.fftSize))
#
#     def get_fftWindow(self):
#         return self.fftWindow
# 
#     def set_fftWindow(self, fftWindow):
#         self.fftWindow = fftWindow
