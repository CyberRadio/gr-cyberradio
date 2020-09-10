#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver.log
# 
# Logging support for objects within the driver.  
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2017-2020 CyberRadio Solutions, Inc.  
#    All rights reserved.
#
###############################################################

# Imports from other modules in this package
# Imports from external modules
# Python standard library imports
import json
import sys
import time
#from matplotlib import verbose

##
# Base class for objects that produce log output.
#
# This base class consumes the following keyword arguments in
# its constructor:
# -- "verbose": a Boolean value (defaults to True) that 
#    controls verbose mode
# -- "logFile": Indicates where the log output should go.  This
#    is an open file or a file-like object that can consume the
#    log output.  The default is standard output.  If specified 
#    as None, log output will be disabled altogether.
class _logger(object):
    
    ##
    # Constructor
    def __init__(self, *args, **kwargs):
        # Consume this class's keyword arguments.
        self.verbose = kwargs.get("verbose", True)
        self.logFile = kwargs.get("logFile", sys.stdout)
        
#     def __myClassName(self):
#         ret = str(self.__class__).replace("<class ","").replace("'","").replace(">","")
#         return ret

    ##
    # Writes output to the log.
    #
    # \param args A variable-length list of items to write to the
    # log.  Each item needs to be representable as a string.  Items
    # are separated by spaces in the output.
    def log(self, *args):
        if self.logFile is not None:
            myname = str(self).strip()
            message = " ".join([str(q) for q in args])
            #self.logFile.write("[%s] " % self.__myClassName())
            if myname is None:
                self.logFile.write("%s :: %s" % (time.strftime("%x %X"), 
                                                   message))
            else:
                # This construct looks strange, but the idea behind it is: "Don't 
                # print my so-called 'name' if my string representation is 
                # actually a JSON command".
                try:
                    json.loads(myname)
                    self.logFile.write("%s :: %s" % (time.strftime("%x %X"), 
                                                       message))
                except:
                    self.logFile.write("%s %s :: %s" % (time.strftime("%x %X"), 
                                                          myname, message))
            self.logFile.write("\n")
            self.logFile.flush()
                
    ##
    # Writes verbose-mode output to the log.
    #
    # \param args A variable-length list of items to write to the
    # log.  Each item needs to be representable as a string.  Items
    # are separated by spaces in the output.
    def logIfVerbose(self, *args):
        if self.verbose:
            self.log(*args)
    
    ##
    # Gets whether or not the object is in verbose mode.
    #
    # \returns True if verbose mode is set, False otherwise.
    def getVerbose(self):
        return self.verbose
    
    ##
    # Sets whether or not the object is in verbose mode.
    #
    # \param verbose True if verbose mode is set, False otherwise.
    def setVerbose(self, verbose):
        self.verbose = verbose
        
    ##
    # Gets the object's log file.
    #
    # \returns The file or file-like object used for logging.
    def getLogFile(self):
        return self.logFile
    
    ##
    # Sets the object's log file.
    #
    # \param logFile The file or file-like object used for logging.  If None,
    #     disables logging.
    def setLogFile(self, logFile):
        self.logFile = logFile

