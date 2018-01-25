#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NDR651 High-Res FFT
# Generated: Wed Sep  6 16:13:38 2017
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
from gnuradio.eng_notation import *
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import ConfigParser
import CyberRadio
import CyberRadioDriver as crd
import os, numpy, time
import sip
import sys
from gnuradio import qtgui


class ndr651_txrx_gui(gr.top_block, Qt.QWidget):

    def __init__(self, dataPort1=1, dataPort2=1, dipIndex=-1, ducIndex=1, fftRate=8, fftSizeExp=15, hostname='ndr651', localInterface1="eth0", localInterface2="eth7"):
        gr.top_block.__init__(self, "NDR651 High-Res FFT")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDR651 High-Res FFT")
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

        self.settings = Qt.QSettings("GNU Radio", "ndr651_txrx_gui")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.dataPort1 = dataPort1
        self.dataPort2 = dataPort2
        self.dipIndex = dipIndex
        self.ducIndex = ducIndex
        self.fftRate = fftRate
        self.fftSizeExp = fftSizeExp
        self.hostname = hostname
        self.localInterface1 = localInterface1
        self.localInterface2 = localInterface2

        ##################################################
        # Variables
        ##################################################
        self.confPath = confPath = os.path.expanduser( "~/ndr651_txrx_gui.conf" )
        self.radioObj = radioObj = crd.getRadioObject("ndr651", verbose=False)
        self._nbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcRateIndexCfg_config.read(confPath)
        try: nbddcRateIndexCfg = self._nbddcRateIndexCfg_config.getint('nbddc', 'rate_index')
        except: nbddcRateIndexCfg = 0
        self.nbddcRateIndexCfg = nbddcRateIndexCfg
        self._ducRateIndexCfg_config = ConfigParser.ConfigParser()
        self._ducRateIndexCfg_config.read(confPath)
        try: ducRateIndexCfg = self._ducRateIndexCfg_config.getint('duc', 'rate_index')
        except: ducRateIndexCfg = 1
        self.ducRateIndexCfg = ducRateIndexCfg
        self._cwFreq1Cfg_config = ConfigParser.ConfigParser()
        self._cwFreq1Cfg_config.read(confPath)
        try: cwFreq1Cfg = self._cwFreq1Cfg_config.getfloat('cw', 'freq')
        except: cwFreq1Cfg = 1.25
        self.cwFreq1Cfg = cwFreq1Cfg
        self.rxFreqOffset = rxFreqOffset = 0
        self.nbddcRateSet = nbddcRateSet = radioObj.getNbddcRateSet()
        self.nbddcRateIndex = nbddcRateIndex = nbddcRateIndexCfg
        self.ducTxinvMode = ducTxinvMode = 0
        self.ducRateSet = ducRateSet = radioObj.getWbducRateSet()
        self.ducRateIndex = ducRateIndex = ducRateIndexCfg
        self.ducFreq = ducFreq = 0
        self.cwFreq1 = cwFreq1 = cwFreq1Cfg
        self._txFreqCfg_config = ConfigParser.ConfigParser()
        self._txFreqCfg_config.read(confPath)
        try: txFreqCfg = self._txFreqCfg_config.getfloat('tx', 'freq')
        except: txFreqCfg = 1000
        self.txFreqCfg = txFreqCfg
        self.nbddcFreq_autoCalc = nbddcFreq_autoCalc = numpy.round( (ducFreq-rxFreqOffset)*1e6+(((-1)**(2-ducTxinvMode))*cwFreq1/100.0*ducRateSet[ducRateIndex]) - nbddcRateSet[nbddcRateIndex]/16 )
        self.nbddcFreqSlider = nbddcFreqSlider = 0
        self.autoNbddcFreq = autoNbddcFreq = True
        self._wbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcRateIndexCfg_config.read(confPath)
        try: wbddcRateIndexCfg = self._wbddcRateIndexCfg_config.getint('wbddc', 'rate_index')
        except: wbddcRateIndexCfg = 0
        self.wbddcRateIndexCfg = wbddcRateIndexCfg
        self._wbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcIndexCfg_config.read(confPath)
        try: wbddcIndexCfg = self._wbddcIndexCfg_config.getint('wbddc', 'index')
        except: wbddcIndexCfg = 1
        self.wbddcIndexCfg = wbddcIndexCfg
        self.txFreq = txFreq = txFreqCfg
        self._txAttenCfg_config = ConfigParser.ConfigParser()
        self._txAttenCfg_config.read(confPath)
        try: txAttenCfg = self._txAttenCfg_config.getint('tx', 'atten')
        except: txAttenCfg = 0
        self.txAttenCfg = txAttenCfg
        self._rxAttenCfg_config = ConfigParser.ConfigParser()
        self._rxAttenCfg_config.read(confPath)
        try: rxAttenCfg = self._rxAttenCfg_config.getint('rx', 'atten')
        except: rxAttenCfg = 0
        self.rxAttenCfg = rxAttenCfg
        self._nbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcIndexCfg_config.read(confPath)
        try: nbddcIndexCfg = self._nbddcIndexCfg_config.getint('nbddc', 'index')
        except: nbddcIndexCfg = 1
        self.nbddcIndexCfg = nbddcIndexCfg
        self.nbddcFreq = nbddcFreq = nbddcFreq_autoCalc if ( autoNbddcFreq and (numpy.abs(nbddcFreq_autoCalc)<=25.6e6) )else nbddcFreqSlider*1e6
        self.duchsPfThresh = duchsPfThresh = 25
        self._ducAttenCfg_config = ConfigParser.ConfigParser()
        self._ducAttenCfg_config.read(confPath)
        try: ducAttenCfg = self._ducAttenCfg_config.getfloat('duc', 'atten')
        except: ducAttenCfg = 0
        self.ducAttenCfg = ducAttenCfg
        self._cwFreq2Cfg_config = ConfigParser.ConfigParser()
        self._cwFreq2Cfg_config.read(confPath)
        try: cwFreq2Cfg = self._cwFreq2Cfg_config.getfloat('cw', 'freq2')
        except: cwFreq2Cfg = -1.25
        self.cwFreq2Cfg = cwFreq2Cfg
        self._cwAmp2Cfg_config = ConfigParser.ConfigParser()
        self._cwAmp2Cfg_config.read(confPath)
        try: cwAmp2Cfg = self._cwAmp2Cfg_config.getfloat('cw', 'amp2')
        except: cwAmp2Cfg = -1.0
        self.cwAmp2Cfg = cwAmp2Cfg
        self._cwAmp1Cfg_config = ConfigParser.ConfigParser()
        self._cwAmp1Cfg_config.read(confPath)
        try: cwAmp1Cfg = self._cwAmp1Cfg_config.getfloat('cw', 'amp1')
        except: cwAmp1Cfg = -1.0
        self.cwAmp1Cfg = cwAmp1Cfg
        self.wbddcRateSet = wbddcRateSet = radioObj.getWbddcRateSet()
        self.wbddcRateIndex = wbddcRateIndex = wbddcRateIndexCfg
        self.wbddcIndex = wbddcIndex = wbddcIndexCfg
        self.updatePE = updatePE = False
        self.udpPort = udpPort = 33222
        self.txsumChoice = txsumChoice = 0
        self.txAtten = txAtten = txAttenCfg
        self._rxFreqCfg_config = ConfigParser.ConfigParser()
        self._rxFreqCfg_config.read(confPath)
        try: rxFreqCfg = self._rxFreqCfg_config.getint('rx', 'freq_offset')
        except: rxFreqCfg = 1000
        self.rxFreqCfg = rxFreqCfg
        self.rxFreq = rxFreq = (txFreq+rxFreqOffset) if ((txFreq+rxFreqOffset)>=20) else 20
        self.rxAtten = rxAtten = rxAttenCfg
        self.radioParam = radioParam = {"type":"ndr651", "host":hostname, "port":8617, "obj":radioObj}
        self.nbddcIndex = nbddcIndex = nbddcIndexCfg
        self.nbddcFreqLabel = nbddcFreqLabel = num_to_str(nbddcFreq)+"Hz"
        self.iface2 = iface2 = localInterface2 if dataPort2==2 else localInterface1
        self.iface1 = iface1 = localInterface2 if dataPort1==2 else localInterface1
        self.duchsPeriodList = duchsPeriodList = [0.2,0.5,1,2,5,10,20,50,100,200]
        self.duchsPeriodHz = duchsPeriodHz = 20
        self.duchsPeThresh = duchsPeThresh = duchsPfThresh-1
        self.ducIndexLabel = ducIndexLabel = ducIndex
        self.ducAtten = ducAtten = ducAttenCfg
        self.cwFreq2 = cwFreq2 = cwFreq2Cfg
        self.cwAmp2 = cwAmp2 = cwAmp2Cfg
        self.cwAmp1 = cwAmp1 = cwAmp1Cfg

        ##################################################
        # Blocks
        ##################################################
        self.controlTabs = Qt.QTabWidget()
        self.controlTabs_widget_0 = Qt.QWidget()
        self.controlTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controlTabs_widget_0)
        self.controlTabs_grid_layout_0 = Qt.QGridLayout()
        self.controlTabs_layout_0.addLayout(self.controlTabs_grid_layout_0)
        self.controlTabs.addTab(self.controlTabs_widget_0, 'DDC/DUC Settings')
        self.controlTabs_widget_1 = Qt.QWidget()
        self.controlTabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controlTabs_widget_1)
        self.controlTabs_grid_layout_1 = Qt.QGridLayout()
        self.controlTabs_layout_1.addLayout(self.controlTabs_grid_layout_1)
        self.controlTabs.addTab(self.controlTabs_widget_1, 'Flow Control')
        self.controlTabs_widget_2 = Qt.QWidget()
        self.controlTabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controlTabs_widget_2)
        self.controlTabs_grid_layout_2 = Qt.QGridLayout()
        self.controlTabs_layout_2.addLayout(self.controlTabs_grid_layout_2)
        self.controlTabs.addTab(self.controlTabs_widget_2, 'Sig Gen and TXSUM')
        self.top_grid_layout.addWidget(self.controlTabs, 1,0,1,1)
        self.topTabs = Qt.QTabWidget()
        self.topTabs_widget_0 = Qt.QWidget()
        self.topTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.topTabs_widget_0)
        self.topTabs_grid_layout_0 = Qt.QGridLayout()
        self.topTabs_layout_0.addLayout(self.topTabs_grid_layout_0)
        self.topTabs.addTab(self.topTabs_widget_0, 'WBDDC')
        self.top_grid_layout.addWidget(self.topTabs, 0,0,1,2)
        self._duchsPfThresh_range = Range(0, 25, 1, 25, 200)
        self._duchsPfThresh_win = RangeWidget(self._duchsPfThresh_range, self.set_duchsPfThresh, 'DUCHS PF Threshold', "counter_slider", int)
        self.controlTabs_grid_layout_1.addWidget(self._duchsPfThresh_win, 1,0,1,1)
        self._wbddcRateIndex_options = [-1]+sorted(wbddcRateSet.keys())
        self._wbddcRateIndex_labels = ["Disabled",]+["%d: %ssps"%(i,num_to_str(wbddcRateSet[i])) for i in sorted(wbddcRateSet.keys())]
        self._wbddcRateIndex_tool_bar = Qt.QToolBar(self)
        self._wbddcRateIndex_tool_bar.addWidget(Qt.QLabel('WBDDC Rate'+": "))
        self._wbddcRateIndex_combo_box = Qt.QComboBox()
        self._wbddcRateIndex_tool_bar.addWidget(self._wbddcRateIndex_combo_box)
        for label in self._wbddcRateIndex_labels: self._wbddcRateIndex_combo_box.addItem(label)
        self._wbddcRateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._wbddcRateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._wbddcRateIndex_options.index(i)))
        self._wbddcRateIndex_callback(self.wbddcRateIndex)
        self._wbddcRateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_wbddcRateIndex(self._wbddcRateIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._wbddcRateIndex_tool_bar, 0,1,1,1)
        self._wbddcIndex_options = radioObj.getWbddcIndexRange()
        self._wbddcIndex_labels = map(str, self._wbddcIndex_options)
        self._wbddcIndex_tool_bar = Qt.QToolBar(self)
        self._wbddcIndex_tool_bar.addWidget(Qt.QLabel('NB Tuner Source'+": "))
        self._wbddcIndex_combo_box = Qt.QComboBox()
        self._wbddcIndex_tool_bar.addWidget(self._wbddcIndex_combo_box)
        for label in self._wbddcIndex_labels: self._wbddcIndex_combo_box.addItem(label)
        self._wbddcIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._wbddcIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._wbddcIndex_options.index(i)))
        self._wbddcIndex_callback(self.wbddcIndex)
        self._wbddcIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_wbddcIndex(self._wbddcIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._wbddcIndex_tool_bar, 0,0,1,1)
        self._updatePE_options = [False, True]
        self._updatePE_labels = ["Periodic", "Empty Flag"]
        self._updatePE_group_box = Qt.QGroupBox('Flow Control Update')
        self._updatePE_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._updatePE_button_group = variable_chooser_button_group()
        self._updatePE_group_box.setLayout(self._updatePE_box)
        for i, label in enumerate(self._updatePE_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._updatePE_box.addWidget(radio_button)
        	self._updatePE_button_group.addButton(radio_button, i)
        self._updatePE_callback = lambda i: Qt.QMetaObject.invokeMethod(self._updatePE_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._updatePE_options.index(i)))
        self._updatePE_callback(self.updatePE)
        self._updatePE_button_group.buttonClicked[int].connect(
        	lambda i: self.set_updatePE(self._updatePE_options[i]))
        self.controlTabs_grid_layout_1.addWidget(self._updatePE_group_box, 0,0,1,1)
        self._txsumChoice_options = range(11)
        self._txsumChoice_labels = ["0:  1 / 2 / -","1: 1+E/ 2 / -","2: 1 / 2+E / -","3: - /1+2/ -","4: - / 1+2+E / -","5: - / 2 / 1","6: - / 2 /1+E","7: 1 / - / 2","8: 1 / - /2+E","9:  - / - /ALL","10: 1 / 2 / E"]
        self._txsumChoice_tool_bar = Qt.QToolBar(self)
        self._txsumChoice_tool_bar.addWidget(Qt.QLabel('Tx Output Sum'+": "))
        self._txsumChoice_combo_box = Qt.QComboBox()
        self._txsumChoice_tool_bar.addWidget(self._txsumChoice_combo_box)
        for label in self._txsumChoice_labels: self._txsumChoice_combo_box.addItem(label)
        self._txsumChoice_callback = lambda i: Qt.QMetaObject.invokeMethod(self._txsumChoice_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._txsumChoice_options.index(i)))
        self._txsumChoice_callback(self.txsumChoice)
        self._txsumChoice_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_txsumChoice(self._txsumChoice_options[i]))
        self.controlTabs_layout_2.addWidget(self._txsumChoice_tool_bar)
        self._txFreq_range = Range(2, 6000, 40, txFreqCfg, 200)
        self._txFreq_win = RangeWidget(self._txFreq_range, self.set_txFreq, 'TX Freq (MHz)', "counter_slider", float)
        self.topTabs_grid_layout_0.addWidget(self._txFreq_win, 1,0,1,1)
        self._txAtten_range = Range(0, 15, 1, txAttenCfg, 16)
        self._txAtten_win = RangeWidget(self._txAtten_range, self.set_txAtten, 'TX Atten', "counter_slider", int)
        self.topTabs_grid_layout_0.addWidget(self._txAtten_win, 1,2,1,1)
        self._rxFreqOffset_range = Range(-500, +500, 5, 0, int((1000/10)+1))
        self._rxFreqOffset_win = RangeWidget(self._rxFreqOffset_range, self.set_rxFreqOffset, 'RX Offset (MHz)', "counter_slider", int)
        self.topTabs_grid_layout_0.addWidget(self._rxFreqOffset_win, 1,1,1,1)
        self._rxAtten_range = Range(0, 30, 1, rxAttenCfg, 31)
        self._rxAtten_win = RangeWidget(self._rxAtten_range, self.set_rxAtten, 'RX Atten', "counter_slider", int)
        self.topTabs_grid_layout_0.addWidget(self._rxAtten_win, 1,3,1,1)
        self.plotTabs = Qt.QTabWidget()
        self.plotTabs_widget_0 = Qt.QWidget()
        self.plotTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plotTabs_widget_0)
        self.plotTabs_grid_layout_0 = Qt.QGridLayout()
        self.plotTabs_layout_0.addLayout(self.plotTabs_grid_layout_0)
        self.plotTabs.addTab(self.plotTabs_widget_0, 'Narrowband Rx')
        self.plotTabs_widget_1 = Qt.QWidget()
        self.plotTabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plotTabs_widget_1)
        self.plotTabs_grid_layout_1 = Qt.QGridLayout()
        self.plotTabs_layout_1.addLayout(self.plotTabs_grid_layout_1)
        self.plotTabs.addTab(self.plotTabs_widget_1, 'Tx Signal')
        self.top_grid_layout.addWidget(self.plotTabs, 1,1,1,1)
        self._nbddcRateIndex_options = [-1]+sorted(nbddcRateSet.keys())
        self._nbddcRateIndex_labels = ["Disabled",]+["%d: %ssps"%(i,num_to_str(nbddcRateSet[i])) for i in sorted(nbddcRateSet.keys())]
        self._nbddcRateIndex_tool_bar = Qt.QToolBar(self)
        self._nbddcRateIndex_tool_bar.addWidget(Qt.QLabel('NBDDC Rate'+": "))
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
        self._nbddcIndex_tool_bar.addWidget(Qt.QLabel('NBDDC'+": "))
        self._nbddcIndex_combo_box = Qt.QComboBox()
        self._nbddcIndex_tool_bar.addWidget(self._nbddcIndex_combo_box)
        for label in self._nbddcIndex_labels: self._nbddcIndex_combo_box.addItem(label)
        self._nbddcIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._nbddcIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._nbddcIndex_options.index(i)))
        self._nbddcIndex_callback(self.nbddcIndex)
        self._nbddcIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_nbddcIndex(self._nbddcIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._nbddcIndex_tool_bar, 1,0,1,1)
        self._duchsPeThresh_range = Range(0, 25, 1, duchsPfThresh-1, 200)
        self._duchsPeThresh_win = RangeWidget(self._duchsPeThresh_range, self.set_duchsPeThresh, 'DUCHS PE Threshold', "counter_slider", int)
        self.controlTabs_grid_layout_1.addWidget(self._duchsPeThresh_win, 1,1,1,1)
        _ducTxinvMode_check_box = Qt.QCheckBox('DUC Tx Spectral Inversion')
        self._ducTxinvMode_choices = {True: 1, False: 0}
        self._ducTxinvMode_choices_inv = dict((v,k) for k,v in self._ducTxinvMode_choices.iteritems())
        self._ducTxinvMode_callback = lambda i: Qt.QMetaObject.invokeMethod(_ducTxinvMode_check_box, "setChecked", Qt.Q_ARG("bool", self._ducTxinvMode_choices_inv[i]))
        self._ducTxinvMode_callback(self.ducTxinvMode)
        _ducTxinvMode_check_box.stateChanged.connect(lambda i: self.set_ducTxinvMode(self._ducTxinvMode_choices[bool(i)]))
        self.controlTabs_grid_layout_0.addWidget(_ducTxinvMode_check_box, 4,1,1,1)
        self._ducRateIndex_options = sorted(ducRateSet.keys())
        self._ducRateIndex_labels = ["%d: %ssps"%(i,num_to_str(ducRateSet[i])) for i in sorted(ducRateSet.keys())]
        self._ducRateIndex_tool_bar = Qt.QToolBar(self)
        self._ducRateIndex_tool_bar.addWidget(Qt.QLabel('DUC Rate'+": "))
        self._ducRateIndex_combo_box = Qt.QComboBox()
        self._ducRateIndex_tool_bar.addWidget(self._ducRateIndex_combo_box)
        for label in self._ducRateIndex_labels: self._ducRateIndex_combo_box.addItem(label)
        self._ducRateIndex_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ducRateIndex_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ducRateIndex_options.index(i)))
        self._ducRateIndex_callback(self.ducRateIndex)
        self._ducRateIndex_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_ducRateIndex(self._ducRateIndex_options[i]))
        self.controlTabs_grid_layout_0.addWidget(self._ducRateIndex_tool_bar, 2,1,1,1)
        self._ducFreq_range = Range(-25.5, +25.5, 0.5, 0, 4001)
        self._ducFreq_win = RangeWidget(self._ducFreq_range, self.set_ducFreq, 'DUC Freq (MHz)', "counter_slider", float)
        self.controlTabs_grid_layout_0.addWidget(self._ducFreq_win, 3,0,1,2)
        self._ducAtten_range = Range(-20, 60, 1.0, ducAttenCfg, int(60/0.25)+1)
        self._ducAtten_win = RangeWidget(self._ducAtten_range, self.set_ducAtten, 'DUC Attenuation', "counter_slider", float)
        self.controlTabs_grid_layout_0.addWidget(self._ducAtten_win, 4,0,1,1)
        self._cwFreq2_range = Range(-40.0, +40.0, 1.25, cwFreq2Cfg, int((80.0/2.5)+1))
        self._cwFreq2_win = RangeWidget(self._cwFreq2_range, self.set_cwFreq2, 'GR CW Freq 2 (% BW)', "counter_slider", float)
        self.controlTabs_grid_layout_2.addWidget(self._cwFreq2_win, 2,0,1,1)
        self._cwFreq1_range = Range(-40.0, +40.0, 1.25, cwFreq1Cfg, int((80.0/2.5)+1))
        self._cwFreq1_win = RangeWidget(self._cwFreq1_range, self.set_cwFreq1, 'GR CW Freq 1 (% BW)', "counter_slider", float)
        self.controlTabs_grid_layout_2.addWidget(self._cwFreq1_win, 0,0,1,1)
        self._cwAmp2_range = Range(-90.0, +10.0, 1.0, cwAmp2Cfg, 101)
        self._cwAmp2_win = RangeWidget(self._cwAmp2_range, self.set_cwAmp2, 'GR CW Amp 2 (dB)', "counter_slider", float)
        self.controlTabs_grid_layout_2.addWidget(self._cwAmp2_win, 3,0,1,1)
        self._cwAmp1_range = Range(-90, +10, 1, cwAmp1Cfg, 101)
        self._cwAmp1_win = RangeWidget(self._cwAmp1_range, self.set_cwAmp1, 'GR CW Amp 1 (dB)', "counter_slider", float)
        self.controlTabs_grid_layout_2.addWidget(self._cwAmp1_win, 1,0,1,1)
        self.z_tunerControl_0 = CyberRadio.generic_tuner_control_block(
                    radioParam,
                    2,
                    True,
                    rxFreq,
                    rxAtten,
                    1,
                    {},
                    False
                     )
        self.z_tunerControl = CyberRadio.generic_tuner_control_block(
                    radioParam,
                    1,
                    True,
                    rxFreq,
                    rxAtten,
                    1,
                    {},
                    False
                     )
        self.z_ddcControl_wb_0 = CyberRadio.generic_ddc_control_block(
                    radioParam,
                    2,
                    wbddcRateIndex in wbddcRateSet,
                    True,
                    wbddcRateIndex if wbddcRateIndex in wbddcRateSet else 0,
                    0,
                    0.0,
                    wbddcIndex,
                    0,
                    dataPort2,
                    -1,
                    "",
                    udpPort+2,
                    {},
                    False
                     )
        self.z_ddcControl_wb = CyberRadio.generic_ddc_control_block(
                    radioParam,
                    1,
                    wbddcRateIndex in wbddcRateSet,
                    True,
                    wbddcRateIndex if wbddcRateIndex in wbddcRateSet else 0,
                    0,
                    0.0,
                    wbddcIndex,
                    0,
                    dataPort1,
                    -1,
                    "",
                    udpPort,
                    {},
                    False
                     )
        self.z_ddcControl_nb = CyberRadio.generic_ddc_control_block(
                    radioParam,
                    nbddcIndex,
                    nbddcRateIndex in nbddcRateSet,
                    False,
                    nbddcRateIndex if nbddcRateIndex in nbddcRateSet else 0,
                    0,
                    nbddcFreq,
                    wbddcIndex,
                    0,
                    dataPort1,
                    -1,
                    "",
                    udpPort+1,
                    {},
                    False
                     )
        self.y_vitaIqSource_wb_0 = CyberRadio.vita_iq_source_2(
            3,
            1024*4,
            9*4,
            1*4,
            False,
            True,
            '0.0.0.0',
            udpPort+2,
            False,
            False,
            False,
             )
        self.y_vitaIqSource_wb = CyberRadio.vita_iq_source_2(
            3,
            1024*4,
            9*4,
            1*4,
            False,
            True,
            '0.0.0.0',
            udpPort,
            False,
            False,
            False,
             )
        self.y_vitaIqSource_nb = CyberRadio.vita_iq_source_2(
            3,
            1024*4,
            9*4,
            1*4,
            False,
            True,
            '0.0.0.0',
            udpPort+1,
            False,
            False,
            False,
             )
        self.vecToStream_iq_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1024)
        self.vecToStream_iq_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1024)
        self.vecToStream_iq = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1024)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_HAMMING, #wintype
        	(txFreq)*1e6, #fc
        	ducRateSet[ducRateIndex], #bw
        	'DUC', #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(1.0)
        self.qtgui_freq_sink_x_0_1.set_y_axis(-100, 0)
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(True)
        self.qtgui_freq_sink_x_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_1.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_1.set_plot_pos_half(not True)

        labels = ['Tx 1', 'Tx 2', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "blue", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.plotTabs_layout_1.addWidget(self._qtgui_freq_sink_x_0_1_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rxFreq*1e6, #fc
        	wbddcRateSet[wbddcRateIndex], #bw
        	'Wideband Receivers', #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(1.0/4)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-120, 0)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['Rx 1', 'Rx 2', 'Tx Sig', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "blue", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.topTabs_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_win, 0,0,1,4)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	((txFreq+rxFreqOffset)*1e6)+nbddcFreq, #fc
        	nbddcRateSet[nbddcRateIndex], #bw
        	'NBDDC', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(1.0/8)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 0)
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
        colors = ["dark red", "red", "green", "black", "cyan",
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
        self.plotTabs_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)
        self.nullSink_0_0 = blocks.null_sink(gr.sizeof_int*(9+1024+1))
        self.nullSink_0 = blocks.null_sink(gr.sizeof_int*(9+1024+1))
        self.nullSink = blocks.null_sink(gr.sizeof_int*(9+1024+1))
        self._nbddcFreqSlider_range = Range(-20, +20, 0.1, 0, int((40/0.1)+1))
        self._nbddcFreqSlider_win = RangeWidget(self._nbddcFreqSlider_range, self.set_nbddcFreqSlider, 'Manual (MHz)', "counter_slider", float)
        self.controlTabs_grid_layout_0.addWidget(self._nbddcFreqSlider_win, 6,0,1,2)
        self._nbddcFreqLabel_tool_bar = Qt.QToolBar(self)

        if None:
          self._nbddcFreqLabel_formatter = None
        else:
          self._nbddcFreqLabel_formatter = lambda x: x

        self._nbddcFreqLabel_tool_bar.addWidget(Qt.QLabel('Applied'+": "))
        self._nbddcFreqLabel_label = Qt.QLabel(str(self._nbddcFreqLabel_formatter(self.nbddcFreqLabel)))
        self._nbddcFreqLabel_tool_bar.addWidget(self._nbddcFreqLabel_label)
        self.controlTabs_grid_layout_0.addWidget(self._nbddcFreqLabel_tool_bar, 5,1,1,1)

        self._duchsPeriodHz_options = duchsPeriodList
        self._duchsPeriodHz_labels = ["%0.1fHz, Period=%d*5ms"%(i, 1.0/float(i)/5e-3) for i in duchsPeriodList]
        self._duchsPeriodHz_tool_bar = Qt.QToolBar(self)
        self._duchsPeriodHz_tool_bar.addWidget(Qt.QLabel('DDC Period (Hz)'+": "))
        self._duchsPeriodHz_combo_box = Qt.QComboBox()
        self._duchsPeriodHz_tool_bar.addWidget(self._duchsPeriodHz_combo_box)
        for label in self._duchsPeriodHz_labels: self._duchsPeriodHz_combo_box.addItem(label)
        self._duchsPeriodHz_callback = lambda i: Qt.QMetaObject.invokeMethod(self._duchsPeriodHz_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._duchsPeriodHz_options.index(i)))
        self._duchsPeriodHz_callback(self.duchsPeriodHz)
        self._duchsPeriodHz_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_duchsPeriodHz(self._duchsPeriodHz_options[i]))
        self.controlTabs_grid_layout_1.addWidget(self._duchsPeriodHz_tool_bar, 0,1,1,1)
        self._ducIndexLabel_tool_bar = Qt.QToolBar(self)

        if None:
          self._ducIndexLabel_formatter = None
        else:
          self._ducIndexLabel_formatter = lambda x: x

        self._ducIndexLabel_tool_bar.addWidget(Qt.QLabel('DUC Index'+": "))
        self._ducIndexLabel_label = Qt.QLabel(str(self._ducIndexLabel_formatter(self.ducIndexLabel)))
        self._ducIndexLabel_tool_bar.addWidget(self._ducIndexLabel_label)
        self.controlTabs_grid_layout_0.addWidget(self._ducIndexLabel_tool_bar, 2,0,1,1)

        self.blocks_rotator_cc_0_0 = blocks.rotator_cc(float(cwFreq2)*numpy.pi/50)
        self.blocks_rotator_cc_0 = blocks.rotator_cc(float(cwFreq1)*numpy.pi/50)
        _autoNbddcFreq_check_box = Qt.QCheckBox('Auto NBDDC Freq?')
        self._autoNbddcFreq_choices = {True: True, False: False}
        self._autoNbddcFreq_choices_inv = dict((v,k) for k,v in self._autoNbddcFreq_choices.iteritems())
        self._autoNbddcFreq_callback = lambda i: Qt.QMetaObject.invokeMethod(_autoNbddcFreq_check_box, "setChecked", Qt.Q_ARG("bool", self._autoNbddcFreq_choices_inv[i]))
        self._autoNbddcFreq_callback(self.autoNbddcFreq)
        _autoNbddcFreq_check_box.stateChanged.connect(lambda i: self.set_autoNbddcFreq(self._autoNbddcFreq_choices[bool(i)]))
        self.controlTabs_grid_layout_0.addWidget(_autoNbddcFreq_check_box, 5,0,1,1)
        self.analog_const_source_x_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 10.0**(float(cwAmp2)/20))
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 10.0**(float(cwAmp1)/20))
        self.aaaa_command_block = CyberRadio.generic_ndr_command_block(
                    radioParam,
                    "TXSUM %d"%(txsumChoice),
                    False,
                     )
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1 = CyberRadio.NDR651_duc_sink_mk2(
            radio_host_name = hostname,
            radio_tcp_port = 8617,
            tengig_iface_index = dataPort2,
            iq_scale_factor = 2**15-1,
            duc_channel = (ducIndex%8)+1,
            duc_iface_string = iface2,
            duc_rate_index = ducRateIndex,
            duc_frequency = int( ducFreq*1e6 ),
            duc_attenuation = ducAtten,
            duc_tx_channels = 2,
            duc_tx_frequency = txFreq,
            duc_tx_attenuation = txAtten,
            duc_stream_id = 57005+1,
            config_tx = True,
            debug = True,
            duchsPfThresh = 25,
            duchsPeThresh = 24,
            duchsPeriod = 10,
            updatePE = False,
            txinv_mode = ducTxinvMode,
        )
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0 = CyberRadio.NDR651_duc_sink_mk2(
            radio_host_name = hostname,
            radio_tcp_port = 8617,
            tengig_iface_index = dataPort1,
            iq_scale_factor = 2**15-1,
            duc_channel = ((ducIndex-1)%8)+1,
            duc_iface_string = iface1,
            duc_rate_index = ducRateIndex,
            duc_frequency = int( ducFreq*1e6 ),
            duc_attenuation = ducAtten,
            duc_tx_channels = 1,
            duc_tx_frequency = txFreq,
            duc_tx_attenuation = txAtten,
            duc_stream_id = 57005,
            config_tx = True,
            debug = True,
            duchsPfThresh = 25,
            duchsPeThresh = 24,
            duchsPeriod = 10,
            updatePE = False,
            txinv_mode = ducTxinvMode,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_rotator_cc_0_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.AAA_CyberRadio_NDR651_duc_sink_mk2_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.qtgui_freq_sink_x_0_1, 0))
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.AAA_CyberRadio_NDR651_duc_sink_mk2_1, 0))
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.qtgui_freq_sink_x_0_1, 1))
        self.connect((self.vecToStream_iq, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.vecToStream_iq_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.vecToStream_iq_0_0, 0), (self.qtgui_freq_sink_x_0_0, 1))
        self.connect((self.y_vitaIqSource_nb, 0), (self.nullSink, 0))
        self.connect((self.y_vitaIqSource_nb, 1), (self.vecToStream_iq, 0))
        self.connect((self.y_vitaIqSource_wb, 0), (self.nullSink_0, 0))
        self.connect((self.y_vitaIqSource_wb, 1), (self.vecToStream_iq_0, 0))
        self.connect((self.y_vitaIqSource_wb_0, 0), (self.nullSink_0_0, 0))
        self.connect((self.y_vitaIqSource_wb_0, 1), (self.vecToStream_iq_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ndr651_txrx_gui")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_dataPort1(self):
        return self.dataPort1

    def set_dataPort1(self, dataPort1):
        self.dataPort1 = dataPort1
        self.set_iface1(self.localInterface2 if self.dataPort1==2 else self.localInterface1)
        self.z_ddcControl_wb.set_radioInterface(self.dataPort1)
        self.z_ddcControl_nb.set_radioInterface(self.dataPort1)

    def get_dataPort2(self):
        return self.dataPort2

    def set_dataPort2(self, dataPort2):
        self.dataPort2 = dataPort2
        self.set_iface2(self.localInterface2 if self.dataPort2==2 else self.localInterface1)
        self.z_ddcControl_wb_0.set_radioInterface(self.dataPort2)

    def get_dipIndex(self):
        return self.dipIndex

    def set_dipIndex(self, dipIndex):
        self.dipIndex = dipIndex

    def get_ducIndex(self):
        return self.ducIndex

    def set_ducIndex(self, ducIndex):
        self.ducIndex = ducIndex
        self.set_ducIndexLabel(self._ducIndexLabel_formatter(self.ducIndex))
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_channel((self.ducIndex%8)+1)
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_channel(((self.ducIndex-1)%8)+1)

    def get_fftRate(self):
        return self.fftRate

    def set_fftRate(self, fftRate):
        self.fftRate = fftRate

    def get_fftSizeExp(self):
        return self.fftSizeExp

    def set_fftSizeExp(self, fftSizeExp):
        self.fftSizeExp = fftSizeExp

    def get_hostname(self):
        return self.hostname

    def set_hostname(self, hostname):
        self.hostname = hostname
        self.set_radioParam({"type":"ndr651", "host":self.hostname, "port":8617, "obj":self.radioObj})

    def get_localInterface1(self):
        return self.localInterface1

    def set_localInterface1(self, localInterface1):
        self.localInterface1 = localInterface1
        self.set_iface2(self.localInterface2 if self.dataPort2==2 else self.localInterface1)
        self.set_iface1(self.localInterface2 if self.dataPort1==2 else self.localInterface1)

    def get_localInterface2(self):
        return self.localInterface2

    def set_localInterface2(self, localInterface2):
        self.localInterface2 = localInterface2
        self.set_iface2(self.localInterface2 if self.dataPort2==2 else self.localInterface1)
        self.set_iface1(self.localInterface2 if self.dataPort1==2 else self.localInterface1)

    def get_confPath(self):
        return self.confPath

    def set_confPath(self, confPath):
        self.confPath = confPath
        self._wbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcRateIndexCfg_config.read(self.confPath)
        if not self._wbddcRateIndexCfg_config.has_section('wbddc'):
        	self._wbddcRateIndexCfg_config.add_section('wbddc')
        self._wbddcRateIndexCfg_config.set('wbddc', 'rate_index', str(self.wbddcRateIndex))
        self._wbddcRateIndexCfg_config.write(open(self.confPath, 'w'))
        self._wbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcIndexCfg_config.read(self.confPath)
        if not self._wbddcIndexCfg_config.has_section('wbddc'):
        	self._wbddcIndexCfg_config.add_section('wbddc')
        self._wbddcIndexCfg_config.set('wbddc', 'index', str(self.wbddcIndex))
        self._wbddcIndexCfg_config.write(open(self.confPath, 'w'))
        self._txFreqCfg_config = ConfigParser.ConfigParser()
        self._txFreqCfg_config.read(self.confPath)
        if not self._txFreqCfg_config.has_section('tx'):
        	self._txFreqCfg_config.add_section('tx')
        self._txFreqCfg_config.set('tx', 'freq', str(self.txFreq))
        self._txFreqCfg_config.write(open(self.confPath, 'w'))
        self._txAttenCfg_config = ConfigParser.ConfigParser()
        self._txAttenCfg_config.read(self.confPath)
        if not self._txAttenCfg_config.has_section('tx'):
        	self._txAttenCfg_config.add_section('tx')
        self._txAttenCfg_config.set('tx', 'atten', str(self.txAtten))
        self._txAttenCfg_config.write(open(self.confPath, 'w'))
        self._rxFreqCfg_config = ConfigParser.ConfigParser()
        self._rxFreqCfg_config.read(self.confPath)
        if not self._rxFreqCfg_config.has_section('rx'):
        	self._rxFreqCfg_config.add_section('rx')
        self._rxFreqCfg_config.set('rx', 'freq_offset', str(self.rxFreqOffset))
        self._rxFreqCfg_config.write(open(self.confPath, 'w'))
        self._rxAttenCfg_config = ConfigParser.ConfigParser()
        self._rxAttenCfg_config.read(self.confPath)
        if not self._rxAttenCfg_config.has_section('rx'):
        	self._rxAttenCfg_config.add_section('rx')
        self._rxAttenCfg_config.set('rx', 'atten', str(self.rxAtten))
        self._rxAttenCfg_config.write(open(self.confPath, 'w'))
        self._nbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcRateIndexCfg_config.read(self.confPath)
        if not self._nbddcRateIndexCfg_config.has_section('nbddc'):
        	self._nbddcRateIndexCfg_config.add_section('nbddc')
        self._nbddcRateIndexCfg_config.set('nbddc', 'rate_index', str(self.nbddcRateIndex))
        self._nbddcRateIndexCfg_config.write(open(self.confPath, 'w'))
        self._nbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcIndexCfg_config.read(self.confPath)
        if not self._nbddcIndexCfg_config.has_section('nbddc'):
        	self._nbddcIndexCfg_config.add_section('nbddc')
        self._nbddcIndexCfg_config.set('nbddc', 'index', str(self.nbddcIndex))
        self._nbddcIndexCfg_config.write(open(self.confPath, 'w'))
        self._ducRateIndexCfg_config = ConfigParser.ConfigParser()
        self._ducRateIndexCfg_config.read(self.confPath)
        if not self._ducRateIndexCfg_config.has_section('duc'):
        	self._ducRateIndexCfg_config.add_section('duc')
        self._ducRateIndexCfg_config.set('duc', 'rate_index', str(self.ducRateIndex))
        self._ducRateIndexCfg_config.write(open(self.confPath, 'w'))
        self._ducAttenCfg_config = ConfigParser.ConfigParser()
        self._ducAttenCfg_config.read(self.confPath)
        if not self._ducAttenCfg_config.has_section('duc'):
        	self._ducAttenCfg_config.add_section('duc')
        self._ducAttenCfg_config.set('duc', 'atten', str(self.ducAtten))
        self._ducAttenCfg_config.write(open(self.confPath, 'w'))
        self._cwFreq2Cfg_config = ConfigParser.ConfigParser()
        self._cwFreq2Cfg_config.read(self.confPath)
        if not self._cwFreq2Cfg_config.has_section('cw'):
        	self._cwFreq2Cfg_config.add_section('cw')
        self._cwFreq2Cfg_config.set('cw', 'freq2', str(self.cwFreq2))
        self._cwFreq2Cfg_config.write(open(self.confPath, 'w'))
        self._cwFreq1Cfg_config = ConfigParser.ConfigParser()
        self._cwFreq1Cfg_config.read(self.confPath)
        if not self._cwFreq1Cfg_config.has_section('cw'):
        	self._cwFreq1Cfg_config.add_section('cw')
        self._cwFreq1Cfg_config.set('cw', 'freq', str(self.cwFreq1))
        self._cwFreq1Cfg_config.write(open(self.confPath, 'w'))
        self._cwAmp2Cfg_config = ConfigParser.ConfigParser()
        self._cwAmp2Cfg_config.read(self.confPath)
        if not self._cwAmp2Cfg_config.has_section('cw'):
        	self._cwAmp2Cfg_config.add_section('cw')
        self._cwAmp2Cfg_config.set('cw', 'amp2', str(self.cwAmp2))
        self._cwAmp2Cfg_config.write(open(self.confPath, 'w'))
        self._cwAmp1Cfg_config = ConfigParser.ConfigParser()
        self._cwAmp1Cfg_config.read(self.confPath)
        if not self._cwAmp1Cfg_config.has_section('cw'):
        	self._cwAmp1Cfg_config.add_section('cw')
        self._cwAmp1Cfg_config.set('cw', 'amp1', str(self.cwAmp1))
        self._cwAmp1Cfg_config.write(open(self.confPath, 'w'))

    def get_radioObj(self):
        return self.radioObj

    def set_radioObj(self, radioObj):
        self.radioObj = radioObj
        self.set_radioParam({"type":"ndr651", "host":self.hostname, "port":8617, "obj":self.radioObj})

    def get_nbddcRateIndexCfg(self):
        return self.nbddcRateIndexCfg

    def set_nbddcRateIndexCfg(self, nbddcRateIndexCfg):
        self.nbddcRateIndexCfg = nbddcRateIndexCfg
        self.set_nbddcRateIndex(self.nbddcRateIndexCfg)

    def get_ducRateIndexCfg(self):
        return self.ducRateIndexCfg

    def set_ducRateIndexCfg(self, ducRateIndexCfg):
        self.ducRateIndexCfg = ducRateIndexCfg
        self.set_ducRateIndex(self.ducRateIndexCfg)

    def get_cwFreq1Cfg(self):
        return self.cwFreq1Cfg

    def set_cwFreq1Cfg(self, cwFreq1Cfg):
        self.cwFreq1Cfg = cwFreq1Cfg
        self.set_cwFreq1(self.cwFreq1Cfg)

    def get_rxFreqOffset(self):
        return self.rxFreqOffset

    def set_rxFreqOffset(self, rxFreqOffset):
        self.rxFreqOffset = rxFreqOffset
        self.set_rxFreq((self.txFreq+self.rxFreqOffset) if ((self.txFreq+self.rxFreqOffset)>=20) else 20)
        self._rxFreqCfg_config = ConfigParser.ConfigParser()
        self._rxFreqCfg_config.read(self.confPath)
        if not self._rxFreqCfg_config.has_section('rx'):
        	self._rxFreqCfg_config.add_section('rx')
        self._rxFreqCfg_config.set('rx', 'freq_offset', str(self.rxFreqOffset))
        self._rxFreqCfg_config.write(open(self.confPath, 'w'))
        self.qtgui_freq_sink_x_0.set_frequency_range(((self.txFreq+self.rxFreqOffset)*1e6)+self.nbddcFreq, self.nbddcRateSet[self.nbddcRateIndex])
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))

    def get_nbddcRateSet(self):
        return self.nbddcRateSet

    def set_nbddcRateSet(self, nbddcRateSet):
        self.nbddcRateSet = nbddcRateSet
        self.z_ddcControl_nb.set_enable(self.nbddcRateIndex in self.nbddcRateSet)
        self.z_ddcControl_nb.set_rate(self.nbddcRateIndex if self.nbddcRateIndex in self.nbddcRateSet else 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(((self.txFreq+self.rxFreqOffset)*1e6)+self.nbddcFreq, self.nbddcRateSet[self.nbddcRateIndex])
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))

    def get_nbddcRateIndex(self):
        return self.nbddcRateIndex

    def set_nbddcRateIndex(self, nbddcRateIndex):
        self.nbddcRateIndex = nbddcRateIndex
        self._nbddcRateIndex_callback(self.nbddcRateIndex)
        self.z_ddcControl_nb.set_enable(self.nbddcRateIndex in self.nbddcRateSet)
        self.z_ddcControl_nb.set_rate(self.nbddcRateIndex if self.nbddcRateIndex in self.nbddcRateSet else 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(((self.txFreq+self.rxFreqOffset)*1e6)+self.nbddcFreq, self.nbddcRateSet[self.nbddcRateIndex])
        self._nbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcRateIndexCfg_config.read(self.confPath)
        if not self._nbddcRateIndexCfg_config.has_section('nbddc'):
        	self._nbddcRateIndexCfg_config.add_section('nbddc')
        self._nbddcRateIndexCfg_config.set('nbddc', 'rate_index', str(self.nbddcRateIndex))
        self._nbddcRateIndexCfg_config.write(open(self.confPath, 'w'))
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))

    def get_ducTxinvMode(self):
        return self.ducTxinvMode

    def set_ducTxinvMode(self, ducTxinvMode):
        self.ducTxinvMode = ducTxinvMode
        self._ducTxinvMode_callback(self.ducTxinvMode)
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_txinv_mode(self.ducTxinvMode)
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_txinv_mode(self.ducTxinvMode)

    def get_ducRateSet(self):
        return self.ducRateSet

    def set_ducRateSet(self, ducRateSet):
        self.ducRateSet = ducRateSet
        self.qtgui_freq_sink_x_0_1.set_frequency_range((self.txFreq)*1e6, self.ducRateSet[self.ducRateIndex])
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))

    def get_ducRateIndex(self):
        return self.ducRateIndex

    def set_ducRateIndex(self, ducRateIndex):
        self.ducRateIndex = ducRateIndex
        self._ducRateIndex_callback(self.ducRateIndex)
        self.qtgui_freq_sink_x_0_1.set_frequency_range((self.txFreq)*1e6, self.ducRateSet[self.ducRateIndex])
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))
        self._ducRateIndexCfg_config = ConfigParser.ConfigParser()
        self._ducRateIndexCfg_config.read(self.confPath)
        if not self._ducRateIndexCfg_config.has_section('duc'):
        	self._ducRateIndexCfg_config.add_section('duc')
        self._ducRateIndexCfg_config.set('duc', 'rate_index', str(self.ducRateIndex))
        self._ducRateIndexCfg_config.write(open(self.confPath, 'w'))
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_rate_index(self.ducRateIndex)
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_rate_index(self.ducRateIndex)

    def get_ducFreq(self):
        return self.ducFreq

    def set_ducFreq(self, ducFreq):
        self.ducFreq = ducFreq
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_frequency(int( self.ducFreq*1e6 ))
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_frequency(int( self.ducFreq*1e6 ))

    def get_cwFreq1(self):
        return self.cwFreq1

    def set_cwFreq1(self, cwFreq1):
        self.cwFreq1 = cwFreq1
        self.set_nbddcFreq_autoCalc(numpy.round( (self.ducFreq-self.rxFreqOffset)*1e6+(((-1)**(2-self.ducTxinvMode))*self.cwFreq1/100.0*self.ducRateSet[self.ducRateIndex]) - self.nbddcRateSet[self.nbddcRateIndex]/16 ))
        self._cwFreq1Cfg_config = ConfigParser.ConfigParser()
        self._cwFreq1Cfg_config.read(self.confPath)
        if not self._cwFreq1Cfg_config.has_section('cw'):
        	self._cwFreq1Cfg_config.add_section('cw')
        self._cwFreq1Cfg_config.set('cw', 'freq', str(self.cwFreq1))
        self._cwFreq1Cfg_config.write(open(self.confPath, 'w'))
        self.blocks_rotator_cc_0.set_phase_inc(float(self.cwFreq1)*numpy.pi/50)

    def get_txFreqCfg(self):
        return self.txFreqCfg

    def set_txFreqCfg(self, txFreqCfg):
        self.txFreqCfg = txFreqCfg
        self.set_txFreq(self.txFreqCfg)

    def get_nbddcFreq_autoCalc(self):
        return self.nbddcFreq_autoCalc

    def set_nbddcFreq_autoCalc(self, nbddcFreq_autoCalc):
        self.nbddcFreq_autoCalc = nbddcFreq_autoCalc
        self.set_nbddcFreq(self.nbddcFreq_autoCalc if ( self.autoNbddcFreq and (numpy.abs(self.nbddcFreq_autoCalc)<=25.6e6) )else self.nbddcFreqSlider*1e6)

    def get_nbddcFreqSlider(self):
        return self.nbddcFreqSlider

    def set_nbddcFreqSlider(self, nbddcFreqSlider):
        self.nbddcFreqSlider = nbddcFreqSlider
        self.set_nbddcFreq(self.nbddcFreq_autoCalc if ( self.autoNbddcFreq and (numpy.abs(self.nbddcFreq_autoCalc)<=25.6e6) )else self.nbddcFreqSlider*1e6)

    def get_autoNbddcFreq(self):
        return self.autoNbddcFreq

    def set_autoNbddcFreq(self, autoNbddcFreq):
        self.autoNbddcFreq = autoNbddcFreq
        self.set_nbddcFreq(self.nbddcFreq_autoCalc if ( self.autoNbddcFreq and (numpy.abs(self.nbddcFreq_autoCalc)<=25.6e6) )else self.nbddcFreqSlider*1e6)
        self._autoNbddcFreq_callback(self.autoNbddcFreq)

    def get_wbddcRateIndexCfg(self):
        return self.wbddcRateIndexCfg

    def set_wbddcRateIndexCfg(self, wbddcRateIndexCfg):
        self.wbddcRateIndexCfg = wbddcRateIndexCfg
        self.set_wbddcRateIndex(self.wbddcRateIndexCfg)

    def get_wbddcIndexCfg(self):
        return self.wbddcIndexCfg

    def set_wbddcIndexCfg(self, wbddcIndexCfg):
        self.wbddcIndexCfg = wbddcIndexCfg
        self.set_wbddcIndex(self.wbddcIndexCfg)

    def get_txFreq(self):
        return self.txFreq

    def set_txFreq(self, txFreq):
        self.txFreq = txFreq
        self.set_rxFreq((self.txFreq+self.rxFreqOffset) if ((self.txFreq+self.rxFreqOffset)>=20) else 20)
        self._txFreqCfg_config = ConfigParser.ConfigParser()
        self._txFreqCfg_config.read(self.confPath)
        if not self._txFreqCfg_config.has_section('tx'):
        	self._txFreqCfg_config.add_section('tx')
        self._txFreqCfg_config.set('tx', 'freq', str(self.txFreq))
        self._txFreqCfg_config.write(open(self.confPath, 'w'))
        self.qtgui_freq_sink_x_0_1.set_frequency_range((self.txFreq)*1e6, self.ducRateSet[self.ducRateIndex])
        self.qtgui_freq_sink_x_0.set_frequency_range(((self.txFreq+self.rxFreqOffset)*1e6)+self.nbddcFreq, self.nbddcRateSet[self.nbddcRateIndex])
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_tx_frequency(self.txFreq)
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_tx_frequency(self.txFreq)

    def get_txAttenCfg(self):
        return self.txAttenCfg

    def set_txAttenCfg(self, txAttenCfg):
        self.txAttenCfg = txAttenCfg
        self.set_txAtten(self.txAttenCfg)

    def get_rxAttenCfg(self):
        return self.rxAttenCfg

    def set_rxAttenCfg(self, rxAttenCfg):
        self.rxAttenCfg = rxAttenCfg
        self.set_rxAtten(self.rxAttenCfg)

    def get_nbddcIndexCfg(self):
        return self.nbddcIndexCfg

    def set_nbddcIndexCfg(self, nbddcIndexCfg):
        self.nbddcIndexCfg = nbddcIndexCfg
        self.set_nbddcIndex(self.nbddcIndexCfg)

    def get_nbddcFreq(self):
        return self.nbddcFreq

    def set_nbddcFreq(self, nbddcFreq):
        self.nbddcFreq = nbddcFreq
        self.z_ddcControl_nb.set_freq(self.nbddcFreq)
        self.qtgui_freq_sink_x_0.set_frequency_range(((self.txFreq+self.rxFreqOffset)*1e6)+self.nbddcFreq, self.nbddcRateSet[self.nbddcRateIndex])
        self.set_nbddcFreqLabel(self._nbddcFreqLabel_formatter(num_to_str(self.nbddcFreq)+"Hz"))

    def get_duchsPfThresh(self):
        return self.duchsPfThresh

    def set_duchsPfThresh(self, duchsPfThresh):
        self.duchsPfThresh = duchsPfThresh
        self.set_duchsPeThresh(self.duchsPfThresh-1)

    def get_ducAttenCfg(self):
        return self.ducAttenCfg

    def set_ducAttenCfg(self, ducAttenCfg):
        self.ducAttenCfg = ducAttenCfg
        self.set_ducAtten(self.ducAttenCfg)

    def get_cwFreq2Cfg(self):
        return self.cwFreq2Cfg

    def set_cwFreq2Cfg(self, cwFreq2Cfg):
        self.cwFreq2Cfg = cwFreq2Cfg
        self.set_cwFreq2(self.cwFreq2Cfg)

    def get_cwAmp2Cfg(self):
        return self.cwAmp2Cfg

    def set_cwAmp2Cfg(self, cwAmp2Cfg):
        self.cwAmp2Cfg = cwAmp2Cfg
        self.set_cwAmp2(self.cwAmp2Cfg)

    def get_cwAmp1Cfg(self):
        return self.cwAmp1Cfg

    def set_cwAmp1Cfg(self, cwAmp1Cfg):
        self.cwAmp1Cfg = cwAmp1Cfg
        self.set_cwAmp1(self.cwAmp1Cfg)

    def get_wbddcRateSet(self):
        return self.wbddcRateSet

    def set_wbddcRateSet(self, wbddcRateSet):
        self.wbddcRateSet = wbddcRateSet
        self.z_ddcControl_wb_0.set_enable(self.wbddcRateIndex in self.wbddcRateSet)
        self.z_ddcControl_wb_0.set_rate(self.wbddcRateIndex if self.wbddcRateIndex in self.wbddcRateSet else 0)
        self.z_ddcControl_wb.set_enable(self.wbddcRateIndex in self.wbddcRateSet)
        self.z_ddcControl_wb.set_rate(self.wbddcRateIndex if self.wbddcRateIndex in self.wbddcRateSet else 0)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rxFreq*1e6, self.wbddcRateSet[self.wbddcRateIndex])

    def get_wbddcRateIndex(self):
        return self.wbddcRateIndex

    def set_wbddcRateIndex(self, wbddcRateIndex):
        self.wbddcRateIndex = wbddcRateIndex
        self._wbddcRateIndex_callback(self.wbddcRateIndex)
        self.z_ddcControl_wb_0.set_enable(self.wbddcRateIndex in self.wbddcRateSet)
        self.z_ddcControl_wb_0.set_rate(self.wbddcRateIndex if self.wbddcRateIndex in self.wbddcRateSet else 0)
        self.z_ddcControl_wb.set_enable(self.wbddcRateIndex in self.wbddcRateSet)
        self.z_ddcControl_wb.set_rate(self.wbddcRateIndex if self.wbddcRateIndex in self.wbddcRateSet else 0)
        self._wbddcRateIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcRateIndexCfg_config.read(self.confPath)
        if not self._wbddcRateIndexCfg_config.has_section('wbddc'):
        	self._wbddcRateIndexCfg_config.add_section('wbddc')
        self._wbddcRateIndexCfg_config.set('wbddc', 'rate_index', str(self.wbddcRateIndex))
        self._wbddcRateIndexCfg_config.write(open(self.confPath, 'w'))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rxFreq*1e6, self.wbddcRateSet[self.wbddcRateIndex])

    def get_wbddcIndex(self):
        return self.wbddcIndex

    def set_wbddcIndex(self, wbddcIndex):
        self.wbddcIndex = wbddcIndex
        self._wbddcIndex_callback(self.wbddcIndex)
        self.z_ddcControl_wb_0.set_rfSource(self.wbddcIndex)
        self.z_ddcControl_wb.set_rfSource(self.wbddcIndex)
        self.z_ddcControl_nb.set_rfSource(self.wbddcIndex)
        self._wbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._wbddcIndexCfg_config.read(self.confPath)
        if not self._wbddcIndexCfg_config.has_section('wbddc'):
        	self._wbddcIndexCfg_config.add_section('wbddc')
        self._wbddcIndexCfg_config.set('wbddc', 'index', str(self.wbddcIndex))
        self._wbddcIndexCfg_config.write(open(self.confPath, 'w'))

    def get_updatePE(self):
        return self.updatePE

    def set_updatePE(self, updatePE):
        self.updatePE = updatePE
        self._updatePE_callback(self.updatePE)

    def get_udpPort(self):
        return self.udpPort

    def set_udpPort(self, udpPort):
        self.udpPort = udpPort
        self.z_ddcControl_wb_0.set_udpPort(self.udpPort+2)
        self.z_ddcControl_wb.set_udpPort(self.udpPort)
        self.z_ddcControl_nb.set_udpPort(self.udpPort+1)

    def get_txsumChoice(self):
        return self.txsumChoice

    def set_txsumChoice(self, txsumChoice):
        self.txsumChoice = txsumChoice
        self._txsumChoice_callback(self.txsumChoice)
        self.aaaa_command_block.send_command("TXSUM %d"%(self.txsumChoice))

    def get_txAtten(self):
        return self.txAtten

    def set_txAtten(self, txAtten):
        self.txAtten = txAtten
        self._txAttenCfg_config = ConfigParser.ConfigParser()
        self._txAttenCfg_config.read(self.confPath)
        if not self._txAttenCfg_config.has_section('tx'):
        	self._txAttenCfg_config.add_section('tx')
        self._txAttenCfg_config.set('tx', 'atten', str(self.txAtten))
        self._txAttenCfg_config.write(open(self.confPath, 'w'))
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_tx_attenuation(self.txAtten)
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_tx_attenuation(self.txAtten)

    def get_rxFreqCfg(self):
        return self.rxFreqCfg

    def set_rxFreqCfg(self, rxFreqCfg):
        self.rxFreqCfg = rxFreqCfg

    def get_rxFreq(self):
        return self.rxFreq

    def set_rxFreq(self, rxFreq):
        self.rxFreq = rxFreq
        self.z_tunerControl_0.set_freq(self.rxFreq)
        self.z_tunerControl.set_freq(self.rxFreq)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rxFreq*1e6, self.wbddcRateSet[self.wbddcRateIndex])

    def get_rxAtten(self):
        return self.rxAtten

    def set_rxAtten(self, rxAtten):
        self.rxAtten = rxAtten
        self.z_tunerControl_0.set_attenuation(self.rxAtten)
        self.z_tunerControl.set_attenuation(self.rxAtten)
        self._rxAttenCfg_config = ConfigParser.ConfigParser()
        self._rxAttenCfg_config.read(self.confPath)
        if not self._rxAttenCfg_config.has_section('rx'):
        	self._rxAttenCfg_config.add_section('rx')
        self._rxAttenCfg_config.set('rx', 'atten', str(self.rxAtten))
        self._rxAttenCfg_config.write(open(self.confPath, 'w'))

    def get_radioParam(self):
        return self.radioParam

    def set_radioParam(self, radioParam):
        self.radioParam = radioParam

    def get_nbddcIndex(self):
        return self.nbddcIndex

    def set_nbddcIndex(self, nbddcIndex):
        self.nbddcIndex = nbddcIndex
        self._nbddcIndex_callback(self.nbddcIndex)
        self.z_ddcControl_nb.set_index(self.nbddcIndex)
        self._nbddcIndexCfg_config = ConfigParser.ConfigParser()
        self._nbddcIndexCfg_config.read(self.confPath)
        if not self._nbddcIndexCfg_config.has_section('nbddc'):
        	self._nbddcIndexCfg_config.add_section('nbddc')
        self._nbddcIndexCfg_config.set('nbddc', 'index', str(self.nbddcIndex))
        self._nbddcIndexCfg_config.write(open(self.confPath, 'w'))

    def get_nbddcFreqLabel(self):
        return self.nbddcFreqLabel

    def set_nbddcFreqLabel(self, nbddcFreqLabel):
        self.nbddcFreqLabel = nbddcFreqLabel
        Qt.QMetaObject.invokeMethod(self._nbddcFreqLabel_label, "setText", Qt.Q_ARG("QString", str(self.nbddcFreqLabel)))

    def get_iface2(self):
        return self.iface2

    def set_iface2(self, iface2):
        self.iface2 = iface2
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_iface_string(self.iface2)

    def get_iface1(self):
        return self.iface1

    def set_iface1(self, iface1):
        self.iface1 = iface1
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_iface_string(self.iface1)

    def get_duchsPeriodList(self):
        return self.duchsPeriodList

    def set_duchsPeriodList(self, duchsPeriodList):
        self.duchsPeriodList = duchsPeriodList

    def get_duchsPeriodHz(self):
        return self.duchsPeriodHz

    def set_duchsPeriodHz(self, duchsPeriodHz):
        self.duchsPeriodHz = duchsPeriodHz
        self._duchsPeriodHz_callback(self.duchsPeriodHz)

    def get_duchsPeThresh(self):
        return self.duchsPeThresh

    def set_duchsPeThresh(self, duchsPeThresh):
        self.duchsPeThresh = duchsPeThresh

    def get_ducIndexLabel(self):
        return self.ducIndexLabel

    def set_ducIndexLabel(self, ducIndexLabel):
        self.ducIndexLabel = ducIndexLabel
        Qt.QMetaObject.invokeMethod(self._ducIndexLabel_label, "setText", Qt.Q_ARG("QString", str(self.ducIndexLabel)))

    def get_ducAtten(self):
        return self.ducAtten

    def set_ducAtten(self, ducAtten):
        self.ducAtten = ducAtten
        self._ducAttenCfg_config = ConfigParser.ConfigParser()
        self._ducAttenCfg_config.read(self.confPath)
        if not self._ducAttenCfg_config.has_section('duc'):
        	self._ducAttenCfg_config.add_section('duc')
        self._ducAttenCfg_config.set('duc', 'atten', str(self.ducAtten))
        self._ducAttenCfg_config.write(open(self.confPath, 'w'))
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_1.set_duc_attenuation(self.ducAtten)
        self.AAA_CyberRadio_NDR651_duc_sink_mk2_0.set_duc_attenuation(self.ducAtten)

    def get_cwFreq2(self):
        return self.cwFreq2

    def set_cwFreq2(self, cwFreq2):
        self.cwFreq2 = cwFreq2
        self._cwFreq2Cfg_config = ConfigParser.ConfigParser()
        self._cwFreq2Cfg_config.read(self.confPath)
        if not self._cwFreq2Cfg_config.has_section('cw'):
        	self._cwFreq2Cfg_config.add_section('cw')
        self._cwFreq2Cfg_config.set('cw', 'freq2', str(self.cwFreq2))
        self._cwFreq2Cfg_config.write(open(self.confPath, 'w'))
        self.blocks_rotator_cc_0_0.set_phase_inc(float(self.cwFreq2)*numpy.pi/50)

    def get_cwAmp2(self):
        return self.cwAmp2

    def set_cwAmp2(self, cwAmp2):
        self.cwAmp2 = cwAmp2
        self._cwAmp2Cfg_config = ConfigParser.ConfigParser()
        self._cwAmp2Cfg_config.read(self.confPath)
        if not self._cwAmp2Cfg_config.has_section('cw'):
        	self._cwAmp2Cfg_config.add_section('cw')
        self._cwAmp2Cfg_config.set('cw', 'amp2', str(self.cwAmp2))
        self._cwAmp2Cfg_config.write(open(self.confPath, 'w'))
        self.analog_const_source_x_0_0.set_offset(10.0**(float(self.cwAmp2)/20))

    def get_cwAmp1(self):
        return self.cwAmp1

    def set_cwAmp1(self, cwAmp1):
        self.cwAmp1 = cwAmp1
        self._cwAmp1Cfg_config = ConfigParser.ConfigParser()
        self._cwAmp1Cfg_config.read(self.confPath)
        if not self._cwAmp1Cfg_config.has_section('cw'):
        	self._cwAmp1Cfg_config.add_section('cw')
        self._cwAmp1Cfg_config.set('cw', 'amp1', str(self.cwAmp1))
        self._cwAmp1Cfg_config.write(open(self.confPath, 'w'))
        self.analog_const_source_x_0.set_offset(10.0**(float(self.cwAmp1)/20))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-p", "--dataPort1", dest="dataPort1", type="intx", default=1,
        help="Set Radio Data Port for DUC/DDC 1 [default=%default]")
    parser.add_option(
        "-P", "--dataPort2", dest="dataPort2", type="intx", default=1,
        help="Set Radio Data Port for DUC/DDC 2 [default=%default]")
    parser.add_option(
        "", "--dipIndex", dest="dipIndex", type="intx", default=-1,
        help="Set DIP Index [default=%default]")
    parser.add_option(
        "-d", "--ducIndex", dest="ducIndex", type="intx", default=1,
        help="Set DUC Index [default=%default]")
    parser.add_option(
        "", "--fftRate", dest="fftRate", type="intx", default=8,
        help="Set FFT Rate [default=%default]")
    parser.add_option(
        "", "--fftSizeExp", dest="fftSizeExp", type="intx", default=15,
        help="Set FFT Size [default=%default]")
    parser.add_option(
        "-n", "--hostname", dest="hostname", type="string", default='ndr651',
        help="Set Radio Hostname/IP [default=%default]")
    parser.add_option(
        "-i", "--localInterface1", dest="localInterface1", type="string", default="eth0",
        help="Set 10GbE Port #1 [default=%default]")
    parser.add_option(
        "-I", "--localInterface2", dest="localInterface2", type="string", default="eth7",
        help="Set 10GbE Port #2 [default=%default]")
    return parser


def main(top_block_cls=ndr651_txrx_gui, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(dataPort1=options.dataPort1, dataPort2=options.dataPort2, dipIndex=options.dipIndex, ducIndex=options.ducIndex, fftRate=options.fftRate, fftSizeExp=options.fftSizeExp, hostname=options.hostname, localInterface1=options.localInterface1, localInterface2=options.localInterface2)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
