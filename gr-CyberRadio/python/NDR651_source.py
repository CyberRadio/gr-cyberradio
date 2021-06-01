#!/usr/bin/env python
###############################################################
# \package CyberRadio.NDR651_source
# 
# \brief I/Q data source block using the NDR651 radio
#
# \author DA
# 
# \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.  
#    All rights reserved.
#
###############################################################

from gnuradio import gr, blocks
import CyberRadio
import copy
import CyberRadioDriver
import sys

TUNER_PARAM_ENABLE = 0
TUNER_PARAM_FREQ = 1
TUNER_PARAM_ATTEN = 2
DDC_PARAM_IFACE = 0
DDC_PARAM_STREAM = 1
DDC_PARAM_VITA = 2
DDC_PARAM_RATE = 3
DDC_PARAM_ENABLE = 4 
DDC_PARAM_FREQ = 5 

##
# \class NDR651_source
# \ingroup CyberRadioNDR651
# \brief I/Q data source block using the NDR651 radio.
#
# The NDR651_source block supplies wideband DDC outputs, as indicated 
# by the Number of WBDDCs setting, and narrowband DDC outputs, as indicated 
# by the Number of NBDDCs setting. Any outputs supplied by this block are 
# optional, so the user does not need to connect them if they are not 
# being used.  The NDR651_source block also supplies a character-stream 
# output for collecting logging data from the underlying driver interface.
#
# Tuners, WBDDCs, and NBDDCs are configured via parameter lists.  Parameter
# lists are standard Python lists, formatted as follows:
# \li A tuner parameter list contains the following elements: [tuner 
#    enabled flag, tuner frequency (Hz), tuner attenuation (dB)]. 
# \li A WBDDC parameter list contains the following elements: [10GigE
#    interface to use, UDP port number, VITA type, sample rate index, 
#    enabled flag].
# \li An NBDDC parameter list contains the following elements: [10GigE
#    interface to use, UDP port number, VITA type, sample rate index, 
#    enabled flag, frequency offset (Hz)]. 
# For all DDC parameter lists, the first three items are not changeable.
#
# The NDR651_source block can also produce stream tags for any DDCs 
# configured to use VITA 49 frames.  See the documentation for the base 
# VITA I/Q Source block for details on the stream tags produced.
# 
# \note The parameter list scheme is a workaround to get around the
#    (undocumented) parameter limit that GNU Radio Companion 
#    silently imposes.
# 
class NDR651_source(gr.hier_block2):

    ##
    # \brief Constructs an NDR651_source object.
    #
    # \param verbose_mode Verbose mode for logging.
    # \param radio_host_name Host name for the radio.
    # \param radio_host_port TCP port to use for communicating with the 
    #    radio.
    # \param tengig_iface_list The list of 10GigE interface names used
    #    for the radio.
    # \param num_tuners Number of tuners to use.
    # \param tuner1_param_list Tuner 1 parameter list. 
    # \param tuner2_param_list Tuner 2 parameter list.
    # \param num_wbddcs Number of WBDDCs to use.
    # \param wbddc1_param_list WBDDC 1 parameter list. 
    # \param wbddc2_param_list WBDDC 2 parameter list.
    # \param num_nbddcs Number of NBDDCs to use.
    # \param nbddc1_param_list NBDDC 1 parameter list. 
    # \param nbddc2_param_list NBDDC 2 parameter list. 
    # \param nbddc3_param_list NBDDC 3 parameter list. 
    # \param nbddc4_param_list NBDDC 4 parameter list. 
    # \param nbddc5_param_list NBDDC 5 parameter list. 
    # \param nbddc6_param_list NBDDC 6 parameter list. 
    # \param nbddc7_param_list NBDDC 7 parameter list. 
    # \param nbddc8_param_list NBDDC 8 parameter list. 
    # \param nbddc9_param_list NBDDC 9 parameter list. 
    # \param nbddc10_param_list NBDDC 10 parameter list. 
    # \param nbddc11_param_list NBDDC 11 parameter list. 
    # \param nbddc12_param_list NBDDC 12 parameter list. 
    # \param nbddc13_param_list NBDDC 13 parameter list. 
    # \param nbddc14_param_list NBDDC 14 parameter list. 
    # \param nbddc15_param_list NBDDC 15 parameter list. 
    # \param nbddc16_param_list NBDDC 16 parameter list. 
    # \param tagged Whether the block should produce stream tags.
    # \param debug Whether the block should produce debug output.
    def __init__(self, 
                 verbose_mode=True, 
                 radio_host_name="ndr651", 
                 radio_host_port=8617, 
                 tengig_iface_list=['eth10', 'eth11'], 
                 num_tuners=1,
                 tuner1_param_list=[False, 900e6, 0],
                 tuner2_param_list=[False, 900e6, 0],
                 num_wbddcs=1, 
                 wbddc1_param_list=["eth10", 40001, 0, 0, False],
                 wbddc2_param_list=["eth10", 40002, 0, 0, False],
                 num_nbddcs=1, 
                 nbddc1_param_list=["eth10", 41001, 0, 0, False, 0.0],
                 nbddc2_param_list=["eth10", 41002, 0, 0, False, 0.0],
                 nbddc3_param_list=["eth10", 41003, 0, 0, False, 0.0],
                 nbddc4_param_list=["eth10", 41004, 0, 0, False, 0.0],
                 nbddc5_param_list=["eth10", 41005, 0, 0, False, 0.0],
                 nbddc6_param_list=["eth10", 41006, 0, 0, False, 0.0],
                 nbddc7_param_list=["eth10", 41007, 0, 0, False, 0.0],
                 nbddc8_param_list=["eth10", 41008, 0, 0, False, 0.0],
                 nbddc9_param_list=["eth10", 41009, 0, 0, False, 0.0],
                 nbddc10_param_list=["eth10", 41010, 0, 0, False, 0.0],
                 nbddc11_param_list=["eth10", 41011, 0, 0, False, 0.0],
                 nbddc12_param_list=["eth10", 41012, 0, 0, False, 0.0],
                 nbddc13_param_list=["eth10", 41013, 0, 0, False, 0.0],
                 nbddc14_param_list=["eth10", 41014, 0, 0, False, 0.0],
                 nbddc15_param_list=["eth10", 41015, 0, 0, False, 0.0],
                 nbddc16_param_list=["eth10", 41016, 0, 0, False, 0.0],
                 tagged=False,
                 debug=False,
                 ):
        gr.hier_block2.__init__(
            self, "[CyberRadio] NDR651 Source",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev(num_wbddcs + num_nbddcs + 1, 
                             num_wbddcs + num_nbddcs + 1, 
                             [gr.sizeof_char*1] +
                                num_wbddcs * [gr.sizeof_gr_complex*1] + \
                                num_nbddcs * [gr.sizeof_gr_complex*1]),
        )
        self.logger = gr.logger("CyberRadio")
        self.logger.set_level("INFO")
        self.tuner_param_lists = {}
        self.wbddc_sources = {}
        self.wbddc_param_lists = {}
        self.nbddc_sources = {}
        self.nbddc_param_lists = {}
        self.verbose_mode = verbose_mode
        self.radio_host_name = radio_host_name
        self.radio_host_port = radio_host_port
        self.tengig_iface_list = tengig_iface_list
        self.num_tuners = num_tuners
        self.tuner_param_lists[1] = tuner1_param_list
        self.tuner_param_lists[2] = tuner2_param_list
        self.num_wbddcs = num_wbddcs
        self.wbddc_param_lists[1] = wbddc1_param_list
        self.wbddc_param_lists[2] = wbddc2_param_list
        self.num_nbddcs = num_nbddcs
        self.nbddc_param_lists[1] = nbddc1_param_list
        self.nbddc_param_lists[2] = nbddc2_param_list
        self.nbddc_param_lists[3] = nbddc3_param_list
        self.nbddc_param_lists[4] = nbddc4_param_list
        self.nbddc_param_lists[5] = nbddc5_param_list
        self.nbddc_param_lists[6] = nbddc6_param_list
        self.nbddc_param_lists[7] = nbddc7_param_list
        self.nbddc_param_lists[8] = nbddc8_param_list
        self.nbddc_param_lists[9] = nbddc9_param_list
        self.nbddc_param_lists[10] = nbddc10_param_list
        self.nbddc_param_lists[11] = nbddc11_param_list
        self.nbddc_param_lists[12] = nbddc12_param_list
        self.nbddc_param_lists[13] = nbddc13_param_list
        self.nbddc_param_lists[14] = nbddc14_param_list
        self.nbddc_param_lists[15] = nbddc15_param_list
        self.nbddc_param_lists[16] = nbddc16_param_list
        self.tagged = tagged
        self.debug = debug
        self.CyberRadio_file_like_object_source_0 = CyberRadio.file_like_object_source()
        self.connect((self.CyberRadio_file_like_object_source_0, 0), (self, 0))
        self.CyberRadio_NDR_driver_interface_0 = CyberRadio.NDR_driver_interface(
            radio_type="ndr651",
            verbose=verbose_mode,
            log_file=self.CyberRadio_file_like_object_source_0,
            connect_mode="tcp",
            host_name=radio_host_name,
            host_port=radio_host_port,
        )
        self.vita_tail_size = self.CyberRadio_NDR_driver_interface_0.getVitaTailSize()
        self.vita_payload_size = self.CyberRadio_NDR_driver_interface_0.getVitaPayloadSize()
        self.vita_header_size = self.CyberRadio_NDR_driver_interface_0.getVitaHeaderSize()
        self.iq_swapped = self.CyberRadio_NDR_driver_interface_0.isIqSwapped()
        self.byte_swapped = self.CyberRadio_NDR_driver_interface_0.isByteswapped()
        # tengig_iface_info = Nested dictionary caching info for our 10GigE 
        # interfaces.  Keyed by interface name and datum keyword ("index", 
        # , "destMAC", "sourceIP", or "destIP").
        self.tengig_iface_info = {}
        self._get_tengig_iface_info()
        # UDP destination info needs to be tracked dynamically, since
        # DDCs can be freely assigned to any 10GigE port but there are
        # not enough DIP table entries to hard-code any assignments.
        self.udp_dest_dip_entries = {}
        self.udp_dest_dip_entry_range = self.CyberRadio_NDR_driver_interface_0.getGigEDipEntryIndexRange()
        self._set_udp_dest_info()
        for tuner_index in range(1, self.num_tuners + 1, 1):
            self._set_tuner_param_list(tuner_index, self.tuner_param_lists[tuner_index])
        for wbddc_index in range(1, self.num_wbddcs + 1, 1):
            self.wbddc_sources[wbddc_index] = self._get_configured_wbddc(
                                                    wbddc_index, 
                                                    self.wbddc_param_lists[wbddc_index])
            self.connect((self.wbddc_sources[wbddc_index], 0), (self, wbddc_index))
        for nbddc_index in range(1, self.num_nbddcs + 1, 1):
            self.nbddc_sources[nbddc_index] = self._get_configured_nbddc(
                                                    nbddc_index, 
                                                    self.nbddc_param_lists[nbddc_index])
            self.connect((self.nbddc_sources[nbddc_index], 0), (self, self.num_wbddcs + nbddc_index))


