#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
from gnuradio import audio
from gnuradio import blocks

class safe_audio_sink(gr.hier_block2):
    """
    docstring for block safe_audio_sink
    """
    def __init__(self, device_name="", samp_rate=4e3, ok_to_block=False):
        gr.hier_block2.__init__(
                                    self, "Audio Failsafe Block",
                                    gr.io_signature(1, 1, gr.sizeof_float*1),
                                    gr.io_signature(0, 0, 0),
                                )
        self.device_name = str(device_name) if device_name is not None else ""
        self.ok_to_block = bool(ok_to_block)
        self.samp_rate = int(samp_rate)
        try:
            print("Using a sample rate of ",self.samp_rate)
            self.audioSink = audio.sink(self.samp_rate, self.device_name, self.ok_to_block)
        except:
            self.audioSink = None
            traceback.print_exc()
            print("Falling back to null sink!")
            self.audioSink = blocks.null_sink(gr.sizeof_float*1)
        self.connect((self, 0), (self.audioSink, 0))
