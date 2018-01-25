#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Freq Msg Strobe Test
# Author: NH
# Generated: Fri Nov  3 13:15:16 2017
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
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
import time
from gnuradio import qtgui


class frq_strobe_test(gr.top_block, Qt.QWidget):

    def __init__(self, radioHostname='192.168.0.20', radioType='ndr364'):
        gr.top_block.__init__(self, "Freq Msg Strobe Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Freq Msg Strobe Test")
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

        self.settings = Qt.QSettings("GNU Radio", "frq_strobe_test")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.radioHostname = radioHostname
        self.radioType = radioType

        ##################################################
        # Variables
        ##################################################
        self.radioObj = radioObj = crd.getRadioObject(radioType, verbose=bool(False), host=radioHostname)
        self.wbddcRateSet = wbddcRateSet = dict( [(k,v) for k,v in radioObj.getWbddcRateSet().iteritems() if radioObj.getDdcDataFormat(True).get(k,"iq")!="real"] )
        self.configFilePath = configFilePath = os.path.expanduser( os.path.join("~",".%s_demo.cfg"%(radioObj.name.lower(),)) )
        self._cfg_wbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_wbddcRateIndex_config.read(configFilePath)
        try: cfg_wbddcRateIndex = self._cfg_wbddcRateIndex_config.getint('wbddc', 'rate_index')
        except: cfg_wbddcRateIndex = sorted(wbddcRateSet.keys())[0]
        self.cfg_wbddcRateIndex = cfg_wbddcRateIndex
        self._cfg_iirAvgExp_config = ConfigParser.ConfigParser()
        self._cfg_iirAvgExp_config.read(configFilePath)
        try: cfg_iirAvgExp = self._cfg_iirAvgExp_config.getint('gui', 'iirAvgExp')
        except: cfg_iirAvgExp = int(3)
        self.cfg_iirAvgExp = cfg_iirAvgExp
        self.wbddcRateIndex = wbddcRateIndex = cfg_wbddcRateIndex
        self.wbddcBwSet = wbddcBwSet = dict( [(k,v) for k,v in radioObj.getWbddcBwSet().iteritems() if radioObj.getDdcDataFormat(True).get(k,"iq")!="real"] )
        self.iirAvgExp = iirAvgExp = cfg_iirAvgExp
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
        self._cfg_dynRange_config = ConfigParser.ConfigParser()
        self._cfg_dynRange_config.read(configFilePath)
        try: cfg_dynRange = self._cfg_dynRange_config.getint('display', 'dyn_range')
        except: cfg_dynRange = 120
        self.cfg_dynRange = cfg_dynRange
        self.wbSampleRate = wbSampleRate = wbddcRateSet[wbddcRateIndex]
        self.wbBw = wbBw = wbddcBwSet[wbddcRateIndex]
        self.udpBasePort = udpBasePort = 0xcafe
        self.tunerIndex = tunerIndex = cfg_tunerIndex
        self.tunerAtten = tunerAtten = cfg_tunerAtten
        self.samp_rate = samp_rate = 10e6
        self.rfFreqMhz = rfFreqMhz = cfg_rfFreqMhz
        self.refLevel = refLevel = cfg_refLevel
        self.pauseScan = pauseScan = False
        self.iirAlpha = iirAlpha = 2.0**(float(-iirAvgExp))
        self.fStep = fStep = 100
        self.f2 = f2 = int(radioObj.getTunerFrequencyRange()[1]/1e6)
        self.f1 = f1 = 100
        self.dynRange = dynRange = cfg_dynRange
        self.dwell = dwell = 0.5

        ##################################################
        # Blocks
        ##################################################
        self.wbTabs = Qt.QTabWidget()
        self.wbTabs_widget_0 = Qt.QWidget()
        self.wbTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.wbTabs_widget_0)
        self.wbTabs_grid_layout_0 = Qt.QGridLayout()
        self.wbTabs_layout_0.addLayout(self.wbTabs_grid_layout_0)
        self.wbTabs.addTab(self.wbTabs_widget_0, 'Spectrum')
        self.top_grid_layout.addWidget(self.wbTabs, 1,0,1,3)
        self.controlTabs = Qt.QTabWidget()
        self.controlTabs_widget_0 = Qt.QWidget()
        self.controlTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controlTabs_widget_0)
        self.controlTabs_grid_layout_0 = Qt.QGridLayout()
        self.controlTabs_layout_0.addLayout(self.controlTabs_grid_layout_0)
        self.controlTabs.addTab(self.controlTabs_widget_0, 'control')
        self.top_grid_layout.addWidget(self.controlTabs, 0,0,1,1)
        self._wbddcRateIndex_options = sorted(wbddcRateSet.keys())
        self._wbddcRateIndex_labels = ["%d: %ssps"%(k,num_to_str(wbddcRateSet[k])) for k in sorted(wbddcRateSet.keys())]
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
        self._tunerAtten_range = Range(int(radioObj.getTunerAttenuationRange()[0]), int(radioObj.getTunerAttenuationRange()[1]), int(radioObj.getTunerAttenuationRes()), cfg_tunerAtten, 200)
        self._tunerAtten_win = RangeWidget(self._tunerAtten_range, self.set_tunerAtten, 'Tuner Atten (dB)', "counter", int)
        self.controlTabs_grid_layout_0.addWidget(self._tunerAtten_win, 0,2,1,1)
        self._rfFreqMhz_range = Range(int(radioObj.getTunerFrequencyRange()[0]/1e6), int(radioObj.getTunerFrequencyRange()[1]/1e6), 10, cfg_rfFreqMhz, 200)
        self._rfFreqMhz_win = RangeWidget(self._rfFreqMhz_range, self.set_rfFreqMhz, 'Tuner Freq (MHz)', "counter_slider", int)
        self.controlTabs_grid_layout_0.addWidget(self._rfFreqMhz_win, 0,3,1,2)
        self._refLevel_range = Range(-120, +10, 5, cfg_refLevel, (130/5)+1)
        self._refLevel_win = RangeWidget(self._refLevel_range, self.set_refLevel, "Ref.\nLevel\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._refLevel_win, 0,1,1,1)
        self._pauseScan_options = (False, True, )
        self._pauseScan_labels = ('Run', 'Pause', )
        self._pauseScan_group_box = Qt.QGroupBox('Scan')
        self._pauseScan_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._pauseScan_button_group = variable_chooser_button_group()
        self._pauseScan_group_box.setLayout(self._pauseScan_box)
        for i, label in enumerate(self._pauseScan_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._pauseScan_box.addWidget(radio_button)
        	self._pauseScan_button_group.addButton(radio_button, i)
        self._pauseScan_callback = lambda i: Qt.QMetaObject.invokeMethod(self._pauseScan_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._pauseScan_options.index(i)))
        self._pauseScan_callback(self.pauseScan)
        self._pauseScan_button_group.buttonClicked[int].connect(
        	lambda i: self.set_pauseScan(self._pauseScan_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._pauseScan_group_box, 1,0,1,1)
        self._fStep_range = Range(1, 1000, 10, 100, 200)
        self._fStep_win = RangeWidget(self._fStep_range, self.set_fStep, 'Step (MHz)', "counter", float)
        self.controlTabs_grid_layout_0.addWidget(self._fStep_win, 1,3,1,1)
        self._f2_range = Range(int(radioObj.getTunerFrequencyRange()[0]/1e6), int(radioObj.getTunerFrequencyRange()[1]/1e6), 10, int(radioObj.getTunerFrequencyRange()[1]/1e6), 200)
        self._f2_win = RangeWidget(self._f2_range, self.set_f2, 'f2 (MHz)', "counter", float)
        self.controlTabs_grid_layout_0.addWidget(self._f2_win, 1,2,1,1)
        self._f1_range = Range(int(radioObj.getTunerFrequencyRange()[0]/1e6), int(radioObj.getTunerFrequencyRange()[1]/1e6), 10, 100, 200)
        self._f1_win = RangeWidget(self._f1_range, self.set_f1, 'f1 (MHz)', "counter", float)
        self.controlTabs_grid_layout_0.addWidget(self._f1_win, 1,1,1,1)
        self._dynRange_range = Range(5, 200, 5, cfg_dynRange, (195/5)+1)
        self._dynRange_win = RangeWidget(self._dynRange_range, self.set_dynRange, "Dyn.\nRange\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._dynRange_win, 1,1,1,1)
        self._dwell_range = Range(0.001, 10.0, 0.1, 0.5, 200)
        self._dwell_win = RangeWidget(self._dwell_range, self.set_dwell, 'dwell', "counter", float)
        self.controlTabs_grid_layout_0.addWidget(self._dwell_win, 1,4,1,1)
        self.z_tunerControl = CyberRadio.generic_tuner_control_block(
                    radioObj,
                    tunerIndex,
                    True,
                    1000,
                    tunerAtten,
                    1,
                    None,
                    {},
                    False
                     )
        self.y_ddcControl = CyberRadio.generic_ddc_control_block(
                    radioObj,
                    tunerIndex,
                    True,
                    True,
                    wbddcRateIndex,
                    0,
                    0,
                    tunerIndex,
                    0,
                    -1,
                    -1,
                    '',
                    udpBasePort,
                    {},
                    True
                     )
        self.uhd_usrp_sink_1 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		otw_format='sc8',
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_1.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_1.set_center_freq(uhd.tune_request_t((rfFreqMhz+1)*1e6, 2*samp_rate), 0)
        self.uhd_usrp_sink_1.set_gain(20, 0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	wbSampleRate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(1.0/32)
        self.qtgui_freq_sink_x_0.set_y_axis(refLevel-dynRange, refLevel)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
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
        colors = ["blue", "red", "green", "black", "cyan",
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
        self.wbTabs_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,3,1)
        self._iirAvgExp_range = Range(0, 8, 1, cfg_iirAvgExp, 200)
        self._iirAvgExp_win = RangeWidget(self._iirAvgExp_range, self.set_iirAvgExp, 'Avg.', "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._iirAvgExp_win, 2,1,1,1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, radioObj.getVitaPayloadSize()/4)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((0.7, ))
        self.blocks_message_debug_1 = blocks.message_debug()
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 0.1, 1, 0)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(1)
        self.CyberRadio_zero_copy_source_0 = CyberRadio.zero_copy_source(
              '255.255.255.255', udpBasePort,
              1, radioObj.getVitaHeaderSize(), radioObj.getVitaPayloadSize()/4,
              radioObj.isByteswapped(), radioObj.isIqSwapped(),
              "ip proto 17 and ip dst 255.255.255.255 and udp dst port %d"%(udpBasePort,), True,
               )
        self.CyberRadio_generic_group_control_block_0 = CyberRadio.generic_group_control_block(
                  radioObj,
                  0,
                  False,
                  True,
                  ([0,1,2,3,]),
                  {},
                  False,
                   )
        self.CyberRadio_freq_msg_strobe_0 = CyberRadio.freq_msg_strobe(
              pause = bool(pauseScan),
              f1 = f1,
              f2 = f2,
              step = fStep,
              dwell = dwell,
              wrap = True,
              fManual = rfFreqMhz,
              msgUnits = 1.0,
              msgRes = 1.0e6,
              debug = False,
               )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.CyberRadio_freq_msg_strobe_0, 'freq'), (self.uhd_usrp_sink_1, 'command'))
        self.msg_connect((self.CyberRadio_freq_msg_strobe_0, 'freq'), (self.z_tunerControl, 'freq'))
        self.msg_connect((self.y_ddcControl, 'status'), (self.blocks_message_debug_1, 'print'))
        self.msg_connect((self.z_tunerControl, 'freq'), (self.qtgui_freq_sink_x_0, 'freq'))
        self.connect((self.CyberRadio_zero_copy_source_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.uhd_usrp_sink_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_freq_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "frq_strobe_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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

    def get_cfg_iirAvgExp(self):
        return self.cfg_iirAvgExp

    def set_cfg_iirAvgExp(self, cfg_iirAvgExp):
        self.cfg_iirAvgExp = cfg_iirAvgExp
        self.set_iirAvgExp(self.cfg_iirAvgExp)

    def get_wbddcRateIndex(self):
        return self.wbddcRateIndex

    def set_wbddcRateIndex(self, wbddcRateIndex):
        self.wbddcRateIndex = wbddcRateIndex
        self._wbddcRateIndex_callback(self.wbddcRateIndex)
        self.set_wbSampleRate(self.wbddcRateSet[self.wbddcRateIndex])
        self.y_ddcControl.set_rate(self.wbddcRateIndex)
        self.set_wbBw(self.wbddcBwSet[self.wbddcRateIndex])
        self._cfg_wbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_wbddcRateIndex_config.read(self.configFilePath)
        if not self._cfg_wbddcRateIndex_config.has_section('wbddc'):
        	self._cfg_wbddcRateIndex_config.add_section('wbddc')
        self._cfg_wbddcRateIndex_config.set('wbddc', 'rate_index', str(self.wbddcRateIndex))
        self._cfg_wbddcRateIndex_config.write(open(self.configFilePath, 'w'))

    def get_wbddcBwSet(self):
        return self.wbddcBwSet

    def set_wbddcBwSet(self, wbddcBwSet):
        self.wbddcBwSet = wbddcBwSet
        self.set_wbBw(self.wbddcBwSet[self.wbddcRateIndex])

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

    def get_cfg_dynRange(self):
        return self.cfg_dynRange

    def set_cfg_dynRange(self, cfg_dynRange):
        self.cfg_dynRange = cfg_dynRange
        self.set_dynRange(self.cfg_dynRange)

    def get_wbSampleRate(self):
        return self.wbSampleRate

    def set_wbSampleRate(self, wbSampleRate):
        self.wbSampleRate = wbSampleRate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.wbSampleRate)

    def get_wbBw(self):
        return self.wbBw

    def set_wbBw(self, wbBw):
        self.wbBw = wbBw

    def get_udpBasePort(self):
        return self.udpBasePort

    def set_udpBasePort(self, udpBasePort):
        self.udpBasePort = udpBasePort
        self.y_ddcControl.set_udpPort(self.udpBasePort)

    def get_tunerIndex(self):
        return self.tunerIndex

    def set_tunerIndex(self, tunerIndex):
        self.tunerIndex = tunerIndex
        self._tunerIndex_callback(self.tunerIndex)
        self.z_tunerControl.set_index(self.tunerIndex)
        self.y_ddcControl.set_index(self.tunerIndex)
        self.y_ddcControl.set_rfSource(self.tunerIndex)
        self._cfg_tunerIndex_config = ConfigParser.ConfigParser()
        self._cfg_tunerIndex_config.read(self.configFilePath)
        if not self._cfg_tunerIndex_config.has_section('tuner'):
        	self._cfg_tunerIndex_config.add_section('tuner')
        self._cfg_tunerIndex_config.set('tuner', 'index', str(self.tunerIndex))
        self._cfg_tunerIndex_config.write(open(self.configFilePath, 'w'))

    def get_tunerAtten(self):
        return self.tunerAtten

    def set_tunerAtten(self, tunerAtten):
        self.tunerAtten = tunerAtten
        self.z_tunerControl.set_attenuation(self.tunerAtten)
        self._cfg_tunerAtten_config = ConfigParser.ConfigParser()
        self._cfg_tunerAtten_config.read(self.configFilePath)
        if not self._cfg_tunerAtten_config.has_section('tuner'):
        	self._cfg_tunerAtten_config.add_section('tuner')
        self._cfg_tunerAtten_config.set('tuner', 'atten', str(self.tunerAtten))
        self._cfg_tunerAtten_config.write(open(self.configFilePath, 'w'))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_1.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_1.set_center_freq(uhd.tune_request_t((self.rfFreqMhz+1)*1e6, 2*self.samp_rate), 0)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_rfFreqMhz(self):
        return self.rfFreqMhz

    def set_rfFreqMhz(self, rfFreqMhz):
        self.rfFreqMhz = rfFreqMhz
        self.uhd_usrp_sink_1.set_center_freq(uhd.tune_request_t((self.rfFreqMhz+1)*1e6, 2*self.samp_rate), 0)
        self._cfg_rfFreqMhz_config = ConfigParser.ConfigParser()
        self._cfg_rfFreqMhz_config.read(self.configFilePath)
        if not self._cfg_rfFreqMhz_config.has_section('tuner'):
        	self._cfg_rfFreqMhz_config.add_section('tuner')
        self._cfg_rfFreqMhz_config.set('tuner', 'freq', str(self.rfFreqMhz))
        self._cfg_rfFreqMhz_config.write(open(self.configFilePath, 'w'))
        self.CyberRadio_freq_msg_strobe_0.set_fManual(self.rfFreqMhz)

    def get_refLevel(self):
        return self.refLevel

    def set_refLevel(self, refLevel):
        self.refLevel = refLevel
        self.qtgui_freq_sink_x_0.set_y_axis(self.refLevel-self.dynRange, self.refLevel)
        self._cfg_refLevel_config = ConfigParser.ConfigParser()
        self._cfg_refLevel_config.read(self.configFilePath)
        if not self._cfg_refLevel_config.has_section('display'):
        	self._cfg_refLevel_config.add_section('display')
        self._cfg_refLevel_config.set('display', 'ref_level', str(self.refLevel))
        self._cfg_refLevel_config.write(open(self.configFilePath, 'w'))

    def get_pauseScan(self):
        return self.pauseScan

    def set_pauseScan(self, pauseScan):
        self.pauseScan = pauseScan
        self._pauseScan_callback(self.pauseScan)
        self.CyberRadio_freq_msg_strobe_0.set_pause(bool(self.pauseScan))

    def get_iirAlpha(self):
        return self.iirAlpha

    def set_iirAlpha(self, iirAlpha):
        self.iirAlpha = iirAlpha

    def get_fStep(self):
        return self.fStep

    def set_fStep(self, fStep):
        self.fStep = fStep
        self.CyberRadio_freq_msg_strobe_0.set_step(self.fStep)

    def get_f2(self):
        return self.f2

    def set_f2(self, f2):
        self.f2 = f2
        self.CyberRadio_freq_msg_strobe_0.set_f2(self.f2)

    def get_f1(self):
        return self.f1

    def set_f1(self, f1):
        self.f1 = f1
        self.CyberRadio_freq_msg_strobe_0.set_f1(self.f1)

    def get_dynRange(self):
        return self.dynRange

    def set_dynRange(self, dynRange):
        self.dynRange = dynRange
        self.qtgui_freq_sink_x_0.set_y_axis(self.refLevel-self.dynRange, self.refLevel)
        self._cfg_dynRange_config = ConfigParser.ConfigParser()
        self._cfg_dynRange_config.read(self.configFilePath)
        if not self._cfg_dynRange_config.has_section('display'):
        	self._cfg_dynRange_config.add_section('display')
        self._cfg_dynRange_config.set('display', 'dyn_range', str(self.dynRange))
        self._cfg_dynRange_config.write(open(self.configFilePath, 'w'))

    def get_dwell(self):
        return self.dwell

    def set_dwell(self, dwell):
        self.dwell = dwell
        self.CyberRadio_freq_msg_strobe_0.set_dwell(self.dwell)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-n", "--radioHostname", dest="radioHostname", type="string", default='192.168.0.20',
        help="Set Radio Hostname [default=%default]")
    parser.add_option(
        "-r", "--radioType", dest="radioType", type="string", default='ndr364',
        help="Set Radio Type [default=%default]")
    return parser


def main(top_block_cls=frq_strobe_test, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(radioHostname=options.radioHostname, radioType=options.radioType)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
