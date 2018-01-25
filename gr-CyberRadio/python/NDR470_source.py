#!/usr/bin/env python
###############################################################
# \package CyberRadio.NDR470_source
# 
# \brief I/Q data source block using the NDR470 radio
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
# \class NDR470_source
# \ingroup CyberRadioNDR470
# \brief I/Q data source block using the NDR470 radio.
#
# The NDR470_source block supplies wideband DDC outputs, as indicated 
# by the Number of WBDDCs setting, and narrowband DDC outputs, as indicated 
# by the Number of NBDDCs setting. Any outputs supplied by this block are
# optional, so the user does not need to connect them if they are not
# being used.  The NDR470_source block also supplies a character-stream
# output for collecting logging data from the underlying driver interface.
# 
# Tuners, WBDDCs, and NBDDCs are configured via parameter lists.  Parameter
# lists are standard Python lists, formatted as follows:
# \li A tuner parameter list contains the following elements: [tuner 
#    enabled flag, tuner frequency (Hz), tuner attenuation (dB)]. 
# \li A WBDDC parameter list contains the following elements: [UDP 
#    port number, VITA type, sample rate index, enabled flag, 
#    DDC frequency offset (Hz)]. 
# \li An NBDDC parameter list contains the following elements: [UDP 
#    port number, VITA type, tuner index, sample rate index, enabled flag, 
#    frequency offset (Hz)]. 
# 
# The NDR470_source block can also produce stream tags for any DDCs 
# configured to use VITA 49 frames.  See the documentation for the base 
# VITA I/Q Source block for details on the stream tags produced.
# 
# \note The parameter list scheme is a workaround to get around the
#    (undocumented) parameter limit that GNU Radio Companion 
#    silently imposes.
# 
class NDR470_source(gr.hier_block2):

    ##
    # \brief Constructs an NDR470_source object.
    #
    # \param verbose_mode Verbose mode for logging.
    # \param radio_device_name System device name for the radio.
    # \param radio_baud_rate Radio baud rate.
    # \param gig_iface_to_use The name of the Gigabit Ethernet interface 
    #    used by the radio.
    # \param num_tuners Number of tuners to use.
    # \param tuner1_param_list Tuner 1 parameter list. 
    # \param tuner2_param_list Tuner 2 parameter list.
    # \param tuner3_param_list Tuner 3 parameter list. 
    # \param tuner4_param_list Tuner 4 parameter list. 
    # \param num_wbddcs Number of WBDDCs to use.
    # \param wbddc1_param_list WBDDC 1 parameter list. 
    # \param wbddc2_param_list WBDDC 2 parameter list.
    # \param wbddc3_param_list WBDDC 3 parameter list. 
    # \param wbddc4_param_list WBDDC 4 parameter list. 
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
    # \param nbddc17_param_list NBDDC 17 parameter list. 
    # \param nbddc18_param_list NBDDC 18 parameter list. 
    # \param nbddc19_param_list NBDDC 19 parameter list. 
    # \param nbddc20_param_list NBDDC 20 parameter list. 
    # \param nbddc21_param_list NBDDC 21 parameter list. 
    # \param nbddc22_param_list NBDDC 22 parameter list. 
    # \param nbddc23_param_list NBDDC 23 parameter list. 
    # \param nbddc24_param_list NBDDC 24 parameter list. 
    # \param nbddc25_param_list NBDDC 25 parameter list. 
    # \param nbddc26_param_list NBDDC 26 parameter list. 
    # \param nbddc27_param_list NBDDC 27 parameter list. 
    # \param nbddc28_param_list NBDDC 28 parameter list. 
    # \param nbddc29_param_list NBDDC 29 parameter list. 
    # \param nbddc30_param_list NBDDC 30 parameter list. 
    # \param nbddc31_param_list NBDDC 31 parameter list. 
    # \param nbddc32_param_list NBDDC 32 parameter list. 
    # \param tagged Whether the block should produce stream tags.
    def __init__(self, 
                 verbose_mode=True, 
                 radio_device_name="/dev/ndr47x", 
                 radio_baud_rate=921600, 
                 gig_iface_to_use="eth0",
                 num_tuners=1,
                 tuner1_param_list=[False, 900e6, 0],
                 tuner2_param_list=[False, 900e6, 0],
                 tuner3_param_list=[False, 900e6, 0],
                 tuner4_param_list=[False, 900e6, 0],
                 num_wbddcs=1,
                 wbddc1_param_list=[40001, 0, 0, False, 0e6],
                 wbddc2_param_list=[40002, 0, 0, False, 0e6],
                 wbddc3_param_list=[40003, 0, 0, False, 0e6],
                 wbddc4_param_list=[40004, 0, 0, False, 0e6],
                 num_nbddcs=1, 
                 nbddc1_param_list=[41001, 0, 1, 0, False, 0.0],
                 nbddc2_param_list=[41002, 0, 1, 0, False, 0.0],
                 nbddc3_param_list=[41003, 0, 1, 0, False, 0.0],
                 nbddc4_param_list=[41004, 0, 1, 0, False, 0.0],
                 nbddc5_param_list=[41005, 0, 1, 0, False, 0.0],
                 nbddc6_param_list=[41006, 0, 1, 0, False, 0.0],
                 nbddc7_param_list=[41007, 0, 1, 0, False, 0.0],
                 nbddc8_param_list=[41008, 0, 1, 0, False, 0.0],
                 nbddc9_param_list=[41009, 0, 1, 0, False, 0.0],
                 nbddc10_param_list=[41010, 0, 1, 0, False, 0.0],
                 nbddc11_param_list=[41011, 0, 1, 0, False, 0.0],
                 nbddc12_param_list=[41012, 0, 1, 0, False, 0.0],
                 nbddc13_param_list=[41013, 0, 1, 0, False, 0.0],
                 nbddc14_param_list=[41014, 0, 1, 0, False, 0.0],
                 nbddc15_param_list=[41015, 0, 1, 0, False, 0.0],
                 nbddc16_param_list=[41016, 0, 1, 0, False, 0.0],
                 nbddc17_param_list=[41017, 0, 1, 0, False, 0.0],
                 nbddc18_param_list=[41018, 0, 1, 0, False, 0.0],
                 nbddc19_param_list=[41019, 0, 1, 0, False, 0.0],
                 nbddc20_param_list=[41020, 0, 1, 0, False, 0.0],
                 nbddc21_param_list=[41021, 0, 1, 0, False, 0.0],
                 nbddc22_param_list=[41022, 0, 1, 0, False, 0.0],
                 nbddc23_param_list=[41023, 0, 1, 0, False, 0.0],
                 nbddc24_param_list=[41024, 0, 1, 0, False, 0.0],
                 nbddc25_param_list=[41025, 0, 1, 0, False, 0.0],
                 nbddc26_param_list=[41026, 0, 1, 0, False, 0.0],
                 nbddc27_param_list=[41027, 0, 1, 0, False, 0.0],
                 nbddc28_param_list=[41028, 0, 1, 0, False, 0.0],
                 nbddc29_param_list=[41029, 0, 1, 0, False, 0.0],
                 nbddc30_param_list=[41030, 0, 1, 0, False, 0.0],
                 nbddc31_param_list=[41031, 0, 1, 0, False, 0.0],
                 nbddc32_param_list=[41032, 0, 1, 0, False, 0.0],
                 tagged=False,
                 ):
        gr.hier_block2.__init__(
            self, "[CyberRadio] NDR470 Source",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev(num_wbddcs + num_nbddcs + 1, 
                             num_wbddcs + num_nbddcs + 1, 
                             [gr.sizeof_char*1] +
                             num_wbddcs * [gr.sizeof_gr_complex*1] + 
                             num_nbddcs * [gr.sizeof_gr_complex*1]), 
        )
        self.verbose_mode = verbose_mode
        self.radio_device_name = radio_device_name
        self.radio_baud_rate = radio_baud_rate
        self.gig_iface_to_use = gig_iface_to_use
        self.udp_host_name = CyberRadioDriver.getInterfaceAddresses(self.gig_iface_to_use)[1]
        self.num_tuners = num_tuners
        self.tuner1_param_list = tuner1_param_list
        self.tuner2_param_list = tuner2_param_list
        self.tuner3_param_list = tuner3_param_list
        self.tuner4_param_list = tuner4_param_list
        self.num_wbddcs = num_wbddcs
        self.wbddc1_param_list = wbddc1_param_list
        self.wbddc2_param_list = wbddc2_param_list
        self.wbddc3_param_list = wbddc3_param_list
        self.wbddc4_param_list = wbddc4_param_list
        self.num_nbddcs = num_nbddcs
        self.nbddc1_param_list = nbddc1_param_list
        self.nbddc2_param_list = nbddc2_param_list
        self.nbddc3_param_list = nbddc3_param_list
        self.nbddc4_param_list = nbddc4_param_list
        self.nbddc5_param_list = nbddc5_param_list
        self.nbddc6_param_list = nbddc6_param_list
        self.nbddc7_param_list = nbddc7_param_list
        self.nbddc8_param_list = nbddc8_param_list
        self.nbddc9_param_list = nbddc9_param_list
        self.nbddc10_param_list = nbddc10_param_list
        self.nbddc11_param_list = nbddc11_param_list
        self.nbddc12_param_list = nbddc12_param_list
        self.nbddc13_param_list = nbddc13_param_list
        self.nbddc14_param_list = nbddc14_param_list
        self.nbddc15_param_list = nbddc15_param_list
        self.nbddc16_param_list = nbddc16_param_list
        self.nbddc17_param_list = nbddc17_param_list
        self.nbddc18_param_list = nbddc18_param_list
        self.nbddc19_param_list = nbddc19_param_list
        self.nbddc20_param_list = nbddc20_param_list
        self.nbddc21_param_list = nbddc21_param_list
        self.nbddc22_param_list = nbddc22_param_list
        self.nbddc23_param_list = nbddc23_param_list
        self.nbddc24_param_list = nbddc24_param_list
        self.nbddc25_param_list = nbddc25_param_list
        self.nbddc26_param_list = nbddc26_param_list
        self.nbddc27_param_list = nbddc27_param_list
        self.nbddc28_param_list = nbddc28_param_list
        self.nbddc29_param_list = nbddc29_param_list
        self.nbddc30_param_list = nbddc30_param_list
        self.nbddc31_param_list = nbddc31_param_list
        self.nbddc32_param_list = nbddc32_param_list
        self.tagged = tagged
        self.CyberRadio_file_like_object_source_0 = CyberRadio.file_like_object_source()
        self.connect((self.CyberRadio_file_like_object_source_0, 0), (self, 0))
        self.CyberRadio_NDR_driver_interface_0 = CyberRadio.NDR_driver_interface(
            radio_type="ndr470",
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
        self._set_udp_dest_info()
        if self.num_tuners >= 1:
            self._set_tuner_param_list(1, tuner1_param_list)
        if self.num_tuners >= 2:
            self._set_tuner_param_list(2, tuner2_param_list)
        if self.num_tuners >= 3:
            self._set_tuner_param_list(3, tuner3_param_list)
        if self.num_tuners >= 4:
            self._set_tuner_param_list(4, tuner4_param_list)
        self.wbddc_sources = {}
        if self.num_wbddcs >= 1:
            self.CyberRadio_vita_iq_source_wbddc_1 = self._get_configured_wbddc(1, wbddc1_param_list)
            self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 0), (self, 1))
            self.wbddc_sources[1] = self.CyberRadio_vita_iq_source_wbddc_1
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
        self.nbddc_sources = {}
        if self.num_nbddcs >= 1:
            self.CyberRadio_vita_iq_source_nbddc_1 = self._get_configured_nbddc(1, nbddc1_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_1, 0), (self, self.num_wbddcs + 1))
            self.nbddc_sources[1] = self.CyberRadio_vita_iq_source_nbddc_1
        if self.num_nbddcs >= 2:
            self.CyberRadio_vita_iq_source_nbddc_2 = self._get_configured_nbddc(2, nbddc2_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_2, 0), (self, self.num_wbddcs + 2))
            self.nbddc_sources[2] = self.CyberRadio_vita_iq_source_nbddc_2
        if self.num_nbddcs >= 3:
            self.CyberRadio_vita_iq_source_nbddc_3 = self._get_configured_nbddc(3, nbddc3_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_3, 0), (self, self.num_wbddcs + 3))
            self.nbddc_sources[3] = self.CyberRadio_vita_iq_source_nbddc_3
        if self.num_nbddcs >= 4:
            self.CyberRadio_vita_iq_source_nbddc_4 = self._get_configured_nbddc(4, nbddc4_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_4, 0), (self, self.num_wbddcs + 4))
            self.nbddc_sources[4] = self.CyberRadio_vita_iq_source_nbddc_4
        if self.num_nbddcs >= 5:
            self.CyberRadio_vita_iq_source_nbddc_5 = self._get_configured_nbddc(5, nbddc5_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_5, 0), (self, self.num_wbddcs + 5))
            self.nbddc_sources[5] = self.CyberRadio_vita_iq_source_nbddc_5
        if self.num_nbddcs >= 6:
            self.CyberRadio_vita_iq_source_nbddc_6 = self._get_configured_nbddc(6, nbddc6_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_6, 0), (self, self.num_wbddcs + 6))
            self.nbddc_sources[6] = self.CyberRadio_vita_iq_source_nbddc_6
        if self.num_nbddcs >= 7:
            self.CyberRadio_vita_iq_source_nbddc_6 = self._get_configured_nbddc(7, nbddc7_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_6, 0), (self, self.num_wbddcs + 6))
            self.nbddc_sources[7] = self.CyberRadio_vita_iq_source_nbddc_6
        if self.num_nbddcs >= 8:
            self.CyberRadio_vita_iq_source_nbddc_8 = self._get_configured_nbddc(8, nbddc8_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_8, 0), (self, self.num_wbddcs + 8))
            self.nbddc_sources[8] = self.CyberRadio_vita_iq_source_nbddc_8
        if self.num_nbddcs >= 9:
            self.CyberRadio_vita_iq_source_nbddc_9 = self._get_configured_nbddc(9, nbddc9_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_9, 0), (self, self.num_wbddcs + 9))
            self.nbddc_sources[9] = self.CyberRadio_vita_iq_source_nbddc_9
        if self.num_nbddcs >= 10:
            self.CyberRadio_vita_iq_source_nbddc_10 = self._get_configured_nbddc(10, nbddc10_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_10, 0), (self, self.num_wbddcs + 10))
            self.nbddc_sources[10] = self.CyberRadio_vita_iq_source_nbddc_10
        if self.num_nbddcs >= 11:
            self.CyberRadio_vita_iq_source_nbddc_11 = self._get_configured_nbddc(11, nbddc11_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_11, 0), (self, self.num_wbddcs + 11))
            self.nbddc_sources[11] = self.CyberRadio_vita_iq_source_nbddc_11
        if self.num_nbddcs >= 12:
            self.CyberRadio_vita_iq_source_nbddc_12 = self._get_configured_nbddc(12, nbddc12_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_12, 0), (self, self.num_wbddcs + 12))
            self.nbddc_sources[12] = self.CyberRadio_vita_iq_source_nbddc_12
        if self.num_nbddcs >= 13:
            self.CyberRadio_vita_iq_source_nbddc_13 = self._get_configured_nbddc(13, nbddc13_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_13, 0), (self, self.num_wbddcs + 13))
            self.nbddc_sources[13] = self.CyberRadio_vita_iq_source_nbddc_13
        if self.num_nbddcs >= 14:
            self.CyberRadio_vita_iq_source_nbddc_14 = self._get_configured_nbddc(14, nbddc14_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_14, 0), (self, self.num_wbddcs + 14))
            self.nbddc_sources[14] = self.CyberRadio_vita_iq_source_nbddc_14
        if self.num_nbddcs >= 15:
            self.CyberRadio_vita_iq_source_nbddc_15 = self._get_configured_nbddc(15, nbddc15_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_15, 0), (self, self.num_wbddcs + 15))
            self.nbddc_sources[15] = self.CyberRadio_vita_iq_source_nbddc_15
        if self.num_nbddcs >= 16:
            self.CyberRadio_vita_iq_source_nbddc_16 = self._get_configured_nbddc(16, nbddc16_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_16, 0), (self, self.num_wbddcs + 16))
            self.nbddc_sources[16] = self.CyberRadio_vita_iq_source_nbddc_16
        if self.num_nbddcs >= 17:
            self.CyberRadio_vita_iq_source_nbddc_17 = self._get_configured_nbddc(17, nbddc17_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_17, 0), (self, self.num_wbddcs + 17))
            self.nbddc_sources[17] = self.CyberRadio_vita_iq_source_nbddc_17
        if self.num_nbddcs >= 18:
            self.CyberRadio_vita_iq_source_nbddc_18 = self._get_configured_nbddc(18, nbddc18_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_18, 0), (self, self.num_wbddcs + 18))
            self.nbddc_sources[18] = self.CyberRadio_vita_iq_source_nbddc_18
        if self.num_nbddcs >= 19:
            self.CyberRadio_vita_iq_source_nbddc_19 = self._get_configured_nbddc(19, nbddc19_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_19, 0), (self, self.num_wbddcs + 19))
            self.nbddc_sources[19] = self.CyberRadio_vita_iq_source_nbddc_19
        if self.num_nbddcs >= 20:
            self.CyberRadio_vita_iq_source_nbddc_20 = self._get_configured_nbddc(20, nbddc20_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_20, 0), (self, self.num_wbddcs + 20))
            self.nbddc_sources[20] = self.CyberRadio_vita_iq_source_nbddc_20
        if self.num_nbddcs >= 21:
            self.CyberRadio_vita_iq_source_nbddc_21 = self._get_configured_nbddc(21, nbddc21_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_21, 0), (self, self.num_wbddcs + 21))
            self.nbddc_sources[21] = self.CyberRadio_vita_iq_source_nbddc_21
        if self.num_nbddcs >= 22:
            self.CyberRadio_vita_iq_source_nbddc_22 = self._get_configured_nbddc(22, nbddc22_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_22, 0), (self, self.num_wbddcs + 22))
            self.nbddc_sources[22] = self.CyberRadio_vita_iq_source_nbddc_22
        if self.num_nbddcs >= 23:
            self.CyberRadio_vita_iq_source_nbddc_23 = self._get_configured_nbddc(23, nbddc23_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_23, 0), (self, self.num_wbddcs + 23))
            self.nbddc_sources[23] = self.CyberRadio_vita_iq_source_nbddc_23
        if self.num_nbddcs >= 24:
            self.CyberRadio_vita_iq_source_nbddc_24 = self._get_configured_nbddc(24, nbddc24_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_24, 0), (self, self.num_wbddcs + 24))
            self.nbddc_sources[24] = self.CyberRadio_vita_iq_source_nbddc_24
        if self.num_nbddcs >= 25:
            self.CyberRadio_vita_iq_source_nbddc_25 = self._get_configured_nbddc(25, nbddc25_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_25, 0), (self, self.num_wbddcs + 25))
            self.nbddc_sources[25] = self.CyberRadio_vita_iq_source_nbddc_25
        if self.num_nbddcs >= 26:
            self.CyberRadio_vita_iq_source_nbddc_26 = self._get_configured_nbddc(26, nbddc26_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_26, 0), (self, self.num_wbddcs + 26))
            self.nbddc_sources[26] = self.CyberRadio_vita_iq_source_nbddc_26
        if self.num_nbddcs >= 27:
            self.CyberRadio_vita_iq_source_nbddc_27 = self._get_configured_nbddc(27, nbddc27_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_27, 0), (self, self.num_wbddcs + 27))
            self.nbddc_sources[27] = self.CyberRadio_vita_iq_source_nbddc_27
        if self.num_nbddcs >= 28:
            self.CyberRadio_vita_iq_source_nbddc_28 = self._get_configured_nbddc(28, nbddc28_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_28, 0), (self, self.num_wbddcs + 28))
            self.nbddc_sources[28] = self.CyberRadio_vita_iq_source_nbddc_28
        if self.num_nbddcs >= 29:
            self.CyberRadio_vita_iq_source_nbddc_29 = self._get_configured_nbddc(29, nbddc29_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_29, 0), (self, self.num_wbddcs + 29))
            self.nbddc_sources[29] = self.CyberRadio_vita_iq_source_nbddc_29
        if self.num_nbddcs >= 30:
            self.CyberRadio_vita_iq_source_nbddc_30 = self._get_configured_nbddc(30, nbddc30_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_30, 0), (self, self.num_wbddcs + 30))
            self.nbddc_sources[30] = self.CyberRadio_vita_iq_source_nbddc_30
        if self.num_nbddcs >= 31:
            self.CyberRadio_vita_iq_source_nbddc_31 = self._get_configured_nbddc(31, nbddc31_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_31, 0), (self, self.num_wbddcs + 31))
            self.nbddc_sources[31] = self.CyberRadio_vita_iq_source_nbddc_31
        if self.num_nbddcs >= 32:
            self.CyberRadio_vita_iq_source_nbddc_32 = self._get_configured_nbddc(32, nbddc32_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_32, 0), (self, self.num_wbddcs + 32))
            self.nbddc_sources[32] = self.CyberRadio_vita_iq_source_nbddc_32


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
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner2_param_list(self):
        return self.tuner2_param_list

    ##
    # \brief Sets the parameter list for Tuner 2.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner2_param_list(self, param_list):
        self.tuner2_param_list = param_list
        self._set_tuner_param_list(2, param_list)

    ##
    # \brief Gets the parameter list for Tuner 3.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner3_param_list(self):
        return self.tuner3_param_list

    ##
    # \brief Sets the parameter list for Tuner 3.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner3_param_list(self, param_list):
        self.tuner3_param_list = param_list
        self._set_tuner_param_list(3, param_list)

    ##
    # \brief Gets the parameter list for Tuner 4.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner4_param_list(self):
        return self.tuner4_param_list

    ##
    # \brief Sets the parameter list for Tuner 4.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner4_param_list(self, param_list):
        self.tuner4_param_list = param_list
        self._set_tuner_param_list(4, param_list)

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
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc2_param_list(self):
        return self.wbddc2_param_list

    ##
    # \brief Sets the parameter list for WBDDC 2.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc2_param_list(self, param_list):
        self.wbddc2_param_list = param_list
        self._set_wbddc_param_list(2, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 3.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc3_param_list(self):
        return self.wbddc3_param_list

    ##
    # \brief Sets the parameter list for WBDDC 3.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc3_param_list(self, param_list):
        self.wbddc3_param_list = param_list
        self._set_wbddc_param_list(3, param_list)

    ##
    # \brief Gets the parameter list for WBDDC 4.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc4_param_list(self):
        return self.wbddc4_param_list

    ##
    # \brief Sets the parameter list for WBDDC 4.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc4_param_list(self, param_list):
        self.wbddc4_param_list = param_list
        self._set_wbddc_param_list(4, param_list)

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
        return self.nbddc1_param_list

    ##
    # \brief Sets the parameter list for NBDDC 1.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc1_param_list(self, param_list):
        self.nbddc1_param_list = param_list
        self._set_nbddc_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 2.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc2_param_list(self):
        return self.nbddc2_param_list

    ##
    # \brief Sets the parameter list for NBDDC 2.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc2_param_list(self, param_list):
        self.nbddc2_param_list = param_list
        self._set_nbddc_param_list(2, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 3.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc3_param_list(self):
        return self.nbddc3_param_list

    ##
    # \brief Sets the parameter list for NBDDC 3.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc3_param_list(self, param_list):
        self.nbddc3_param_list = param_list
        self._set_nbddc_param_list(3, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 4.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc4_param_list(self):
        return self.nbddc4_param_list

    ##
    # \brief Sets the parameter list for NBDDC 4.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc4_param_list(self, param_list):
        self.nbddc4_param_list = param_list
        self._set_nbddc_param_list(4, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 5.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc5_param_list(self):
        return self.nbddc5_param_list

    ##
    # \brief Sets the parameter list for NBDDC 5.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc5_param_list(self, param_list):
        self.nbddc5_param_list = param_list
        self._set_nbddc_param_list(5, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 6.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc6_param_list(self):
        return self.nbddc6_param_list

    ##
    # \brief Sets the parameter list for NBDDC 6.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc6_param_list(self, param_list):
        self.nbddc6_param_list = param_list
        self._set_nbddc_param_list(6, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 7.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc7_param_list(self):
        return self.nbddc7_param_list

    ##
    # \brief Sets the parameter list for NBDDC 7.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc7_param_list(self, param_list):
        self.nbddc7_param_list = param_list
        self._set_nbddc_param_list(7, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 8.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc8_param_list(self):
        return self.nbddc8_param_list

    ##
    # \brief Sets the parameter list for NBDDC 8.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc8_param_list(self, param_list):
        self.nbddc8_param_list = param_list
        self._set_nbddc_param_list(8, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 9.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc9_param_list(self):
        return self.nbddc9_param_list

    ##
    # \brief Sets the parameter list for NBDDC 9.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc9_param_list(self, param_list):
        self.nbddc9_param_list = param_list
        self._set_nbddc_param_list(9, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 10.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc10_param_list(self):
        return self.nbddc10_param_list

    ##
    # \brief Sets the parameter list for NBDDC 10.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc10_param_list(self, param_list):
        self.nbddc10_param_list = param_list
        self._set_nbddc_param_list(10, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 11.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc11_param_list(self):
        return self.nbddc11_param_list

    ##
    # \brief Sets the parameter list for NBDDC 11.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc11_param_list(self, param_list):
        self.nbddc11_param_list = param_list
        self._set_nbddc_param_list(11, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 12.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc12_param_list(self):
        return self.nbddc12_param_list

    ##
    # \brief Sets the parameter list for NBDDC 12.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc12_param_list(self, param_list):
        self.nbddc12_param_list = param_list
        self._set_nbddc_param_list(12, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 13.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc13_param_list(self):
        return self.nbddc13_param_list

    ##
    # \brief Sets the parameter list for NBDDC 13.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc13_param_list(self, param_list):
        self.nbddc13_param_list = param_list
        self._set_nbddc_param_list(13, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 14.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc14_param_list(self):
        return self.nbddc14_param_list

    ##
    # \brief Sets the parameter list for NBDDC 14.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc14_param_list(self, param_list):
        self.nbddc14_param_list = param_list
        self._set_nbddc_param_list(14, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 15.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc15_param_list(self):
        return self.nbddc15_param_list

    ##
    # \brief Sets the parameter list for NBDDC 15.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc15_param_list(self, param_list):
        self.nbddc15_param_list = param_list
        self._set_nbddc_param_list(15, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 16.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc16_param_list(self):
        return self.nbddc16_param_list

    ##
    # \brief Sets the parameter list for NBDDC 16.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc16_param_list(self, param_list):
        self.nbddc16_param_list = param_list
        self._set_nbddc_param_list(16, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 17.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc17_param_list(self):
        return self.nbddc17_param_list

    ##
    # \brief Sets the parameter list for NBDDC 17.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc17_param_list(self, param_list):
        self.nbddc17_param_list = param_list
        self._set_nbddc_param_list(17, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 18.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc18_param_list(self):
        return self.nbddc18_param_list

    ##
    # \brief Sets the parameter list for NBDDC 18.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc18_param_list(self, param_list):
        self.nbddc18_param_list = param_list
        self._set_nbddc_param_list(18, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 19.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc19_param_list(self):
        return self.nbddc19_param_list

    ##
    # \brief Sets the parameter list for NBDDC 19.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc19_param_list(self, param_list):
        self.nbddc19_param_list = param_list
        self._set_nbddc_param_list(19, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 20.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc20_param_list(self):
        return self.nbddc20_param_list

    ##
    # \brief Sets the parameter list for NBDDC 20.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc20_param_list(self, param_list):
        self.nbddc20_param_list = param_list
        self._set_nbddc_param_list(20, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 21.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc21_param_list(self):
        return self.nbddc21_param_list

    ##
    # \brief Sets the parameter list for NBDDC 21.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc21_param_list(self, param_list):
        self.nbddc21_param_list = param_list
        self._set_nbddc_param_list(21, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 22.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc22_param_list(self):
        return self.nbddc22_param_list

    ##
    # \brief Sets the parameter list for NBDDC 22.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc22_param_list(self, param_list):
        self.nbddc22_param_list = param_list
        self._set_nbddc_param_list(22, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 23.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc23_param_list(self):
        return self.nbddc23_param_list

    ##
    # \brief Sets the parameter list for NBDDC 23.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc23_param_list(self, param_list):
        self.nbddc23_param_list = param_list
        self._set_nbddc_param_list(23, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 24.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc24_param_list(self):
        return self.nbddc24_param_list

    ##
    # \brief Sets the parameter list for NBDDC 24.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc24_param_list(self, param_list):
        self.nbddc24_param_list = param_list
        self._set_nbddc_param_list(24, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 25.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc25_param_list(self):
        return self.nbddc25_param_list

    ##
    # \brief Sets the parameter list for NBDDC 25.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc25_param_list(self, param_list):
        self.nbddc25_param_list = param_list
        self._set_nbddc_param_list(25, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 26.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc26_param_list(self):
        return self.nbddc26_param_list

    ##
    # \brief Sets the parameter list for NBDDC 26.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc26_param_list(self, param_list):
        self.nbddc26_param_list = param_list
        self._set_nbddc_param_list(26, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 27.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc27_param_list(self):
        return self.nbddc27_param_list

    ##
    # \brief Sets the parameter list for NBDDC 27.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc27_param_list(self, param_list):
        self.nbddc27_param_list = param_list
        self._set_nbddc_param_list(27, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 28.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc28_param_list(self):
        return self.nbddc28_param_list

    ##
    # \brief Sets the parameter list for NBDDC 28.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc28_param_list(self, param_list):
        self.nbddc28_param_list = param_list
        self._set_nbddc_param_list(28, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 29.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc29_param_list(self):
        return self.nbddc29_param_list

    ##
    # \brief Sets the parameter list for NBDDC 29.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc29_param_list(self, param_list):
        self.nbddc29_param_list = param_list
        self._set_nbddc_param_list(29, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 30.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc30_param_list(self):
        return self.nbddc30_param_list

    ##
    # \brief Sets the parameter list for NBDDC 30.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc30_param_list(self, param_list):
        self.nbddc30_param_list = param_list
        self._set_nbddc_param_list(30, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 31.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc31_param_list(self):
        return self.nbddc31_param_list

    ##
    # \brief Sets the parameter list for NBDDC 31.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc31_param_list(self, param_list):
        self.nbddc31_param_list = param_list
        self._set_nbddc_param_list(31, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 32.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc32_param_list(self):
        return self.nbddc32_param_list

    ##
    # \brief Sets the parameter list for NBDDC 32.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc32_param_list(self, param_list):
        self.nbddc32_param_list = param_list
        self._set_nbddc_param_list(32, param_list)

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
    
    def _set_nbddc_param_list(self, nbddc_index, nbddc_param_list, atinit=False):
        configDict = {
          "ddcConfiguration": {
            "narrowband": {
                nbddc_index: {
                    'rfIndex': nbddc_param_list[2],
                    'rateIndex': nbddc_param_list[3],
                    'enable': 1 if nbddc_param_list[4] else 0,
                    'frequency': nbddc_param_list[5],
                },
            },
          },
        }
        if atinit:
            configDict = self._merge_dicts(configDict, {
              "ddcConfiguration": {
                "narrowband": {
                    nbddc_index: {
                        'udpDest': nbddc_param_list[0],          
                        'streamId': nbddc_param_list[0], 
                        'vitaEnable': nbddc_param_list[1],
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
            ddc_coherent=False,
            num_outputs=1,
            tagged=self.tagged,
            debug=False,
        )
    
    def _get_configured_nbddc(self, nbddc_index, nbddc_param_list):
        self._set_nbddc_param_list(nbddc_index, nbddc_param_list, atinit=True)
        return CyberRadio.vita_iq_source_mk3(
            vita_type=nbddc_param_list[1],
            payload_size=self.vita_payload_size,
            vita_header_size=self.vita_header_size,
            vita_tail_size=self.vita_tail_size,
            byte_swapped=self.byte_swapped,
            iq_swapped=self.iq_swapped,
            iq_scale_factor=2**-15,
            host=self.udp_host_name,
            port=nbddc_param_list[0],
            ddc_coherent=False,
            num_outputs=1,
            tagged=self.tagged,
            debug=False,
        )
    
    def _merge_dicts(self, a, b):
        if not isinstance(b, dict):
            return b
        result = copy.deepcopy(a)
        for k, v in b.iteritems():
            if k in result and isinstance(result[k], dict):
                    result[k] = self._merge_dicts(result[k], v)
            else:
                result[k] = copy.deepcopy(v)
        return result
        
