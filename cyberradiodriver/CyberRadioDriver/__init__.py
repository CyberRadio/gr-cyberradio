#!/usr/bin/env python
###############################################################
# \package CyberRadioDriver
#
# \brief The CyberRadio Solutions NDR Radio Driver module
# (CyberRadioDriver) provides users with a common application
# programming interface (API) for all CyberRadio Solutions
# NDR-class radios.
#
# End-users of the driver should obtain a radio handler object
# for their radio(s) by calling CyberRadioDriver.getRadioObject()
# with the name string for the desired radio.  They can then use
# the methods provided by the CyberRadioDriver.IRadio interface
# to manipulate their radio handler object.
#
# The driver package documentation also includes other modules
# and objects. These implement the high-level functionality
# exposed by CyberRadioDriver.getRadioObject() and the
# CyberRadioDriver.IRadio interface. However, these items will
# be of little interest to end-users.  They are included mainly
# for the benefit of those who maintain the driver.
#
# \author NH
# \author DA
# \author MN
# \copyright Copyright (c) 2014-2021 CyberRadio Solutions, Inc.
#    All rights reserved.
#
###############################################################

###############################################################
# \mainpage CyberRadio Solutions NDR Radio Driver for Python
#
# \section Description
#
# The CyberRadio Solutions NDR Radio Driver module
# (CyberRadioDriver) provides users with a common application
# programming interface (API) for all CyberRadio Solutions
# NDR-class radios.
#
# End-users of the driver should obtain a radio handler object
# for their radio(s) by calling CyberRadioDriver.getRadioObject()
# with the name string for the desired radio.  They can then use
# the methods provided by the CyberRadioDriver.IRadio interface
# to manipulate their radio handler object.
#
# The driver package documentation also includes other modules
# and objects. These implement the high-level functionality
# exposed by CyberRadioDriver.getRadioObject() and the
# CyberRadioDriver.IRadio interface. However, these items will
# be of little interest to end-users.  They are included mainly
# for the benefit of those who maintain the driver.
#
# \section SupportedRadios Supported Radios
#
# <table>
#    <tr><th>Radio</th><th>Name String</th></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr301::ndr301 NDR301 \endlink</td><td>"ndr301"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr301ptt::ndr301_ptt NDR301PTT \endlink</td><td>"ndr301-ptt"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr303::ndr303 NDR303 \endlink</td><td>"ndr303"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr304::ndr304 NDR304 \endlink</td><td>"ndr304"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr308::ndr308_1 NDR308-1 \endlink</td><td>"ndr308_1"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr308::ndr308_ts NDR308-TS \endlink</td><td>"ndr308ts"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr308::ndr308 NDR308 \endlink</td><td>"ndr308"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr308::ndr308_4 NDR308 4-tuner \endlink</td><td>"ndr308_4"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr328::ndr328 NDR328 \endlink</td><td>"ndr328"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr354::ndr354 NDR354 \endlink</td><td>"ndr354"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr357::ndr357 NDR357 \endlink</td><td>"ndr357"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr358::ndr358 NDR358 \endlink</td><td>"ndr358"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr358::ndr358_recorder NDR358 Recorder Variant\endlink</td><td>"ndr358-recorder"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr364::ndr364 NDR364 \endlink</td><td>"ndr364"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr470::ndr470 NDR470 \endlink</td><td>"ndr470"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr472::ndr472_1 NDR472-1 \endlink</td><td>"ndr472_1"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr472::ndr472 NDR472 \endlink</td><td>"ndr472"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr551::ndr551 NDR551 \endlink</td><td>"ndr551"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr559::ndr559 NDR559 \endlink</td><td>"ndr559"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr562::ndr562 NDR562 \endlink</td><td>"ndr562"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr601::ndr601 NDR601 \endlink</td><td>"ndr601"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::ndr651::ndr651 NDR651 \endlink</td><td>"ndr651"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr804::ndr804 NDR804 \endlink</td><td>"ndr804"</td></tr>
#    <tr><td>\link CyberRadioDriver::radios::internal::ndr810::ndr810 NDR810 \endlink</td><td>"ndr810"</td></tr>
# </table>
#
# The name string from this table is used in
# CyberRadioDriver.getRadioObject() to get a radio handler object
# for a particular radio.
#
###############################################################

# Imports from other modules in this package
from . import configKeys
from . import radio
# Imports from external modules
# Python standard library imports
import importlib
import inspect
import pkgutil
import socket
import struct
import sys


##
# \brief Driver module name (string).
name = "CyberRadioDriver"
##
# \brief Driver module description (string).
description = "CyberRadio Solutions NDR Driver"
##
# \brief Driver version number (string).
version = "21.03.22"

# # This section of code inspects the "radio" module for radio handler
# # objects (objects derived from _radio, thus implementing the IRadio interface)
# # and imports those objects into this module's namespace (that is, it mirrors
# # a "from radio import <radio handler class>" statement).
# for objname, obj in inspect.getmembers(radio):
#     if inspect.isclass(obj) and issubclass(obj, radio._radio) \
#       and "_radio" not in objname:
#         # Import that object into this module's namespace.
#         setattr(sys.modules[__name__], objname, obj)


