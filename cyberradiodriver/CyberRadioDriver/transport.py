#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.transport
# 
# Provides classes that define communication transports.
#
# \author NH
# \author DA
# \copyright Copyright (c) 2014 CyberRadio Solutions, Inc.  All rights 
# reserved.
#
###############################################################

import socket, select, serial, traceback, time, sys
import command, log
from time import gmtime, strftime
import datetime

##
# Radio transport class.
#
# A radio transport object manages sending information to a given
# destination and collecting the information it gets back.  
#
class radio_transport(log._logger):
	_name = "transportXXX"
	## Default timeout value for transactions managed over this transport.
	defaultTimeout = 1.0
	## Default port used for TCP and UDP connections
	defaultPort = 8617
	## Default baud rate used for TTY connections
	defaultBaudrate = 921600
	
	##
	# Constructs a radio transport object.
	#
	# \param parent The parent object that manages this transport.
	# \param verbose Verbose mode (Boolean)
	# \param logCtrl A GUI control that receives log output (GUI-dependent)
	# \param json Whether the transport should expect JSON-formatted commands
	#    and responses (Boolean).
	# \param logFile An open file or file-like object to be used for log output.  
	#	If not provided, this defaults to standard output. 
	def __init__(self,parent,verbose=False,logCtrl=None,json=False, 
				 logFile=sys.stdout):
		'''
		Constructor
		'''
		# Base-class constructor consumes "verbose" and "logFile"
		# keyword arguments
		log._logger.__init__(self, verbose=verbose, logFile=logFile)
		self.parent = parent
		self.tcp = None
		self.tty = None
		self.udp = None
		self.fd = None
		self.logCtrl = logCtrl
		self.selectInput = []
		self.connected = False
		self.lastTime = datetime.datetime.now()
		self.lastTx = 0
		self.lastRx = 0
		if json:
			self.rxFunction = self.receiveJson
		else:
			self.rxFunction = self.receiveCli
		self.connectError = ""
	
	##
	# \internal
	# Perform actions on object being deleted.
	def __del__(self,):
		self.disconnect()
	
	##
	# \internal
	# Define this object's string representation.
	def __str__(self):
		return self._name
	
	##
	# Connects the transport and tests the connection.
	#
	# \param mode One of "tty", "tcp", or "udp".
	# \param host_or_dev If mode is "tcp" or "udp", this parameter is the 
	#     hostname for the remote device.  If mode is "tty", this parameter is the
	#     name of the TTY device on the system.
	# \param port_or_baudrate If mode is "tcp" or "udp", this parameter is the 
	#     port for the remote device.  If mode is "tty", this parameter is the
	#     baud rate of the TTY device on the system.
	# \return True if connection was successful, False otherwise.
	def connect(self,mode,host_or_dev,port_or_baudrate):
		mode = str(mode).strip().lower()
		self.log("Connecting (%s,%s,%s)..."%(repr(mode),repr(host_or_dev),repr(port_or_baudrate)))
		if mode in ("tcp","tty","udp"):
			if self.connected:
				self.disconnect()
			if mode == "tcp":
				self.connectTcp(str(host_or_dev),int(port_or_baudrate) if port_or_baudrate is not None else self.defaultPort,)
			elif mode == "udp":
				self.connectUdp(str(host_or_dev),int(port_or_baudrate) if port_or_baudrate is not None else self.defaultPort,)
			elif mode == "tty":
				self.connectTty(str(host_or_dev),int(port_or_baudrate) if port_or_baudrate is not None else self.defaultBaudrate,)
		if mode in ("tcp","tty",):
			testCmd = command.radio_command(parent=self, verbose=self.verbose, 
										    logFile=self.logFile)
			testCmd.send( self.sendCommandAndReceive )
			if any((not testCmd.ok, testCmd.error)):
				self.disconnect()
				self.log(" CONNECTION TEST FAILURE ".center(80,"!"))
			else:
				self.log("...Connected!")
		elif mode in ("udp",):
			#TODO: Add some sort of connection test here.
			self.log("...Connected! (w/o connection test)")
		return self.connected
	
	##
	# \internal
	# Connects the transport via UDP.
	#
	# This method just connects the transport.  No connection testing
	# is performed.
	#
	# \param host The hostname for the remote device.
	# \param port The port for the remote device.
	# \return True if connection was successful, False otherwise.
	def connectUdp(self,host,port):
		self.log("Connecting via UDP (%s,%s)..."%(repr(host),repr(port)))
		self._name = "transportUDP"
		try:
			self.udp = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
			self.udp.connect((str(host),int(port)))
			self.selectInput.append(self.udp)
			self.connected = True
		except:
			self.connectError = sys.exc_info()[1]
			self.log(traceback.format_exc())
			#traceback.print_exc()
			self.disconnect()
		return self.connected
	
	##
	# \internal
	# Connects the transport via TCP.
	#
	# This method just connects the transport.  No connection testing
	# is performed.
	#
	# \param host The hostname for the remote device.
	# \param port The port for the remote device.
	# \return True if connection was successful, False otherwise.
	def connectTcp(self,host,port):
		self.log("Connecting via TCP (%s,%s)..."%(repr(host),repr(port)))
		self._name = "transportTCP"
		try:
			self.tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			self.tcp.connect((str(host),int(port)))
			self.selectInput.append(self.tcp)
			self.connected = True
		except:
			self.connectError = sys.exc_info()[1]
			self.log(traceback.format_exc())
			#traceback.print_exc()
			self.disconnect()
		return self.connected
	
	##
	# \internal
	# Connects the transport via TTY.
	#
	# This method just connects the transport.  No connection testing
	# is performed.
	#
	# \param mode One of "tty", "tcp", or "udp".  Supported connection 
	#     modes vary by radio.
	# \param dev The name of the TTY device on the system.
	# \param baudrate The baud rate of the TTY device on the system.
	# \return True if connection was successful, False otherwise.
	def connectTty(self,dev,baudrate):
		self.log("Connecting via TTY (%s,%s)..."%(repr(dev),repr(baudrate)))
		self._name = "transportTTY"
		try:
			self.tty = serial.Serial(str(dev),baudrate=int(baudrate))
			if not self.tty.isOpen():
				self.tty.open()
			self.selectInput.append(self.tty)
			self.connected = True
		except:
			self.connectError = sys.exc_info()[1]
			self.log(traceback.format_exc())
			#traceback.print_exc()
			self.disconnect()
		return self.connected
	
	##
	# Disconnects the transport.
	def disconnect(self):
		self.log("Disconnecting... ")
		self._name = "transportXXX"
		if self.tcp is not None:
			self.log("TCP... ")
			try:
				self.tcp.close()
			except:
				self.log(traceback.format_exc())
				#traceback.print_exc()
		elif self.tty is not None:
			self.log("TTY... ")
			try:
				self.tty.close()
			except:
				self.log(traceback.format_exc())
				#traceback.print_exc()
		self.log("...Disconnected!")
		self.connected = False
		self.tcp = None
		self.tty = None
		self.selectInput = []
	
	##
	# Gets whether the transport is connected.
	def isConnected(self,):
		return any( conn is not None for conn in (self.tty,self.tcp,self.udp,) )
	
	##
	# Sends a command over the the transport.
	#
	# \param cmd The command string to send out.
	# \param clearRx Whether to make sure that the receive buffer is clear before
	#    sending the command.
	# \return Whether the transport is still connected.
	def sendCommand(self,cmd,clearRx=True):
		try:
			delta = datetime.timedelta(seconds=0,microseconds=0)
			if self.lastTx == 0:
				self.lastTx = datetime.datetime.now()
			else:
				delta = datetime.datetime.now() - self.lastTx
				self.lastTx = datetime.datetime.now()
			if clearRx:
				rx = self.receive(timeout=0.0)
				if len(rx)>0:
					self.logIfVerbose("**  Rx(%s)%s: %s" % ( "TCP" if self.tcp is not None else "UDP" if self.udp is not None else "TTY",\
													datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
													"!! Data waiting before sending a command %s  !!"%repr(rx), \
													 ))
			if self.tcp is not None:
				self.tcp.send( str(cmd) )
			elif self.tty is not None:
				self.tty.write( str(cmd) )
			elif self.udp is not None:
				self.udp.send( str(cmd) )
			self.logIfVerbose("**  Tx(%s)%s delta %s.%s: %r" % ( \
												"TCP" if self.tcp is not None else "UDP" if self.udp is not None else "TTY", \
												datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
												delta.seconds, \
												delta.microseconds, \
												str(cmd), \
												 ))
			if self.logCtrl is not None:
				self.logCtrl.addTransaction( txTime="%s" % ( \
												datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),\
												txString=str(cmd), \
												rxTime=None, \
												rxString=None, \
												 )

		except:
			self.log(traceback.format_exc())
			#traceback.print_exc()
			self.disconnect()
		return self.connected
	
	##
	# \internal
	# Receives a JSON-formatted string over the transport.
	#
	# \param timeout The timeout value to use for receiving data.  If None,
	#     use the default timeout value for the transport.
	# \return The received string.
	def receiveJson(self,timeout=None):
		rxString = ""
		try:
			delta = datetime.timedelta(seconds=0)
			if self.lastRx == 0:
				self.lastRx = datetime.datetime.now()
			else:
				delta = datetime.datetime.now() - self.lastRx
				self.lastRx = datetime.datetime.now()
			ins,outs,excepts = select.select(self.selectInput,[],[],float(timeout) if timeout is not None else self.defaultTimeout)
			if ins and self.udp is not None:
				rxString,address = self.udp.recvfrom(8192)
				if len(rxString)>0:
					self.logIfVerbose("**  Rx(UDP)%s delta %s.%s: %s" % ( \
										datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
										delta.seconds,delta.microseconds, \
										repr(rxString), \
										 ))
				else:
					self.disconnect()
		except:
			self.log(traceback.format_exc())
			#traceback.print_exc()
			rxString = "Exception"
		return rxString
	
	##
	# \internal
	# Receives client-formatted data over the transport.
	#
	# \param timeout The timeout value to use for receiving data.  If None,
	#     use the default timeout value for the transport.
	# \return The list of received data strings.
	def receiveCli(self,timeout=None):
		rx = []
		inString = ""
		try:
			while True:
				delta = datetime.timedelta(seconds=0)
				if self.lastRx == 0:
					self.lastRx = datetime.datetime.now()
				else:
					delta = datetime.datetime.now() - self.lastRx
					self.lastRx = datetime.datetime.now()
				ins,outs,excepts = select.select(self.selectInput,[],[],float(timeout) if timeout is not None else self.defaultTimeout)
				if ins:
					if self.tcp is not None:
						inString = self.tcp.recv(8192)
					elif self.tty is not None:
						inString = self.tty.read(self.tty.inWaiting())
					elif self.udp is not None:
						inString = self.udp.recv(8192)
					else:
						inString = ""
					if len(inString)>0:
						self.logIfVerbose("**  Rx(%s)%s delta %s.%s: %s" % ("TCP" if self.tcp is not None else "TTY",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),delta.seconds,delta.microseconds,repr(inString)))
