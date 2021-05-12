##################################################
# GNU Radio Python Flow Graph
# Title: Sinad Calc Block
# Generated: Wed Apr 13 16:42:45 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio import blocks as grc_blks2
from numpy import pi,round
import math
import threading
import time


class sinad_calc_block(gr.hier_block2):

    def __init__(self, cutoffFreq=2**-6, freqUpdateRate=1.0, fs=1.0, isReal=False, notchFreq=0.0, rmsAvgExp=5, transBw=2.0**-8, useFreqEstimate=False):
        gr.hier_block2.__init__(
            self, "Sinad Calc Block",
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_float*1]),
            gr.io_signaturev(5, 5, [gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_gr_complex*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.cutoffFreq = cutoffFreq
        self.freqUpdateRate = freqUpdateRate
        self.fs = fs
        self.isReal = isReal
        self.notchFreq = notchFreq
        self.rmsAvgExp = rmsAvgExp
        self.transBw = transBw
        self.useFreqEstimate = useFreqEstimate

        ##################################################
        # Variables
        ##################################################
        self.freqEstQuery = freqEstQuery = 0.0
        self.estimatedFrequency = estimatedFrequency = round( fs*freqEstQuery )
        self.rotationFreq = rotationFreq = estimatedFrequency if useFreqEstimate else notchFreq
        self.useReal = useReal = bool(isReal)
        self.sinadLevel = sinadLevel = 0.0
        self.signalLevel = signalLevel = 0.0
        self.rotation = rotation = -2*pi*rotationFreq/fs
        self.rmsAvgGain = rmsAvgGain = 2.0**-rmsAvgExp
        self.noiseLevel = noiseLevel = 0.0

        ##################################################
        # Blocks
        ##################################################
        self.sinadProbe = blocks.probe_signal_f()
        self.signalProbe = blocks.probe_signal_f()
        self.noiseProbe = blocks.probe_signal_f()
        self.freqEstProbe = blocks.probe_signal_f()
        self.sinadLog10 = blocks.nlog10_ff(20, 1, 0)
        def _sinadLevel_probe():
            while True:
                val = self.sinadProbe.level()
                try:
                    self.set_sinadLevel(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (freqUpdateRate))
        _sinadLevel_thread = threading.Thread(target=_sinadLevel_probe)
        _sinadLevel_thread.daemon = True
        _sinadLevel_thread.start()
        self.sinadDivider = blocks.divide_ff(1)
        self.signalLevelRms = blocks.rms_cf(rmsAvgGain)
        self.signalLevelLog10 = blocks.nlog10_ff(20, 1, 0)
        def _signalLevel_probe():
            while True:
                val = self.signalProbe.level()
                try:
                    self.set_signalLevel(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (freqUpdateRate))
        _signalLevel_thread = threading.Thread(target=_signalLevel_probe)
        _signalLevel_thread.daemon = True
        _signalLevel_thread.start()
        self.rotatorBlock = blocks.rotator_cc(rotation)
        self.realOrIqSelector = grc_blks2.selector(
            item_size=gr.sizeof_gr_complex*1,
            num_inputs=2,
            num_outputs=1,
            input_index=1 if useReal else 0,
            output_index=0,
        )
        self.realHilbertFilter = filter.hilbert_fc(1025, firdes.WIN_KAISER, 6.76)
        self.noiseRms = blocks.rms_cf(rmsAvgGain)
        self.noiseLog10 = blocks.nlog10_ff(20, 1, 0)
        def _noiseLevel_probe():
            while True:
                val = self.noiseProbe.level()
                try:
                    self.set_noiseLevel(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (freqUpdateRate))
        _noiseLevel_thread = threading.Thread(target=_noiseLevel_probe)
        _noiseLevel_thread.daemon = True
        _noiseLevel_thread.start()
        self.highPassFilter = filter.fir_filter_ccf(1, firdes.high_pass(
            1, 1.0, cutoffFreq, transBw, firdes.WIN_KAISER, 6.76))
        self.freqEstScale = blocks.multiply_const_vff((fs, ))
        def _freqEstQuery_probe():
            while True:
                val = self.freqEstProbe.level()
                try:
                    self.set_freqEstQuery(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (freqUpdateRate))
        _freqEstQuery_thread = threading.Thread(target=_freqEstQuery_probe)
        _freqEstQuery_thread.daemon = True
        _freqEstQuery_thread.start()
        self.freqEstNullSink = blocks.null_sink(gr.sizeof_float*1)
        self.freqEstFilter = filter.single_pole_iir_filter_ff(2**-10, 1)
        self.freqEstDemod = analog.quadrature_demod_cf(1.0/(2*pi))
        self.derotatorBlock = blocks.rotator_cc(-1.0*rotation)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.derotatorBlock, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.derotatorBlock, 0), (self, 4))    
        self.connect((self.freqEstDemod, 0), (self.freqEstFilter, 0))    
        self.connect((self.freqEstFilter, 0), (self.freqEstProbe, 0))    
        self.connect((self.freqEstFilter, 0), (self.freqEstScale, 0))    
        self.connect((self.freqEstScale, 0), (self.freqEstNullSink, 0))    
        self.connect((self.freqEstScale, 0), (self, 3))    
        self.connect((self.highPassFilter, 0), (self.derotatorBlock, 0))    
        self.connect((self.highPassFilter, 0), (self.noiseRms, 0))    
        self.connect((self, 0), (self.realOrIqSelector, 0))    
        self.connect((self.noiseLog10, 0), (self.noiseProbe, 0))    
        self.connect((self.noiseLog10, 0), (self, 2))    
        self.connect((self.noiseRms, 0), (self.noiseLog10, 0))    
        self.connect((self.noiseRms, 0), (self.sinadDivider, 1))    
        self.connect((self.realHilbertFilter, 0), (self.realOrIqSelector, 1))    
        self.connect((self, 1), (self.realHilbertFilter, 0))    
        self.connect((self.realOrIqSelector, 0), (self.freqEstDemod, 0))    
        self.connect((self.realOrIqSelector, 0), (self.rotatorBlock, 0))    
        self.connect((self.realOrIqSelector, 0), (self.signalLevelRms, 0))    
        self.connect((self.rotatorBlock, 0), (self.highPassFilter, 0))    
        self.connect((self.signalLevelLog10, 0), (self, 1))    
        self.connect((self.signalLevelLog10, 0), (self.signalProbe, 0))    
        self.connect((self.signalLevelRms, 0), (self.signalLevelLog10, 0))    
        self.connect((self.signalLevelRms, 0), (self.sinadDivider, 0))    
        self.connect((self.sinadDivider, 0), (self.sinadLog10, 0))    
        self.connect((self.sinadLog10, 0), (self, 0))    
        self.connect((self.sinadLog10, 0), (self.sinadProbe, 0))    


    def get_cutoffFreq(self):
        return self.cutoffFreq

    def set_cutoffFreq(self, cutoffFreq):
        self.cutoffFreq = cutoffFreq
        self.highPassFilter.set_taps(firdes.high_pass(1, 1.0, self.cutoffFreq, self.transBw, firdes.WIN_KAISER, 6.76))

    def get_freqUpdateRate(self):
        return self.freqUpdateRate

    def set_freqUpdateRate(self, freqUpdateRate):
        self.freqUpdateRate = freqUpdateRate

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        if fs != self.fs:
            print("Setting fs: old=%r, new=%r"%(self.fs,fs))
            self.fs = fs
            self.set_estimatedFrequency(round( self.fs*self.freqEstQuery ))
            self.set_rotation(-2*pi*self.rotationFreq/self.fs)
            self.freqEstScale.set_k((self.fs, ))

    def get_isReal(self):
        return self.isReal

    def set_isReal(self, isReal):
        self.isReal = isReal
        self.set_useReal(bool(self.isReal))

    def get_notchFreq(self):
        return self.notchFreq

    def set_notchFreq(self, notchFreq):
        self.notchFreq = notchFreq
        self.set_rotationFreq(self.estimatedFrequency if self.useFreqEstimate else self.notchFreq)

    def get_rmsAvgExp(self):
        return self.rmsAvgExp

    def set_rmsAvgExp(self, rmsAvgExp):
        self.rmsAvgExp = rmsAvgExp
        self.set_rmsAvgGain(2.0**-self.rmsAvgExp)

    def get_transBw(self):
        return self.transBw

    def set_transBw(self, transBw):
        self.transBw = transBw
        self.highPassFilter.set_taps(firdes.high_pass(1, 1.0, self.cutoffFreq, self.transBw, firdes.WIN_KAISER, 6.76))

    def get_useFreqEstimate(self):
        return self.useFreqEstimate

    def set_useFreqEstimate(self, useFreqEstimate):
        self.useFreqEstimate = useFreqEstimate
        self.set_rotationFreq(self.estimatedFrequency if self.useFreqEstimate else self.notchFreq)

    def get_freqEstQuery(self):
        return self.freqEstQuery

    def set_freqEstQuery(self, freqEstQuery):
        self.freqEstQuery = freqEstQuery
        self.set_estimatedFrequency(round( self.fs*self.freqEstQuery ))

    def get_estimatedFrequency(self):
        return self.estimatedFrequency

    def set_estimatedFrequency(self, estimatedFrequency):
        self.estimatedFrequency = estimatedFrequency
        self.set_rotationFreq(self.estimatedFrequency if self.useFreqEstimate else self.notchFreq)

    def get_rotationFreq(self):
        return self.rotationFreq

    def set_rotationFreq(self, rotationFreq):
        self.rotationFreq = rotationFreq
        self.set_rotation(-2*pi*self.rotationFreq/self.fs)

    def get_useReal(self):
        return self.useReal

    def set_useReal(self, useReal):
        self.useReal = useReal
        self.realOrIqSelector.set_input_index(int(1 if self.useReal else 0))

    def get_sinadLevel(self):
        return self.sinadLevel

    def set_sinadLevel(self, sinadLevel):
        self.sinadLevel = sinadLevel

    def get_signalLevel(self):
        return self.signalLevel

    def set_signalLevel(self, signalLevel):
        self.signalLevel = signalLevel

    def get_rotation(self):
        return self.rotation

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.derotatorBlock.set_phase_inc(-1.0*self.rotation)
        self.rotatorBlock.set_phase_inc(self.rotation)

    def get_rmsAvgGain(self):
        return self.rmsAvgGain

    def set_rmsAvgGain(self, rmsAvgGain):
        self.rmsAvgGain = rmsAvgGain
        self.noiseRms.set_alpha(self.rmsAvgGain)
        self.signalLevelRms.set_alpha(self.rmsAvgGain)

    def get_noiseLevel(self):
        return self.noiseLevel

    def set_noiseLevel(self, noiseLevel):
        self.noiseLevel = noiseLevel

