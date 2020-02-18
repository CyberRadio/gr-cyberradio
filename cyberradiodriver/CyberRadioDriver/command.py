#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.command
# 
# \brief Provides classes that define hardware commands.
#
# \note This module defines standard behavior only.  To customize
#     a command class for a particular radio, derive a new
#     class from the appropriate base class.  It is recommended
#     that behavior specific to a given radio be placed in the
#     module that supports that radio.
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.  
#     All rights reserved.
#
###############################################################

# Imports from other modules in this package
import configKeys
import log
# Imports from external modules
# Python standard library imports
import json
import string
import traceback 

##
# \internal
# \brief Helper method for dealing with return values from hardware commands
#    that might be hexadecimal
# \param value Command return value, as a string
# \return The command return value, as an integer
def maybeHex(value):
    if value.startswith("0x"):
        return int(value, 16)
    else:
        return int(value, 10)

#----------------------------------------------------------------------------#
#--  Generic Radio Command Object  ------------------------------------------#

##
# \brief Base hardware command class.
#
# A radio command object maintains all of the information that it needs to 
# issue a command to the radio and to parse the response it gets back.  
#
# Members \c setParameters and \c queryParameters identify which parameters
# a command accepts for setting and querying, respectively.  The user passes
# these parameters to the command object through keyword arguments to its 
# constructor.  Once the command object is created, these parameters are 
# available as attributes of the command object itself; each named parameter
# has an attribute with the same name.
#
class _commandBase(log._logger):
    ## Command delimiter.
    delimiter = "\n"
    ## Command mnemonic.
    mnemonic = ""
    ## Whether the command can be used to set values on the radio.
    settable = True
    ## List of parameters used in the "set" version of the command.
    #
    # Each entry in the list is a 4-tuple:
    # <ul>
    # <li> Parameter name (string)
    # <li> Parameter type (class)
    # <li> Whether parameter is optional (Boolean)
    # <li> Default parameter value (varies by type)
    # </ul>
    setParameters = []
    ## Whether the command can be used to query values on the radio.
    queryable = True
    ## List of parameters used in the "query" version of the command.
    #
    # Each entry in the list is a 4-tuple:
    # <ul>
    # <li> Parameter name (string)
    # <li> Parameter type (class)
    # <li> Whether parameter is optional (Boolean)
    # <li> Default parameter value (varies by type)
    # </ul>
    queryParameters = []
    ## List of parameters returned in the "query" version of the command.
    #
    # Response elements (separated by spaces) are assigned to keywords in the 
    # response information dictionary.  These elements are processed in the 
    # order that they appear in this list.  Elements in the list are either 
    # None (in which case the corresponding response element is ignored) or
    # a 3-tuple consisting of:
    # <ul>
    # <li> Keyword (string)
    # <li> Data type (class)
    # <li> Whether unit specifiers in the response are ignored (Boolean)
    # </ul>
    #
    # The resulting response information dictionary is available through
    # the getResponseInfo() method.
    #  
    queryResponseData = []
    ## Timeout value for issuing the command and getting the response back.
    timeout = 10.0
    
    ##
    # \brief Constructs a hardware command object.
    #
    # The constructor uses keyword arguments to configure the class.  It 
    # consumes the following keyword arguments:
    # <ul>
    # <li> "verbose": Verbose mode (Boolean)
    # <li> "logFile": An open file or file-like object to be used for log output.  
    #    If not provided, this defaults to standard output. 
    # <li> "parent": The component object that is issuing this command. 
    # <li> "mnemonic": A string used to override the default command mnemonic.
    # <li> "query": Whether this command is a query (Boolean). 
    # <li> "cmdString": A string containing the entire command to send to the
    #   radio.  If this keyword argument is provided, then the object does no
    #   parameter processing. 
    # </ul>
    #
    # \param args Variable-length list of positional arguments.  Positional
    #     arguments are ignored.
    # \param kwargs Dictionary of keyword arguments for the component
    #     object.  Which keyword arguments are valid depends on the 
    #     specific component.  Unsupported keyword arguments will be ignored.
    def __init__(self,*args,**kwargs):
        # Consume keyword arguments "verbose" and "logFile" for logging support
        log._logger.__init__(self, *args, **kwargs)
        # Consume our own keyword arguments
        self.parent = kwargs.get("parent",None)
        self.parameterList = []
        self.mnemonic = kwargs.get("mnemonic",self.mnemonic)
        self.query = kwargs.get("query",not self.settable)
        if kwargs.has_key("cmdString"):
            self.cmd = str(kwargs.get("cmdString")).strip()
            self.mnemonic = self.cmd[:self.cmd.find(" ")]
        else:
            self.cmd = ( "%s%s %s"%(self.mnemonic,"?" if self.query else "",", ".join(self.parameterList),) ).strip()
