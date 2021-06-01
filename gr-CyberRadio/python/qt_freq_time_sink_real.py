##################################################
# GNU Radio Python Flow Graph
# Title: Freq and Time Sink (Real)
# Author: NH
# Generated: Wed Mar 30 09:37:42 2016
##################################################

from PyQt5 import Qt
#from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
import sip
import threading
import time
import numpy, traceback

class qt_freq_time_sink_real(gr.hier_block2, Qt.QWidget):

    def __init__(self, 
                    label="Real", 
                    sampRate=1.0, 
                    centerFreq=0.0,
                    fftPlotRange=[-120,0], 
                    fftSizeN=10, 
                    rmsGainRange=[0,11], 
                    enableSpectrum=True, 
                    enableTimeWaveform=True, 
                    enableWaterfall=True, 
                    enableRssiDisplay=True, 
                    enableRssi=True, 
                    fftGainLog=0.0, 
                    rssiPollRate=1.0, 
                    updatePeriod=0.1, 
                    rmsAvgGainExpInit=5, 
                    hilbertFilterLength=10, 
                     ):
        gr.hier_block2.__init__(
            self, "Freq and Time Sink (%s)"%(label,),
            gr.io_signature(1, 1, gr.sizeof_float*1),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_out("freq")
        self.message_port_register_hier_in("freq")

        Qt.QWidget.__init__(self)
        self.top_layout = Qt.QVBoxLayout()
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)
        self.setLayout(self.top_layout)

        self._lock = threading.RLock()

        ##################################################
        # Parameters
        ##################################################
        self.centerFreq = centerFreq
        self.enableRssiDisplay = enableRssiDisplay and enableRssi
        self.enableRssi = enableRssi
        self.enableSpectrum = enableSpectrum
        self.enableTimeWaveform = enableTimeWaveform
        self.enableWaterfall = enableWaterfall
        self.fftGainLog = fftGainLog
        self.fftPlotRange = fftPlotRange
        self.fftSizeN = fftSizeN
        self.hilbertFilterLength = hilbertFilterLength
        self.label = label
        self.rmsGainRange = rmsGainRange
        self.rssiPollRate = rssiPollRate
        self.sampRate = sampRate
        self.updatePeriod = updatePeriod

        ##################################################
        # Variables
        ##################################################
        self.rssi = rssi = "n/a"
        self.rmsAvgGainExp = rmsAvgGainExp = rmsAvgGainExpInit
        self.hilbertLen = hilbertLen = int(2**hilbertFilterLength)+1
        self.fftSize = fftSize = int(2**fftSizeN)
        self.fftGainLinear = fftGainLinear = 10.0**( float(fftGainLog)/20 )
        self.N = N = int(sampRate*updatePeriod)

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        
        if self.enableTimeWaveform:
            self.tabs_widget_0 = Qt.QWidget()
            self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
            self.tabs_grid_layout_0 = Qt.QGridLayout()
            self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
            self.tabs.addTab(self.tabs_widget_0, "%s Time Waveform"%(label,))
        
        if self.enableSpectrum:
            self.tabs_widget_1 = Qt.QWidget()
            self.tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_1)
            self.tabs_grid_layout_1 = Qt.QGridLayout()
            self.tabs_layout_1.addLayout(self.tabs_grid_layout_1)
            self.tabs.addTab(self.tabs_widget_1, "%s Spectrum"%(label,))
        
        if self.enableWaterfall:
            self.tabs_widget_2 = Qt.QWidget()
            self.tabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_2)
            self.tabs_grid_layout_2 = Qt.QGridLayout()
            self.tabs_layout_2.addLayout(self.tabs_grid_layout_2)
            self.tabs.addTab(self.tabs_widget_2, "%s Waterfall"%(label,))
        
        self.top_grid_layout.addWidget(self.tabs, 0,0,1,2)
        
        if self.enableRssiDisplay:
            self._rmsAvgGainExp_range = Range(rmsGainRange[0], rmsGainRange[1], 1, rmsAvgGainExp, 200)
            self._rmsAvgGainExp_win = RangeWidget(self._rmsAvgGainExp_range, self.set_rmsAvgGainExp, "Avg\nGain\n2^-[%s]"%( ",".join(str(i) for i in rmsGainRange) ), "dial", float)
            self.top_grid_layout.addWidget(self._rmsAvgGainExp_win, 1,1,1,1)
        
        if self.enableWaterfall:
            self.waterfallSink = qtgui.waterfall_sink_f(
                1024, #size
                firdes.WIN_BLACKMAN_hARRIS, #wintype
                centerFreq, #fc
                sampRate, #bw
                "", #name
                    1 #number of inputs
            )
            self.waterfallSink.set_update_time(updatePeriod)
            self.waterfallSink.enable_grid(True)
            
            if not True:
              self.waterfallSink.disable_legend()
            
            if float == type(float()):
              self.waterfallSink.set_plot_pos_half(not False)
            
            labels = ["", "", "", "", "",
                      "", "", "", "", ""]
            colors = [0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0]
            alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                      1.0, 1.0, 1.0, 1.0, 1.0]
            for i in range(1):
                if len(labels[i]) == 0:
                    self.waterfallSink.set_line_label(i, "Data {0}".format(i))
                else:
                    self.waterfallSink.set_line_label(i, labels[i])
                self.waterfallSink.set_color_map(i, colors[i])
                self.waterfallSink.set_line_alpha(i, alphas[i])
            
            self.waterfallSink.set_intensity_range(fftPlotRange[0]+20, fftPlotRange[1])
            
            self._waterfallSink_win = sip.wrapinstance(self.waterfallSink.pyqwidget(), Qt.QWidget)
            self.tabs_grid_layout_2.addWidget(self._waterfallSink_win, 0,0,1,1)
        
        if self.enableTimeWaveform:
            numInput = 2 if self.enableRssi else 1
            self.timeSink = qtgui.time_sink_f(
                fftSize, #size
                sampRate, #samp_rate
                "", #name
                numInput, #number of inputs
            )
            self.timeSink.set_update_time(updatePeriod)
            self.timeSink.set_y_axis(-1, 1)
            
            self.timeSink.set_y_label("Amplitude", "")
            
            self.timeSink.enable_tags(-1, True)
            self.timeSink.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
            self.timeSink.enable_autoscale(True)
            self.timeSink.enable_grid(True)
            self.timeSink.enable_control_panel(False)
            
            if not False:
                self.timeSink.disable_legend()
            
            labels = ["I", "Q", "", "", "",
                      "", "", "", "", ""]
            widths = [1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1]
            colors = ["blue", "green", "green", "black", "cyan",
                      "magenta", "yellow", "dark red", "dark green", "blue"]
            styles = [1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1]
            markers = [-1, -1, -1, -1, -1,
                       -1, -1, -1, -1, -1]
            alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                      1.0, 1.0, 1.0, 1.0, 1.0]
            
            for i in range(numInput):
                if len(labels[i]) == 0:
                    self.timeSink.set_line_label(i, "Data {0}".format(i))
                else:
                    self.timeSink.set_line_label(i, labels[i])
                self.timeSink.set_line_width(i, widths[i])
                self.timeSink.set_line_color(i, colors[i])
                self.timeSink.set_line_style(i, styles[i])
                self.timeSink.set_line_marker(i, markers[i])
                self.timeSink.set_line_alpha(i, alphas[i])
            
            self._timeSink_win = sip.wrapinstance(self.timeSink.pyqwidget(), Qt.QWidget)
            self.tabs_layout_0.addWidget(self._timeSink_win)
        
        
        if self.enableRssi:
            self.rmsCalc = blocks.rms_cf(2**-rmsAvgGainExp)
            self.nLog10 = blocks.nlog10_ff(20, 1, 0)
            self.keepOneInN = blocks.keep_one_in_n(gr.sizeof_float*1, N if N>0 else 1)
            self.rssiProbe = blocks.probe_signal_f()
            self.hilbertFilter = filter.hilbert_fc(hilbertLen, firdes.WIN_KAISER, 6.76)
            def _rssi_probe():
                while True:
                    val = self.rssiProbe.level()
                    try:
                        self.set_rssi(val)
                    except AttributeError:
                        pass
                    time.sleep(1.0 / (rssiPollRate))
            _rssi_thread = threading.Thread(target=_rssi_probe)
            _rssi_thread.daemon = True
            _rssi_thread.start()
        
        if self.enableRssiDisplay:
            self.numberSInk = qtgui.number_sink(
                    gr.sizeof_float,
                    0,
                    qtgui.NUM_GRAPH_HORIZ,
                1
            )
            self.numberSInk.set_update_time(updatePeriod)
            self.numberSInk.set_title("")
            
            labels = ["\n".join( (label,"RMS Mag") ), "NBDDC", "", "", "",
                      "", "", "", "", ""]
            units = ["dBfs", "dBfs", "", "", "",
                      "", "", "", "", ""]
            colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                      ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
            factor = [1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1]
            for i in range(1):
                self.numberSInk.set_min(i, fftPlotRange[0])
                self.numberSInk.set_max(i, fftPlotRange[1])
                self.numberSInk.set_color(i, colors[i][0], colors[i][1])
                if len(labels[i]) == 0:
                    self.numberSInk.set_label(i, "Data {0}".format(i))
                else:
                    self.numberSInk.set_label(i, labels[i])
                self.numberSInk.set_unit(i, units[i])
                self.numberSInk.set_factor(i, factor[i])
            
            self.numberSInk.enable_autoscale(False)
            self._numberSInk_win = sip.wrapinstance(self.numberSInk.pyqwidget(), Qt.QWidget)
            self.top_grid_layout.addWidget(self._numberSInk_win, 1,0,1,1)
        
        if self.enableSpectrum:
            self.freqSink = qtgui.freq_sink_f(
                fftSize, #size
                firdes.WIN_BLACKMAN_hARRIS, #wintype
                centerFreq, #fc
                sampRate, #bw
                "", #name
                1 #number of inputs
            )
            self.freqSink.set_update_time(updatePeriod)
            self.freqSink.set_y_axis(fftPlotRange[0], fftPlotRange[1])
            self.freqSink.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
            self.freqSink.enable_autoscale(False)
            self.freqSink.enable_grid(True)
            self.freqSink.set_fft_average(1.0)
            self.freqSink.enable_control_panel(False)
            
            if not True:
              self.freqSink.disable_legend()
            
            if float == type(float()):
              self.freqSink.set_plot_pos_half(not False)
            
            labels = ["", "", "", "", "",
                      "", "", "", "", ""]
            widths = [1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1]
            colors = ["blue", "red", "green", "black", "cyan",
                      "magenta", "yellow", "dark red", "dark green", "dark blue"]
            alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                      1.0, 1.0, 1.0, 1.0, 1.0]
            for i in range(1):
                if len(labels[i]) == 0:
                    self.freqSink.set_line_label(i, "Data {0}".format(i))
                else:
                    self.freqSink.set_line_label(i, labels[i])
                self.freqSink.set_line_width(i, widths[i])
                self.freqSink.set_line_color(i, colors[i])
                self.freqSink.set_line_alpha(i, alphas[i])
            
            self._freqSink_win = sip.wrapinstance(self.freqSink.pyqwidget(), Qt.QWidget)
            self.tabs_grid_layout_1.addWidget(self._freqSink_win, 0,0,1,2)
        
        if self.enableSpectrum or self.enableWaterfall:
            self.fftGainMultiplier = blocks.multiply_const_vff((fftGainLinear, ))
            _fftsize_probe_thread = threading.Thread(target=self.checkFftScale)
            _fftsize_probe_thread.daemon = True
            _fftsize_probe_thread.start()
        
        ##################################################
        # Connections
        ##################################################
        if self.enableSpectrum or self.enableWaterfall:
            self.connect((self, 0), (self.fftGainMultiplier, 0))   
        if self.enableSpectrum:
            self.connect((self.fftGainMultiplier, 0), (self.freqSink, 0)) 
            self.msg_connect((self, 'freq'), (self.freqSink, 'freq'))    
            self.msg_connect((self.freqSink, 'freq'), (self, 'freq'))    
        if self.enableWaterfall:
            self.connect((self.fftGainMultiplier, 0), (self.waterfallSink, 0))    
            self.msg_connect((self, 'freq'), (self.waterfallSink, 'freq'))    
        if self.enableRssi:
            self.connect((self, 0), (self.hilbertFilter, 0))    
            self.connect((self.hilbertFilter, 0), (self.rmsCalc, 0))    
            self.connect((self.rmsCalc, 0), (self.keepOneInN, 0))   
            self.connect((self.keepOneInN, 0), (self.nLog10, 0))    
            self.connect((self.nLog10, 0), (self.rssiProbe, 0))    
            if self.enableRssiDisplay:
                self.connect((self.nLog10, 0), (self.numberSInk, 0))    
            if self.enableTimeWaveform:
                self.connect((self.rmsCalc, 0), (self.timeSink, 1))    
        if self.enableTimeWaveform:
            self.connect((self, 0), (self.timeSink, 0))    
        

    def checkFftScale(self,):
        firstRun = True
        while True:
            try:
                fftSize = int( self.freqSink.fft_size() )
                fftSizeN = int( numpy.log2( float(fftSize) ) )
                if firstRun or fftSizeN!=self.fftSizeN:
                    firstRun = False
                    print(self.label, "Adjusting FFT Scaling", fftSize, fftSizeN)
                    self.set_fftSizeN = fftSizeN
                    self.fftSize = fftSize
                    winType = self.freqSink.fft_window()
                    #~ w  = firdes.window(winType, fftSize, 6.76)
                    #~ wsum = numpy.sum(numpy.sum(w))
                    #~ print wsum, fftSizeN, float(fftSize)/wsum
                    logScale = 20*numpy.log10( 2.0*float(fftSize)/numpy.sum(firdes.window(winType, fftSize, 6.76)) )
                    print(self.label, winType, logScale)
                    self.set_fftGainLog(logScale)
            except:
                traceback.print_exc()
            time.sleep(10.0)
    

    def get_centerFreq(self):
        return self.centerFreq

    def set_centerFreq(self, centerFreq):
        with self._lock:
            self.centerFreq = centerFreq
            self.freqSink.set_frequency_range(self.centerFreq, self.sampRate)
            self.waterfallSink.set_frequency_range(self.centerFreq, self.sampRate)

    def get_enableRssiDisplay(self):
        return self.enableRssiDisplay

    def set_enableRssiDisplay(self, enableRssiDisplay):
        with self._lock:
            self.enableRssiDisplay = enableRssiDisplay

    def get_enableSpectrum(self):
        return self.enableSpectrum

    def set_enableSpectrum(self, enableSpectrum):
        with self._lock:
            self.enableSpectrum = enableSpectrum

    def get_enableTimeWaveform(self):
        return self.enableTimeWaveform

    def set_enableTimeWaveform(self, enableTimeWaveform):
        with self._lock:
            self.enableTimeWaveform = enableTimeWaveform

    def get_enableWaterfall(self):
        return self.enableWaterfall

    def set_enableWaterfall(self, enableWaterfall):
        with self._lock:
            self.enableWaterfall = enableWaterfall

    def get_fftGainLog(self):
        return self.fftGainLog

    def set_fftGainLog(self, fftGainLog):
        with self._lock:
            self.fftGainLog = fftGainLog
            self.set_fftGainLinear(10.0**( float(self.fftGainLog)/20 ))

    def get_fftPlotRange(self):
        return self.fftPlotRange

    def set_fftPlotRange(self, fftPlotRange):
        with self._lock:
            self.fftPlotRange = fftPlotRange
            self.freqSink.set_y_axis(self.fftPlotRange[0], self.fftPlotRange[1])
            self.waterfallSink.set_intensity_range(self.fftPlotRange[0], self.fftPlotRange[1])

    def get_fftSizeN(self):
        return self.fftSizeN

    def set_fftSizeN(self, fftSizeN):
        with self._lock:
            self.fftSizeN = fftSizeN
            self.set_fftSize(int(2**self.fftSizeN))

    def get_hilbertFilterLength(self):
        return self.hilbertFilterLength

    def set_hilbertFilterLength(self, hilbertFilterLength):
        with self._lock:
            self.hilbertFilterLength = hilbertFilterLength
            self.set_hilbertLen(int(2**self.hilbertFilterLength)+1)

    def get_label(self):
        return self.label

    def set_label(self, label):
        with self._lock:
            self.label = label

    def get_rmsAvgGainExpInit(self):
        return self.rmsAvgGainExpInit

    def set_rmsAvgGainExpInit(self, rmsAvgGainExpInit):
        with self._lock:
            self.rmsAvgGainExpInit = rmsAvgGainExpInit
            self.set_rmsAvgGainExp(self.rmsAvgGainExpInit)

    def get_rmsGainRange(self):
        return self.rmsGainRange

    def set_rmsGainRange(self, rmsGainRange):
        with self._lock:
            self.rmsGainRange = rmsGainRange

    def get_rssiPollRate(self):
        return self.rssiPollRate

    def set_rssiPollRate(self, rssiPollRate):
        with self._lock:
            self.rssiPollRate = rssiPollRate

    def get_sampRate(self):
        return self.sampRate

    def set_sampRate(self, sampRate):
        if self.sampRate != sampRate:
            with self._lock:
                self.sampRate = sampRate
                self.set_N(int(self.sampRate*self.updatePeriod))
                self.freqSink.set_frequency_range(self.centerFreq, self.sampRate)
                self.timeSink.set_samp_rate(self.sampRate)
                self.waterfallSink.set_frequency_range(self.centerFreq, self.sampRate)

    def get_updatePeriod(self):
        return self.updatePeriod

    def set_updatePeriod(self, updatePeriod):
        with self._lock:
            self.updatePeriod = updatePeriod
            self.set_N(int(self.sampRate*self.updatePeriod))
            self.freqSink.set_update_time(self.updatePeriod)
            self.numberSInk.set_update_time(self.updatePeriod)
            self.timeSink.set_update_time(self.updatePeriod)
            self.waterfallSink.set_update_time(self.updatePeriod)

    def get_rssi(self):
        return self.rssi

    def set_rssi(self, rssi):
        with self._lock:
            self.rssi = rssi

    def get_rmsAvgGainExp(self):
        return self.rmsAvgGainExp

    def set_rmsAvgGainExp(self, rmsAvgGainExp):
        with self._lock:
            self.rmsAvgGainExp = rmsAvgGainExp
            self.rmsCalc.set_alpha(2**-self.rmsAvgGainExp)

    def get_hilbertLen(self):
        return self.hilbertLen

    def set_hilbertLen(self, hilbertLen):
        with self._lock:
            self.hilbertLen = hilbertLen

    def get_fftSize(self):
        return self.fftSize

    def set_fftSize(self, fftSize):
        with self._lock:
            self.fftSize = fftSize

    def get_fftGainLinear(self):
        return self.fftGainLinear

    def set_fftGainLinear(self, fftGainLinear):
        with self._lock:
            self.fftGainLinear = fftGainLinear
            self.fftGainMultiplier.set_k((self.fftGainLinear, ))

    def get_N(self):
        return self.N

    def set_N(self, N):
        with self._lock:
            self.N = N
            self.keepOneInN.set_n(self.N if self.N>0 else 1)

