#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NDR651 Single Tx/Rx Example
# Author: NH
# Generated: Fri Aug 25 13:09:00 2017
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
from gnuradio import analog
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
import CyberRadioDriver as crd
import os, numpy, time
import sys
from gnuradio import qtgui


class ndr651_single_trx(gr.top_block, Qt.QWidget):

    def __init__(self, dataPort=1, ducIndex=1, ducRateIndex=1, hostname='ndr651', localInterface="eth6", txChannel=1):
        gr.top_block.__init__(self, "NDR651 Single Tx/Rx Example")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDR651 Single Tx/Rx Example")
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

        self.settings = Qt.QSettings("GNU Radio", "ndr651_single_trx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.dataPort = dataPort
        self.ducIndex = ducIndex
        self.ducRateIndex = ducRateIndex
        self.hostname = hostname
        self.localInterface = localInterface
        self.txChannel = txChannel

        ##################################################
        # Variables
        ##################################################
        self.confPath = confPath = os.path.expanduser("~/.ndr651_single_trx.cfg")
        self._txFreqCfg_config = ConfigParser.ConfigParser()
        self._txFreqCfg_config.read(confPath)
        try: txFreqCfg = self._txFreqCfg_config.getfloat('tx', 'freq')
        except: txFreqCfg = 1000
        self.txFreqCfg = txFreqCfg
        self._txAttenCfg_config = ConfigParser.ConfigParser()
        self._txAttenCfg_config.read(confPath)
        try: txAttenCfg = self._txAttenCfg_config.getint('tx', 'atten')
        except: txAttenCfg = 0
        self.txAttenCfg = txAttenCfg
        self.radioObj = radioObj = crd.getRadioObject("ndr651", verbose=False)
        self._ducFreqCfg_config = ConfigParser.ConfigParser()
        self._ducFreqCfg_config.read(confPath)
        try: ducFreqCfg = self._ducFreqCfg_config.getfloat('duc', 'fre')
        except: ducFreqCfg = 0
        self.ducFreqCfg = ducFreqCfg
        self._ducAttenCfg_config = ConfigParser.ConfigParser()
        self._ducAttenCfg_config.read(confPath)
        try: ducAttenCfg = self._ducAttenCfg_config.getfloat('duc', 'atten')
        except: ducAttenCfg = 0
        self.ducAttenCfg = ducAttenCfg
        self._cwFreqCfg_config = ConfigParser.ConfigParser()
        self._cwFreqCfg_config.read(confPath)
        try: cwFreqCfg = self._cwFreqCfg_config.getfloat('cw', 'freq')
        except: cwFreqCfg = 1.25
        self.cwFreqCfg = cwFreqCfg
        self._cwAmpCfg_config = ConfigParser.ConfigParser()
        self._cwAmpCfg_config.read(confPath)
        try: cwAmpCfg = self._cwAmpCfg_config.getfloat('cw', 'amp1')
        except: cwAmpCfg = -1.0
        self.cwAmpCfg = cwAmpCfg
        self.txFreq = txFreq = txFreqCfg
        self.txAtten = txAtten = txAttenCfg
        self.radioParam = radioParam = {"type":"ndr651", "host":hostname, "port":8617, "obj":radioObj}
        self.ducRateSet = ducRateSet = radioObj.getWbducRateSet()
        self.ducFreq = ducFreq = ducFreqCfg
        self.ducAtten = ducAtten = ducAttenCfg
        self.cwFreq = cwFreq = cwFreqCfg
        self.cwAmp = cwAmp = cwAmpCfg

        ##################################################
        # Blocks
        ##################################################
        self._txFreq_range = Range(2, 6000, 40, txFreqCfg, 200)
        self._txFreq_win = RangeWidget(self._txFreq_range, self.set_txFreq, 'TX Freq (MHz)', "counter_slider", float)
        self.top_layout.addWidget(self._txFreq_win)
        self._txAtten_range = Range(0, 15, 1, txAttenCfg, 16)
        self._txAtten_win = RangeWidget(self._txAtten_range, self.set_txAtten, 'TX Atten', "counter_slider", int)
        self.top_layout.addWidget(self._txAtten_win)
        self._ducFreq_range = Range(-25.5, +25.5, 0.5, ducFreqCfg, 4001)
        self._ducFreq_win = RangeWidget(self._ducFreq_range, self.set_ducFreq, 'DUC Freq (MHz)', "counter_slider", float)
        self.top_layout.addWidget(self._ducFreq_win)
        self._ducAtten_range = Range(-20, 60, 1.0, ducAttenCfg, int(60/0.25)+1)
        self._ducAtten_win = RangeWidget(self._ducAtten_range, self.set_ducAtten, 'DUC Attenuation', "counter_slider", float)
        self.top_layout.addWidget(self._ducAtten_win)
        self._cwFreq_range = Range(-40.0, +40.0, 1.25, cwFreqCfg, int((80.0/2.5)+1))
        self._cwFreq_win = RangeWidget(self._cwFreq_range, self.set_cwFreq, 'GR CW Freq (% BW)', "counter_slider", float)
        self.top_layout.addWidget(self._cwFreq_win)
        self._cwAmp_range = Range(-90, +10, 1, cwAmpCfg, 101)
        self._cwAmp_win = RangeWidget(self._cwAmp_range, self.set_cwAmp, 'GR CW Amp (dB)', "counter_slider", float)
        self.top_layout.addWidget(self._cwAmp_win)
        self.new_651_sink = CyberRadio.ndr651_sink(hostname, 1024, True)
        self.new_651_sink.setDUCParameters(ducIndex, ducRateIndex, txChannel)
        self.new_651_sink.setDUCFreq(ducFreq*1e6)
        self.new_651_sink.setDUCAtten(ducAtten)
        self.new_651_sink.setEthernetInterface(dataPort, localInterface, ducIndex+65000)
        self.new_651_sink.setTxFreq(txFreq)
        self.new_651_sink.setTxAtten(txAtten)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_rotator_cc_0 = blocks.rotator_cc(float(cwFreq)*numpy.pi/50)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 10.0**(float(cwAmp)/20))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.new_651_sink, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ndr651_single_trx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_dataPort(self):
        return self.dataPort

    def set_dataPort(self, dataPort):
        self.dataPort = dataPort

    def get_ducIndex(self):
        return self.ducIndex

    def set_ducIndex(self, ducIndex):
        self.ducIndex = ducIndex

    def get_ducRateIndex(self):
        return self.ducRateIndex

    def set_ducRateIndex(self, ducRateIndex):
        self.ducRateIndex = ducRateIndex
        self.new_651_sink.setDUCRateIndex(self.ducRateIndex)

    def get_hostname(self):
        return self.hostname

    def set_hostname(self, hostname):
        self.hostname = hostname
        self.set_radioParam({"type":"ndr651", "host":self.hostname, "port":8617, "obj":self.radioObj})

    def get_localInterface(self):
        return self.localInterface

    def set_localInterface(self, localInterface):
        self.localInterface = localInterface

    def get_txChannel(self):
        return self.txChannel

    def set_txChannel(self, txChannel):
        self.txChannel = txChannel

    def get_confPath(self):
        return self.confPath

    def set_confPath(self, confPath):
        self.confPath = confPath
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
        self._ducFreqCfg_config = ConfigParser.ConfigParser()
        self._ducFreqCfg_config.read(self.confPath)
        if not self._ducFreqCfg_config.has_section('duc'):
        	self._ducFreqCfg_config.add_section('duc')
        self._ducFreqCfg_config.set('duc', 'fre', str(self.ducFreq))
        self._ducFreqCfg_config.write(open(self.confPath, 'w'))
        self._ducAttenCfg_config = ConfigParser.ConfigParser()
        self._ducAttenCfg_config.read(self.confPath)
        if not self._ducAttenCfg_config.has_section('duc'):
        	self._ducAttenCfg_config.add_section('duc')
        self._ducAttenCfg_config.set('duc', 'atten', str(self.ducAtten))
        self._ducAttenCfg_config.write(open(self.confPath, 'w'))
        self._cwFreqCfg_config = ConfigParser.ConfigParser()
        self._cwFreqCfg_config.read(self.confPath)
        if not self._cwFreqCfg_config.has_section('cw'):
        	self._cwFreqCfg_config.add_section('cw')
        self._cwFreqCfg_config.set('cw', 'freq', str(self.cwFreq))
        self._cwFreqCfg_config.write(open(self.confPath, 'w'))
        self._cwAmpCfg_config = ConfigParser.ConfigParser()
        self._cwAmpCfg_config.read(self.confPath)
        if not self._cwAmpCfg_config.has_section('cw'):
        	self._cwAmpCfg_config.add_section('cw')
        self._cwAmpCfg_config.set('cw', 'amp1', str(self.cwAmp))
        self._cwAmpCfg_config.write(open(self.confPath, 'w'))

    def get_txFreqCfg(self):
        return self.txFreqCfg

    def set_txFreqCfg(self, txFreqCfg):
        self.txFreqCfg = txFreqCfg
        self.set_txFreq(self.txFreqCfg)

    def get_txAttenCfg(self):
        return self.txAttenCfg

    def set_txAttenCfg(self, txAttenCfg):
        self.txAttenCfg = txAttenCfg
        self.set_txAtten(self.txAttenCfg)

    def get_radioObj(self):
        return self.radioObj

    def set_radioObj(self, radioObj):
        self.radioObj = radioObj
        self.set_radioParam({"type":"ndr651", "host":self.hostname, "port":8617, "obj":self.radioObj})

    def get_ducFreqCfg(self):
        return self.ducFreqCfg

    def set_ducFreqCfg(self, ducFreqCfg):
        self.ducFreqCfg = ducFreqCfg
        self.set_ducFreq(self.ducFreqCfg)

    def get_ducAttenCfg(self):
        return self.ducAttenCfg

    def set_ducAttenCfg(self, ducAttenCfg):
        self.ducAttenCfg = ducAttenCfg
        self.set_ducAtten(self.ducAttenCfg)

    def get_cwFreqCfg(self):
        return self.cwFreqCfg

    def set_cwFreqCfg(self, cwFreqCfg):
        self.cwFreqCfg = cwFreqCfg
        self.set_cwFreq(self.cwFreqCfg)

    def get_cwAmpCfg(self):
        return self.cwAmpCfg

    def set_cwAmpCfg(self, cwAmpCfg):
        self.cwAmpCfg = cwAmpCfg
        self.set_cwAmp(self.cwAmpCfg)

    def get_txFreq(self):
        return self.txFreq

    def set_txFreq(self, txFreq):
        self.txFreq = txFreq
        self._txFreqCfg_config = ConfigParser.ConfigParser()
        self._txFreqCfg_config.read(self.confPath)
        if not self._txFreqCfg_config.has_section('tx'):
        	self._txFreqCfg_config.add_section('tx')
        self._txFreqCfg_config.set('tx', 'freq', str(self.txFreq))
        self._txFreqCfg_config.write(open(self.confPath, 'w'))
        self.new_651_sink.setTxFreq(self.txFreq)

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
        self.new_651_sink.setTxAtten(self.txAtten)

    def get_radioParam(self):
        return self.radioParam

    def set_radioParam(self, radioParam):
        self.radioParam = radioParam

    def get_ducRateSet(self):
        return self.ducRateSet

    def set_ducRateSet(self, ducRateSet):
        self.ducRateSet = ducRateSet

    def get_ducFreq(self):
        return self.ducFreq

    def set_ducFreq(self, ducFreq):
        self.ducFreq = ducFreq
        self.new_651_sink.setDUCFreq(self.ducFreq*1e6)
        self._ducFreqCfg_config = ConfigParser.ConfigParser()
        self._ducFreqCfg_config.read(self.confPath)
        if not self._ducFreqCfg_config.has_section('duc'):
        	self._ducFreqCfg_config.add_section('duc')
        self._ducFreqCfg_config.set('duc', 'fre', str(self.ducFreq))
        self._ducFreqCfg_config.write(open(self.confPath, 'w'))

    def get_ducAtten(self):
        return self.ducAtten

    def set_ducAtten(self, ducAtten):
        self.ducAtten = ducAtten
        self.new_651_sink.setDUCAtten(self.ducAtten)
        self._ducAttenCfg_config = ConfigParser.ConfigParser()
        self._ducAttenCfg_config.read(self.confPath)
        if not self._ducAttenCfg_config.has_section('duc'):
        	self._ducAttenCfg_config.add_section('duc')
        self._ducAttenCfg_config.set('duc', 'atten', str(self.ducAtten))
        self._ducAttenCfg_config.write(open(self.confPath, 'w'))

    def get_cwFreq(self):
        return self.cwFreq

    def set_cwFreq(self, cwFreq):
        self.cwFreq = cwFreq
        self._cwFreqCfg_config = ConfigParser.ConfigParser()
        self._cwFreqCfg_config.read(self.confPath)
        if not self._cwFreqCfg_config.has_section('cw'):
        	self._cwFreqCfg_config.add_section('cw')
        self._cwFreqCfg_config.set('cw', 'freq', str(self.cwFreq))
        self._cwFreqCfg_config.write(open(self.confPath, 'w'))
        self.blocks_rotator_cc_0.set_phase_inc(float(self.cwFreq)*numpy.pi/50)

    def get_cwAmp(self):
        return self.cwAmp

    def set_cwAmp(self, cwAmp):
        self.cwAmp = cwAmp
        self._cwAmpCfg_config = ConfigParser.ConfigParser()
        self._cwAmpCfg_config.read(self.confPath)
        if not self._cwAmpCfg_config.has_section('cw'):
        	self._cwAmpCfg_config.add_section('cw')
        self._cwAmpCfg_config.set('cw', 'amp1', str(self.cwAmp))
        self._cwAmpCfg_config.write(open(self.confPath, 'w'))
        self.analog_const_source_x_0.set_offset(10.0**(float(self.cwAmp)/20))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-p", "--dataPort", dest="dataPort", type="intx", default=1,
        help="Set Radio Data Port [default=%default]")
    parser.add_option(
        "-d", "--ducIndex", dest="ducIndex", type="intx", default=1,
        help="Set DUC Index [default=%default]")
    parser.add_option(
        "-r", "--ducRateIndex", dest="ducRateIndex", type="intx", default=1,
        help="Set DUC Rate Index [default=%default]")
    parser.add_option(
        "-n", "--hostname", dest="hostname", type="string", default='ndr651',
        help="Set Radio Hostname/IP [default=%default]")
    parser.add_option(
        "-i", "--localInterface", dest="localInterface", type="string", default="eth6",
        help="Set 10GbE Port [default=%default]")
    parser.add_option(
        "-t", "--txChannel", dest="txChannel", type="intx", default=1,
        help="Set TX Channel [default=%default]")
    return parser


def main(top_block_cls=ndr651_single_trx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(dataPort=options.dataPort, ducIndex=options.ducIndex, ducRateIndex=options.ducRateIndex, hostname=options.hostname, localInterface=options.localInterface, txChannel=options.txChannel)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
