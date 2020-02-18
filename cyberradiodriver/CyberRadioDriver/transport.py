#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.transport
# 
# Provides classes that define communication transports.
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.  
#     All rights reserved.
#
###############################################################

# Imports from other modules in this package
import command
import log
# Imports from external modules
import serial
# Python standard library imports
import datetime
import errno
import select
import socket
import sys
import time
import traceback
#from time import gmtime, strftime
import requests
import ndrcert
import json

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
    #    If not provided, this defaults to standard output. 
    # \param timeout Timeout for the transport (seconds).  If this is None,
    #   use the default timeout.
    def __init__(self,parent,verbose=False,logCtrl=None,json=False, 
                 logFile=sys.stdout, timeout=None):
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
        self.https = None
        self.fd = None
        self.logCtrl = logCtrl
        self.selectInput = []
        self.connected = False
        self.lastTime = datetime.datetime.now()
        self.lastTx = 0
        self.lastRx = 0
        self.isJson = json
        if json:
            self.rxFunction = self.receiveJson
        else:
            self.rxFunction = self.receiveCli
        self.connectError = ""
        self.httpStr = ""
        self.timeout = timeout
        if self.timeout is None:
            self.timeout = self.defaultTimeout
        
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
        if mode in ("tcp","tty","udp","https"):
            if self.connected:
                self.disconnect()
            if mode == "tcp":
                self.connectTcp(str(host_or_dev),int(port_or_baudrate) if port_or_baudrate is not None else self.defaultPort,)
            elif mode == "udp":
                self.connectUdp(str(host_or_dev),int(port_or_baudrate) if port_or_baudrate is not None else self.defaultPort,)
            elif mode == "tty":
                self.connectTty(str(host_or_dev),int(port_or_baudrate) if port_or_baudrate is not None else self.defaultBaudrate,)
            elif mode == "https":
                self.connectHttps(str(host_or_dev),int(port_or_baudrate) if port_or_baudrate is not None else 8617,)
        if mode in ("tcp","tty",):
            if self.isJson:
                testCmd = command.status_json(parent=self, verbose=self.verbose, 
                                              logFile=self.logFile)
            else:
                testCmd = command.radio_command(parent=self, verbose=self.verbose, 
                                                logFile=self.logFile)
            testCmd.send( self.sendCommandAndReceive )
            if any((not testCmd.ok, testCmd.error)):
                self.disconnect()
                self.log(" CONNECTION TEST FAILURE ".center(80,"!"))
                self.connectError = testCmd.errorInfo
            else:
                self.log("...Connected!")
        elif mode in ("udp",):
            #TODO: Add some sort of connection test here.
            if self.isJson:
                testCmd = command.status_json(parent=self, verbose=self.verbose, 
                                              logFile=self.logFile)
            else:
                testCmd = command.radio_command(parent=self, verbose=self.verbose, 
                                                logFile=self.logFile)
            testCmd.send( self.sendCommandAndReceive )
            if any((not testCmd.ok, testCmd.error)):
                self.disconnect()
                self.log(" CONNECTION TEST FAILURE ".center(80,"!"))
                self.connectError = testCmd.errorInfo
            else:
                self.log("...Connected!")
            #self.log("...Connected! (w/o connection test)")
        elif mode in ("https",) and self.connected:
            self.log("...Connected!")
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
        self.parent.ipAddr = host
        try:
            self.udp = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            self.udp.settimeout(self.timeout)
            self.udp.connect((str(host),int(port)))
            self.selectInput.append(self.udp)
            self.connected = True
        except:
            self.connectError = sys.exc_info()[1]
            self.log("EXCEPTION:", self.connectError)
            self.logIfVerbose(traceback.format_exc())
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
            self.tcp.settimeout(self.timeout)
            self.tcp.connect((str(host),int(port)))
            self.selectInput.append(self.tcp)
            self.connected = True
        except:
            self.connectError = sys.exc_info()[1]
            self.log("EXCEPTION:", self.connectError)
            self.logIfVerbose(traceback.format_exc())
            #traceback.print_exc()
            self.disconnect()
        return self.connected
    
    ##
    # \internal
    # Connects the transport via HTTPS.
    #
    # This method just connects the transport.  No connection testing
    # is performed.
    #
    # \param host The hostname for the remote device.
    # \param port The port for the remote device.
    # \return True if connection was successful, False otherwise.
    def connectHttps(self,host,port):
        self.log("Connecting via HTTPS (%s,%s)..."%(repr(host),repr(port)))
        self._name = "transportHTTPS"
        self.parent.ipAddr = host
        try:
            self.https = requests.Session()
            self.httpsUrl = "https://{0}:{1}/api/command".format(host,port)
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            from requests.packages.urllib3.exceptions import InsecurePlatformWarning
            requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
            from requests.packages.urllib3.exceptions import SNIMissingWarning
            requests.packages.urllib3.disable_warnings(SNIMissingWarning)
            rsp = self.https.get("https://{0}:{1}".format(host,port), 
                                 verify=False, timeout=self.timeout)
            if (rsp.status_code != 200):
                self.disconnect()