#             for parmName,parmType,parmOpt,parmDefault in self.queryParameters if self.query else self.setParameters:
            for parm in self.queryParameters if self.query else self.setParameters:
                if isinstance(parm, tuple):
                    parmName,parmType,parmOpt,parmDefault = parm
    #                 self.logIfVerbose((parmName,parmType,parmOpt,parmDefault,repr(kwargs.get(parmName))))
                    if not kwargs.has_key(parmName):
                        #self.logIfVerbose(parmName,parmType,parmOpt)
                        if not parmOpt:
                            self.log( "MISSING MANDATORY PARAMETER %s" % repr(parmName) )
                        break
                    else:
                        try:
                            setattr( self, parmName, parmType(kwargs.get(parmName,parmDefault)) )
                            self.parameterList.append( format( parmType(kwargs.get(parmName,parmDefault)) ) )
                        except:
                            pass
                else:
                    self.parameterList.append( format( parm ) )
            self.cmd = ( "%s%s %s"%(self.mnemonic,"?" if self.query else "",", ".join(self.parameterList),) ).strip()
        ## A list of strings returned by the radio in response to the command.
        self.rsp = None
        ## Whether the command completed successfully.
        self.ok = None
        ## Whether the command resulted in an error.
        self.error = None
        ## A list of information about the error.
        self.errorInfo = None
        ## Whether the command resulted in a successful outcome.
        self.success = None
        ## A list of information about the success.
        self.successInfo = None
        ## A dictionary of key-value pairs describing the command response.
        self.responseInfo = None
    
    ##
    # \internal
    def __nonzero__(self):
        return bool(self.success)
    
    # OVERRIDE
    ##
    # \brief Writes output to the log.
    #
    # The output sent to the log file will contain information about the object
    # issuing the command and the command itself.
    # 
    # \param string String to send to the log file.
    def log(self,string):
        log._logger.log(self, "%s.%s%s :: %s"%(str(self.parent),self.mnemonic,"?" if self.query else "",str(string)))
    
    ##
    # \brief Sends the command over a connected transport.
    #
    # \param transportFunction A method called to send the command over a 
    #    transport.
    # \param timeout The timeout value to use for the command.  If None, use
    #    the command's default timeout.
    # \return True if the command succeeded, False otherwise.
    def send(self,transportFunction,timeout=None):
        try:
            rsp = transportFunction( str(self), timeout if timeout is not None else self.timeout )
            self.addResponse(rsp)
            # Sanity-check: No point in parsing a response we never received.
            if self.rsp is not None:
                self.parseResponse()
            #if self.verbose:
            if False:
                self.logIfVerbose("\n\t"+"\n\t".join( ( repr(self.cmd), \
                    repr(";".join(self.rsp) if self.rsp is not None else None), \
                    repr(self.success), repr(self.successInfo) ) ) ) 
            else:
                self.logIfVerbose( repr(self) )
            if not self.ok:
                self.log( "SOMETHING WENT WRONG" )
            elif self.error:
                self.log( "ERROR DETECTED, %s"%( repr(self.errorInfo), ) )
        except:
            self.logIfVerbose(traceback.format_exc())
            self.ok = False
        return self.ok
    
    ##
    # \internal
    def __str__(self):
        return "%s%s"%(self.cmd.strip(),self.delimiter)
    
    ##
    # \internal
    def __repr__(self):
        return "CMD: %s | RSP: %s | SUCCESS: %s (%s)" % \
                ( repr(self.cmd), \
                    repr(";".join(self.rsp)) if self.rsp is not None else None, \
                    self.success, self.successInfo )
                
    ##
    # \brief Adds a command response to the object's internal state.
    #
    # This method checks the returned responses for key strings and sets
    # the object's state variables accordingly.
    # 
    # \param rsp A list of strings containing the command response returned by
    #    the radio.
    def addResponse(self,rsp):
        if rsp is not None:
            self.rsp = rsp
            self.ok = any( "OK" in i.upper() for i in self.rsp )
            self.error = any( "ERROR" in i.upper() for i in self.rsp )
            self.timeout = any( "TIMEOUT" in i.upper() for i in self.rsp )
            self.exception = any( "EXCEPTION" in i.upper() for i in self.rsp )
            self.success = self.ok and all( not i for i in (self.error,self.timeout,self.exception) )
            self.successInfo = ", ".join( "%s: %s"%(i,j) for i,j in ( ("OK",self.ok), \
                                                                        ("ERROR",self.error),
                                                                        ("TIMEOUT",self.timeout), \
                                                                        ("EXCEPT",self.exception), \
                                                                    ) if j \
                                         )
            if self.error:
                self.errorInfo = [ i.split(":")[-1].strip() for i in self.rsp if "ERROR" in i.upper() ]
        else:
            self.error = True
            
    ##
    # \brief Parses the command response into the response information dictionary.
    def parseResponse(self):
        if len(self.queryResponseData) > 0:
            self.responseInfo = {}
            for rspLine in self.rsp:
                # Ignore lines that echo back the query command
                if "%s?" % self.mnemonic in rspLine:
                    continue
                # Ignore lines that contain command status
                elif any([q in rspLine.upper() for q in ["OK", "ERROR", "TIMEOUT", "EXCEPTION"]]):
                    continue
                # Start response parsing
                # -- Break line into response elements
                rspVec = rspLine.replace(", ", " ").replace(",", " ").split(" ")
                # -- Sanity check to make sure we even got a response
                if len(rspVec) > 0:
                    # -- Pop the first element if it is the command mnemonic
                    if rspVec[0] == self.mnemonic:
                        rspVec.pop(0)
                    # -- Sanity check again
                    if len(rspVec) > 0:
                        # -- Iterate over our expected response keys
                        for i, rspDataInfo in enumerate(self.queryResponseData):
                            # Stop we didn't get enough data in the response
                            if i >= len(rspVec):
                                break
                            # Skip element if response data info entry is None
                            if rspDataInfo is None:
                                continue
                            # Strip unit designators if desired
                            if rspDataInfo[2]:
                                rspVec[i] = rspVec[i].translate(None, string.ascii_letters)
                            # Convert the response element into the appropriate type
                            # and put it in the dictionary.  If the conversion doesn't
                            # work, assign None instead.
                            try:
                                self.responseInfo[rspDataInfo[0]] = rspDataInfo[1](rspVec[i])
                            except:
#                                 print "[DEBUG] EXCEPTION"
#                                 traceback.print_exc()
                                self.responseInfo[rspDataInfo[0]] = None
                            pass
            
    ##
    # \brief Gets the command response information dictionary.
    #
    # \return The command response information dictionary.
    def getResponseInfo(self):
        return self.responseInfo


#--  Generic Radio Command Object  ------------------------------------------#

##
# \brief Generic radio command.
#
# This command class can be used to issue arbitrary commands to the radio
# hardware, but cannot perform parameter handling.  
#
class radio_command(_commandBase):
    pass

##
# \brief JSON command configuration class.
#
# This class provides a common message ID generation capacity
# for all JSON commands sent by the driver.  
#
class jsonConfig(object):
    msgIdVal = 0
    
    @classmethod
    def newMessageId(cls):
        cls.msgIdVal += 1
        return cls.msgIdVal


