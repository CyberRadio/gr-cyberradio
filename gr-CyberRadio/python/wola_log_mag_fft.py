#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 G3 Technologies, Inc..
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

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import CyberRadio
import scipy.signal

class wola_log_mag_fft(gr.hier_block2):
    """
    docstring for block wola_log_mag_fft
    """
    def __init__(self, avg_alpha=2.0**-3.25, fft_size=int(2**10), n_overlap=4, window_type="blackmanharris"):
        gr.hier_block2.__init__(
            self, "[CyberRadio] WOLA FFT (Local)",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*fft_size*n_overlap),
            gr.io_signaturev(4, 4, [gr.sizeof_float*fft_size, gr.sizeof_float*fft_size, gr.sizeof_float*fft_size, gr.sizeof_float*fft_size]),
        )
        self.message_port_register_hier_in("reset")

        self._lock = threading.RLock()

        ##################################################
        # Parameters
        ##################################################
        self.avg_alpha = avg_alpha
        self.fft_size = fft_size
        self.n_overlap = n_overlap
        self.window_type = window_type

        ##################################################
        # Variables
        ##################################################
        self.fftSize = fftSize = int(fft_size)
        self.N = N = int(n_overlap)
        self.windowType = windowType = str(window_type)
        self.inputSize = inputSize = fftSize*N
        self.fftWindow = fftWindow = scipy.signal.get_window(windowType, inputSize)
        self.fftWindowEnergy = fftWindowEnergy = fftWindow.sum()
        self.fftWindowScale = fftWindowScale = fftWindowEnergy/(fftSize*N)
        self.avgAlpha = avgAlpha = float(avg_alpha)

        ##################################################
        # Blocks
        ##################################################
        self.vecToStreams = blocks.vector_to_streams(gr.sizeof_gr_complex*fftSize, N)
        self.nullSink_wola = blocks.null_sink(gr.sizeof_float*fftSize)
        self.nullSink_small = blocks.null_sink(gr.sizeof_float*fftSize)
        # self.nullSink_large = blocks.null_sink(gr.sizeof_float*inputSize)
        self.multiplyConstant = []
        for n in range(self.N):
            self.multiplyConstant.append(blocks.multiply_const_vcc((fftWindow[n*fftSize:(n+1)*fftSize]/fftWindowScale)))
        self.logMagFFT_wola = CyberRadio.log_mag_fft(
            numInputs=1,
            fftSize=fftSize,
            windowType="boxcar",
            iirAlpha=avgAlpha,
            secondaryOutput="mag_filtered",
            resetOnAlphaChange=False,
             )
        self.logMagFFT_small = CyberRadio.log_mag_fft(
            numInputs=1,
            fftSize=fftSize,
            windowType=windowType,
            iirAlpha=avgAlpha,
            secondaryOutput="mag_filtered",
            resetOnAlphaChange=False,
             )
        # self.logMagFFT_large = CyberRadio.log_mag_fft(
        #     numInputs=1,
        #     fftSize=inputSize,
        #     windowType=windowType,
        #     iirAlpha=avgAlpha,
        #     secondaryOutput="mag_filtered",
        #     resetOnAlphaChange=False,
        #      )
        self.adder = blocks.add_vcc(fftSize)



        ##################################################
        # Connections
        ##################################################
        # self.msg_connect((self, 'reset'), (self.logMagFFT_large, 'reset'))
        self.msg_connect((self, 'reset'), (self.logMagFFT_small, 'reset'))
        self.msg_connect((self, 'reset'), (self.logMagFFT_wola, 'reset'))
        self.connect((self.adder, 0), (self.logMagFFT_wola, 0))
        # self.connect((self.logMagFFT_large, 0), (self.nullSink_large, 0))
        # self.connect((self.logMagFFT_large, 1), (self.nullSink_large, 1))
        # self.connect((self.logMagFFT_large, 0), (self, 4))
        self.connect((self.logMagFFT_small, 0), (self.nullSink_small, 0))
        self.connect((self.logMagFFT_small, 1), (self.nullSink_small, 1))
        self.connect((self.logMagFFT_small, 0), (self, 2))
        self.connect((self.logMagFFT_small, 1), (self, 3))
        self.connect((self.logMagFFT_wola, 0), (self.nullSink_wola, 0))
        self.connect((self.logMagFFT_wola, 1), (self.nullSink_wola, 1))
        self.connect((self.logMagFFT_wola, 0), (self, 0))
        self.connect((self.logMagFFT_wola, 1), (self, 1))
        for n in range(self.N):
            self.connect((self.vecToStreams, n), (self.multiplyConstant[n], 0))
            self.connect((self.multiplyConstant[n], 0), (self.adder, n))
        # self.connect((self, 0), (self.logMagFFT_large, 0))
        self.connect((self, 0), (self.vecToStreams, 0))
        self.connect((self.vecToStreams, 0), (self.logMagFFT_small, 0))

    def get_avg_alpha(self):
        return self.avg_alpha

    def set_avg_alpha(self, avg_alpha):
        with self._lock:
            self.avg_alpha = avg_alpha
            self.set_avgAlpha(float(self.avg_alpha))

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        with self._lock:
            self.fft_size = fft_size
            self.set_fftSize(int(self.fft_size))

    def get_n_overlap(self):
        return self.n_overlap

    def set_n_overlap(self, n_overlap):
        with self._lock:
            self.n_overlap = n_overlap
            self.set_N(int(self.n_overlap))

    def get_window_type(self):
        return self.window_type

    def set_window_type(self, window_type):
        with self._lock:
            self.window_type = window_type
            self.set_windowType(str(self.window_type))

    def get_fftSize(self):
        return self.fftSize

    def set_fftSize(self, fftSize):
        with self._lock:
            self.fftSize = fftSize
            self.set_inputSize(self.fftSize*self.N)
            self.set_fftWindowScale(self.fftWindowEnergy/self.fftSize)
            for i,j in enumerate(self.multiplyConstant):
                print(("set_fftSize for multiplier %d"%(i,)))
                j.set_k((self.fftWindow[i*self.fftSize:(i+1)*self.fftSize]/self.fftWindowScale))

    def get_N(self):
        return self.N

    def set_N(self, N):
        with self._lock:
            self.N = N
            self.set_fftWindowScale(self.fftWindowEnergy/(self.fftSize*self.N))
            self.set_inputSize(self.fftSize*self.N)

    def get_windowType(self):
        return self.windowType

    def set_windowType(self, windowType):
        with self._lock:
            self.windowType = windowType
            self.set_fftWindow(scipy.signal.get_window(self.windowType, self.inputSize))

    def get_inputSize(self):
        return self.inputSize

    def set_inputSize(self, inputSize):
        with self._lock:
            self.inputSize = inputSize
            self.set_fftWindow(scipy.signal.get_window(self.windowType, self.inputSize))

    def get_fftWindow(self):
        return self.fftWindow

    def set_fftWindow(self, fftWindow):
        with self._lock:
            self.fftWindow = fftWindow
            for i,j in enumerate(self.multiplyConstant):
                print(("set_fftWindow for multiplier %d"%(i,)))
                j.set_k((self.fftWindow[i*self.fftSize:(i+1)*self.fftSize]/self.fftWindowScale))

    def get_fftWindowEnergy(self):
        return self.fftWindowEnergy

    def set_fftWindowEnergy(self, fftWindowEnergy):
        with self._lock:
            self.fftWindowEnergy = fftWindowEnergy
            self.set_fftWindowScale(self.fftWindowEnergy/(self.fftSize*self.N))

    def get_fftWindowScale(self):
        return self.fftWindowScale

    def set_fftWindowScale(self, fftWindowScale):
        with self._lock:
            self.fftWindowScale = fftWindowScale
            for i,j in enumerate(self.multiplyConstant):
                print(("set_fftWindowScale for multiplier %d"%(i,)))
                j.set_k((self.fftWindow[i*self.fftSize:(i+1)*self.fftSize]/self.fftWindowScale))

    def get_avgAlpha(self):
        return self.avgAlpha

    def set_avgAlpha(self, avgAlpha):
        with self._lock:
            self.avgAlpha = avgAlpha
            self.logMagFFT_wola.set_iirAlpha(self.avgAlpha)
            self.logMagFFT_small.set_iirAlpha(self.avgAlpha)
            # self.logMagFFT_large.set_iirAlpha(self.avgAlpha)
