#!/usr/bin/env python
###############################################################
# \package CyberRadio.NDR_driver_interface
# 
# \brief GNU Radio support for the CyberRadio Solutions NDR 
#    Driver
#
# \author DA
# 
# \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.  
#    All rights reserved.
#
###############################################################

from gnuradio import gr
import CyberRadioDriver
import sys


##
# \class NDR_driver_interface
# \ingroup CyberRadioBase
# \brief GNU Radio support for the CyberRadio Solutions NDR Driver.
#
# The NDR_driver_interface block allows GNU Radio applications to 
# access the CyberRadio Solutions NDR Driver to configure an NDR-class 
# radio and query its capabilities. The block supports all of the 
# methods from the Driver's IRadio interface; the results of those
# methods depend on which radio is being targeted.
#
# \implements CyberRadioDriver.IRadio
class NDR_driver_interface(gr.hier_block2):
    
    ##
    # \brief Creates an NDR_driver_interface object.
    #
    # \param radio_type The name string for the radio of interest (for
    #    example, "ndr304" for an NDR304 radio).
    # \param verbose Verbose mode (True or False).
    # \param log_file A file-like object to be used for log output.  
    #    If this is None, then log output is disabled.
    # \param connect_mode The connection mode to use to connect to the 
    #    radio.  This will be one of "", "tty", "tcp", or "udp".  
    #    Supported connection modes vary by radio.  If this is an 
    #    empty string, then no connection will be made.
    # \param dev_name For TTY connections, this is the name of the TTY 
    #    device representing the radio on the system.
    # \param baud_rate For TTY connections, this is the baud rate (bits 
    #    per second).
    # \param host_name For TCP/UDP connections, this is the host name
    #    used by the radio.
    # \param host_name For TCP/UDP connections, this is the port number
    #    used by the radio.
    def __init__(self, radio_type=None, verbose=True, log_file=None, 
                 connect_mode=None, dev_name=None, baud_rate=None, 
                 host_name=None, host_port=None):
        gr.hier_block2.__init__(
            self, "[CyberRadio] NDR Driver Interface",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0),
        )
        self.pyradio = None
        self.pyradio_cls = None
        self.radio_type = radio_type
        self.verbose = verbose
        self.log_file = log_file
        self.connect_mode = connect_mode
        self.dev_name = dev_name
        self.baud_rate = baud_rate 
        self.host_name = host_name
        self.host_port = host_port
        self.last_error = ""
        self._do_connect()
        
    def __del__(self):
        if self.isConnected():
            self.disconnect()
            
    # Getters and setters for GNU Radio's callback method paradigm
    
    ##
    # \brief Gets the radio type string.
    # \return The radio type string.
    def get_radio_type(self):
        return self.radio_type
    
    ##
    # \brief Sets the radio type string.
    # \param radio_type The radio type string.
    def set_radio_type(self, radio_type):
        self.radio_type = radio_type
        return self._do_connect()
    
    ##
    # \brief Gets the verbosity setting.
    # \return The verbosity setting.
    def get_verbose(self):
        return self.verbose
    
    ##
    # \brief Sets the verbosity setting.
    # \param verbose The verbosity setting.
    def set_verbose(self, verbose):
        self.verbose = verbose
        return self._do_connect()
    
    ##
    # \brief Gets the log file setting.
    # \return The log file setting.
    def get_log_file(self):
        return self.log_file
    
    ##
    # \brief Sets the log file setting.
    # \param log_file The log file setting.
    def set_log_file(self, log_file):
        self.log_file = log_file
        return self._do_connect()
    
    ##
    # \brief Gets the connection mode setting.
    # \return The connection mode setting.
    def get_connect_mode(self):
        return self.connect_mode
    
    ##
    # \brief Sets the connection mode setting.
    # \param connect_mode The connection mode setting.
    def set_connect_mode(self, connect_mode):
        self.connect_mode = connect_mode
        return self._do_connect()
    
    ##
    # \brief Gets the radio device name.
    # \return The radio device name.
    def get_dev_name(self):
        return self.dev_name
    
    ##
    # \brief Sets the radio device name.
    # \param dev_name The radio device name.
    def set_dev_name(self, dev_name):
        self.dev_name = dev_name
        return self._do_connect()
    
    ##
    # \brief Gets the radio baud rate.
    # \return The radio baud rate.
    def get_baud_rate(self):
        return self.baud_rate
    
    ##
    # \brief Sets the radio baud rate.
    # \param baud_rate The radio baud rate.
    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        return self._do_connect()
    
    ##
    # \brief Gets the radio host name.
    # \return The radio host name.
    def get_host_name(self):
        return self.host_name
    
    ##
    # \brief Sets the radio host name.
    # \param host_name The radio host name.
    def set_host_name(self, host_name):
        self.host_name = host_name
        return self._do_connect()
    
    ##
    # \brief Gets the radio host port.
    # \return The radio host port.
    def get_host_port(self):
        return self.host_port
    
    ##
    # \brief Sets the radio host port.
    # \param host_port The radio host port.
    def set_host_port(self, host_port):
        self.host_port = host_port
        return self._do_connect()
    
    ##
    # \brief Gets the last error encountered by the radio.
    # \return The last error message.
    def get_last_error(self):
        return self.last_error
    
    # Begin IRadio interface implementation
    
    ##
    # \brief Indicates whether the radio is connected.
    #
    # \return True if connected, False otherwise.
    def isConnected(self):
        return self._IRadio_method("isConnected", False)
    
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
        return self._IRadio_method("getVersionInfo", {})
        
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
        return self._IRadio_method("getConnectionInfo", {})
        
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
        return self._IRadio_method("connect", False, mode, host_or_dev, \
                                   port_or_baudrate, setTime, initDdc, \
                                   reset)
            
    ##
    # \brief Disconnects from the radio.
    def disconnect(self):
        return self._IRadio_method("disconnect", None)
    
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
        return self._IRadio_method("sendCommand", None, cmdString, timeout)
    
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
        return self._IRadio_method("setConfiguration", False, configDict)
    
    ##
    # \brief Gets the radio configuration.
    #
    # See setConfiguration() for the format of the returned
    # dictionary.
    #
    # \return The dictionary of radio settings.
    def getConfiguration(self):
        return self._IRadio_method("getConfiguration", {})
    
    ##
    # \brief Gets the last set of error information returned by the radio.
    #
    # The error information set is reset on each call to getConfiguration()
    # or setConfiguration().
    #
    # \return A list of error information strings.  This list will 
    # be empty if all commands completed successfully.
    def getLastCommandErrorInfo(self):
        return self._IRadio_method("getLastCommandErrorInfo", [])
    
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
        return self._IRadio_method("sendReset", False, resetType)
    
    ##
    # \brief Gets the pulse-per-second (PPS) rising edge from the radio.
    #
    # \return True if successful, False if the radio does not support
    # PPS edge detection or if the command was unsuccessful.
    def getPps(self):
        return self._IRadio_method("getPps", False)
    
    ##
    # \brief Sets the time for the next PPS rising edge on the radio.
    #
    # \param checkTime Whether to verify that the time was set properly.
    # \param useGpsTime Whether to use the GPS time rather than the system time.
    # \return True if successful, False if the radio does not support
    # PPS edge detection and time setting or if the command was unsuccessful.
    def setTimeNextPps(self,checkTime=False,useGpsTime=False):
        return self._IRadio_method("setTimeNextPps", False, checkTime, \
                                   useGpsTime)
            
    ##
    # \brief Gets the current radio time.
    #
    # \return The UTC time in seconds from the epoch, or None if the radio 
    # does not support time querying or if the command was unsuccessful.
    def getTimeNow(self):
        return self._IRadio_method("getTimeNow", None)
    
    ##
    # \brief Gets the time for the next PPS rising edge on the radio.
    #
    # \return The UTC time in seconds from the epoch, or None if the radio 
    # does not support PPS edge detection and time querying or if the command 
    # was unsuccessful.
    def getTimeNextPps(self):
        return self._IRadio_method("getTimeNextPps", None)
    
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
        return self._IRadio_method("getStatus", {})
    
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
        return self._IRadio_method("getTstatus", {})
    
    ##
    # \brief Sets the reference mode on the radio.
    #
    # \param mode An integer indicating the reference mode to set.  Valid
    # reference mode numbers vary by radio.
    # \return True if successful, False if unsuccessful or if reference mode
    # setting is not supported on the radio or if the provided mode is not
    # supported. 
    def setReferenceMode(self,mode):
        return self._IRadio_method("setReferenceMode", False, mode)
    
    ##
    # \brief Sets the reference bypass mode on the radio.
    #
    # \param mode An integer indicating the reference bypass mode to set.  Valid
    # bypass mode numbers vary by radio.
    # \return True if successful, False if unsuccessful or if reference bypass mode
    # setting is not supported on the radio or if the provided mode is not
    # supported. 
    def setBypassMode(self,mode):
        return self._IRadio_method("setBypassMode", False, mode)
            
    ##
    # \brief Sets the time adjustment for tuners on the radio.
    #
    # \param tunerIndex Either None (adjust all tuners), a tuner index number 
    #    (adjust that tuner alone), or a list of tuner index numbers.
    # \param timeAdjustValue Time adjustment value.
    # \return True if successful, False if unsuccessful or if adjusting the time
    #    is not supported. 
    def setTimeAdjustment(self,tunerIndex=None,timeAdjustValue=0):
        return self._IRadio_method("setTimeAdjustment", False, tunerIndex, \
                                   timeAdjustValue)

    ##
    # \brief Sets the calibration frequency on the radio.
    #
    # \param calibFrequency The frequency to set, in MHz.  If 0, disable the 
    #    calibration signal.
    # \return True if successful, False if unsuccessful or if adjusting calibration
    #    frequency is not supported. 
    def setCalibrationFrequency(self, calibFrequency=0):
        return self._IRadio_method("setCalibrationFrequency", False, 
                                   calibFrequency)

    ##
    # \brief Gets the name of the radio.
    #
    # \return The name, as a string. 
    def getName(self):
        return self._IRadio_classmethod("getName", "")
    
    ##
    # \brief Gets the number of tuners on the radio.
    #
    # \return The number of tuners. 
    def getNumTuner(self):
        return self._IRadio_classmethod("getNumTuner", 0)
    
    ##
    # \brief Gets the index range for the tuners on the radio.
    #
    # \return The list of tuner indexes. 
    def getTunerIndexRange(self):
        return self._IRadio_classmethod("getTunerIndexRange", (0.0, 0.0))
    
    ##
    # \brief Gets the frequency range for the tuners on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    def getTunerFrequencyRange(self):
        return self._IRadio_classmethod("getTunerFrequencyRange", (0.0, 0.0))
    
    ##
    # \brief Gets the frequency resolution for tuners on the radio.
    #
    # \return The frequency resolution. 
    def getTunerFrequencyRes(self):
        return self._IRadio_classmethod("getTunerFrequencyRes", 0.0)
    
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
    def getTunerFrequencyUnit(self):
        return self._IRadio_classmethod("getTunerFrequencyUnit", 0.0)
    
    ##
    # \brief Gets the attenuation range for the tuners on the radio.
    #
    # \return The attenuation range.  This is a 2-tuple: (minimum, maximum). 
    def getTunerAttenuationRange(self):
        return self._IRadio_classmethod("getTunerAttenuationRange", (0.0, 0.0))
    
    ##
    # \brief Gets the attenuation resolution for tuners on the radio.
    #
    # \return The attenuation resolution. 
    def getTunerAttenuationRes(self):
        return self._IRadio_classmethod("getTunerAttenuationRes", 0.0)
    
    ##
    # \brief Gets the number of wideband DDCs on the radio.
    #
    # \return The number of wideband DDCs. 
    def getNumWbddc(self):
        return self._IRadio_classmethod("getNumWbddc", 0)
    
    ##
    # \brief Gets the index range for the wideband DDCs on the radio.
    #
    # \return The list of wideband DDC indexes. 
    def getWbddcIndexRange(self):
        return self._IRadio_classmethod("getWbddcIndexRange", (0, 0))
    
    ##
    # \brief Gets whether the wideband DDCs on the radio are tunable.
    #
    # \return True if tunable, False otherwise.
    def isWbddcTunable(self):
        return self._IRadio_classmethod("isWbddcTunable", False)
    
    ##
    # \brief Gets whether the wideband DDCs on the radio have selectable
    # sources.
    #
    # \return True if selectable, False otherwise.
    def isWbddcSelectableSource(self):
        return self._IRadio_classmethod("isWbddcSelectableSource", False)
    
    ##
    # \brief Gets the frequency offset range for the wideband DDCs on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    def getWbddcFrequencyRange(self):
        return self._IRadio_classmethod("getWbddcFrequencyRange", (0.0, 0.0))
    
    ##
    # \brief Gets the frequency offset resolution for wideband DDCs on the radio.
    #
    # \return The frequency offset resolution. 
    def getWbddcFrequencyRes(self):
        return self._IRadio_classmethod("getWbddcFrequencyRes", 0.0)
    
    ##
    # \brief Gets the allowed rate set for the wideband DDCs on the radio.
    #
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    def getWbddcRateSet(self):
        return self._IRadio_classmethod("getWbddcRateSet", {})
    
    ##
    # \brief Gets the allowed rate list for the wideband DDCs on the radio.
    #
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    def getWbddcRateList(self):
        return self._IRadio_classmethod("getWbddcRateList", [])

    ##
    # \brief Gets the number of narrowband DDCs on the radio.
    #
    # \return The number of narrowband DDCs. 
    def getNumNbddc(self):
        return self._IRadio_classmethod("getNumNbddc", 0)
    
    ##
    # \brief Gets the index range for the narrowband DDCs on the radio.
    #
    # \return The list of narrowband DDC indexes. 
    def getNbddcIndexRange(self):
        return self._IRadio_classmethod("getNbddcIndexRange", (0.0, 0.0))
    
    ##
    # \brief Gets whether the narrowband DDCs on the radio are tunable.
    #
    # \return True if tunable, False otherwise.
    def isNbddcTunable(self):
        return self._IRadio_classmethod("isNbddcTunable", False)
    
    ##
    # \brief Gets whether the narrowband DDCs on the radio have selectable
    # sources.
    #
    # \return True if selectable, False otherwise.
    def isNbddcSelectableSource(self):
        return self._IRadio_classmethod("isNbddcSelectableSource", False)
    
    ##
    # \brief Gets the frequency offset range for the narrowband DDCs on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    def getNbddcFrequencyRange(self):
        return self._IRadio_classmethod("getNbddcFrequencyRange", (0.0, 0.0))
    
    ##
    # \brief Gets the frequency offset resolution for narrowband DDCs on the radio.
    #
    # \return The frequency offset resolution. 
    def getNbddcFrequencyRes(self):
        return self._IRadio_classmethod("getNbddcFrequencyRes", 0.0)
    
    ##
    # \brief Gets the allowed rate set for the narrowband DDCs on the radio.
    #
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    def getNbddcRateSet(self):
        return self._IRadio_classmethod("getNbddcRateSet", {})
    
    ##
    # \brief Gets the allowed rate list for the narrowband DDCs on the radio.
    #
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    def getNbddcRateList(self):
        return self._IRadio_classmethod("getNbddcRateList", [])

    ##
    # \brief Gets the number of DDCs on the radio.
    #
    # \deprecated Use getNumWbddc() or getNumNbddc() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).  
    # \return The number of DDCs of the provided type. 
    def getNumDdc(self, wideband):
        return self._IRadio_classmethod("getNumDdc", 0, wideband)
    
    ##
    # \brief Gets the allowed rate set for the DDCs on the radio.
    #
    # \deprecated Use getWbddcRateSet() or getNbddcRateSet() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).  
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    def getDdcRateSet(self, wideband):
        return self._IRadio_classmethod("getDdcRateSet", {})
    
    ##
    # \brief Gets the allowed rate list for the DDCs on the radio.
    #
    # \deprecated Use getWbddcRateList() or getNbddcRateList() instead.
    #
    # \param wideband Whether to look at wideband DDCs (True) or narrowband
    #     DDCs (False).  
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    def getDdcRateList(self, wideband):
        return self._IRadio_classmethod("getDdcRateList", [])

    ##
    # \brief Gets the VITA 49 header size for the radio.
    #
    # \return The header size, in bytes.
    def getVitaHeaderSize(self):
        return self._IRadio_classmethod("getVitaHeaderSize", 0)
    
    ##
    # \brief Gets the VITA 49 payload size for the radio.
    #
    # If VITA 49 output is disabled, then the returned value 
    # indicates the number of raw I/Q data bytes in each packet. 
    #
    # \return The payload size, in bytes.
    def getVitaPayloadSize(self):
        return self._IRadio_classmethod("getVitaPayloadSize", 0)
    
    ##
    # \brief Gets the VITA 49 tail size for the radio.
    #
    # \return The tail size, in bytes.
    def getVitaTailSize(self):
        return self._IRadio_classmethod("getVitaTailSize", 0)
    
    ##
    # \brief Gets whether data coming from the radio is byte-swapped with 
    # respect to the endianness of the host operating system.
    # \return True or False, as appropriate for the radio.
    def isByteswapped(self):
        return self._IRadio_classmethod("isByteswapped", False)
    
    ##
    # \brief Gets whether data coming from the radio has I and Q data swapped.
    #
    # \return True or False, as appropriate for the radio.
    def isIqSwapped(self):
        return self._IRadio_classmethod("isIqSwapped", False)

    ##
    # \brief Gets the number of Gigabit Ethernet interfaces on the radio.
    #
    # \return The number of GigE interfaces. 
    def getNumGigE(self):
        return self._IRadio_classmethod("getNumGigE", 0)
    
    ##
    # \brief Gets the index range for the Gigabit Ethernet interfaces on the radio.
    #
    # \return The list of GigE interface indexes. 
    def getGigEIndexRange(self):
        return self._IRadio_classmethod("getGigEIndexRange", (0, 0))
    
    ##
    # \brief Gets the number of destination IP address table entries available for 
    # each Gigabit Ethernet interface on the radio.
    #
    # \return The number of destination IP address table entries. 
    def getNumGigEDipEntries(self):
        return self._IRadio_classmethod("getNumGigEDipEntries", 0)
    
    ##
    # \brief Gets the index range for the destination IP address table entries 
    # available for the Gigabit Ethernet interfaces on the radio.
    #
    # \return The list of destination IP address table entry indexes. 
    def getGigEDipEntryIndexRange(self):
        return self._IRadio_classmethod("getGigEDipEntryIndexRange", (0, 0))
    
    ##
    # \brief Gets the list of connection modes that the radio supports.
    #
    # \return The list of connection modes. 
    def getConnectionModeList(self):
        return self._IRadio_classmethod("getConnectionModeList", [])
    
    ##
    # \brief Gets whether the radio supports a given connection mode.
    #
    # \param mode The connection mode of interest.
    # \return True if the connection mode is supported, False otherwise.
    def isConnectionModeSupported(self, mode):
        return self._IRadio_classmethod("isConnectionModeSupported", False, mode)
    
    ##
    # \brief Gets the allowed VITA enable options set for the radio.
    #
    # \return The option set.  This is a dictionary whose keys are 
    #     VITA enable option values and whose values are the corresponding 
    #     meanings for those values. 
    def getVitaEnableOptionSet(self):
        return self._IRadio_classmethod("getVitaEnableOptionSet", {})
    
    ##
    # \brief Gets the number of transmitters on the radio.
    #
    # \return The number of transmitters. 
    def getNumTransmitters(self):
        return self._IRadio_classmethod("getNumTransmitters", 0)
    
    ##
    # \brief Gets the index range for the transmitters on the radio.
    #
    # \return The list of transmitter indexes. 
    def getTransmitterIndexRange(self):
        return self._IRadio_classmethod("getTransmitterIndexRange", (0, 0))
    
    ##
    # \brief Gets the frequency range for the transmitters on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterFrequencyRange(self):
        return self._IRadio_classmethod("getTransmitterFrequencyRange", (0.0, 0.0))
    
    ##
    # \brief Gets the frequency resolution for transmitters on the radio.
    #
    # \return The frequency resolution. 
    def getTransmitterFrequencyRes(self):
        return self._IRadio_classmethod("getTransmitterFrequencyRes", 0.0)
    
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
    def getTransmitterFrequencyUnit(self):
        return self._IRadio_classmethod("getTransmitterFrequencyUnit", 0.0)
    
    ##
    # \brief Gets the attenuation range for the transmitters on the radio.
    #
    # \return The attenuation range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterAttenuationRange(self):
        return self._IRadio_classmethod("getTransmitterAttenuationRange", (0.0, 0.0))
    
    ##
    # \brief Gets the attenuation resolution for transmitters on the radio.
    #
    # \return The attenuation resolution. 
    def getTransmitterAttenuationRes(self):
        return self._IRadio_classmethod("getTransmitterAttenuationRes", 0.0)
    
    ##
    # \brief Gets whether transmitters on the radio support continuous-wave
    # (CW) tone generation.
    #
    # \return True if tone generation is supported, False otherwise. 
    def transmitterSupportsCW(self):
        return self._IRadio_classmethod("getTunerAttenuationRange", False)

    ##
    # \brief Gets the number of CW tone generators for each transmitter.
    #
    # \return The number of tone generators. 
    def getTransmitterCWNum(self):
        return self._IRadio_classmethod("getTransmitterCWNum", 0)

    ##
    # \brief Gets the CW tone generator index range for transmitters on the radio.
    #
    # \return The list of tone generator indexes. 
    def getTransmitterCWIndexRange(self):
        return self._IRadio_classmethod("getTransmitterCWIndexRange", (0, 0))
    
    ##
    # \brief Gets the CW tone generator frequency range for transmitters on the radio.
    #
    # \return The frequency range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterCWFrequencyRange(self):
        return self._IRadio_classmethod("getTransmitterCWFrequencyRange", (0.0, 0.0))
    
    ##
    # \brief Gets the CW tone generator frequency resolution for transmitters on the radio.
    #
    # \return The frequency resolution. 
    def getTransmitterCWFrequencyRes(self):
        return self._IRadio_classmethod("getTransmitterCWFrequencyRes", 0.0)
    
    ##
    # \brief Gets the CW tone generator amplitude range for transmitters on the radio.
    #
    # \return The amplitude range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterCWAmplitudeRange(self):
        return self._IRadio_classmethod("getTransmitterCWAmplitudeRange", (0.0, 0.0))
    
    ##
    # \brief Gets the CW tone generator amplitude resolution for transmitters on the radio.
    #
    # \return The amplitude resolution. 
    def getTransmitterCWAmplitudeRes(self):
        return self._IRadio_classmethod("getTransmitterCWAmplitudeRes", 0.0)
    
    ##
    # \brief Gets the CW tone generator phase range for transmitters on the radio.
    #
    # \return The phase range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterCWPhaseRange(self):
        return self._IRadio_classmethod("getTransmitterCWPhaseRange", (0.0, 0.0))
    
    ##
    # \brief Gets the CW tone generator phase resolution for transmitters on the radio.
    #
    # \return The phase resolution. 
    def getTransmitterCWPhaseRes(self):
        return self._IRadio_classmethod("getTransmitterCWPhaseRes", 0.0)
    
    ##
    # \brief Gets whether transmitters on the radio support sweep functions
    # during continuous-wave (CW) tone generation.
    #
    # \return True if sweep is supported, False otherwise. 
    def transmitterSupportsCWSweep(self):
        return self._IRadio_classmethod("transmitterSupportsCWSweep", False)

    ##
    # \brief Gets the CW tone generator sweep start frequency range for 
    # transmitters on the radio.
    #
    # \return The start range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterCWSweepStartRange(self):
        return self._IRadio_classmethod("getTransmitterCWSweepStartRange", (0.0, 0.0))
    
    ##
    # \brief Gets the CW tone generator sweep start frequency resolution for 
    # transmitters on the radio.
    #
    # \return The start resolution. 
    def getTransmitterCWSweepStartRes(self):
        return self._IRadio_classmethod("getTransmitterCWSweepStartRes", 0.0)
    
    ##
    # \brief Gets the CW tone generator sweep stop frequency range for 
    # transmitters on the radio.
    #
    # \return The stop range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterCWSweepStopRange(self):
        return self._IRadio_classmethod("getTransmitterCWSweepStopRange", (0.0, 0.0))
    
    ##
    # \brief Gets the CW tone generator sweep stop frequency resolution for 
    # transmitters on the radio.
    #
    # \return The stop resolution. 
    def getTransmitterCWSweepStopRes(self):
        return self._IRadio_classmethod("getTransmitterCWSweepStopRes", 0.0)
    
    ##
    # \brief Gets the CW tone generator sweep step frequency range for 
    # transmitters on the radio.
    #
    # \return The step range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterCWSweepStepRange(self):
        return self._IRadio_classmethod("getTransmitterCWSweepStepRange", (0.0, 0.0))
    
    ##
    # \brief Gets the CW tone generator sweep step frequency resolution for 
    # transmitters on the radio.
    #
    # \return The step resolution. 
    def getTransmitterCWSweepStepRes(self):
        return self._IRadio_classmethod("getTransmitterCWSweepStepRes", 0.0)
    
    ##
    # \brief Gets the CW tone generator sweep dwell time range for 
    # transmitters on the radio.
    #
    # \return The dwell time range.  This is a 2-tuple: (minimum, maximum). 
    def getTransmitterCWSweepDwellRange(self):
        return self._IRadio_classmethod("getTransmitterCWSweepDwellRange", (0.0, 0.0))
    
    ##
    # \brief Gets the CW tone generator sweep dwell time resolution for 
    # transmitters on the radio.
    #
    # \return The dwell time resolution. 
    def getTransmitterCWSweepDwellRes(self):
        return self._IRadio_classmethod("getTransmitterCWSweepDwellRes", 0.0)
    
    ##
    # \brief Gets the number of wideband DUCs on the radio.
    #
    # \return The number of wideband DUCs. 
    def getNumWbduc(self):
        return self._IRadio_classmethod("getNumWbduc", 0)
    
    ##
    # \brief Gets the index range for the wideband DUCs on the radio.
    #
    # \return The list of wideband DUC indexes. 
    def getWbducIndexRange(self):
        return self._IRadio_classmethod("getWbducIndexRange", (0, 0))
    
    ##
    # \brief Gets the allowed rate set for the wideband DUCs on the radio.
    #
    # \return The rate set.  This is a dictionary whose keys are rate indices
    #     and whose values are the corresponding rates. 
    def getWbducRateSet(self):
        return self._IRadio_classmethod("getWbducRateSet", {})
    
    ##
    # \brief Gets the allowed rate list for the wideband DUCs on the radio.
    #
    # \return The rate list.  This is a list of rate values, following the 
    #     order of their corresponding rate indices. 
    def getWbducRateList(self):
        return self._IRadio_classmethod("getWbducRateList", [])

    ##
    # \brief Gets whether or not the wideband DUCs on the radio support loading
    # sample snapshots.
    #
    # \return True if supported, False otherwise.
    def wbducSupportsSnapshotLoad(self):
        return self._IRadio_classmethod("wbducSupportsSnapshotLoad", False)

    ##
    # \brief Gets whether or not the wideband DUCs on the radio support transmitting
    # sample snapshots.
    #
    # \return True if supported, False otherwise.
    def wbducSupportsSnapshotTransmit(self):
        return self._IRadio_classmethod("wbducSupportsSnapshotTransmit", False)

    # End IRadio interface implementation
    
    # Helper method -- executes an IRadio interface instance method, 
    # returning a default value if no radio handler object exists.
    def _IRadio_method(self, methodName, defaultReturn, *args, **kwargs):
        ret = defaultReturn
        try:
            ret = getattr(self.pyradio, methodName)(*args, **kwargs)
        except:
            pass
        return ret

    # Helper method -- executes an IRadio interface class method, 
    # returning a default value if no radio handler class exists.
    def _IRadio_classmethod(self, methodName, defaultReturn, *args, **kwargs):
        ret = defaultReturn
        try:
            ret = getattr(self.pyradio_cls, methodName)(*args, **kwargs)
        except:
            pass
        return ret

    # Helper method -- handles radio handler creation, connection, and
    # disconnection.  Returns True if there is a valid radio handler
    # object and if the connection completed successfully, False
    # otherwise.
    def _do_connect(self):
        ret = False
        if self.isConnected():
            self.disconnect()
        self.pyradio = None
        self.pyradio_cls = None
        if self.radio_type is None or self.radio_type == "":
            self.last_error = "No radio type defined"
        elif self.radio_type not in CyberRadioDriver.getSupportedRadios():
            self.last_error = "Unsupported radio type: %s" % str(self.radio_type)
        else:
            self.pyradio_cls = CyberRadioDriver.getRadioClass(self.radio_type)
            self.pyradio = CyberRadioDriver.getRadioObject(self.radio_type, \
                                                      verbose=self.verbose, \
                                                      logFile=self.log_file)
            if self.connect_mode == "":
                # No connection -- this mode supports class method queries
                # only.
                pass
            elif not self.isConnectionModeSupported(self.connect_mode):
                self.last_error = "Unsupported connection mode: %s" % \
                                  self.connect_mode
            elif self.connect_mode == "tty":
                ret = self.connect(self.connect_mode, self.dev_name, \
                                   self.baud_rate, False, False, False)
                if not ret:
                    self.last_error = "Could not connect to %s radio at %s" % \
                                      (self.getName(), self.dev_name)
            elif self.connect_mode in ["tcp", "udp"]:
                ret = self.connect(self.connect_mode, self.host_name, \
                                   self.host_port, False, False, False)
                if not ret:
                    self.last_error = "Could not connect to %s radio at %s" % \
                                      (self.getName(), self.host_name)
        return ret
    
    