# BEGIN NON-WINDOWS METHODS
if sys.platform != "win32":

    import fcntl

    ##
    # \brief Returns the MAC address and IP address (and, optionally, the
    #    MTU) for a given Ethernet interface.
    #
    # \note The MTU query is optional in order to provide backward compatibility
    #    with CyberRadioDriver programs that do not use this value.
    # \note This method is not defined under Windows.
    #
    # \param ifname The name of the Ethernet system interface ("eth0", for
    #    example).
    # \param getMTU If True, return the MTU as well.
    # \returns If getMTU is False, a 2-tuple: (MAC Address string, IP Address string).
    #    If getMTU is True, a 3-tuple: (MAC address string, IP address string, MTU).
    #    If the given interface does not exist, then both returned strings will be
    #    empty strings.
    def getInterfaceAddresses(ifname, getMTU=False):
        mac = ""
        ip = ""
        mtu = 0
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ifr = struct.pack('256s', ifname[:15])
            info = fcntl.ioctl(s.fileno(),
                               0x8927, # SIOCGIFHWADDR
                               ifr)
            mac = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
            ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                              0x8915,  # SIOCGIFADDR
                                              ifr)[20:24])
            if getMTU:
                mtu = struct.unpack("<H",
                          fcntl.ioctl(s.fileno(),
                                      0x8921, # SIOCGIFMTU
                                      ifr)[16:18])[0]
        except:
            pass
        if getMTU:
            return mac, ip, mtu
        else:
            return mac,ip

# END NON-WINDOWS METHODS

##
# \internal
# \brief Recursively import submodules that are part of some arbitrary package.
#
# This code was found here:
# https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
#
# \param package Either the package name (string) or the actual imported module.
# \param recursive Whether or not to import recursively (boolean).
# \returns A dictionary where the keys are module name strings and the values
#     are module type objects.
def import_submodules(package, recursive=True):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results

##
# \internal
# \brief Creates the radio class map from radio handler modules.
#
# To support a radio, create a radio handler object (an object derived
# from radio._radio, thus implementing the IRadio interface) in a
# separate module under the CyberRadioDriver.radios package tree.
# This method imports these radio handler modules recursively, and then
# forms the radio class map from the results.
#
# \note Doxygen is not as intelligent as Python when it comes to
# generating documentation dynamically. When creating a new radio handler
# module, you will need to add the new radio to the list of supported radios
# in the "mainpage" documentation section at the top of this file.
#
# \returns The radio class map.  This is a dictionary whose keys are radio
#     name strings and whose values are radio handler class names.
def create_radio_class_map():
    ret = {}
    radio_module_info = import_submodules("CyberRadioDriver.radios")
    for modname, modinfo in radio_module_info.items():
        for name, obj in inspect.getmembers(modinfo):
            if inspect.isclass(obj) and issubclass(obj, radio._radio) and "_radio" not in name:
                # Add the object to the radio class map.
                ret[name.replace("_","-")] = obj
    return ret

##
# \internal
# \brief Radio class map.  This maps radio name strings to radio handler class names.
_radio_class_map = create_radio_class_map()

##
# \brief Gets the list of supported radios.
# \return The list of supported radios.
def getSupportedRadios():
    return sorted(_radio_class_map.keys())

##
# \brief Factory method for obtaining a radio handler class name from the name
# of the radio.
#
# The name string used to identify the radio can be any string returned
# by getSupportedRadios(), but the check is not case-sensitive.
# The returned radio handler class will support the CyberRadioDriver.IRadio
# interface.
#
# \param nameString The name string for the radio of interest.
# \returns The radio handler class name for the desired radio.
# \throws RuntimeError if the desired radio is not supported.
def getRadioClass(nameString):
    nameString = nameString.strip().lower().replace("_","-")
    try:
        return _radio_class_map[nameString]
    except:
        raise RuntimeError("Unsupported radio: %s" % nameString)

