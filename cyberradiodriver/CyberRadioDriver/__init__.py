#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver
# 
# \brief The CyberRadio Solutions NDR Radio Driver module 
# (CyberRadioDriver) provides users with a common application programming 
# interface (API) for all CyberRadio Solutions NDR-class radios.
#
# End-users of the driver should obtain a radio handler object for
# their radio(s) by calling CyberRadioDriver.getRadioObject() with the name
# string for the desired radio.  They can then use the methods provided 
# by the CyberRadioDriver.IRadio interface to manipulate their radio handler
# object.
#
# The driver package documentation also includes other modules and objects.  
# These implement the high-level functionality exposed by 
# CyberRadioDriver.getRadioObject() and the CyberRadioDriver.IRadio interface.
# However, these items will be of little interest to end-users.  They are 
# included mainly for the benefit of those who maintain the driver.
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.  All rights 
# reserved.
#
###############################################################

###############################################################
# \mainpage CyberRadio Solutions NDR Radio Driver for Python
#
# \section Description
#
# The CyberRadio Solutions NDR Radio Driver module (CyberRadioDriver) 
# provides users with a common application programming interface 
# (API) for all CyberRadio Solutions NDR-class radios.
#
# End-users of the driver should obtain a radio handler object for
# their radio(s) by calling CyberRadioDriver.getRadioObject() with the name
# string for the desired radio.  They can then use the methods provided 
# by the CyberRadioDriver.IRadio interface to manipulate their radio handler
# object.
#
# The driver package documentation also includes other modules and objects.  
# These implement the high-level functionality exposed by 
# CyberRadioDriver.getRadioObject() and the CyberRadioDriver.IRadio interface.
# However, these items will be of little interest to end-users.  They are 
# included mainly for the benefit of those who maintain the driver.
#
# \section SupportedRadios Supported Radios
#
# <table>
#    <tr><th>Radio</th><th>Name String</th></tr>
#    <tr><td>\link CyberRadioDriver::radio::ndr304 NDR304 \endlink</td><td>"ndr304"</td></tr>
#    <tr><td>\link CyberRadioDriver::radio::ndr308_1 NDR308-1 \endlink</td><td>"ndr308_1"</td></tr>
#    <tr><td>\link CyberRadioDriver::radio::ndr308ts NDR308-TS \endlink</td><td>"ndr308ts"</td></tr>
#    <tr><td>\link CyberRadioDriver::radio::ndr308 NDR308 \endlink</td><td>"ndr308"</td></tr>
#    <tr><td>\link CyberRadioDriver::radio::ndr651 NDR651 \endlink</td><td>"ndr651"</td></tr>
# </table>
#
# The name string from this table is used in 
# CyberRadioDriver.getRadioObject() to get a radio handler object
# for a particular radio.
#
###############################################################

import inspect, sys
import socket, fcntl, struct
from command import radio_command
import radio, configKeys

##
# \brief Driver module name (string).
name = "CyberRadioDriver"
##
# \brief Driver module description (string).
description = "CyberRadio Solutions NDR Driver"
##
# \brief Driver version number (string).
version = "16.01.05"

# This section of code inspects the "radio" module for radio handler
# objects (objects derived from _radio, thus implementing the IRadio interface)
# and imports those objects into this module's namespace (that is, it mirrors
# a "from radio import <radio handler class>" statement).
for objname, obj in inspect.getmembers(radio):
    if inspect.isclass(obj) and issubclass(obj, radio._radio) \
      and "_radio" not in objname:
        # Import that object into this module's namespace.
        setattr(sys.modules[__name__], objname, obj)
        
##
# \brief Returns the MAC address and IP address for a given Ethernet 
#    interface.
#
# \param ifname The name of the Ethernet system interface ("eth0", for 
#    example).
# \returns A 2-tuple: (MAC Address string, IP Address string).  If the
#    given interface does not exist, then both returned strings will be
#    empty strings.
def getInterfaceAddresses(ifname):
    mac = ""
    ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        mac = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])
    except:
        pass
    return mac,ip

##
# \brief Gets the list of supported radios.
# \return The list of supported radios.
def getSupportedRadios():
    return sorted(radio._radio_class_map.keys())

##
# \brief Factory method for obtaining a radio handler class name from the name
# of the radio.
#
# The name string used to identify the radio can be any string returned 
# by getSupportedRadios(), but the check is not case-sensitive.
#
# \param nameString The name string for the radio of interest.
# \returns The radio handler class name for the desired radio.
# \throws RuntimeError if the desired radio is not supported.
def getRadioClass(nameString):
    return radio.getRadioObject(nameString)

##
# \brief Factory method for obtaining a radio handler object from the name
# of the radio.
#
# The name string used to identify the radio can be any string returned 
# by getSupportedRadios(), but the check is not case-sensitive.  The 
# returned radio handler object will support the CyberRadioDriver.IRadio interface.
#
# \param nameString The name string for the radio of interest.
# \param args Variable-length list of positional arguments.  Positional
#     arguments are ignored.
# \param kwargs Dictionary of keyword arguments to pass to the radio
#     handler object.  Which keyword arguments are valid depends on the 
#     specific radio.  Unsupported keyword arguments will be ignored.
# \returns A radio handler object for the desired radio.
# \throws RuntimeError if the desired radio is not supported.
def getRadioObject(nameString, *args, **kwargs):
    return getRadioClass(nameString)(*args, **kwargs)

