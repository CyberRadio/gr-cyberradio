#!/usr/bin/env python
###############################################################
# \package CyberRadio.NDR304_source
# 
# \brief I/Q data source block using the NDR304 radio
#
# \author DA
# 
# \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.  
#    All rights reserved.
#
###############################################################

from gnuradio import gr
import CyberRadio
import copy
import CyberRadioDriver

##
# \class NDR304_source
# \ingroup CyberRadioNDR304
# \brief I/Q data source block using the NDR304 radio.
#
# The NDR304_source block supplies wideband DDC outputs, as indicated
# by the Number of WBDDCs setting. Any outputs supplied by this block are
# optional, so the user does not need to connect them if they are not
# being used.  The NDR304_source block also supplies a character-stream
# output for collecting logging data from the underlying driver interface.
# 
# Tuners and WBDDCs are configured via parameter lists.  Parameter
# lists are standard Python lists, formatted as follows:
# \li A tuner parameter list contains the following elements: [tuner 
#    enabled flag, tuner frequency (Hz), tuner attenuation (dB)]. 
# \li A WBDDC parameter list contains the following elements: [UDP 
#    port number, VITA type, sample rate index, enabled flag, 
#    DDC frequency offset (Hz)]. 
# 
# The NDR304_source block can also produce stream tags for any WBDDCs 
# configured to use VITA 49 frames.  See the documentation for the base 
# VITA I/Q Source block for details on the stream tags produced.
# 
# \note The parameter list scheme is a workaround to get around the
#    (undocumented) parameter limit that GNU Radio Companion 
#    silently imposes.
# 
class NDR304_source(gr.hier_block2):

    ##
    # \brief Constructs an NDR304_source object.
    #
    # \param verbose_mode Verbose mode for logging.
    # \param radio_device_name System device name for the radio.
    # \param radio_baud_rate Radio baud rate.
    # \param gig_iface_to_use The name of the Gigabit Ethernet interface 
    #    used by the radio.
    # \param coherent_mode Coherent mode setting on the radio.
    # \param num_tuners Number of tuners to use.
    # \param tuner1_param_list Tuner 1 parameter list. 
    # \param tuner2_param_list Tuner 2 parameter list.
    # \param tuner3_param_list Tuner 3 parameter list. 
    # \param tuner4_param_list Tuner 4 parameter list. 
    # \param tuner5_param_list Tuner 5 parameter list. 
    # \param tuner6_param_list Tuner 6 parameter list. 
    # \param num_wbddcs Number of WBDDCs to use.
    # \param wbddc1_param_list WBDDC 1 parameter list. 
    # \param wbddc2_param_list WBDDC 2 parameter list.
    # \param wbddc3_param_list WBDDC 3 parameter list. 
    # \param wbddc4_param_list WBDDC 4 parameter list. 
    # \param wbddc5_param_list WBDDC 5 parameter list. 
    # \param wbddc6_param_list WBDDC 6 parameter list. 
    # \param tagged Whether the block should produce stream tags.
    def __init__(self, 
                 verbose_mode=True, 
                 radio_device_name="/dev/ndr47x", 
                 radio_baud_rate=921600, 
                 gig_iface_to_use="eth0",
                 coherent_mode=0,
                 num_tuners=1,
                 tuner1_param_list=[False, 900e6, 0],
                 tuner2_param_list=[False, 900e6, 0],
                 tuner3_param_list=[False, 900e6, 0],
                 tuner4_param_list=[False, 900e6, 0],
                 tuner5_param_list=[False, 900e6, 0],
                 tuner6_param_list=[False, 900e6, 0],
                 num_wbddcs=1,
                 wbddc1_param_list=[40001, 0, 0, False, 0e6],
                 wbddc2_param_list=[40002, 0, 0, False, 0e6],
                 wbddc3_param_list=[40003, 0, 0, False, 0e6],
                 wbddc4_param_list=[40004, 0, 0, False, 0e6],
                 wbddc5_param_list=[40005, 0, 0, False, 0e6],
                 wbddc6_param_list=[40006, 0, 0, False, 0e6],
                 tagged=False,
                 ):
        gr.hier_block2.__init__(
            self, "[CyberRadio] NDR304 Source",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev((6 if coherent_mode & 0x02 > 0 else num_wbddcs) + 1, 
                             (6 if coherent_mode & 0x02 > 0 else num_wbddcs) + 1, 
                             [gr.sizeof_char*1] +
                             (6 if coherent_mode & 0x02 > 0 else num_wbddcs) * [gr.sizeof_gr_complex*1]), 
        )
        self.verbose_mode = verbose_mode
        self.radio_device_name = radio_device_name
        self.radio_baud_rate = radio_baud_rate
        self.gig_iface_to_use = gig_iface_to_use
        self.coherent_mode = coherent_mode
        self.tuners_coherent = (self.coherent_mode & 0x01 > 0)
        self.ddcs_coherent = (self.coherent_mode & 0x02 > 0)
        self.udp_host_name = CyberRadioDriver.getInterfaceAddresses(self.gig_iface_to_use)[1]
        self.num_tuners = num_tuners
        self.tuner1_param_list = tuner1_param_list
        if not self.tuners_coherent:
            self.tuner2_param_list = tuner2_param_list
            self.tuner3_param_list = tuner3_param_list
            self.tuner4_param_list = tuner4_param_list
            self.tuner5_param_list = tuner5_param_list
            self.tuner6_param_list = tuner6_param_list
        self.num_wbddcs = num_wbddcs
        self.wbddc1_param_list = wbddc1_param_list
        if not self.ddcs_coherent:
            self.wbddc2_param_list = wbddc2_param_list
            self.wbddc3_param_list = wbddc3_param_list
            self.wbddc4_param_list = wbddc4_param_list
            self.wbddc5_param_list = wbddc5_param_list
            self.wbddc6_param_list = wbddc6_param_list
        self.tagged = tagged
        self.CyberRadio_file_like_object_source_0 = CyberRadio.file_like_object_source()
        self.connect((self.CyberRadio_file_like_object_source_0, 0), (self, 0))
        self.CyberRadio_NDR_driver_interface_0 = CyberRadio.NDR_driver_interface(
            radio_type="ndr304",
            verbose=verbose_mode,
            log_file=self.CyberRadio_file_like_object_source_0,
            connect_mode="tty",
            dev_name=radio_device_name,
            baud_rate=radio_baud_rate,
        )
        self.vita_tail_size = self.CyberRadio_NDR_driver_interface_0.getVitaTailSize()
        self.vita_payload_size = self.CyberRadio_NDR_driver_interface_0.getVitaPayloadSize()
        self.vita_header_size = self.CyberRadio_NDR_driver_interface_0.getVitaHeaderSize()
        self.iq_swapped = self.CyberRadio_NDR_driver_interface_0.isIqSwapped()
        self.byte_swapped = self.CyberRadio_NDR_driver_interface_0.isByteswapped()
        self._set_coherent_mode(self.coherent_mode)
        self._set_udp_dest_info()
        if self.num_tuners >= 1:
            self._set_tuner_param_list(1, tuner1_param_list)
        if not self.tuners_coherent:
            if self.num_tuners >= 2:
                self._set_tuner_param_list(2, tuner2_param_list)
            if self.num_tuners >= 3:
                self._set_tuner_param_list(3, tuner3_param_list)
            if self.num_tuners >= 4:
                self._set_tuner_param_list(4, tuner4_param_list)
            if self.num_tuners >= 5:
                self._set_tuner_param_list(5, tuner5_param_list)
            if self.num_tuners >= 6:
                self._set_tuner_param_list(6, tuner6_param_list)
        self.wbddc_sources = {}
        if self.num_wbddcs >= 1:
            self.CyberRadio_vita_iq_source_wbddc_1 = self._get_configured_wbddc(1, wbddc1_param_list)
            if self.ddcs_coherent:
                self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 0), (self, 1))
                self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 1), (self, 2))
                self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 2), (self, 3))
                self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 3), (self, 4))
                self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 4), (self, 5))
                self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 5), (self, 6))
            else:
                self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 0), (self, 1))
            self.wbddc_sources[1] = self.CyberRadio_vita_iq_source_wbddc_1
        if not self.ddcs_coherent:
            if self.num_wbddcs >= 2:
                self.CyberRadio_vita_iq_source_wbddc_2 = self._get_configured_wbddc(2, wbddc2_param_list)
                self.connect((self.CyberRadio_vita_iq_source_wbddc_2, 0), (self, 2))
                self.wbddc_sources[2] = self.CyberRadio_vita_iq_source_wbddc_2
            if self.num_wbddcs >= 3:
                self.CyberRadio_vita_iq_source_wbddc_3 = self._get_configured_wbddc(3, wbddc3_param_list)
                self.connect((self.CyberRadio_vita_iq_source_wbddc_3, 0), (self, 3))
                self.wbddc_sources[3] = self.CyberRadio_vita_iq_source_wbddc_3
            if self.num_wbddcs >= 4:
                self.CyberRadio_vita_iq_source_wbddc_4 = self._get_configured_wbddc(4, wbddc4_param_list)
                self.connect((self.CyberRadio_vita_iq_source_wbddc_4, 0), (self, 4))
                self.wbddc_sources[4] = self.CyberRadio_vita_iq_source_wbddc_4
            if self.num_wbddcs >= 5:
                self.CyberRadio_vita_iq_source_wbddc_5 = self._get_configured_wbddc(5, wbddc5_param_list)
                self.connect((self.CyberRadio_vita_iq_source_wbddc_5, 0), (self, 5))
                self.wbddc_sources[5] = self.CyberRadio_vita_iq_source_wbddc_5
            if self.num_wbddcs >= 6:
                self.CyberRadio_vita_iq_source_wbddc_6 = self._get_configured_wbddc(6, wbddc6_param_list)
                self.connect((self.CyberRadio_vita_iq_source_wbddc_6, 0), (self, 6))
                self.wbddc_sources[6] = self.CyberRadio_vita_iq_source_wbddc_6


