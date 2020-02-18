#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NDRxxx Continuous FFT Test
# Generated: Wed Nov 15 11:36:54 2017
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
from gnuradio import gr
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
import sys
from gnuradio import qtgui


class continuous_fft_demo(gr.top_block, Qt.QWidget):

    def __init__(self, debug=False, fftRate=50, fftSizeExponent=12, fftWindowType='hann', radioHostname='192.168.0.20', radioType='ndr364', threadsPerFft=1):
        gr.top_block.__init__(self, "NDRxxx Continuous FFT Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDRxxx Continuous FFT Test")
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

        self.settings = Qt.QSettings("GNU Radio", "continuous_fft_demo")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.debug = debug
        self.fftRate = fftRate
        self.fftSizeExponent = fftSizeExponent
        self.fftWindowType = fftWindowType
        self.radioHostname = radioHostname
        self.radioType = radioType
        self.threadsPerFft = threadsPerFft

        ##################################################
        # Variables
        ##################################################
        self.radioObj = radioObj = crd.getRadioObject(radioType, verbose=bool(bool(debug)), host=radioHostname)
        self.wbddcRateSet = wbddcRateSet = dict( [(k,v) for k,v in radioObj.getWbddcRateSet().iteritems() if radioObj.getDdcDataFormat(True).get(k,"iq")!="real"] )
        self._cfg_wbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_wbddcRateIndex_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        try: cfg_wbddcRateIndex = self._cfg_wbddcRateIndex_config.getint('wbddc', 'rate_index')
        except: cfg_wbddcRateIndex = sorted(wbddcRateSet.keys())[0]
        self.cfg_wbddcRateIndex = cfg_wbddcRateIndex
        self._cfg_iirAvgExp_config = ConfigParser.ConfigParser()
        self._cfg_iirAvgExp_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        try: cfg_iirAvgExp = self._cfg_iirAvgExp_config.getint('gui', 'iirAvgExp')
        except: cfg_iirAvgExp = int(3)
        self.cfg_iirAvgExp = cfg_iirAvgExp
        self.wbddcRateIndex = wbddcRateIndex = cfg_wbddcRateIndex
        self.iirAvgExp = iirAvgExp = cfg_iirAvgExp
        self.fftSize = fftSize = 1*(radioObj.getVitaPayloadSize()/4)
        self._cfg_tunerIndex_config = ConfigParser.ConfigParser()
        self._cfg_tunerIndex_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        try: cfg_tunerIndex = self._cfg_tunerIndex_config.getint('tuner', 'index')
        except: cfg_tunerIndex = radioObj.getTunerIndexRange()[0]
        self.cfg_tunerIndex = cfg_tunerIndex
        self._cfg_tunerAtten_config = ConfigParser.ConfigParser()
        self._cfg_tunerAtten_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        try: cfg_tunerAtten = self._cfg_tunerAtten_config.getint('tuner', 'atten')
        except: cfg_tunerAtten = int(radioObj.getTunerAttenuationRange()[0])
        self.cfg_tunerAtten = cfg_tunerAtten
        self._cfg_rfFreqMhz_config = ConfigParser.ConfigParser()
        self._cfg_rfFreqMhz_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        try: cfg_rfFreqMhz = self._cfg_rfFreqMhz_config.getint('tuner', 'freq')
        except: cfg_rfFreqMhz = int(radioObj.getTunerFrequencyRange()[0]/1e6)
        self.cfg_rfFreqMhz = cfg_rfFreqMhz
        self._cfg_refLevel_config = ConfigParser.ConfigParser()
        self._cfg_refLevel_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        try: cfg_refLevel = self._cfg_refLevel_config.getint('display', 'ref_level')
        except: cfg_refLevel = 0
        self.cfg_refLevel = cfg_refLevel
        self._cfg_dynRange_config = ConfigParser.ConfigParser()
        self._cfg_dynRange_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        try: cfg_dynRange = self._cfg_dynRange_config.getint('display', 'dyn_range')
        except: cfg_dynRange = 120
        self.cfg_dynRange = cfg_dynRange
        self.N = N = 8
        self.wolaWindow = wolaWindow = scipy.signal.get_window(fftWindowType,N*fftSize)
        self.wbSampleRate = wbSampleRate = wbddcRateSet[wbddcRateIndex]
        self.udpBasePort = udpBasePort = 44000
        self.tunerIndex = tunerIndex = cfg_tunerIndex
        self.tunerAtten = tunerAtten = cfg_tunerAtten
        self.rfFreqMhz = rfFreqMhz = cfg_rfFreqMhz
        self.refLevel = refLevel = cfg_refLevel
        self.nbddcRateSet = nbddcRateSet = radioObj.getNbddcRateSet()
        self.iirAlpha = iirAlpha = 2.0**(float(-iirAvgExp))
        self.fftWindow = fftWindow = scipy.signal.get_window(fftWindowType,fftSize)
        self.dynRange = dynRange = cfg_dynRange
        self.dispSize = dispSize = fftSize
        self.ddcEnable = ddcEnable = False

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
        self.wbTabs.addTab(self.wbTabs_widget_1, 'WOLA FFT')
        self.top_grid_layout.addWidget(self.wbTabs, 0,1,1,1)
        self.controlTabs = Qt.QTabWidget()
        self.controlTabs_widget_0 = Qt.QWidget()
        self.controlTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controlTabs_widget_0)
        self.controlTabs_grid_layout_0 = Qt.QGridLayout()
        self.controlTabs_layout_0.addLayout(self.controlTabs_grid_layout_0)
        self.controlTabs.addTab(self.controlTabs_widget_0, 'Control')
        self.top_grid_layout.addWidget(self.controlTabs, 1,1,1,1)
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
        self._tunerAtten_win = RangeWidget(self._tunerAtten_range, self.set_tunerAtten, "Tuner\nAtten.\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._tunerAtten_win, 3,1,1,1)
        self._rfFreqMhz_range = Range(int(radioObj.getTunerFrequencyRange()[0]/1e6), int(radioObj.getTunerFrequencyRange()[1]/1e6), 10, cfg_rfFreqMhz, 200)
        self._rfFreqMhz_win = RangeWidget(self._rfFreqMhz_range, self.set_rfFreqMhz, 'Tuner Freq (MHz)', "counter_slider", int)
        self.wbTabs_grid_layout_0.addWidget(self._rfFreqMhz_win, 3,0,1,1)
        self._ddcEnable_options = (False, True, )
        self._ddcEnable_labels = ('OFF', 'ON', )
        self._ddcEnable_group_box = Qt.QGroupBox('DDC Enable')
        self._ddcEnable_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ddcEnable_button_group = variable_chooser_button_group()
        self._ddcEnable_group_box.setLayout(self._ddcEnable_box)
        for i, label in enumerate(self._ddcEnable_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ddcEnable_box.addWidget(radio_button)
        	self._ddcEnable_button_group.addButton(radio_button, i)
        self._ddcEnable_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ddcEnable_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ddcEnable_options.index(i)))
        self._ddcEnable_callback(self.ddcEnable)
        self._ddcEnable_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ddcEnable(self._ddcEnable_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._ddcEnable_group_box, 0,2,1,1)
        self._refLevel_range = Range(-120, +10, 5, cfg_refLevel, (130/5)+1)
        self._refLevel_win = RangeWidget(self._refLevel_range, self.set_refLevel, "Ref.\nLevel\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._refLevel_win, 0,1,1,1)
        self._iirAvgExp_range = Range(0, 8, 1, cfg_iirAvgExp, 200)
        self._iirAvgExp_win = RangeWidget(self._iirAvgExp_range, self.set_iirAvgExp, 'Avg.', "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._iirAvgExp_win, 2,1,1,1)
        self._dynRange_range = Range(5, 200, 5, cfg_dynRange, (195/5)+1)
        self._dynRange_win = RangeWidget(self._dynRange_range, self.set_dynRange, "Dyn.\nRange\n(dB)", "dial", int)
        self.wbTabs_grid_layout_0.addWidget(self._dynRange_win, 1,1,1,1)
        self.blocks_probe_rate_0 = blocks.probe_rate(gr.sizeof_gr_complex*fftSize*N, 1000, 2.0**-4)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.CyberRadio_zero_copy_source_0 = CyberRadio.zero_copy_source(
              '255.255.255.255', udpBasePort,
              N, radioObj.getVitaHeaderSize()+8, radioObj.getVitaPayloadSize()/4,
              radioObj.isByteswapped(), radioObj.isIqSwapped(),
              '', N,
              False,
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
                    bool(debug)
                     )
        self.CyberRadio_generic_group_control_block_0 = CyberRadio.generic_group_control_block(
                  radioObj,
                  2,
                  False,
                  True,
                  ([0,1,2,3,]),
                  {},
                  bool(debug),
                   )
        self.CyberRadio_generic_ddc_control_block_0 = CyberRadio.generic_ddc_control_block(
                    radioObj,
                    tunerIndex,
                    ddcEnable,
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
                    bool(debug)
                     )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.CyberRadio_generic_ddc_control_block_0, 'status'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.blocks_probe_rate_0, 'rate'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.CyberRadio_zero_copy_source_0, 0), (self.blocks_probe_rate_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "continuous_fft_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_debug(self):
        return self.debug

    def set_debug(self, debug):
        self.debug = debug

    def get_fftRate(self):
        return self.fftRate

    def set_fftRate(self, fftRate):
        self.fftRate = fftRate

    def get_fftSizeExponent(self):
        return self.fftSizeExponent

    def set_fftSizeExponent(self, fftSizeExponent):
        self.fftSizeExponent = fftSizeExponent

    def get_fftWindowType(self):
        return self.fftWindowType

    def set_fftWindowType(self, fftWindowType):
        self.fftWindowType = fftWindowType
        self.set_wolaWindow(scipy.signal.get_window(self.fftWindowType,self.N*self.fftSize))
        self.set_fftWindow(scipy.signal.get_window(self.fftWindowType,self.fftSize))

    def get_radioHostname(self):
        return self.radioHostname

    def set_radioHostname(self, radioHostname):
        self.radioHostname = radioHostname

    def get_radioType(self):
        return self.radioType

    def set_radioType(self, radioType):
        self.radioType = radioType

    def get_threadsPerFft(self):
        return self.threadsPerFft

    def set_threadsPerFft(self, threadsPerFft):
        self.threadsPerFft = threadsPerFft

    def get_radioObj(self):
        return self.radioObj

    def set_radioObj(self, radioObj):
        self.radioObj = radioObj

    def get_wbddcRateSet(self):
        return self.wbddcRateSet

    def set_wbddcRateSet(self, wbddcRateSet):
        self.wbddcRateSet = wbddcRateSet
        self.set_wbSampleRate(self.wbddcRateSet[self.wbddcRateIndex])

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
        self._cfg_wbddcRateIndex_config = ConfigParser.ConfigParser()
        self._cfg_wbddcRateIndex_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        if not self._cfg_wbddcRateIndex_config.has_section('wbddc'):
        	self._cfg_wbddcRateIndex_config.add_section('wbddc')
        self._cfg_wbddcRateIndex_config.set('wbddc', 'rate_index', str(self.wbddcRateIndex))
        self._cfg_wbddcRateIndex_config.write(open(os.path.expanduser("~/.wbSpecSearch.cfg"), 'w'))
        self.CyberRadio_generic_ddc_control_block_0.set_rate(self.wbddcRateIndex)

    def get_iirAvgExp(self):
        return self.iirAvgExp

    def set_iirAvgExp(self, iirAvgExp):
        self.iirAvgExp = iirAvgExp
        self.set_iirAlpha(2.0**(float(-self.iirAvgExp)))
        self._cfg_iirAvgExp_config = ConfigParser.ConfigParser()
        self._cfg_iirAvgExp_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        if not self._cfg_iirAvgExp_config.has_section('gui'):
        	self._cfg_iirAvgExp_config.add_section('gui')
        self._cfg_iirAvgExp_config.set('gui', 'iirAvgExp', str(self.iirAvgExp))
        self._cfg_iirAvgExp_config.write(open(os.path.expanduser("~/.wbSpecSearch.cfg"), 'w'))

    def get_fftSize(self):
        return self.fftSize

    def set_fftSize(self, fftSize):
        self.fftSize = fftSize
        self.set_wolaWindow(scipy.signal.get_window(self.fftWindowType,self.N*self.fftSize))
        self.set_fftWindow(scipy.signal.get_window(self.fftWindowType,self.fftSize))
        self.set_dispSize(self.fftSize)

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

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.set_wolaWindow(scipy.signal.get_window(self.fftWindowType,self.N*self.fftSize))

    def get_wolaWindow(self):
        return self.wolaWindow

    def set_wolaWindow(self, wolaWindow):
        self.wolaWindow = wolaWindow

    def get_wbSampleRate(self):
        return self.wbSampleRate

    def set_wbSampleRate(self, wbSampleRate):
        self.wbSampleRate = wbSampleRate

    def get_udpBasePort(self):
        return self.udpBasePort

    def set_udpBasePort(self, udpBasePort):
        self.udpBasePort = udpBasePort
        self.CyberRadio_generic_ddc_control_block_0.set_udpPort(self.udpBasePort)

    def get_tunerIndex(self):
        return self.tunerIndex

    def set_tunerIndex(self, tunerIndex):
        self.tunerIndex = tunerIndex
        self._tunerIndex_callback(self.tunerIndex)
        self._cfg_tunerIndex_config = ConfigParser.ConfigParser()
        self._cfg_tunerIndex_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        if not self._cfg_tunerIndex_config.has_section('tuner'):
        	self._cfg_tunerIndex_config.add_section('tuner')
        self._cfg_tunerIndex_config.set('tuner', 'index', str(self.tunerIndex))
        self._cfg_tunerIndex_config.write(open(os.path.expanduser("~/.wbSpecSearch.cfg"), 'w'))
        self.CyberRadio_generic_tuner_control_block_0.set_index(self.tunerIndex)
        self.CyberRadio_generic_ddc_control_block_0.set_index(self.tunerIndex)
        self.CyberRadio_generic_ddc_control_block_0.set_rfSource(self.tunerIndex)

    def get_tunerAtten(self):
        return self.tunerAtten

    def set_tunerAtten(self, tunerAtten):
        self.tunerAtten = tunerAtten
        self._cfg_tunerAtten_config = ConfigParser.ConfigParser()
        self._cfg_tunerAtten_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        if not self._cfg_tunerAtten_config.has_section('tuner'):
        	self._cfg_tunerAtten_config.add_section('tuner')
        self._cfg_tunerAtten_config.set('tuner', 'atten', str(self.tunerAtten))
        self._cfg_tunerAtten_config.write(open(os.path.expanduser("~/.wbSpecSearch.cfg"), 'w'))
        self.CyberRadio_generic_tuner_control_block_0.set_attenuation(self.tunerAtten)

    def get_rfFreqMhz(self):
        return self.rfFreqMhz

    def set_rfFreqMhz(self, rfFreqMhz):
        self.rfFreqMhz = rfFreqMhz
        self._cfg_rfFreqMhz_config = ConfigParser.ConfigParser()
        self._cfg_rfFreqMhz_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        if not self._cfg_rfFreqMhz_config.has_section('tuner'):
        	self._cfg_rfFreqMhz_config.add_section('tuner')
        self._cfg_rfFreqMhz_config.set('tuner', 'freq', str(self.rfFreqMhz))
        self._cfg_rfFreqMhz_config.write(open(os.path.expanduser("~/.wbSpecSearch.cfg"), 'w'))
        self.CyberRadio_generic_tuner_control_block_0.set_freq(self.rfFreqMhz)

    def get_refLevel(self):
        return self.refLevel

    def set_refLevel(self, refLevel):
        self.refLevel = refLevel
        self._cfg_refLevel_config = ConfigParser.ConfigParser()
        self._cfg_refLevel_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        if not self._cfg_refLevel_config.has_section('display'):
        	self._cfg_refLevel_config.add_section('display')
        self._cfg_refLevel_config.set('display', 'ref_level', str(self.refLevel))
        self._cfg_refLevel_config.write(open(os.path.expanduser("~/.wbSpecSearch.cfg"), 'w'))

    def get_nbddcRateSet(self):
        return self.nbddcRateSet

    def set_nbddcRateSet(self, nbddcRateSet):
        self.nbddcRateSet = nbddcRateSet

    def get_iirAlpha(self):
        return self.iirAlpha

    def set_iirAlpha(self, iirAlpha):
        self.iirAlpha = iirAlpha

    def get_fftWindow(self):
        return self.fftWindow

    def set_fftWindow(self, fftWindow):
        self.fftWindow = fftWindow

    def get_dynRange(self):
        return self.dynRange

    def set_dynRange(self, dynRange):
        self.dynRange = dynRange
        self._cfg_dynRange_config = ConfigParser.ConfigParser()
        self._cfg_dynRange_config.read(os.path.expanduser("~/.wbSpecSearch.cfg"))
        if not self._cfg_dynRange_config.has_section('display'):
        	self._cfg_dynRange_config.add_section('display')
        self._cfg_dynRange_config.set('display', 'dyn_range', str(self.dynRange))
        self._cfg_dynRange_config.write(open(os.path.expanduser("~/.wbSpecSearch.cfg"), 'w'))

    def get_dispSize(self):
        return self.dispSize

    def set_dispSize(self, dispSize):
        self.dispSize = dispSize

    def get_ddcEnable(self):
        return self.ddcEnable

    def set_ddcEnable(self, ddcEnable):
        self.ddcEnable = ddcEnable
        self._ddcEnable_callback(self.ddcEnable)
        self.CyberRadio_generic_ddc_control_block_0.set_enable(self.ddcEnable)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-d", "--debug", dest="debug", type="intx", default=False,
        help="Set Debug? [default=%default]")
    parser.add_option(
        "-R", "--fftRate", dest="fftRate", type="intx", default=50,
        help="Set fftRate [default=%default]")
    parser.add_option(
        "-F", "--fftSizeExponent", dest="fftSizeExponent", type="intx", default=12,
        help="Set FFT Size (<=17) [default=%default]")
    parser.add_option(
        "-w", "--fftWindowType", dest="fftWindowType", type="string", default='hann',
        help="Set FFT Window Type [default=%default]")
    parser.add_option(
        "-n", "--radioHostname", dest="radioHostname", type="string", default='192.168.0.20',
        help="Set Radio Hostname [default=%default]")
    parser.add_option(
        "-r", "--radioType", dest="radioType", type="string", default='ndr364',
        help="Set Radio Type [default=%default]")
    parser.add_option(
        "-t", "--threadsPerFft", dest="threadsPerFft", type="intx", default=1,
        help="Set # of Threads per FFT [default=%default]")
    return parser


def main(top_block_cls=continuous_fft_demo, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(debug=options.debug, fftRate=options.fftRate, fftSizeExponent=options.fftSizeExponent, fftWindowType=options.fftWindowType, radioHostname=options.radioHostname, radioType=options.radioType, threadsPerFft=options.threadsPerFft)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