##
# \brief Base hardware command class for use with JSON commands.
#
# A radio command object maintains all of the information that it needs to 
# issue a JSON command to the radio and to parse the JSON response it gets back.  
#    
class _jsonCommandBase(log._logger):
    ## Command mnemonic.
    mnemonic = ""
    ## Prefix for command mnemonics that represent queries. 
    mnemonicQueryPrefix = "q"
    ## Whether the command can be used to set values on the radio.
    settable = True
    ## Whether the command can be used to query values on the radio.
    queryable = True
    ## Timeout value for issuing the command and getting the response back.
    timeout = 10.0
    ## Query parameter map.
    # This is a dictionary that maps a keyword argument supplied in the 
    # configuration dictionary (key) to the appropriate parameter actually 
    # sent in the command (value).
    # This mapping is reversed when "unpacking" the command response.
    # If the map is empty, then no mapping is performed.  
    queryParamMap = {} 
    ## Set parameter map.
    # This is a dictionary that maps a keyword argument supplied in the 
    # configuration dictionary (key) to the appropriate parameter actually 
    # sent in the command (value).
    # If the map is empty, then no mapping is performed.  
    setParamMap = {} 
    
    def __init__(self,*args,**kwargs):
        # Consume keyword arguments "verbose" and "logFile" for logging support
        log._logger.__init__(self, *args, **kwargs)
        # Now consume our own
        self.parent = kwargs.get("parent", None)
        self.query = kwargs.get("query", not self.settable)
        self.mnemonic = kwargs.get("mnemonic", 
                                   (self.mnemonicQueryPrefix if self.query else "") + self.mnemonic)
        # Start with a new message ID
        self.cmd = { "msg": jsonConfig.newMessageId() }
        # If the user specified the command string, parse it
        if kwargs.has_key("cmdString"):
            self.cmd.update(json.loads(str(kwargs.get("cmdString")), 
                                       object_hook=_jsonCommandBase.ascii_encode_dict))
            self.mnemonic = self.cmd.get("cmd", "")
            self.query = self.mnemonic.startswith(self.mnemonicQueryPrefix)
        # Otherwise, use the command mnemonic and keyword arguments to
        # parse it.  Set atttributes appropriately.
        else:
            self.cmd.update({ "cmd": self.mnemonic, })
            parmDict = {}
            argParamMap = self.queryParamMap if self.query else self.setParamMap
            for key in argParamMap:
                setattr(self, key, None)
            for key in kwargs:
                if key in argParamMap:
                    parmDict.update({ argParamMap[key]: kwargs[key] })
                    setattr(self, key, kwargs[key])
            self.cmd.update({ "params": parmDict, })
        #self.logIfVerbose("jsonCommandBase init: cmd=%s" % str(self.cmd))
        ## A list of strings returned by the radio in response to the command.
        self.rsp = None
        ## Whether the command completed successfully.
        self.ok = None
        ## Whether the command resulted in an error.
        self.error = None
        ## A list of information about the error.
        self.errorInfo = None
        ## Whether the command resulted in a successful outcome.
        self.success = None
        ## A list of information about the success.
        self.successInfo = None
        ## A dictionary of key-value pairs describing the command response.
        self.responseInfo = None
    
    ##
    # \brief Converts Unicode strings to ASCII strings when handling JSON.
    #
    # Use this method as the object_hook keyword argument when calling 
    # json.loads().
    #
    @staticmethod
    def ascii_encode_dict(data):
        ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x 
        return dict(map(ascii_encode, pair) for pair in data.items())

    def __nonzero__(self):
        return bool(self.success)
    
    def log(self,string):
        log._logger.log(self, "%s.%s :: %s"%(str(self.parent),self.mnemonic,str(string)))
    
    ##
    # \brief Sends the command over a connected transport.
    #
    # \param transportFunction A method called to send the command over a 
    #    transport.
    # \param timeout The timeout value to use for the command.  If None, use
    #    the command's default timeout.
    # \return True if the command succeeded, False otherwise.
    def send(self,transportFunction,timeout=None):
        # Sanity check: Don't even bother trying to send the command if
        # the transport function doesn't exist
        if transportFunction is None:
            return False
        try:
            rsp = transportFunction( str(self), timeout if timeout is not None else self.timeout )
            self.addResponse(rsp)
            self.parseResponse()
            #if self.verbose:
            if False:
                self.logIfVerbose("\n\t"+"\n\t".join( ( repr(self.cmd), \
                    repr(";".join(self.rsp) if self.rsp is not None else None), \
                    repr(self.success), repr(self.successInfo) ) ) ) 
            else:
                self.logIfVerbose( repr(self) )
            if self.error:
                self.log( "ERROR DETECTED, %s"%( repr(self.errorInfo), ) )
            elif not self.ok:
                self.log( "SOMETHING WENT WRONG" )
        except:
            self.logIfVerbose(traceback.format_exc())
            self.ok = False
        return self.ok
    
    def __str__(self):
        if hasattr(self, "cmd"):
            return json.dumps(self.cmd)
        else:
            return ""
    
    def __repr__(self):
        return "CMD: %s | RSP: %s | SUCCESS: %s (%s)" % \
                ( str(self), \
                    repr(self.rsp) if self.rsp is not None else None, \
                    self.success, self.successInfo )
                
    def addResponse(self,rsp):
        if rsp is not None:
            # For JSON, the response is just a string
            self.rsp = rsp
            self.timeout = any( "TIMEOUT" in i.upper() for i in self.rsp )
            self.exception = any( "EXCEPTION" in i.upper() for i in self.rsp )
            if self.timeout:
                self.ok = self.success = False
                self.error = True
                self.errorInfo = ["JSON response timeout"]
            elif self.exception:
                self.ok = self.success = False
                self.error = True
                self.errorInfo = ["JSON response exception"]
            else:
                try:
                    rspDict = json.loads(self.rsp, 
                                         object_hook=_jsonCommandBase.ascii_encode_dict)
                    self.ok = self.success = rspDict["success"]
                    if self.success:
                        # Translate returned results into attributes/response info
                        # -- Reverse the argument-parameter mapping
                        argParamMap = self.queryParamMap if self.query else self.setParamMap
                        revMap = dict( (v,k) for (k,v) in argParamMap.iteritems() )
                        # -- Map parameter to argument, then make an attribute for it
                        #    and enter the value into the response info dictionary
                        self.responseInfo = {}
                        # Queries return their results in "result"
                        if "result" in rspDict:
                            # If "result" is a dictionary...
                            if isinstance(rspDict["result"], dict):
                                for key in rspDict["result"]:
                                    if key in revMap:
                                        setattr(self, revMap[key], rspDict["result"][key])
                                        self.responseInfo[revMap[key]] = rspDict["result"][key]
                                self.successInfo = ", ".join(["%s: %s" % (k,v) for k,v in \
                                                              rspDict["result"].iteritems()])
                            # ...else "result" is a string
                            else:
                                self.responseInfo["result"] = rspDict["result"]
                    self.error = "error" in rspDict
                    if self.error:
                        self.errorInfo = ["%s: %s" % (k,v) for k,v in rspDict["error"].iteritems()]
                    pass
                except:
                    # Malformed JSON
                    self.ok = self.success = False
                    self.error = True
                    self.errorInfo = ["JSON response is malformed"]
                    self.errorInfo += [traceback.format_exc()]
        else:
            self.error = True
            self.ok = self.success = False
            self.errorInfo = ["No command response received"]
                        
    ##
    # \brief Parses the command response.
    #
    # \note For JSON commands, this method does nothing.  The 
    # addResponse() method handles all response parsing. 
    def parseResponse(self):
        pass

    ##
    # \brief Gets the command response information dictionary.
    #
    # \return The command response information dictionary.
    def getResponseInfo(self):
        return self.responseInfo

    ## 
    # \brief Returns the string representation of this object's attributes.
    #
    # This is available to derived classes as _SelfDescribingMixin__myRepr().
    #
    # \returns The string representation.