##
# \brief Factory method for obtaining a documentation string for a 
# radio handler object from the name of the radio.
#
# The name string used to identify the radio can be any string returned 
# by getSupportedRadios(), but the check is not case-sensitive.  The 
# documentation block returned is compatible with Doxygen. 
#
# \param nameString The name string for the radio of interest.
# \returns A documentation block for the corresponding radio handler
#    object.
# \throws RuntimeError if the desired radio is not supported.
def getRadioObjectDocstring(nameString):
    radioClass = getRadioClass(nameString)
    outstr = """##
# \\brief Radio handler class for the {name}.
#
# This class implements the CyberRadioDriver.IRadio interface.
#
# \\section ConnectionModes_{name} Connection Modes
#
# {modes}
#
# \\section RadioConfig_{name} Radio Configuration Options
#
# \\code
# configDict = {{
""".format(name=radioClass._name, 
           modes=", ".join(['"%s"' % mode for mode in radioClass.getConnectionModeList()]))
    if radioClass.cfgCmd is not None:
        outstr += """#      "{keyword}": {range},
""".format(keyword=configKeys.CONFIG_MODE, 
           range=str([0,1]))
    if radioClass.refCmd is not None:
        outstr += """#      "{keyword}": {range},
""".format(keyword=configKeys.REFERENCE_MODE, 
           range=str(sorted(radioClass.refModes.keys())))
    if radioClass.rbypCmd is not None:
        outstr += """#      "{keyword}": {range},
""".format(keyword=configKeys.BYPASS_MODE,
           range=str(sorted(radioClass.rbypModes.keys())))
    if radioClass.calfCmd is not None:
        outstr += """#      "{keyword}": {range},
""".format(keyword=configKeys.CALIB_FREQUENCY,
           range="[0, 25.0-3000.0]")
    if radioClass.numTuner > 0:
        outstr += """#      "{keyword}": {{
""".format(keyword=configKeys.CONFIG_TUNER)
        outstr += """#            {min}: {{
""".format(min=radioClass.getTunerIndexRange()[0])
        for i, key in enumerate(radioClass.tunerType.validConfigurationKeywords):
            if key == configKeys.ENABLE:
                outstr += """#               "{keyword}": {range},
""".format(keyword=configKeys.ENABLE, 
           range=str([0,1]))
            elif key == configKeys.TUNER_FREQUENCY:
                outstr += """#               "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.TUNER_FREQUENCY, 
               min=radioClass.getTunerFrequencyRange()[0],
               max=radioClass.getTunerFrequencyRange()[1],
               step=radioClass.getTunerFrequencyRes())
            elif key == configKeys.TUNER_ATTENUATION:
                outstr += """#               "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.TUNER_ATTENUATION, 
               min=radioClass.getTunerAttenuationRange()[0],
               max=radioClass.getTunerAttenuationRange()[1],
               step=radioClass.getTunerAttenuationRes())
        outstr += """#            },
"""
        if radioClass.getNumTuner() > 1:
            outstr += """#         ...{max} (repeat for each tuner)
""".format(max=radioClass.getTunerIndexRange()[-1])
        outstr += """#      },
"""
    if radioClass.getNumTuner() > 0 or radioClass.getNumNbddc() > 0:
        outstr += """#      "{keyword}": {{
""".format(keyword=configKeys.CONFIG_DDC)
        if radioClass.getNumTuner() > 0:
            outstr += """#         "{keyword}": {{
""".format(keyword=configKeys.CONFIG_WBDDC)
            outstr += """#              {min}: {{
""".format(min=radioClass.getWbddcIndexRange()[0])
            for i, key in enumerate(radioClass.wbddcType.validConfigurationKeywords):
                if key == configKeys.ENABLE:
                    outstr += """#                 "{keyword}": {range},
""".format(keyword=configKeys.ENABLE, 
           range=str([0,1]))
                elif key == configKeys.DDC_RATE_INDEX:
                    outstr += """#                 "{keyword}": {range},
""".format(keyword=configKeys.DDC_RATE_INDEX, 
           range=str(sorted(radioClass.getWbddcRateSet().keys())))
                elif key == configKeys.DDC_UDP_DESTINATION:
                    outstr += """#                 "{keyword}": [{destination}],
""".format(keyword=configKeys.DDC_UDP_DESTINATION,
           destination=radioClass.udpDestInfo)
                elif key == configKeys.DDC_VITA_ENABLE:
                    outstr += """#                 "{keyword}": {range},
""".format(keyword=configKeys.DDC_VITA_ENABLE,
           range=str(sorted(radioClass.getVitaEnableOptionSet().keys())))
                elif key == configKeys.DDC_STREAM_ID:
                    outstr += """#                 "{keyword}": [stream ID],
""".format(keyword=configKeys.DDC_STREAM_ID)
                elif key == configKeys.DDC_FREQUENCY_OFFSET:
                    outstr += """#                 "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.DDC_FREQUENCY_OFFSET,
               min=radioClass.getWbddcFrequencyRange()[0],
               max=radioClass.getWbddcFrequencyRange()[1],
               step=radioClass.getWbddcFrequencyRes())
            outstr += """#              },
"""
            if radioClass.getNumTuner() > 1:
                outstr += """#           ...{max} (repeat for each WBDDC)
""".format(max=radioClass.getWbddcIndexRange()[-1])
            outstr += """#         },
"""
        if radioClass.getNumNbddc() > 0:
            outstr += """#         "{keyword}": {{
""".format(keyword=configKeys.CONFIG_NBDDC)
            outstr += """#              {min}: {{
""".format(min=radioClass.getNbddcIndexRange()[0])
            for i, key in enumerate(radioClass.nbddcType.validConfigurationKeywords):
                if key == configKeys.ENABLE:
                    outstr += """#                 "{keyword}": {range},
""".format(keyword=configKeys.ENABLE, 
           range=str([0,1]))
                elif key == configKeys.DDC_RATE_INDEX:
                    outstr += """#                 "{keyword}": {range},
""".format(keyword=configKeys.DDC_RATE_INDEX, 
           range=str(sorted(radioClass.getNbddcRateSet().keys())))
                elif key == configKeys.DDC_UDP_DESTINATION:
                    outstr += """#                 "{keyword}": [{destination}],
