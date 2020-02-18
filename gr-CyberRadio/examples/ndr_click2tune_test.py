#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NDRxxx Click2Tune Test
# Generated: Thu Sep 20 14:20:58 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_notation import *
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ConfigParser
import CyberRadio
import CyberRadioDriver
import CyberRadioDriver as crd
import os, numpy, json, scipy.signal
import sip
import sys
from gnuradio import qtgui


class ndr_click2tune_test(gr.top_block, Qt.QWidget):

    def __init__(self, fftRate=16, fftSizeExponent=15, fftWindowType='hann', localDataInterface='', radioDataPort=2, radioHostname='ndr301', radioType='ndr301'):
        gr.top_block.__init__(self, "NDRxxx Click2Tune Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDRxxx Click2Tune Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ndr_click2tune_test")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.fftRate = fftRate
        self.fftSizeExponent = fftSizeExponent
        self.fftWindowType = fftWindowType
        self.localDataInterface = localDataInterface
        self.radioDataPort = radioDataPort
        self.radioHostname = radioHostname
        self.radioType = radioType

        ##################################################
        # Variables
        ##################################################
        self.radioObj = radioObj = crd.getRadioObject(
                radioType,
                verbose=True,
                host=radioHostname if True else None,
                 )
        if True and radioObj.isConnected():
            print("{0} is {1}connected to {2} as {3}. Using CyberRadioDriver version {4}.".format("radioObj", "" if radioObj.isConnected() else "not ", radioObj.host_or_dev, radioObj, crd.version))
        self.wbddcRateSet = wbddcRateSet = dict( [(k,v) for k,v in radioObj.getWbddcRateSet().iteritems() if radioObj.getDdcDataFormat(True).get(k,"iq")!="real"] )
        self.configFilePath = configFilePath = os.path.expanduser( os.path.join("~",".%s_demo.cfg"%(radioObj.name.lower(),)) )
        self._cfg_wbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_wbddcRateIndex_config.read(configFilePath)
        try: cfg_wbddcRateIndex = self._cfg_wbddcRateIndex_config.getint('wbddc', 'rate_index')
        except: cfg_wbddcRateIndex = sorted(wbddcRateSet.keys())[0]
        self.cfg_wbddcRateIndex = cfg_wbddcRateIndex
        self.wbddcRateIndex = wbddcRateIndex = cfg_wbddcRateIndex
        self.wbSampleRate = wbSampleRate = wbddcRateSet[wbddcRateIndex]
        self.samplesPerFrame = samplesPerFrame = int( radioObj.getVitaPayloadSize()/4 )
        self.nbddcRateSet = nbddcRateSet = radioObj.getNbddcRateSet()
        self.framesPerSecond = framesPerSecond = float(wbSampleRate)/float(samplesPerFrame)
        self.fftSize = fftSize = int(2**fftSizeExponent)
        self._cfg_nbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_nbddcRateIndex_config.read(configFilePath)
        try: cfg_nbddcRateIndex = self._cfg_nbddcRateIndex_config.getint('nbddc', 'rate_index')
        except: cfg_nbddcRateIndex = sorted(nbddcRateSet.keys())[0]
        self.cfg_nbddcRateIndex = cfg_nbddcRateIndex
        self._cfg_iirAvgExp_config = ConfigParser.ConfigParser()
        self._cfg_iirAvgExp_config.read(configFilePath)
        try: cfg_iirAvgExp = self._cfg_iirAvgExp_config.getint('gui', 'iirAvgExp')
        except: cfg_iirAvgExp = int(3)
        self.cfg_iirAvgExp = cfg_iirAvgExp
        self.nbddcRateIndex = nbddcRateIndex = cfg_nbddcRateIndex
        self.iirAvgExp = iirAvgExp = cfg_iirAvgExp
        self.framesPerFft = framesPerFft = int( numpy.round( float(fftSize)/samplesPerFrame ) )
        self.framesPerBlock = framesPerBlock = float(framesPerSecond)/fftRate
        self._cfg_tunerIndex_config = ConfigParser.ConfigParser()
        self._cfg_tunerIndex_config.read(configFilePath)
        try: cfg_tunerIndex = self._cfg_tunerIndex_config.getint('tuner', 'index')
        except: cfg_tunerIndex = radioObj.getTunerIndexRange()[0]
        self.cfg_tunerIndex = cfg_tunerIndex
        self._cfg_tunerAtten_config = ConfigParser.ConfigParser()
        self._cfg_tunerAtten_config.read(configFilePath)
        try: cfg_tunerAtten = self._cfg_tunerAtten_config.getint('tuner', 'atten')
        except: cfg_tunerAtten = int(radioObj.getTunerAttenuationRange()[0])
        self.cfg_tunerAtten = cfg_tunerAtten
        self._cfg_rfFreqMhz_config = ConfigParser.ConfigParser()
        self._cfg_rfFreqMhz_config.read(configFilePath)
        try: cfg_rfFreqMhz = self._cfg_rfFreqMhz_config.getint('tuner', 'freq')
        except: cfg_rfFreqMhz = int(radioObj.getTunerFrequencyRange()[0]/1e6)
        self.cfg_rfFreqMhz = cfg_rfFreqMhz
        self._cfg_refLevel_config = ConfigParser.ConfigParser()
        self._cfg_refLevel_config.read(configFilePath)
        try: cfg_refLevel = self._cfg_refLevel_config.getint('display', 'ref_level')
        except: cfg_refLevel = 0
        self.cfg_refLevel = cfg_refLevel
        self._cfg_nbddcIndex_config = ConfigParser.ConfigParser()
        self._cfg_nbddcIndex_config.read(configFilePath)
        try: cfg_nbddcIndex = self._cfg_nbddcIndex_config.getint('nbddc', 'index')
        except: cfg_nbddcIndex = radioObj.getNbddcIndexRange()[0]
        self.cfg_nbddcIndex = cfg_nbddcIndex
        self._cfg_dynRange_config = ConfigParser.ConfigParser()
        self._cfg_dynRange_config.read(configFilePath)
        try: cfg_dynRange = self._cfg_dynRange_config.getint('display', 'dyn_range')
        except: cfg_dynRange = 120
        self.cfg_dynRange = cfg_dynRange
        self.wbddcEnable = wbddcEnable = True
        self.wbddcBwSet = wbddcBwSet = dict( [(k,v) for k,v in radioObj.getWbddcBwSet().iteritems() if radioObj.getDdcDataFormat(True).get(k,"iq")!="real"] )
        self.udpBasePort = udpBasePort = 44000
        self.tunerIndex = tunerIndex = cfg_tunerIndex
        self.tunerAtten = tunerAtten = cfg_tunerAtten
        self.rfFreqMhz = rfFreqMhz = cfg_rfFreqMhz
        self.refLevel = refLevel = cfg_refLevel
        self.nbddcIndex = nbddcIndex = cfg_nbddcIndex
        self.nbddcEnable = nbddcEnable = True
        self.nbddcBwSet = nbddcBwSet = dict( [(k,v) for k,v in radioObj.getNbddcBwSet().iteritems() if radioObj.getDdcDataFormat(False).get(k,"iq")!="real"] )
        self.nbSampleRate = nbSampleRate = nbddcRateSet[nbddcRateIndex]
        self.iirAlpha = iirAlpha = 2.0**(float(-iirAvgExp))
        self.framesToSkip = framesToSkip = int(numpy.round(framesPerBlock-framesPerFft))
        self.fftWindow = fftWindow = scipy.signal.get_window(fftWindowType,fftSize)
        self.dynRange = dynRange = cfg_dynRange
        self.dispSize = dispSize = fftSize

        ##################################################
        # Blocks
        ##################################################
        self.wbTabs = Qt.QTabWidget()
        self.wbTabs_widget_0 = Qt.QWidget()
        self.wbTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.wbTabs_widget_0)
        self.wbTabs_grid_layout_0 = Qt.QGridLayout()
        self.wbTabs_layout_0.addLayout(self.wbTabs_grid_layout_0)
        self.wbTabs.addTab(self.wbTabs_widget_0, 'High-Res Wideband')
        self.wbTabs_widget_1 = Qt.QWidget()
        self.wbTabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.wbTabs_widget_1)
        self.wbTabs_grid_layout_1 = Qt.QGridLayout()
        self.wbTabs_layout_1.addLayout(self.wbTabs_grid_layout_1)
        self.wbTabs.addTab(self.wbTabs_widget_1, 'Time Plot')
        self.top_grid_layout.addWidget(self.wbTabs, 0,0,2,3)
        self.controlTabs = Qt.QTabWidget()
        self.controlTabs_widget_0 = Qt.QWidget()
        self.controlTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controlTabs_widget_0)
        self.controlTabs_grid_layout_0 = Qt.QGridLayout()
        self.controlTabs_layout_0.addLayout(self.controlTabs_grid_layout_0)
        self.controlTabs.addTab(self.controlTabs_widget_0, 'Control')
        self.top_grid_layout.addWidget(self.controlTabs, 2,0,1,1)
        self._wbddcRateIndex_options = sorted(wbddcRateSet.keys())
        self._wbddcRateIndex_labels = ["%d: %sHz @ %ssps"%(k,num_to_str(wbddcBwSet[k]),num_to_str(wbddcRateSet[k])) for k in sorted(wbddcRateSet.keys())]
        self._wbddcRateIndex_tool_bar = Qt.QToolBar(self)
        self._wbddcRateIndex_tool_bar.addWidget(Qt.QLabel('WBDDC Sample Rate'+": "))
        self._wbddcRateIndex_combo_box = Qt.QComboBox()
        self._wbddcRateIndex_tool_bar.addWidget(self._wbddcRateIndex_combo_box)
        for label in self._wbddcRateIndex_labels: self._wbddcRateIndex_combo_box.addItem(label)
        self._wbddcRateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._wbddcRateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._wbddcRateIndex_options.index(i)))
        self._wbddcRateIndex_callback(self.wbddcRateIndex)
        self._wbddcRateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_wbddcRateIndex(self._wbddcRateIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._wbddcRateIndex_tool_bar, 0,1,1,1)
        self._tunerIndex_options = radioObj.getTunerIndexRange()
        self._tunerIndex_labels = map(str, self._tunerIndex_options)
        self._tunerIndex_tool_bar = Qt.QToolBar(self)
        self._tunerIndex_tool_bar.addWidget(Qt.QLabel('Tuner Index'+": "))
        self._tunerIndex_combo_box = Qt.QComboBox()
        self._tunerIndex_tool_bar.addWidget(self._tunerIndex_combo_box)
        for label in self._tunerIndex_labels: self._tunerIndex_combo_box.addItem(label)
        self._tunerIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._tunerIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._tunerIndex_options.index(i)))
        self._tunerIndex_callback(self.tunerIndex)
        self._tunerIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_tunerIndex(self._tunerIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._tunerIndex_tool_bar, 0,0,1,1)
        self._tunerAtten_range = Range(int(radioObj.getTunerAttenuationRange()[0]), int(radioObj.getTunerAttenuationRange()[1]), 1, cfg_tunerAtten, 200)
        self._tunerAtten_win = RangeWidget(self._tunerAtten_range, self.set_tunerAtten, "Tuner\nAtten.\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._tunerAtten_win, 3,1,1,1)
        self._rfFreqMhz_range = Range(int(radioObj.getTunerFrequencyRange()[0]/1e6), int(radioObj.getTunerFrequencyRange()[1]/1e6), 10, cfg_rfFreqMhz, 200)
        self._rfFreqMhz_win = RangeWidget(self._rfFreqMhz_range, self.set_rfFreqMhz, 'Tuner Freq (MHz)', "counter_slider", int)
        self.wbTabs_grid_layout_0.addWidget(self._rfFreqMhz_win, 3,0,1,1)
        self._refLevel_range = Range(-120, +10, 5, cfg_refLevel, (130/5)+1)
        self._refLevel_win = RangeWidget(self._refLevel_range, self.set_refLevel, "Ref.\nLevel\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._refLevel_win, 0,1,1,1)
        self._nbddcRateIndex_options = sorted(nbddcRateSet.keys())
        self._nbddcRateIndex_labels = ["%d: %sHz @ %ssps"%(k,num_to_str(nbddcBwSet[k]),num_to_str(nbddcRateSet[k])) for k in sorted(nbddcRateSet.keys())]
        self._nbddcRateIndex_tool_bar = Qt.QToolBar(self)
        self._nbddcRateIndex_tool_bar.addWidget(Qt.QLabel('NBDDC Index'+": "))
        self._nbddcRateIndex_combo_box = Qt.QComboBox()
        self._nbddcRateIndex_tool_bar.addWidget(self._nbddcRateIndex_combo_box)
        for label in self._nbddcRateIndex_labels: self._nbddcRateIndex_combo_box.addItem(label)
        self._nbddcRateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcRateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcRateIndex_options.index(i)))
        self._nbddcRateIndex_callback(self.nbddcRateIndex)
        self._nbddcRateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcRateIndex(self._nbddcRateIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._nbddcRateIndex_tool_bar, 1,1,1,1)
        self._nbddcIndex_options = radioObj.getNbddcIndexRange()
        self._nbddcIndex_labels = map(str, self._nbddcIndex_options)
        self._nbddcIndex_tool_bar = Qt.QToolBar(self)
        self._nbddcIndex_tool_bar.addWidget(Qt.QLabel('NBDDC Index'+": "))
        self._nbddcIndex_combo_box = Qt.QComboBox()
        self._nbddcIndex_tool_bar.addWidget(self._nbddcIndex_combo_box)
        for label in self._nbddcIndex_labels: self._nbddcIndex_combo_box.addItem(label)
        self._nbddcIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcIndex_options.index(i)))
        self._nbddcIndex_callback(self.nbddcIndex)
        self._nbddcIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcIndex(self._nbddcIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._nbddcIndex_tool_bar, 1,0,1,1)
        self.nbTabs = Qt.QTabWidget()
        self.nbTabs_widget_0 = Qt.QWidget()
        self.nbTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.nbTabs_widget_0)
        self.nbTabs_grid_layout_0 = Qt.QGridLayout()
        self.nbTabs_layout_0.addLayout(self.nbTabs_grid_layout_0)
        self.nbTabs.addTab(self.nbTabs_widget_0, 'Frequency')
        self.nbTabs_widget_1 = Qt.QWidget()
        self.nbTabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.nbTabs_widget_1)
        self.nbTabs_grid_layout_1 = Qt.QGridLayout()
        self.nbTabs_layout_1.addLayout(self.nbTabs_grid_layout_1)
        self.nbTabs.addTab(self.nbTabs_widget_1, 'Time')
        self.nbTabs_widget_2 = Qt.QWidget()
        self.nbTabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.nbTabs_widget_2)
        self.nbTabs_grid_layout_2 = Qt.QGridLayout()
        self.nbTabs_layout_2.addLayout(self.nbTabs_grid_layout_2)
        self.nbTabs.addTab(self.nbTabs_widget_2, 'FM Demod')
        self.top_grid_layout.addWidget(self.nbTabs, 2,1,1,1)
        self._dynRange_range = Range(5, 200, 5, cfg_dynRange, (195/5)+1)
        self._dynRange_win = RangeWidget(self._dynRange_range, self.set_dynRange, "Dyn.\nRange\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._dynRange_win, 1,1,1,1)
        self.wb_rx_source_snap = CyberRadio.snapshot_vector_source(radioObj.name.lower(), '0.0.0.0', udpBasePort, fftSize, fftRate)
        print("%s = CyberRadio.snapshot_vector_source(%r, %r, %r, %r, %r)"%("wb_rx_source_snap", '0.0.0.0', udpBasePort, fftSize, fftRate, radioObj.name.lower()))

        self.single_pole_iir_filter_xx_1 = filter.single_pole_iir_filter_ff(2.0**-8, 1)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            dispSize,
            0,
            1.0/1024,
            'Sample',
            'Amplitude',
            '',
            2 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis(-1, +1)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units('Frame')
        self.qtgui_vector_sink_f_0_0.set_y_axis_units('V')
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)

        labels = ['I', 'Q', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["black", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.pyqwidget(), Qt.QWidget)
        self.wbTabs_layout_1.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            dispSize,
            rfFreqMhz-wbSampleRate/2e6,
            wbSampleRate/1e6/fftSize,
            'Frequency (MHz)',
            'Magnitude (dBfs)',
            '',
            2 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(refLevel-dynRange, refLevel)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units('MHz')
        self.qtgui_vector_sink_f_0.set_y_axis_units('dBfs')
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['Realtime', 'Average', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["green", "dark red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0/8, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.wbTabs_grid_layout_0.addWidget(self._qtgui_vector_sink_f_0_win, 0,0,3,1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	1024, #size
        	nbSampleRate, #samp_rate
        	'FM Demod Output', #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-nbSampleRate/2e3, nbSampleRate/2e3)

        self.qtgui_time_sink_x_0_0.set_y_label('Inst. Freq', 'kHz')

        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['FM Out', 'FM Mean', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["magenta", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.nbTabs_layout_2.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	nbSampleRate, #samp_rate
        	"", #name
        	3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['I', 'Q', 'Mag', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.nbTabs_layout_1.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rfFreqMhz*1e6, #fc
        	nbSampleRate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(1.0/20)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 0)
        self.qtgui_freq_sink_x_0.set_y_label('Magnitude (dBfs)', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["dark blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.nbTabs_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)
        self._iirAvgExp_range = Range(0, 8, 1, cfg_iirAvgExp, 200)
        self._iirAvgExp_win = RangeWidget(self._iirAvgExp_range, self.set_iirAvgExp, 'Avg.', "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._iirAvgExp_win, 2,1,1,1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((nbSampleRate/(2e3*numpy.pi), ))
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_message_debug_1_0 = blocks.message_debug()
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(fftSize)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.CyberRadio_vita49_source_0 = CyberRadio.vita_udp_rx(
              '0.0.0.0',
              udpBasePort+1,
              radioObj.getVitaHeaderSize(),
              radioObj.getVitaPayloadSize()//4,
              radioObj.getVitaHeaderSize()+radioObj.getVitaPayloadSize()+radioObj.getVitaTailSize(),
              radioObj.isByteswapped(),
              radioObj.isIqSwapped(),
              False,
              False,
               )
        self.CyberRadio_log_mag_fft_0 = CyberRadio.log_mag_fft(
            numInputs=1,
            fftSize=fftSize,
            windowType="blackmanharris",
            iirAlpha=iirAlpha,
            secondaryOutput="log_mag_unfiltered",
            resetOnAlphaChange=True,
             )
        self.CyberRadio_generic_tuner_control_block_0 = CyberRadio.generic_tuner_control_block(
                    radioObj,
                    tunerIndex,
                    True,
                    rfFreqMhz,
                    tunerAtten,
                    1,
                    None,
                    {},
                    True
                     )
        self.CyberRadio_generic_ddc_control_block_0_0 = CyberRadio.generic_ddc_control_block(
                    radioObj,
                    nbddcIndex,
                    nbddcEnable,
                    False,
                    nbddcRateIndex,
                    0,
                    0,
                    tunerIndex,
                    0,
                    radioDataPort,
                    -1,
                    localDataInterface,
                    udpBasePort+1,
                    {},
                    True,
                    1,
                    1,
                     )
        self.CyberRadio_generic_ddc_control_block_0 = CyberRadio.generic_ddc_control_block(
                    radioObj,
                    tunerIndex,
                    wbddcEnable,
                    True,
                    wbddcRateIndex,
                    0,
                    0,
                    tunerIndex,
                    0,
                    radioDataPort,
                    -1,
                    localDataInterface,
                    udpBasePort,
                    {},
                    True,
                    1,
                    1,
                     )
        self.CyberRadio_freq_msg_converter_0_1 = CyberRadio.freq_msg_converter(
              msgKey = 'freq',
              unitsIn = 1.0e6,
              unitsOut = 1.0,
              offset = rfFreqMhz*-1e0,
              roundOutput = False,
              triggerOnChange = True,
              debug = True,
               )
        self.CyberRadio_freq_msg_converter_0_0 = CyberRadio.freq_msg_converter(
              msgKey = 'freq',
              unitsIn = 1.0,
              unitsOut = 1.0,
              offset = rfFreqMhz*1e6,
              roundOutput = False,
              triggerOnChange = True,
              debug = True,
               )
        self.CyberRadio_freq_msg_converter_0 = CyberRadio.freq_msg_converter(
              msgKey = 'freq',
              unitsIn = 1.0,
              unitsOut = 1.0,
              offset = rfFreqMhz*-1e6,
              roundOutput = False,
              triggerOnChange = True,
              debug = True,
               )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.CyberRadio_freq_msg_converter_0, 'freq'), (self.CyberRadio_generic_ddc_control_block_0_0, 'freq'))
        self.msg_connect((self.CyberRadio_freq_msg_converter_0_0, 'freq'), (self.qtgui_freq_sink_x_0, 'freq'))
        self.msg_connect((self.CyberRadio_freq_msg_converter_0_1, 'freq'), (self.CyberRadio_generic_ddc_control_block_0_0, 'freq'))
        self.msg_connect((self.CyberRadio_generic_ddc_control_block_0, 'status'), (self.blocks_message_debug_1_0, 'print'))
        self.msg_connect((self.CyberRadio_generic_ddc_control_block_0_0, 'freq'), (self.CyberRadio_freq_msg_converter_0_0, 'freq'))
        self.msg_connect((self.CyberRadio_generic_ddc_control_block_0_0, 'udp'), (self.CyberRadio_vita49_source_0, 'control'))
        self.msg_connect((self.CyberRadio_vita49_source_0, 'status'), (self.CyberRadio_generic_ddc_control_block_0_0, 'udp'))
        self.msg_connect((self.qtgui_freq_sink_x_0, 'freq'), (self.CyberRadio_freq_msg_converter_0, 'freq'))
        self.msg_connect((self.qtgui_vector_sink_f_0, 'xval'), (self.CyberRadio_freq_msg_converter_0_1, 'freq'))
        self.connect((self.CyberRadio_log_mag_fft_0, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.CyberRadio_log_mag_fft_0, 1), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.CyberRadio_vita49_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.CyberRadio_vita49_source_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.CyberRadio_vita49_source_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.CyberRadio_vita49_source_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.CyberRadio_vita49_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_float_1, 1), (self.qtgui_vector_sink_f_0_0, 1))
        self.connect((self.blocks_complex_to_float_1, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.single_pole_iir_filter_xx_1, 0))
        self.connect((self.single_pole_iir_filter_xx_1, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.wb_rx_source_snap, 0), (self.CyberRadio_log_mag_fft_0, 0))
        self.connect((self.wb_rx_source_snap, 0), (self.blocks_complex_to_float_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ndr_click2tune_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_fftRate(self):
        return self.fftRate

    def set_fftRate(self, fftRate):
        self.fftRate = fftRate
        self.set_framesPerBlock(float(self.framesPerSecond)/self.fftRate)

    def get_fftSizeExponent(self):
        return self.fftSizeExponent

    def set_fftSizeExponent(self, fftSizeExponent):
        self.fftSizeExponent = fftSizeExponent
        self.set_fftSize(int(2**self.fftSizeExponent))

    def get_fftWindowType(self):
        return self.fftWindowType

    def set_fftWindowType(self, fftWindowType):
        self.fftWindowType = fftWindowType
        self.set_fftWindow(scipy.signal.get_window(self.fftWindowType,self.fftSize))

    def get_localDataInterface(self):
        return self.localDataInterface

    def set_localDataInterface(self, localDataInterface):
        self.localDataInterface = localDataInterface

    def get_radioDataPort(self):
        return self.radioDataPort

    def set_radioDataPort(self, radioDataPort):
        self.radioDataPort = radioDataPort

    def get_radioHostname(self):
        return self.radioHostname

    def set_radioHostname(self, radioHostname):
        self.radioHostname = radioHostname

    def get_radioType(self):
        return self.radioType

    def set_radioType(self, radioType):
        self.radioType = radioType

    def get_radioObj(self):
        return self.radioObj

    def set_radioObj(self, radioObj):
        self.radioObj = radioObj

    def get_wbddcRateSet(self):
        return self.wbddcRateSet

    def set_wbddcRateSet(self, wbddcRateSet):
        self.wbddcRateSet = wbddcRateSet
        self.set_wbSampleRate(self.wbddcRateSet[self.wbddcRateIndex])

    def get_configFilePath(self):
        return self.configFilePath

    def set_configFilePath(self, configFilePath):
        self.configFilePath = configFilePath
        self._cfg_wbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_wbddcRateIndex_config.read(self.configFilePath)
        if not self._cfg_wbddcRateIndex_config.has_section('wbddc'):
        	self._cfg_wbddcRateIndex_config.add_section('wbddc')
        self._cfg_wbddcRateIndex_config.set('wbddc', 'rate_index', str(self.wbddcRateIndex))
        self._cfg_wbddcRateIndex_config.write(open(self.configFilePath, 'w'))
        self._cfg_tunerIndex_config = ConfigParser.ConfigParser()
        self._cfg_tunerIndex_config.read(self.configFilePath)
        if not self._cfg_tunerIndex_config.has_section('tuner'):
        	self._cfg_tunerIndex_config.add_section('tuner')
        self._cfg_tunerIndex_config.set('tuner', 'index', str(self.tunerIndex))
        self._cfg_tunerIndex_config.write(open(self.configFilePath, 'w'))
        self._cfg_tunerAtten_config = ConfigParser.ConfigParser()
        self._cfg_tunerAtten_config.read(self.configFilePath)
        if not self._cfg_tunerAtten_config.has_section('tuner'):
        	self._cfg_tunerAtten_config.add_section('tuner')
        self._cfg_tunerAtten_config.set('tuner', 'atten', str(self.tunerAtten))
        self._cfg_tunerAtten_config.write(open(self.configFilePath, 'w'))
        self._cfg_rfFreqMhz_config = ConfigParser.ConfigParser()
        self._cfg_rfFreqMhz_config.read(self.configFilePath)
        if not self._cfg_rfFreqMhz_config.has_section('tuner'):
        	self._cfg_rfFreqMhz_config.add_section('tuner')
        self._cfg_rfFreqMhz_config.set('tuner', 'freq', str(self.rfFreqMhz))
        self._cfg_rfFreqMhz_config.write(open(self.configFilePath, 'w'))
        self._cfg_refLevel_config = ConfigParser.ConfigParser()
        self._cfg_refLevel_config.read(self.configFilePath)
        if not self._cfg_refLevel_config.has_section('display'):
        	self._cfg_refLevel_config.add_section('display')
        self._cfg_refLevel_config.set('display', 'ref_level', str(self.refLevel))
        self._cfg_refLevel_config.write(open(self.configFilePath, 'w'))
        self._cfg_nbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_nbddcRateIndex_config.read(self.configFilePath)
        if not self._cfg_nbddcRateIndex_config.has_section('nbddc'):
        	self._cfg_nbddcRateIndex_config.add_section('nbddc')
        self._cfg_nbddcRateIndex_config.set('nbddc', 'rate_index', str(self.nbddcRateIndex))
        self._cfg_nbddcRateIndex_config.write(open(self.configFilePath, 'w'))
        self._cfg_nbddcIndex_config = ConfigParser.ConfigParser()
        self._cfg_nbddcIndex_config.read(self.configFilePath)
        if not self._cfg_nbddcIndex_config.has_section('nbddc'):
        	self._cfg_nbddcIndex_config.add_section('nbddc')
        self._cfg_nbddcIndex_config.set('nbddc', 'index', str(self.nbddcIndex))
        self._cfg_nbddcIndex_config.write(open(self.configFilePath, 'w'))
        self._cfg_iirAvgExp_config = ConfigParser.ConfigParser()
        self._cfg_iirAvgExp_config.read(self.configFilePath)
        if not self._cfg_iirAvgExp_config.has_section('gui'):
        	self._cfg_iirAvgExp_config.add_section('gui')
        self._cfg_iirAvgExp_config.set('gui', 'iirAvgExp', str(self.iirAvgExp))
        self._cfg_iirAvgExp_config.write(open(self.configFilePath, 'w'))
        self._cfg_dynRange_config = ConfigParser.ConfigParser()
        self._cfg_dynRange_config.read(self.configFilePath)
        if not self._cfg_dynRange_config.has_section('display'):
        	self._cfg_dynRange_config.add_section('display')
        self._cfg_dynRange_config.set('display', 'dyn_range', str(self.dynRange))
        self._cfg_dynRange_config.write(open(self.configFilePath, 'w'))

    def get_cfg_wbddcRateIndex(self):
        return self.cfg_wbddcRateIndex

    def set_cfg_wbddcRateIndex(self, cfg_wbddcRateIndex):
        self.cfg_wbddcRateIndex = cfg_wbddcRateIndex
        self.set_wbddcRateIndex(self.cfg_wbddcRateIndex)

    def get_wbddcRateIndex(self):
        return self.wbddcRateIndex

    def set_wbddcRateIndex(self, wbddcRateIndex):
        self.wbddcRateIndex = wbddcRateIndex
        self._wbddcRateIndex_callback(self.wbddcRateIndex)
        self.set_wbSampleRate(self.wbddcRateSet[self.wbddcRateIndex])
        self._cfg_wbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_wbddcRateIndex_config.read(self.configFilePath)
        if not self._cfg_wbddcRateIndex_config.has_section('wbddc'):
        	self._cfg_wbddcRateIndex_config.add_section('wbddc')
        self._cfg_wbddcRateIndex_config.set('wbddc', 'rate_index', str(self.wbddcRateIndex))
        self._cfg_wbddcRateIndex_config.write(open(self.configFilePath, 'w'))
        self.CyberRadio_generic_ddc_control_block_0.set_rate(self.wbddcRateIndex)

    def get_wbSampleRate(self):
        return self.wbSampleRate

    def set_wbSampleRate(self, wbSampleRate):
        self.wbSampleRate = wbSampleRate
        self.qtgui_vector_sink_f_0.set_x_axis(self.rfFreqMhz-self.wbSampleRate/2e6, self.wbSampleRate/1e6/self.fftSize)
        self.set_framesPerSecond(float(self.wbSampleRate)/float(self.samplesPerFrame))

    def get_samplesPerFrame(self):
        return self.samplesPerFrame

    def set_samplesPerFrame(self, samplesPerFrame):
        self.samplesPerFrame = samplesPerFrame
        self.set_framesPerSecond(float(self.wbSampleRate)/float(self.samplesPerFrame))
        self.set_framesPerFft(int( numpy.round( float(self.fftSize)/self.samplesPerFrame ) ))

    def get_nbddcRateSet(self):
        return self.nbddcRateSet

    def set_nbddcRateSet(self, nbddcRateSet):
        self.nbddcRateSet = nbddcRateSet
        self.set_nbSampleRate(self.nbddcRateSet[self.nbddcRateIndex])

    def get_framesPerSecond(self):
        return self.framesPerSecond

    def set_framesPerSecond(self, framesPerSecond):
        self.framesPerSecond = framesPerSecond
        self.set_framesPerBlock(float(self.framesPerSecond)/self.fftRate)

    def get_fftSize(self):
        return self.fftSize

    def set_fftSize(self, fftSize):
        self.fftSize = fftSize
        self.set_dispSize(self.fftSize)
        self.qtgui_vector_sink_f_0.set_x_axis(self.rfFreqMhz-self.wbSampleRate/2e6, self.wbSampleRate/1e6/self.fftSize)
        self.set_framesPerFft(int( numpy.round( float(self.fftSize)/self.samplesPerFrame ) ))
        self.set_fftWindow(scipy.signal.get_window(self.fftWindowType,self.fftSize))

    def get_cfg_nbddcRateIndex(self):
        return self.cfg_nbddcRateIndex

    def set_cfg_nbddcRateIndex(self, cfg_nbddcRateIndex):
        self.cfg_nbddcRateIndex = cfg_nbddcRateIndex
        self.set_nbddcRateIndex(self.cfg_nbddcRateIndex)

    def get_cfg_iirAvgExp(self):
        return self.cfg_iirAvgExp

    def set_cfg_iirAvgExp(self, cfg_iirAvgExp):
        self.cfg_iirAvgExp = cfg_iirAvgExp
        self.set_iirAvgExp(self.cfg_iirAvgExp)

    def get_nbddcRateIndex(self):
        return self.nbddcRateIndex

    def set_nbddcRateIndex(self, nbddcRateIndex):
        self.nbddcRateIndex = nbddcRateIndex
        self._nbddcRateIndex_callback(self.nbddcRateIndex)
        self.set_nbSampleRate(self.nbddcRateSet[self.nbddcRateIndex])
        self._cfg_nbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_nbddcRateIndex_config.read(self.configFilePath)
        if not self._cfg_nbddcRateIndex_config.has_section('nbddc'):
        	self._cfg_nbddcRateIndex_config.add_section('nbddc')
        self._cfg_nbddcRateIndex_config.set('nbddc', 'rate_index', str(self.nbddcRateIndex))
        self._cfg_nbddcRateIndex_config.write(open(self.configFilePath, 'w'))
        self.CyberRadio_generic_ddc_control_block_0_0.set_rate(self.nbddcRateIndex)

    def get_iirAvgExp(self):
        return self.iirAvgExp

    def set_iirAvgExp(self, iirAvgExp):
        self.iirAvgExp = iirAvgExp
        self.set_iirAlpha(2.0**(float(-self.iirAvgExp)))
        self._cfg_iirAvgExp_config = ConfigParser.ConfigParser()
        self._cfg_iirAvgExp_config.read(self.configFilePath)
        if not self._cfg_iirAvgExp_config.has_section('gui'):
        	self._cfg_iirAvgExp_config.add_section('gui')
        self._cfg_iirAvgExp_config.set('gui', 'iirAvgExp', str(self.iirAvgExp))
        self._cfg_iirAvgExp_config.write(open(self.configFilePath, 'w'))

    def get_framesPerFft(self):
        return self.framesPerFft

    def set_framesPerFft(self, framesPerFft):
        self.framesPerFft = framesPerFft
        self.set_framesToSkip(int(numpy.round(self.framesPerBlock-self.framesPerFft)))

    def get_framesPerBlock(self):
        return self.framesPerBlock

    def set_framesPerBlock(self, framesPerBlock):
        self.framesPerBlock = framesPerBlock
        self.set_framesToSkip(int(numpy.round(self.framesPerBlock-self.framesPerFft)))

    def get_cfg_tunerIndex(self):
        return self.cfg_tunerIndex

    def set_cfg_tunerIndex(self, cfg_tunerIndex):
        self.cfg_tunerIndex = cfg_tunerIndex
        self.set_tunerIndex(self.cfg_tunerIndex)

    def get_cfg_tunerAtten(self):
        return self.cfg_tunerAtten

    def set_cfg_tunerAtten(self, cfg_tunerAtten):
        self.cfg_tunerAtten = cfg_tunerAtten
        self.set_tunerAtten(self.cfg_tunerAtten)

    def get_cfg_rfFreqMhz(self):
        return self.cfg_rfFreqMhz

    def set_cfg_rfFreqMhz(self, cfg_rfFreqMhz):
        self.cfg_rfFreqMhz = cfg_rfFreqMhz
        self.set_rfFreqMhz(self.cfg_rfFreqMhz)

    def get_cfg_refLevel(self):
        return self.cfg_refLevel

    def set_cfg_refLevel(self, cfg_refLevel):
        self.cfg_refLevel = cfg_refLevel
        self.set_refLevel(self.cfg_refLevel)

    def get_cfg_nbddcIndex(self):
        return self.cfg_nbddcIndex

    def set_cfg_nbddcIndex(self, cfg_nbddcIndex):
        self.cfg_nbddcIndex = cfg_nbddcIndex
        self.set_nbddcIndex(self.cfg_nbddcIndex)

    def get_cfg_dynRange(self):
        return self.cfg_dynRange

    def set_cfg_dynRange(self, cfg_dynRange):
        self.cfg_dynRange = cfg_dynRange
        self.set_dynRange(self.cfg_dynRange)

    def get_wbddcEnable(self):
        return self.wbddcEnable

    def set_wbddcEnable(self, wbddcEnable):
        self.wbddcEnable = wbddcEnable
        self.CyberRadio_generic_ddc_control_block_0.set_enable(self.wbddcEnable)

    def get_wbddcBwSet(self):
        return self.wbddcBwSet

    def set_wbddcBwSet(self, wbddcBwSet):
        self.wbddcBwSet = wbddcBwSet

    def get_udpBasePort(self):
        return self.udpBasePort

    def set_udpBasePort(self, udpBasePort):
        self.udpBasePort = udpBasePort
        self.CyberRadio_generic_ddc_control_block_0_0.set_udpPort(self.udpBasePort+1)
        self.CyberRadio_generic_ddc_control_block_0.set_udpPort(self.udpBasePort)

    def get_tunerIndex(self):
        return self.tunerIndex

    def set_tunerIndex(self, tunerIndex):
        self.tunerIndex = tunerIndex
        self._tunerIndex_callback(self.tunerIndex)
        self._cfg_tunerIndex_config = ConfigParser.ConfigParser()
        self._cfg_tunerIndex_config.read(self.configFilePath)
        if not self._cfg_tunerIndex_config.has_section('tuner'):
        	self._cfg_tunerIndex_config.add_section('tuner')
        self._cfg_tunerIndex_config.set('tuner', 'index', str(self.tunerIndex))
        self._cfg_tunerIndex_config.write(open(self.configFilePath, 'w'))
        self.CyberRadio_generic_tuner_control_block_0.set_index(self.tunerIndex)
        self.CyberRadio_generic_ddc_control_block_0_0.set_rfSource(self.tunerIndex)
        self.CyberRadio_generic_ddc_control_block_0.set_index(self.tunerIndex)
        self.CyberRadio_generic_ddc_control_block_0.set_rfSource(self.tunerIndex)

    def get_tunerAtten(self):
        return self.tunerAtten

    def set_tunerAtten(self, tunerAtten):
        self.tunerAtten = tunerAtten
        self._cfg_tunerAtten_config = ConfigParser.ConfigParser()
        self._cfg_tunerAtten_config.read(self.configFilePath)
        if not self._cfg_tunerAtten_config.has_section('tuner'):
        	self._cfg_tunerAtten_config.add_section('tuner')
        self._cfg_tunerAtten_config.set('tuner', 'atten', str(self.tunerAtten))
        self._cfg_tunerAtten_config.write(open(self.configFilePath, 'w'))
        self.CyberRadio_generic_tuner_control_block_0.set_attenuation(self.tunerAtten)

    def get_rfFreqMhz(self):
        return self.rfFreqMhz

    def set_rfFreqMhz(self, rfFreqMhz):
        self.rfFreqMhz = rfFreqMhz
        self.qtgui_vector_sink_f_0.set_x_axis(self.rfFreqMhz-self.wbSampleRate/2e6, self.wbSampleRate/1e6/self.fftSize)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rfFreqMhz*1e6, self.nbSampleRate)
        self._cfg_rfFreqMhz_config = ConfigParser.ConfigParser()
        self._cfg_rfFreqMhz_config.read(self.configFilePath)
        if not self._cfg_rfFreqMhz_config.has_section('tuner'):
        	self._cfg_rfFreqMhz_config.add_section('tuner')
        self._cfg_rfFreqMhz_config.set('tuner', 'freq', str(self.rfFreqMhz))
        self._cfg_rfFreqMhz_config.write(open(self.configFilePath, 'w'))
        self.CyberRadio_generic_tuner_control_block_0.set_freq(self.rfFreqMhz)
        self.CyberRadio_freq_msg_converter_0_1.set_offset(self.rfFreqMhz*-1e0)
        self.CyberRadio_freq_msg_converter_0_0.set_offset(self.rfFreqMhz*1e6)
        self.CyberRadio_freq_msg_converter_0.set_offset(self.rfFreqMhz*-1e6)

    def get_refLevel(self):
        return self.refLevel

    def set_refLevel(self, refLevel):
        self.refLevel = refLevel
        self.qtgui_vector_sink_f_0.set_y_axis(self.refLevel-self.dynRange, self.refLevel)
        self._cfg_refLevel_config = ConfigParser.ConfigParser()
        self._cfg_refLevel_config.read(self.configFilePath)
        if not self._cfg_refLevel_config.has_section('display'):
        	self._cfg_refLevel_config.add_section('display')
        self._cfg_refLevel_config.set('display', 'ref_level', str(self.refLevel))
        self._cfg_refLevel_config.write(open(self.configFilePath, 'w'))

    def get_nbddcIndex(self):
        return self.nbddcIndex

    def set_nbddcIndex(self, nbddcIndex):
        self.nbddcIndex = nbddcIndex
        self._nbddcIndex_callback(self.nbddcIndex)
        self._cfg_nbddcIndex_config = ConfigParser.ConfigParser()
        self._cfg_nbddcIndex_config.read(self.configFilePath)
        if not self._cfg_nbddcIndex_config.has_section('nbddc'):
        	self._cfg_nbddcIndex_config.add_section('nbddc')
        self._cfg_nbddcIndex_config.set('nbddc', 'index', str(self.nbddcIndex))
        self._cfg_nbddcIndex_config.write(open(self.configFilePath, 'w'))
        self.CyberRadio_generic_ddc_control_block_0_0.set_index(self.nbddcIndex)

    def get_nbddcEnable(self):
        return self.nbddcEnable

    def set_nbddcEnable(self, nbddcEnable):
        self.nbddcEnable = nbddcEnable
        self.CyberRadio_generic_ddc_control_block_0_0.set_enable(self.nbddcEnable)

    def get_nbddcBwSet(self):
        return self.nbddcBwSet

    def set_nbddcBwSet(self, nbddcBwSet):
        self.nbddcBwSet = nbddcBwSet

    def get_nbSampleRate(self):
        return self.nbSampleRate

    def set_nbSampleRate(self, nbSampleRate):
        self.nbSampleRate = nbSampleRate
        self.qtgui_time_sink_x_0_0.set_y_axis(-self.nbSampleRate/2e3, self.nbSampleRate/2e3)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.nbSampleRate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.nbSampleRate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rfFreqMhz*1e6, self.nbSampleRate)
        self.blocks_multiply_const_vxx_0.set_k((self.nbSampleRate/(2e3*numpy.pi), ))

    def get_iirAlpha(self):
        return self.iirAlpha

    def set_iirAlpha(self, iirAlpha):
        self.iirAlpha = iirAlpha
        self.CyberRadio_log_mag_fft_0.set_iirAlpha(self.iirAlpha)

    def get_framesToSkip(self):
        return self.framesToSkip

    def set_framesToSkip(self, framesToSkip):
        self.framesToSkip = framesToSkip

    def get_fftWindow(self):
        return self.fftWindow

    def set_fftWindow(self, fftWindow):
        self.fftWindow = fftWindow

    def get_dynRange(self):
        return self.dynRange

    def set_dynRange(self, dynRange):
        self.dynRange = dynRange
        self.qtgui_vector_sink_f_0.set_y_axis(self.refLevel-self.dynRange, self.refLevel)
        self._cfg_dynRange_config = ConfigParser.ConfigParser()
        self._cfg_dynRange_config.read(self.configFilePath)
        if not self._cfg_dynRange_config.has_section('display'):
        	self._cfg_dynRange_config.add_section('display')
        self._cfg_dynRange_config.set('display', 'dyn_range', str(self.dynRange))
        self._cfg_dynRange_config.write(open(self.configFilePath, 'w'))

    def get_dispSize(self):
        return self.dispSize

    def set_dispSize(self, dispSize):
        self.dispSize = dispSize


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-R", "--fftRate", dest="fftRate", type="intx", default=16,
        help="Set fftRate [default=%default]")
    parser.add_option(
        "-F", "--fftSizeExponent", dest="fftSizeExponent", type="intx", default=15,
        help="Set FFT Size (<=17) [default=%default]")
    parser.add_option(
        "-w", "--fftWindowType", dest="fftWindowType", type="string", default='hann',
        help="Set FFT Window Type [default=%default]")
    parser.add_option(
        "-D", "--localDataInterface", dest="localDataInterface", type="string", default='',
        help="Set Local Data Interface [default=%default]")
    parser.add_option(
        "-d", "--radioDataPort", dest="radioDataPort", type="intx", default=2,
        help="Set Radio Data Port (-1 for auto select) [default=%default]")
    parser.add_option(
        "-n", "--radioHostname", dest="radioHostname", type="string", default='ndr301',
        help="Set Radio Hostname [default=%default]")
    parser.add_option(
        "-r", "--radioType", dest="radioType", type="string", default='ndr301',
        help="Set Radio Type [default=%default]")
    return parser


def main(top_block_cls=ndr_click2tune_test, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(fftRate=options.fftRate, fftSizeExponent=options.fftSizeExponent, fftWindowType=options.fftWindowType, localDataInterface=options.localDataInterface, radioDataPort=options.radioDataPort, radioHostname=options.radioHostname, radioType=options.radioType)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