#     def attributeDump(self):
#         tmp = []
#         cname = str(self.__class__).replace("<class ","").replace("'","").replace(">","")
#         cname = cname.replace(self.__module__ + ".","")
#         for (attr, value) in sorted(self.__dict__.iteritems()):
#             tmp.append( attr + "=\"" + str(value) + "\"" )
#         ret = cname + "(" + ",".join(tmp) + ")"
#         return ret
            

##--  Generic Radio Command Object  ------------------------------------------##
#
# \brief This command class can be used to issue arbitrary commands to the radio
# hardware, but cannot perform parameter handling.  
#
class json_radio_command(_jsonCommandBase):
    pass
        
#--  Frequency Command  -----------------------------------------------------#

##
# \brief Frequency command.
#
class frq(_commandBase):
    mnemonic = "FRQ"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.TUNER_FREQUENCY,int,False,1000), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_FREQUENCY, int, True), \
                        ]
    
#--  Attenuation Command  ---------------------------------------------------#

##
# \brief Attenuation command.
#
class att(_commandBase):
    mnemonic = "ATT"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.TUNER_ATTENUATION,int,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_ATTENUATION, int, True), \
                        ]

#--  AGP Command  ---------------------------------------------------#

##
# \brief AGP command.
#
class agp(_commandBase):
    mnemonic = "AGP"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.TUNER_AGP,int,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_AGP, int, True), \
                        ]
                        
##--  Tuner Command  -----------------------------------------------------##

#--  DDC Frequency Commands  ------------------------------------------------#

##
# \brief WBDDC frequency offset command.
#
class wbfrq(_commandBase):
    mnemonic = "WBFRQ"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.DDC_FREQUENCY_OFFSET,int,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ (configKeys.INDEX, int, False), \
                          (configKeys.DDC_FREQUENCY_OFFSET, int, True), \
                        ]

##
# \brief NBDDC frequency offset command.
#
class nbfrq(wbfrq):
    mnemonic = "NBFRQ"

#--  DDC Configuration Commands  --------------------------------------------#

##
# \brief WBDDC configuration command.
#
class wbddc(_commandBase):
    ## This should apply to the NDR470, NDR472, and NDR304
    mnemonic = "WBDDC"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.DDC_RATE_INDEX,int,False,0), \
                        (configKeys.DDC_UDP_DESTINATION,int,False,0), \
                        (configKeys.ENABLE,int,False,0), \
                        (configKeys.DDC_VITA_ENABLE,int,True,0), \
                        (configKeys.DDC_STREAM_ID,int,True,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DDC_RATE_INDEX, int, True), \
                        (configKeys.DDC_UDP_DESTINATION, int, True), \
                        (configKeys.ENABLE, int, True), \
                        (configKeys.DDC_VITA_ENABLE, int, True), \
                        (configKeys.DDC_STREAM_ID, int, True), \
                        ]

##
# \brief NBDDC configuration command.
#
class nbddc(wbddc):
    ## This should apply to the NDR470, NDR472, and NDR304
    mnemonic = "NBDDC"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.NBDDC_RF_INDEX,int,False,0), \
                        (configKeys.DDC_RATE_INDEX,int,False,0), \
                        (configKeys.DDC_UDP_DESTINATION,int,False,0), \
                        (configKeys.ENABLE,int,False,0), \
                        (configKeys.DDC_VITA_ENABLE,int,True,None), \
                        (configKeys.DDC_STREAM_ID,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.NBDDC_RF_INDEX, int, True), \
                        (configKeys.DDC_RATE_INDEX, int, True), \
                        (configKeys.DDC_UDP_DESTINATION, int, True), \
                        (configKeys.ENABLE, int, True), \
                        (configKeys.DDC_VITA_ENABLE, int, True), \
                        (configKeys.DDC_STREAM_ID, int, True), \
                        ]

##
# \brief WBDDC source select.
#
class wbss(_commandBase):
    mnemonic="WBSS"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.NBDDC_RF_INDEX,int,True,None), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.NBDDC_RF_INDEX, int, True), \
                        ]

##
# \brief NBDDC source select.
#
class nbss(_commandBase):
    mnemonic="NBSS"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.NBDDC_RF_INDEX,int,True,None), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.NBDDC_RF_INDEX, int, True), \
                        ]

##
# \brief WBDDC data port select.
#
class wbdp(_commandBase):
    mnemonic="WBDP"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.DDC_DATA_PORT,int,True,None), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DDC_DATA_PORT, int, True), \
                        ]


##
# \brief NBDDC data port select.
#
class nbdp(_commandBase):
    mnemonic="NBDP"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.DDC_DATA_PORT,int,True,None), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DDC_DATA_PORT, int, True), \
                        ]


#--  Networking Commands  ---------------------------------------------------#

##
# \brief Destination IP address configuration command.
#
# Supports radios which do not have dedicated Gigabit Ethernet ports.
class dip(_commandBase):
    mnemonic="DIP"
    setParameters = [ (configKeys.IP_DEST, str, True, None) ]
    queryResponseData = [ \
                        (configKeys.IP_DEST, str, False), \
                        ]
    
##
# \brief Destination MAC address configuration command.
#
# Supports radios which do not have dedicated Gigabit Ethernet ports.
class dmac(_commandBase):
    mnemonic="TDMAC"
    setParameters = [ (configKeys.MAC_DEST, str, True, None) ]
    queryResponseData = [ \
                        (configKeys.MAC_DEST, str, False), \
                        ]

##
# \brief Source IP address configuration command.
#
# Supports radios which do not have dedicated Gigabit Ethernet ports.
class sip(_commandBase):
    mnemonic="SIP"
    setParameters = [ (configKeys.IP_SOURCE, str, True, None) ]
    queryResponseData = [ \
                        (configKeys.IP_SOURCE, str, False), \
                        ]
    