#             self.https = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#             self.https.connect((str(host),int(port)))
#             self.selectInput.append(self.https)
            self.connected = True
        except:
            self.connectError = sys.exc_info()[1]
            self.log("EXCEPTION:", self.connectError)
            self.logIfVerbose(traceback.format_exc())
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
            self.log("EXCEPTION:", self.connectError)
            self.logIfVerbose(traceback.format_exc())
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
                self.logIfVerbose(traceback.format_exc())
                #traceback.print_exc()
        elif self.tty is not None:
            self.log("TTY... ")
            try:
                self.tty.close()
            except:
                self.logIfVerbose(traceback.format_exc())
                #traceback.print_exc()
        elif self.https is not None:
            self.log("HTTPS... ")
        self.log("...Disconnected!")
        self.connected = False
        self.tcp = None
        self.tty = None
        self.udp = None
        self.https = None
        self.selectInput = []
    
    ##
    # Gets whether the transport is connected.
    def isConnected(self,):
        return any( conn is not None for conn in (self.tty,self.tcp,self.udp,self.https,) )
    
    ##
    # Sends a command over the the transport.
    #
    # \param cmd The command string to send out.
    # \param clearRx Whether to make sure that the receive buffer is clear before
    #    sending the command.
    # \param timeout Timeout, in seconds.  If this is None, never time out.
    # \return Whether the transport is still connected.
    #def sendCommand(self,cmd,clearRx=True):
    def sendCommand(self,cmd,clearRx=False, timeout=None):
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
                    self.logIfVerbose("**  Rx(%s)%s: %s" % ( self.transportIdent(), \
                                                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
                                                    "!! Data waiting before sending a command %s  !!"%repr(rx), \
                                                     ))
            logCmd = str(cmd)
            if self.tcp is not None:
                self.tcp.send( str(cmd) )
            elif self.tty is not None:
                self.tty.write( str(cmd) )
            elif self.udp is not None:
                self.udp.send(cmd)
            elif self.https is not None:
                if isinstance(cmd, str):
                    jsonCmd = json.loads(cmd)
                elif isinstance(cmd, dict):
                    jsonCmd = cmd
                else:
                    jsonCmd = None
                self.logIfVerbose("cmd is : %r"%(str(jsonCmd),))
                if jsonCmd is not None:
                    cmdTimeout = self.timeout if timeout is None else timeout
                    httprsp = self.https.post(self.httpsUrl, json=jsonCmd, 
                                              verify=False, timeout=cmdTimeout)
                    self.logIfVerbose("HTTPS rsp: code=%d  %r" % (httprsp.status_code, httprsp.text) )
                    # Radios return HTTP 400 (Bad Request) when commands don't work. These may have
                    # valid JSON responses.
#                     if httprsp.status_code==200:
#                         self.httpStr = httprsp.text
#                     else:
#                         self.httpStr = None
                    self.httpStr = httprsp.text