# QT sink close method reimplementation

    ##
    # \brief Gets the verbose mode setting.
    # \return The verbose mode setting.
    def get_verbose_mode(self):
        return self.verbose_mode

    ##
    # \brief Gets the radio host name.
    # \return The radio host name.
    def get_radio_host_name(self):
        return self.radio_host_name

    ##
    # \brief Gets the radio host port.
    # \return The radio host port.
    def get_radio_host_port(self):
        return self.radio_host_port

    ##
    # \brief Gets the 10GigE interface list.
    # \return The 10GigE interface list.
    def get_tengig_iface_list(self):
        return self.tengig_iface_list

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
        return self._get_tuner_param_list(1)

    ##
    # \brief Sets the parameter list for Tuner 1.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner1_param_list(self, param_list):
        self._set_tuner_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for Tuner 2.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner2_param_list(self):
        return self._get_tuner_param_list(2)

    ##
    # \brief Sets the parameter list for Tuner 2.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner2_param_list(self, param_list):
        self._set_tuner_param_list(2, param_list)

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
        return self._get_wbddc_param_list(1)

    ##
    # \brief Sets the parameter list for WBDDC 1.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc1_param_list(self, param_list):
        self._set_wbddc_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 2.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc2_param_list(self):
        return self._get_wbddc_param_list(2)

    ##
    # \brief Sets the parameter list for WBDDC 2.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc2_param_list(self, param_list):
        self._set_wbddc_param_list(2, param_list)

    ##
    # \brief Gets the number of NBDDCs in use.
    # \return The the number of NBDDCs in use.
    def get_num_nbddcs(self):
        return self.num_nbddcs

    ##
    # \brief Gets the parameter list for NBDDC 1.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc1_param_list(self):
        return self._get_nbddc_param_list(1)

    ##
    # \brief Sets the parameter list for NBDDC 1.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc1_param_list(self, param_list):
        self._set_nbddc_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 2.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc2_param_list(self):
        return self._get_nbddc_param_list(2)

    ##
    # \brief Sets the parameter list for NBDDC 2.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc2_param_list(self, param_list):
        self._set_nbddc_param_list(2, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 3.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc3_param_list(self):
        return self._get_nbddc_param_list(3)

    ##
    # \brief Sets the parameter list for NBDDC 3.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc3_param_list(self, param_list):
        self._set_nbddc_param_list(3, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 4.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc4_param_list(self):
        return self._get_nbddc_param_list(4)

    ##
    # \brief Sets the parameter list for NBDDC 4.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc4_param_list(self, param_list):
        self._set_nbddc_param_list(4, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 5.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc5_param_list(self):
        return self._get_nbddc_param_list(5)

    ##
    # \brief Sets the parameter list for NBDDC 5.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc5_param_list(self, param_list):
        self._set_nbddc_param_list(5, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 6.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc6_param_list(self):
        return self._get_nbddc_param_list(6)

    ##
    # \brief Sets the parameter list for NBDDC 6.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc6_param_list(self, param_list):
        self._set_nbddc_param_list(6, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 7.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc7_param_list(self):
        return self._get_nbddc_param_list(7)

    ##
    # \brief Sets the parameter list for NBDDC 7.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc7_param_list(self, param_list):
        self._set_nbddc_param_list(7, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 8.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc8_param_list(self):
        return self._get_nbddc_param_list(8)

    ##
    # \brief Sets the parameter list for NBDDC 8.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc8_param_list(self, param_list):
        self._set_nbddc_param_list(8, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 9.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc9_param_list(self):
        return self._get_nbddc_param_list(9)

    ##
    # \brief Sets the parameter list for NBDDC 9.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc9_param_list(self, param_list):
        self._set_nbddc_param_list(9, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 10.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc10_param_list(self):
        return self._get_nbddc_param_list(10)

    ##
    # \brief Sets the parameter list for NBDDC 10.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc10_param_list(self, param_list):
        self._set_nbddc_param_list(10, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 11.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc11_param_list(self):
        return self._get_nbddc_param_list(11)

    ##
    # \brief Sets the parameter list for NBDDC 11.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc11_param_list(self, param_list):
        self._set_nbddc_param_list(11, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 12.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc12_param_list(self):
        return self._get_nbddc_param_list(12)

    ##
    # \brief Sets the parameter list for NBDDC 12.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc12_param_list(self, param_list):
        self._set_nbddc_param_list(12, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 13.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc13_param_list(self):
        return self._get_nbddc_param_list(13)

    ##
    # \brief Sets the parameter list for NBDDC 13.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc13_param_list(self, param_list):
        self._set_nbddc_param_list(13, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 14.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc14_param_list(self):
        return self._get_nbddc_param_list(14)

    ##
    # \brief Sets the parameter list for NBDDC 14.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc14_param_list(self, param_list):
        self._set_nbddc_param_list(14, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 15.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc15_param_list(self):
        return self._get_nbddc_param_list(15)

    ##
    # \brief Sets the parameter list for NBDDC 15.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc15_param_list(self, param_list):
        self._set_nbddc_param_list(15, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 16.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc16_param_list(self):
        return self._get_nbddc_param_list(16)

    ##
    # \brief Sets the parameter list for NBDDC 16.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc16_param_list(self, param_list):
        self._set_nbddc_param_list(16, param_list)

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
        
    ##
    # \brief Gets the nominal (expected) sample rate for a given NBDDC.
    # \param nbddc_index The NBDDC index.
    # \return The sample rate, in samples per second.
    def get_nbddc_nominal_sample_rate(self, nbddc_index):
        rate_index = self.CyberRadio_NDR_driver_interface_0.getConfiguration()['ddcConfiguration']['narrowband'][nbddc_index]['rateIndex']
        rate_set = self.CyberRadio_NDR_driver_interface_0.getNbddcRateSet()
        return rate_set.get(rate_index, 0)
    
    ##
    # \brief Gets the real-time (measured) sample rate for a given NBDDC.
    # \param nbddc_index The NBDDC index.
    # \return The sample rate, in samples per second.
    def get_nbddc_realtime_sample_rate(self, nbddc_index):
        if nbddc_index in self.nbddc_sources:
            return self.nbddc_sources[nbddc_index].get_realtime_sample_rate()
        else:
            return 0
        
    def _get_tengig_iface_index(self, tengig_iface_to_use):
        tengig_iface_dict = dict(list(zip(self.tengig_iface_list, 
                                     self.CyberRadio_NDR_driver_interface_0.getGigEIndexRange())))
        return tengig_iface_dict.get(tengig_iface_to_use, 0)
    
    def _get_tengig_iface_info(self):
        for zero_index, iface_name in enumerate(self.tengig_iface_list):
            self.tengig_iface_info[iface_name] = {}
            # NDR651 interface indexes are one-based
            self.tengig_iface_info[iface_name]["index"] = zero_index + 1
            # Determine destination MAC and IP addresses from interface name
            self.tengig_iface_info[iface_name]["destMAC"], \
                self.tengig_iface_info[iface_name]["destIP"] = \
                CyberRadioDriver.getInterfaceAddresses(iface_name)
            # Calculate a source IP address from the destination IP address
            srcIpVec = self.tengig_iface_info[iface_name]["destIP"].split(".")
            srcIpVec[-1] = str(int(srcIpVec[-1]) + 100)
            self.tengig_iface_info[iface_name]["sourceIP"] = ".".join(srcIpVec)
        pass
    
    # UDP destination index assignment: 
    # UDP destination info needs to be tracked dynamically, since
    # DDCs can be freely assigned to any 10GigE port but there are
    # not enough DIP table entries to hard-code any assignments.
    
    def _set_udp_dest_info(self):
        configDict = {}
        for iface_name in self.tengig_iface_info:
            configDict = self._merge_dicts(configDict, {
              "ipConfiguration": {
                self.tengig_iface_info[iface_name]["index"]: {
                   "sourceIP": self.tengig_iface_info[iface_name]["sourceIP"],
                   "destIP": {
                       "all": {
                          "ipAddr": "0.0.0.0",
                          "macAddr": "00:00:00:00:00:00",
                          "sourcePort": 0,
                          "destPort": 0,
                       },
                    },
                 },
               },
            })
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
        # Initialize UDP destination DIP entry dictionary
        for iface_name in self.tengig_iface_info:
            self.udp_dest_dip_entries[iface_name] = {}
            for entry_index in self.udp_dest_dip_entry_range:
                self.udp_dest_dip_entries[iface_name][entry_index] = None
            pass
        for wbddc_index in self.wbddc_param_lists:
            self._set_ddc_udp_dest_info("wideband", 
                                        wbddc_index, 
                                        ['', None, None, None, None], 
                                        self.wbddc_param_lists[wbddc_index])
        for nbddc_index in self.nbddc_param_lists:
            self._set_ddc_udp_dest_info("narrowband", 
                                        nbddc_index, 
                                        ['', None, None, None, None, None], 
                                        self.nbddc_param_lists[nbddc_index])
        
    # Gets UDP destination info for a given DDC.
    # -- ddc_type: either "wideband" or "narrowband"
    # -- ddc_index: self-explanatory :)
    # Returns a 2-tuple -- (interface name, DIP table index) -- 
    # if the DDC is found, or None if not.
    def _get_ddc_udp_dest_info(self, ddc_type, ddc_index):
        ret = None
        found = False
        for iface_name in self.udp_dest_dip_entries:
            for entry_index in self.udp_dest_dip_entry_range:
                entry = self.udp_dest_dip_entries[iface_name][entry_index]
                if entry is not None and \
                   entry["ddc_type"] == ddc_type and \
                   entry["ddc_index"] == ddc_index:
                    found = True
                    break
            if found:
                break
        if found:
            ret = (iface_name, entry_index)
        return ret
    
    # Gets an open UDP destination info slot for a given interface.
    # -- iface_name: interface
    # Returns a DIP table index if an open slot is available, or None 
    # if not.
    def _get_open_udp_dest_info(self, iface_name):
        ret = None
        if iface_name in self.udp_dest_dip_entries:
            found = False
            for entry_index in self.udp_dest_dip_entry_range:
                entry = self.udp_dest_dip_entries[iface_name][entry_index]
                if entry is None:
                    found = True
                    break
            if found:
                ret = entry_index
        return ret
    
    # Sets UDP destination info for a given DDC.
    def _set_ddc_udp_dest_info(self, ddc_type, ddc_index, \
                               old_ddc_param_list, new_ddc_param_list):
        #print "SET", ddc_type, str(ddc_index)
        # See if we have an existing entry for this DDC
        udp_dest = self._get_ddc_udp_dest_info(ddc_type, ddc_index)
        #print "-- OLD DEST", udp_dest
        # If an entry already exists
        entry_index = None 
        if udp_dest is not None:
            # See if the interface name changed.  If so, release the
            # entry for the old interface.
            if old_ddc_param_list[DDC_PARAM_IFACE] != \
               new_ddc_param_list[DDC_PARAM_IFACE]:
                #print "-- CLEAR DEST", old_ddc_param_list[DDC_PARAM_IFACE], \
                #      "==>", new_ddc_param_list[DDC_PARAM_IFACE]
                self.udp_dest_dip_entries[udp_dest[0]][udp_dest[1]] = None
                # Create a new entry for the new interface
                entry_index = self._get_open_udp_dest_info(new_ddc_param_list[DDC_PARAM_IFACE])
            # Otherwise, we reuse the existing entry.
            else:
                #print "-- REUSE DEST", udp_dest
                entry_index = udp_dest[1]
            pass
        # Create a new entry if it didn't exist already
        else:
            entry_index = self._get_open_udp_dest_info(new_ddc_param_list[DDC_PARAM_IFACE])
            #print "-- NEW DEST", new_ddc_param_list[DDC_PARAM_IFACE], entry_index
        # Sanity-check the returned entry index.  If it is None, then the new
        # "interface name" is out of bounds and we shouldn't go any further.
        if entry_index is not None:
            self.udp_dest_dip_entries[new_ddc_param_list[DDC_PARAM_IFACE]][entry_index] = \
                          {"ddc_type": ddc_type, "ddc_index": ddc_index}
            #self._dump_udp_dest_info("-- END DUMP", 3)
            # Reconfigure the DIP tables
            configDict = {
              "ipConfiguration": {
                self.tengig_iface_info[new_ddc_param_list[DDC_PARAM_IFACE]]["index"]: {
                   "destIP": {
                       entry_index: {
                          "ipAddr": self.tengig_iface_info[new_ddc_param_list[DDC_PARAM_IFACE]]["destIP"],
                          "macAddr": self.tengig_iface_info[new_ddc_param_list[DDC_PARAM_IFACE]]["destMAC"],
                          "sourcePort": new_ddc_param_list[DDC_PARAM_STREAM],
                          "destPort": new_ddc_param_list[DDC_PARAM_STREAM],
                       },
                   },
                },
              },
              "ddcConfiguration": {
                ddc_type: {
                    ddc_index: {
                        'streamId': new_ddc_param_list[DDC_PARAM_STREAM], 
                        'dataPort': self.tengig_iface_info[new_ddc_param_list[DDC_PARAM_IFACE]]["index"],
                        'udpDest': entry_index,
                    },
                },
              },
            }
            self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
    
    def _get_tuner_param_list(self, tuner_index):
        return self.tuner_param_lists.get(tuner_index, [False, 900e6, 0])
    
    def _set_tuner_param_list(self, tuner_index, tuner_param_list):
        self.tuner_param_lists[tuner_index] = tuner_param_list
        configDict = {
          "tunerConfiguration": {
                tuner_index: {
                    'enable': 1 if tuner_param_list[TUNER_PARAM_ENABLE] else 0,
                    'frequency': tuner_param_list[TUNER_PARAM_FREQ],
                    'attenuation': tuner_param_list[TUNER_PARAM_ATTEN],
                },
          },
        }
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
    
    def _get_wbddc_param_list(self, wbddc_index):
        return self.wbddc_param_lists.get(wbddc_index, \
                                          ["", 40001, 0, 0, False])
    
    def _set_wbddc_param_list(self, wbddc_index, wbddc_param_list, atinit=False):
#         self._set_ddc_udp_dest_info("wideband", wbddc_index, 
#                                     self.wbddc_param_lists[wbddc_index], 
#                                     wbddc_param_list)
        self.wbddc_param_lists[wbddc_index] = wbddc_param_list
        configDict = {
          "ddcConfiguration": {
            "wideband": {
                wbddc_index: {
                    'rateIndex': wbddc_param_list[DDC_PARAM_RATE],
                    'enable': 1 if wbddc_param_list[DDC_PARAM_ENABLE] else 0,
                    'vitaEnable': wbddc_param_list[DDC_PARAM_VITA],
                },
            },
          },
        }
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
    
    def _get_nbddc_param_list(self, nbddc_index):
        return self.nbddc_param_lists.get(nbddc_index, \
                                          ["", 40001, 0, 0, False, 0])
    
    def _set_nbddc_param_list(self, nbddc_index, nbddc_param_list, atinit=False):
#         self._set_ddc_udp_dest_info("narrowband", nbddc_index, 
#                                     self.nbddc_param_lists[nbddc_index], 
#                                     nbddc_param_list)
        self.nbddc_param_lists[nbddc_index] = nbddc_param_list
        configDict = {
          "ddcConfiguration": {
            "narrowband": {
                nbddc_index: {
                    'rateIndex': nbddc_param_list[DDC_PARAM_RATE],
                    'enable': 1 if nbddc_param_list[DDC_PARAM_ENABLE] else 0,
                    'vitaEnable': nbddc_param_list[DDC_PARAM_VITA],
                    'frequency': nbddc_param_list[DDC_PARAM_FREQ],
                },
            },
          },
        }
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
    
    def _get_configured_wbddc(self, wbddc_index, wbddc_param_list):
        self._set_wbddc_param_list(wbddc_index, wbddc_param_list, atinit=True)
        if wbddc_param_list[DDC_PARAM_IFACE] in self.tengig_iface_info:
            return CyberRadio.vita_iq_source_mk3(
                vita_type=wbddc_param_list[DDC_PARAM_VITA],
                payload_size=self.vita_payload_size,
                vita_header_size=self.vita_header_size,
                vita_tail_size=self.vita_tail_size,
                byte_swapped=self.byte_swapped,
                iq_swapped=self.iq_swapped,
                iq_scale_factor=2**-15,
                host=self.tengig_iface_info[wbddc_param_list[DDC_PARAM_IFACE]]["destIP"],
                port=wbddc_param_list[DDC_PARAM_STREAM],
                ddc_coherent=False,
                num_outputs=1,
                tagged=self.tagged,
                debug=self.debug,
            )
        else:
            self.logger.error("WBDDC %d: Interface \"%s\" not found in interface list.  DDC not configured." % (wbddc_index, str(wbddc_param_list[DDC_PARAM_IFACE])))
            return blocks.null_source(gr.sizeof_gr_complex * 1)
    
    def _get_configured_nbddc(self, nbddc_index, nbddc_param_list):
        self._set_nbddc_param_list(nbddc_index, nbddc_param_list, atinit=True)
        if nbddc_param_list[DDC_PARAM_IFACE] in self.tengig_iface_info:
            return CyberRadio.vita_iq_source(
                vita_type=nbddc_param_list[DDC_PARAM_VITA],
                payload_size=self.vita_payload_size,
                vita_header_size=self.vita_header_size,
                vita_tail_size=self.vita_tail_size,
                byte_swapped=self.byte_swapped,
                iq_swapped=self.iq_swapped,
                iq_scale_factor=2**-15,
                host=self.tengig_iface_info[nbddc_param_list[DDC_PARAM_IFACE]]["destIP"],
                port=nbddc_param_list[DDC_PARAM_STREAM],
                ddc_coherent=False,
                num_outputs=1,
                tagged=self.tagged,
                debug=self.debug,
            )
        else:
            self.logger.error("NBDDC %d: Interface \"%s\" not found in interface list.  DDC not configured." % (nbddc_index, str(nbddc_param_list[DDC_PARAM_IFACE])))
            return blocks.null_source(gr.sizeof_gr_complex * 1)
    
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