""".format(keyword=configKeys.DDC_UDP_DESTINATION,
           destination=radioClass.udpDestInfo)
                elif key == configKeys.DDC_VITA_ENABLE:
                    outstr += """#                 "{keyword}": {range},
""".format(keyword=configKeys.DDC_VITA_ENABLE,
           range=str(sorted(radioClass.getVitaEnableOptionSet().keys())))
                elif key == configKeys.DDC_STREAM_ID:
                    outstr += """#                 "{keyword}": [stream ID],
""".format(keyword=configKeys.DDC_STREAM_ID)
                elif key == configKeys.DDC_FREQUENCY_OFFSET:
                    outstr += """#                 "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.DDC_FREQUENCY_OFFSET,
               min=radioClass.getNbddcFrequencyRange()[0],
               max=radioClass.getNbddcFrequencyRange()[1],
               step=radioClass.getNbddcFrequencyRes())
                elif key == configKeys.NBDDC_RF_INDEX:
                    outstr += """#                 "{keyword}": {range},
""".format(keyword=configKeys.NBDDC_RF_INDEX,
           range=str(radioClass.getTunerIndexRange()))
            outstr += """#              },
"""
            if radioClass.getNumNbddc() > 1:
                outstr += """#           ...{max} (repeat for each NBDDC)
""".format(max=radioClass.getNbddcIndexRange()[-1])
            outstr += """#         },
"""
        outstr += """#      },
"""

    if any([radioClass.sipCmd is not None, radioClass.dipCmd is not None]):
        outstr += """#      "{keyword}": {{
""".format(keyword=configKeys.CONFIG_IP)
        if radioClass.getNumGigE() == 0:
            if radioClass.sipCmd is not None:
                outstr += """#         "{keyword}": [IP address],
""".format(keyword=configKeys.IP_SOURCE)
            if radioClass.dipCmd is not None:
                outstr += """#         "{keyword}": [IP address],
""".format(keyword=configKeys.IP_DEST)
            if radioClass.smacCmd is not None:
                outstr += """#         "{keyword}": [MAC address{readonly}],
""".format(keyword=configKeys.MAC_SOURCE,
           readonly="" if radioClass.smacCmd.settable else " (read-only)")
            if radioClass.dmacCmd is not None:
                outstr += """#         "{keyword}": [MAC address],
""".format(keyword=configKeys.MAC_DEST)
        else:
            outstr += """#            {min}: {{
""".format(min=radioClass.getGigEIndexRange()[0])
            if radioClass.sipCmd is not None:
                outstr += """#               "{keyword}": [IP address],
""".format(keyword=configKeys.IP_SOURCE)
            if radioClass.dipCmd is not None:
                outstr += """#               "{keyword}": {{
""".format(keyword=configKeys.IP_DEST)
                outstr += """#                   {min}: {{
""".format(min=radioClass.getGigEDipEntryIndexRange()[0])
                outstr += """#                      "{keyword}": [IP address],
""".format(keyword=configKeys.GIGE_IP_ADDR)
                outstr += """#                      "{keyword}": [MAC address],
""".format(keyword=configKeys.GIGE_MAC_ADDR)
                outstr += """#                      "{keyword}": [port],
""".format(keyword=configKeys.GIGE_SOURCE_PORT)
                outstr += """#                      "{keyword}": [port],
""".format(keyword=configKeys.GIGE_DEST_PORT)
                outstr += """#                   },
"""
                if radioClass.getNumGigEDipEntries() > 1:
                    outstr += """#                ...{max} (repeat for each DIP table entry)
""".format(max=radioClass.getGigEDipEntryIndexRange()[-1])
                outstr += """#               },
"""
            outstr += """#            },
"""
            if radioClass.getNumGigE() > 1:
                outstr += """#         ...{max} (repeat for each Gigabit Ethernet port)
""".format(max=radioClass.getGigEIndexRange()[-1])
        outstr += """#      },
"""
    if radioClass.getNumTransmitters() > 0:
        outstr += """#      "{keyword}": {{
""".format(keyword=configKeys.CONFIG_TX)
        outstr += """#            {min}: {{
""".format(min=radioClass.getTransmitterIndexRange()[0])
        for i, key in enumerate(radioClass.txType.validConfigurationKeywords):
            if key == configKeys.ENABLE:
                outstr += """#               "{keyword}": {range},
""".format(keyword=configKeys.ENABLE, 
           range=str([0,1]))
            elif key == configKeys.TX_FREQUENCY:
                outstr += """#               "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.TX_FREQUENCY, 
               min=radioClass.getTransmitterFrequencyRange()[0],
               max=radioClass.getTransmitterFrequencyRange()[1],
               step=radioClass.getTransmitterFrequencyRes())
            elif key == configKeys.TX_ATTENUATION:
                outstr += """#               "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.TX_ATTENUATION, 
               min=radioClass.getTransmitterAttenuationRange()[0],
               max=radioClass.getTransmitterAttenuationRange()[1],
               step=radioClass.getTransmitterAttenuationRes())
            elif key == configKeys.CONFIG_CW:
                outstr += """#               "{keyword}": {{
""".format(keyword=configKeys.CONFIG_CW)
                outstr += """#                     {min}: {{
""".format(min=radioClass.getTransmitterCWIndexRange()[0])
                for i, key in enumerate(radioClass.txType.toneGenType.validConfigurationKeywords):
                    if key in [configKeys.CW_FREQUENCY, configKeys.CW_SWEEP_START, 
                               configKeys.CW_SWEEP_STOP, configKeys.CW_SWEEP_STEP]:
                        outstr += """#                        "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=key, 
               min=radioClass.getTransmitterCWFrequencyRange()[0],
               max=radioClass.getTransmitterCWFrequencyRange()[1],
               step=radioClass.getTransmitterCWFrequencyRes())
                    elif key == configKeys.CW_AMPLITUDE:
                        outstr += """#                        "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.CW_AMPLITUDE, 
               min=radioClass.getTransmitterCWAmplitudeRange()[0],
               max=radioClass.getTransmitterCWAmplitudeRange()[1],
               step=radioClass.getTransmitterCWAmplitudeRes())
                    elif key == configKeys.CW_PHASE:
                        outstr += """#                        "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.CW_PHASE, 
               min=radioClass.getTransmitterCWPhaseRange()[0],
               max=radioClass.getTransmitterCWPhaseRange()[1],
               step=radioClass.getTransmitterCWPhaseRes())
                    elif key == configKeys.CW_SWEEP_DWELL:
                        outstr += """#                        "{keyword}": [{min}-{max}, step {step}],