#                 hname = self.parent.ipAddr
#                 cmdurl = 'https://' + hname + '/api/command'
#                 loadcmd = json.loads(cmd)
#                 logCmd = str(loadcmd)
#                 self.logIfVerbose("cmd is : %r", str(loadcmd))
#                 try:
#                     httprsp = requests.post(cmdurl,json=loadcmd,verify=ndrcert.crt)
#                     self.httpStr = httprsp.text
#                     print "http response text is ", self.httpStr
#                 except:
#                     print "could not post http command to radio"
            self.logIfVerbose("**  Tx(%s)%s delta %s.%s: %r" % ( \
                                                self.transportIdent(), \
                                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
                                                delta.seconds, \
                                                delta.microseconds, \
                                                logCmd, \
                                                 ))
            if self.logCtrl is not None:
                self.logCtrl.addTransaction( txTime="%s" % ( \
                                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),\
                                                txString=logCmd, \
                                                rxTime=None, \
                                                rxString=None, \
                                                 )

        except:
            self.connectError = sys.exc_info()[1]
            self.log("EXCEPTION:", self.connectError)
            self.logIfVerbose(traceback.format_exc())
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
        if self.udp is not None:
            return self.receiveJsonUdp(timeout)
        elif self.tcp is not None:
            return self.receiveJsonTcp(timeout)
        elif self.https is not None:
            return self.receiveJsonHttps(timeout)
    
    ##
    # \internal
    # Receives a JSON-formatted string over the HTTPS transport.
    #
    # \param timeout The timeout value to use for receiving data.  If None,
    #     use the default timeout value for the transport.
    # \return The received string.
    def receiveJsonHttps(self,timeout=None):
#         self.logIfVerbose("Transport.py - Receive JSON over HTTPS")
        delta = datetime.timedelta(seconds=0)
        if self.lastRx == 0:
            self.lastRx = datetime.datetime.now()
        else:
            delta = datetime.datetime.now() - self.lastRx
            self.lastRx = datetime.datetime.now()

#         self.logIfVerbose("HTTP response text while response processing is %s" % self.httpStr)
        rxString = str(self.httpStr)

        if (rxString is not None) and (len(rxString)>0):
            self.logIfVerbose("**  Rx(HTTPS)%s delta %s.%s: %s" % ( \
                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
                                delta.seconds,delta.microseconds, \
                                repr(rxString), \
                                 ))
        else:
            rxString = "Empty Read"
            self.disconnect()

        return rxString
    
    ##
    # \internal
    # Receives a JSON-formatted string over the UDP transport.
    #
    # \param timeout The timeout value to use for receiving data.  If None,
    #     use the default timeout value for the transport.
    # \return The received string.
    def receiveJsonUdp(self,timeout=None):
        self.logIfVerbose("Transport.py - Receive JSON over UDP")
        rxString = ""
        try:
            delta = datetime.timedelta(seconds=0)
            if self.lastRx == 0:
                self.lastRx = datetime.datetime.now()
            else:
                delta = datetime.datetime.now() - self.lastRx
                self.lastRx = datetime.datetime.now()
            # Sometimes, select() will fail with an "Interrupted system call" (EINTR) 
            # exception. We need to trap that case and keep selecting if that happens.
            ins = self.selectInput
            try:
                ins,outs,excepts = self.select(self.selectInput,[],[],float(timeout) if timeout is not None else self.defaultTimeout)
            except select.error as ex:
                if ex[0] == errno.EINTR:
                    pass
                else:
                    raise
            if ins and self.udp is not None:
                rxString,address = self.udp.recvfrom(32768)
                if len(rxString)>0:
                    self.logIfVerbose("**  Rx(UDP)%s delta %s.%s: %s" % ( \
                                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
                                        delta.seconds,delta.microseconds, \
                                        repr(rxString), \
                                         ))
                else:
                    rxString = "Empty Read"
                    self.disconnect()
        except:
            self.logIfVerbose(traceback.format_exc())
            #traceback.print_exc()
            rxString = "Exception"
        return rxString
    
    ##
    # \internal
    # Receives a JSON-formatted string over the TCP transport.
    #
    # \param timeout The timeout value to use for receiving data.  If None,
    #     use the default timeout value for the transport.
    # \return The received string.
    def receiveJsonTcp(self,timeout=None):
        self.logIfVerbose("Transport.py - Receive JSON over TCP")
        rxString = ""
        try:
            delta = datetime.timedelta(seconds=0)
            if self.lastRx == 0:
                self.lastRx = datetime.datetime.now()
            else:
                delta = datetime.datetime.now() - self.lastRx
                self.lastRx = datetime.datetime.now()
            # Sometimes, select() will fail with an "Interrupted system call" (EINTR) 
            # exception. We need to trap that case and keep selecting if that happens.
            ins = self.selectInput
            try:
                ins,outs,excepts = self.select(self.selectInput,[],[],float(timeout) if timeout is not None else self.defaultTimeout)
            except select.error as ex:
                if ex[0] == errno.EINTR:
                    pass
                else:
                    raise
            if ins and self.tcp is not None:
                rxString,address = self.tcp.recvfrom(32768)
                if len(rxString)>0:
                    self.logIfVerbose("**  Rx(TCP)%s delta %s.%s: %s" % ( \
                                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), \
                                        delta.seconds,delta.microseconds, \
                                        repr(rxString), \
                                         ))
                else:
                    rxString = "Empty Read"
                    self.disconnect()
        except:
            self.logIfVerbose(traceback.format_exc())
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
                # Sometimes, select() will fail with an "Interrupted system call" (EINTR) 
                # exception. We need to trap that case and keep selecting if that happens.
                ins = self.selectInput
                try:
                    ins,outs,excepts = self.select(self.selectInput,[],[],float(timeout) if timeout is not None else self.defaultTimeout)
                except select.error as ex:
                    if ex[0] == errno.EINTR:
                        pass
                    else:
                        raise
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
                        self.logIfVerbose("**  Rx(%s)%s delta %s.%s: %s" % (self.transportIdent(),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),delta.seconds,delta.microseconds,repr(inString)))
