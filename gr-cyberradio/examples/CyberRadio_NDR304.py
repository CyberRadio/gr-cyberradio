#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: NDR304 Example
# Author: CyberRadio
# Description: Example flowgraph featuring the NDR304 Source block
# Generated: Thu Sep 10 13:09:05 2015
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

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import CyberRadio
import threading
import time
import wx


class CyberRadio_NDR304(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="NDR304 Example")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.wbddc1_tuner_freq_mhz = wbddc1_tuner_freq_mhz = 900
        self.wbddc1_nominal_sample_rate = wbddc1_nominal_sample_rate = 32000
        self.wbddc1_ddc_offset = wbddc1_ddc_offset = 0

        ##################################################
        # Blocks
        ##################################################
        self._wbddc1_tuner_freq_mhz_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.wbddc1_tuner_freq_mhz,
        	callback=self.set_wbddc1_tuner_freq_mhz,
        	label="WBDDC 1 Tuner Frequency (MHz)",
        	converter=forms.int_converter(),
        )
        self.Add(self._wbddc1_tuner_freq_mhz_text_box)
        self._wbddc1_ddc_offset_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.wbddc1_ddc_offset,
        	callback=self.set_wbddc1_ddc_offset,
        	label="WBDDC 1 Frequency Offset (Hz)",
        	converter=forms.float_converter(),
        )
        self.Add(self._wbddc1_ddc_offset_text_box)
        self.CyberRadio_NDR304_source_0 = CyberRadio.NDR304_source(
            verbose_mode=True,
            radio_device_name="/dev/ndr47x",
            radio_baud_rate=921600,
            gig_iface_to_use="eth0",
            num_tuners=1,
            tuner1_param_list=[True, wbddc1_tuner_freq_mhz * 1e6, 0],
            num_wbddcs=1,
            wbddc1_param_list=[40001, 0, 0, True, wbddc1_ddc_offset],
            tagged=True,
        )
        def _wbddc1_nominal_sample_rate_probe():
        	while True:
        		val = self.CyberRadio_NDR304_source_0.get_wbddc_nominal_sample_rate(1)
        		try: self.set_wbddc1_nominal_sample_rate(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(10))
        _wbddc1_nominal_sample_rate_thread = threading.Thread(target=_wbddc1_nominal_sample_rate_probe)
        _wbddc1_nominal_sample_rate_thread.daemon = True
        _wbddc1_nominal_sample_rate_thread.start()
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=wbddc1_tuner_freq_mhz * 1e6 + wbddc1_ddc_offset,
        	y_per_div=10,
        	y_divs=12,
        	ref_level=0,
        	ref_scale=2,
        	sample_rate=wbddc1_nominal_sample_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.blocks_file_descriptor_sink_0 = blocks.file_descriptor_sink(gr.sizeof_char*1, 2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.CyberRadio_NDR304_source_0, 0), (self.blocks_file_descriptor_sink_0, 0))    
        self.connect((self.CyberRadio_NDR304_source_0, 1), (self.wxgui_fftsink2_0, 0))    


    def get_wbddc1_tuner_freq_mhz(self):
        return self.wbddc1_tuner_freq_mhz

    def set_wbddc1_tuner_freq_mhz(self, wbddc1_tuner_freq_mhz):
        self.wbddc1_tuner_freq_mhz = wbddc1_tuner_freq_mhz
        self._wbddc1_tuner_freq_mhz_text_box.set_value(self.wbddc1_tuner_freq_mhz)
        self.CyberRadio_NDR304_source_0.set_tuner1_param_list([True, self.wbddc1_tuner_freq_mhz * 1e6, 0])
        self.wxgui_fftsink2_0.set_baseband_freq(self.wbddc1_tuner_freq_mhz * 1e6 + self.wbddc1_ddc_offset)

    def get_wbddc1_nominal_sample_rate(self):
        return self.wbddc1_nominal_sample_rate

    def set_wbddc1_nominal_sample_rate(self, wbddc1_nominal_sample_rate):
        self.wbddc1_nominal_sample_rate = wbddc1_nominal_sample_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.wbddc1_nominal_sample_rate)

    def get_wbddc1_ddc_offset(self):
        return self.wbddc1_ddc_offset

    def set_wbddc1_ddc_offset(self, wbddc1_ddc_offset):
        self.wbddc1_ddc_offset = wbddc1_ddc_offset
        self._wbddc1_ddc_offset_text_box.set_value(self.wbddc1_ddc_offset)
        self.CyberRadio_NDR304_source_0.set_wbddc1_param_list([40001, 0, 0, True, self.wbddc1_ddc_offset])
        self.wxgui_fftsink2_0.set_baseband_freq(self.wbddc1_tuner_freq_mhz * 1e6 + self.wbddc1_ddc_offset)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    tb = CyberRadio_NDR304()
    tb.Start(True)
    tb.Wait()
