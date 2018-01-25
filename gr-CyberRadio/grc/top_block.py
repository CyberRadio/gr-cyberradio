#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Nov  3 17:46:03 2017
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import CyberRadio
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self, fftWindow=window.blackmanharris(1024), iirAlpha=2.0**-3, samp_rate=1.0e6, vecLen=2**11, vecRate=32):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.fftWindow = fftWindow
        self.iirAlpha = iirAlpha
        self.samp_rate = samp_rate
        self.vecLen = vecLen
        self.vecRate = vecRate

        ##################################################
        # Blocks
        ##################################################
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(iirAlpha, vecLen)
        self.fft_vxx_0 = fft.fft_vcc(vecLen, True, (fftWindow), True, 1)
        self.blocks_stream_to_vector_decimator_0 = blocks.stream_to_vector_decimator(
        	item_size=gr.sizeof_gr_complex,
        	sample_rate=samp_rate,
        	vec_rate=vecRate,
        	vec_len=vecLen,
        )
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*vecLen)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vecLen)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(vecLen)
        self.CyberRadio_vector_nlog10_ff_0 = CyberRadio.vector_nlog10_ff(10, vecLen, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.CyberRadio_vector_nlog10_ff_0, 0), (self, 2))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self, 3))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_stream_to_vector_decimator_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_stream_to_vector_decimator_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_decimator_0, 0), (self, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.fft_vxx_0, 0), (self, 1))
        self.connect((self, 0), (self.blocks_stream_to_vector_decimator_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.CyberRadio_vector_nlog10_ff_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_fftWindow(self):
        return self.fftWindow

    def set_fftWindow(self, fftWindow):
        self.fftWindow = fftWindow

    def get_iirAlpha(self):
        return self.iirAlpha

    def set_iirAlpha(self, iirAlpha):
        self.iirAlpha = iirAlpha
        self.single_pole_iir_filter_xx_0.set_taps(self.iirAlpha)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_stream_to_vector_decimator_0.set_sample_rate(self.samp_rate)

    def get_vecLen(self):
        return self.vecLen

    def set_vecLen(self, vecLen):
        self.vecLen = vecLen

    def get_vecRate(self):
        return self.vecRate

    def set_vecRate(self, vecRate):
        self.vecRate = vecRate
        self.blocks_stream_to_vector_decimator_0.set_vec_rate(self.vecRate)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--iirAlpha", dest="iirAlpha", type="eng_float", default=eng_notation.num_to_str(2.0**-3),
        help="Set Avg Gain [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(1.0e6),
        help="Set Sample Rate [default=%default]")
    parser.add_option(
        "", "--vecLen", dest="vecLen", type="intx", default=2**11,
        help="Set Vector/FFT Size [default=%default]")
    parser.add_option(
        "", "--vecRate", dest="vecRate", type="intx", default=32,
        help="Set Vector Rate [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(iirAlpha=options.iirAlpha, samp_rate=options.samp_rate, vecLen=options.vecLen, vecRate=options.vecRate)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
