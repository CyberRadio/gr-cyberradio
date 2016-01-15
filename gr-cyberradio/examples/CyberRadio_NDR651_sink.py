#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: NDR651 Sink Demo
# Author: CRS
# Description: CRS NDR651 Sink Demo
# Generated: Fri Oct 23 11:00:10 2015
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
from optparse import OptionParser
import CyberRadio
import sys
import threading
import time


class ndr651_sink_demo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NDR651 Sink Demo")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDR651 Sink Demo")
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

        self.settings = Qt.QSettings("GNU Radio", "ndr651_sink_demo")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.wbduc2_stream = wbduc2_stream = 42002
        self.wbduc2_rate = wbduc2_rate = 0
        self.wbduc2_nominal_sample_rate = wbduc2_nominal_sample_rate = 32000
        self.wbduc2_iface = wbduc2_iface = "eth10"
        self.wbduc2_freq = wbduc2_freq = 0
        self.wbduc2_chans = wbduc2_chans = 2
        self.wbduc2_atten = wbduc2_atten = 0
        self.wbduc1_stream = wbduc1_stream = 42001
        self.wbduc1_rate = wbduc1_rate = 0
        self.wbduc1_nominal_sample_rate = wbduc1_nominal_sample_rate = 32000
        self.wbduc1_iface = wbduc1_iface = "eth10"
        self.wbduc1_freq = wbduc1_freq = 0
        self.wbduc1_chans = wbduc1_chans = 1
        self.wbduc1_atten = wbduc1_atten = 0
        self.tx2_freq = tx2_freq = 901
        self.tx2_enable = tx2_enable = True
        self.tx2_atten = tx2_atten = 2
        self.tx1_freq = tx1_freq = 899
        self.tx1_enable = tx1_enable = True
        self.tx1_atten = tx1_atten = 1

        ##################################################
        # Blocks
        ##################################################
        self._wbduc2_stream_tool_bar = Qt.QToolBar(self)
        self._wbduc2_stream_tool_bar.addWidget(Qt.QLabel("Stream"+": "))
        self._wbduc2_stream_line_edit = Qt.QLineEdit(str(self.wbduc2_stream))
        self._wbduc2_stream_tool_bar.addWidget(self._wbduc2_stream_line_edit)
        self._wbduc2_stream_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc2_stream(int(str(self._wbduc2_stream_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc2_stream_tool_bar, 3, 5, 1, 1)
        self._wbduc2_rate_tool_bar = Qt.QToolBar(self)
        self._wbduc2_rate_tool_bar.addWidget(Qt.QLabel("Rate"+": "))
        self._wbduc2_rate_line_edit = Qt.QLineEdit(str(self.wbduc2_rate))
        self._wbduc2_rate_tool_bar.addWidget(self._wbduc2_rate_line_edit)
        self._wbduc2_rate_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc2_rate(int(str(self._wbduc2_rate_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc2_rate_tool_bar, 3, 1, 1, 1)
        self._wbduc2_iface_tool_bar = Qt.QToolBar(self)
        self._wbduc2_iface_tool_bar.addWidget(Qt.QLabel("DUC2: IFace"+": "))
        self._wbduc2_iface_line_edit = Qt.QLineEdit(str(self.wbduc2_iface))
        self._wbduc2_iface_tool_bar.addWidget(self._wbduc2_iface_line_edit)
        self._wbduc2_iface_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc2_iface(str(str(self._wbduc2_iface_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc2_iface_tool_bar, 3, 0, 1, 1)
        self._wbduc2_freq_tool_bar = Qt.QToolBar(self)
        self._wbduc2_freq_tool_bar.addWidget(Qt.QLabel("Freq"+": "))
        self._wbduc2_freq_line_edit = Qt.QLineEdit(str(self.wbduc2_freq))
        self._wbduc2_freq_tool_bar.addWidget(self._wbduc2_freq_line_edit)
        self._wbduc2_freq_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc2_freq(int(str(self._wbduc2_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc2_freq_tool_bar, 3, 2, 1, 1)
        self._wbduc2_chans_tool_bar = Qt.QToolBar(self)
        self._wbduc2_chans_tool_bar.addWidget(Qt.QLabel("Chans"+": "))
        self._wbduc2_chans_line_edit = Qt.QLineEdit(str(self.wbduc2_chans))
        self._wbduc2_chans_tool_bar.addWidget(self._wbduc2_chans_line_edit)
        self._wbduc2_chans_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc2_chans(int(str(self._wbduc2_chans_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc2_chans_tool_bar, 3, 4, 1, 1)
        self._wbduc2_atten_tool_bar = Qt.QToolBar(self)
        self._wbduc2_atten_tool_bar.addWidget(Qt.QLabel("Atten"+": "))
        self._wbduc2_atten_line_edit = Qt.QLineEdit(str(self.wbduc2_atten))
        self._wbduc2_atten_tool_bar.addWidget(self._wbduc2_atten_line_edit)
        self._wbduc2_atten_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc2_atten(int(str(self._wbduc2_atten_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc2_atten_tool_bar, 3, 3, 1, 1)
        self._wbduc1_stream_tool_bar = Qt.QToolBar(self)
        self._wbduc1_stream_tool_bar.addWidget(Qt.QLabel("Stream"+": "))
        self._wbduc1_stream_line_edit = Qt.QLineEdit(str(self.wbduc1_stream))
        self._wbduc1_stream_tool_bar.addWidget(self._wbduc1_stream_line_edit)
        self._wbduc1_stream_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc1_stream(int(str(self._wbduc1_stream_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc1_stream_tool_bar, 2, 5, 1, 1)
        self._wbduc1_rate_tool_bar = Qt.QToolBar(self)
        self._wbduc1_rate_tool_bar.addWidget(Qt.QLabel("Rate"+": "))
        self._wbduc1_rate_line_edit = Qt.QLineEdit(str(self.wbduc1_rate))
        self._wbduc1_rate_tool_bar.addWidget(self._wbduc1_rate_line_edit)
        self._wbduc1_rate_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc1_rate(int(str(self._wbduc1_rate_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc1_rate_tool_bar, 2, 1, 1, 1)
        self._wbduc1_iface_tool_bar = Qt.QToolBar(self)
        self._wbduc1_iface_tool_bar.addWidget(Qt.QLabel("DUC1: IFace"+": "))
        self._wbduc1_iface_line_edit = Qt.QLineEdit(str(self.wbduc1_iface))
        self._wbduc1_iface_tool_bar.addWidget(self._wbduc1_iface_line_edit)
        self._wbduc1_iface_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc1_iface(str(str(self._wbduc1_iface_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc1_iface_tool_bar, 2, 0, 1, 1)
        self._wbduc1_freq_tool_bar = Qt.QToolBar(self)
        self._wbduc1_freq_tool_bar.addWidget(Qt.QLabel("Freq"+": "))
        self._wbduc1_freq_line_edit = Qt.QLineEdit(str(self.wbduc1_freq))
        self._wbduc1_freq_tool_bar.addWidget(self._wbduc1_freq_line_edit)
        self._wbduc1_freq_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc1_freq(int(str(self._wbduc1_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc1_freq_tool_bar, 2, 2, 1, 1)
        self._wbduc1_chans_tool_bar = Qt.QToolBar(self)
        self._wbduc1_chans_tool_bar.addWidget(Qt.QLabel("Chans"+": "))
        self._wbduc1_chans_line_edit = Qt.QLineEdit(str(self.wbduc1_chans))
        self._wbduc1_chans_tool_bar.addWidget(self._wbduc1_chans_line_edit)
        self._wbduc1_chans_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc1_chans(int(str(self._wbduc1_chans_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc1_chans_tool_bar, 2, 4, 1, 1)
        self._wbduc1_atten_tool_bar = Qt.QToolBar(self)
        self._wbduc1_atten_tool_bar.addWidget(Qt.QLabel("Atten"+": "))
        self._wbduc1_atten_line_edit = Qt.QLineEdit(str(self.wbduc1_atten))
        self._wbduc1_atten_tool_bar.addWidget(self._wbduc1_atten_line_edit)
        self._wbduc1_atten_line_edit.returnPressed.connect(
        	lambda: self.set_wbduc1_atten(int(str(self._wbduc1_atten_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbduc1_atten_tool_bar, 2, 3, 1, 1)
        self._tx2_freq_tool_bar = Qt.QToolBar(self)
        self._tx2_freq_tool_bar.addWidget(Qt.QLabel("Freq"+": "))
        self._tx2_freq_line_edit = Qt.QLineEdit(str(self.tx2_freq))
        self._tx2_freq_tool_bar.addWidget(self._tx2_freq_line_edit)
        self._tx2_freq_line_edit.returnPressed.connect(
        	lambda: self.set_tx2_freq(int(str(self._tx2_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tx2_freq_tool_bar, 1, 1, 1, 1)
        _tx2_enable_check_box = Qt.QCheckBox("TX2: Enable")
        self._tx2_enable_choices = {True: True, False: False}
        self._tx2_enable_choices_inv = dict((v,k) for k,v in self._tx2_enable_choices.iteritems())
        self._tx2_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_tx2_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._tx2_enable_choices_inv[i]))
        self._tx2_enable_callback(self.tx2_enable)
        _tx2_enable_check_box.stateChanged.connect(lambda i: self.set_tx2_enable(self._tx2_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_tx2_enable_check_box, 1, 0, 1, 1)
        self._tx2_atten_tool_bar = Qt.QToolBar(self)
        self._tx2_atten_tool_bar.addWidget(Qt.QLabel("Atten"+": "))
        self._tx2_atten_line_edit = Qt.QLineEdit(str(self.tx2_atten))
        self._tx2_atten_tool_bar.addWidget(self._tx2_atten_line_edit)
        self._tx2_atten_line_edit.returnPressed.connect(
        	lambda: self.set_tx2_atten(int(str(self._tx2_atten_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tx2_atten_tool_bar, 1, 2, 1, 1)
        self._tx1_freq_tool_bar = Qt.QToolBar(self)
        self._tx1_freq_tool_bar.addWidget(Qt.QLabel("Freq"+": "))
        self._tx1_freq_line_edit = Qt.QLineEdit(str(self.tx1_freq))
        self._tx1_freq_tool_bar.addWidget(self._tx1_freq_line_edit)
        self._tx1_freq_line_edit.returnPressed.connect(
        	lambda: self.set_tx1_freq(int(str(self._tx1_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tx1_freq_tool_bar, 0, 1, 1, 1)
        _tx1_enable_check_box = Qt.QCheckBox("TX1: Enable")
        self._tx1_enable_choices = {True: True, False: False}
        self._tx1_enable_choices_inv = dict((v,k) for k,v in self._tx1_enable_choices.iteritems())
        self._tx1_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_tx1_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._tx1_enable_choices_inv[i]))
        self._tx1_enable_callback(self.tx1_enable)
        _tx1_enable_check_box.stateChanged.connect(lambda i: self.set_tx1_enable(self._tx1_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_tx1_enable_check_box, 0, 0, 1, 1)
        self._tx1_atten_tool_bar = Qt.QToolBar(self)
        self._tx1_atten_tool_bar.addWidget(Qt.QLabel("Atten"+": "))
        self._tx1_atten_line_edit = Qt.QLineEdit(str(self.tx1_atten))
        self._tx1_atten_tool_bar.addWidget(self._tx1_atten_line_edit)
        self._tx1_atten_line_edit.returnPressed.connect(
        	lambda: self.set_tx1_atten(int(str(self._tx1_atten_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tx1_atten_tool_bar, 0, 2, 1, 1)
        self.CyberRadio_NDR651_sink_0 = CyberRadio.NDR651_sink(
            verbose_mode=True,
            radio_host_name="ndr651",
            radio_host_port=8617,
            tengig_iface_list=['eth10', 'eth11'],
            iq_scale_factor=2**15,
            num_transmitters=2,
            transmitter1_param_list=[tx1_enable, tx1_freq, tx1_atten],
            transmitter2_param_list=[tx2_enable, tx2_freq, tx2_atten],
            num_wbducs=2,
            wbduc1_param_list=[wbduc1_iface, wbduc1_rate, wbduc1_freq, wbduc1_atten, wbduc1_chans, wbduc1_stream],
            wbduc2_param_list=[wbduc2_iface, wbduc2_rate, wbduc2_freq, wbduc2_atten, wbduc2_chans, wbduc2_stream],
        	debug=False,
        )
        def _wbduc2_nominal_sample_rate_probe():
        	while True:
        		val = self.CyberRadio_NDR651_sink_0.get_wbduc_nominal_sample_rate(2)
        		try: self.set_wbduc2_nominal_sample_rate(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(2))
        _wbduc2_nominal_sample_rate_thread = threading.Thread(target=_wbduc2_nominal_sample_rate_probe)
        _wbduc2_nominal_sample_rate_thread.daemon = True
        _wbduc2_nominal_sample_rate_thread.start()
        def _wbduc1_nominal_sample_rate_probe():
        	while True:
        		val = self.CyberRadio_NDR651_sink_0.get_wbduc_nominal_sample_rate(1)
        		try: self.set_wbduc1_nominal_sample_rate(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(2))
        _wbduc1_nominal_sample_rate_thread = threading.Thread(target=_wbduc1_nominal_sample_rate_probe)
        _wbduc1_nominal_sample_rate_thread.daemon = True
        _wbduc1_nominal_sample_rate_thread.start()
        self.blocks_file_descriptor_sink_1 = blocks.file_descriptor_sink(gr.sizeof_char*1, 2)
        self.analog_sig_source_x_1 = analog.sig_source_c(wbduc2_nominal_sample_rate, analog.GR_SQR_WAVE, 1e6, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(wbduc1_nominal_sample_rate, analog.GR_SQR_WAVE, 1e6, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.CyberRadio_NDR651_sink_0, 0), (self.blocks_file_descriptor_sink_1, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.CyberRadio_NDR651_sink_0, 0))    
        self.connect((self.analog_sig_source_x_1, 0), (self.CyberRadio_NDR651_sink_0, 1))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ndr651_sink_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_wbduc2_stream(self):
        return self.wbduc2_stream

    def set_wbduc2_stream(self, wbduc2_stream):
        self.wbduc2_stream = wbduc2_stream
        Qt.QMetaObject.invokeMethod(self._wbduc2_stream_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc2_stream)))
        self.CyberRadio_NDR651_sink_0.set_wbduc2_param_list([self.wbduc2_iface, self.wbduc2_rate, self.wbduc2_freq, self.wbduc2_atten, self.wbduc2_chans, self.wbduc2_stream])

    def get_wbduc2_rate(self):
        return self.wbduc2_rate

    def set_wbduc2_rate(self, wbduc2_rate):
        self.wbduc2_rate = wbduc2_rate
        Qt.QMetaObject.invokeMethod(self._wbduc2_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc2_rate)))
        self.CyberRadio_NDR651_sink_0.set_wbduc2_param_list([self.wbduc2_iface, self.wbduc2_rate, self.wbduc2_freq, self.wbduc2_atten, self.wbduc2_chans, self.wbduc2_stream])

    def get_wbduc2_nominal_sample_rate(self):
        return self.wbduc2_nominal_sample_rate

    def set_wbduc2_nominal_sample_rate(self, wbduc2_nominal_sample_rate):
        self.wbduc2_nominal_sample_rate = wbduc2_nominal_sample_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.wbduc2_nominal_sample_rate)

    def get_wbduc2_iface(self):
        return self.wbduc2_iface

    def set_wbduc2_iface(self, wbduc2_iface):
        self.wbduc2_iface = wbduc2_iface
        Qt.QMetaObject.invokeMethod(self._wbduc2_iface_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc2_iface)))
        self.CyberRadio_NDR651_sink_0.set_wbduc2_param_list([self.wbduc2_iface, self.wbduc2_rate, self.wbduc2_freq, self.wbduc2_atten, self.wbduc2_chans, self.wbduc2_stream])

    def get_wbduc2_freq(self):
        return self.wbduc2_freq

    def set_wbduc2_freq(self, wbduc2_freq):
        self.wbduc2_freq = wbduc2_freq
        Qt.QMetaObject.invokeMethod(self._wbduc2_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc2_freq)))
        self.CyberRadio_NDR651_sink_0.set_wbduc2_param_list([self.wbduc2_iface, self.wbduc2_rate, self.wbduc2_freq, self.wbduc2_atten, self.wbduc2_chans, self.wbduc2_stream])

    def get_wbduc2_chans(self):
        return self.wbduc2_chans

    def set_wbduc2_chans(self, wbduc2_chans):
        self.wbduc2_chans = wbduc2_chans
        Qt.QMetaObject.invokeMethod(self._wbduc2_chans_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc2_chans)))
        self.CyberRadio_NDR651_sink_0.set_wbduc2_param_list([self.wbduc2_iface, self.wbduc2_rate, self.wbduc2_freq, self.wbduc2_atten, self.wbduc2_chans, self.wbduc2_stream])

    def get_wbduc2_atten(self):
        return self.wbduc2_atten

    def set_wbduc2_atten(self, wbduc2_atten):
        self.wbduc2_atten = wbduc2_atten
        Qt.QMetaObject.invokeMethod(self._wbduc2_atten_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc2_atten)))
        self.CyberRadio_NDR651_sink_0.set_wbduc2_param_list([self.wbduc2_iface, self.wbduc2_rate, self.wbduc2_freq, self.wbduc2_atten, self.wbduc2_chans, self.wbduc2_stream])

    def get_wbduc1_stream(self):
        return self.wbduc1_stream

    def set_wbduc1_stream(self, wbduc1_stream):
        self.wbduc1_stream = wbduc1_stream
        Qt.QMetaObject.invokeMethod(self._wbduc1_stream_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc1_stream)))
        self.CyberRadio_NDR651_sink_0.set_wbduc1_param_list([self.wbduc1_iface, self.wbduc1_rate, self.wbduc1_freq, self.wbduc1_atten, self.wbduc1_chans, self.wbduc1_stream])

    def get_wbduc1_rate(self):
        return self.wbduc1_rate

    def set_wbduc1_rate(self, wbduc1_rate):
        self.wbduc1_rate = wbduc1_rate
        Qt.QMetaObject.invokeMethod(self._wbduc1_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc1_rate)))
        self.CyberRadio_NDR651_sink_0.set_wbduc1_param_list([self.wbduc1_iface, self.wbduc1_rate, self.wbduc1_freq, self.wbduc1_atten, self.wbduc1_chans, self.wbduc1_stream])

    def get_wbduc1_nominal_sample_rate(self):
        return self.wbduc1_nominal_sample_rate

    def set_wbduc1_nominal_sample_rate(self, wbduc1_nominal_sample_rate):
        self.wbduc1_nominal_sample_rate = wbduc1_nominal_sample_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.wbduc1_nominal_sample_rate)

    def get_wbduc1_iface(self):
        return self.wbduc1_iface

    def set_wbduc1_iface(self, wbduc1_iface):
        self.wbduc1_iface = wbduc1_iface
        Qt.QMetaObject.invokeMethod(self._wbduc1_iface_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc1_iface)))
        self.CyberRadio_NDR651_sink_0.set_wbduc1_param_list([self.wbduc1_iface, self.wbduc1_rate, self.wbduc1_freq, self.wbduc1_atten, self.wbduc1_chans, self.wbduc1_stream])

    def get_wbduc1_freq(self):
        return self.wbduc1_freq

    def set_wbduc1_freq(self, wbduc1_freq):
        self.wbduc1_freq = wbduc1_freq
        Qt.QMetaObject.invokeMethod(self._wbduc1_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc1_freq)))
        self.CyberRadio_NDR651_sink_0.set_wbduc1_param_list([self.wbduc1_iface, self.wbduc1_rate, self.wbduc1_freq, self.wbduc1_atten, self.wbduc1_chans, self.wbduc1_stream])

    def get_wbduc1_chans(self):
        return self.wbduc1_chans

    def set_wbduc1_chans(self, wbduc1_chans):
        self.wbduc1_chans = wbduc1_chans
        Qt.QMetaObject.invokeMethod(self._wbduc1_chans_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc1_chans)))
        self.CyberRadio_NDR651_sink_0.set_wbduc1_param_list([self.wbduc1_iface, self.wbduc1_rate, self.wbduc1_freq, self.wbduc1_atten, self.wbduc1_chans, self.wbduc1_stream])

    def get_wbduc1_atten(self):
        return self.wbduc1_atten

    def set_wbduc1_atten(self, wbduc1_atten):
        self.wbduc1_atten = wbduc1_atten
        Qt.QMetaObject.invokeMethod(self._wbduc1_atten_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbduc1_atten)))
        self.CyberRadio_NDR651_sink_0.set_wbduc1_param_list([self.wbduc1_iface, self.wbduc1_rate, self.wbduc1_freq, self.wbduc1_atten, self.wbduc1_chans, self.wbduc1_stream])

    def get_tx2_freq(self):
        return self.tx2_freq

    def set_tx2_freq(self, tx2_freq):
        self.tx2_freq = tx2_freq
        Qt.QMetaObject.invokeMethod(self._tx2_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx2_freq)))
        self.CyberRadio_NDR651_sink_0.set_transmitter2_param_list([self.tx2_enable, self.tx2_freq, self.tx2_atten])

    def get_tx2_enable(self):
        return self.tx2_enable

    def set_tx2_enable(self, tx2_enable):
        self.tx2_enable = tx2_enable
        self._tx2_enable_callback(self.tx2_enable)
        self.CyberRadio_NDR651_sink_0.set_transmitter2_param_list([self.tx2_enable, self.tx2_freq, self.tx2_atten])

    def get_tx2_atten(self):
        return self.tx2_atten

    def set_tx2_atten(self, tx2_atten):
        self.tx2_atten = tx2_atten
        Qt.QMetaObject.invokeMethod(self._tx2_atten_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx2_atten)))
        self.CyberRadio_NDR651_sink_0.set_transmitter2_param_list([self.tx2_enable, self.tx2_freq, self.tx2_atten])

    def get_tx1_freq(self):
        return self.tx1_freq

    def set_tx1_freq(self, tx1_freq):
        self.tx1_freq = tx1_freq
        Qt.QMetaObject.invokeMethod(self._tx1_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx1_freq)))
        self.CyberRadio_NDR651_sink_0.set_transmitter1_param_list([self.tx1_enable, self.tx1_freq, self.tx1_atten])

    def get_tx1_enable(self):
        return self.tx1_enable

    def set_tx1_enable(self, tx1_enable):
        self.tx1_enable = tx1_enable
        self._tx1_enable_callback(self.tx1_enable)
        self.CyberRadio_NDR651_sink_0.set_transmitter1_param_list([self.tx1_enable, self.tx1_freq, self.tx1_atten])

    def get_tx1_atten(self):
        return self.tx1_atten

    def set_tx1_atten(self, tx1_atten):
        self.tx1_atten = tx1_atten
        Qt.QMetaObject.invokeMethod(self._tx1_atten_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx1_atten)))
        self.CyberRadio_NDR651_sink_0.set_transmitter1_param_list([self.tx1_enable, self.tx1_freq, self.tx1_atten])


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = ndr651_sink_demo()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None  # to clean up Qt widgets
