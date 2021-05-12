#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

import CyberRadioDriver as crd
from .generic_radio_control_block import generic_radio_control_block

class generic_ndr_command_block(generic_radio_control_block):
    """
    docstring for block generic_ndr_command_block
    """
    
    def __init__(self, radioObj, cmd, debug):
        self._init = True
        self._name = "NDR_CMD"
        self._debug = debug
        
        generic_radio_control_block.__init__(self, radioObj=radioObj, otherArgs={}, debug=debug)
        
        if cmd:
            self.send_command(cmd)
        else:
            self.rsp = ""
        self._init = False


    ## Setter & getter for radioParam
    def set_radioParam(self, radioParam={"type":"ndr308","host":"ndr308","port":8617,"obj":None}):
        if self._init or not hasattr(self, "radioParam"):
            self.radioParam = radioParam
            self.radioType = self.radioParam.get("type")
            self.log.debug("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
        elif radioParam!=self.radioParam:
            self.log.debug("%s.set_radioParam: %s -> %s"%(self._name, repr(self.radioParam), repr(radioParam),))
            self.radioParam = radioParam
            self.updateConfig("radioParam")

    def get_radioParam(self,):
        return self.radioParam

    def send_command(self,cmdString):
        if cmdString is not None:
            cmd = cmdString.strip()+"\n"
            rsp = self.radioObj.sendCommand(cmd)
            self.rsp = "; ".join(rsp)
            for line in rsp:
                self.log.debug("CMD = %r & RSP = %r"%(repr(cmd), repr(line),))
            return self.rsp

    def get_response(self,):
        return self.rsp if self.rsp is not None else ""