""".format(keyword=configKeys.CW_SWEEP_DWELL, 
               min=radioClass.getTransmitterCWDwellRange()[0],
               max=radioClass.getTransmitterCWDwellRange()[1],
               step=radioClass.getTransmitterCWDwellRes())
                outstr += """#                     },
"""
                outstr += """#                  ...{max} (repeat for each tone generator)
""".format(max=radioClass.getTransmitterCWIndexRange()[-1])
                outstr += """#               },
"""
                pass
        outstr += """#            },
"""
        if radioClass.getNumTransmitters() > 1:
            outstr += """#         ...{max} (repeat for each transmitter)
""".format(max=radioClass.getTransmitterIndexRange()[-1])
        outstr += """#      },
"""
    outstr += """# }
"""
    outstr += """# \\endcode
#
"""
    if radioClass.wbddcType is not None and \
       configKeys.DDC_RATE_INDEX in \
       radioClass.wbddcType.validConfigurationKeywords:
        outstr += """# \\section WbddcRates_{name} WBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th></tr>
""".format(name=radioClass._name)
        for key in sorted(radioClass.getWbddcRateSet().keys()):
            outstr += """# <tr><td>{index}</td><td>{rate}</td></tr>
""".format(index=key, rate=radioClass.getWbddcRateSet()[key])
        outstr += """# </table>
#
"""
    if radioClass.nbddcType is not None and \
       configKeys.DDC_RATE_INDEX in \
       radioClass.nbddcType.validConfigurationKeywords:
        outstr += """# \\section NbddcRates_{name} NBDDC Rate Settings
#
# <table>
# <tr><th>Rate Index</th><th>NBDDC Rate (samples per second)</th></tr>
""".format(name=radioClass._name)
        for key in sorted(radioClass.getNbddcRateSet().keys()):
            outstr += """# <tr><td>{index}</td><td>{rate}</td></tr>
""".format(index=key, rate=radioClass.getNbddcRateSet()[key])
        outstr += """# </table>
#
"""
    if (radioClass.wbddcType is not None and \
        configKeys.DDC_VITA_ENABLE in \
        radioClass.wbddcType.validConfigurationKeywords) or \
       (radioClass.nbddcType is not None and \
        configKeys.DDC_VITA_ENABLE in \
        radioClass.nbddcType.validConfigurationKeywords):
        outstr += """# \\section VitaEnable_{name} VITA 49 Enabling Options
#
# <table>
# <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
""".format(name=radioClass._name)
        for key in sorted(radioClass.getVitaEnableOptionSet().keys()):
            outstr += """# <tr><td>{index}</td><td>{meaning}</td></tr>
""".format(index=key, meaning=radioClass.getVitaEnableOptionSet()[key])
        outstr += """# </table>
#
"""
    outstr += """# \\implements CyberRadioDriver.IRadio