##
# \brief Flow control configuration command.
#
# Supports radios which have dedicated Gigabit Ethernet ports.
class tgfc(_commandBase):
    mnemonic="TGFC"
    setParameters = [ (configKeys.GIGE_PORT_INDEX, int, True, None), \
                      (configKeys.GIGE_FLOW_CONTROL, int, True, None), \
                     ]
    queryParameters = [ (configKeys.GIGE_PORT_INDEX, int, True, None), \
                        ]
    queryResponseData = [ \
                        (configKeys.GIGE_PORT_INDEX, int, False), \
                        (configKeys.GIGE_FLOW_CONTROL, int, False), \
                        ]
    
##
# \brief Source MAC address configuration command.
#
# Supports radios which do not have dedicated Gigabit Ethernet ports.
class smac(_commandBase):
    mnemonic="#MAC"
    settable=False
    #setParameters = [ (configKeys.MAC_SOURCE, str, True, None) ]
    queryResponseData = [ \
                        (configKeys.MAC_SOURCE, str, False), \
                        ]

#--  GPS/Time Stuff  --------------------------------------------------------#

##
# \brief Pulse-per-second (PPS) command.
#
class pps(_commandBase):
    mnemonic="PPS"
    settable=False
    timeout=4
    
##
# \brief UTC time command.
#
class utc(_commandBase):
    mnemonic="UTC"
    timeout = 1.5
    setParameters = [ (configKeys.TIME_UTC,str,False,None) ]
    queryResponseData = [ (configKeys.TIME_UTC, int, False), \
                        ]

##
# \brief GPS enable command.
#
class gps(_commandBase):
    mnemonic="GPS"
    setParameters = [ (configKeys.GPS_ENABLE,int,False,0) ]
    queryResponseData = [ (configKeys.GPS_ENABLE, int, False), \
                        ]

##
# \brief GPS position query command.
#
class gpos(_commandBase):
    mnemonic="GPOS"
    settable=False
    queryResponseData = [ \
                        (configKeys.GPS_LATITUDE, str, False), \
                        (configKeys.GPS_LONGITUDE, str, False), \
                        ]


#--  Identity Command  ------------------------------------------------------#

##
# \brief Identity command.
#
# This command response differs per radio.
#
# For this command, getResponseInfo() returns a dictionary that may
# have the following entries:
# <ul>
# <li> "model": radio model
# <li> "serialNumber": radio serial number
# </ul>
#
class idn(_commandBase):
    mnemonic = "*IDN"
    settable = False

    # OVERRIDE
    ##
    # Parses the command response into the response information dictionary.
    def parseResponse(self):
        self.responseInfo = {}
        if self.rsp is not None:
            for rspLine in self.rsp:
                # Ignore lines that echo back the query command
                if "%s?" % self.mnemonic in rspLine:
                    continue
                # Ignore lines that contain command status
                elif any([q in rspLine.upper() for q in ["OK", "ERROR", "TIMEOUT", "EXCEPTION"]]):
                    continue
                # Start response parsing
                # -- NDR301 combines model and serial number in a single-line response
                if "-SN" in rspLine:
                    vec = rspLine.split("-SN")
                    self.responseInfo["model"] = vec[0]
                    self.responseInfo["serialNumber"] = vec[1]
                elif "S/N" in rspLine:
                    self.responseInfo["serialNumber"] = rspLine.replace("S/N ", "")
                else:
                    self.responseInfo["model"] = rspLine.replace(" Receiver", "")


#--  Software Version Command  ----------------------------------------------#

##
# \brief Software version command.
#
# This command response differs per radio.
#
# For this command, getResponseInfo() returns a dictionary that may
# have the following entries:
# <ul>
# <li> "softwareVersion": application version number
# <li> "firmwareVersion": FPGA software version number
# <li> "referenceVersion": Reference/timing version number
# </ul>
#
class ver(_commandBase):
    mnemonic = "VER"
    settable = False
    
    # OVERRIDE
    ##
    # Parses the command response into the response information dictionary.
    def parseResponse(self):
        self.responseInfo = {}
        if self.rsp is not None:
            for rspLine in self.rsp:
                # Ignore lines that echo back the query command
                if "%s?" % self.mnemonic in rspLine:
                    continue
                # Ignore lines that contain command status
                elif any([q in rspLine.upper() for q in ["OK", "ERROR", "TIMEOUT", "EXCEPTION"]]):
                    continue
                # Start response parsing
                if "REV: " in rspLine:
                    self.responseInfo["softwareVersion"] = rspLine.replace("REV: ", "")
                if "Rev: " in rspLine:
                    self.responseInfo["firmwareVersion"] = rspLine[rspLine.find("Rev:"):].split(" ")[1]
                if "Date:" in rspLine:
                    self.responseInfo["firmwareDate"] = rspLine[rspLine.find("Date:")+5:].strip()
                if "Reference Code Version: " in rspLine:
                    self.responseInfo["referenceVersion"] = rspLine[rspLine.find("Version:"):].split(" ")[1]
                if "NDR301 Version: " in rspLine:
                    self.responseInfo["softwareVersion"] = rspLine.replace("NDR301 Version: ", "")
                if "NDR301PTT Version: " in rspLine:
                    self.responseInfo["model"] = "NDR301PTT"
                    self.responseInfo["softwareVersion"] = rspLine.replace("NDR301PTT Version: ", "")
                if "FPGA Revision: " in rspLine:
                    self.responseInfo["firmwareVersion"] = rspLine.replace("FPGA Revision: ", "")
    
    
#--  Hardware Revision Command  ---------------------------------------------#

