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
    def __init__(self,
                    numInputs=1,
                    fftSize=1024,
                    windowType="blackmanharris",
                    iirAlpha=2.0**-3,
                    secondaryOutput="fft",
                    resetOnAlphaChange = False,
                    magSquared = True,
                     ):

        numOutput = numInputs
        outSig = [gr.sizeof_float*fftSize,]*numInputs
        connectFft = False
        connectMagFiltered = False
        connectMagUnfiltered = False
        connectLogMagUnfiltered = False
        if secondaryOutput=="fft":
            numOutput *= 2
            outSig += [gr.sizeof_gr_complex*fftSize,]*numInputs
            connectFft = True
        elif secondaryOutput=="mag_filtered":
            numOutput *= 2
            outSig += [gr.sizeof_float*fftSize,]*numInputs
            connectMagFiltered = True
        elif secondaryOutput=="mag_unfiltered":
            numOutput *= 2
            outSig += [gr.sizeof_float*fftSize,]*numInputs
            connectMagUnfiltered = True
        elif secondaryOutput=="log_mag_unfiltered":
            numOutput *= 2
            outSig += [gr.sizeof_float*fftSize,]*numInputs
            connectLogMagUnfiltered = True
        else:
            pass

        gr.hier_block2.__init__(
            self, "LogMagFFT",
            gr.io_signaturev(numInputs, numInputs, [gr.sizeof_gr_complex*fftSize,]*numInputs),
            gr.io_signaturev(numOutput, numOutput, outSig),
        )

        self.message_port_register_hier_in("reset")

        ##################################################
        # Parameters
        ##################################################
        self.fftSize = fftSize
        self.iirAlpha = iirAlpha
        self.windowType = windowType
        self.resetOnAlphaChange = resetOnAlphaChange
        self.magSquared = magSquared
        self.nLog10_n = 10 if self.magSquared else 20

        ##################################################
        # Variables
        ##################################################
        self.fftWindow = fftWindow = scipy.signal.get_window(windowType, fftSize)

        ##################################################
        # Blocks
        ##################################################
        self.nLog10=[CyberRadio.vector_nlog10_ff(self.nLog10_n, fftSize, 0) for i in range(numInputs)]
        if connectLogMagUnfiltered:
            self.nLog10 += [CyberRadio.vector_nlog10_ff(self.nLog10_n, fftSize, 0) for i in range(numInputs)]
        if iirAlpha is not None:
            self.singlePoleIIR=[CyberRadio.single_pole_iir_filter_ff(iirAlpha, fftSize, resetOnAlphaChange) for i in range(numInputs)]
        else:
            self.singlePoleIIR = None
        if self.magSquared:
            self.compToMag=[blocks.complex_to_mag_squared(fftSize) for i in range(numInputs)]
        else:
            self.compToMag=[blocks.complex_to_mag(fftSize) for i in range(numInputs)]
        self.fwdFFT=[fft.fft_vcc(fftSize, True, (fftWindow/numpy.sum(fftWindow)), True, 1) for i in range(numInputs)]

        ##################################################
        # Connections
        ##################################################
        for i in range(numInputs):
            self.connect((self, i), (self.fwdFFT[i], 0))
            self.connect((self.fwdFFT[i], 0), (self.compToMag[i], 0))
            if self.singlePoleIIR is not None:
                self.msg_connect((self,"reset"), (self.singlePoleIIR[i],"reset"))
                self.connect((self.compToMag[i], 0), (self.singlePoleIIR[i], 0))
                self.connect((self.singlePoleIIR[i], 0), (self.nLog10[i], 0))
            else:
                self.connect((self.compToMag[i], 0), (self.nLog10[i], 0))
            self.connect((self.nLog10[i], 0), (self, i))
            if connectFft:
                self.connect((self.fwdFFT[i], 0), (self, i+numInputs))
            elif connectMagFiltered:
                if self.singlePoleIIR is not None:
                    self.connect((self.singlePoleIIR[i], 0), (self, i+numInputs))
                else:
                    self.connect((self.compToMag[i], 0), (self, i+numInputs))
            elif connectMagUnfiltered:
                self.connect((self.compToMag[i], 0), (self, i+numInputs))
            elif connectLogMagUnfiltered:
                self.connect((self.compToMag[i], 0), (self.nLog10[i+numInputs], 0))
                self.connect((self.nLog10[i+numInputs], 0), (self, i+numInputs))

    def get_fftSize(self):
        return self.fftSize

    def get_iirAlpha(self):
        return self.iirAlpha

    def set_iirAlpha(self, iirAlpha):
        if self.singlePoleIIR is not None:
            self.iirAlpha = iirAlpha
            res = [i.set_taps(self.iirAlpha) for i in self.singlePoleIIR]

    def get_windowType(self):
        return self.windowType