"""
    return outstr
    
##
# \interface CyberRadioDriver.IRadio
# \brief Radio handler interface.
#
# This interface provides a standard API for manipulating the various radios
# supported by the driver.  All radio handler objects returned by 
# CyberRadioDriver.getRadioObject() will conform to this interface.  However, not 
# all radios will support all of the capabilities of this interface.
#
class IRadio(object):
    
    ##
    # \brief Constructs a radio handler object.
    #
    # The constructor uses keyword arguments to configure the class.  It 
    # consumes the following keyword arguments:
    # <ul>
    # <li> "verbose": Verbose mode (Boolean)
    # <li> "logFile": An open file or file-like object to be used for log output.  
    #    If not provided, this defaults to standard output. 
    # <li> "setTime": Whether to set the time on the radio (Boolean)
    # <li> "logCtrl": A GUI control that receives log output (GUI-dependent)
    # </ul>
    # Radio handler objects may consume other keyword arguments on a 
    # radio-by-radio basis.  See the documentation for the specific radio
    # for further details.
    #
    # \param args Variable-length list of positional arguments.  Positional
    #     arguments are ignored.
    # \param kwargs Dictionary of keyword arguments for the radio
    #     handler object.  Which keyword arguments are valid depends on the 
    #     specific radio.  Unsupported keyword arguments will be ignored.
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
    ##
    # \brief Indicates whether the radio is connected.
    #
    # \return True if connected, False otherwise.
    def isConnected(self):
        raise NotImplementedError
    
    ##
    # \brief Returns version information for the radio.
    #
    # Version information is returned in a dictionary with
    # the following keys:
    # <ul>
    # <li> "model": radio model
    # <li> "serialNumber": radio serial number
    # <li> "unitRevision": radio unit revision number
    # <li> "softwareVersion": application version number
    # <li> "firmwareVersion": FPGA software version number
    # <li> "firmwareDate": FPGA software date string
    # <li> "referenceVersion": Reference/timing version number
    # <li> "hardwareVersion": list of strings
    # </ul>
    #
    # This method caches version information between queries.
    # 
    # \return A dictionary with the version info.
    def getVersionInfo(self):
        raise NotImplementedError
        
    ##
    # \brief Returns connection information for the radio.
    #
    # Connection information is returned in a dictionary with
    # the following keys:
    # <ul>
    # <li> "mode": Connection mode (one of "tty", "tcp", or "udp")
    # <li> If mode is "tty", then the following keys will be present:
    #      <ul>
    #      <li> "device": Name of the TTY device representing the radio 
    #           on the system
    #      <li> "baudrate": Baud rate (bits per second)
    #      </ul>
    # <li> If mode is "tcp" or "udp", then the following keys will be present:
    #      <ul>
    #      <li> "hostname": Host name for the radio
    #      <li> "port": Port number for the radio
    #      </ul>
    # </ul>
    #
    # \return A dictionary with the connection info.
    def getConnectionInfo(self):
        raise NotImplementedError
        
    ##
    # \brief Connects to a given radio.
    #
    # \param mode One of "tty", "tcp", or "udp".  Supported connection 
    #     modes vary by radio.
    # \param host_or_dev If mode is "tcp" or "udp", this parameter is the 
    #     hostname for the radio.  If mode is "tty", this parameter is the
    #     name of the TTY device representing the radio on the system.
    # \param port_or_baudrate If mode is "tcp" or "udp", this parameter is the 
    #     port for the radio.  If mode is "tty", this parameter is the
    #     baud rate of the TTY device representing the radio on the system.
    #     This parameter may be None, in which case default values are used.
    # \param setTime Whether or not to set the time on the radio.  Not all radios
    #     support setting the time.
    # \param initDdc Whether or not to initialize the DDCs on the radio.
    # \param reset Whether to reset the radio immediately after connecting to it.
    # \return True if connection was successful, False otherwise.
    def connect(self,mode,host_or_dev,port_or_baudrate=None,setTime=True,initDdc=True,
                reset=False):
        raise NotImplementedError
            
    ##
    # \brief Disconnects from the radio.
    def disconnect(self):
        raise NotImplementedError
    
    ##
    # \brief Sends a command to the radio.
    #
    # \param cmdString The command string to send.
    # \param timeout The timeout period, in seconds.  A timeout of None 
    #     uses the default timeout as determined by the transport.
    # \return The command response if command was successfully executed
    #     (whether or not the command itself returned an error).  Returns
    #     None if the command could not be executed.
    def sendCommand(self,cmdString,timeout=None):
        raise NotImplementedError
    
    ##
    # \brief Sets the radio configuration.
    #
    # Keyword argument "configDict" is a nested dictionary containing
    # the settings that need to be set on the radio.
    #
    # \code
    # configDict = {
    #      "configMode": 0,
    #      "referenceMode": 0,
    #      "bypassMode": 0,
    #      "tunerConfiguration": {
    #            1: {
    #               <radio-dependent tuner settings>
    #            },
    #         ...N (number of supported tuners)
    #      },
    #      "ddcConfiguration": {
    #         "wideband": {
    #              1: {
    #                 <radio-dependent WBDDC settings>
    #              },
    #           ...N (number of supported WBDDCs)
    #         },
    #         "narrowband": {
    #              1: {
    #                 <radio-dependent NBDDC settings>
    #              },
    #           ...N (number of supported NBDDCs)
    #         }
    #      },
    #      "ipConfiguration": {
    #         <radio-dependent IP address configuration settings>
    #      },
    #      "txConfiguration": {
    #         <radio-dependent transmitter configuration settings>
    #      },
    # }
    # \endcode
    #
    # The above format assumes that index bases start at 1.  Some radios use 
    # a different base for numbering components, so consult the documentation
    # for the specific radio for further details.
    #
    # At any level where an enumeration is performed, the keyword "all" can be 
    # used as a shortcut to provide common settings for all entries at that level.
    # Individual entries can then override any common settings.  For example:
    # 
    # \code
    # radioHandler.setConfiguration(configDict={
    #      "tunerConfiguration": {
    #            "all": {
    #               "frequency": 900e6,
    #               "attenuation": 10,
    #            },
    #            1: {
    #               "attenuation": 15,
    #            },
    #      },
    # })
    # \endcode
    #
    # This example tunes all tuners on the radio to 900 MHz, and sets 10dB 
    # attenuation on all tuners except for tuner #1, which gets set to 15dB 
    # attenuation instead. 
    #
    # \param configDict The dictionary of radio settings.
    # \return True if all commands completed successfully, False otherwise.
    #    Use getLastCommandErrorInfo() to retrieve any error information.  
    def setConfiguration(self, configDict={}):
        raise NotImplementedError
    
    ##
    # \brief Gets the radio configuration.
    #
    # See setConfiguration() for the format of the returned
    # dictionary.
    #
    # \return The dictionary of radio settings.
    def getConfiguration(self):
        raise NotImplementedError
    
    ##
    # \brief Gets the last set of error information returned by the radio.
    #
    # The error information set is reset on each call to getConfiguration()
    # or setConfiguration().
    #
    # \return A list of error information strings.  This list will 
    # be empty if all commands completed successfully.
    def getLastCommandErrorInfo(self):
        raise NotImplementedError
    
    ##
    # \brief Resets the radio.
    #
    # \note This method supports different types of resets, but not all
    # radios support specifying a reset type.  For these radios, specifying
    # a reset type has no effect.
    # \param resetType The reset type.  Default is "full".  
    # \return True if successful, False if the radio does not support
    # resetting or if the command was unsuccessful.
    def sendReset(self, resetType="full"):
        raise NotImplementedError
    
    ##
    # \brief Gets the pulse-per-second (PPS) rising edge from the radio.
    #
    # \return True if successful, False if the radio does not support
    # PPS edge detection or if the command was unsuccessful.
    def getPps(self):
        raise NotImplementedError
    
    ##
    # \brief Sets the time for the next PPS rising edge on the radio.
    #
    # \param checkTime Whether to verify that the time was set properly.
    # \param useGpsTime Whether to use the GPS time rather than the system time.
    # \return True if successful, False if the radio does not support
    # PPS edge detection and time setting or if the command was unsuccessful.
    def setTimeNextPps(self,checkTime=False,useGpsTime=False):
        raise NotImplementedError
            
    ##
    # \brief Gets the current radio time.
    #
    # \return The UTC time in seconds from the epoch, or None if the radio 
    # does not support time querying or if the command was unsuccessful.
    def getTimeNow(self):
        raise NotImplementedError
    
    ##
    # \brief Gets the time for the next PPS rising edge on the radio.
    #
    # \return The UTC time in seconds from the epoch, or None if the radio 
    # does not support PPS edge detection and time querying or if the command 
    # was unsuccessful.
    def getTimeNextPps(self):
        raise NotImplementedError
    
    ##
    # \brief Gets the status from the radio.
    #
    # \return A dictionary containing the radio status.  This dictionary
    # contains the following keys:
    # <ul>
    # <li> "int": The status bitmask provided by the radio, as an integer value.
    # <li> "statValues": A list of status bits that are set in the bitmask.
    # <li> "statText": A list of text descriptions for the bits that are set.
    # </ul>
    # This command returns None if the radio does not support status queries.
    def getStatus(self):
        raise NotImplementedError
    
    ##
    # \brief Gets the RF tuner status from the radio.
    #
    # \return A dictionary containing the radio status.  This dictionary
    # contains the following keys:
    # <ul>
    # <li> "int": The status bitmask provided by the radio, as an integer value.
    # <li> "statValues": A list of status bits that are set in the bitmask.
    # <li> "statText": A list of text descriptions for the bits that are set.
    # </ul>
    # This command returns None if the radio does not support RF tuner status 
    # queries.
    def getTstatus(self):
        raise NotImplementedError
    
    ##
    # \brief Sets the reference mode on the radio.
    #
    # \param mode An integer indicating the reference mode to set.  Valid
    # reference mode numbers vary by radio.
    # \return True if successful, False if unsuccessful or if reference mode
    # setting is not supported on the radio or if the provided mode is not
    # supported. 
    def setReferenceMode(self,mode):
        raise NotImplementedError
    
    ##
    # \brief Sets the reference bypass mode on the radio.
    #
    # \param mode An integer indicating the reference bypass mode to set.  Valid
    # bypass mode numbers vary by radio.
    # \return True if successful, False if unsuccessful or if reference bypass mode
    # setting is not supported on the radio or if the provided mode is not
    # supported. 
    def setBypassMode(self,mode):
        raise NotImplementedError
            
    ##
    # \brief Sets the time adjustment for tuners on the radio.
    #
    # \param tunerIndex Either None (adjust all tuners), a tuner index number 
    #    (adjust that tuner alone), or a list of tuner index numbers.
    # \param timeAdjustValue Time adjustment value.
    # \return True if successful, False if unsuccessful or if adjusting the time
    #    is not supported. 
    def setTimeAdjustment(self,tunerIndex=None,timeAdjustValue=0):
        raise NotImplementedError

    ##
    # \brief Sets the calibration frequency on the radio.
    #
    # \param calibFrequency The frequency to set, in MHz.  If 0, disable the 
    #    calibration signal.
    # \return True if successful, False if unsuccessful or if adjusting calibration
    #    frequency is not supported. 
    def setCalibrationFrequency(self, calibFrequency=0):
        raise NotImplementedError

    ##
    # \brief Gets the current GPS position.
    #
    # \return A 2-tuple (latitude, longitude) in decimal degrees.  West 
    #    longitudes and south latitudes are negative.  If the radio does
    #    not support GPS, or if the GPS receiver does not have a valid
    #    position lock, then this method returns 0.0 for both latitude
    #    and longitude.
    def getGpsPosition(self):
        raise NotImplementedError
    
    ##
    # \brief Gets the current radio temperature.
    #
    # \return The temperature, in degrees Celsius.  If the radio does
    #    not support temperature querying, this method returns 0.
    def getTemperature(self):
        raise NotImplementedError
    
    ##
    # \brief Gets the current GPIO output bits.
    #    
    # \return The GPIO output bits, as an integer bitmask.  If the GPIO 
    #    module is running in sequence mode, then this value is undefined.
    def getGpioOutput(self):
        raise NotImplementedError
    
    ##
    # \brief Gets the GPIO output settings for a given sequence index.
    # \param index The GPIO sequence index.
    # \return A 3-tuple (bitmask, duration, loop).  
    def getGpioOutputByIndex(self, index):
        raise NotImplementedError
    
    ##
    # \brief Sets the current GPIO output bits.
    # \note Executing this method puts the GPIO module into static mode.
    # \param value The GPIO output value, as an integer bitmask.
    # \return True if successful, False if unsuccessful or if setting
    #    GPIO output is not supported. 
    def setGpioOutput(self, value):
        raise NotImplementedError
    
    ##
    # \brief Sets the GPIO output settings for a given sequence index.
    # \note Executing this method puts the GPIO module into sequence mode
    #    if the "go" parameter is 1.
    # \param index The GPIO sequence index.
    # \param value The GPIO output value, as an integer bitmask.
    # \param duration The duration for that value, as a number of ADC
    #    clock cycles.
    # \param loop Whether the sequence loops back to the beginning after
    #    this step (1) or not (0).
    # \param loop Whether to execute the sequence (1) or not (0).
    # \return True if successful, False if unsuccessful or if setting
    #    GPIO output is not supported. 
    def setGpioOutputByIndex(self, index, value, duration, loop, go):
        raise NotImplementedError
    
    ##
    # \brief Gets the name of the radio.
    #
    # \return The name, as a string. 
    @classmethod
    def getName(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the number of tuners on the radio.
    #
    # \return The number of tuners. 
    @classmethod
    def getNumTuner(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the index range for the tuners on the radio.
    #
    # \return The list of tuner indexes. 
    @classmethod
    def getTunerIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency range for the tuners on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTunerFrequencyRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency resolution for tuners on the radio.
    #
    # \return The frequency resolution. 
    @classmethod
    def getTunerFrequencyRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency unit for tuners on the radio.
    #
    # The frequency unit is a floating-point value that indicates
    # how the frequency is specified in commands given to the radio.
    # <ul>
    # <li> 1.0: Frequency given in Hz
    # <li> 1.0e6: Frequency given in MHz
    # </ul> 
    #
    # \return The frequency unit.
    @classmethod
    def getTunerFrequencyUnit(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the attenuation range for the tuners on the radio.
    #
    # \return The attenuation range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTunerAttenuationRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the attenuation resolution for tuners on the radio.
    #
    # \return The attenuation resolution. 
    @classmethod
    def getTunerAttenuationRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the number of wideband DDCs on the radio.
    #
    # \return The number of wideband DDCs. 
    @classmethod
    def getNumWbddc(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the index range for the wideband DDCs on the radio.
    #
    # \return The list of wideband DDC indexes. 
    @classmethod
    def getWbddcIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether the wideband DDCs on the radio are tunable.
    #
    # \return True if tunable, False otherwise.
    @classmethod
    def isWbddcTunable(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether the wideband DDCs on the radio have selectable
    # sources.
    #
    # \return True if selectable, False otherwise.
    @classmethod
    def isWbddcSelectableSource(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency offset range for the wideband DDCs on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getWbddcFrequencyRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency offset resolution for wideband DDCs on the radio.
    #
    # \return The frequency offset resolution. 
    @classmethod
    def getWbddcFrequencyRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate set for the wideband DDCs on the radio.
    #
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    @classmethod
    def getWbddcRateSet(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate list for the wideband DDCs on the radio.
    #
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    @classmethod
    def getWbddcRateList(cls):
        raise NotImplementedError

    ##
    # \brief Gets the number of narrowband DDCs on the radio.
    #
    # \return The number of narrowband DDCs. 
    @classmethod
    def getNumNbddc(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the index range for the narrowband DDCs on the radio.
    #
    # \return The list of narrowband DDC indexes. 
    @classmethod
    def getNbddcIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether the narrowband DDCs on the radio are tunable.
    #
    # \return True if tunable, False otherwise.
    @classmethod
    def isNbddcTunable(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether the narrowband DDCs on the radio have selectable
    # sources.
    #
    # \return True if selectable, False otherwise.
    @classmethod
    def isNbddcSelectableSource(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency offset range for the narrowband DDCs on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getNbddcFrequencyRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency offset resolution for narrowband DDCs on the radio.
    #
    # \return The frequency offset resolution. 
    @classmethod
    def getNbddcFrequencyRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate set for the narrowband DDCs on the radio.
    #
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    @classmethod
    def getNbddcRateSet(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate list for the narrowband DDCs on the radio.
    #
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    @classmethod
    def getNbddcRateList(cls):
        raise NotImplementedError

    ##
    # \brief Gets the number of DDCs on the radio.
    #
    # \deprecated Use getNumWbddc() or getNumNbddc() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).  
    # \return The number of DDCs of the provided type. 
    @classmethod
    def getNumDdc(cls, wideband):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate set for the DDCs on the radio.
    #
    # \deprecated Use getWbddcRateSet() or getNbddcRateSet() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).  
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    @classmethod
    def getDdcRateSet(cls, wideband):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate list for the DDCs on the radio.
    #
    # \deprecated Use getWbddcRateList() or getNbddcRateList() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).  
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    @classmethod
    def getDdcRateList(cls, wideband):
        raise NotImplementedError

    ##
    # \brief Gets the VITA 49 header size for the radio.
    #
    # \return The header size, in bytes.
    @classmethod
    def getVitaHeaderSize(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the VITA 49 payload size for the radio.
    #
    # If VITA 49 output is disabled, then the returned value 
    # indicates the number of raw I/Q data bytes in each packet. 
    #
    # \return The payload size, in bytes.
    @classmethod
    def getVitaPayloadSize(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the VITA 49 tail size for the radio.
    #
    # \return The tail size, in bytes.
    @classmethod
    def getVitaTailSize(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether data coming from the radio is byte-swapped with 
    # respect to the endianness of the host operating system.
    #
    # \return True or False, as appropriate for the radio.
    @classmethod
    def isByteswapped(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether data coming from the radio has I and Q data swapped.
    #
    # \return True or False, as appropriate for the radio.
    @classmethod
    def isIqSwapped(cls):
        return cls.ifSpec.iqSwapped

    ##
    # \brief Gets the byte order for data coming from the radio.
    #
    # \return The byte order, as a string.
    @classmethod
    def getByteOrder(cls):
        return cls.ifSpec.byteOrder
    
    ##
    # \brief Gets the number of Gigabit Ethernet interfaces on the radio.
    #
    # \return The number of GigE interfaces. 
    @classmethod
    def getNumGigE(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the index range for the Gigabit Ethernet interfaces on the radio.
    #
    # \return The list of GigE interface indexes. 
    @classmethod
    def getGigEIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the number of destination IP address table entries available for 
    # each Gigabit Ethernet interface on the radio.
    #
    # \return The number of destination IP address table entries. 
    @classmethod
    def getNumGigEDipEntries(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the index range for the destination IP address table entries 
    # available for the Gigabit Ethernet interfaces on the radio.
    #
    # \return The list of destination IP address table entry indexes. 
    @classmethod
    def getGigEDipEntryIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the list of connection modes that the radio supports.
    #
    # \return The list of connection modes. 
    @classmethod
    def getConnectionModeList(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether the radio supports a given connection mode.
    #
    # \param mode The connection mode of interest.
    # \return True if the connection mode is supported, False otherwise.
    @classmethod
    def isConnectionModeSupported(cls, mode):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed VITA enable options set for the radio.
    #
    # \return The option set.  This is a dictionary whose keys are 
    #     VITA enable option values and whose values are the corresponding 
    #     meanings for those values. 
    @classmethod
    def getVitaEnableOptionSet(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the number of transmitters on the radio.
    #
    # \return The number of transmitters. 
    @classmethod
    def getNumTransmitters(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the index range for the transmitters on the radio.
    #
    # \return The list of transmitter indexes. 
    @classmethod
    def getTransmitterIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency range for the transmitters on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterFrequencyRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency resolution for transmitters on the radio.
    #
    # \return The frequency resolution. 
    @classmethod
    def getTransmitterFrequencyRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the frequency unit for transmitters on the radio.
    #
    # The frequency unit is a floating-point value that indicates
    # how the frequency is specified in commands given to the radio.
    # <ul>
    # <li> 1.0: Frequency given in Hz
    # <li> 1.0e6: Frequency given in MHz
    # </ul> 
    #
    # \return The frequency unit.
    @classmethod
    def getTransmitterFrequencyUnit(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the attenuation range for the transmitters on the radio.
    #
    # \return The attenuation range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterAttenuationRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the attenuation resolution for transmitters on the radio.
    #
    # \return The attenuation resolution. 
    @classmethod
    def getTransmitterAttenuationRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether transmitters on the radio support continuous-wave
    # (CW) tone generation.
    #
    # \return True if tone generation is supported, False otherwise. 
    @classmethod
    def transmitterSupportsCW(cls):
        raise NotImplementedError

    ##
    # \brief Gets the number of CW tone generators for each transmitter.
    #
    # \return The number of tone generators. 
    @classmethod
    def getTransmitterCWNum(cls):
        raise NotImplementedError

    ##
    # \brief Gets the CW tone generator index range for transmitters on the radio.
    #
    # \return The list of tone generator indexes. 
    @classmethod
    def getTransmitterCWIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator frequency range for transmitters on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterCWFrequencyRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator frequency resolution for transmitters on the radio.
    #
    # \return The frequency resolution. 
    @classmethod
    def getTransmitterCWFrequencyRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator amplitude range for transmitters on the radio.
    #
    # \return The amplitude range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterCWAmplitudeRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator amplitude resolution for transmitters on the radio.
    #
    # \return The amplitude resolution. 
    @classmethod
    def getTransmitterCWAmplitudeRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator phase range for transmitters on the radio.
    #
    # \return The phase range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterCWPhaseRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator phase resolution for transmitters on the radio.
    #
    # \return The phase resolution. 
    @classmethod
    def getTransmitterCWPhaseRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets whether transmitters on the radio support sweep functions
    # during continuous-wave (CW) tone generation.
    #
    # \return True if sweep is supported, False otherwise. 
    @classmethod
    def transmitterSupportsCWSweep(cls):
        raise NotImplementedError

    ##
    # \brief Gets the CW tone generator sweep start frequency range for 
    # transmitters on the radio.
    #
    # \return The start range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterCWSweepStartRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator sweep start frequency resolution for 
    # transmitters on the radio.
    #
    # \return The start resolution. 
    @classmethod
    def getTransmitterCWSweepStartRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator sweep stop frequency range for 
    # transmitters on the radio.
    #
    # \return The stop range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterCWSweepStopRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator sweep stop frequency resolution for 
    # transmitters on the radio.
    #
    # \return The stop resolution. 
    @classmethod
    def getTransmitterCWSweepStopRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator sweep step frequency range for 
    # transmitters on the radio.
    #
    # \return The step range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterCWSweepStepRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator sweep step frequency resolution for 
    # transmitters on the radio.
    #
    # \return The step resolution. 
    @classmethod
    def getTransmitterCWSweepStepRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator sweep dwell time range for 
    # transmitters on the radio.
    #
    # \return The dwell time range.  This is a 2-tuple: (minimum, maximum). 
    @classmethod
    def getTransmitterCWSweepDwellRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the CW tone generator sweep dwell time resolution for 
    # transmitters on the radio.
    #
    # \return The dwell time resolution. 
    @classmethod
    def getTransmitterCWSweepDwellRes(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the number of wideband DUCs on the radio.
    #
    # \return The number of wideband DUCs. 
    @classmethod
    def getNumWbduc(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the index range for the wideband DUCs on the radio.
    #
    # \return The list of wideband DUC indexes. 
    @classmethod
    def getWbducIndexRange(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate set for the wideband DUCs on the radio.
    #
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    @classmethod
    def getWbducRateSet(cls):
        raise NotImplementedError
    
    ##
    # \brief Gets the allowed rate list for the wideband DUCs on the radio.
    #
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    @classmethod
    def getWbducRateList(cls):
        raise NotImplementedError

    ##
    # \brief Gets whether or not the wideband DUCs on the radio support loading
    # sample snapshots.
    #
    # \return True if supported, False otherwise.
    @classmethod
    def wbducSupportsSnapshotLoad(cls):
        raise NotImplementedError

    ##
    # \brief Gets whether or not the wideband DUCs on the radio support transmitting
    # sample snapshots.
    #
    # \return True if supported, False otherwise.
    @classmethod
    def wbducSupportsSnapshotTransmit(cls):
        raise NotImplementedError

    