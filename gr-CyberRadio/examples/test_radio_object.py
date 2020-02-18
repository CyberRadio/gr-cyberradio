#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Radio Object Test
# Generated: Wed Oct 18 15:27:45 2017
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
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import CyberRadio
import CyberRadioDriver
import CyberRadioDriver as crd
import sys
import threading
import time
from gnuradio import qtgui


class test_radio_object(gr.top_block, Qt.QWidget):

    def __init__(self, radioControlPort=8617, radioHostname='ndr308', radioType='ndr308', radioVerbose=True):
        gr.top_block.__init__(self, "Radio Object Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Radio Object Test")
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

        self.settings = Qt.QSettings("GNU Radio", "test_radio_object")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.radioControlPort = radioControlPort
        self.radioHostname = radioHostname
        self.radioType = radioType
        self.radioVerbose = radioVerbose

        ##################################################
        # Variables
        ##################################################
        self.radioObj = radioObj = crd.getRadioObject(radioType, verbose=bool(radioVerbose))
        self.radioObj.connect('tcp', 'ndr308', 8617)
        self.funprober = funprober = 0
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = funprober
        self.samp_rate = samp_rate = 1.0
        self.rfFreqMhz = rfFreqMhz = radioObj.getTunerFrequencyRange()[0]/1e6
        self.radioParam = radioParam = {"type":radioType,"host":radioHostname,"port":8617,"obj":radioObj}
        self.radioObj_class = radioObj_class = radioObj.__class__

        ##################################################
        # Blocks
        ##################################################
        self._rfFreqMhz_range = Range(radioObj.getTunerFrequencyRange()[0]/1e6, radioObj.getTunerFrequencyRange()[-1]/1e6, 100, radioObj.getTunerFrequencyRange()[0]/1e6, 200)
        self._rfFreqMhz_win = RangeWidget(self._rfFreqMhz_range, self.set_rfFreqMhz, 'RF Freq (MHz)', "counter_slider", float)
        self.top_layout.addWidget(self._rfFreqMhz_win)
        self.levelProber = blocks.probe_signal_f()
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: x

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Signal Level'+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_tool_bar)

        self.throttler = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.sigSource = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, samp_rate/16, 1, 0)

        def _funprober_probe():
            while True:
                val = self.levelProber.level()
                try:
                    self.set_funprober(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _funprober_thread = threading.Thread(target=_funprober_probe)
        _funprober_thread.daemon = True
        _funprober_thread.start()

        self.comp2mag = blocks.complex_to_mag(1)
        self.CyberRadio_generic_tuner_control_block_0_0 = CyberRadio.generic_tuner_control_block(
                    radioParam,
                    1,
                    True,
                    int(rfFreqMhz),
                    0,
                    1,
                    {},
                    True
                     )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.comp2mag, 0), (self.levelProber, 0))
        self.connect((self.sigSource, 0), (self.throttler, 0))
        self.connect((self.throttler, 0), (self.comp2mag, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_radio_object")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_radioControlPort(self):
        return self.radioControlPort

    def set_radioControlPort(self, radioControlPort):
        self.radioControlPort = radioControlPort

    def get_radioHostname(self):
        return self.radioHostname

    def set_radioHostname(self, radioHostname):
        self.radioHostname = radioHostname
        self.set_radioParam({"type":self.radioType,"host":self.radioHostname,"port":8617,"obj":self.radioObj})

    def get_radioType(self):
        return self.radioType

    def set_radioType(self, radioType):
        self.radioType = radioType
        self.set_radioParam({"type":self.radioType,"host":self.radioHostname,"port":8617,"obj":self.radioObj})

    def get_radioVerbose(self):
        return self.radioVerbose

    def set_radioVerbose(self, radioVerbose):
        self.radioVerbose = radioVerbose

    def get_radioObj(self):
        return self.radioObj

    def set_radioObj(self, radioObj):
        self.radioObj = radioObj
        self.set_radioParam({"type":self.radioType,"host":self.radioHostname,"port":8617,"obj":self.radioObj})

    def get_funprober(self):
        return self.funprober

    def set_funprober(self, funprober):
        self.funprober = funprober
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.funprober))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_label_0)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.throttler.set_sample_rate(self.samp_rate)
        self.sigSource.set_sampling_freq(self.samp_rate)
        self.sigSource.set_frequency(self.samp_rate/16)

    def get_rfFreqMhz(self):
        return self.rfFreqMhz

    def set_rfFreqMhz(self, rfFreqMhz):
        self.rfFreqMhz = rfFreqMhz
        self.CyberRadio_generic_tuner_control_block_0_0.set_freq(int(self.rfFreqMhz))

    def get_radioParam(self):
        return self.radioParam

    def set_radioParam(self, radioParam):
        self.radioParam = radioParam

    def get_radioObj_class(self):
        return self.radioObj_class

    def set_radioObj_class(self, radioObj_class):
        self.radioObj_class = radioObj_class


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-p", "--radioControlPort", dest="radioControlPort", type="intx", default=8617,
        help="Set Radio Control Port [default=%default]")
    parser.add_option(
        "-n", "--radioHostname", dest="radioHostname", type="string", default='ndr308',
        help="Set Radio Hostname [default=%default]")
    parser.add_option(
        "-r", "--radioType", dest="radioType", type="string", default='ndr308',
        help="Set Radio Type [default=%default]")
    parser.add_option(
        "-v", "--radioVerbose", dest="radioVerbose", type="intx", default=True,
        help="Set Verbose Radio Connection [default=%default]")
    return parser


def main(top_block_cls=test_radio_object, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(radioControlPort=options.radioControlPort, radioHostname=options.radioHostname, radioType=options.radioType, radioVerbose=options.radioVerbose)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