##
# \brief Hardware revision command.
#
# This command response differs per radio.
#
# For this command, getResponseInfo() returns a dictionary that may
# have the following entries:
# <ul>
# <li> "model": radio model
# <li> "serialNumber": radio serial number
# <li> "unitRevision": radio unit revision number
# <li> "hardwareVersion": list of strings
# </ul>
#
class hrev(_commandBase):
    mnemonic = "HREV"
    settable = False

    # OVERRIDE
    ##
    # Parses the command response into the response information dictionary.
    def parseResponse(self):
        self.responseInfo = {}
        if self.rsp is not None:
            hwVersionInfo = []
            lastwasunit=False
            for rspLine in self.rsp:
                # Ignore lines that echo back the query command
                if "%s?" % self.mnemonic in rspLine:
                    continue
                # Ignore lines that contain command status
                elif any([q in rspLine.upper() for q in ["OK", "ERROR", "TIMEOUT", "EXCEPTION"]]):
                    continue
                # Start response parsing
                if rspLine.strip() == "Unit":
                    lastwasunit=True
                    continue
                if lastwasunit and "Model: " in rspLine:
                    self.responseInfo["model"] = rspLine.replace("Model: ", "")
                elif "Unit Model: " in rspLine:
                    self.responseInfo["model"] = rspLine.replace("Unit Model: ", "")
                elif "Model: " in rspLine and " Receiver" in rspLine:
                    self.responseInfo["model"] = rspLine.replace("Model: ", "").replace(" Receiver", "")
                elif "S/N: " in rspLine and not self.responseInfo.has_key("serialNumber"):
                    self.responseInfo["serialNumber"] = rspLine.replace("S/N: ", "")
                elif "Unit Serial Number: " in rspLine and not self.responseInfo.has_key("serialNumber"):
                    self.responseInfo["serialNumber"] = rspLine.replace("Unit Serial Number: ", "")
                elif "Serial: " in rspLine and not self.responseInfo.has_key("serialNumber"):
                    self.responseInfo["serialNumber"] = rspLine.replace("Serial: ", "")
                elif "Unit Revision: " in rspLine and not self.responseInfo.has_key("unitRevision"):
                    self.responseInfo["unitRevision"] = rspLine.replace("Unit Revision: ", "")
                elif "Revision: " in rspLine and not self.responseInfo.has_key("unitRevision"):
                    self.responseInfo["unitRevision"] = rspLine.replace("Revision: ", "")
                else:
                    hwVersionInfo.append(rspLine)
                lastwasunit=False    
            if len(hwVersionInfo) > 0:
                self.responseInfo["hardwareVersion"] = ", ".join(hwVersionInfo)

#--  Status Query Command  ---------------------------------------------#

#--  Timing Adjustment Command  ---------------------------------------------#

##
# \brief Timing adjustment command.
#
class tadj(_commandBase):
    mnemonic="TADJ"
    setParameters = [ (configKeys.INDEX,int,True,None), \
                        (configKeys.TUNER_TIMING_ADJ,int,True,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_TIMING_ADJ, int, True), \
                        ]

#--  Calibration Frequency Command  ---------------------------------------------#

##
# \brief Calibration frequency command.
#
class calf(_commandBase):
    mnemonic="CALF"
    setParameters = [ (configKeys.CALIB_FREQUENCY, float, False, None), \
                        ]
    queryParameters = [ ]
    queryResponseData = [ \
                        (configKeys.CALIB_FREQUENCY, float, False), \
                        ]

#--  Frequency Normalization Command  ---------------------------------------------#

##
# \brief Frequency normalization command.
#
class fnr(_commandBase):
    mnemonic="FNR"
    setParameters = [ (configKeys.FNR_MODE,int,False,0) ]
    queryResponseData = [ (configKeys.FNR_MODE, int, False), \
                        ]

#--  Reset Command  ---------------------------------------------------------#

##
# \brief Radio reset command.
#
class reset(_commandBase):
    mnemonic = "*RST"

#--  Reference and Bypass Commands  -----------------------------------------#

##
# \brief Reference mode command.
#
class ref(_commandBase):
    mnemonic = "REF"
    timeout = 5
    setParameters = [ (configKeys.REFERENCE_MODE,int,False,0) ]
    queryResponseData = [ (configKeys.REFERENCE_MODE, int, False), \
                        ]

##
# \brief Reference mode bypass command.
#
class rbyp(_commandBase):
    mnemonic = "RBYP"
    setParameters = [ (configKeys.BYPASS_MODE,int,False,0) ]
    queryResponseData = [ (configKeys.BYPASS_MODE, int, False), \
                        ]

#--  Reference Tuning Voltage Commands  --------------------------------------#

##
# \brief Reference tuning voltage command.
#
class rtv(_commandBase):
    mnemonic="RTV"
    setParameters = [ (configKeys.REF_TUNING_VOLT, int, False, 0) ]
    queryResponseData = [ (configKeys.REF_TUNING_VOLT, int, False), \
                        ]

#--  Tuner Commands  ---------------------------------------------------------#

##
# \brief Tuner power command.
#
class tpwr(_commandBase):
    mnemonic = "TPWR"
    setParameters = [ (configKeys.INDEX,int,False,None), \
                      (configKeys.ENABLE,int,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ (configKeys.INDEX, int, False), \
                          (configKeys.ENABLE, int, True), \
                        ]

##
# \brief Tuner filter setting command.
#
class fif(_commandBase):
    mnemonic = "FIF"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.TUNER_FILTER,int,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.TUNER_FILTER, int, True), \
                        ]
    
#--  Configuration Commands  -------------------------------------------------#

##
# \brief Configuration mode command.
#
class cfg(_commandBase):
    mnemonic = "CFG"
    setParameters = [ (configKeys.CONFIG_MODE,int,False,0), \
                    ]
    queryParameters = [ \
                        ]
    queryResponseData = [ (configKeys.CONFIG_MODE, int, True), \
                        ]


#--  Status Commands  ---------------------------------------------------------#

##
# \brief Status command.
#
# Static member "statTextValues" is a dictionary where the keys are bits in 
# the status bitmask, and the values are text strings indicating what those 
# bits mean when set.
#
# The response information dictionary for the status command contains the
# following keywords:
# <ul>
# <li> "int": The status bitmask returned by the radio, as an integer.
# <li> "statValues": The list of bits in status bitmask that are set.
# <li> "statText": The list of strings that describe the bits that are set.
# </ul>
#
class stat(_commandBase):
    mnemonic = "STAT"
    settable = False
    statTextValues = {}
    timeout = 5.0
    
    # OVERRIDE
    ##
    # \brief Parses the command response into the response information dictionary.
    def parseResponse(self):
        self.logIfVerbose("Parsing %s response" % self.mnemonic)
        try:
            self.responseInfo = {}
            if self.rsp is not None:
                for i in self.rsp:
                    line = i.lower()
                    if "tstat" in line:
                        line = line.replace("tstat ", "")
                    elif "stat" in line:
                        line = line.replace("stat ", "")
                    if "0x" in line:
                        statRes = int( line.strip(), 16 )
                        self.responseInfo["int"] = statRes
                        self.responseInfo["statValues"] = []
                        self.responseInfo["statText"] = []
                        for i in range(32):
                            mask = (2**i)
#                            if statRes&mask == mask:
                            if (statRes&mask)>0:
                                self.responseInfo["statValues"].append(mask)
                                if mask in self.statTextValues.keys():
                                    self.responseInfo["statText"].append(self.statTextValues.get(mask))
                        break
        except:
            self.logIfVerbose(traceback.format_exc())
            self.responseInfo = None
        return self.responseInfo


