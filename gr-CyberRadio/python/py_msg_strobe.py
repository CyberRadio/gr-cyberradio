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

import numpy
from gnuradio import gr
import threading, time, traceback
from gnuradio.gr import pmt
#~ from gnuradio.eng_notation import num_to_str, str_to_num

class py_msg_strobe(gr.basic_block):
    """
    docstring for block py_msg_strobe
    """
    
    def __init__(self, value=None, rate=1.0):
        gr.basic_block.__init__(self,
            name="py_msg_strobe",
            in_sig=None,
            out_sig=None,)
        self.init = True
        self.value = None
        self.msgOut = None
        self.rate = 0.0
        self.interval = 0.0
        
        print("py_msg_strobe.__init__".center(80,"~"))
        self.inPortName = pmt.intern("msg")
        self.message_port_register_in(self.inPortName)
        self.set_msg_handler(self.inPortName, self.msgRx)
        self.outPortName = pmt.intern("msg")
        self.message_port_register_out(self.outPortName)
        
        self.setValue(value)
        self.setRate(rate)
        
        self.thread = threading.Thread(target=self.msgTxLoop)
        self.thread.daemon = True
        self.thread.start()
        self.init = False
    
    def setValue(self, value):
        if value != self.value:
            print("py_msg_strobe.setValue".center(80,"~"))
            print("Current:",type(self.value),repr(self.value))
            print("    New:",type(value),repr(value))#, end=' ')
            self.value = value
            if type(self.value) in (str,float,int,bool):
                if type(self.value) is float:
                    valueStr = "float(%s)"%self.value
                elif type(self.value) is int:
                    valueStr = "int(%s)"%self.value
                else:
                    valueStr = repr(self.value)
                self.msgOut = pmt.make_u8vector( len(valueStr), ord("\n") )
                for i,j in enumerate(valueStr):
                    pmt.u8vector_set(self.msgOut,i,ord(j))
            else:
                self.msgOut = None
            self.msgTx()
    
    def getValue(self,):
        #~ print "py_msg_strobe.getValue".center(80,"~")
        #~ print type(self.value),repr(self.value)
        return self.value
    
    def setRate(self, rate):
        if rate != self.rate:
            print("py_msg_strobe.setRate".center(80,"~"))
            print("Current:",self.rate)
            print("    New:",rate)
            self.rate = float(rate)
            if self.rate>0:
                self.interval = 1.0/self.rate
            else:
                self.interval = 0.0
    
    def msgRx(self, msg):
        try:
            #~ print "py_msg_strobe.msgRx".center(80,"~")
            pyMsg = pmt.to_python(msg)
            #~ print type(pyMsg),repr(pyMsg)
            try:
                content = pyMsg[-1].tostring()
                #~ print repr(content)
                self.value = eval(content.strip())
            except:
                traceback.print_exc()
                self.value = None
        except:
            traceback.print_exc()
    
    def msgTx(self,):
        #~ print "py_msg_strobe.msgTx".center(80,"~")
        try:
            if self.msgOut is not None:
                #~ print "repr(msgOut):",repr(msgOut)
                self.message_port_pub(self.outPortName, pmt.cons(pmt.PMT_NIL, self.msgOut))
        except:
            traceback.print_exc()
    
    def msgTxLoop(self):
        while self.interval>0.0:
            #~ print "py_msg_strobe.msgTxLoop".center(80,"~")
            self.msgTx()
            time.sleep(self.interval)

    def work(self, input_items, output_items):
#        out = output_items[0]
#        # <+signal processing here+>
#        out[:] = whatever
        return len(output_items[0])
