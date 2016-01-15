#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: NDR651 Source Demo
# Author: CRS
# Description: CRS NDR651 Source Demo
# Generated: Tue Oct 27 15:50:20 2015
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
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import CyberRadio
import sip
import sys
import threading
import time


class CyberRadio_NDR651_source(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NDR651 Source Demo")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NDR651 Source Demo")
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

        self.settings = Qt.QSettings("GNU Radio", "CyberRadio_NDR651_source")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.wbddc2_rate = wbddc2_rate = 0
        self.wbddc2_nominal_sample_rate = wbddc2_nominal_sample_rate = 32000
        self.wbddc2_enable = wbddc2_enable = True
        self.wbddc1_rate = wbddc1_rate = 0
        self.wbddc1_nominal_sample_rate = wbddc1_nominal_sample_rate = 32000
        self.wbddc1_enable = wbddc1_enable = True
        self.tuner2_freq = tuner2_freq = 900
        self.tuner2_enable = tuner2_enable = True
        self.tuner2_atten = tuner2_atten = 0
        self.tuner1_freq = tuner1_freq = 900
        self.tuner1_enable = tuner1_enable = True
        self.tuner1_atten = tuner1_atten = 0

        ##################################################
        # Blocks
        ##################################################
        self._wbddc2_rate_tool_bar = Qt.QToolBar(self)
        self._wbddc2_rate_tool_bar.addWidget(Qt.QLabel("WBDDC 2: Rate"+": "))
        self._wbddc2_rate_line_edit = Qt.QLineEdit(str(self.wbddc2_rate))
        self._wbddc2_rate_tool_bar.addWidget(self._wbddc2_rate_line_edit)
        self._wbddc2_rate_line_edit.returnPressed.connect(
        	lambda: self.set_wbddc2_rate(int(str(self._wbddc2_rate_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbddc2_rate_tool_bar, 3, 0, 1, 1)
        _wbddc2_enable_check_box = Qt.QCheckBox("Enabled")
        self._wbddc2_enable_choices = {True: True, False: False}
        self._wbddc2_enable_choices_inv = dict((v,k) for k,v in self._wbddc2_enable_choices.iteritems())
        self._wbddc2_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_wbddc2_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._wbddc2_enable_choices_inv[i]))
        self._wbddc2_enable_callback(self.wbddc2_enable)
        _wbddc2_enable_check_box.stateChanged.connect(lambda i: self.set_wbddc2_enable(self._wbddc2_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_wbddc2_enable_check_box, 3, 1, 1, 1)
        self._wbddc1_rate_tool_bar = Qt.QToolBar(self)
        self._wbddc1_rate_tool_bar.addWidget(Qt.QLabel("WBDDC 1: Rate"+": "))
        self._wbddc1_rate_line_edit = Qt.QLineEdit(str(self.wbddc1_rate))
        self._wbddc1_rate_tool_bar.addWidget(self._wbddc1_rate_line_edit)
        self._wbddc1_rate_line_edit.returnPressed.connect(
        	lambda: self.set_wbddc1_rate(int(str(self._wbddc1_rate_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._wbddc1_rate_tool_bar, 2, 0, 1, 1)
        _wbddc1_enable_check_box = Qt.QCheckBox("Enabled")
        self._wbddc1_enable_choices = {True: True, False: False}
        self._wbddc1_enable_choices_inv = dict((v,k) for k,v in self._wbddc1_enable_choices.iteritems())
        self._wbddc1_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_wbddc1_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._wbddc1_enable_choices_inv[i]))
        self._wbddc1_enable_callback(self.wbddc1_enable)
        _wbddc1_enable_check_box.stateChanged.connect(lambda i: self.set_wbddc1_enable(self._wbddc1_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_wbddc1_enable_check_box, 2, 1, 1, 1)
        self._tuner2_freq_tool_bar = Qt.QToolBar(self)
        self._tuner2_freq_tool_bar.addWidget(Qt.QLabel("Freq"+": "))
        self._tuner2_freq_line_edit = Qt.QLineEdit(str(self.tuner2_freq))
        self._tuner2_freq_tool_bar.addWidget(self._tuner2_freq_line_edit)
        self._tuner2_freq_line_edit.returnPressed.connect(
        	lambda: self.set_tuner2_freq(int(str(self._tuner2_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tuner2_freq_tool_bar, 1, 1, 1, 1)
        _tuner2_enable_check_box = Qt.QCheckBox("Tuner 2: Enable")
        self._tuner2_enable_choices = {True: True, False: False}
        self._tuner2_enable_choices_inv = dict((v,k) for k,v in self._tuner2_enable_choices.iteritems())
        self._tuner2_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_tuner2_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._tuner2_enable_choices_inv[i]))
        self._tuner2_enable_callback(self.tuner2_enable)
        _tuner2_enable_check_box.stateChanged.connect(lambda i: self.set_tuner2_enable(self._tuner2_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_tuner2_enable_check_box, 1, 0, 1, 1)
        self._tuner2_atten_tool_bar = Qt.QToolBar(self)
        self._tuner2_atten_tool_bar.addWidget(Qt.QLabel("Atten"+": "))
        self._tuner2_atten_line_edit = Qt.QLineEdit(str(self.tuner2_atten))
        self._tuner2_atten_tool_bar.addWidget(self._tuner2_atten_line_edit)
        self._tuner2_atten_line_edit.returnPressed.connect(
        	lambda: self.set_tuner2_atten(int(str(self._tuner2_atten_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tuner2_atten_tool_bar, 1, 2, 1, 1)
        self._tuner1_freq_tool_bar = Qt.QToolBar(self)
        self._tuner1_freq_tool_bar.addWidget(Qt.QLabel("Freq"+": "))
        self._tuner1_freq_line_edit = Qt.QLineEdit(str(self.tuner1_freq))
        self._tuner1_freq_tool_bar.addWidget(self._tuner1_freq_line_edit)
        self._tuner1_freq_line_edit.returnPressed.connect(
        	lambda: self.set_tuner1_freq(int(str(self._tuner1_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tuner1_freq_tool_bar, 0, 1, 1, 1)
        _tuner1_enable_check_box = Qt.QCheckBox("Tuner 1: Enable")
        self._tuner1_enable_choices = {True: True, False: False}
        self._tuner1_enable_choices_inv = dict((v,k) for k,v in self._tuner1_enable_choices.iteritems())
        self._tuner1_enable_callback = lambda i: Qt.QMetaObject.invokeMethod(_tuner1_enable_check_box, "setChecked", Qt.Q_ARG("bool", self._tuner1_enable_choices_inv[i]))
        self._tuner1_enable_callback(self.tuner1_enable)
        _tuner1_enable_check_box.stateChanged.connect(lambda i: self.set_tuner1_enable(self._tuner1_enable_choices[bool(i)]))
        self.top_grid_layout.addWidget(_tuner1_enable_check_box, 0, 0, 1, 1)
        self._tuner1_atten_tool_bar = Qt.QToolBar(self)
        self._tuner1_atten_tool_bar.addWidget(Qt.QLabel("Atten"+": "))
        self._tuner1_atten_line_edit = Qt.QLineEdit(str(self.tuner1_atten))
        self._tuner1_atten_tool_bar.addWidget(self._tuner1_atten_line_edit)
        self._tuner1_atten_line_edit.returnPressed.connect(
        	lambda: self.set_tuner1_atten(int(str(self._tuner1_atten_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tuner1_atten_tool_bar, 0, 2, 1, 1)
        self.CyberRadio_NDR651_source_0 = CyberRadio.NDR651_source(
            verbose_mode=True,
            radio_host_name="ndr651",
            radio_host_port=8617,
            tengig_iface_list=['eth10', 'eth11'],
            num_tuners=2,
            tuner1_param_list=[tuner1_enable, tuner1_freq * 1e6, tuner1_atten],
            tuner2_param_list=[tuner2_enable, tuner2_freq * 1e6, tuner2_atten],
            num_wbddcs=2,
            wbddc1_param_list=["eth10", 40001, 1, wbddc1_rate, wbddc1_enable],
            wbddc2_param_list=["eth10", 40002, 1, wbddc2_rate, wbddc2_enable],
            num_nbddcs=1,
            nbddc1_param_list=["eth10", 41001, 0, 0, False, 0.0],
            tagged=False,
            debug=False,
        )
        def _wbddc1_nominal_sample_rate_probe():
        	while True:
        		val = self.CyberRadio_NDR651_source_0.get_wbddc_nominal_sample_rate(1)
        		try: self.set_wbddc1_nominal_sample_rate(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(2))
        _wbddc1_nominal_sample_rate_thread = threading.Thread(target=_wbddc1_nominal_sample_rate_probe)
        _wbddc1_nominal_sample_rate_thread.daemon = True
        _wbddc1_nominal_sample_rate_thread.start()
        def _wbddc2_nominal_sample_rate_probe():
        	while True:
        		val = self.CyberRadio_NDR651_source_0.get_wbddc_nominal_sample_rate(2)
        		try: self.set_wbddc2_nominal_sample_rate(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(2))
        _wbddc2_nominal_sample_rate_thread = threading.Thread(target=_wbddc2_nominal_sample_rate_probe)
        _wbddc2_nominal_sample_rate_thread.daemon = True
        _wbddc2_nominal_sample_rate_thread.start()
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	900e6, #fc
        	wbddc1_nominal_sample_rate, #bw
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["WBDDC 1", "WBDDC 2", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_file_descriptor_sink_0 = blocks.file_descriptor_sink(gr.sizeof_char*1, 2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.CyberRadio_NDR651_source_0, 0), (self.blocks_file_descriptor_sink_0, 0))    
        self.connect((self.CyberRadio_NDR651_source_0, 1), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.CyberRadio_NDR651_source_0, 2), (self.qtgui_freq_sink_x_0, 1))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "CyberRadio_NDR651_source")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_wbddc2_rate(self):
        return self.wbddc2_rate

    def set_wbddc2_rate(self, wbddc2_rate):
        self.wbddc2_rate = wbddc2_rate
        Qt.QMetaObject.invokeMethod(self._wbddc2_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbddc2_rate)))
        self.CyberRadio_NDR651_source_0.set_wbddc2_param_list(["eth10", 40002, 1, self.wbddc2_rate, self.wbddc2_enable])

    def get_wbddc2_nominal_sample_rate(self):
        return self.wbddc2_nominal_sample_rate

    def set_wbddc2_nominal_sample_rate(self, wbddc2_nominal_sample_rate):
        self.wbddc2_nominal_sample_rate = wbddc2_nominal_sample_rate

    def get_wbddc2_enable(self):
        return self.wbddc2_enable

    def set_wbddc2_enable(self, wbddc2_enable):
        self.wbddc2_enable = wbddc2_enable
        self._wbddc2_enable_callback(self.wbddc2_enable)
        self.CyberRadio_NDR651_source_0.set_wbddc2_param_list(["eth10", 40002, 1, self.wbddc2_rate, self.wbddc2_enable])

    def get_wbddc1_rate(self):
        return self.wbddc1_rate

    def set_wbddc1_rate(self, wbddc1_rate):
        self.wbddc1_rate = wbddc1_rate
        Qt.QMetaObject.invokeMethod(self._wbddc1_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.wbddc1_rate)))
        self.CyberRadio_NDR651_source_0.set_wbddc1_param_list(["eth10", 40001, 1, self.wbddc1_rate, self.wbddc1_enable])

    def get_wbddc1_nominal_sample_rate(self):
        return self.wbddc1_nominal_sample_rate

    def set_wbddc1_nominal_sample_rate(self, wbddc1_nominal_sample_rate):
        self.wbddc1_nominal_sample_rate = wbddc1_nominal_sample_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(900e6, self.wbddc1_nominal_sample_rate)

    def get_wbddc1_enable(self):
        return self.wbddc1_enable

    def set_wbddc1_enable(self, wbddc1_enable):
        self.wbddc1_enable = wbddc1_enable
        self._wbddc1_enable_callback(self.wbddc1_enable)
        self.CyberRadio_NDR651_source_0.set_wbddc1_param_list(["eth10", 40001, 1, self.wbddc1_rate, self.wbddc1_enable])

    def get_tuner2_freq(self):
        return self.tuner2_freq

    def set_tuner2_freq(self, tuner2_freq):
        self.tuner2_freq = tuner2_freq
        Qt.QMetaObject.invokeMethod(self._tuner2_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.tuner2_freq)))
        self.CyberRadio_NDR651_source_0.set_tuner2_param_list([self.tuner2_enable, self.tuner2_freq * 1e6, self.tuner2_atten])

    def get_tuner2_enable(self):
        return self.tuner2_enable

    def set_tuner2_enable(self, tuner2_enable):
        self.tuner2_enable = tuner2_enable
        self._tuner2_enable_callback(self.tuner2_enable)
        self.CyberRadio_NDR651_source_0.set_tuner2_param_list([self.tuner2_enable, self.tuner2_freq * 1e6, self.tuner2_atten])

    def get_tuner2_atten(self):
        return self.tuner2_atten

    def set_tuner2_atten(self, tuner2_atten):
        self.tuner2_atten = tuner2_atten
        Qt.QMetaObject.invokeMethod(self._tuner2_atten_line_edit, "setText", Qt.Q_ARG("QString", str(self.tuner2_atten)))
        self.CyberRadio_NDR651_source_0.set_tuner2_param_list([self.tuner2_enable, self.tuner2_freq * 1e6, self.tuner2_atten])

    def get_tuner1_freq(self):
        return self.tuner1_freq

    def set_tuner1_freq(self, tuner1_freq):
        self.tuner1_freq = tuner1_freq
        Qt.QMetaObject.invokeMethod(self._tuner1_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.tuner1_freq)))
        self.CyberRadio_NDR651_source_0.set_tuner1_param_list([self.tuner1_enable, self.tuner1_freq * 1e6, self.tuner1_atten])

    def get_tuner1_enable(self):
        return self.tuner1_enable

    def set_tuner1_enable(self, tuner1_enable):
        self.tuner1_enable = tuner1_enable
        self._tuner1_enable_callback(self.tuner1_enable)
        self.CyberRadio_NDR651_source_0.set_tuner1_param_list([self.tuner1_enable, self.tuner1_freq * 1e6, self.tuner1_atten])

    def get_tuner1_atten(self):
        return self.tuner1_atten

    def set_tuner1_atten(self, tuner1_atten):
        self.tuner1_atten = tuner1_atten
        Qt.QMetaObject.invokeMethod(self._tuner1_atten_line_edit, "setText", Qt.Q_ARG("QString", str(self.tuner1_atten)))
        self.CyberRadio_NDR651_source_0.set_tuner1_param_list([self.tuner1_enable, self.tuner1_freq * 1e6, self.tuner1_atten])


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = CyberRadio_NDR651_source()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None  # to clean up Qt widgets