##
# \brief Generic Status Query command for JSON-oriented radios.
#
# This is mostly intended for radio auto-detection.
#
class status_json(_jsonCommandBase):
    mnemonic = "status"
    settable = False
    queryParamMap = {
                configKeys.VERINFO_MODEL: "model",
                configKeys.VERINFO_SN: "sn",
                configKeys.VERINFO_UNITREV: "unit",
                configKeys.VERINFO_SW: "sw",
                configKeys.VERINFO_FW: "fw",
                }
    
        
# Radio-specific STAT commands.  Each radio also has a class associated with
# it that provides the meanings for the bits in its status bitmask.

#--  TSTAT Commands  --------------------------------------------------------#

##
# \brief Tuner RF status command.
#
# \copydetails stat
#
class tstat(stat):
    mnemonic = "TSTAT"

# Radio-specific TSTAT commands.

##
# \brief Temperature query command.
#
class temp(_commandBase):
    mnemonic="TEMP"
    settable=False
    queryResponseData = [ \
                        (configKeys.TEMPERATURE, int, False), \
                        ]


#--  GPIO Commands  ------------------------------------------------------#
# The GPIO command is weird in that the format changes depending on
# what GPIO output mode the user uses (static or programmed sequence).
# The query form (GPIO?) actually returns different output based on the
# last GPIO command that was issued.

##
# \brief GPIO pin setting command (static mode).
#
class gpio_static(_commandBase):
    mnemonic = "GPIO"
    setParameters = [   (configKeys.GPIO_VALUE,int,False,0), \
                        ]
    queryParameters = [ ]
    queryResponseData = [ \
                        (configKeys.GPIO_VALUE, maybeHex, False), \
                        ]

##
# \brief GPIO pin setting command (sequence mode).
#
class gpio_sequence(_commandBase):
    mnemonic = "GPIO"
    setParameters = [   (configKeys.INDEX,int,False,None), \
                        (configKeys.GPIO_VALUE,int,False,0), \
                        (configKeys.GPIO_DURATION,int,False,0), \
                        (configKeys.GPIO_LOOP,int,False,0), \
                        (configKeys.GPIO_GO,int,False,0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.GPIO_VALUE, maybeHex, False), \
                        (configKeys.GPIO_DURATION, int, True), \
                        (configKeys.GPIO_LOOP, int, True), \
                        ]


#--  TX Commands  --------------------------------------------------------#

##
# \brief Transmitter center frequency command.
#
class txf(_commandBase):
    mnemonic = "TXF"
    setParameters = [   (configKeys.TX_INDEX,int,False,None), \
                        (configKeys.TX_FREQUENCY,float,False,1000), \
                        ]
    queryParameters = [ (configKeys.TX_INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.TX_INDEX, int, False), \
                        (configKeys.TX_FREQUENCY, float, True), \
                        ]
    
##
# \brief Transmitter attenuation command.
#
class txa(_commandBase):
    mnemonic = "TXA"
    setParameters = [   (configKeys.TX_INDEX,int,False,None), \
                        (configKeys.TX_ATTENUATION,float,False,0), \
                        ]
    queryParameters = [ (configKeys.TX_INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.TX_INDEX, int, False), \
                        (configKeys.TX_ATTENUATION, float, True), \
                        ]
    
##
# \brief Transmitter power command.
#
class txp(_commandBase):
    mnemonic = "TXP"
    setParameters = [   (configKeys.TX_INDEX,int,False,None), \
                        (configKeys.ENABLE,int,False,0), \
                        ]
    queryParameters = [ (configKeys.TX_INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.TX_INDEX, int, False), \
                        (configKeys.ENABLE, int, True), \
                        ]
    
#--  CW Tone Generation Commands  ------------------------------------------#

##
# \brief CW tone generator tone characteristics command.
#
class cwt(_commandBase):
    mnemonic = "CWT"
    setParameters = [   (configKeys.TX_INDEX,int,False,None), \
                        (configKeys.CW_INDEX,int,False,None), \
                        (configKeys.CW_FREQUENCY,float,False,None), \
                        (configKeys.CW_AMPLITUDE,int,False,None), \
                        (configKeys.CW_PHASE,int,False,None), \
                        ]
    queryParameters = [ (configKeys.TX_INDEX,int,True,None), \
                        (configKeys.CW_INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.TX_INDEX, int, False), \
                        (configKeys.CW_INDEX, int, False), \
                        (configKeys.CW_FREQUENCY, float, True), \
                        (configKeys.CW_AMPLITUDE, int, False), \
                        (configKeys.CW_PHASE, int, False), \
                        ]

##
# \brief CW tone generator sweep command.
#
class cws(_commandBase):
    mnemonic = "CWS"
    setParameters = [   (configKeys.TX_INDEX,int,False,None), \
                        (configKeys.CW_INDEX,int,False,None), \
                        (configKeys.CW_SWEEP_START,float,False,None), \
                        (configKeys.CW_SWEEP_STOP,float,False,None), \
                        (configKeys.CW_SWEEP_STEP,float,False,None), \
                        (configKeys.CW_SWEEP_DWELL,int,False,None), \
                        ]
    queryParameters = [ (configKeys.TX_INDEX,int,True,None), \
                        (configKeys.CW_INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.TX_INDEX, int, False), \
                        (configKeys.CW_INDEX, int, False), \
                        (configKeys.CW_SWEEP_START, float, True), \
                        (configKeys.CW_SWEEP_STOP, float, True), \
                        (configKeys.CW_SWEEP_STEP, float, True), \
                        (configKeys.CW_SWEEP_DWELL, int, False), \
                        ]

#--  DUC Commands  ------------------------------------------#

##
# \brief WBDUC configuration command.
#
class wbduc(_commandBase):
    ## This should apply to the NDR651
    mnemonic = "WBDUC"
    setParameters = [   (configKeys.DUC_INDEX, int, False, None), \
                        (configKeys.DUC_DATA_PORT, int, False, 1), \
                        (configKeys.DUC_FREQUENCY, float, False, 0.0), \
                        (configKeys.DUC_ATTENUATION, float, False, 0.0), \
                        (configKeys.DUC_RATE_INDEX, int, False, 0), \
                        (configKeys.DUC_TX_CHANNELS, int, False, 0), \
                        (configKeys.DUC_MODE, int, False, 0), \
                        (configKeys.DUC_STREAM_ID, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.DUC_INDEX, int, True, None), \
                        ]
    queryResponseData = [ \
                        (configKeys.DUC_INDEX, int, False), \
                        (configKeys.DUC_DATA_PORT, int, False), \
                        (configKeys.DUC_FREQUENCY, float, False), \
                        (configKeys.DUC_ATTENUATION, float, False), \
                        (configKeys.DUC_RATE_INDEX, int, False), \
                        (configKeys.DUC_TX_CHANNELS, int, False), \
                        (configKeys.DUC_MODE, int, False), \
                        (configKeys.DUC_STREAM_ID, int, False), \
                        ]