#                        if self.logCtrl is not None:
#                            self.logCtrl.addTransaction(txTime=None,txString=None,rxTime="%s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")), \
#                                                    rxString="%r"%(repr(inString)))
                            
                        rx.append( inString )
                        if ">" in inString:
                            break
                    else:
                        self.disconnect()
                        rx.append( "\nDISCONNECTED\n" )
                        break
                else:
                    if timeout is not None and timeout>0:
                        self.logIfVerbose("**  Rx(%s)%s: %s" % (self.transportIdent(),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),"!! TIMEOUT  !!"))
                        rx.append( "\nTIMEOUT\n" )
                    break
        except:
            self.logIfVerbose(traceback.format_exc())
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
        if self.sendCommand(str(cmd), timeout=timeout):
            return self.receive(timeout)

    ##
    # \internal
    # \brief Wraps select() call so that it properly handles serial device read 
    #    selection under Windows.
    # \param rlist List of file-like objects to check for read availability.
    # \param wlist List of file-like objects to check for write availability.
    # \param xlist List of file-like objects to check for exception conditions.
    # \param timeout Time to wait, or None if the call should wait forever.
    # \returns A 3-tuple: (reads, writes, excepts)
    def select(self, rlist, wlist, xlist, timeout=None):
        if sys.platform == "win32":
            #print "[DBG][select] rlist=", rlist
            #print "[DBG][select] wlist=", wlist
            #print "[DBG][select] xlist=", xlist
            # Get start time
            startTime = time.time()
            # Do standard select call on socket devices only -- but skip this call if
            # all three socket list is empty, as Windows select() errors out in this case.
            sock_rlist = [q for q in rlist if isinstance(q, socket.socket)]
            #print "[DBG][select] sock_rlist=", sock_rlist
            sock_rlist_hit, wlist_hit, xlist_hit = ([], [], [])
            if any([len(q) > 0 for q in [sock_rlist, wlist, xlist]]):
                sock_rlist_hit, wlist_hit, xlist_hit = select.select(sock_rlist, wlist, xlist, timeout)
            #print "[DBG][select] sock_rlist_hit=", sock_rlist_hit
            # Use remaining time to poll serial devices for devices in waiting
            ser_rlist = [q for q in rlist if isinstance(q, serial.Serial)]
            ser_rlist_hit = []
            while len(ser_rlist_hit) == 0:
                ser_rlist_hit += [ser for ser in ser_rlist if ser.inWaiting() > 0]
                if len(ser_rlist_hit) == 0 and (timeout is None or \
                                               time.time() - startTime <= timeout):
                    time.sleep(0.1)
                else:
                    break
            #print "[DBG][select] ser_rlist_hit=", ser_rlist_hit
            return sock_rlist_hit + ser_rlist_hit, wlist_hit, xlist_hit
        else:
            return select.select(rlist, wlist, xlist, timeout)

    ##
    # \internal
    # \brief Brief identifier for the active transport method
    # \returns A string identifying the transport.
    def transportIdent(self):
        ret = "<unknown>"
        if self.tcp is not None:
            ret = "TCP"
        elif self.tty is not None:
            ret = "TTY"
        elif self.udp is not None:
            ret = "UDP"
        elif self.https is not None:
            ret = "HTTPS"
        return ret


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