#						if self.logCtrl is not None:
#							self.logCtrl.addTransaction(txTime=None,txString=None,rxTime="%s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")), \
#													rxString="%r"%(repr(inString)))
							
						rx.append( inString )
						if ">" in inString:
							break
					else:
						self.disconnect()
						rx.append( "\nDISCONNECTED\n" )
						break
				else:
					if timeout is not None and timeout>0:
						self.log("**  Rx(%s)%s: %s" % ("TCP" if self.tcp is not None else "TTY",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),"!! TIMEOUT  !!"))
						rx.append( "\nTIMEOUT\n" )
					break
		except:
			self.log(traceback.format_exc())
			#traceback.print_exc()
			self.disconnect()
			rx.append( "\nEXCEPTION\n" )
		rxString=("".join(rx)).strip()
		if self.logCtrl is not None and len(rxString)>0:
			self.logCtrl.addTransaction( txTime=None, \
											txString=None, \
											rxTime="%s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")), \
											rxString="".join(rx), \
											 )
		return [" ".join(i.strip().split()) for i in "".join(rx).replace(">","").split("\n") if i.strip()]
	
	# Basic function for receiving - requires self.rxFunction to point to the appropriate method for the radio!
	##
	# Receives data over the transport.
	#
	# The format of the received data depends on whether the "json" flag
	# was set at construction time.
	#
	# \param timeout The timeout value to use for receiving data.  If None,
	#     use the default timeout value for the transport.
	# \return If json=True, a JSON-formatted string; if json=False, a list of 
	#     received data strings.
	def receive(self,timeout=None):
		return self.rxFunction(timeout=timeout)
	
	##
	# Sends a command and receives the response over the transport.
	#
	# The format of the received data depends on whether the "json" flag
	# was set at construction time.
	#
	# \param cmd The command string to send out over the transport.
	# \param timeout The timeout value to use for receiving data.  If None,
	#     use the default timeout value for the transport.
	# \return If json=True, a JSON-formatted string; if json=False, a list of 
	#     received data strings.
	def sendCommandAndReceive(self,cmd,timeout=None):
		if self.sendCommand(str(cmd)):
			return self.receive(timeout)


if __name__=="__main__":
	import sys
	x = radio_transport(None)
	tick = time.time()
	if x.connect("tty" if "/dev/" in sys.argv[1] else "tcp",*sys.argv[1:]):
		for i in range(1):
			for cmd in ("*IDN?","VER?","FRQ?","ATT?","WBDDC?","WBFRQ?","NBDDC?","NBFRQ?",):
				print repr( x.sendCommandAndReceive("%s\r\n"%cmd, 1.0) )
			tock = time.time()
			print "%0.3f -> %0.3f = %0.3f" % (tick,tock,tock-tick,)
