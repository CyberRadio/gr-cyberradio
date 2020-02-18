#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NDR328 Display GUI  $Id: ndr804_display.grc 596 2016-04-22 17:26:43Z nathan.harter $
# Generated: Mon Oct 22 17:06:09 2018
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
from gnuradio.eng_notation import num_to_str
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from numpy import pi
from optparse import OptionParser
import ConfigParser
import CyberRadio
import CyberRadioDriver
import CyberRadioDriver as crd
import os, datetime
import sip
import sys
import threading
import time
from gnuradio import qtgui


class ndr804_display(gr.top_block, Qt.QWidget):

    def __init__(self, configPath=None, dataPort=2, hostname='ndr308', ifname='enp3s0f1', radioType='ndr328', verbose=1):
        gr.top_block.__init__(self, "NDR328 Display GUI  $Id: ndr804_display.grc 596 2016-04-22 17:26:43Z nathan.harter $")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDR328 Display GUI  $Id: ndr804_display.grc 596 2016-04-22 17:26:43Z nathan.harter $")
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

        self.settings = Qt.QSettings("GNU Radio", "ndr804_display")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.configPath = configPath
        self.dataPort = dataPort
        self.hostname = hostname
        self.ifname = ifname
        self.radioType = radioType
        self.verbose = verbose

        ##################################################
        # Variables
        ##################################################
        self.radioObj = radioObj = crd.getRadioObject(
                radioType,
                verbose=bool(verbose),
                host=hostname if True else None,
                 )
        if bool(verbose) and radioObj.isConnected():
            print("{0} is {1}connected to {2} as {3}. Using CyberRadioDriver version {4}.".format("radioObj", "" if radioObj.isConnected() else "not ", radioObj.host_or_dev, radioObj, crd.version))
        self.configFile = configFile = configPath if configPath is not None else os.path.join("/public","ndrDemoGui","ndr804_display.%s.cfg"%radioType)
        self.wbddcRateSet = wbddcRateSet = radioObj.getWbddcRateSet()
        self.nbddcRateIndexOptions = nbddcRateIndexOptions = sorted(radioObj.getNbddcRateSet().keys())
        self._nbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcIndexCfg_config.read(configFile)
        try: nbddcIndexCfg = self._nbddcIndexCfg_config.getint('NBDDC', 'index')
        except: nbddcIndexCfg = radioObj.getNbddcIndexRange()[0]
        self.nbddcIndexCfg = nbddcIndexCfg
        self._wbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcRateIndexCfg_config.read(configFile)
        try: wbddcRateIndexCfg = self._wbddcRateIndexCfg_config.getint('WBDDC', 'rateIndex')
        except: wbddcRateIndexCfg = sorted(wbddcRateSet.keys())[0]
        self.wbddcRateIndexCfg = wbddcRateIndexCfg
        self._nbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcRateIndexCfg_config.read(configFile)
        try: nbddcRateIndexCfg = self._nbddcRateIndexCfg_config.getint('NBDDC', 'rateIndex')
        except: nbddcRateIndexCfg = nbddcRateIndexOptions[0]
        self.nbddcRateIndexCfg = nbddcRateIndexCfg
        self.nbddcIndex = nbddcIndex = nbddcIndexCfg
        self._nbddcDagcTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcDagcTypeCfg_config.read(configFile)
        try: nbddcDagcTypeCfg = self._nbddcDagcTypeCfg_config.getint('Demod', 'dagcType')
        except: nbddcDagcTypeCfg = 0
        self.nbddcDagcTypeCfg = nbddcDagcTypeCfg
        self._nbddcAlcTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcAlcTypeCfg_config.read(configFile)
        try: nbddcAlcTypeCfg = self._nbddcAlcTypeCfg_config.getint('Demod', 'alcType')
        except: nbddcAlcTypeCfg = 0
        self.nbddcAlcTypeCfg = nbddcAlcTypeCfg
        self.dagcDefault = dagcDefault = {0:1, 1:0, 2:0}
        self.alcDefault = alcDefault = {0:1, 1:0, 2:0}
        self.wbddcRateIndex = wbddcRateIndex = wbddcRateIndexCfg
        self._wbddcFormatCfg_config = ConfigParser.ConfigParser()
        self._wbddcFormatCfg_config.read(configFile)
        try: wbddcFormatCfg = self._wbddcFormatCfg_config.getint('WBDDC', 'format')
        except: wbddcFormatCfg = 0
        self.wbddcFormatCfg = wbddcFormatCfg
        self.squelchRange = squelchRange = [-150,21] if radioType=="ndr328" else [0,0]
        self._rfIndexCfg_config = ConfigParser.ConfigParser()
        self._rfIndexCfg_config.read(configFile)
        try: rfIndexCfg = self._rfIndexCfg_config.getint('Tuner', 'index')
        except: rfIndexCfg = radioObj.getTunerIndexRange()[0]
        self.rfIndexCfg = rfIndexCfg
        self.nbddcRateSet = nbddcRateSet = radioObj.getNbddcRateSet(nbddcIndex)
        self.nbddcRateIndex = nbddcRateIndex = nbddcRateIndexCfg
        self._nbddcDemodTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcDemodTypeCfg_config.read(configFile)
        try: nbddcDemodTypeCfg = self._nbddcDemodTypeCfg_config.getint('Demod', 'type')
        except: nbddcDemodTypeCfg = -1
        self.nbddcDemodTypeCfg = nbddcDemodTypeCfg
        self._nbddcDagcLevelSelectionCfg_config = ConfigParser.ConfigParser()
        self._nbddcDagcLevelSelectionCfg_config.read(configFile)
        try: nbddcDagcLevelSelectionCfg = self._nbddcDagcLevelSelectionCfg_config.getint('Demod', 'dagcLevel')
        except: nbddcDagcLevelSelectionCfg = dagcDefault.get(nbddcDagcTypeCfg,0)
        self.nbddcDagcLevelSelectionCfg = nbddcDagcLevelSelectionCfg
        self.nbddcBwSet = nbddcBwSet = radioObj.getNbddcBwSet(nbddcIndex)
        self._nbddcBfoCfg_config = ConfigParser.ConfigParser()
        self._nbddcBfoCfg_config.read(configFile)
        try: nbddcBfoCfg = self._nbddcBfoCfg_config.getint('Demod', 'bfo')
        except: nbddcBfoCfg = 0
        self.nbddcBfoCfg = nbddcBfoCfg
        self._nbddcAlcLevelSelectionCfg_config = ConfigParser.ConfigParser()
        self._nbddcAlcLevelSelectionCfg_config.read(configFile)
        try: nbddcAlcLevelSelectionCfg = self._nbddcAlcLevelSelectionCfg_config.getint('Demod', 'alcLevel')
        except: nbddcAlcLevelSelectionCfg = alcDefault.get(nbddcAlcTypeCfg)
        self.nbddcAlcLevelSelectionCfg = nbddcAlcLevelSelectionCfg
        self.wbddcRxRate = wbddcRxRate = 0.0
        self.wbddcFormat = wbddcFormat = wbddcFormatCfg
        self._specRateCfg_config = ConfigParser.ConfigParser()
        self._specRateCfg_config.read(configFile)
        try: specRateCfg = self._specRateCfg_config.getint('WBDDC', 'specRate')
        except: specRateCfg = 1
        self.specRateCfg = specRateCfg
        self.rssiResponse = rssiResponse = "-"
        self.rfIndex = rfIndex = rfIndexCfg
        self._rfFreqCfg_config = ConfigParser.ConfigParser()
        self._rfFreqCfg_config.read(configFile)
        try: rfFreqCfg = self._rfFreqCfg_config.getint('Tuner', 'freq')
        except: rfFreqCfg = 1500
        self.rfFreqCfg = rfFreqCfg
        self._rfFilterCfg_config = ConfigParser.ConfigParser()
        self._rfFilterCfg_config.read(configFile)
        try: rfFilterCfg = self._rfFilterCfg_config.getint('Tuner', 'filter')
        except: rfFilterCfg = 1
        self.rfFilterCfg = rfFilterCfg
        self._rfAttenCfg_config = ConfigParser.ConfigParser()
        self._rfAttenCfg_config.read(configFile)
        try: rfAttenCfg = self._rfAttenCfg_config.getint('Tuner', 'atten')
        except: rfAttenCfg = 0
        self.rfAttenCfg = rfAttenCfg
        self.radioRsp = radioRsp = ""
        self._radioCmdCfg_config = ConfigParser.ConfigParser()
        self._radioCmdCfg_config.read(configFile)
        try: radioCmdCfg = self._radioCmdCfg_config.get('Radio', 'cmd')
        except: radioCmdCfg = '*IDN?'
        self.radioCmdCfg = radioCmdCfg
        self._nbddcSquelchLevelCfg_config = ConfigParser.ConfigParser()
        self._nbddcSquelchLevelCfg_config.read(configFile)
        try: nbddcSquelchLevelCfg = self._nbddcSquelchLevelCfg_config.getint('Demod', 'squelchLevel')
        except: nbddcSquelchLevelCfg = squelchRange[0]
        self.nbddcSquelchLevelCfg = nbddcSquelchLevelCfg
        self.nbddcRxRate = nbddcRxRate = 0.0
        self.nbddcDemodType = nbddcDemodType = nbddcDemodTypeCfg
        self._nbddcDemodDcBlockCfg_config = ConfigParser.ConfigParser()
        self._nbddcDemodDcBlockCfg_config.read(configFile)
        try: nbddcDemodDcBlockCfg = self._nbddcDemodDcBlockCfg_config.getboolean('Demod', 'dcBlock')
        except: nbddcDemodDcBlockCfg = False
        self.nbddcDemodDcBlockCfg = nbddcDemodDcBlockCfg
        self.nbddcDagcType = nbddcDagcType = 0
        self.nbddcDagcLevelSelection = nbddcDagcLevelSelection = nbddcDagcLevelSelectionCfg
        self.nbddcBfoSelection = nbddcBfoSelection = nbddcBfoCfg
        self.nbddcAlcType = nbddcAlcType = nbddcAlcTypeCfg
        self.nbddcAlcLevelSelection = nbddcAlcLevelSelection = nbddcAlcLevelSelectionCfg if radioType=="ndr328" else 0
        self._nbFrqCfg_config = ConfigParser.ConfigParser()
        self._nbFrqCfg_config.read(configFile)
        try: nbFrqCfg = self._nbFrqCfg_config.getint('NBDDC', 'freq')
        except: nbFrqCfg = 0
        self.nbFrqCfg = nbFrqCfg
        self.iqRssi = iqRssi = "n/a"
        self.fsWb = fsWb = wbddcRateSet[wbddcRateIndex]
        self.fsNb = fsNb = nbddcRateSet[nbddcRateIndex]
        self.fsDemod = fsDemod = 8e3
        self.demodRxRate = demodRxRate = 0.0
        self.demodRssi = demodRssi = "n/a"
        self.dagcMultiplier = dagcMultiplier = {0:1, 1:0, 2:0}
        self._calFreqCfg_config = ConfigParser.ConfigParser()
        self._calFreqCfg_config.read(configFile)
        try: calFreqCfg = self._calFreqCfg_config.getfloat('Cal', 'freq')
        except: calFreqCfg = 1.0
        self.calFreqCfg = calFreqCfg
        self._calEnableCfg_config = ConfigParser.ConfigParser()
        self._calEnableCfg_config.read(configFile)
        try: calEnableCfg = self._calEnableCfg_config.getboolean('Cal', 'enable')
        except: calEnableCfg = False
        self.calEnableCfg = calEnableCfg
        self.bwNb = bwNb = nbddcBwSet[nbddcRateIndex]
        self.alcMultiplier = alcMultiplier = {0:1, 1:0, 2:0}
        self.wbddcUdpPort = wbddcUdpPort = 41000
        self.wbddcRxRateLabel = wbddcRxRateLabel = "%5.1f%%"%(100.0*wbddcRxRate/fsWb)
        self._wbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcIndexCfg_config.read(configFile)
        try: wbddcIndexCfg = self._wbddcIndexCfg_config.getint('WBDDC', 'index')
        except: wbddcIndexCfg = rfIndexCfg
        self.wbddcIndexCfg = wbddcIndexCfg
        self.wbddcIndex = wbddcIndex = rfIndex if wbddcFormat in (0,1) else -1
        self.wbddcFormatProbe = wbddcFormatProbe = 1
        self.specVecLen = specVecLen = 4096
        self.specRate = specRate = specRateCfg
        self.rssiRspBox = rssiRspBox = rssiResponse
        self.rfFreq = rfFreq = rfFreqCfg
        self.rfFilter = rfFilter = rfFilterCfg
        self.rfAtten = rfAtten = rfAttenCfg
        self.rateProbeGain = rateProbeGain = 2**-3
        self.radioRspTrigger = radioRspTrigger = True
        self.radioRspDisplay = radioRspDisplay = radioRsp
        self.radioCmd = radioCmd = radioCmdCfg
        self.plotRowSpan = plotRowSpan = 2
        self.plotColSpan = plotColSpan = 3
        self.otherNbddcEnable = otherNbddcEnable = False
        self.osDotSetCwd = osDotSetCwd = os.chdir( os.path.expanduser( os.path.join( "~", "Desktop") ) )
        self.nbfsTxt = nbfsTxt = "%sHz @ %ssps"%(num_to_str(bwNb),num_to_str(fsNb))
        self.nbddcSquelchLevel = nbddcSquelchLevel = nbddcSquelchLevelCfg
        self.nbddcSinadSRC = nbddcSinadSRC = 0
        self.nbddcRxRateLabel = nbddcRxRateLabel = "%5.1f%%"%(100.0*nbddcRxRate/fsNb)
        self.nbddcFormatProbe = nbddcFormatProbe = 0
        self._nbddcEnableCfg_config = ConfigParser.ConfigParser()
        self._nbddcEnableCfg_config.read(configFile)
        try: nbddcEnableCfg = self._nbddcEnableCfg_config.getboolean('NBDDC', 'enable')
        except: nbddcEnableCfg = True
        self.nbddcEnableCfg = nbddcEnableCfg
        self.nbddcEnable = nbddcEnable = nbddcIndex>=0
        self.nbddcDemodDcBlock = nbddcDemodDcBlock = nbddcDemodDcBlockCfg
        self.nbddcDagcLevel = nbddcDagcLevel = dagcMultiplier.get(nbddcDagcType,1)*nbddcDagcLevelSelection
        self.nbddcBfo = nbddcBfo = nbddcBfoSelection if nbddcDemodType==0 else 0
        self.nbddcAlcLevel = nbddcAlcLevel = alcMultiplier.get(nbddcAlcType,1)*nbddcAlcLevelSelection
        self.nbFrq = nbFrq = nbFrqCfg
        self.iqRssiRsp = iqRssiRsp = str(iqRssi)
        self.iirAlpha = iirAlpha = 5
        self.fsAudio = fsAudio = 24e3
        self.demodRxRateLabel = demodRxRateLabel = "%5.1f%%"%(100.0*demodRxRate/fsDemod)
        self.demodRssiRsp = demodRssiRsp = str(demodRssi)
        self.dagcRange = dagcRange = [0,127] if radioType=="ndr328" else [0,0]
        self.calFreq = calFreq = calFreqCfg
        self.calEnable = calEnable = bool(calEnableCfg)
        self.bfoRange = bfoRange = [-4000,4000] if radioType=="ndr328" else [0,0]
        self.alcLevelRange = alcLevelRange = [0,127] if radioType=="ndr328" else [0,0]

        ##################################################
        # Blocks
        ##################################################
        self.control_tabs = Qt.QTabWidget()
        self.control_tabs_widget_0 = Qt.QWidget()
        self.control_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tabs_widget_0)
        self.control_tabs_grid_layout_0 = Qt.QGridLayout()
        self.control_tabs_layout_0.addLayout(self.control_tabs_grid_layout_0)
        self.control_tabs.addTab(self.control_tabs_widget_0, 'RF/WBDDC Parameters')
        self.control_tabs_widget_1 = Qt.QWidget()
        self.control_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tabs_widget_1)
        self.control_tabs_grid_layout_1 = Qt.QGridLayout()
        self.control_tabs_layout_1.addLayout(self.control_tabs_grid_layout_1)
        self.control_tabs.addTab(self.control_tabs_widget_1, 'Commands/Misc.')
        self.control_tabs_widget_2 = Qt.QWidget()
        self.control_tabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tabs_widget_2)
        self.control_tabs_grid_layout_2 = Qt.QGridLayout()
        self.control_tabs_layout_2.addLayout(self.control_tabs_grid_layout_2)
        self.control_tabs.addTab(self.control_tabs_widget_2, 'NBDDC Parameters')
        self.control_tabs_widget_3 = Qt.QWidget()
        self.control_tabs_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tabs_widget_3)
        self.control_tabs_grid_layout_3 = Qt.QGridLayout()
        self.control_tabs_layout_3.addLayout(self.control_tabs_grid_layout_3)
        self.control_tabs.addTab(self.control_tabs_widget_3, 'Debug')
        self.top_grid_layout.addWidget(self.control_tabs, 2, 0, 1, 6)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._wbddcRateIndex_options = sorted(wbddcRateSet.keys())
        self._wbddcRateIndex_labels = map(str, self._wbddcRateIndex_options)
        self._wbddcRateIndex_tool_bar = Qt.QToolBar(self)
        self._wbddcRateIndex_tool_bar.addWidget(Qt.QLabel('WBDDC Rate'+": "))
        self._wbddcRateIndex_combo_box = Qt.QComboBox()
        self._wbddcRateIndex_tool_bar.addWidget(self._wbddcRateIndex_combo_box)
        for label in self._wbddcRateIndex_labels: self._wbddcRateIndex_combo_box.addItem(label)
        self._wbddcRateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._wbddcRateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._wbddcRateIndex_options.index(i)))
        self._wbddcRateIndex_callback(self.wbddcRateIndex)
        self._wbddcRateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_wbddcRateIndex(self._wbddcRateIndex_options[i]))
        self.control_tabs_grid_layout_0.addWidget(self._wbddcRateIndex_tool_bar, 2, 2, 1, 1)
        for r in range(2, 3):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self._wbddcFormat_options = [-1,0,1]
        self._wbddcFormat_labels = ["Disabled","Spectral","IQ"]
        self._wbddcFormat_group_box = Qt.QGroupBox('WBDDC Output')
        self._wbddcFormat_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._wbddcFormat_button_group = variable_chooser_button_group()
        self._wbddcFormat_group_box.setLayout(self._wbddcFormat_box)
        for i, label in enumerate(self._wbddcFormat_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._wbddcFormat_box.addWidget(radio_button)
        	self._wbddcFormat_button_group.addButton(radio_button, i)
        self._wbddcFormat_callback = lambda i: Qt.QMetaObject.invokeMethod(self._wbddcFormat_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._wbddcFormat_options.index(i)))
        self._wbddcFormat_callback(self.wbddcFormat)
        self._wbddcFormat_button_group.buttonClicked[int].connect(
        	lambda i: self.set_wbddcFormat(self._wbddcFormat_options[i]))
        self.control_tabs_grid_layout_0.addWidget(self._wbddcFormat_group_box, 2, 0, 1, 2)
        for r in range(2, 3):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self._specRate_options = range(3)
        self._specRate_labels = ["Full Rate","10/second","100/second"]
        self._specRate_tool_bar = Qt.QToolBar(self)
        self._specRate_tool_bar.addWidget(Qt.QLabel('Spectral Rate'+": "))
        self._specRate_combo_box = Qt.QComboBox()
        self._specRate_tool_bar.addWidget(self._specRate_combo_box)
        for label in self._specRate_labels: self._specRate_combo_box.addItem(label)
        self._specRate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._specRate_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._specRate_options.index(i)))
        self._specRate_callback(self.specRate)
        self._specRate_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_specRate(self._specRate_options[i]))
        self.control_tabs_grid_layout_0.addWidget(self._specRate_tool_bar, 2, 3, 1, 1)
        for r in range(2, 3):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self._rfIndex_options = radioObj.getTunerIndexRange()
        self._rfIndex_labels = map(str, self._rfIndex_options)
        self._rfIndex_tool_bar = Qt.QToolBar(self)
        self._rfIndex_tool_bar.addWidget(Qt.QLabel('Tuner'+": "))
        self._rfIndex_combo_box = Qt.QComboBox()
        self._rfIndex_tool_bar.addWidget(self._rfIndex_combo_box)
        for label in self._rfIndex_labels: self._rfIndex_combo_box.addItem(label)
        self._rfIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rfIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rfIndex_options.index(i)))
        self._rfIndex_callback(self.rfIndex)
        self._rfIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_rfIndex(self._rfIndex_options[i]))
        self.control_tabs_grid_layout_0.addWidget(self._rfIndex_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self._rfFreq_range = Range(int( radioObj.getTunerFrequencyRange()[0]/1e6 ), int( radioObj.getTunerFrequencyRange()[1]/1e6 ), 10, rfFreqCfg, 200)
        self._rfFreq_win = RangeWidget(self._rfFreq_range, self.set_rfFreq, 'RF Freq. (MHz)', "counter_slider", int)
        self.control_tabs_grid_layout_0.addWidget(self._rfFreq_win, 0, 2, 1, 3)
        for r in range(0, 1):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 5):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self._rfFilter_options = (0, 1, )
        self._rfFilter_labels = ('LC', 'SAW', )
        self._rfFilter_tool_bar = Qt.QToolBar(self)
        self._rfFilter_tool_bar.addWidget(Qt.QLabel('IF Filter'+": "))
        self._rfFilter_combo_box = Qt.QComboBox()
        self._rfFilter_tool_bar.addWidget(self._rfFilter_combo_box)
        for label in self._rfFilter_labels: self._rfFilter_combo_box.addItem(label)
        self._rfFilter_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rfFilter_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rfFilter_options.index(i)))
        self._rfFilter_callback(self.rfFilter)
        self._rfFilter_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_rfFilter(self._rfFilter_options[i]))
        self.control_tabs_grid_layout_0.addWidget(self._rfFilter_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self._rfAtten_range = Range(int( radioObj.getTunerAttenuationRange()[0]), int( radioObj.getTunerAttenuationRange()[1]), 1, rfAttenCfg, 200)
        self._rfAtten_win = RangeWidget(self._rfAtten_range, self.set_rfAtten, 'RF Atten. (dB)', "counter_slider", int)
        self.control_tabs_grid_layout_0.addWidget(self._rfAtten_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        _otherNbddcEnable_check_box = Qt.QCheckBox('All NBDDCs?')
        self._otherNbddcEnable_choices = {True: True, False: False}
        self._otherNbddcEnable_choices_inv = dict((v,k) for k,v in self._otherNbddcEnable_choices.iteritems())
        self._otherNbddcEnable_callback = lambda i: Qt.QMetaObject.invokeMethod(_otherNbddcEnable_check_box, "setChecked", Qt.Q_ARG("bool", self._otherNbddcEnable_choices_inv[i]))
        self._otherNbddcEnable_callback(self.otherNbddcEnable)
        _otherNbddcEnable_check_box.stateChanged.connect(lambda i: self.set_otherNbddcEnable(self._otherNbddcEnable_choices[bool(i)]))
        self.control_tabs_grid_layout_1.addWidget(_otherNbddcEnable_check_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.control_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tabs_grid_layout_1.setColumnStretch(c, 1)
        self.nbddc_tabs = Qt.QTabWidget()
        self.nbddc_tabs_widget_0 = Qt.QWidget()
        self.nbddc_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.nbddc_tabs_widget_0)
        self.nbddc_tabs_grid_layout_0 = Qt.QGridLayout()
        self.nbddc_tabs_layout_0.addLayout(self.nbddc_tabs_grid_layout_0)
        self.nbddc_tabs.addTab(self.nbddc_tabs_widget_0, 'NBDDC Spectrum')
        self.nbddc_tabs_widget_1 = Qt.QWidget()
        self.nbddc_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.nbddc_tabs_widget_1)
        self.nbddc_tabs_grid_layout_1 = Qt.QGridLayout()
        self.nbddc_tabs_layout_1.addLayout(self.nbddc_tabs_grid_layout_1)
        self.nbddc_tabs.addTab(self.nbddc_tabs_widget_1, 'NB Demod Output')
        self.top_grid_layout.addWidget(self.nbddc_tabs, 0, 3, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._nbddcSquelchLevel_range = Range(squelchRange[0], squelchRange[1], 1, nbddcSquelchLevelCfg, 200)
        self._nbddcSquelchLevel_win = RangeWidget(self._nbddcSquelchLevel_range, self.set_nbddcSquelchLevel, 'Squelch', "counter_slider", int)
        self.control_tabs_grid_layout_2.addWidget(self._nbddcSquelchLevel_win, 2, 5, 1, 3)
        for r in range(2, 3):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(5, 8):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbddcRateIndex_options = nbddcRateIndexOptions
        self._nbddcRateIndex_labels = map(str, self._nbddcRateIndex_options)
        self._nbddcRateIndex_tool_bar = Qt.QToolBar(self)
        self._nbddcRateIndex_tool_bar.addWidget(Qt.QLabel('NBDDC Rate'+": "))
        self._nbddcRateIndex_combo_box = Qt.QComboBox()
        self._nbddcRateIndex_tool_bar.addWidget(self._nbddcRateIndex_combo_box)
        for label in self._nbddcRateIndex_labels: self._nbddcRateIndex_combo_box.addItem(label)
        self._nbddcRateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcRateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcRateIndex_options.index(i)))
        self._nbddcRateIndex_callback(self.nbddcRateIndex)
        self._nbddcRateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcRateIndex(self._nbddcRateIndex_options[i]))
        self.control_tabs_grid_layout_2.addWidget(self._nbddcRateIndex_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbddcIndex_options = [-1,]+radioObj.getNbddcIndexRange()
        self._nbddcIndex_labels = ["Disabled",]+[str(i) for i in radioObj.getNbddcIndexRange()]
        self._nbddcIndex_tool_bar = Qt.QToolBar(self)
        self._nbddcIndex_tool_bar.addWidget(Qt.QLabel('NBDDC'+": "))
        self._nbddcIndex_combo_box = Qt.QComboBox()
        self._nbddcIndex_tool_bar.addWidget(self._nbddcIndex_combo_box)
        for label in self._nbddcIndex_labels: self._nbddcIndex_combo_box.addItem(label)
        self._nbddcIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcIndex_options.index(i)))
        self._nbddcIndex_callback(self.nbddcIndex)
        self._nbddcIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcIndex(self._nbddcIndex_options[i]))
        self.control_tabs_grid_layout_2.addWidget(self._nbddcIndex_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbddcDemodType_options = [-1, 0,1,2,3,4] if radioType=="ndr328" else [-1]
        self._nbddcDemodType_labels = ["None","CW", "AM","FM","LSB","USB"] if radioType=="ndr328" else ["None"]
        self._nbddcDemodType_tool_bar = Qt.QToolBar(self)
        self._nbddcDemodType_tool_bar.addWidget(Qt.QLabel('Demod Type'+": "))
        self._nbddcDemodType_combo_box = Qt.QComboBox()
        self._nbddcDemodType_tool_bar.addWidget(self._nbddcDemodType_combo_box)
        for label in self._nbddcDemodType_labels: self._nbddcDemodType_combo_box.addItem(label)
        self._nbddcDemodType_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcDemodType_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcDemodType_options.index(i)))
        self._nbddcDemodType_callback(self.nbddcDemodType)
        self._nbddcDemodType_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcDemodType(self._nbddcDemodType_options[i]))
        self.control_tabs_grid_layout_2.addWidget(self._nbddcDemodType_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        _nbddcDemodDcBlock_check_box = Qt.QCheckBox('DC Block')
        self._nbddcDemodDcBlock_choices = {True: True, False: False}
        self._nbddcDemodDcBlock_choices_inv = dict((v,k) for k,v in self._nbddcDemodDcBlock_choices.iteritems())
        self._nbddcDemodDcBlock_callback = lambda i: Qt.QMetaObject.invokeMethod(_nbddcDemodDcBlock_check_box, "setChecked", Qt.Q_ARG("bool", self._nbddcDemodDcBlock_choices_inv[i]))
        self._nbddcDemodDcBlock_callback(self.nbddcDemodDcBlock)
        _nbddcDemodDcBlock_check_box.stateChanged.connect(lambda i: self.set_nbddcDemodDcBlock(self._nbddcDemodDcBlock_choices[bool(i)]))
        self.control_tabs_grid_layout_2.addWidget(_nbddcDemodDcBlock_check_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbddcDagcType_options = [0,1,2] if radioType=="ndr328" else [0]
        self._nbddcDagcType_labels = ["Manual","Slow","Fast",] if radioType=="ndr328" else ["n/a"]
        self._nbddcDagcType_tool_bar = Qt.QToolBar(self)
        self._nbddcDagcType_tool_bar.addWidget(Qt.QLabel('DAGC Type'+": "))
        self._nbddcDagcType_combo_box = Qt.QComboBox()
        self._nbddcDagcType_tool_bar.addWidget(self._nbddcDagcType_combo_box)
        for label in self._nbddcDagcType_labels: self._nbddcDagcType_combo_box.addItem(label)
        self._nbddcDagcType_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcDagcType_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcDagcType_options.index(i)))
        self._nbddcDagcType_callback(self.nbddcDagcType)
        self._nbddcDagcType_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcDagcType(self._nbddcDagcType_options[i]))
        self.control_tabs_grid_layout_2.addWidget(self._nbddcDagcType_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbddcAlcType_options = [0,1,2] if radioType=="ndr328" else [0]
        self._nbddcAlcType_labels = ["Manual","Slow","Fast",] if radioType=="ndr328" else ["n/a"]
        self._nbddcAlcType_tool_bar = Qt.QToolBar(self)
        self._nbddcAlcType_tool_bar.addWidget(Qt.QLabel('ALC Type'+": "))
        self._nbddcAlcType_combo_box = Qt.QComboBox()
        self._nbddcAlcType_tool_bar.addWidget(self._nbddcAlcType_combo_box)
        for label in self._nbddcAlcType_labels: self._nbddcAlcType_combo_box.addItem(label)
        self._nbddcAlcType_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcAlcType_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcAlcType_options.index(i)))
        self._nbddcAlcType_callback(self.nbddcAlcType)
        self._nbddcAlcType_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcAlcType(self._nbddcAlcType_options[i]))
        self.control_tabs_grid_layout_2.addWidget(self._nbddcAlcType_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbFrq_range = Range(int( -20e6 ), int( +20e6 ), int( 1e3 ), nbFrqCfg, int(40e6))
        self._nbFrq_win = RangeWidget(self._nbFrq_range, self.set_nbFrq, 'NB Freq (Hz)', "counter_slider", int)
        self.control_tabs_grid_layout_2.addWidget(self._nbFrq_win, 0, 3, 1, 5)
        for r in range(0, 1):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(3, 8):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._calFreq_range = Range(-30, +30, .005, calFreqCfg, 200)
        self._calFreq_win = RangeWidget(self._calFreq_range, self.set_calFreq, 'Cal. Freq. Offset (MHz)', "counter_slider", float)
        self.control_tabs_grid_layout_0.addWidget(self._calFreq_win, 1, 3, 1, 2)
        for r in range(1, 2):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 5):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        _calEnable_check_box = Qt.QCheckBox('Enable Cal Signal')
        self._calEnable_choices = {True: True, False: False}
        self._calEnable_choices_inv = dict((v,k) for k,v in self._calEnable_choices.iteritems())
        self._calEnable_callback = lambda i: Qt.QMetaObject.invokeMethod(_calEnable_check_box, "setChecked", Qt.Q_ARG("bool", self._calEnable_choices_inv[i]))
        self._calEnable_callback(self.calEnable)
        _calEnable_check_box.stateChanged.connect(lambda i: self.set_calEnable(self._calEnable_choices[bool(i)]))
        self.control_tabs_grid_layout_0.addWidget(_calEnable_check_box, 1, 2, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self.wbddc_tabs = Qt.QTabWidget()
        self.wbddc_tabs_widget_0 = Qt.QWidget()
        self.wbddc_tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.wbddc_tabs_widget_0)
        self.wbddc_tabs_grid_layout_0 = Qt.QGridLayout()
        self.wbddc_tabs_layout_0.addLayout(self.wbddc_tabs_grid_layout_0)
        self.wbddc_tabs.addTab(self.wbddc_tabs_widget_0, 'WBDDC Spectral Output')
        self.wbddc_tabs_widget_1 = Qt.QWidget()
        self.wbddc_tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.wbddc_tabs_widget_1)
        self.wbddc_tabs_grid_layout_1 = Qt.QGridLayout()
        self.wbddc_tabs_layout_1.addLayout(self.wbddc_tabs_grid_layout_1)
        self.wbddc_tabs.addTab(self.wbddc_tabs_widget_1, 'WBDDC IQ Spectrum')
        self.top_grid_layout.addWidget(self.wbddc_tabs, 0, 0, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.ndrControlBlock = CyberRadio.ndr_control(radioType,
                        hostname,
                        bool(verbose),
                        str(ifname),
                        dataPort,
                        rfFreq*1e6,
                        rfAtten,
                        rfFilter,
                        rfIndex,
                        (rfFreq+calFreq) if calEnable else 0,
                        wbddcIndex>0,
                        2,
                        wbddcRateIndex,
                        wbddcFormat,
                        0.0,
                        wbddcUdpPort,
                        wbddcIndex,
                        specRate,
                        nbddcEnable,
                        2,
                        nbddcRateIndex,
                        nbddcDemodType,
                        nbddcBfo,
                        nbddcDemodDcBlock,
                        nbddcAlcType,
                        nbddcAlcLevel,
                        nbddcSquelchLevel,
                                        nbddcDagcType,
                                        nbddcDagcLevel,
                        nbFrq,
                        wbddcUdpPort+1,
                        nbddcIndex,
                        otherNbddcEnable,
                        wbddcUdpPort+2)
        self._nbddcSinadSRC_options = [0,1,2,3] if radioType=="ndr328" else [0]
        self._nbddcSinadSRC_labels = ["CW","AM","FM1","FM2",] if radioType=="ndr328" else ["n/a"]
        self._nbddcSinadSRC_tool_bar = Qt.QToolBar(self)
        self._nbddcSinadSRC_tool_bar.addWidget(Qt.QLabel('SINAD Src'+": "))
        self._nbddcSinadSRC_combo_box = Qt.QComboBox()
        self._nbddcSinadSRC_tool_bar.addWidget(self._nbddcSinadSRC_combo_box)
        for label in self._nbddcSinadSRC_labels: self._nbddcSinadSRC_combo_box.addItem(label)
        self._nbddcSinadSRC_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcSinadSRC_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcSinadSRC_options.index(i)))
        self._nbddcSinadSRC_callback(self.nbddcSinadSRC)
        self._nbddcSinadSRC_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcSinadSRC(self._nbddcSinadSRC_options[i]))
        self.control_tabs_grid_layout_3.addWidget(self._nbddcSinadSRC_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tabs_grid_layout_3.setColumnStretch(c, 1)
        self.nbIqDisplay = CyberRadio.qt_freq_time_sink_iq(
            label="NBDDC",
            sampRate=fsNb,
            centerFreq=rfFreq*1e6 + nbFrq,
            fftPlotRange=[-140,0],
            fftSizeN=10,
            rmsGainRange=[0,11],
            enableSpectrum=True,
            enableWaterfall=True,
            enableTimeWaveform=True,
            enableRssiDisplay=False,
            enableRssi=True,
            fftGainLog=0.0,
            rssiPollRate=1.0,
            updatePeriod=0.1,
            rmsAvgGainExpInit=5,
        )
        self.nbddc_tabs_grid_layout_0.addWidget(self.nbIqDisplay)
        self._iirAlpha_range = Range(1, 15, 1, 5, 200)
        self._iirAlpha_win = RangeWidget(self._iirAlpha_range, self.set_iirAlpha, 'Display Alpha', "counter", int)
        self.control_tabs_grid_layout_0.addWidget(self._iirAlpha_win, 2, 4, 1, 1)
        for r in range(2, 3):
            self.control_tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 5):
            self.control_tabs_grid_layout_0.setColumnStretch(c, 1)
        self.demodDisplay = CyberRadio.qt_freq_time_sink_real(
            label="Demod",
            sampRate=fsDemod,
            centerFreq=0.0,
            fftPlotRange=[-140,0],
            fftSizeN=10,
            rmsGainRange=[0,11],
            enableSpectrum=True,
            enableWaterfall=True,
            enableTimeWaveform=True,
            enableRssiDisplay=False,
            enableRssi=True,
            fftGainLog=0.0,
            rssiPollRate=1.0,
            updatePeriod=0.1,
            rmsAvgGainExpInit=5,
            hilbertFilterLength=10
        )
        self.nbddc_tabs_grid_layout_1.addWidget(self.demodDisplay, 0, 0, 1, 1)
        for r in range(0, 1):
            self.nbddc_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.nbddc_tabs_grid_layout_1.setColumnStretch(c, 1)
        self.wbddcRxRateProbe = blocks.probe_rate(gr.sizeof_gr_complex*1, 125.0, rateProbeGain)
        self._wbddcRxRateLabel_tool_bar = Qt.QToolBar(self)

        if None:
          self._wbddcRxRateLabel_formatter = None
        else:
          self._wbddcRxRateLabel_formatter = lambda x: str(x)

        self._wbddcRxRateLabel_tool_bar.addWidget(Qt.QLabel('WBDDC Rx Rate (Rel. to expected)'+": "))
        self._wbddcRxRateLabel_label = Qt.QLabel(str(self._wbddcRxRateLabel_formatter(self.wbddcRxRateLabel)))
        self._wbddcRxRateLabel_tool_bar.addWidget(self._wbddcRxRateLabel_label)
        self.control_tabs_grid_layout_1.addWidget(self._wbddcRxRateLabel_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tabs_grid_layout_1.setColumnStretch(c, 1)

        def _wbddcRxRate_probe():
            while True:
                val = self.wbddcRxRateProbe.rate()
                try:
                    self.set_wbddcRxRate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _wbddcRxRate_thread = threading.Thread(target=_wbddcRxRate_probe)
        _wbddcRxRate_thread.daemon = True
        _wbddcRxRate_thread.start()


        def _wbddcFormatProbe_probe():
            while True:
                val = self.wbddc_tabs.setCurrentIndex(self.wbddcFormat)
                try:
                    self.set_wbddcFormatProbe(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _wbddcFormatProbe_thread = threading.Thread(target=_wbddcFormatProbe_probe)
        _wbddcFormatProbe_thread.daemon = True
        _wbddcFormatProbe_thread.start()

        self.wbIqSource = CyberRadio.vita_iq_source(
            vita_type=3,
            payload_size=4096,
            vita_header_size=36,
            vita_tail_size=4,
            byte_swapped=False,
            iq_swapped=False,
            iq_scale_factor=1.0/((2**15)-1),
            host='0.0.0.0',
            port_list=([wbddcUdpPort]),
            tagged=False,
            debug=False,
        )
        self.wbIqDisplay = CyberRadio.qt_freq_time_sink_iq(
            label="WBDDC",
            sampRate=fsWb,
            centerFreq=rfFreq*1e6,
            fftPlotRange=[-120,0],
            fftSizeN=11,
            rmsGainRange=[0,11],
            enableSpectrum=True,
            enableWaterfall=True,
            enableTimeWaveform=False,
            enableRssiDisplay=True,
            enableRssi=True,
            fftGainLog=0.0,
            rssiPollRate=1.0,
            updatePeriod=0.2,
            rmsAvgGainExpInit=5,
        )
        self.wbddc_tabs_grid_layout_1.addWidget(self.wbIqDisplay)
        self.stdoutFileDescriptor = blocks.file_descriptor_sink(gr.sizeof_char*1, 2)
        self.spectralVectorSink = qtgui.vector_sink_f(
            4096,
            rfFreq-25.6,
            51.2/4096,
            'Frequency (MHz)',
            'Amplitude (dBfs)',
            'Spectral Data',
            2 # Number of inputs
        )
        self.spectralVectorSink.set_update_time(0.10)
        self.spectralVectorSink.set_y_axis(-90, 0)
        self.spectralVectorSink.enable_autoscale(False)
        self.spectralVectorSink.enable_grid(True)
        self.spectralVectorSink.set_x_axis_units('MHz')
        self.spectralVectorSink.set_y_axis_units('dBfs')
        self.spectralVectorSink.set_ref_level(0)

        labels = ['Realtime', 'Average', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["dark red", "blue", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.spectralVectorSink.set_line_label(i, "Data {0}".format(i))
            else:
                self.spectralVectorSink.set_line_label(i, labels[i])
            self.spectralVectorSink.set_line_width(i, widths[i])
            self.spectralVectorSink.set_line_color(i, colors[i])
            self.spectralVectorSink.set_line_alpha(i, alphas[i])

        self._spectralVectorSink_win = sip.wrapinstance(self.spectralVectorSink.pyqwidget(), Qt.QWidget)
        self.wbddc_tabs_grid_layout_0.addWidget(self._spectralVectorSink_win)
        self.spectralUdpSource = blocks.udp_source(gr.sizeof_char*1, '0.0.0.0', wbddcUdpPort+4, 4136, True)
        self.spectralStreamToVector = blocks.stream_to_vector(gr.sizeof_char*1, specVecLen)
        self.spectralPayloadExtractor = blocks.keep_m_in_n(gr.sizeof_char, 4096, 4136, 36)
        self.spectralGuiAveraging = filter.single_pole_iir_filter_ff(2**-iirAlpha, specVecLen)
        self.spectralByteToFloat = blocks.char_to_float(specVecLen, 1.0)
        self._rssiRspBox_tool_bar = Qt.QToolBar(self)
        self._rssiRspBox_tool_bar.addWidget(Qt.QLabel('RSSI Rsp'+": "))
        self._rssiRspBox_line_edit = Qt.QLineEdit(str(self.rssiRspBox))
        self._rssiRspBox_tool_bar.addWidget(self._rssiRspBox_line_edit)
        self._rssiRspBox_line_edit.returnPressed.connect(
        	lambda: self.set_rssiRspBox(str(str(self._rssiRspBox_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._rssiRspBox_tool_bar, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)

        def _rssiResponse_probe():
            while True:
                val = self.ndrControlBlock.query_rssi()
                try:
                    self.set_rssiResponse(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (0.5 if radioType=="ndr328" else 0.0))
        _rssiResponse_thread = threading.Thread(target=_rssiResponse_probe)
        _rssiResponse_thread.daemon = True
        _rssiResponse_thread.start()

        _radioRspTrigger_push_button = Qt.QPushButton('Send RSP')
        self._radioRspTrigger_choices = {'Pressed': True, 'Released': False}
        _radioRspTrigger_push_button.pressed.connect(lambda: self.set_radioRspTrigger(self._radioRspTrigger_choices['Pressed']))
        _radioRspTrigger_push_button.released.connect(lambda: self.set_radioRspTrigger(self._radioRspTrigger_choices['Released']))
        self.control_tabs_grid_layout_1.addWidget(_radioRspTrigger_push_button, 1, 3, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(3, 4):
            self.control_tabs_grid_layout_1.setColumnStretch(c, 1)
        self._radioRspDisplay_tool_bar = Qt.QToolBar(self)
        self._radioRspDisplay_tool_bar.addWidget(Qt.QLabel('Response'+": "))
        self._radioRspDisplay_line_edit = Qt.QLineEdit(str(self.radioRspDisplay))
        self._radioRspDisplay_tool_bar.addWidget(self._radioRspDisplay_line_edit)
        self._radioRspDisplay_line_edit.returnPressed.connect(
        	lambda: self.set_radioRspDisplay(str(str(self._radioRspDisplay_line_edit.text().toAscii()))))
        self.control_tabs_grid_layout_1.addWidget(self._radioRspDisplay_tool_bar, 0, 2, 1, 2)
        for r in range(0, 1):
            self.control_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 4):
            self.control_tabs_grid_layout_1.setColumnStretch(c, 1)

        def _radioRsp_probe():
            while True:
                val = self.ndrControlBlock.get_radio_rsp()
                try:
                    self.set_radioRsp(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _radioRsp_thread = threading.Thread(target=_radioRsp_probe)
        _radioRsp_thread.daemon = True
        _radioRsp_thread.start()

        self._radioCmd_tool_bar = Qt.QToolBar(self)
        self._radioCmd_tool_bar.addWidget(Qt.QLabel('Command'+": "))
        self._radioCmd_line_edit = Qt.QLineEdit(str(self.radioCmd))
        self._radioCmd_tool_bar.addWidget(self._radioCmd_line_edit)
        self._radioCmd_line_edit.returnPressed.connect(
        	lambda: self.set_radioCmd(str(str(self._radioCmd_line_edit.text().toAscii()))))
        self.control_tabs_grid_layout_1.addWidget(self._radioCmd_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.control_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.control_tabs_grid_layout_1.setColumnStretch(c, 1)
        self._nbfsTxt_tool_bar = Qt.QToolBar(self)

        if None:
          self._nbfsTxt_formatter = None
        else:
          self._nbfsTxt_formatter = lambda x: str(x)

        self._nbfsTxt_tool_bar.addWidget(Qt.QLabel('Filter'+": "))
        self._nbfsTxt_label = Qt.QLabel(str(self._nbfsTxt_formatter(self.nbfsTxt)))
        self._nbfsTxt_tool_bar.addWidget(self._nbfsTxt_label)
        self.control_tabs_grid_layout_2.addWidget(self._nbfsTxt_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 3):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self.nbddcRxRateProbe = blocks.probe_rate(gr.sizeof_gr_complex*1, 100.0, rateProbeGain)
        self._nbddcRxRateLabel_tool_bar = Qt.QToolBar(self)

        if None:
          self._nbddcRxRateLabel_formatter = None
        else:
          self._nbddcRxRateLabel_formatter = lambda x: str(x)

        self._nbddcRxRateLabel_tool_bar.addWidget(Qt.QLabel('NBDDC Rx Rate'+": "))
        self._nbddcRxRateLabel_label = Qt.QLabel(str(self._nbddcRxRateLabel_formatter(self.nbddcRxRateLabel)))
        self._nbddcRxRateLabel_tool_bar.addWidget(self._nbddcRxRateLabel_label)
        self.control_tabs_grid_layout_1.addWidget(self._nbddcRxRateLabel_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.control_tabs_grid_layout_1.setColumnStretch(c, 1)

        def _nbddcRxRate_probe():
            while True:
                val = self.nbddcRxRateProbe.rate()
                try:
                    self.set_nbddcRxRate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _nbddcRxRate_thread = threading.Thread(target=_nbddcRxRate_probe)
        _nbddcRxRate_thread.daemon = True
        _nbddcRxRate_thread.start()


        def _nbddcFormatProbe_probe():
            while True:
                val = self.nbddc_tabs.setCurrentIndex(int(self.nbddcDemodType>=0))
                try:
                    self.set_nbddcFormatProbe(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _nbddcFormatProbe_thread = threading.Thread(target=_nbddcFormatProbe_probe)
        _nbddcFormatProbe_thread.daemon = True
        _nbddcFormatProbe_thread.start()

        self._nbddcDagcLevelSelection_range = Range(dagcRange[0], dagcRange[1], 1, nbddcDagcLevelSelectionCfg, 200)
        self._nbddcDagcLevelSelection_win = RangeWidget(self._nbddcDagcLevelSelection_range, self.set_nbddcDagcLevelSelection, "DAGC Gain (dB)", "counter_slider", int)
        self.control_tabs_grid_layout_2.addWidget(self._nbddcDagcLevelSelection_win, 2, 2, 1, 3)
        for r in range(2, 3):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 5):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbddcBfoSelection_range = Range(bfoRange[0], bfoRange[1], 1, nbddcBfoCfg, 200)
        self._nbddcBfoSelection_win = RangeWidget(self._nbddcBfoSelection_range, self.set_nbddcBfoSelection, 'BFO (Hz)', "counter_slider", int)
        self.control_tabs_grid_layout_2.addWidget(self._nbddcBfoSelection_win, 1, 5, 1, 3)
        for r in range(1, 2):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(5, 8):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self._nbddcAlcLevelSelection_range = Range(alcLevelRange[0], alcLevelRange[1], 1, nbddcAlcLevelSelectionCfg if radioType=="ndr328" else 0, 200)
        self._nbddcAlcLevelSelection_win = RangeWidget(self._nbddcAlcLevelSelection_range, self.set_nbddcAlcLevelSelection, "Alc Gain (Linear)", "counter_slider", int)
        self.control_tabs_grid_layout_2.addWidget(self._nbddcAlcLevelSelection_win, 1, 2, 1, 3)
        for r in range(1, 2):
            self.control_tabs_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 5):
            self.control_tabs_grid_layout_2.setColumnStretch(c, 1)
        self.nbIqSource = CyberRadio.vita_iq_source(
            vita_type=3,
            payload_size=1024,
            vita_header_size=36,
            vita_tail_size=4,
            byte_swapped=False,
            iq_swapped=False,
            iq_scale_factor=1.0/((2**15)-1),
            host='0.0.0.0',
            port_list=([wbddcUdpPort+1]),
            tagged=False,
            debug=False,
        )
        self._iqRssiRsp_tool_bar = Qt.QToolBar(self)
        self._iqRssiRsp_tool_bar.addWidget(Qt.QLabel('IQ RSSI'+": "))
        self._iqRssiRsp_line_edit = Qt.QLineEdit(str(self.iqRssiRsp))
        self._iqRssiRsp_tool_bar.addWidget(self._iqRssiRsp_line_edit)
        self._iqRssiRsp_line_edit.returnPressed.connect(
        	lambda: self.set_iqRssiRsp(str(str(self._iqRssiRsp_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._iqRssiRsp_tool_bar, 1, 2, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)

        def _iqRssi_probe():
            while True:
                val = self.nbIqDisplay.get_rssi()
                try:
                    self.set_iqRssi(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (0.5))
        _iqRssi_thread = threading.Thread(target=_iqRssi_probe)
        _iqRssi_thread.daemon = True
        _iqRssi_thread.start()

        self.demodUdpSource = blocks.udp_source(gr.sizeof_short*1, '0.0.0.0', wbddcUdpPort+5, 256*2+40, True)
        self.demodShortToFloat = blocks.short_to_float(1, (2**15)-1)
        self.demodRxRateProbe = blocks.probe_rate(gr.sizeof_float*1, 100.0, rateProbeGain)
        self._demodRxRateLabel_tool_bar = Qt.QToolBar(self)

        if None:
          self._demodRxRateLabel_formatter = None
        else:
          self._demodRxRateLabel_formatter = lambda x: str(x)

        self._demodRxRateLabel_tool_bar.addWidget(Qt.QLabel('Demod Rx Rate'+": "))
        self._demodRxRateLabel_label = Qt.QLabel(str(self._demodRxRateLabel_formatter(self.demodRxRateLabel)))
        self._demodRxRateLabel_tool_bar.addWidget(self._demodRxRateLabel_label)
        self.control_tabs_grid_layout_1.addWidget(self._demodRxRateLabel_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.control_tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.control_tabs_grid_layout_1.setColumnStretch(c, 1)

        def _demodRxRate_probe():
            while True:
                val = self.demodRxRateProbe.rate()
                try:
                    self.set_demodRxRate(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _demodRxRate_thread = threading.Thread(target=_demodRxRate_probe)
        _demodRxRate_thread.daemon = True
        _demodRxRate_thread.start()

        self._demodRssiRsp_tool_bar = Qt.QToolBar(self)
        self._demodRssiRsp_tool_bar.addWidget(Qt.QLabel('Demod RSSI'+": "))
        self._demodRssiRsp_line_edit = Qt.QLineEdit(str(self.demodRssiRsp))
        self._demodRssiRsp_tool_bar.addWidget(self._demodRssiRsp_line_edit)
        self._demodRssiRsp_line_edit.returnPressed.connect(
        	lambda: self.set_demodRssiRsp(str(str(self._demodRssiRsp_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._demodRssiRsp_tool_bar, 1, 4, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)

        def _demodRssi_probe():
            while True:
                val = self.demodDisplay.get_rssi()
                try:
                    self.set_demodRssi(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (0.5))
        _demodRssi_thread = threading.Thread(target=_demodRssi_probe)
        _demodRssi_thread.daemon = True
        _demodRssi_thread.start()

        self.demodPayloadExtractor = blocks.keep_m_in_n(gr.sizeof_short, 256, 552/2, 18)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_udp_sink_0_0_0 = blocks.udp_sink(gr.sizeof_float*1, '0.0.0.0', 55002, 256*4, True)
        self.blocks_udp_sink_0_0 = blocks.udp_sink(gr.sizeof_float*1, '0.0.0.0', 55002, 256*4, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_short*1, '0.0.0.0', 55001, 2048*2, True)
        self.blocks_sub_xx_0 = blocks.sub_ss(1)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0_1 = blocks.multiply_const_vff((1 if nbddcSinadSRC==3 else 0, ))
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_vff((1 if nbddcSinadSRC==2 else 0, ))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((1 if nbddcSinadSRC==1 else 0, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((1 if nbddcSinadSRC==0 else 0, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((1.0/32768, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((32768/pi, ))
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 1)
        self.blocks_delay_1 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_short*1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_arg_0_0 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_arg_0_0, 0), (self.blocks_multiply_const_vxx_1_0_1, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_delay_1, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_arg_0_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_udp_sink_0_0_0, 0))
        self.connect((self.demodPayloadExtractor, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.demodPayloadExtractor, 0), (self.demodShortToFloat, 0))
        self.connect((self.demodShortToFloat, 0), (self.blocks_udp_sink_0_0, 0))
        self.connect((self.demodShortToFloat, 0), (self.demodDisplay, 0))
        self.connect((self.demodShortToFloat, 0), (self.demodRxRateProbe, 0))
        self.connect((self.demodUdpSource, 0), (self.demodPayloadExtractor, 0))
        self.connect((self.nbIqSource, 0), (self.blocks_delay_1, 0))
        self.connect((self.nbIqSource, 0), (self.nbIqDisplay, 0))
        self.connect((self.nbIqSource, 0), (self.nbddcRxRateProbe, 0))
        self.connect((self.ndrControlBlock, 0), (self.stdoutFileDescriptor, 0))
        self.connect((self.spectralByteToFloat, 0), (self.spectralGuiAveraging, 0))
        self.connect((self.spectralByteToFloat, 0), (self.spectralVectorSink, 0))
        self.connect((self.spectralGuiAveraging, 0), (self.spectralVectorSink, 1))
        self.connect((self.spectralPayloadExtractor, 0), (self.spectralStreamToVector, 0))
        self.connect((self.spectralStreamToVector, 0), (self.spectralByteToFloat, 0))
        self.connect((self.spectralUdpSource, 0), (self.spectralPayloadExtractor, 0))
        self.connect((self.wbIqSource, 0), (self.wbIqDisplay, 0))
        self.connect((self.wbIqSource, 0), (self.wbddcRxRateProbe, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ndr804_display")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_configPath(self):
        return self.configPath

    def set_configPath(self, configPath):
        self.configPath = configPath
        self.set_configFile(self.configPath if self.configPath is not None else os.path.join("/public","ndrDemoGui","ndr804_display.%s.cfg"%self.radioType))

    def get_dataPort(self):
        return self.dataPort

    def set_dataPort(self, dataPort):
        self.dataPort = dataPort
        self.ndrControlBlock.set_dataPort(self.dataPort)

    def get_hostname(self):
        return self.hostname

    def set_hostname(self, hostname):
        self.hostname = hostname
        self.ndrControlBlock.set_hostname(self.hostname)

    def get_ifname(self):
        return self.ifname

    def set_ifname(self, ifname):
        self.ifname = ifname
        self.ndrControlBlock.set_interface(str(self.ifname))

    def get_radioType(self):
        return self.radioType

    def set_radioType(self, radioType):
        self.radioType = radioType
        self.set_squelchRange([-150,21] if self.radioType=="ndr328" else [0,0])
        self.ndrControlBlock.set_radioType(self.radioType)
        self.set_dagcRange([0,127] if self.radioType=="ndr328" else [0,0])
        self.set_bfoRange([-4000,4000] if self.radioType=="ndr328" else [0,0])
        self.set_alcLevelRange([0,127] if self.radioType=="ndr328" else [0,0])
        self.set_nbddcAlcLevelSelection(self.nbddcAlcLevelSelectionCfg if self.radioType=="ndr328" else 0)
        self.set_configFile(self.configPath if self.configPath is not None else os.path.join("/public","ndrDemoGui","ndr804_display.%s.cfg"%self.radioType))

    def get_verbose(self):
        return self.verbose

    def set_verbose(self, verbose):
        self.verbose = verbose

    def get_radioObj(self):
        return self.radioObj

    def set_radioObj(self, radioObj):
        self.radioObj = radioObj

    def get_configFile(self):
        return self.configFile

    def set_configFile(self, configFile):
        self.configFile = configFile
        self._nbddcBfoCfg_config = ConfigParser.ConfigParser()
        self._nbddcBfoCfg_config.read(self.configFile)
        if not self._nbddcBfoCfg_config.has_section('Demod'):
        	self._nbddcBfoCfg_config.add_section('Demod')
        self._nbddcBfoCfg_config.set('Demod', 'bfo', str(self.nbddcBfo))
        self._nbddcBfoCfg_config.write(open(self.configFile, 'w'))
        self._wbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcRateIndexCfg_config.read(self.configFile)
        if not self._wbddcRateIndexCfg_config.has_section('WBDDC'):
        	self._wbddcRateIndexCfg_config.add_section('WBDDC')
        self._wbddcRateIndexCfg_config.set('WBDDC', 'rateIndex', str(self.wbddcRateIndex))
        self._wbddcRateIndexCfg_config.write(open(self.configFile, 'w'))
        self._wbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcIndexCfg_config.read(self.configFile)
        if not self._wbddcIndexCfg_config.has_section('WBDDC'):
        	self._wbddcIndexCfg_config.add_section('WBDDC')
        self._wbddcIndexCfg_config.set('WBDDC', 'index', str(self.wbddcIndex))
        self._wbddcIndexCfg_config.write(open(self.configFile, 'w'))
        self._wbddcFormatCfg_config = ConfigParser.ConfigParser()
        self._wbddcFormatCfg_config.read(self.configFile)
        if not self._wbddcFormatCfg_config.has_section('WBDDC'):
        	self._wbddcFormatCfg_config.add_section('WBDDC')
        self._wbddcFormatCfg_config.set('WBDDC', 'format', str(self.wbddcFormat))
        self._wbddcFormatCfg_config.write(open(self.configFile, 'w'))
        self._specRateCfg_config = ConfigParser.ConfigParser()
        self._specRateCfg_config.read(self.configFile)
        if not self._specRateCfg_config.has_section('WBDDC'):
        	self._specRateCfg_config.add_section('WBDDC')
        self._specRateCfg_config.set('WBDDC', 'specRate', str(self.specRate))
        self._specRateCfg_config.write(open(self.configFile, 'w'))
        self._rfIndexCfg_config = ConfigParser.ConfigParser()
        self._rfIndexCfg_config.read(self.configFile)
        if not self._rfIndexCfg_config.has_section('Tuner'):
        	self._rfIndexCfg_config.add_section('Tuner')
        self._rfIndexCfg_config.set('Tuner', 'index', str(self.rfIndex))
        self._rfIndexCfg_config.write(open(self.configFile, 'w'))
        self._rfFreqCfg_config = ConfigParser.ConfigParser()
        self._rfFreqCfg_config.read(self.configFile)
        if not self._rfFreqCfg_config.has_section('Tuner'):
        	self._rfFreqCfg_config.add_section('Tuner')
        self._rfFreqCfg_config.set('Tuner', 'freq', str(self.rfFreq))
        self._rfFreqCfg_config.write(open(self.configFile, 'w'))
        self._rfFilterCfg_config = ConfigParser.ConfigParser()
        self._rfFilterCfg_config.read(self.configFile)
        if not self._rfFilterCfg_config.has_section('Tuner'):
        	self._rfFilterCfg_config.add_section('Tuner')
        self._rfFilterCfg_config.set('Tuner', 'filter', str(self.rfFilter))
        self._rfFilterCfg_config.write(open(self.configFile, 'w'))
        self._rfAttenCfg_config = ConfigParser.ConfigParser()
        self._rfAttenCfg_config.read(self.configFile)
        if not self._rfAttenCfg_config.has_section('Tuner'):
        	self._rfAttenCfg_config.add_section('Tuner')
        self._rfAttenCfg_config.set('Tuner', 'atten', str(self.rfAtten))
        self._rfAttenCfg_config.write(open(self.configFile, 'w'))
        self._radioCmdCfg_config = ConfigParser.ConfigParser()
        self._radioCmdCfg_config.read(self.configFile)
        if not self._radioCmdCfg_config.has_section('Radio'):
        	self._radioCmdCfg_config.add_section('Radio')
        self._radioCmdCfg_config.set('Radio', 'cmd', str(self.radioCmd))
        self._radioCmdCfg_config.write(open(self.configFile, 'w'))
        self._nbddcSquelchLevelCfg_config = ConfigParser.ConfigParser()
        self._nbddcSquelchLevelCfg_config.read(self.configFile)
        if not self._nbddcSquelchLevelCfg_config.has_section('Demod'):
        	self._nbddcSquelchLevelCfg_config.add_section('Demod')
        self._nbddcSquelchLevelCfg_config.set('Demod', 'squelchLevel', str(self.nbddcSquelchLevel))
        self._nbddcSquelchLevelCfg_config.write(open(self.configFile, 'w'))
        self._nbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcRateIndexCfg_config.read(self.configFile)
        if not self._nbddcRateIndexCfg_config.has_section('NBDDC'):
        	self._nbddcRateIndexCfg_config.add_section('NBDDC')
        self._nbddcRateIndexCfg_config.set('NBDDC', 'rateIndex', str(self.nbddcRateIndex))
        self._nbddcRateIndexCfg_config.write(open(self.configFile, 'w'))
        self._nbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcIndexCfg_config.read(self.configFile)
        if not self._nbddcIndexCfg_config.has_section('NBDDC'):
        	self._nbddcIndexCfg_config.add_section('NBDDC')
        self._nbddcIndexCfg_config.set('NBDDC', 'index', str(self.nbddcIndex))
        self._nbddcIndexCfg_config.write(open(self.configFile, 'w'))
        self._nbddcEnableCfg_config = ConfigParser.ConfigParser()
        self._nbddcEnableCfg_config.read(self.configFile)
        if not self._nbddcEnableCfg_config.has_section('NBDDC'):
        	self._nbddcEnableCfg_config.add_section('NBDDC')
        self._nbddcEnableCfg_config.set('NBDDC', 'enable', str(self.nbddcEnable))
        self._nbddcEnableCfg_config.write(open(self.configFile, 'w'))
        self._nbddcDemodTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcDemodTypeCfg_config.read(self.configFile)
        if not self._nbddcDemodTypeCfg_config.has_section('Demod'):
        	self._nbddcDemodTypeCfg_config.add_section('Demod')
        self._nbddcDemodTypeCfg_config.set('Demod', 'type', str(self.nbddcDemodType))
        self._nbddcDemodTypeCfg_config.write(open(self.configFile, 'w'))
        self._nbddcDemodDcBlockCfg_config = ConfigParser.ConfigParser()
        self._nbddcDemodDcBlockCfg_config.read(self.configFile)
        if not self._nbddcDemodDcBlockCfg_config.has_section('Demod'):
        	self._nbddcDemodDcBlockCfg_config.add_section('Demod')
        self._nbddcDemodDcBlockCfg_config.set('Demod', 'dcBlock', str(self.nbddcDemodDcBlock))
        self._nbddcDemodDcBlockCfg_config.write(open(self.configFile, 'w'))
        self._nbddcDagcTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcDagcTypeCfg_config.read(self.configFile)
        if not self._nbddcDagcTypeCfg_config.has_section('Demod'):
        	self._nbddcDagcTypeCfg_config.add_section('Demod')
        self._nbddcDagcTypeCfg_config.set('Demod', 'dagcType', str(self.nbddcDagcType))
        self._nbddcDagcTypeCfg_config.write(open(self.configFile, 'w'))
        self._nbddcDagcLevelSelectionCfg_config = ConfigParser.ConfigParser()
        self._nbddcDagcLevelSelectionCfg_config.read(self.configFile)
        if not self._nbddcDagcLevelSelectionCfg_config.has_section('Demod'):
        	self._nbddcDagcLevelSelectionCfg_config.add_section('Demod')
        self._nbddcDagcLevelSelectionCfg_config.set('Demod', 'dagcLevel', str(self.nbddcDagcLevelSelection))
        self._nbddcDagcLevelSelectionCfg_config.write(open(self.configFile, 'w'))
        self._nbddcAlcTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcAlcTypeCfg_config.read(self.configFile)
        if not self._nbddcAlcTypeCfg_config.has_section('Demod'):
        	self._nbddcAlcTypeCfg_config.add_section('Demod')
        self._nbddcAlcTypeCfg_config.set('Demod', 'alcType', str(self.nbddcAlcType))
        self._nbddcAlcTypeCfg_config.write(open(self.configFile, 'w'))
        self._nbddcAlcLevelSelectionCfg_config = ConfigParser.ConfigParser()
        self._nbddcAlcLevelSelectionCfg_config.read(self.configFile)
        if not self._nbddcAlcLevelSelectionCfg_config.has_section('Demod'):
        	self._nbddcAlcLevelSelectionCfg_config.add_section('Demod')
        self._nbddcAlcLevelSelectionCfg_config.set('Demod', 'alcLevel', str(self.nbddcAlcLevelSelection))
        self._nbddcAlcLevelSelectionCfg_config.write(open(self.configFile, 'w'))
        self._nbFrqCfg_config = ConfigParser.ConfigParser()
        self._nbFrqCfg_config.read(self.configFile)
        if not self._nbFrqCfg_config.has_section('NBDDC'):
        	self._nbFrqCfg_config.add_section('NBDDC')
        self._nbFrqCfg_config.set('NBDDC', 'freq', str(self.nbFrq))
        self._nbFrqCfg_config.write(open(self.configFile, 'w'))
        self._calFreqCfg_config = ConfigParser.ConfigParser()
        self._calFreqCfg_config.read(self.configFile)
        if not self._calFreqCfg_config.has_section('Cal'):
        	self._calFreqCfg_config.add_section('Cal')
        self._calFreqCfg_config.set('Cal', 'freq', str(self.calFreq))
        self._calFreqCfg_config.write(open(self.configFile, 'w'))
        self._calEnableCfg_config = ConfigParser.ConfigParser()
        self._calEnableCfg_config.read(self.configFile)
        if not self._calEnableCfg_config.has_section('Cal'):
        	self._calEnableCfg_config.add_section('Cal')
        self._calEnableCfg_config.set('Cal', 'enable', str(self.calEnable))
        self._calEnableCfg_config.write(open(self.configFile, 'w'))

    def get_wbddcRateSet(self):
        return self.wbddcRateSet

    def set_wbddcRateSet(self, wbddcRateSet):
        self.wbddcRateSet = wbddcRateSet
        self.set_fsWb(self.wbddcRateSet[self.wbddcRateIndex])

    def get_nbddcRateIndexOptions(self):
        return self.nbddcRateIndexOptions

    def set_nbddcRateIndexOptions(self, nbddcRateIndexOptions):
        self.nbddcRateIndexOptions = nbddcRateIndexOptions
        self.set_nbddcRateIndexCfg(self.nbddcRateIndexOptions[0])

    def get_nbddcIndexCfg(self):
        return self.nbddcIndexCfg

    def set_nbddcIndexCfg(self, nbddcIndexCfg):
        self.nbddcIndexCfg = nbddcIndexCfg
        self.set_nbddcIndex(self.nbddcIndexCfg)

    def get_wbddcRateIndexCfg(self):
        return self.wbddcRateIndexCfg

    def set_wbddcRateIndexCfg(self, wbddcRateIndexCfg):
        self.wbddcRateIndexCfg = wbddcRateIndexCfg
        self.set_wbddcRateIndex(self.wbddcRateIndexCfg)

    def get_nbddcRateIndexCfg(self):
        return self.nbddcRateIndexCfg

    def set_nbddcRateIndexCfg(self, nbddcRateIndexCfg):
        self.nbddcRateIndexCfg = nbddcRateIndexCfg
        self.set_nbddcRateIndex(self.nbddcRateIndexCfg)

    def get_nbddcIndex(self):
        return self.nbddcIndex

    def set_nbddcIndex(self, nbddcIndex):
        self.nbddcIndex = nbddcIndex
        self._nbddcIndex_callback(self.nbddcIndex)
        self.set_nbddcEnable(self.nbddcIndex>=0)
        self.ndrControlBlock.set_nbddcIndex(self.nbddcIndex)
        self.set_nbddcRateSet(radioObj.getNbddcRateSet(self.nbddcIndex))
        self._nbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcIndexCfg_config.read(self.configFile)
        if not self._nbddcIndexCfg_config.has_section('NBDDC'):
        	self._nbddcIndexCfg_config.add_section('NBDDC')
        self._nbddcIndexCfg_config.set('NBDDC', 'index', str(self.nbddcIndex))
        self._nbddcIndexCfg_config.write(open(self.configFile, 'w'))
        self.set_nbddcBwSet(radioObj.getNbddcBwSet(self.nbddcIndex))

    def get_nbddcDagcTypeCfg(self):
        return self.nbddcDagcTypeCfg

    def set_nbddcDagcTypeCfg(self, nbddcDagcTypeCfg):
        self.nbddcDagcTypeCfg = nbddcDagcTypeCfg
        self.set_nbddcDagcLevelSelectionCfg(dagcDefault.get(self.nbddcDagcTypeCfg,0))

    def get_nbddcAlcTypeCfg(self):
        return self.nbddcAlcTypeCfg

    def set_nbddcAlcTypeCfg(self, nbddcAlcTypeCfg):
        self.nbddcAlcTypeCfg = nbddcAlcTypeCfg
        self.set_nbddcAlcType(self.nbddcAlcTypeCfg)
        self.set_nbddcAlcLevelSelectionCfg(alcDefault.get(self.nbddcAlcTypeCfg))

    def get_dagcDefault(self):
        return self.dagcDefault

    def set_dagcDefault(self, dagcDefault):
        self.dagcDefault = dagcDefault

    def get_alcDefault(self):
        return self.alcDefault

    def set_alcDefault(self, alcDefault):
        self.alcDefault = alcDefault

    def get_wbddcRateIndex(self):
        return self.wbddcRateIndex

    def set_wbddcRateIndex(self, wbddcRateIndex):
        self.wbddcRateIndex = wbddcRateIndex
        self._wbddcRateIndex_callback(self.wbddcRateIndex)
        self.ndrControlBlock.set_wbddcRate(self.wbddcRateIndex)
        self.set_fsWb(self.wbddcRateSet[self.wbddcRateIndex])
        self._wbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcRateIndexCfg_config.read(self.configFile)
        if not self._wbddcRateIndexCfg_config.has_section('WBDDC'):
        	self._wbddcRateIndexCfg_config.add_section('WBDDC')
        self._wbddcRateIndexCfg_config.set('WBDDC', 'rateIndex', str(self.wbddcRateIndex))
        self._wbddcRateIndexCfg_config.write(open(self.configFile, 'w'))

    def get_wbddcFormatCfg(self):
        return self.wbddcFormatCfg

    def set_wbddcFormatCfg(self, wbddcFormatCfg):
        self.wbddcFormatCfg = wbddcFormatCfg
        self.set_wbddcFormat(self.wbddcFormatCfg)

    def get_squelchRange(self):
        return self.squelchRange

    def set_squelchRange(self, squelchRange):
        self.squelchRange = squelchRange
        self.set_nbddcSquelchLevelCfg(self.squelchRange[0])

    def get_rfIndexCfg(self):
        return self.rfIndexCfg

    def set_rfIndexCfg(self, rfIndexCfg):
        self.rfIndexCfg = rfIndexCfg
        self.set_rfIndex(self.rfIndexCfg)
        self.set_wbddcIndexCfg(self.rfIndexCfg)

    def get_nbddcRateSet(self):
        return self.nbddcRateSet

    def set_nbddcRateSet(self, nbddcRateSet):
        self.nbddcRateSet = nbddcRateSet
        self.set_fsNb(self.nbddcRateSet[self.nbddcRateIndex])

    def get_nbddcRateIndex(self):
        return self.nbddcRateIndex

    def set_nbddcRateIndex(self, nbddcRateIndex):
        self.nbddcRateIndex = nbddcRateIndex
        self._nbddcRateIndex_callback(self.nbddcRateIndex)
        self.set_fsNb(self.nbddcRateSet[self.nbddcRateIndex])
        self.ndrControlBlock.set_nbddcRate(self.nbddcRateIndex)
        self._nbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcRateIndexCfg_config.read(self.configFile)
        if not self._nbddcRateIndexCfg_config.has_section('NBDDC'):
        	self._nbddcRateIndexCfg_config.add_section('NBDDC')
        self._nbddcRateIndexCfg_config.set('NBDDC', 'rateIndex', str(self.nbddcRateIndex))
        self._nbddcRateIndexCfg_config.write(open(self.configFile, 'w'))
        self.set_bwNb(self.nbddcBwSet[self.nbddcRateIndex])

    def get_nbddcDemodTypeCfg(self):
        return self.nbddcDemodTypeCfg

    def set_nbddcDemodTypeCfg(self, nbddcDemodTypeCfg):
        self.nbddcDemodTypeCfg = nbddcDemodTypeCfg
        self.set_nbddcDemodType(self.nbddcDemodTypeCfg)

    def get_nbddcDagcLevelSelectionCfg(self):
        return self.nbddcDagcLevelSelectionCfg

    def set_nbddcDagcLevelSelectionCfg(self, nbddcDagcLevelSelectionCfg):
        self.nbddcDagcLevelSelectionCfg = nbddcDagcLevelSelectionCfg
        self.set_nbddcDagcLevelSelection(self.nbddcDagcLevelSelectionCfg)

    def get_nbddcBwSet(self):
        return self.nbddcBwSet

    def set_nbddcBwSet(self, nbddcBwSet):
        self.nbddcBwSet = nbddcBwSet
        self.set_bwNb(self.nbddcBwSet[self.nbddcRateIndex])

    def get_nbddcBfoCfg(self):
        return self.nbddcBfoCfg

    def set_nbddcBfoCfg(self, nbddcBfoCfg):
        self.nbddcBfoCfg = nbddcBfoCfg
        self.set_nbddcBfoSelection(self.nbddcBfoCfg)

    def get_nbddcAlcLevelSelectionCfg(self):
        return self.nbddcAlcLevelSelectionCfg

    def set_nbddcAlcLevelSelectionCfg(self, nbddcAlcLevelSelectionCfg):
        self.nbddcAlcLevelSelectionCfg = nbddcAlcLevelSelectionCfg
        self.set_nbddcAlcLevelSelection(self.nbddcAlcLevelSelectionCfg if self.radioType=="ndr328" else 0)

    def get_wbddcRxRate(self):
        return self.wbddcRxRate

    def set_wbddcRxRate(self, wbddcRxRate):
        self.wbddcRxRate = wbddcRxRate
        self.set_wbddcRxRateLabel(self._wbddcRxRateLabel_formatter("%5.1f%%"%(100.0*self.wbddcRxRate/self.fsWb)))

    def get_wbddcFormat(self):
        return self.wbddcFormat

    def set_wbddcFormat(self, wbddcFormat):
        self.wbddcFormat = wbddcFormat
        self.set_wbddcIndex(self.rfIndex if self.wbddcFormat in (0,1) else -1)
        self._wbddcFormat_callback(self.wbddcFormat)
        self.ndrControlBlock.set_wbddcFormat(self.wbddcFormat)
        self._wbddcFormatCfg_config = ConfigParser.ConfigParser()
        self._wbddcFormatCfg_config.read(self.configFile)
        if not self._wbddcFormatCfg_config.has_section('WBDDC'):
        	self._wbddcFormatCfg_config.add_section('WBDDC')
        self._wbddcFormatCfg_config.set('WBDDC', 'format', str(self.wbddcFormat))
        self._wbddcFormatCfg_config.write(open(self.configFile, 'w'))

    def get_specRateCfg(self):
        return self.specRateCfg

    def set_specRateCfg(self, specRateCfg):
        self.specRateCfg = specRateCfg
        self.set_specRate(self.specRateCfg)

    def get_rssiResponse(self):
        return self.rssiResponse

    def set_rssiResponse(self, rssiResponse):
        self.rssiResponse = rssiResponse
        self.set_rssiRspBox(self.rssiResponse)

    def get_rfIndex(self):
        return self.rfIndex

    def set_rfIndex(self, rfIndex):
        self.rfIndex = rfIndex
        self.set_wbddcIndex(self.rfIndex if self.wbddcFormat in (0,1) else -1)
        self._rfIndex_callback(self.rfIndex)
        self.ndrControlBlock.set_tunerIndex(self.rfIndex)
        self._rfIndexCfg_config = ConfigParser.ConfigParser()
        self._rfIndexCfg_config.read(self.configFile)
        if not self._rfIndexCfg_config.has_section('Tuner'):
        	self._rfIndexCfg_config.add_section('Tuner')
        self._rfIndexCfg_config.set('Tuner', 'index', str(self.rfIndex))
        self._rfIndexCfg_config.write(open(self.configFile, 'w'))

    def get_rfFreqCfg(self):
        return self.rfFreqCfg

    def set_rfFreqCfg(self, rfFreqCfg):
        self.rfFreqCfg = rfFreqCfg
        self.set_rfFreq(self.rfFreqCfg)

    def get_rfFilterCfg(self):
        return self.rfFilterCfg

    def set_rfFilterCfg(self, rfFilterCfg):
        self.rfFilterCfg = rfFilterCfg
        self.set_rfFilter(self.rfFilterCfg)

    def get_rfAttenCfg(self):
        return self.rfAttenCfg

    def set_rfAttenCfg(self, rfAttenCfg):
        self.rfAttenCfg = rfAttenCfg
        self.set_rfAtten(self.rfAttenCfg)

    def get_radioRsp(self):
        return self.radioRsp

    def set_radioRsp(self, radioRsp):
        self.radioRsp = radioRsp
        self.set_radioRspDisplay(self.radioRsp)

    def get_radioCmdCfg(self):
        return self.radioCmdCfg

    def set_radioCmdCfg(self, radioCmdCfg):
        self.radioCmdCfg = radioCmdCfg
        self.set_radioCmd(self.radioCmdCfg)

    def get_nbddcSquelchLevelCfg(self):
        return self.nbddcSquelchLevelCfg

    def set_nbddcSquelchLevelCfg(self, nbddcSquelchLevelCfg):
        self.nbddcSquelchLevelCfg = nbddcSquelchLevelCfg
        self.set_nbddcSquelchLevel(self.nbddcSquelchLevelCfg)

    def get_nbddcRxRate(self):
        return self.nbddcRxRate

    def set_nbddcRxRate(self, nbddcRxRate):
        self.nbddcRxRate = nbddcRxRate
        self.set_nbddcRxRateLabel(self._nbddcRxRateLabel_formatter("%5.1f%%"%(100.0*self.nbddcRxRate/self.fsNb)))

    def get_nbddcDemodType(self):
        return self.nbddcDemodType

    def set_nbddcDemodType(self, nbddcDemodType):
        self.nbddcDemodType = nbddcDemodType
        self._nbddcDemodType_callback(self.nbddcDemodType)
        self.set_nbddcBfo(self.nbddcBfoSelection if self.nbddcDemodType==0 else 0)
        self.ndrControlBlock.set_nbddcDemodType(self.nbddcDemodType)
        self._nbddcDemodTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcDemodTypeCfg_config.read(self.configFile)
        if not self._nbddcDemodTypeCfg_config.has_section('Demod'):
        	self._nbddcDemodTypeCfg_config.add_section('Demod')
        self._nbddcDemodTypeCfg_config.set('Demod', 'type', str(self.nbddcDemodType))
        self._nbddcDemodTypeCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcDemodDcBlockCfg(self):
        return self.nbddcDemodDcBlockCfg

    def set_nbddcDemodDcBlockCfg(self, nbddcDemodDcBlockCfg):
        self.nbddcDemodDcBlockCfg = nbddcDemodDcBlockCfg
        self.set_nbddcDemodDcBlock(self.nbddcDemodDcBlockCfg)

    def get_nbddcDagcType(self):
        return self.nbddcDagcType

    def set_nbddcDagcType(self, nbddcDagcType):
        self.nbddcDagcType = nbddcDagcType
        self._nbddcDagcType_callback(self.nbddcDagcType)
        self.set_nbddcDagcLevel(dagcMultiplier.get(self.nbddcDagcType,1)*self.nbddcDagcLevelSelection)
        self.ndrControlBlock.set_nbddcDagcType(self.nbddcDagcType)
        self._nbddcDagcTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcDagcTypeCfg_config.read(self.configFile)
        if not self._nbddcDagcTypeCfg_config.has_section('Demod'):
        	self._nbddcDagcTypeCfg_config.add_section('Demod')
        self._nbddcDagcTypeCfg_config.set('Demod', 'dagcType', str(self.nbddcDagcType))
        self._nbddcDagcTypeCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcDagcLevelSelection(self):
        return self.nbddcDagcLevelSelection

    def set_nbddcDagcLevelSelection(self, nbddcDagcLevelSelection):
        self.nbddcDagcLevelSelection = nbddcDagcLevelSelection
        self.set_nbddcDagcLevel(dagcMultiplier.get(self.nbddcDagcType,1)*self.nbddcDagcLevelSelection)
        self._nbddcDagcLevelSelectionCfg_config = ConfigParser.ConfigParser()
        self._nbddcDagcLevelSelectionCfg_config.read(self.configFile)
        if not self._nbddcDagcLevelSelectionCfg_config.has_section('Demod'):
        	self._nbddcDagcLevelSelectionCfg_config.add_section('Demod')
        self._nbddcDagcLevelSelectionCfg_config.set('Demod', 'dagcLevel', str(self.nbddcDagcLevelSelection))
        self._nbddcDagcLevelSelectionCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcBfoSelection(self):
        return self.nbddcBfoSelection

    def set_nbddcBfoSelection(self, nbddcBfoSelection):
        self.nbddcBfoSelection = nbddcBfoSelection
        self.set_nbddcBfo(self.nbddcBfoSelection if self.nbddcDemodType==0 else 0)

    def get_nbddcAlcType(self):
        return self.nbddcAlcType

    def set_nbddcAlcType(self, nbddcAlcType):
        self.nbddcAlcType = nbddcAlcType
        self._nbddcAlcType_callback(self.nbddcAlcType)
        self.set_nbddcAlcLevel(alcMultiplier.get(self.nbddcAlcType,1)*self.nbddcAlcLevelSelection)
        self.ndrControlBlock.set_nbddcDemodAlcType(self.nbddcAlcType)
        self._nbddcAlcTypeCfg_config = ConfigParser.ConfigParser()
        self._nbddcAlcTypeCfg_config.read(self.configFile)
        if not self._nbddcAlcTypeCfg_config.has_section('Demod'):
        	self._nbddcAlcTypeCfg_config.add_section('Demod')
        self._nbddcAlcTypeCfg_config.set('Demod', 'alcType', str(self.nbddcAlcType))
        self._nbddcAlcTypeCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcAlcLevelSelection(self):
        return self.nbddcAlcLevelSelection

    def set_nbddcAlcLevelSelection(self, nbddcAlcLevelSelection):
        self.nbddcAlcLevelSelection = nbddcAlcLevelSelection
        self.set_nbddcAlcLevel(alcMultiplier.get(self.nbddcAlcType,1)*self.nbddcAlcLevelSelection)
        self._nbddcAlcLevelSelectionCfg_config = ConfigParser.ConfigParser()
        self._nbddcAlcLevelSelectionCfg_config.read(self.configFile)
        if not self._nbddcAlcLevelSelectionCfg_config.has_section('Demod'):
        	self._nbddcAlcLevelSelectionCfg_config.add_section('Demod')
        self._nbddcAlcLevelSelectionCfg_config.set('Demod', 'alcLevel', str(self.nbddcAlcLevelSelection))
        self._nbddcAlcLevelSelectionCfg_config.write(open(self.configFile, 'w'))

    def get_nbFrqCfg(self):
        return self.nbFrqCfg

    def set_nbFrqCfg(self, nbFrqCfg):
        self.nbFrqCfg = nbFrqCfg
        self.set_nbFrq(self.nbFrqCfg)

    def get_iqRssi(self):
        return self.iqRssi

    def set_iqRssi(self, iqRssi):
        self.iqRssi = iqRssi
        self.set_iqRssiRsp(str(self.iqRssi))

    def get_fsWb(self):
        return self.fsWb

    def set_fsWb(self, fsWb):
        self.fsWb = fsWb
        self.set_wbddcRxRateLabel(self._wbddcRxRateLabel_formatter("%5.1f%%"%(100.0*self.wbddcRxRate/self.fsWb)))
        self.wbIqDisplay.set_sampRate(self.fsWb)

    def get_fsNb(self):
        return self.fsNb

    def set_fsNb(self, fsNb):
        self.fsNb = fsNb
        self.nbIqDisplay.set_sampRate(self.fsNb)
        self.set_nbfsTxt(self._nbfsTxt_formatter("%sHz @ %ssps"%(num_to_str(self.bwNb),num_to_str(self.fsNb))))
        self.set_nbddcRxRateLabel(self._nbddcRxRateLabel_formatter("%5.1f%%"%(100.0*self.nbddcRxRate/self.fsNb)))

    def get_fsDemod(self):
        return self.fsDemod

    def set_fsDemod(self, fsDemod):
        self.fsDemod = fsDemod
        self.demodDisplay.set_sampRate(self.fsDemod)
        self.set_demodRxRateLabel(self._demodRxRateLabel_formatter("%5.1f%%"%(100.0*self.demodRxRate/self.fsDemod)))

    def get_demodRxRate(self):
        return self.demodRxRate

    def set_demodRxRate(self, demodRxRate):
        self.demodRxRate = demodRxRate
        self.set_demodRxRateLabel(self._demodRxRateLabel_formatter("%5.1f%%"%(100.0*self.demodRxRate/self.fsDemod)))

    def get_demodRssi(self):
        return self.demodRssi

    def set_demodRssi(self, demodRssi):
        self.demodRssi = demodRssi
        self.set_demodRssiRsp(str(self.demodRssi))

    def get_dagcMultiplier(self):
        return self.dagcMultiplier

    def set_dagcMultiplier(self, dagcMultiplier):
        self.dagcMultiplier = dagcMultiplier

    def get_calFreqCfg(self):
        return self.calFreqCfg

    def set_calFreqCfg(self, calFreqCfg):
        self.calFreqCfg = calFreqCfg
        self.set_calFreq(self.calFreqCfg)

    def get_calEnableCfg(self):
        return self.calEnableCfg

    def set_calEnableCfg(self, calEnableCfg):
        self.calEnableCfg = calEnableCfg
        self.set_calEnable(bool(self.calEnableCfg))

    def get_bwNb(self):
        return self.bwNb

    def set_bwNb(self, bwNb):
        self.bwNb = bwNb
        self.set_nbfsTxt(self._nbfsTxt_formatter("%sHz @ %ssps"%(num_to_str(self.bwNb),num_to_str(self.fsNb))))

    def get_alcMultiplier(self):
        return self.alcMultiplier

    def set_alcMultiplier(self, alcMultiplier):
        self.alcMultiplier = alcMultiplier

    def get_wbddcUdpPort(self):
        return self.wbddcUdpPort

    def set_wbddcUdpPort(self, wbddcUdpPort):
        self.wbddcUdpPort = wbddcUdpPort
        self.ndrControlBlock.set_wbddcPort(self.wbddcUdpPort)
        self.ndrControlBlock.set_nbddcPort(self.wbddcUdpPort+1)
        self.ndrControlBlock.set_otherNbddcPort(self.wbddcUdpPort+2)

    def get_wbddcRxRateLabel(self):
        return self.wbddcRxRateLabel

    def set_wbddcRxRateLabel(self, wbddcRxRateLabel):
        self.wbddcRxRateLabel = wbddcRxRateLabel
        Qt.QMetaObject.invokeMethod(self._wbddcRxRateLabel_label, "setText", Qt.Q_ARG("QString", self.wbddcRxRateLabel))

    def get_wbddcIndexCfg(self):
        return self.wbddcIndexCfg

    def set_wbddcIndexCfg(self, wbddcIndexCfg):
        self.wbddcIndexCfg = wbddcIndexCfg

    def get_wbddcIndex(self):
        return self.wbddcIndex

    def set_wbddcIndex(self, wbddcIndex):
        self.wbddcIndex = wbddcIndex
        self.ndrControlBlock.set_wbddcEnable(self.wbddcIndex>0)
        self.ndrControlBlock.set_wbddcEnable(self.wbddcIndex>0)
        self.ndrControlBlock.set_wbddcIndex(self.wbddcIndex)
        self._wbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcIndexCfg_config.read(self.configFile)
        if not self._wbddcIndexCfg_config.has_section('WBDDC'):
        	self._wbddcIndexCfg_config.add_section('WBDDC')
        self._wbddcIndexCfg_config.set('WBDDC', 'index', str(self.wbddcIndex))
        self._wbddcIndexCfg_config.write(open(self.configFile, 'w'))

    def get_wbddcFormatProbe(self):
        return self.wbddcFormatProbe

    def set_wbddcFormatProbe(self, wbddcFormatProbe):
        self.wbddcFormatProbe = wbddcFormatProbe

    def get_specVecLen(self):
        return self.specVecLen

    def set_specVecLen(self, specVecLen):
        self.specVecLen = specVecLen

    def get_specRate(self):
        return self.specRate

    def set_specRate(self, specRate):
        self.specRate = specRate
        self._specRate_callback(self.specRate)
        self.ndrControlBlock.set_specRate(self.specRate)
        self._specRateCfg_config = ConfigParser.ConfigParser()
        self._specRateCfg_config.read(self.configFile)
        if not self._specRateCfg_config.has_section('WBDDC'):
        	self._specRateCfg_config.add_section('WBDDC')
        self._specRateCfg_config.set('WBDDC', 'specRate', str(self.specRate))
        self._specRateCfg_config.write(open(self.configFile, 'w'))

    def get_rssiRspBox(self):
        return self.rssiRspBox

    def set_rssiRspBox(self, rssiRspBox):
        self.rssiRspBox = rssiRspBox
        Qt.QMetaObject.invokeMethod(self._rssiRspBox_line_edit, "setText", Qt.Q_ARG("QString", str(self.rssiRspBox)))

    def get_rfFreq(self):
        return self.rfFreq

    def set_rfFreq(self, rfFreq):
        self.rfFreq = rfFreq
        self.ndrControlBlock.set_tunerFreq(self.rfFreq*1e6)
        self.ndrControlBlock.set_calFrequency((self.rfFreq+self.calFreq) if self.calEnable else 0)
        self.nbIqDisplay.set_centerFreq(self.rfFreq*1e6 + self.nbFrq)
        self.wbIqDisplay.set_centerFreq(self.rfFreq*1e6)
        self.spectralVectorSink.set_x_axis(self.rfFreq-25.6, 51.2/4096)
        self._rfFreqCfg_config = ConfigParser.ConfigParser()
        self._rfFreqCfg_config.read(self.configFile)
        if not self._rfFreqCfg_config.has_section('Tuner'):
        	self._rfFreqCfg_config.add_section('Tuner')
        self._rfFreqCfg_config.set('Tuner', 'freq', str(self.rfFreq))
        self._rfFreqCfg_config.write(open(self.configFile, 'w'))

    def get_rfFilter(self):
        return self.rfFilter

    def set_rfFilter(self, rfFilter):
        self.rfFilter = rfFilter
        self._rfFilter_callback(self.rfFilter)
        self.ndrControlBlock.set_tunerFilter(self.rfFilter)
        self._rfFilterCfg_config = ConfigParser.ConfigParser()
        self._rfFilterCfg_config.read(self.configFile)
        if not self._rfFilterCfg_config.has_section('Tuner'):
        	self._rfFilterCfg_config.add_section('Tuner')
        self._rfFilterCfg_config.set('Tuner', 'filter', str(self.rfFilter))
        self._rfFilterCfg_config.write(open(self.configFile, 'w'))

    def get_rfAtten(self):
        return self.rfAtten

    def set_rfAtten(self, rfAtten):
        self.rfAtten = rfAtten
        self.ndrControlBlock.set_tunerAtten(self.rfAtten)
        self._rfAttenCfg_config = ConfigParser.ConfigParser()
        self._rfAttenCfg_config.read(self.configFile)
        if not self._rfAttenCfg_config.has_section('Tuner'):
        	self._rfAttenCfg_config.add_section('Tuner')
        self._rfAttenCfg_config.set('Tuner', 'atten', str(self.rfAtten))
        self._rfAttenCfg_config.write(open(self.configFile, 'w'))

    def get_rateProbeGain(self):
        return self.rateProbeGain

    def set_rateProbeGain(self, rateProbeGain):
        self.rateProbeGain = rateProbeGain

    def get_radioRspTrigger(self):
        return self.radioRspTrigger

    def set_radioRspTrigger(self, radioRspTrigger):
        self.radioRspTrigger = radioRspTrigger
        self.ndrControlBlock.send_radio_rsp(self.radioRspTrigger)

    def get_radioRspDisplay(self):
        return self.radioRspDisplay

    def set_radioRspDisplay(self, radioRspDisplay):
        self.radioRspDisplay = radioRspDisplay
        Qt.QMetaObject.invokeMethod(self._radioRspDisplay_line_edit, "setText", Qt.Q_ARG("QString", str(self.radioRspDisplay)))

    def get_radioCmd(self):
        return self.radioCmd

    def set_radioCmd(self, radioCmd):
        self.radioCmd = radioCmd
        self.ndrControlBlock.set_radio_cmd(self.radioCmd)
        self._radioCmdCfg_config = ConfigParser.ConfigParser()
        self._radioCmdCfg_config.read(self.configFile)
        if not self._radioCmdCfg_config.has_section('Radio'):
        	self._radioCmdCfg_config.add_section('Radio')
        self._radioCmdCfg_config.set('Radio', 'cmd', str(self.radioCmd))
        self._radioCmdCfg_config.write(open(self.configFile, 'w'))
        Qt.QMetaObject.invokeMethod(self._radioCmd_line_edit, "setText", Qt.Q_ARG("QString", str(self.radioCmd)))

    def get_plotRowSpan(self):
        return self.plotRowSpan

    def set_plotRowSpan(self, plotRowSpan):
        self.plotRowSpan = plotRowSpan

    def get_plotColSpan(self):
        return self.plotColSpan

    def set_plotColSpan(self, plotColSpan):
        self.plotColSpan = plotColSpan

    def get_otherNbddcEnable(self):
        return self.otherNbddcEnable

    def set_otherNbddcEnable(self, otherNbddcEnable):
        self.otherNbddcEnable = otherNbddcEnable
        self._otherNbddcEnable_callback(self.otherNbddcEnable)
        self.ndrControlBlock.set_otherNbddcEnable(self.otherNbddcEnable)

    def get_osDotSetCwd(self):
        return self.osDotSetCwd

    def set_osDotSetCwd(self, osDotSetCwd):
        self.osDotSetCwd = osDotSetCwd

    def get_nbfsTxt(self):
        return self.nbfsTxt

    def set_nbfsTxt(self, nbfsTxt):
        self.nbfsTxt = nbfsTxt
        Qt.QMetaObject.invokeMethod(self._nbfsTxt_label, "setText", Qt.Q_ARG("QString", self.nbfsTxt))

    def get_nbddcSquelchLevel(self):
        return self.nbddcSquelchLevel

    def set_nbddcSquelchLevel(self, nbddcSquelchLevel):
        self.nbddcSquelchLevel = nbddcSquelchLevel
        self.ndrControlBlock.set_nbddcDemodSquelchLevel(self.nbddcSquelchLevel)
        self._nbddcSquelchLevelCfg_config = ConfigParser.ConfigParser()
        self._nbddcSquelchLevelCfg_config.read(self.configFile)
        if not self._nbddcSquelchLevelCfg_config.has_section('Demod'):
        	self._nbddcSquelchLevelCfg_config.add_section('Demod')
        self._nbddcSquelchLevelCfg_config.set('Demod', 'squelchLevel', str(self.nbddcSquelchLevel))
        self._nbddcSquelchLevelCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcSinadSRC(self):
        return self.nbddcSinadSRC

    def set_nbddcSinadSRC(self, nbddcSinadSRC):
        self.nbddcSinadSRC = nbddcSinadSRC
        self._nbddcSinadSRC_callback(self.nbddcSinadSRC)
        self.blocks_multiply_const_vxx_1_0_1.set_k((1 if self.nbddcSinadSRC==3 else 0, ))
        self.blocks_multiply_const_vxx_1_0_0.set_k((1 if self.nbddcSinadSRC==2 else 0, ))
        self.blocks_multiply_const_vxx_1_0.set_k((1 if self.nbddcSinadSRC==1 else 0, ))
        self.blocks_multiply_const_vxx_1.set_k((1 if self.nbddcSinadSRC==0 else 0, ))

    def get_nbddcRxRateLabel(self):
        return self.nbddcRxRateLabel

    def set_nbddcRxRateLabel(self, nbddcRxRateLabel):
        self.nbddcRxRateLabel = nbddcRxRateLabel
        Qt.QMetaObject.invokeMethod(self._nbddcRxRateLabel_label, "setText", Qt.Q_ARG("QString", self.nbddcRxRateLabel))

    def get_nbddcFormatProbe(self):
        return self.nbddcFormatProbe

    def set_nbddcFormatProbe(self, nbddcFormatProbe):
        self.nbddcFormatProbe = nbddcFormatProbe

    def get_nbddcEnableCfg(self):
        return self.nbddcEnableCfg

    def set_nbddcEnableCfg(self, nbddcEnableCfg):
        self.nbddcEnableCfg = nbddcEnableCfg

    def get_nbddcEnable(self):
        return self.nbddcEnable

    def set_nbddcEnable(self, nbddcEnable):
        self.nbddcEnable = nbddcEnable
        self.ndrControlBlock.set_nbddcEnable(self.nbddcEnable)
        self._nbddcEnableCfg_config = ConfigParser.ConfigParser()
        self._nbddcEnableCfg_config.read(self.configFile)
        if not self._nbddcEnableCfg_config.has_section('NBDDC'):
        	self._nbddcEnableCfg_config.add_section('NBDDC')
        self._nbddcEnableCfg_config.set('NBDDC', 'enable', str(self.nbddcEnable))
        self._nbddcEnableCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcDemodDcBlock(self):
        return self.nbddcDemodDcBlock

    def set_nbddcDemodDcBlock(self, nbddcDemodDcBlock):
        self.nbddcDemodDcBlock = nbddcDemodDcBlock
        self._nbddcDemodDcBlock_callback(self.nbddcDemodDcBlock)
        self.ndrControlBlock.set_nbddcDemodDcBlock(self.nbddcDemodDcBlock)
        self._nbddcDemodDcBlockCfg_config = ConfigParser.ConfigParser()
        self._nbddcDemodDcBlockCfg_config.read(self.configFile)
        if not self._nbddcDemodDcBlockCfg_config.has_section('Demod'):
        	self._nbddcDemodDcBlockCfg_config.add_section('Demod')
        self._nbddcDemodDcBlockCfg_config.set('Demod', 'dcBlock', str(self.nbddcDemodDcBlock))
        self._nbddcDemodDcBlockCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcDagcLevel(self):
        return self.nbddcDagcLevel

    def set_nbddcDagcLevel(self, nbddcDagcLevel):
        self.nbddcDagcLevel = nbddcDagcLevel
        self.ndrControlBlock.set_nbddcDagcLevel(self.nbddcDagcLevel)

    def get_nbddcBfo(self):
        return self.nbddcBfo

    def set_nbddcBfo(self, nbddcBfo):
        self.nbddcBfo = nbddcBfo
        self.ndrControlBlock.set_nbddcDemodBfo(self.nbddcBfo)
        self._nbddcBfoCfg_config = ConfigParser.ConfigParser()
        self._nbddcBfoCfg_config.read(self.configFile)
        if not self._nbddcBfoCfg_config.has_section('Demod'):
        	self._nbddcBfoCfg_config.add_section('Demod')
        self._nbddcBfoCfg_config.set('Demod', 'bfo', str(self.nbddcBfo))
        self._nbddcBfoCfg_config.write(open(self.configFile, 'w'))

    def get_nbddcAlcLevel(self):
        return self.nbddcAlcLevel

    def set_nbddcAlcLevel(self, nbddcAlcLevel):
        self.nbddcAlcLevel = nbddcAlcLevel
        self.ndrControlBlock.set_nbddcDemodAlcLevel(self.nbddcAlcLevel)

    def get_nbFrq(self):
        return self.nbFrq

    def set_nbFrq(self, nbFrq):
        self.nbFrq = nbFrq
        self.ndrControlBlock.set_nbddcFreq(self.nbFrq)
        self.nbIqDisplay.set_centerFreq(self.rfFreq*1e6 + self.nbFrq)
        self._nbFrqCfg_config = ConfigParser.ConfigParser()
        self._nbFrqCfg_config.read(self.configFile)
        if not self._nbFrqCfg_config.has_section('NBDDC'):
        	self._nbFrqCfg_config.add_section('NBDDC')
        self._nbFrqCfg_config.set('NBDDC', 'freq', str(self.nbFrq))
        self._nbFrqCfg_config.write(open(self.configFile, 'w'))

    def get_iqRssiRsp(self):
        return self.iqRssiRsp

    def set_iqRssiRsp(self, iqRssiRsp):
        self.iqRssiRsp = iqRssiRsp
        Qt.QMetaObject.invokeMethod(self._iqRssiRsp_line_edit, "setText", Qt.Q_ARG("QString", str(self.iqRssiRsp)))

    def get_iirAlpha(self):
        return self.iirAlpha

    def set_iirAlpha(self, iirAlpha):
        self.iirAlpha = iirAlpha
        self.spectralGuiAveraging.set_taps(2**-self.iirAlpha)

    def get_fsAudio(self):
        return self.fsAudio

    def set_fsAudio(self, fsAudio):
        self.fsAudio = fsAudio

    def get_demodRxRateLabel(self):
        return self.demodRxRateLabel

    def set_demodRxRateLabel(self, demodRxRateLabel):
        self.demodRxRateLabel = demodRxRateLabel
        Qt.QMetaObject.invokeMethod(self._demodRxRateLabel_label, "setText", Qt.Q_ARG("QString", self.demodRxRateLabel))

    def get_demodRssiRsp(self):
        return self.demodRssiRsp

    def set_demodRssiRsp(self, demodRssiRsp):
        self.demodRssiRsp = demodRssiRsp
        Qt.QMetaObject.invokeMethod(self._demodRssiRsp_line_edit, "setText", Qt.Q_ARG("QString", str(self.demodRssiRsp)))

    def get_dagcRange(self):
        return self.dagcRange

    def set_dagcRange(self, dagcRange):
        self.dagcRange = dagcRange

    def get_calFreq(self):
        return self.calFreq

    def set_calFreq(self, calFreq):
        self.calFreq = calFreq
        self.ndrControlBlock.set_calFrequency((self.rfFreq+self.calFreq) if self.calEnable else 0)
        self._calFreqCfg_config = ConfigParser.ConfigParser()
        self._calFreqCfg_config.read(self.configFile)
        if not self._calFreqCfg_config.has_section('Cal'):
        	self._calFreqCfg_config.add_section('Cal')
        self._calFreqCfg_config.set('Cal', 'freq', str(self.calFreq))
        self._calFreqCfg_config.write(open(self.configFile, 'w'))

    def get_calEnable(self):
        return self.calEnable

    def set_calEnable(self, calEnable):
        self.calEnable = calEnable
        self._calEnable_callback(self.calEnable)
        self.ndrControlBlock.set_calFrequency((self.rfFreq+self.calFreq) if self.calEnable else 0)
        self._calEnableCfg_config = ConfigParser.ConfigParser()
        self._calEnableCfg_config.read(self.configFile)
        if not self._calEnableCfg_config.has_section('Cal'):
        	self._calEnableCfg_config.add_section('Cal')
        self._calEnableCfg_config.set('Cal', 'enable', str(self.calEnable))
        self._calEnableCfg_config.write(open(self.configFile, 'w'))

    def get_bfoRange(self):
        return self.bfoRange

    def set_bfoRange(self, bfoRange):
        self.bfoRange = bfoRange

    def get_alcLevelRange(self):
        return self.alcLevelRange

    def set_alcLevelRange(self, alcLevelRange):
        self.alcLevelRange = alcLevelRange


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-d", "--dataPort", dest="dataPort", type="intx", default=2,
        help="Set Radio NIC Index [default=%default]")
    parser.add_option(
        "-n", "--hostname", dest="hostname", type="string", default='ndr308',
        help="Set Hostname/IP [default=%default]")
    parser.add_option(
        "-i", "--ifname", dest="ifname", type="string", default='enp3s0f1',
        help="Set 10GbE NIC [default=%default]")
    parser.add_option(
        "-r", "--radioType", dest="radioType", type="string", default='ndr328',
        help="Set Tuner Index [default=%default]")
    parser.add_option(
        "-v", "--verbose", dest="verbose", type="intx", default=1,
        help="Set Verbose Driver Mode [default=%default]")
    return parser


def main(top_block_cls=ndr804_display, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(dataPort=options.dataPort, hostname=options.hostname, ifname=options.ifname, radioType=options.radioType, verbose=options.verbose)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