##
# DUC configuration command.
#
class duc(_commandBase):
    ## This should apply to the NDR651
    mnemonic = "DUC"
    setParameters = [   (configKeys.DUC_INDEX, int, False, None), \
                        (configKeys.DUC_DATA_PORT, int, False, 1), \
                        (configKeys.DUC_FREQUENCY, float, False, 0.0), \
                        (configKeys.DUC_ATTENUATION, float, False, 0.0), \
                        (configKeys.DUC_RATE_INDEX, int, False, 0), \
                        (configKeys.DUC_TX_CHANNELS, int, False, 0), \
                        (configKeys.DUC_MODE, int, False, 0), \
                        (configKeys.DUC_STREAM_ID, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.DUC_INDEX, int, True, None), \
                        ]
    queryResponseData = [ \
                        (configKeys.DUC_INDEX, int, False), \
                        (configKeys.DUC_DATA_PORT, int, False), \
                        (configKeys.DUC_FREQUENCY, float, False), \
                        (configKeys.DUC_ATTENUATION, float, False), \
                        (configKeys.DUC_RATE_INDEX, int, False), \
                        (configKeys.DUC_TX_CHANNELS, int, False), \
                        (configKeys.DUC_MODE, int, False), \
                        (configKeys.DUC_STREAM_ID, int, False), \
                        ]


##
# \brief WBDUC trasmit snapshot command.
# \deprecated
#
class txsd(_commandBase):
    ## This should apply to the NDR651
    mnemonic = "TXSD"
    setParameters = [   (configKeys.DUC_INDEX, int, False, None), \
                        (configKeys.DUC_START_BLOCK, int, False, 0), \
                        (configKeys.DUC_END_BLOCK, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.DUC_INDEX, int, True, None), \
                        ]
    queryResponseData = [ \
                        (configKeys.DUC_INDEX, int, False), \
                        (configKeys.DUC_START_BLOCK, int, True), \
                        (configKeys.DUC_END_BLOCK, int, True), \
                        ]


##
# \brief DUC load waveform command.
#
# \note Settable only
#
class lwf(_commandBase):
    ## This should apply to the NDR651
    mnemonic = "LWF"
    queryable = False
    setParameters = [   (configKeys.DUC_FILENAME, str, False, None), \
                        (configKeys.DUC_INDEX, int, False, None), \
                        (configKeys.DUC_START_SAMPLE, int, False, 0), \
                        (configKeys.DUC_SAMPLES, int, False, 0), \
                        ]
    queryParameters = [ ]
    queryResponseData = [ ]


##
# \brief DUC play waveform command.
#
# \note Settable only
class pwf(_commandBase):
    ## This should apply to the NDR651
    mnemonic = "PWF"
    queryable = False
    setParameters = [   (configKeys.DUC_INDEX, int, False, None), \
                        (configKeys.DUC_START_SAMPLE, int, False, 0), \
                        (configKeys.DUC_SAMPLES, int, False, 0), \
                        (configKeys.DUC_SINGLE_PLAYBACK, int, False, 0), \
                        ]
    queryParameters = [ ]
    queryResponseData = [ ]



#--  Miscellaneous Commands  -----------------------------------#

#--  DDC Group Configuration Commands  --------------------------------------------#

##
# \brief WBDDC group configuration command.
#
class wbg(_commandBase):
    mnemonic = "WBG"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.DDC_GROUP_MEMBER, int, False, 0), \
                        (configKeys.ENABLE, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        (configKeys.DDC_GROUP_MEMBER,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DDC_GROUP_MEMBER, int, True), \
                        (configKeys.ENABLE, int, True), \
                        ]

##
# \brief WBDDC group enable command.
#
class wbge(_commandBase):
    mnemonic = "WBGE"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.ENABLE, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.ENABLE, int, True), \
                        ]

##
# \brief NBDDC group configuration command.
#
class nbg(_commandBase):
    mnemonic = "NBG"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.DDC_GROUP_MEMBER, int, False, 0), \
                        (configKeys.ENABLE, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        (configKeys.DDC_GROUP_MEMBER,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DDC_GROUP_MEMBER, int, True), \
                        (configKeys.ENABLE, int, True), \
                        ]

##
# \brief NBDDC group enable command.
#
class nbge(_commandBase):
    mnemonic = "NBGE"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.ENABLE, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.ENABLE, int, True), \
                        ]

#--  DUC Group Configuration Commands  --------------------------------------------#

##
# \brief DUC group configuration command.
#
class ducg(_commandBase):
    mnemonic = "DUCG"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.DUC_GROUP_MEMBER, int, False, 0), \
                        (configKeys.ENABLE, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        (configKeys.DUC_GROUP_MEMBER,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.DUC_GROUP_MEMBER, int, True), \
                        (configKeys.ENABLE, int, True), \
                        ]

##
# \brief DUC group enable command.
#
class ducge(_commandBase):
    mnemonic = "DUCGE"
    setParameters = [   (configKeys.INDEX, int, False, None), \
                        (configKeys.ENABLE, int, False, 0), \
                        ]
    queryParameters = [ (configKeys.INDEX,int,True,None), \
                        ]
    queryResponseData = [ \
                        (configKeys.INDEX, int, False), \
                        (configKeys.ENABLE, int, True), \
                        ]


#--  ADC Configuration Commands  --------------------------------------------#

##
# \brief ADC sample rate mode command.
#
class adcsr(_commandBase):
    mnemonic = "ADCSR"
    setParameters = [   (configKeys.ADC_RATE_MODE, int, False, None), \
                        ]
    queryParameters = [ ]
    queryResponseData = [ \
                        (configKeys.ADC_RATE_MODE, int, True), \
                        ]


#-- FPGA State Selection Commands  ------------------------------------------#

##
# \brief FPGA state selection command.
#
class fun(_jsonCommandBase):
    mnemonic = "fun"
    setParamMap = {
                configKeys.FPGA_STATE: "state",
                 }
    queryParamMap = {
                configKeys.FPGA_STATE: "state",
                 }


