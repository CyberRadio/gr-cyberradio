#!/usr/bin/env python

import time, traceback
import CyberRadioDriver as crd

radio = crd.getRadioObject("ndr651", verbose=False)
radio.connect("tcp", "ndr651", 8617)
lastRsp = {}
while True:
	for chan in (1,):
		for i in ("TXP?", "TXF?", "TXA?", "DUC?"):
			cmd = "%s %d"%(i, chan)
			if not lastRsp.has_key(cmd):
				lastRsp[cmd] = ""
			rsp = "; ".join( radio.sendCommand(cmd+"\n") )
			if lastRsp[cmd]!=rsp:
				print "%10s | %10s | %s"%(time.strftime("%X"), cmd, rsp)
				lastRsp[cmd] = rsp
			time.sleep(0.05)