##
# \brief Factory method for obtaining a radio handler object from the name
# of the radio.
#
# The name string used to identify the radio can be:
# * Any string returned by getSupportedRadios() (but the check is not case-
#   sensitive).
# * "auto", in which case the method will attempt to auto-detect the type of
#   radio connected to the system.  Since radios can operate over both
#   Ethernet and TTY (serial) links, the user needs to supply keyword
#   arguments to indicate which devices to scan ("host" to scan over
#   Ethernet and/or "dev" to scan over TTY -- see below).
# * "server" or "crdd", in which case the method attempts to connect to the
#   radio via the CyberRadio Driver Daemon (crdd).  Supply the "host" and/or
#   "port" arguments if CRDD is not running at the default location (local
#   host, port 65432).  Also, supply the "clientId" argument if you want
#   crdd to log transactions for this client specially.
#
# This method uses keyword arguments to configure the returned radio handler
# object.  It consumes the following keyword arguments:
# <ul>
# <li> "verbose": Verbose mode (Boolean)
# <li> "logFile": An open file or file-like object to be used for log output.
#    If not provided, this defaults to standard output.
# <li> "setTime": Whether to set the time on the radio (Boolean)
# <li> "logCtrl": A GUI control that receives log output (GUI-dependent)
# <li> "host": For TCP-connected radios, this is the host name for the radio.
#    If provided, this method will auto-detect a radio on this device if
#    requested, and automatically connect to it.
# <li> "port": For TCP-connected radios, this is the command port for the radio.
#    If not provided, this defaults to the standard port (8617).
# <li> "dev": For TTY-connected radios, this is the system device name for the
#    radio's serial (USB) link.  If provided, this method will auto-detect a radio
#    on this device if requested, and automatically connect to it.
# <li> "baudrate": For TTY-connected radios, this is the baud rate for the serial
#    connection.  If not provided, this defaults to the standard (921600).
# <li> "clientId": For connections through crdd, this provides an identifier
#    that crdd can use to identify this client for logging purposes.
# </ul>
# If the "host" and "dev" keyword arguments are both provided, then the auto-
# detection algorithm will try a TCP connection first before falling back to a
# TTY connection.
#
# Radio handler objects may consume other keyword arguments on a
# radio-by-radio basis.  See the documentation for the specific radio
# for further details.
#
# The returned radio handler object will support the CyberRadioDriver.IRadio
# interface.
#
# \param nameString The name string for the radio of interest, or "auto".
# \param args Variable-length list of positional arguments.  Positional
#     arguments are ignored.
# \param kwargs Dictionary of keyword arguments to pass to the radio
#     handler object.  Which keyword arguments are valid depends on the
#     specific radio.  Unsupported keyword arguments will be ignored.
# \returns A radio handler object for the desired radio.
# \throws RuntimeError if the desired radio is not supported, or if a
#     radio could not be found.
def getRadioObject(nameString, *args, **kwargs):
    if nameString == "auto":
        radioType = ""
        connModes = []
        ports = {}
        if kwargs.get("host", None) is not None:
            connModes.extend(["https", "tcp", "udp"])
            ports["https"] = [443]
            ports["tcp"] = [8617, 10301]
            ports["udp"] = [19091]
        if kwargs.get("dev", None) is not None:
            connModes.append("tty")
        for connMode in connModes:
            # Grab a temporary handler object of the identifier class
            tmpHandler = None
            if connMode == "https":
                #print "[DBG][getRadioObject] Trying", connMode
                tmpHandler = radio._radio_identifier_json(verbose=False, logFile=None,
                                                     timeout=kwargs.get("timeout", None))
                for port in ports["https"]:
                    #print "[DBG][getRadioObject] -- port", port
                    tmpHandler.connect("https", kwargs.get("host"), kwargs.get("port", port))
                    if tmpHandler.isConnected():
                        break
            elif connMode == "tcp":
                #print "[DBG][getRadioObject] Trying", connMode
                tmpHandler = radio._radio_identifier(verbose=False, logFile=None,
                                                     timeout=kwargs.get("timeout", None))
                for port in ports["tcp"]:
                    #print "[DBG][getRadioObject] -- port", port
                    tmpHandler.connect("tcp", kwargs.get("host"), kwargs.get("port", port))
                    if tmpHandler.isConnected():
                        break
            elif connMode == "udp":
                #print "[DBG][getRadioObject] Trying", connMode
                tmpHandler = radio._radio_identifier_json(verbose=False, logFile=None,
                                                     timeout=kwargs.get("timeout", None))
                for port in ports["udp"]:
                    #print "[DBG][getRadioObject] -- port", port
                    tmpHandler.connect("udp", kwargs.get("host"), kwargs.get("port", port))
                    if tmpHandler.isConnected():
                        break
            elif connMode == "tty":
                #print "[DBG][getRadioObject] Trying", connMode
                tmpHandler = radio._radio_identifier(verbose=False, logFile=None,
                                                     timeout=kwargs.get("timeout", None))
                tmpHandler.connect("tty", kwargs.get("dev"), kwargs.get("baudrate", None))
            if tmpHandler.isConnected():
                radioType = tmpHandler.getVersionInfo()["model"]
                if "\\" in radioType:
                    radioType = radioType[0:radioType.find("\\")]
                radioType = str(radioType).lower()
                radioType = radioType.replace("ts", "_ts")
                radioType = radioType.replace("-", "_")
                radioType = radioType.replace("__", "_")
                # NDR804-PTT weirdness: the model name has a space in it -- DA
                if radioType == "ndr804 ptt":
                    radioType = "ndr804-ptt"
                # NDR301-PTT weirdness: sometimes the model name does not have the dash
                # in it -- DA
                if radioType == "ndr301ptt":
                    radioType = "ndr301-ptt"
                # NDR358 weirdness: the NDR358 Recorder mode variant can self-identify
                # as "NDR358-5", per NH -- DA
                if radioType == "ndr358_5":
                    radioType = "ndr358_recorder"
                # For NDR358 models, read the radio function to identify we should use
                # a handler for a specific variant.  Note that we don't have handlers
                # for all potential variants yet. -- DA
                if radioType == "ndr358":
                    radioFn = tmpHandler.getConfigurationByKeys(configKeys.RADIO_FUNCTION)
                    # radioFn == 0 ==> Receiver mode
                    # radioFn == 1 ==> Fast Scan mode
                    if radioFn == 2:
                        radioType = "ndr358_coherent"
                    # radioFn == 3 ==> Resampler mode
                    elif radioFn == 4:
                        radioType = "ndr358_recorder"
                    # radioFn == 5 ==> ALT_RX1 mode
                tmpHandler.disconnect()
            if radioType != "":
                break
        if radioType != "":
            kwargs["clientId"] = None
            obj = getRadioClass(radioType)(*args, **kwargs)
            if connMode in ["tcp", "udp", "https"]:
                obj.connect(connMode, kwargs.get("host"), kwargs.get("port", None))
            elif connMode == "tty":
                obj.connect("tty", kwargs.get("dev"), kwargs.get("baudrate", None))
            return obj
        else:
            raise RuntimeError("Radio not found")
    elif nameString == "server" or nameString == "crdd":
        connMode = "tcp"
        host = kwargs.get("host", "localhost")
        port = kwargs.get("port", 65432)
        radioType = ""
        # Use a temporary radio identifier class to determine what kind of radio the
        # server is managing
        tmpHandler = None
        # -- Try the non-JSON radio identifier first, since the handshake is just a
        #    line feed.  If that doesn't work, then try the JSON identifier.
        for radioIdentifierCls in [radio._radio_identifier, radio._radio_identifier_json]:
            tmpHandler = radioIdentifierCls(verbose=False,
                                            logFile=None,
                                            timeout=kwargs.get("timeout", None))
            tmpHandler.connect(connMode, host, port)
            #if tmpHandler.isConnected() or any(["Radio is not connected" in q for q in tmpHandler.connectError]):
            if tmpHandler.isConnected():
                break
        # If the radio identifier connected, then identify the radio managed by the server
        # and establish a radio-specific handler.
        if tmpHandler is not None and tmpHandler.isConnected():
            radioType = tmpHandler.getVersionInfo()["model"]
            if "\\" in radioType:
                radioType = radioType[0:radioType.find("\\")]
            radioType = str(radioType).lower()
            radioType = radioType.replace("ts", "_ts")
            radioType = radioType.replace("-", "_")
            radioType = radioType.replace("__", "_")
            # NDR804-PTT weirdness: the model name has a space in it -- DA
            if radioType == "ndr804 ptt":
                radioType = "ndr804-ptt"
            # NDR301-PTT weirdness: sometimes the model name does not have the dash
            # in it -- DA
            if radioType == "ndr301ptt":
                radioType = "ndr301-ptt"
            # NDR358 weirdness: the NDR358 Recorder mode variant can self-identify
            # as "NDR358-5", per NH -- DA
            if radioType == "ndr358_5":
                radioType = "ndr358_recorder"
            # For NDR358 models, read the radio function to identify we should use
            # a handler for a specific variant.  Note that we don't have handlers
            # for all potential variants yet. -- DA
            if radioType == "ndr358":
                radioFn = tmpHandler.getConfigurationByKeys(configKeys.RADIO_FUNCTION)
                # radioFn == 0 ==> Receiver mode
                # radioFn == 1 ==> Fast Scan mode
                if radioFn == 2:
                    radioType = "ndr358_coherent"
                # radioFn == 3 ==> Resampler mode
                elif radioFn == 4:
                    radioType = "ndr358_recorder"
                # radioFn == 5 ==> ALT_RX1 mode
            tmpHandler.disconnect()
        if radioType != "":
            obj = getRadioClass(radioType)(*args, **kwargs)
            # Make sure that the connection mode used for the server is in
            # the allowed connection mode list for the radio handler
            if not obj.isConnectionModeSupported(connMode):
                obj.connectionModes.append(connMode)
            # Set crdd flag
            obj.isCrddConnection = True
            # Connect to the new handler
            obj.connect(connMode, host, port)
            return obj
        else:
            if any(["Radio is not connected" in q for q in tmpHandler.connectError]):
                raise RuntimeError("Radio is not connected")
            else:
                raise RuntimeError("Radio not found")
    else:
        kwargs["clientId"] = None
        obj = getRadioClass(nameString)(*args, **kwargs)
        if kwargs.get("host", None) and any(obj.isConnectionModeSupported(i) for i in ("https","tcp","udp")):
            hostname = kwargs["host"]
            for connectionMethod in ("https","tcp","udp"):
                if not None and obj.isConnectionModeSupported(connectionMethod):
                    obj.connect(connectionMethod, hostname, kwargs.get("port",None))
                    break
        elif kwargs.get("dev", kwargs.get("host",None)) is not None and obj.isConnectionModeSupported("tty"):
            obj.connect("tty", kwargs.get("dev", kwargs.get("host",None)), kwargs.get("baudrate", None))
        return obj

