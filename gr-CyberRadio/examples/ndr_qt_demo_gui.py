#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NDR Demo GUI (QT)
# Author: NH
# Generated: Wed Oct 25 10:00:56 2017
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
from gnuradio import qtgui
from gnuradio.eng_notation import num_to_str
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import CyberRadio
import CyberRadioDriver as crd
import os, datetime
import sip
import sys
import threading
import time
from gnuradio import qtgui


class ndr_qt_demo_gui(gr.top_block, Qt.QWidget):

    def __init__(self, basePort=22200, dataPort=1, hostnameOrDevice='/dev/ndr47x', ifname='eth6', radioType='ndr304', udpPortOrBaudrate=921600, verbose=1, vitaLevel=3, wbfftRate=8, wbfftSize=10, wideband2=0):
        gr.top_block.__init__(self, "NDR Demo GUI (QT)")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDR Demo GUI (QT)")
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

        self.settings = Qt.QSettings("GNU Radio", "ndr_qt_demo_gui")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.basePort = basePort
        self.dataPort = dataPort
        self.hostnameOrDevice = hostnameOrDevice
        self.ifname = ifname
        self.radioType = radioType
        self.udpPortOrBaudrate = udpPortOrBaudrate
        self.verbose = verbose
        self.vitaLevel = vitaLevel
        self.wbfftRate = wbfftRate
        self.wbfftSize = wbfftSize
        self.wideband2 = wideband2

        ##################################################
        # Variables
        ##################################################
        self.radioClass = radioClass = crd.getRadioClass(radioType,)
        self.ch2_wb = ch2_wb = bool(wideband2) or radioClass.getNumNbddc() == 0
        self.ch2_rateSet = ch2_rateSet = radioClass.getWbddcRateSet() if ch2_wb else radioClass.getNbddcRateSet()
        self.ch1_rateSet = ch1_rateSet = radioClass.getWbddcRateSet()
        self.ch2_rateIndex = ch2_rateIndex = sorted(ch2_rateSet.keys())[0]
        self.ch1_rateIndex = ch1_rateIndex = sorted(ch1_rateSet.keys())[0]
        self.radioRsp = radioRsp = ""
        self.macAndIpList = macAndIpList = crd.getInterfaceAddresses(ifname)
        self.ch2_rfAttenRange = ch2_rfAttenRange = [int(i) for i in radioClass.getTunerAttenuationRange()] if ch2_wb else [0,0]
        self.ch2_fs = ch2_fs = ch2_rateSet[ch2_rateIndex]
        self.ch2_channelList = ch2_channelList = radioClass.getWbddcIndexRange()[1::2] if ch2_wb else radioClass.getNbddcIndexRange()
        self.ch1_updateRate = ch1_updateRate = wbfftRate
        self.ch1_fs = ch1_fs = ch1_rateSet[ch1_rateIndex]
        self.ch1_fftSize = ch1_fftSize = int( 2**wbfftSize )
        self.ch1_channelList = ch1_channelList = radioClass.getWbddcIndexRange()[0::2] if ch2_wb else radioClass.getWbddcIndexRange()
        self.udpPortList = udpPortList = [basePort,basePort+1]
        self.radioRspDisplay = radioRspDisplay = radioRsp
        self.radioCmd = radioCmd = ''
        self.logfile = logfile = os.path.join("/public","ndrDemoGui","ndrCmd.%s.log"%datetime.datetime.now().strftime("%y%m%d-%H%M%S"))
        self.ipAddress = ipAddress = macAndIpList[1]
        self.fftColSpan = fftColSpan = 6
        self.ch2_updateRate = ch2_updateRate = ch1_updateRate if ch2_wb else 4*ch1_updateRate
        self.ch2_rfFreqRange = ch2_rfFreqRange = [int(i/1e6) for i in radioClass.getTunerFrequencyRange()] if ch2_wb else [0,0]
        self.ch2_rfFreq = ch2_rfFreq = int(sum(radioClass.getTunerFrequencyRange())/2e6) if ch2_wb else 0
        self.ch2_rfAtten = ch2_rfAtten = ch2_rfAttenRange[0]
        self.ch2_index = ch2_index = ch2_channelList[0]
        self.ch2_fsLabel = ch2_fsLabel = "%sHz"%( num_to_str(ch2_fs) )
        self.ch2_fftSize = ch2_fftSize = ch1_fftSize if ch2_wb else ch1_fftSize/2
        self.ch2_ddcFreq = ch2_ddcFreq = 0
        self.ch1_rfFreq = ch1_rfFreq = int(sum(radioClass.getTunerFrequencyRange())/2e6)
        self.ch1_rfAtten = ch1_rfAtten = int(radioClass.getTunerAttenuationRange()[0])
        self.ch1_index = ch1_index = ch1_channelList[0]
        self.ch1_fsLabel = ch1_fsLabel = "%sHz"%( num_to_str(ch1_fs) )
        self.ch1_ddcFreq = ch1_ddcFreq = 0

        ##################################################
        # Blocks
        ##################################################
        self._ch2_rfFreq_range = Range(int(radioClass.getTunerFrequencyRange()[0]/1e6) if ch2_wb else 0, int(radioClass.getTunerFrequencyRange()[1]/1e6) if ch2_wb else 0, 20, int(sum(radioClass.getTunerFrequencyRange())/2e6) if ch2_wb else 0, 200)
        self._ch2_rfFreq_win = RangeWidget(self._ch2_rfFreq_range, self.set_ch2_rfFreq, 'RF Freq (MHz)', "counter_slider", int)
        self.top_grid_layout.addWidget(self._ch2_rfFreq_win, 2,fftColSpan+0,1,fftColSpan/2)
        self._ch2_rfAtten_range = Range(ch2_rfAttenRange[0], ch2_rfAttenRange[1], 1, ch2_rfAttenRange[0], 200)
        self._ch2_rfAtten_win = RangeWidget(self._ch2_rfAtten_range, self.set_ch2_rfAtten, 'RF Atten (dB)', "counter_slider", int)
        self.top_grid_layout.addWidget(self._ch2_rfAtten_win, 2,fftColSpan+fftColSpan/2,1,fftColSpan/2)
        self._ch2_rateIndex_options = sorted(ch2_rateSet.keys())
        self._ch2_rateIndex_labels = map(str, self._ch2_rateIndex_options)
        self._ch2_rateIndex_tool_bar = Qt.QToolBar(self)
        self._ch2_rateIndex_tool_bar.addWidget(Qt.QLabel('Rate Index'+": "))
        self._ch2_rateIndex_combo_box = Qt.QComboBox()
        self._ch2_rateIndex_tool_bar.addWidget(self._ch2_rateIndex_combo_box)
        for label in self._ch2_rateIndex_labels: self._ch2_rateIndex_combo_box.addItem(label)
        self._ch2_rateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch2_rateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ch2_rateIndex_options.index(i)))
        self._ch2_rateIndex_callback(self.ch2_rateIndex)
        self._ch2_rateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_ch2_rateIndex(self._ch2_rateIndex_options[i]))
        self.top_grid_layout.addWidget(self._ch2_rateIndex_tool_bar, 1,fftColSpan+1,1,1)
        self._ch2_index_options = ch2_channelList
        self._ch2_index_labels = map(str, self._ch2_index_options)
        self._ch2_index_tool_bar = Qt.QToolBar(self)
        self._ch2_index_tool_bar.addWidget(Qt.QLabel("%sDDC"%("WB" if ch2_wb else "NB")+": "))
        self._ch2_index_combo_box = Qt.QComboBox()
        self._ch2_index_tool_bar.addWidget(self._ch2_index_combo_box)
        for label in self._ch2_index_labels: self._ch2_index_combo_box.addItem(label)
        self._ch2_index_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch2_index_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ch2_index_options.index(i)))
        self._ch2_index_callback(self.ch2_index)
        self._ch2_index_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_ch2_index(self._ch2_index_options[i]))
        self.top_grid_layout.addWidget(self._ch2_index_tool_bar, 1,fftColSpan+0,1,1)
        self._ch2_ddcFreq_range = Range((radioClass.getWbddcFrequencyRange() if ch2_wb else radioClass.getNbddcFrequencyRange())[0]/1e3, (radioClass.getWbddcFrequencyRange() if ch2_wb else radioClass.getNbddcFrequencyRange())[1]/1e3, 10, 0, 200)
        self._ch2_ddcFreq_win = RangeWidget(self._ch2_ddcFreq_range, self.set_ch2_ddcFreq, 'Freq (kHz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._ch2_ddcFreq_win, 1,fftColSpan+fftColSpan/2,1,fftColSpan/2)
        self._ch1_rfFreq_range = Range(int(radioClass.getTunerFrequencyRange()[0]/1e6), int(radioClass.getTunerFrequencyRange()[1]/1e6), 20, int(sum(radioClass.getTunerFrequencyRange())/2e6), 200)
        self._ch1_rfFreq_win = RangeWidget(self._ch1_rfFreq_range, self.set_ch1_rfFreq, 'RF Freq (MHz)', "counter_slider", int)
        self.top_grid_layout.addWidget(self._ch1_rfFreq_win, 2,0,1,fftColSpan/2)
        self._ch1_rfAtten_range = Range(int(radioClass.getTunerAttenuationRange()[0]), int(radioClass.getTunerAttenuationRange()[1]), 1, int(radioClass.getTunerAttenuationRange()[0]), 200)
        self._ch1_rfAtten_win = RangeWidget(self._ch1_rfAtten_range, self.set_ch1_rfAtten, 'RF Atten (dB)', "counter_slider", int)
        self.top_grid_layout.addWidget(self._ch1_rfAtten_win, 2,fftColSpan/2,1,fftColSpan/2)
        self._ch1_rateIndex_options = sorted(ch1_rateSet.keys())
        self._ch1_rateIndex_labels = map(str, self._ch1_rateIndex_options)
        self._ch1_rateIndex_tool_bar = Qt.QToolBar(self)
        self._ch1_rateIndex_tool_bar.addWidget(Qt.QLabel('Rate Index'+": "))
        self._ch1_rateIndex_combo_box = Qt.QComboBox()
        self._ch1_rateIndex_tool_bar.addWidget(self._ch1_rateIndex_combo_box)
        for label in self._ch1_rateIndex_labels: self._ch1_rateIndex_combo_box.addItem(label)
        self._ch1_rateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch1_rateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ch1_rateIndex_options.index(i)))
        self._ch1_rateIndex_callback(self.ch1_rateIndex)
        self._ch1_rateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_ch1_rateIndex(self._ch1_rateIndex_options[i]))
        self.top_grid_layout.addWidget(self._ch1_rateIndex_tool_bar, 1,1,1,1)
        self._ch1_index_options = ch1_channelList
        self._ch1_index_labels = map(str, self._ch1_index_options)
        self._ch1_index_tool_bar = Qt.QToolBar(self)
        self._ch1_index_tool_bar.addWidget(Qt.QLabel('WBDDC'+": "))
        self._ch1_index_combo_box = Qt.QComboBox()
        self._ch1_index_tool_bar.addWidget(self._ch1_index_combo_box)
        for label in self._ch1_index_labels: self._ch1_index_combo_box.addItem(label)
        self._ch1_index_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch1_index_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ch1_index_options.index(i)))
        self._ch1_index_callback(self.ch1_index)
        self._ch1_index_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_ch1_index(self._ch1_index_options[i]))
        self.top_grid_layout.addWidget(self._ch1_index_tool_bar, 1,0,1,1)
        self._ch1_ddcFreq_range = Range(radioClass.getWbddcFrequencyRange()[0]/1e3, radioClass.getWbddcFrequencyRange()[1]/1e3, 10, 0, 200)
        self._ch1_ddcFreq_win = RangeWidget(self._ch1_ddcFreq_range, self.set_ch1_ddcFreq, 'Freq (kHz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._ch1_ddcFreq_win, 1,fftColSpan/2,1,fftColSpan/2)
        self.ndrDemoControlBlock = CyberRadio.NDR_demo_control(
                    radio_type = str(radioType),
                    radio_hostname = str(hostnameOrDevice),
                    radio_port = int(udpPortOrBaudrate),
                    tuner1_index = ch1_index,
                    tuner1_freq = float( 1e6*ch1_rfFreq ),
                    tuner1_atten = ch1_rfAtten,
                    tuner2_index = ch2_index if ch2_wb else -1,
                    tuner2_freq = float( 1e6*ch2_rfFreq ),
                    tuner2_atten = ch2_rfAtten,
                    ddc1_index = ch1_index,
                    ddc1_wideband = True,
                    ddc1_enable = True,
                    ddc1_vita49_level = vitaLevel,
                    ddc1_rate_index = ch1_rateIndex,
                    ddc1_freq = ch1_ddcFreq*1e3,
                    ddc1_udp_port = udpPortList[0],
                    ddc1_rf_source = -1,
                    ddc1_data_port = dataPort,
                    ddc2_index = ch2_index,
                    ddc2_wideband = ch2_wb,
                    ddc2_enable = True,
                    ddc2_vita49_level = vitaLevel,
                    ddc2_rate_index = ch2_rateIndex,
                    ddc2_freq = 1e3*ch2_ddcFreq,
                    ddc2_udp_port = udpPortList[1],
                    ddc2_rf_source = -1 if ch2_wb else ch1_index,
                    ddc2_data_port = dataPort,
                    cal_freq = 0.0,
                    interface_dict = {dataPort:str(ifname)},
                    verbose = bool(verbose),
                    other_args = {}
                    )
        self.ch2_tabs = Qt.QTabWidget()
        self.ch2_tabs_widget_0 = Qt.QWidget()
        self.ch2_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.ch2_tabs_widget_0)
        self.ch2_tabs_grid_layout_0 = Qt.QGridLayout()
        self.ch2_tabs_layout_0.addLayout(self.ch2_tabs_grid_layout_0)
        self.ch2_tabs.addTab(self.ch2_tabs_widget_0, 'Spectrum')
        self.ch2_tabs_widget_1 = Qt.QWidget()
        self.ch2_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.ch2_tabs_widget_1)
        self.ch2_tabs_grid_layout_1 = Qt.QGridLayout()
        self.ch2_tabs_layout_1.addLayout(self.ch2_tabs_grid_layout_1)
        self.ch2_tabs.addTab(self.ch2_tabs_widget_1, 'Time')
        self.top_grid_layout.addWidget(self.ch2_tabs, 0,fftColSpan,1,fftColSpan)
        self.ch1_tabs = Qt.QTabWidget()
        self.ch1_tabs_widget_0 = Qt.QWidget()
        self.ch1_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.ch1_tabs_widget_0)
        self.ch1_tabs_grid_layout_0 = Qt.QGridLayout()
        self.ch1_tabs_layout_0.addLayout(self.ch1_tabs_grid_layout_0)
        self.ch1_tabs.addTab(self.ch1_tabs_widget_0, 'Spectrum')
        self.ch1_tabs_widget_1 = Qt.QWidget()
        self.ch1_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.ch1_tabs_widget_1)
        self.ch1_tabs_grid_layout_1 = Qt.QGridLayout()
        self.ch1_tabs_layout_1.addLayout(self.ch1_tabs_grid_layout_1)
        self.ch1_tabs.addTab(self.ch1_tabs_widget_1, 'Waterfall')
        self.top_grid_layout.addWidget(self.ch1_tabs, 0,0,1,fftColSpan)
        self._radioRspDisplay_tool_bar = Qt.QToolBar(self)
        self._radioRspDisplay_tool_bar.addWidget(Qt.QLabel('Command Response'+": "))
        self._radioRspDisplay_line_edit = Qt.QLineEdit(str(self.radioRspDisplay))
        self._radioRspDisplay_tool_bar.addWidget(self._radioRspDisplay_line_edit)
        self._radioRspDisplay_line_edit.returnPressed.connect(
        	lambda: self.set_radioRspDisplay(str(str(self._radioRspDisplay_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._radioRspDisplay_tool_bar, 3,2,1,2*fftColSpan-2)

        def _radioRsp_probe():
            while True:
                val = self.ndrDemoControlBlock.get_radio_rsp()
                try:
                    self.set_radioRsp(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _radioRsp_thread = threading.Thread(target=_radioRsp_probe)
        _radioRsp_thread.daemon = True
        _radioRsp_thread.start()

        self._radioCmd_tool_bar = Qt.QToolBar(self)
        self._radioCmd_tool_bar.addWidget(Qt.QLabel('Manual Command'+": "))
        self._radioCmd_line_edit = Qt.QLineEdit(str(self.radioCmd))
        self._radioCmd_tool_bar.addWidget(self._radioCmd_line_edit)
        self._radioCmd_line_edit.returnPressed.connect(
        	lambda: self.set_radioCmd(str(str(self._radioCmd_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._radioCmd_tool_bar, 3,0,1,2)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	ch1_fftSize, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	ch1_rfFreq*1e6 + ch1_ddcFreq*1e3, #fc
        	ch1_fs, #bw
        	'Ch 1 (Wideband)', #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(1.0/ch1_updateRate)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [5, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-120, 0)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.ch1_tabs_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	ch2_fs, #samp_rate
        	"", #name
        	1 #number of inputs
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

        if not False:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
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

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.ch2_tabs_layout_1.addWidget(self._qtgui_time_sink_x_0_win)
        self._ch2_fsLabel_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch2_fsLabel_formatter = None
        else:
          self._ch2_fsLabel_formatter = lambda x: x

        self._ch2_fsLabel_tool_bar.addWidget(Qt.QLabel('fs'+": "))
        self._ch2_fsLabel_label = Qt.QLabel(str(self._ch2_fsLabel_formatter(self.ch2_fsLabel)))
        self._ch2_fsLabel_tool_bar.addWidget(self._ch2_fsLabel_label)
        self.top_grid_layout.addWidget(self._ch2_fsLabel_tool_bar, 1,fftColSpan+2,1,1)

        self.ch2_fftDisplay = qtgui.freq_sink_c(
        	ch2_fftSize, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	(ch2_rfFreq if ch2_wb else ch1_rfFreq)*1e6 + ch2_ddcFreq*1e3, #fc
        	ch2_fs, #bw
        	"Channel 2 (%sband)"%("Wide" if ch2_wb else "Narrow"), #name
        	1 #number of inputs
        )
        self.ch2_fftDisplay.set_update_time(1.0/ch2_updateRate)
        self.ch2_fftDisplay.set_y_axis(-120, 0)
        self.ch2_fftDisplay.set_y_label('Relative Gain', 'dB')
        self.ch2_fftDisplay.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.ch2_fftDisplay.enable_autoscale(False)
        self.ch2_fftDisplay.enable_grid(True)
        self.ch2_fftDisplay.set_fft_average(0.2)
        self.ch2_fftDisplay.enable_axis_labels(True)
        self.ch2_fftDisplay.enable_control_panel(False)

        if not False:
          self.ch2_fftDisplay.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.ch2_fftDisplay.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.ch2_fftDisplay.set_line_label(i, "Data {0}".format(i))
            else:
                self.ch2_fftDisplay.set_line_label(i, labels[i])
            self.ch2_fftDisplay.set_line_width(i, widths[i])
            self.ch2_fftDisplay.set_line_color(i, colors[i])
            self.ch2_fftDisplay.set_line_alpha(i, alphas[i])

        self._ch2_fftDisplay_win = sip.wrapinstance(self.ch2_fftDisplay.pyqwidget(), Qt.QWidget)
        self.ch2_tabs_layout_0.addWidget(self._ch2_fftDisplay_win)
        self._ch1_fsLabel_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_fsLabel_formatter = None
        else:
          self._ch1_fsLabel_formatter = lambda x: x

        self._ch1_fsLabel_tool_bar.addWidget(Qt.QLabel('fs'+": "))
        self._ch1_fsLabel_label = Qt.QLabel(str(self._ch1_fsLabel_formatter(self.ch1_fsLabel)))
        self._ch1_fsLabel_tool_bar.addWidget(self._ch1_fsLabel_label)
        self.top_grid_layout.addWidget(self._ch1_fsLabel_tool_bar, 1,2,1,1)

        self.ch1_fftDisplay = qtgui.freq_sink_c(
        	ch1_fftSize, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	ch1_rfFreq*1e6 + ch1_ddcFreq*1e3, #fc
        	ch1_fs, #bw
        	'Channel 1 (Wideband)', #name
        	1 #number of inputs
        )
        self.ch1_fftDisplay.set_update_time(1.0/ch1_updateRate)
        self.ch1_fftDisplay.set_y_axis(-120, 0)
        self.ch1_fftDisplay.set_y_label('Relative Gain', 'dB')
        self.ch1_fftDisplay.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.ch1_fftDisplay.enable_autoscale(False)
        self.ch1_fftDisplay.enable_grid(True)
        self.ch1_fftDisplay.set_fft_average(0.2)
        self.ch1_fftDisplay.enable_axis_labels(True)
        self.ch1_fftDisplay.enable_control_panel(False)

        if not False:
          self.ch1_fftDisplay.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.ch1_fftDisplay.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.ch1_fftDisplay.set_line_label(i, "Data {0}".format(i))
            else:
                self.ch1_fftDisplay.set_line_label(i, labels[i])
            self.ch1_fftDisplay.set_line_width(i, widths[i])
            self.ch1_fftDisplay.set_line_color(i, colors[i])
            self.ch1_fftDisplay.set_line_alpha(i, alphas[i])

        self._ch1_fftDisplay_win = sip.wrapinstance(self.ch1_fftDisplay.pyqwidget(), Qt.QWidget)
        self.ch1_tabs_layout_0.addWidget(self._ch1_fftDisplay_win)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, logfile, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_file_descriptor_sink_0 = blocks.file_descriptor_sink(gr.sizeof_char*1, 1)
        uses_v491 = radioType.strip().lower() not in ["ndr354", "ndr364"]
        self.CyberRadio_vita_udp_rx_0 = CyberRadio.vita_udp_rx(macAndIpList[1], udpPortList[0], radioClass.getVitaHeaderSize(), radioClass.getVitaPayloadSize()/4, radioClass.getVitaHeaderSize()+radioClass.getVitaPayloadSize()+radioClass.getVitaTailSize(), radioClass.isByteswapped(), radioClass.isIqSwapped(), False, False, uses_v491)
        self.CyberRadio_vita_udp_rx_1 = CyberRadio.vita_udp_rx(macAndIpList[1], udpPortList[1], radioClass.getVitaHeaderSize(), radioClass.getVitaPayloadSize()/4, radioClass.getVitaHeaderSize()+radioClass.getVitaPayloadSize()+radioClass.getVitaTailSize(), radioClass.isByteswapped(), radioClass.isIqSwapped(), False, False, uses_v491)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.CyberRadio_vita_udp_rx_0, 0), (self.ch1_fftDisplay, 0))
        self.connect((self.CyberRadio_vita_udp_rx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.CyberRadio_vita_udp_rx_1, 0), (self.ch2_fftDisplay, 0))
        self.connect((self.CyberRadio_vita_udp_rx_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.ndrDemoControlBlock, 0), (self.blocks_file_descriptor_sink_0, 0))
        self.connect((self.ndrDemoControlBlock, 0), (self.blocks_file_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ndr_qt_demo_gui")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_basePort(self):
        return self.basePort

    def set_basePort(self, basePort):
        self.basePort = basePort
        self.set_udpPortList([self.basePort,self.basePort+1])

    def get_dataPort(self):
        return self.dataPort

    def set_dataPort(self, dataPort):
        self.dataPort = dataPort
        self.ndrDemoControlBlock.set_ddc1_data_port(self.dataPort)
        self.ndrDemoControlBlock.set_ddc2_data_port(self.dataPort)

    def get_hostnameOrDevice(self):
        return self.hostnameOrDevice

    def set_hostnameOrDevice(self, hostnameOrDevice):
        self.hostnameOrDevice = hostnameOrDevice

    def get_ifname(self):
        return self.ifname

    def set_ifname(self, ifname):
        self.ifname = ifname
        self.set_macAndIpList(crd.getInterfaceAddresses(self.ifname))

    def get_radioType(self):
        return self.radioType

    def set_radioType(self, radioType):
        self.radioType = radioType
        self.set_radioClass(crd.getRadioClass(self.radioType,))

    def get_udpPortOrBaudrate(self):
        return self.udpPortOrBaudrate

    def set_udpPortOrBaudrate(self, udpPortOrBaudrate):
        self.udpPortOrBaudrate = udpPortOrBaudrate

    def get_verbose(self):
        return self.verbose

    def set_verbose(self, verbose):
        self.verbose = verbose

    def get_vitaLevel(self):
        return self.vitaLevel

    def set_vitaLevel(self, vitaLevel):
        self.vitaLevel = vitaLevel
        self.ndrDemoControlBlock.set_ddc1_vita49_level(self.vitaLevel)
        self.ndrDemoControlBlock.set_ddc2_vita49_level(self.vitaLevel)

    def get_wbfftRate(self):
        return self.wbfftRate

    def set_wbfftRate(self, wbfftRate):
        self.wbfftRate = wbfftRate
        self.set_ch1_updateRate(self.wbfftRate)

    def get_wbfftSize(self):
        return self.wbfftSize

    def set_wbfftSize(self, wbfftSize):
        self.wbfftSize = wbfftSize
        self.set_ch1_fftSize(int( 2**self.wbfftSize ))

    def get_wideband2(self):
        return self.wideband2

    def set_wideband2(self, wideband2):
        self.wideband2 = wideband2
        self.set_ch2_wb(bool(self.wideband2) or radioType.strip().lower() in ("ndr304","ndr472"))

    def get_radioClass(self):
        return self.radioClass

    def set_radioClass(self, radioClass):
        self.radioClass = radioClass

    def get_ch2_wb(self):
        return self.ch2_wb

    def set_ch2_wb(self, ch2_wb):
        self.ch2_wb = ch2_wb
        self.set_ch2_rateSet(radioClass.getWbddcRateSet() if self.ch2_wb else radioClass.getNbddcRateSet())
        self.set_ch2_channelList(radioClass.getWbddcIndexRange()[1::2] if self.ch2_wb else radioClass.getNbddcIndexRange())
        self.set_ch1_channelList(radioClass.getWbddcIndexRange()[0::2] if self.ch2_wb else radioClass.getWbddcIndexRange())
        self.set_ch2_rfFreq(int(sum(radioClass.getTunerFrequencyRange())/2e6) if self.ch2_wb else 0)
        self.ndrDemoControlBlock.set_tuner2_index(self.ch2_index if self.ch2_wb else -1)
        self.ndrDemoControlBlock.set_ddc2_wideband(self.ch2_wb)
        self.ndrDemoControlBlock.set_ddc2_rf_source(-1 if self.ch2_wb else self.ch1_index)
        self.set_ch2_updateRate(self.ch1_updateRate if self.ch2_wb else 4*self.ch1_updateRate)
        self.set_ch2_fftSize(self.ch1_fftSize if self.ch2_wb else self.ch1_fftSize/2)
        self.set_ch2_rfFreqRange([int(i/1e6) for i in radioClass.getTunerFrequencyRange()] if self.ch2_wb else [0,0])
        self.set_ch2_rfAttenRange([int(i) for i in radioClass.getTunerAttenuationRange()] if self.ch2_wb else [0,0])
        self.ch2_fftDisplay.set_frequency_range((self.ch2_rfFreq if self.ch2_wb else self.ch1_rfFreq)*1e6 + self.ch2_ddcFreq*1e3, self.ch2_fs)

    def get_ch2_rateSet(self):
        return self.ch2_rateSet

    def set_ch2_rateSet(self, ch2_rateSet):
        self.ch2_rateSet = ch2_rateSet
        self.set_ch2_fs(self.ch2_rateSet[self.ch2_rateIndex])

    def get_ch1_rateSet(self):
        return self.ch1_rateSet

    def set_ch1_rateSet(self, ch1_rateSet):
        self.ch1_rateSet = ch1_rateSet
        self.set_ch1_fs(self.ch1_rateSet[self.ch1_rateIndex])

    def get_ch2_rateIndex(self):
        return self.ch2_rateIndex

    def set_ch2_rateIndex(self, ch2_rateIndex):
        self.ch2_rateIndex = ch2_rateIndex
        self._ch2_rateIndex_callback(self.ch2_rateIndex)
        self.ndrDemoControlBlock.set_ddc2_rate_index(self.ch2_rateIndex)
        self.set_ch2_fs(self.ch2_rateSet[self.ch2_rateIndex])

    def get_ch1_rateIndex(self):
        return self.ch1_rateIndex

    def set_ch1_rateIndex(self, ch1_rateIndex):
        self.ch1_rateIndex = ch1_rateIndex
        self._ch1_rateIndex_callback(self.ch1_rateIndex)
        self.ndrDemoControlBlock.set_ddc1_rate_index(self.ch1_rateIndex)
        self.set_ch1_fs(self.ch1_rateSet[self.ch1_rateIndex])

    def get_radioRsp(self):
        return self.radioRsp

    def set_radioRsp(self, radioRsp):
        self.radioRsp = radioRsp
        self.set_radioRspDisplay(self.radioRsp)

    def get_macAndIpList(self):
        return self.macAndIpList

    def set_macAndIpList(self, macAndIpList):
        self.macAndIpList = macAndIpList
        self.set_ipAddress(self.macAndIpList[1])

    def get_ch2_rfAttenRange(self):
        return self.ch2_rfAttenRange

    def set_ch2_rfAttenRange(self, ch2_rfAttenRange):
        self.ch2_rfAttenRange = ch2_rfAttenRange
        self.set_ch2_rfAtten(self.ch2_rfAttenRange[0])

    def get_ch2_fs(self):
        return self.ch2_fs

    def set_ch2_fs(self, ch2_fs):
        self.ch2_fs = ch2_fs
        self.qtgui_time_sink_x_0.set_samp_rate(self.ch2_fs)
        self.set_ch2_fsLabel(self._ch2_fsLabel_formatter("%sHz"%( num_to_str(self.ch2_fs) )))
        self.ch2_fftDisplay.set_frequency_range((self.ch2_rfFreq if self.ch2_wb else self.ch1_rfFreq)*1e6 + self.ch2_ddcFreq*1e3, self.ch2_fs)

    def get_ch2_channelList(self):
        return self.ch2_channelList

    def set_ch2_channelList(self, ch2_channelList):
        self.ch2_channelList = ch2_channelList
        self.set_ch2_index(self.ch2_channelList[0])

    def get_ch1_updateRate(self):
        return self.ch1_updateRate

    def set_ch1_updateRate(self, ch1_updateRate):
        self.ch1_updateRate = ch1_updateRate
        self.set_ch2_updateRate(self.ch1_updateRate if self.ch2_wb else 4*self.ch1_updateRate)
        self.qtgui_waterfall_sink_x_0.set_update_time(1.0/self.ch1_updateRate)
        self.ch1_fftDisplay.set_update_time(1.0/self.ch1_updateRate)

    def get_ch1_fs(self):
        return self.ch1_fs

    def set_ch1_fs(self, ch1_fs):
        self.ch1_fs = ch1_fs
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.ch1_rfFreq*1e6 + self.ch1_ddcFreq*1e3, self.ch1_fs)
        self.set_ch1_fsLabel(self._ch1_fsLabel_formatter("%sHz"%( num_to_str(self.ch1_fs) )))
        self.ch1_fftDisplay.set_frequency_range(self.ch1_rfFreq*1e6 + self.ch1_ddcFreq*1e3, self.ch1_fs)

    def get_ch1_fftSize(self):
        return self.ch1_fftSize

    def set_ch1_fftSize(self, ch1_fftSize):
        self.ch1_fftSize = ch1_fftSize
        self.set_ch2_fftSize(self.ch1_fftSize if self.ch2_wb else self.ch1_fftSize/2)

    def get_ch1_channelList(self):
        return self.ch1_channelList

    def set_ch1_channelList(self, ch1_channelList):
        self.ch1_channelList = ch1_channelList
        self.set_ch1_index(self.ch1_channelList[0])

    def get_udpPortList(self):
        return self.udpPortList

    def set_udpPortList(self, udpPortList):
        self.udpPortList = udpPortList
        self.ndrDemoControlBlock.set_ddc1_udp_port(self.udpPortList[0])
        self.ndrDemoControlBlock.set_ddc2_udp_port(self.udpPortList[1])

    def get_radioRspDisplay(self):
        return self.radioRspDisplay

    def set_radioRspDisplay(self, radioRspDisplay):
        self.radioRspDisplay = radioRspDisplay
        Qt.QMetaObject.invokeMethod(self._radioRspDisplay_line_edit, "setText", Qt.Q_ARG("QString", str(self.radioRspDisplay)))

    def get_radioCmd(self):
        return self.radioCmd

    def set_radioCmd(self, radioCmd):
        self.radioCmd = radioCmd
        self.ndrDemoControlBlock.set_radio_cmd(str(self.radioCmd))
        Qt.QMetaObject.invokeMethod(self._radioCmd_line_edit, "setText", Qt.Q_ARG("QString", str(self.radioCmd)))

    def get_logfile(self):
        return self.logfile

    def set_logfile(self, logfile):
        self.logfile = logfile
        self.blocks_file_sink_0.open(self.logfile)

    def get_ipAddress(self):
        return self.ipAddress

    def set_ipAddress(self, ipAddress):
        self.ipAddress = ipAddress

    def get_fftColSpan(self):
        return self.fftColSpan

    def set_fftColSpan(self, fftColSpan):
        self.fftColSpan = fftColSpan

    def get_ch2_updateRate(self):
        return self.ch2_updateRate

    def set_ch2_updateRate(self, ch2_updateRate):
        self.ch2_updateRate = ch2_updateRate
        self.ch2_fftDisplay.set_update_time(1.0/self.ch2_updateRate)

    def get_ch2_rfFreqRange(self):
        return self.ch2_rfFreqRange

    def set_ch2_rfFreqRange(self, ch2_rfFreqRange):
        self.ch2_rfFreqRange = ch2_rfFreqRange

    def get_ch2_rfFreq(self):
        return self.ch2_rfFreq

    def set_ch2_rfFreq(self, ch2_rfFreq):
        self.ch2_rfFreq = ch2_rfFreq
        self.ndrDemoControlBlock.set_tuner2_freq(float( 1e6*self.ch2_rfFreq ))
        self.ch2_fftDisplay.set_frequency_range((self.ch2_rfFreq if self.ch2_wb else self.ch1_rfFreq)*1e6 + self.ch2_ddcFreq*1e3, self.ch2_fs)

    def get_ch2_rfAtten(self):
        return self.ch2_rfAtten

    def set_ch2_rfAtten(self, ch2_rfAtten):
        self.ch2_rfAtten = ch2_rfAtten
        self.ndrDemoControlBlock.set_tuner2_atten(self.ch2_rfAtten)

    def get_ch2_index(self):
        return self.ch2_index

    def set_ch2_index(self, ch2_index):
        self.ch2_index = ch2_index
        self._ch2_index_callback(self.ch2_index)
        self.ndrDemoControlBlock.set_tuner2_index(self.ch2_index if self.ch2_wb else -1)
        self.ndrDemoControlBlock.set_ddc2_index(self.ch2_index)

    def get_ch2_fsLabel(self):
        return self.ch2_fsLabel

    def set_ch2_fsLabel(self, ch2_fsLabel):
        self.ch2_fsLabel = ch2_fsLabel
        Qt.QMetaObject.invokeMethod(self._ch2_fsLabel_label, "setText", Qt.Q_ARG("QString", str(self.ch2_fsLabel)))

    def get_ch2_fftSize(self):
        return self.ch2_fftSize

    def set_ch2_fftSize(self, ch2_fftSize):
        self.ch2_fftSize = ch2_fftSize

    def get_ch2_ddcFreq(self):
        return self.ch2_ddcFreq

    def set_ch2_ddcFreq(self, ch2_ddcFreq):
        self.ch2_ddcFreq = ch2_ddcFreq
        self.ndrDemoControlBlock.set_ddc2_freq(1e3*self.ch2_ddcFreq)
        self.ch2_fftDisplay.set_frequency_range((self.ch2_rfFreq if self.ch2_wb else self.ch1_rfFreq)*1e6 + self.ch2_ddcFreq*1e3, self.ch2_fs)

    def get_ch1_rfFreq(self):
        return self.ch1_rfFreq

    def set_ch1_rfFreq(self, ch1_rfFreq):
        self.ch1_rfFreq = ch1_rfFreq
        self.ndrDemoControlBlock.set_tuner1_freq(float( 1e6*self.ch1_rfFreq ))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.ch1_rfFreq*1e6 + self.ch1_ddcFreq*1e3, self.ch1_fs)
        self.ch2_fftDisplay.set_frequency_range((self.ch2_rfFreq if self.ch2_wb else self.ch1_rfFreq)*1e6 + self.ch2_ddcFreq*1e3, self.ch2_fs)
        self.ch1_fftDisplay.set_frequency_range(self.ch1_rfFreq*1e6 + self.ch1_ddcFreq*1e3, self.ch1_fs)

    def get_ch1_rfAtten(self):
        return self.ch1_rfAtten

    def set_ch1_rfAtten(self, ch1_rfAtten):
        self.ch1_rfAtten = ch1_rfAtten
        self.ndrDemoControlBlock.set_tuner1_atten(self.ch1_rfAtten)

    def get_ch1_index(self):
        return self.ch1_index

    def set_ch1_index(self, ch1_index):
        self.ch1_index = ch1_index
        self._ch1_index_callback(self.ch1_index)
        self.ndrDemoControlBlock.set_tuner1_index(self.ch1_index)
        self.ndrDemoControlBlock.set_ddc1_index(self.ch1_index)
        self.ndrDemoControlBlock.set_ddc2_rf_source(-1 if self.ch2_wb else self.ch1_index)

    def get_ch1_fsLabel(self):
        return self.ch1_fsLabel

    def set_ch1_fsLabel(self, ch1_fsLabel):
        self.ch1_fsLabel = ch1_fsLabel
        Qt.QMetaObject.invokeMethod(self._ch1_fsLabel_label, "setText", Qt.Q_ARG("QString", str(self.ch1_fsLabel)))

    def get_ch1_ddcFreq(self):
        return self.ch1_ddcFreq

    def set_ch1_ddcFreq(self, ch1_ddcFreq):
        self.ch1_ddcFreq = ch1_ddcFreq
        self.ndrDemoControlBlock.set_ddc1_freq(self.ch1_ddcFreq*1e3)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.ch1_rfFreq*1e6 + self.ch1_ddcFreq*1e3, self.ch1_fs)
        self.ch1_fftDisplay.set_frequency_range(self.ch1_rfFreq*1e6 + self.ch1_ddcFreq*1e3, self.ch1_fs)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-b", "--basePort", dest="basePort", type="intx", default=22200,
        help="Set Base UDP Port for IF Streaming [default=%default]")
    parser.add_option(
        "-d", "--dataPort", dest="dataPort", type="intx", default=1,
        help="Set Radio NIC Index [default=%default]")
    parser.add_option(
        "-n", "--hostnameOrDevice", dest="hostnameOrDevice", type="string", default='/dev/ndr47x',
        help="Set Radio Hostname or Serial Device name [default=%default]")
    parser.add_option(
        "-i", "--ifname", dest="ifname", type="string", default='eth6',
        help="Set 10GbE NIC [default=%default]")
    parser.add_option(
        "-r", "--radioType", dest="radioType", type="string", default='ndr304',
        help="Set Radio Type [default=%default]")
    parser.add_option(
        "-p", "--udpPortOrBaudrate", dest="udpPortOrBaudrate", type="intx", default=921600,
        help="Set Radio TCP/UDP Control Port or Baudrate [default=%default]")
    parser.add_option(
        "-V", "--verbose", dest="verbose", type="intx", default=1,
        help="Set Verbose Driver Mode [default=%default]")
    parser.add_option(
        "-v", "--vitaLevel", dest="vitaLevel", type="intx", default=3,
        help="Set Vita 49 Level [default=%default]")
    parser.add_option(
        "-u", "--wbfftRate", dest="wbfftRate", type="intx", default=8,
        help="Set Wideband FFT Update Rate (Hz) [default=%default]")
    parser.add_option(
        "-s", "--wbfftSize", dest="wbfftSize", type="intx", default=10,
        help="Set Wideband FFT Size (2^x) [default=%default]")
    parser.add_option(
        "-w", "--wideband2", dest="wideband2", type="intx", default=0,
        help="Set Set 2nd channel to wideband [default=%default]")
    return parser


def main(top_block_cls=ndr_qt_demo_gui, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(basePort=options.basePort, dataPort=options.dataPort, hostnameOrDevice=options.hostnameOrDevice, ifname=options.ifname, radioType=options.radioType, udpPortOrBaudrate=options.udpPortOrBaudrate, verbose=options.verbose, vitaLevel=options.vitaLevel, wbfftRate=options.wbfftRate, wbfftSize=options.wbfftSize, wideband2=options.wideband2)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