# QT sink close method reimplementation

    ##
    # \brief Gets the verbose mode setting.
    # \return The verbose mode setting.
    def get_verbose_mode(self):
        return self.verbose_mode

    ##
    # \brief Gets the radio device name.
    # \return The radio device name.
    def get_radio_device_name(self):
        return self.radio_device_name

    ##
    # \brief Gets the radio baud rate.
    # \return The radio baud rate.
    def get_radio_baud_rate(self):
        return self.radio_baud_rate

    ##
    # \brief Gets the GigE interface in use.
    # \return The GigE interface in use.
    def get_gig_iface_to_use(self):
        return self.gig_iface_to_use

    ##
    # \brief Gets the coherent mode setting.
    # \return The coherent mode setting.
    def get_coherent_mode(self):
        return self.coherent_mode

    ##
    # \brief Gets the number of tuners in use.
    # \return The the number of tuners in use.
    def get_num_tuners(self):
        return self.num_tuners

    ##
    # \brief Gets the parameter list for Tuner 1.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner1_param_list(self):
        return self.tuner1_param_list

    ##
    # \brief Sets the parameter list for Tuner 1.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner1_param_list(self, param_list):
        self.tuner1_param_list = param_list
        self._set_tuner_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for Tuner 2.
    # \note This method returns the Tuner 1 parameter list if the radio 
    #    is in tuner-coherent mode.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner2_param_list(self):
        return self.tuner2_param_list if not self.tuners_coherent else self.tuner1_param_list

    ##
    # \brief Sets the parameter list for Tuner 2.
    # \note This method does nothing if the radio is in tuner-coherent mode.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner2_param_list(self, param_list):
        if not self.tuners_coherent:
            self.tuner2_param_list = param_list
            self._set_tuner_param_list(2, param_list)

    ##
    # \brief Gets the parameter list for Tuner 3.
    # \note This method returns the Tuner 1 parameter list if the radio 
    #    is in tuner-coherent mode.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner3_param_list(self):
        return self.tuner3_param_list if not self.tuners_coherent else self.tuner1_param_list

    ##
    # \brief Sets the parameter list for Tuner 3.
    # \note This method does nothing if the radio is in tuner-coherent mode.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner3_param_list(self, param_list):
        if not self.tuners_coherent:
            self.tuner3_param_list = param_list
            self._set_tuner_param_list(3, param_list)

    ##
    # \brief Gets the parameter list for Tuner 4.
    # \note This method returns the Tuner 1 parameter list if the radio 
    #    is in tuner-coherent mode.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner4_param_list(self):
        return self.tuner4_param_list if not self.tuners_coherent else self.tuner1_param_list

    ##
    # \brief Sets the parameter list for Tuner 4.
    # \note This method does nothing if the radio is in tuner-coherent mode.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner4_param_list(self, param_list):
        if not self.tuners_coherent:
            self.tuner4_param_list = param_list
            self._set_tuner_param_list(4, param_list)

    ##
    # \brief Gets the parameter list for Tuner 5.
    # \note This method returns the Tuner 1 parameter list if the radio 
    #    is in tuner-coherent mode.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner5_param_list(self):
        return self.tuner5_param_list if not self.tuners_coherent else self.tuner1_param_list

    ##
    # \brief Sets the parameter list for Tuner 5.
    # \note This method does nothing if the radio is in tuner-coherent mode.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner5_param_list(self, param_list):
        if not self.tuners_coherent:
            self.tuner5_param_list = param_list
            self._set_tuner_param_list(5, param_list)

    ##
    # \brief Gets the parameter list for Tuner 6.
    # \note This method returns the Tuner 1 parameter list if the radio 
    #    is in tuner-coherent mode.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner6_param_list(self):
        return self.tuner6_param_list if not self.tuners_coherent else self.tuner1_param_list

    ##
    # \brief Sets the parameter list for Tuner 6.
    # \note This method does nothing if the radio is in tuner-coherent mode.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner6_param_list(self, param_list):
        if not self.tuners_coherent:
            self.tuner6_param_list = param_list
            self._set_tuner_param_list(6, param_list)

    ##
    # \brief Gets the number of WBDDCs in use.
    # \return The the number of WBDDCs in use.
    def get_num_wbddcs(self):
        return self.num_wbddcs

    ##
    # \brief Gets the parameter list for WBDDC 1.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc1_param_list(self):
        return self.wbddc1_param_list

    ##
    # \brief Sets the parameter list for WBDDC 1.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc1_param_list(self, param_list):
        self.wbddc1_param_list = param_list
        self._set_wbddc_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 2.
    # \note This method returns the WBDDC 1 parameter list if the radio 
    #    is in DDC-coherent mode.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc2_param_list(self):
        return self.wbddc2_param_list if not self.ddcs_coherent else self.wbddc1_param_list

    ##
    # \brief Sets the parameter list for WBDDC 2.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \note This method does nothing if the radio is in DDC-coherent mode.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc2_param_list(self, param_list):
        if not self.ddcs_coherent:
            self.wbddc2_param_list = param_list
            self._set_wbddc_param_list(2, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 3.
    # \note This method returns the WBDDC 1 parameter list if the radio 
    #    is in DDC-coherent mode.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc3_param_list(self):
        return self.wbddc3_param_list if not self.ddcs_coherent else self.wbddc1_param_list

    ##
    # \brief Sets the parameter list for WBDDC 3.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \note This method does nothing if the radio is in DDC-coherent mode.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc3_param_list(self, param_list):
        if not self.ddcs_coherent:
            self.wbddc3_param_list = param_list
            self._set_wbddc_param_list(3, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 4.
    # \note This method returns the WBDDC 1 parameter list if the radio 
    #    is in DDC-coherent mode.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc4_param_list(self):
        return self.wbddc4_param_list if not self.ddcs_coherent else self.wbddc1_param_list

    ##
    # \brief Sets the parameter list for WBDDC 4.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \note This method does nothing if the radio is in DDC-coherent mode.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc4_param_list(self, param_list):
        if not self.ddcs_coherent:
            self.wbddc4_param_list = param_list
            self._set_wbddc_param_list(4, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 5.
    # \note This method returns the WBDDC 1 parameter list if the radio 
    #    is in DDC-coherent mode.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc5_param_list(self):
        return self.wbddc5_param_list if not self.ddcs_coherent else self.wbddc1_param_list

    ##
    # \brief Sets the parameter list for WBDDC 5.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \note This method does nothing if the radio is in DDC-coherent mode.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc5_param_list(self, param_list):
        if not self.ddcs_coherent:
            self.wbddc5_param_list = param_list
            self._set_wbddc_param_list(5, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 6.
    # \note This method returns the WBDDC 1 parameter list if the radio 
    #    is in DDC-coherent mode.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc6_param_list(self):
        return self.wbddc6_param_list if not self.ddcs_coherent else self.wbddc1_param_list

    ##
    # \brief Sets the parameter list for WBDDC 6.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \note This method does nothing if the radio is in DDC-coherent mode.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc6_param_list(self, param_list):
        if not self.ddcs_coherent:
            self.wbddc6_param_list = param_list
            self._set_wbddc_param_list(6, param_list)

    ##
    # \brief Gets the nominal (expected) sample rate for a given WBDDC.
    # \param wbddc_index The WBDDC index.
    # \return The sample rate, in samples per second.
    def get_wbddc_nominal_sample_rate(self, wbddc_index):
        rate_index = self.CyberRadio_NDR_driver_interface_0.getConfiguration()['ddcConfiguration']['wideband'][wbddc_index]['rateIndex']
        rate_set = self.CyberRadio_NDR_driver_interface_0.getWbddcRateSet()
        return rate_set.get(rate_index, 0)
    
    ##
    # \brief Gets the real-time (measured) sample rate for a given WBDDC.
    # \param wbddc_index The WBDDC index.
    # \return The sample rate, in samples per second.
    def get_wbddc_realtime_sample_rate(self, wbddc_index):
        if wbddc_index in self.wbddc_sources:
            return self.wbddc_sources[wbddc_index].get_realtime_sample_rate()
        else:
            return 0
        
    def _set_udp_dest_info(self):
        destMac, destIp = CyberRadioDriver.getInterfaceAddresses(self.gig_iface_to_use)
        srcIpVec = destIp.split(".")
        srcIpVec[-1] = str(int(srcIpVec[-1]) + 100)
        srcIp = ".".join(srcIpVec)
        configDict = {
            "ipConfiguration": {
                 "sourceIP": srcIp,
                 "destIP": destIp,
                 "destMAC": destMac,
          },
        }
        #self.CyberRadio_file_like_object_source_0.write("Setting UDP Destination Info Config\n")
        #self.CyberRadio_file_like_object_source_0.write("configDict=%s\n" % str(configDict))
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
        #self.CyberRadio_file_like_object_source_0.write("Completed UDP Destination Info Config\n")
        
    def _set_coherent_mode(self, coherent_mode):
        self.CyberRadio_NDR_driver_interface_0.sendCommand("COH %d\n" % coherent_mode)
    
    def _set_tuner_param_list(self, tuner_index, tuner_param_list):
        configDict = {
          "tunerConfiguration": {
                tuner_index: {
                    'enable': tuner_param_list[0],
                    'frequency': tuner_param_list[1],
                    'attenuation': tuner_param_list[2],
                },
          },
        }
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
    
    def _set_wbddc_param_list(self, wbddc_index, wbddc_param_list, atinit=False):
        configDict = {
          "ddcConfiguration": {
            "wideband": {
                wbddc_index: {
                    'rateIndex': wbddc_param_list[2],
                    'enable': 1 if wbddc_param_list[3] else 0,
                    'frequency': wbddc_param_list[4],
                },
            },
          },
        }
        if atinit:
            configDict = self._merge_dicts(configDict, {
              "ddcConfiguration": {
                "wideband": {
                    wbddc_index: {
                        'udpDest': wbddc_param_list[0],          
                        'streamId': wbddc_param_list[0], 
                        'vitaEnable': wbddc_param_list[1],
                    },
                },
              },
            })
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
    
    def _get_configured_wbddc(self, wbddc_index, wbddc_param_list):
        self._set_wbddc_param_list(wbddc_index, wbddc_param_list, atinit=True)
        return CyberRadio.vita_iq_source_mk3(
            vita_type=wbddc_param_list[1],
            payload_size=self.vita_payload_size,
            vita_header_size=self.vita_header_size,
            vita_tail_size=self.vita_tail_size,
            byte_swapped=self.byte_swapped,
            iq_swapped=self.iq_swapped,
            iq_scale_factor=2**-15,
            host=self.udp_host_name,
            port=wbddc_param_list[0],
            ddc_coherent=self.ddcs_coherent,
            num_outputs=self.CyberRadio_NDR_driver_interface_0.getNumTuner() if self.ddcs_coherent else 1,
            tagged=self.tagged,
            debug=False,
        )
    
    def _merge_dicts(self, a, b):
        if not isinstance(b, dict):
            return b
        result = copy.deepcopy(a)
        for k, v in b.items():
            if k in result and isinstance(result[k], dict):
                    result[k] = self._merge_dicts(result[k], v)
            else:
                result[k] = copy.deepcopy(v)
        return result
        