##
# \brief Factory method for obtaining a documentation string for a
# radio handler object from the name of the radio.
#
# The name string used to identify the radio can be any string returned
# by getSupportedRadios(), but the check is not case-sensitive.  The
# documentation block returned is compatible with Doxygen.
#
# \note The generated documentation does not contain all possible
#    configuration options as of yet.
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
    # <li> "timeout": Timeout, in seconds (float)
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
    # \brief Destroys a radio handler object.
    #
    # The default action is to disconnect from the radio when the handler
    # object is destroyed.
    def __del__(self):
        pass

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
    # <li> "mode": Connection mode (one of "tty", "tcp", "udp", or "https")
    # <li> If mode is "tty", then the following keys will be present:
    #      <ul>
    #      <li> "device": Name of the TTY device representing the radio
    #           on the system
    #      <li> "baudrate": Baud rate (bits per second)
    #      </ul>
    # <li> If mode is "tcp", "udp", or "https", then the following keys
    #    will be present:
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
    # \param fcState None (take no action) or boolean used to set 10GbE flow control.
    # \return True if connection was successful, False otherwise.
    def connect(self,mode,host_or_dev,port_or_baudrate=None,setTime=True,initDdc=True,
                reset=False, fcState=None,):
        raise NotImplementedError

    ##
    # \brief Disconnects from the radio.
    def disconnect(self):
        raise NotImplementedError

    ##
    # \brief Sends a command to the radio.
    # \note This method can be used to execute arbitrary commands.  The
    #    user is responsible for interpreting the returned command
    #    response.
    # \param cmdString The command string to send.  This command string
    #    should include any line delimiters as required by the radio.
    # \param timeout The timeout period, in seconds.  A timeout of None
    #     uses the default timeout as determined by the transport.
    # \return The command response if command was successfully executed
    #     (whether or not the command itself returned an error), as a
    #     list of response lines (without line terminators).  Returns
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
    # \brief Sets the radio configuration based on a sequence of configuration
    #    dictionary keys.
    #
    # \param value The value to set in the configuration dictionary.
    # \param keys List of keys used to access the value in the dictionary.
    # \return True if all commands completed successfully, False otherwise.
    #    Use getLastCommandErrorInfo() to retrieve any error information.
    def setConfigurationByKeys(self, value=None, *keys):
        raise NotImplementedError

    ##
    # \brief Gets the radio configuration.
    #
    # See setConfiguration() for the format of the returned dictionary.
    #
    # \return The dictionary of radio settings.
    def getConfiguration(self):
        raise NotImplementedError

    ##
    # \brief Gets radio configuration information based on a sequence of configuration
    #    dictionary keys.
    #
    # \param keys List of keys used to access the value in the dictionary.
    # \return The radio setting(s) at the given level, or None if the configuration
    #    does not have data accessible by the given keys.
    def getConfigurationByKeys(self, *keys):
        raise NotImplementedError

    ##
    # \brief Queries the radio hardware to get its configuration.
    #
    # See setConfiguration() for the format of the returned dictionary.
    #
    # \return The dictionary of radio settings.
    def queryConfiguration(self):
        raise NotImplementedError

    ##
    # \brief Queries the radio hardware to get a subset of configuration information,
    #    based on a sequence of configuration dictionary keys.
    #
    # See setConfiguration() for the format of the returned dictionary.
    #
    # \param keys List of keys used to specify which configuration values to query.
    # \return The radio setting(s) that were updated by the call, as a dictionary.
    def queryConfigurationByKeys(self, *keys):
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
    # \param newPpsTime A specific UTC date/time to set the radio's clock to
    #     (string).  This method supports several formats for the time string,
    #     including YYYY-MM-DD HH:MM:SS and ISO 8601.  Set this to None if you
    #     want to use the current system/GPS time.
    # \return True if successful, False if the radio does not support
    # PPS edge detection and time setting or if the command was unsuccessful.
    def setTimeNextPps(self,checkTime=False,useGpsTime=False,newPpsTime=None):
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
    # \param go Whether to execute the sequence (1) or not (0).
    # \return True if successful, False if unsuccessful or if setting
    #    GPIO output is not supported.
    def setGpioOutputByIndex(self, index, value, duration, loop, go):
        raise NotImplementedError

    ##
    # \brief Gets the current bandwith of the given tuner.
    # \param tuner Tuner index number
    # \returns The tuner bandwidth, in Hz
    # \throws ValueError if the tuner does not exist on the radio
    def getTunerBandwidth(self, tuner):
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
    # \brief Gets the number of tuner boards on the radio.
    #
    # \return The number of tuner boards.
    @classmethod
    def getNumTunerBoards(cls):
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
    # \brief Gets the ifFilter list for the tuners of the radio
    #
    # \return The list of IF filter values
    @classmethod
    def getTunerIfFilterList(cls):
        raise NotImplementedError

    ##
    # \brief Gets whether or not the radio supports setting tuner
    #     bandwidth
    #
    # \return True if the bandwidth is settable, False otherwise
    @classmethod
    def isTunerBandwidthSettable(cls):
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
    # \param index If not None, get the set for the DDC with the given index.
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates.
    @classmethod
    def getWbddcRateSet(cls, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed rate list for the wideband DDCs on the radio.
    #
    # \param index If not None, get the list for the DDC with the given index.
    # \return The rate list.  This is a list of rate values, following the
    #     order of their corresponding rate indices.
    @classmethod
    def getWbddcRateList(cls, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed bandwidth set for the wideband DDCs on the radio.
    #
    # \param index If not None, get the set for the DDC with the given index.
    # \return The bandwidth set.  This is a dictionary whose keys are rate
    #     indices and whose values are the corresponding bandwidths.
    @classmethod
    def getWbddcBwSet(cls, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed rate list for the wideband DDCs on the radio.
    #
    # \param index If not None, get the list for the DDC with the given index.
    # \return The bandwidth list.  This is a list of bandwidth values,
    #     following the order of their corresponding rate indices.
    @classmethod
    def getWbddcBwList(cls, index=None):
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
    # \param index If not None, get the set for the DDC with the given index.
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates.
    @classmethod
    def getNbddcRateSet(cls, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed rate list for the narrowband DDCs on the radio.
    #
    # \param index If not None, get the list for the DDC with the given index.
    # \return The rate list.  This is a list of rate values, following the
    #     order of their corresponding rate indices.
    @classmethod
    def getNbddcRateList(cls, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed bandwidth set for the narrowband DDCs on the radio.
    #
    # \param index If not None, get the set for the DDC with the given index.
    # \return The bandwidth set.  This is a dictionary whose keys are rate
    #     indices and whose values are the corresponding bandwidths.
    @classmethod
    def getNbddcBwSet(cls, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed bandwidth list for the narrowband DDCs on the radio.
    #
    # \param index If not None, get the list for the DDC with the given index.
    # \return The bandwidth list.  This is a list of bandwidth values,
    #     following the order of their corresponding rate indices.
    @classmethod
    def getNbddcBwList(cls, index=None):
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
    # \param index If not None, get the set for the DDC with the given index.
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates.
    @classmethod
    def getDdcRateSet(cls, wideband, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed rate list for the DDCs on the radio.
    #
    # \deprecated Use getWbddcRateList() or getNbddcRateList() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).
    # \param index If not None, get the set for the DDC with the given index.
    # \return The rate list.  This is a list of rate values, following the
    #     order of their corresponding rate indices.
    @classmethod
    def getDdcRateList(cls, wideband, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed bandwidth set for the DDCs on the radio.
    #
    # \deprecated Use getWbddcBwSet() or getNbddcBwSet() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).
    # \param index If not None, get the set for the DDC with the given index.
    # \return The bandwidth set.  This is a dictionary whose keys are rate
    #     indices and whose values are the corresponding bandwidths.
    @classmethod
    def getDdcBwSet(cls, wideband, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the allowed bandwidth list for the DDCs on the radio.
    #
    # \deprecated Use getWbddcBwList() or getNbddcBwList() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).
    # \param index If not None, get the set for the DDC with the given index.
    # \return The bandwidth list.  This is a list of bandwidth values,
    #     following the order of their corresponding rate indices.
    @classmethod
    def getDdcBwList(cls, wideband, index=None):
        raise NotImplementedError

    ##
    # \brief Gets the set of available DDC data formats.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).
    # \return A dictionary where the keys are rate indices and the values are
    #    the corresponding DDC data formats ("iq" or "real").
    @classmethod
    def getDdcDataFormat(cls, wideband):
        raise NotImplementedError

    ##
    # \brief Gets whether the DDCs on the radio have selectable sources.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).
    # \return True if selectable, False otherwise.
    @classmethod
    def isDdcSelectableSource(cls, wideband):
        raise NotImplementedError

    ##
    # \brief Gets the list of DDC indexes for a specified type.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).
    # \return The list of DDC indices for that type.
    @classmethod
    def getDdcIndexRange(cls, wideband):
        raise NotImplementedError

    ##
    # \brief Gets the number of FFT streams on the radio.
    #
    # \return The number of FFT streams.
    @classmethod
    def getNumFftStream(cls):
        raise NotImplementedError

    ##
    # \brief Gets the index range for the FFT streams on the radio.
    #
    # \return The list of FFT stream indices.
    @classmethod
    def getFftStreamIndexRange(cls):
        raise NotImplementedError

    ##
    # \brief Gets the allowed rate set for the FFT streams on the radio.
    #
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates.
    @classmethod
    def getFftStreamRateSet(cls,):
        raise NotImplementedError

    ##
    # \brief Gets the allowed rate list for the FFT streams on the radio.
    #
    # \return The rate list.  This is a list of rate values, following the
    #     order of their corresponding rate indices.
    @classmethod
    def getFftStreamRateList(cls,):
        raise NotImplementedError

    ##
    # \brief Gets the allowed window set for the FFT streams on the radio.
    #
    # \return The window set.  This is a dictionary whose keys are window
    #     types and whose values are the corresponding descriptions.
    @classmethod
    def getFftStreamWindowSet(cls,):
        raise NotImplementedError

    ##
    # \brief Gets the allowed window list for the FFT streams on the radio.
    #
    # \return The window list.  This is a list of window descriptions, following
    #     the order of their corresponding window types.
    @classmethod
    def getFftStreamWindowList(cls,):
        raise NotImplementedError

    ##
    # \brief Gets the allowed size set for the FFT streams on the radio.
    #
    # \return The size set.  This is a dictionary whose keys are size
    #     identifiers and whose values are the corresponding FFT sizes.
    @classmethod
    def getFftStreamSizeSet(cls,):
        raise NotImplementedError

    ##
    # \brief Gets the allowed size list for the FFT streams on the radio.
    #
    # \return The size list.  This is a list of FFT sizes, following
    #     the order of their corresponding size identifiers.
    @classmethod
    def getFftStreamSizeList(cls,):
        raise NotImplementedError

    ##
    # \brief Gets the ADC sample rate for the radio.
    #
    # \return The ADC sample rate, in samples per second.
    @classmethod
    def getAdcRate(cls):
        raise NotImplementedError

    ##
    # \brief Gets the VITA 49 header size for the radio.
    #
    # \param payloadType The type of payload (string).  Only has meaning
    #     for radios that support multiple VITA packet formats.
    #
    # \return The header size, in bytes.
    @classmethod
    def getVitaHeaderSize(cls, payloadType=None):
        raise NotImplementedError

    ##
    # \brief Gets the VITA 49 payload size for the radio.
    #
    # If VITA 49 output is disabled, then the returned value
    # indicates the number of raw I/Q data bytes in each packet.
    #
    # \param payloadType The type of payload (string).  Only has meaning
    #     for radios that support multiple VITA packet formats.
    # \return The payload size, in bytes.
    @classmethod
    def getVitaPayloadSize(cls, payloadType=None):
        raise NotImplementedError

    ##
    # \brief Gets the VITA 49 tail size for the radio.
    #
    # \param payloadType The type of payload (string).  Only has meaning
    #     for radios that support multiple VITA packet formats.
    #
    # \return The tail size, in bytes.
    @classmethod
    def getVitaTailSize(cls, payloadType=None):
        raise NotImplementedError

    ##
    # \brief Gets dictionary with information about VITA 49 framing.
    #
    # A framing information dictionary contains the following elements:
    # * "headerWords": Number of 32-bit words in the VITA 49 header
    # * "payloadWords": Number of 32-bit words in the VITA 49 payload
    # * "tailWords": Number of 32-bit words in the VITA 49 trailer
    # * "frameSize": Number of bytes in the VITA 49 frame
    # * "v49.0": Whether Vita 49.0 is used
    # * "v49.1": Whether Vita 49.1 is used
    # * "byteSwap": Whether the byte order in the VITA 49 frame is swapped
    #   with respect to the byte order used by the system
    # * "iqSwap": Whether the I and Q samples in the payload are swapped
    #
    # \param payloadType The type of payload (string).  Only has meaning
    #     for radios that support multiple VITA packet formats.
    #
    # \return The framing information dictionary.
    @classmethod
    def getVitaFrameInfoDict(cls, payloadType=None):
        raise NotImplementedError

    ##
    # \brief Gets whether data coming from the radio is byte-swapped with
    # respect to the endianness of the host operating system.
    #
    # \param payloadType The type of payload (string).  Only has meaning
    #     for radios that support multiple VITA packet formats.
    #
    # \return True or False, as appropriate for the radio.
    @classmethod
    def isByteswapped(cls, payloadType=None):
        raise NotImplementedError

    ##
    # \brief Gets whether data coming from the radio has I and Q data swapped.
    #
    # \param payloadType The type of payload (string).  Only has meaning
    #     for radios that support multiple VITA packet formats.
    #
    # \return True or False, as appropriate for the radio.
    @classmethod
    def isIqSwapped(cls, payloadType=None):
        raise NotImplementedError

    ##
    # \brief Gets the byte order for data coming from the radio.
    #
    # \param payloadType The type of payload (string).  Only has meaning
    #     for radios that support multiple VITA packet formats.
    #
    # \return The byte order, as a string.
    @classmethod
    def getByteOrder(cls, payloadType=None):
        raise NotImplementedError

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
    # \brief Gets the radio's default baud rate.
    #
    # \return The default baud rate.  This has no meaning if the radio does
    #    not use serial control connections.
    @classmethod
    def getDefaultBaudrate(cls):
        raise NotImplementedError

    ##
    # \brief Gets the radio's default control port.
    #
    # \return The default port number.  This has no meaning if the radio does
    #    not use network control connections.
    @classmethod
    def getDefaultControlPort(cls):
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
    # \return The list of tonroot directorye generator indexes.
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
    # \brief Gets the frequency offset range for the wideband DUCs on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum).
    @classmethod
    def getWbducFrequencyRange(cls):
        raise NotImplementedError

    ##
    # \brief Gets the frequency resolution for wideband DUCs on the radio.
    #
    # \return The frequency resolution.
    @classmethod
    def getWbducFrequencyRes(cls):
        raise NotImplementedError

    ##
    # \brief Gets the frequency unit for wideband DUCs on the radio.
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
    def getWbducFrequencyUnit(cls):
        raise NotImplementedError

    ##
    # \brief Gets the attenuation range for the wideband DUCs on the radio.
    #
    # \return The attenuation range.  This is a 2-tuple: (minimum, maximum).
    @classmethod
    def getWbducAttenuationRange(cls):
        raise NotImplementedError

    ##
    # \brief Gets the attenuation resolution for wideband DUCs on the radio.
    #
    # \return The attenuation resolution.
    @classmethod
    def getWbducAttenuationRes(cls):
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

    ##
    # \brief Gets the number of wideband DDC groups on the radio.
    # \returns The number of DDC groups.
    @classmethod
    def getNumWbddcGroups(cls):
        raise NotImplementedError

    ##
    # \brief Gets the index range for the wideband DDC groups on the radio.
    #
    # \return The list of wideband DDC group indexes.
    @classmethod
    def getWbddcGroupIndexRange(cls):
        raise NotImplementedError

    ##
    # \brief Gets the number of narrowband DDC groups on the radio.
    # \returns The number of DDC groups.
    @classmethod
    def getNumNbddcGroups(cls):
        raise NotImplementedError

    ##
    # \brief Gets the index range for the narrowband DDC groups on the radio.
    #
    # \return The list of narrowband DDC group indexes.
    @classmethod
    def getNbddcGroupIndexRange(cls):
        raise NotImplementedError

    ##
    # \brief Gets the number of combined DDC groups on the radio.
    # \returns The number of DDC groups.
    @classmethod
    def getNumCombinedDdcGroups(cls):
        raise NotImplementedError

    ##
    # \brief Gets the index range for the combined DDC groups on the radio.
    #
    # \return The list of combined DDC group indexes.
    @classmethod
    def getCombinedDdcGroupIndexRange(cls):
        raise NotImplementedError

    ##
    # \brief Gets the number of wideband DUC groups on the radio.
    # \returns The number of DUC groups.
    @classmethod
    def getNumWbducGroups(cls):
        raise NotImplementedError

    ##
    # \brief Gets the index range for the wideband DUC groups on the radio.
    #
    # \return The list of wideband DUC group indexes.
    @classmethod
    def getWbducGroupIndexRange(cls):
        raise NotImplementedError

    ##
    # \brief Disables ethernet flow control on the radio.
    #
    # \return Boolean value to indicate success
    def disableTenGigFlowControl(self,):
        raise NotImplementedError

    ##
    # \brief Enables ethernet flow control on the radio.
    #
    # \return Boolean value to indicate success
    def enableTenGigFlowControl(self,):
        raise NotImplementedError

    ##
    # \brief method to enable or disable ethernet flow control on the radio.
    #
    # \return Boolean value to indicate success
    def setTenGigFlowControlStatus(self,enable=False):
        raise NotImplementedError

    ##
    # \brief Queries status of flow control handling.
    #
    # \return A dictionary of flow control statuses, keyed by 10GigE
    #    port number.
    def getTenGigFlowControlStatus(self,):
        raise NotImplementedError

    ##
    # \brief Performs coherent tuning.
    #
    # \param cohGroup Coherent tuning group number.
    # \param freq Frequency, in Hz.
    #
    # \return True if successful, False otherwise. Returns False if the radio
    #    does not support coherent tuning.
    def coherentTune(self, cohGroup, freq):
        raise NotImplementedError

    ##
    # \brief Gets the current FPGA state.
    # \returns The FPGA state indicator.  The meaning of the returned value
    #    depends on the radio.  Returns None if the radio does not support
    #    FPGA states.
    def getFpgaState(self):
        raise NotImplementedError

    ##
    # \brief Sets the current FPGA state.
    # \note Issuing this command will automatically disconnect the radio
    #    handler.
    # \param state The new FPGA state indicator.  The meaning of the this
    #    value depends on the radio.
    # \returns True if successful, False otherwise.  Returns False if the
    #    radio does not support manipulating the FPGA state.
    def setFpgaState(self, state):
        raise NotImplementedError

    ##
    # \brief Sets whether or not the object is in verbose mode.
    #
    # \param verbose True if verbose mode is set, False otherwise.
    def setVerbose(self, verbose):
        raise NotImplementedError

    ##
    # \brief Sets the log file.
    #
    # \param logFile File or file-like object that receives log messages.
    #    If None, logging is disabled.
    def setLogFile(self, logFile):
        raise NotImplementedError
    
    ##
    # \brief Gets the list of connected data port interface indices.
    # \note This method only applies to radio handler objects connected through
    #     crdd.  If the radio handler object is connected directly to the radio,
    #     then this method will return an empty list.
    # \returns The list of connected data port indices.  This will be an empty
    #     list in case of error.
    def getConnectedDataPorts(self):
        raise NotImplementedError
    
