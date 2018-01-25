#!/usr/bin/env python
###############################################################
# \package CyberRadio.NDR551_source
# 
# \brief I/Q data source block using the NDR551 radio
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

##
# \class NDR551_source
# \ingroup CyberRadioNDR551
# \brief I/Q data source block using the NDR551 radio.
#
# The NDR551_source block supplies wideband DDC outputs, as indicated 
# by the Number of WBDDCs setting, and narrowband DDC outputs, as indicated 
# by the Number of NBDDCs setting. Any outputs supplied by this block are 
# optional, so the user does not need to connect them if they are not 
# being used.  The NDR551_source block also supplies a character-stream 
# output for collecting logging data from the underlying driver interface.
#
# Tuners, WBDDCs, and NBDDCs are configured via parameter lists.  Parameter
# lists are standard Python lists, formatted as follows:
# \li A tuner parameter list contains the following elements: [tuner 
#    enabled flag, tuner frequency (Hz), tuner attenuation (dB)]. 
# \li A WBDDC parameter list contains the following elements: [UDP 
#    port number, VITA type, sample rate index, enabled flag, 
#    frequency (Hz), attenuation (dB)]. 
# \li An NBDDC parameter list contains the following elements: [UDP 
#    port number, VITA type, sample rate index, enabled flag, 
#    frequency offset (Hz)]. 
#
# The NDR551_source block can also produce stream tags for any DDCs 
# configured to use VITA 49 frames.  See the documentation for the base 
# VITA I/Q Source block for details on the stream tags produced.
# 
# \note The parameter list scheme is a workaround to get around the
#    (undocumented) parameter limit that GNU Radio Companion 
#    silently imposes.
# 
class NDR551_source(gr.hier_block2):

    ##
    # \brief Constructs an NDR551_source object.
    #
    # \param verbose_mode Verbose mode for logging.
    # \param radio_host_name Host name for the radio.
    # \param radio_host_port TCP port to use for communicating with the 
    #    radio.
    # \param tengig_iface_list The list of 10GigE interface names used
    #    for the radio.
    # \param num_tuners Number of tuners to use.
    # \param tuner0_param_list Tuner 0 parameter list. 
    # \param tuner1_param_list Tuner 1 parameter list. 
    # \param tuner2_param_list Tuner 2 parameter list.
    # \param tuner3_param_list Tuner 3 parameter list. 
    # \param num_wbddcs Number of WBDDCs to use.
    # \param wbddc0_param_list WBDDC 0 parameter list.
    # \param wbddc1_param_list WBDDC 1 parameter list. 
    # \param wbddc2_param_list WBDDC 2 parameter list.
    # \param wbddc3_param_list WBDDC 3 parameter list. 
    # \param num_nbddcs Number of NBDDCs to use.
    # \param nbddc0_param_list NBDDC 0 parameter list. 
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
    # \param nbddc33_param_list NBDDC 33 parameter list. 
    # \param nbddc34_param_list NBDDC 34 parameter list. 
    # \param nbddc35_param_list NBDDC 35 parameter list. 
    # \param nbddc36_param_list NBDDC 36 parameter list. 
    # \param nbddc37_param_list NBDDC 37 parameter list. 
    # \param nbddc38_param_list NBDDC 38 parameter list. 
    # \param nbddc39_param_list NBDDC 39 parameter list. 
    # \param nbddc40_param_list NBDDC 40 parameter list. 
    # \param nbddc41_param_list NBDDC 41 parameter list. 
    # \param nbddc42_param_list NBDDC 42 parameter list. 
    # \param nbddc43_param_list NBDDC 43 parameter list. 
    # \param nbddc44_param_list NBDDC 44 parameter list. 
    # \param nbddc45_param_list NBDDC 45 parameter list. 
    # \param nbddc46_param_list NBDDC 46 parameter list. 
    # \param nbddc47_param_list NBDDC 47 parameter list. 
    # \param nbddc48_param_list NBDDC 48 parameter list. 
    # \param nbddc49_param_list NBDDC 49 parameter list. 
    # \param nbddc50_param_list NBDDC 50 parameter list. 
    # \param nbddc51_param_list NBDDC 51 parameter list. 
    # \param nbddc52_param_list NBDDC 52 parameter list. 
    # \param nbddc53_param_list NBDDC 53 parameter list. 
    # \param nbddc54_param_list NBDDC 54 parameter list. 
    # \param nbddc55_param_list NBDDC 55 parameter list. 
    # \param nbddc56_param_list NBDDC 56 parameter list. 
    # \param nbddc57_param_list NBDDC 57 parameter list. 
    # \param nbddc58_param_list NBDDC 58 parameter list. 
    # \param nbddc59_param_list NBDDC 59 parameter list. 
    # \param nbddc60_param_list NBDDC 60 parameter list. 
    # \param nbddc61_param_list NBDDC 61 parameter list. 
    # \param nbddc62_param_list NBDDC 62 parameter list. 
    # \param nbddc63_param_list NBDDC 63 parameter list. 
    # \param tagged Whether the block should produce stream tags.
    def __init__(self, 
                 verbose_mode=True, 
                 radio_host_name="ndr651", 
                 radio_host_port=8617, 
                 tengig_iface_list=['eth10', 'eth11', 'eth12', 'eth13'], 
                 num_tuners=1,
                 tuner0_param_list=[False, 900e6, 0],
                 tuner1_param_list=[False, 900e6, 0],
                 tuner2_param_list=[False, 900e6, 0],
                 tuner3_param_list=[False, 900e6, 0],
                 num_wbddcs=1, 
                 wbddc0_param_list=[40000, 0, 0, False],
                 wbddc1_param_list=[40001, 0, 0, False],
                 wbddc2_param_list=[40002, 0, 0, False],
                 wbddc3_param_list=[40003, 0, 0, False],
                 num_nbddcs=1, 
                 nbddc0_param_list=[41000, 0, 0, False, 0.0],
                 nbddc1_param_list=[41001, 0, 0, False, 0.0],
                 nbddc2_param_list=[41002, 0, 0, False, 0.0],
                 nbddc3_param_list=[41003, 0, 0, False, 0.0],
                 nbddc4_param_list=[41004, 0, 0, False, 0.0],
                 nbddc5_param_list=[41005, 0, 0, False, 0.0],
                 nbddc6_param_list=[41006, 0, 0, False, 0.0],
                 nbddc7_param_list=[41007, 0, 0, False, 0.0],
                 nbddc8_param_list=[41008, 0, 0, False, 0.0],
                 nbddc9_param_list=[41009, 0, 0, False, 0.0],
                 nbddc10_param_list=[41010, 0, 0, False, 0.0],
                 nbddc11_param_list=[41011, 0, 0, False, 0.0],
                 nbddc12_param_list=[41012, 0, 0, False, 0.0],
                 nbddc13_param_list=[41013, 0, 0, False, 0.0],
                 nbddc14_param_list=[41014, 0, 0, False, 0.0],
                 nbddc15_param_list=[41015, 0, 0, False, 0.0],
                 nbddc16_param_list=[41016, 0, 0, False, 0.0],
                 nbddc17_param_list=[41017, 0, 0, False, 0.0],
                 nbddc18_param_list=[41018, 0, 0, False, 0.0],
                 nbddc19_param_list=[41019, 0, 0, False, 0.0],
                 nbddc20_param_list=[41020, 0, 0, False, 0.0],
                 nbddc21_param_list=[41021, 0, 0, False, 0.0],
                 nbddc22_param_list=[41022, 0, 0, False, 0.0],
                 nbddc23_param_list=[41023, 0, 0, False, 0.0],
                 nbddc24_param_list=[41024, 0, 0, False, 0.0],
                 nbddc25_param_list=[41025, 0, 0, False, 0.0],
                 nbddc26_param_list=[41026, 0, 0, False, 0.0],
                 nbddc27_param_list=[41027, 0, 0, False, 0.0],
                 nbddc28_param_list=[41028, 0, 0, False, 0.0],
                 nbddc29_param_list=[41029, 0, 0, False, 0.0],
                 nbddc30_param_list=[41030, 0, 0, False, 0.0],
                 nbddc31_param_list=[41031, 0, 0, False, 0.0],
                 nbddc32_param_list=[41032, 0, 0, False, 0.0],
                 nbddc33_param_list=[41033, 0, 0, False, 0.0],
                 nbddc34_param_list=[41034, 0, 0, False, 0.0],
                 nbddc35_param_list=[41035, 0, 0, False, 0.0],
                 nbddc36_param_list=[41036, 0, 0, False, 0.0],
                 nbddc37_param_list=[41037, 0, 0, False, 0.0],
                 nbddc38_param_list=[41038, 0, 0, False, 0.0],
                 nbddc39_param_list=[41039, 0, 0, False, 0.0],
                 nbddc40_param_list=[41040, 0, 0, False, 0.0],
                 nbddc41_param_list=[41041, 0, 0, False, 0.0],
                 nbddc42_param_list=[41042, 0, 0, False, 0.0],
                 nbddc43_param_list=[41043, 0, 0, False, 0.0],
                 nbddc44_param_list=[41044, 0, 0, False, 0.0],
                 nbddc45_param_list=[41045, 0, 0, False, 0.0],
                 nbddc46_param_list=[41046, 0, 0, False, 0.0],
                 nbddc47_param_list=[41047, 0, 0, False, 0.0],
                 nbddc48_param_list=[41048, 0, 0, False, 0.0],
                 nbddc49_param_list=[41049, 0, 0, False, 0.0],
                 nbddc50_param_list=[41050, 0, 0, False, 0.0],
                 nbddc51_param_list=[41051, 0, 0, False, 0.0],
                 nbddc52_param_list=[41052, 0, 0, False, 0.0],
                 nbddc53_param_list=[41053, 0, 0, False, 0.0],
                 nbddc54_param_list=[41054, 0, 0, False, 0.0],
                 nbddc55_param_list=[41055, 0, 0, False, 0.0],
                 nbddc56_param_list=[41056, 0, 0, False, 0.0],
                 nbddc57_param_list=[41057, 0, 0, False, 0.0],
                 nbddc58_param_list=[41058, 0, 0, False, 0.0],
                 nbddc59_param_list=[41059, 0, 0, False, 0.0],
                 nbddc60_param_list=[41060, 0, 0, False, 0.0],
                 nbddc61_param_list=[41061, 0, 0, False, 0.0],
                 nbddc62_param_list=[41062, 0, 0, False, 0.0],
                 nbddc63_param_list=[41063, 0, 0, False, 0.0],
                 tagged=False,
                 ):
        gr.hier_block2.__init__(
            self, "[CyberRadio] NDR551 Source",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev(num_wbddcs + num_nbddcs + 1, 
                             num_wbddcs + num_nbddcs + 1, 
                             [gr.sizeof_char*1] +
                                num_wbddcs * [gr.sizeof_gr_complex*1] + \
                                num_nbddcs * [gr.sizeof_gr_complex*1]),
        )
        self.logger = gr.logger("CyberRadio")
        self.logger.set_level("INFO")
        self.verbose_mode = verbose_mode
        self.radio_host_name = radio_host_name
        self.radio_host_port = radio_host_port
        self.tengig_iface_list = tengig_iface_list
        self.num_tuners = num_tuners
        self.tuner0_param_list = tuner0_param_list
        self.tuner1_param_list = tuner1_param_list
        self.tuner2_param_list = tuner2_param_list
        self.tuner3_param_list = tuner3_param_list
        self.num_wbddcs = num_wbddcs
        self.wbddc0_param_list = wbddc0_param_list
        self.wbddc1_param_list = wbddc1_param_list
        self.wbddc2_param_list = wbddc2_param_list
        self.wbddc3_param_list = wbddc3_param_list
        self.num_nbddcs = num_nbddcs
        self.nbddc0_param_list = nbddc0_param_list
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
        self.nbddc33_param_list = nbddc33_param_list
        self.nbddc34_param_list = nbddc34_param_list
        self.nbddc35_param_list = nbddc35_param_list
        self.nbddc36_param_list = nbddc36_param_list
        self.nbddc37_param_list = nbddc37_param_list
        self.nbddc38_param_list = nbddc38_param_list
        self.nbddc39_param_list = nbddc39_param_list
        self.nbddc40_param_list = nbddc40_param_list
        self.nbddc41_param_list = nbddc41_param_list
        self.nbddc42_param_list = nbddc42_param_list
        self.nbddc43_param_list = nbddc43_param_list
        self.nbddc44_param_list = nbddc44_param_list
        self.nbddc45_param_list = nbddc45_param_list
        self.nbddc46_param_list = nbddc46_param_list
        self.nbddc47_param_list = nbddc47_param_list
        self.nbddc48_param_list = nbddc48_param_list
        self.nbddc49_param_list = nbddc49_param_list
        self.nbddc50_param_list = nbddc50_param_list
        self.nbddc51_param_list = nbddc51_param_list
        self.nbddc52_param_list = nbddc52_param_list
        self.nbddc53_param_list = nbddc53_param_list
        self.nbddc54_param_list = nbddc54_param_list
        self.nbddc55_param_list = nbddc55_param_list
        self.nbddc56_param_list = nbddc56_param_list
        self.nbddc57_param_list = nbddc57_param_list
        self.nbddc58_param_list = nbddc58_param_list
        self.nbddc59_param_list = nbddc59_param_list
        self.nbddc60_param_list = nbddc60_param_list
        self.nbddc61_param_list = nbddc61_param_list
        self.nbddc62_param_list = nbddc62_param_list
        self.nbddc63_param_list = nbddc63_param_list
        self.tagged = tagged
        self.CyberRadio_file_like_object_source_0 = CyberRadio.file_like_object_source()
        self.connect((self.CyberRadio_file_like_object_source_0, 0), (self, 0))
        self.CyberRadio_NDR_driver_interface_0 = CyberRadio.NDR_driver_interface(
            radio_type="ndr551",
            verbose=verbose_mode,
            log_file=self.CyberRadio_file_like_object_source_0,
            connect_mode="udp",
            host_name=radio_host_name,
            host_port=radio_host_port,
        )
        self.vita_tail_size = vita_tail_size = self.CyberRadio_NDR_driver_interface_0.getVitaTailSize()
        self.vita_payload_size = vita_payload_size = self.CyberRadio_NDR_driver_interface_0.getVitaPayloadSize()
        self.vita_header_size = vita_header_size = self.CyberRadio_NDR_driver_interface_0.getVitaHeaderSize()
        self.iq_swapped = iq_swapped = self.CyberRadio_NDR_driver_interface_0.isIqSwapped()
        self.byte_swapped = byte_swapped = self.CyberRadio_NDR_driver_interface_0.isByteswapped()
        self.udp_host_name = CyberRadioDriver.getInterfaceAddresses(self.tengig_iface_to_use)[1]
        self._set_udp_dest_info()
        if self.num_tuners >= 1:
            self._set_tuner_param_list(0, tuner0_param_list)
        if self.num_tuners >= 2:
            self._set_tuner_param_list(1, tuner1_param_list)
        if self.num_tuners >= 3:
            self._set_tuner_param_list(2, tuner2_param_list)
        if self.num_tuners >= 4:
            self._set_tuner_param_list(3, tuner3_param_list)
        self.wbddc_sources = {}
        if self.num_wbddcs >= 1:
            self.CyberRadio_vita_iq_source_wbddc_0 = self._get_configured_wbddc(0, wbddc0_param_list)
            self.connect((self.CyberRadio_vita_iq_source_wbddc_4, 0), (self, 1))
            self.wbddc_sources[0] = self.CyberRadio_vita_iq_source_wbddc_0
        if self.num_wbddcs >= 2:
            self.CyberRadio_vita_iq_source_wbddc_1 = self._get_configured_wbddc(1, wbddc1_param_list)
            self.connect((self.CyberRadio_vita_iq_source_wbddc_1, 0), (self, 2))
            self.wbddc_sources[1] = self.CyberRadio_vita_iq_source_wbddc_1
        if self.num_wbddcs >= 3:
            self.CyberRadio_vita_iq_source_wbddc_2 = self._get_configured_wbddc(2, wbddc2_param_list)
            self.connect((self.CyberRadio_vita_iq_source_wbddc_2, 0), (self, 3))
            self.wbddc_sources[2] = self.CyberRadio_vita_iq_source_wbddc_2
        if self.num_wbddcs >= 4:
            self.CyberRadio_vita_iq_source_wbddc_3 = self._get_configured_wbddc(3, wbddc3_param_list)
            self.connect((self.CyberRadio_vita_iq_source_wbddc_3, 0), (self, 4))
            self.wbddc_sources[3] = self.CyberRadio_vita_iq_source_wbddc_3
        self.nbddc_sources = {}
        if self.num_nbddcs >= 1:
            self.CyberRadio_vita_iq_source_nbddc_0 = self._get_configured_nbddc(0, nbddc64_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_0, 0), (self, self.num_wbddcs + 1))
            self.nbddc_sources[0] = self.CyberRadio_vita_iq_source_nbddc_0
        if self.num_nbddcs >= 2:
            self.CyberRadio_vita_iq_source_nbddc_1 = self._get_configured_nbddc(1, nbddc1_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_1, 0), (self, self.num_wbddcs + 2))
            self.nbddc_sources[1] = self.CyberRadio_vita_iq_source_nbddc_1
        if self.num_nbddcs >= 3:
            self.CyberRadio_vita_iq_source_nbddc_2 = self._get_configured_nbddc(2, nbddc2_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_2, 0), (self, self.num_wbddcs + 3))
            self.nbddc_sources[2] = self.CyberRadio_vita_iq_source_nbddc_2
        if self.num_nbddcs >= 4:
            self.CyberRadio_vita_iq_source_nbddc_3 = self._get_configured_nbddc(3, nbddc3_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_3, 0), (self, self.num_wbddcs + 4))
            self.nbddc_sources[3] = self.CyberRadio_vita_iq_source_nbddc_3
        if self.num_nbddcs >= 5:
            self.CyberRadio_vita_iq_source_nbddc_4 = self._get_configured_nbddc(4, nbddc4_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_4, 0), (self, self.num_wbddcs + 5))
            self.nbddc_sources[4] = self.CyberRadio_vita_iq_source_nbddc_4
        if self.num_nbddcs >= 6:
            self.CyberRadio_vita_iq_source_nbddc_5 = self._get_configured_nbddc(5, nbddc5_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_5, 0), (self, self.num_wbddcs + 6))
            self.nbddc_sources[5] = self.CyberRadio_vita_iq_source_nbddc_5
        if self.num_nbddcs >= 7:
            self.CyberRadio_vita_iq_source_nbddc_6 = self._get_configured_nbddc(6, nbddc6_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_6, 0), (self, self.num_wbddcs + 7))
            self.nbddc_sources[6] = self.CyberRadio_vita_iq_source_nbddc_6
        if self.num_nbddcs >= 8:
            self.CyberRadio_vita_iq_source_nbddc_6 = self._get_configured_nbddc(7, nbddc7_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_6, 0), (self, self.num_wbddcs + 8))
            self.nbddc_sources[7] = self.CyberRadio_vita_iq_source_nbddc_6
        if self.num_nbddcs >= 9:
            self.CyberRadio_vita_iq_source_nbddc_8 = self._get_configured_nbddc(8, nbddc8_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_8, 0), (self, self.num_wbddcs + 9))
            self.nbddc_sources[8] = self.CyberRadio_vita_iq_source_nbddc_8
        if self.num_nbddcs >= 10:
            self.CyberRadio_vita_iq_source_nbddc_9 = self._get_configured_nbddc(9, nbddc9_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_9, 0), (self, self.num_wbddcs + 10))
            self.nbddc_sources[9] = self.CyberRadio_vita_iq_source_nbddc_9
        if self.num_nbddcs >= 11:
            self.CyberRadio_vita_iq_source_nbddc_10 = self._get_configured_nbddc(10, nbddc10_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_10, 0), (self, self.num_wbddcs + 11))
            self.nbddc_sources[10] = self.CyberRadio_vita_iq_source_nbddc_10
        if self.num_nbddcs >= 12:
            self.CyberRadio_vita_iq_source_nbddc_11 = self._get_configured_nbddc(11, nbddc11_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_11, 0), (self, self.num_wbddcs + 12))
            self.nbddc_sources[11] = self.CyberRadio_vita_iq_source_nbddc_11
        if self.num_nbddcs >= 13:
            self.CyberRadio_vita_iq_source_nbddc_12 = self._get_configured_nbddc(12, nbddc12_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_12, 0), (self, self.num_wbddcs + 13))
            self.nbddc_sources[12] = self.CyberRadio_vita_iq_source_nbddc_12
        if self.num_nbddcs >= 14:
            self.CyberRadio_vita_iq_source_nbddc_13 = self._get_configured_nbddc(13, nbddc13_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_13, 0), (self, self.num_wbddcs + 14))
            self.nbddc_sources[13] = self.CyberRadio_vita_iq_source_nbddc_13
        if self.num_nbddcs >= 15:
            self.CyberRadio_vita_iq_source_nbddc_14 = self._get_configured_nbddc(14, nbddc14_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_14, 0), (self, self.num_wbddcs + 15))
            self.nbddc_sources[14] = self.CyberRadio_vita_iq_source_nbddc_14
        if self.num_nbddcs >= 16:
            self.CyberRadio_vita_iq_source_nbddc_15 = self._get_configured_nbddc(15, nbddc15_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_15, 0), (self, self.num_wbddcs + 16))
            self.nbddc_sources[15] = self.CyberRadio_vita_iq_source_nbddc_15
        if self.num_nbddcs >= 17:
            self.CyberRadio_vita_iq_source_nbddc_16 = self._get_configured_nbddc(16, nbddc16_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_16, 0), (self, self.num_wbddcs + 17))
            self.nbddc_sources[16] = self.CyberRadio_vita_iq_source_nbddc_16
        if self.num_nbddcs >= 18:
            self.CyberRadio_vita_iq_source_nbddc_17 = self._get_configured_nbddc(17, nbddc17_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_17, 0), (self, self.num_wbddcs + 18))
            self.nbddc_sources[17] = self.CyberRadio_vita_iq_source_nbddc_17
        if self.num_nbddcs >= 19:
            self.CyberRadio_vita_iq_source_nbddc_18 = self._get_configured_nbddc(18, nbddc18_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_18, 0), (self, self.num_wbddcs + 19))
            self.nbddc_sources[18] = self.CyberRadio_vita_iq_source_nbddc_18
        if self.num_nbddcs >= 20:
            self.CyberRadio_vita_iq_source_nbddc_19 = self._get_configured_nbddc(19, nbddc19_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_19, 0), (self, self.num_wbddcs + 20))
            self.nbddc_sources[19] = self.CyberRadio_vita_iq_source_nbddc_19
        if self.num_nbddcs >= 21:
            self.CyberRadio_vita_iq_source_nbddc_20 = self._get_configured_nbddc(20, nbddc20_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_20, 0), (self, self.num_wbddcs + 21))
            self.nbddc_sources[20] = self.CyberRadio_vita_iq_source_nbddc_20
        if self.num_nbddcs >= 22:
            self.CyberRadio_vita_iq_source_nbddc_21 = self._get_configured_nbddc(21, nbddc21_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_21, 0), (self, self.num_wbddcs + 22))
            self.nbddc_sources[21] = self.CyberRadio_vita_iq_source_nbddc_21
        if self.num_nbddcs >= 23:
            self.CyberRadio_vita_iq_source_nbddc_22 = self._get_configured_nbddc(22, nbddc22_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_22, 0), (self, self.num_wbddcs + 23))
            self.nbddc_sources[22] = self.CyberRadio_vita_iq_source_nbddc_22
        if self.num_nbddcs >= 24:
            self.CyberRadio_vita_iq_source_nbddc_23 = self._get_configured_nbddc(23, nbddc23_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_23, 0), (self, self.num_wbddcs + 24))
            self.nbddc_sources[23] = self.CyberRadio_vita_iq_source_nbddc_23
        if self.num_nbddcs >= 25:
            self.CyberRadio_vita_iq_source_nbddc_24 = self._get_configured_nbddc(24, nbddc24_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_24, 0), (self, self.num_wbddcs + 25))
            self.nbddc_sources[24] = self.CyberRadio_vita_iq_source_nbddc_24
        if self.num_nbddcs >= 26:
            self.CyberRadio_vita_iq_source_nbddc_25 = self._get_configured_nbddc(25, nbddc25_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_25, 0), (self, self.num_wbddcs + 26))
            self.nbddc_sources[25] = self.CyberRadio_vita_iq_source_nbddc_25
        if self.num_nbddcs >= 27:
            self.CyberRadio_vita_iq_source_nbddc_26 = self._get_configured_nbddc(26, nbddc26_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_26, 0), (self, self.num_wbddcs + 27))
            self.nbddc_sources[26] = self.CyberRadio_vita_iq_source_nbddc_26
        if self.num_nbddcs >= 28:
            self.CyberRadio_vita_iq_source_nbddc_27 = self._get_configured_nbddc(27, nbddc27_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_27, 0), (self, self.num_wbddcs + 28))
            self.nbddc_sources[27] = self.CyberRadio_vita_iq_source_nbddc_27
        if self.num_nbddcs >= 29:
            self.CyberRadio_vita_iq_source_nbddc_28 = self._get_configured_nbddc(28, nbddc28_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_28, 0), (self, self.num_wbddcs + 29))
            self.nbddc_sources[28] = self.CyberRadio_vita_iq_source_nbddc_28
        if self.num_nbddcs >= 30:
            self.CyberRadio_vita_iq_source_nbddc_29 = self._get_configured_nbddc(29, nbddc29_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_29, 0), (self, self.num_wbddcs + 30))
            self.nbddc_sources[29] = self.CyberRadio_vita_iq_source_nbddc_29
        if self.num_nbddcs >= 31:
            self.CyberRadio_vita_iq_source_nbddc_30 = self._get_configured_nbddc(30, nbddc30_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_30, 0), (self, self.num_wbddcs + 31))
            self.nbddc_sources[30] = self.CyberRadio_vita_iq_source_nbddc_30
        if self.num_nbddcs >= 32:
            self.CyberRadio_vita_iq_source_nbddc_31 = self._get_configured_nbddc(31, nbddc31_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_31, 0), (self, self.num_wbddcs + 32))
            self.nbddc_sources[31] = self.CyberRadio_vita_iq_source_nbddc_31
        if self.num_nbddcs >= 33:
            self.CyberRadio_vita_iq_source_nbddc_32 = self._get_configured_nbddc(32, nbddc32_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_32, 0), (self, self.num_wbddcs + 33))
            self.nbddc_sources[32] = self.CyberRadio_vita_iq_source_nbddc_32
        if self.num_nbddcs >= 34:
            self.CyberRadio_vita_iq_source_nbddc_33 = self._get_configured_nbddc(33, nbddc33_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_33, 0), (self, self.num_wbddcs + 34))
            self.nbddc_sources[33] = self.CyberRadio_vita_iq_source_nbddc_33
        if self.num_nbddcs >= 35:
            self.CyberRadio_vita_iq_source_nbddc_34 = self._get_configured_nbddc(34, nbddc34_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_34, 0), (self, self.num_wbddcs + 35))
            self.nbddc_sources[34] = self.CyberRadio_vita_iq_source_nbddc_34
        if self.num_nbddcs >= 36:
            self.CyberRadio_vita_iq_source_nbddc_35 = self._get_configured_nbddc(35, nbddc35_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_35, 0), (self, self.num_wbddcs + 36))
            self.nbddc_sources[35] = self.CyberRadio_vita_iq_source_nbddc_35
        if self.num_nbddcs >= 37:
            self.CyberRadio_vita_iq_source_nbddc_36 = self._get_configured_nbddc(36, nbddc36_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_36, 0), (self, self.num_wbddcs + 37))
            self.nbddc_sources[36] = self.CyberRadio_vita_iq_source_nbddc_36
        if self.num_nbddcs >= 38:
            self.CyberRadio_vita_iq_source_nbddc_37 = self._get_configured_nbddc(37, nbddc37_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_37, 0), (self, self.num_wbddcs + 38))
            self.nbddc_sources[37] = self.CyberRadio_vita_iq_source_nbddc_37
        if self.num_nbddcs >= 39:
            self.CyberRadio_vita_iq_source_nbddc_38 = self._get_configured_nbddc(38, nbddc38_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_38, 0), (self, self.num_wbddcs + 39))
            self.nbddc_sources[38] = self.CyberRadio_vita_iq_source_nbddc_38
        if self.num_nbddcs >= 40:
            self.CyberRadio_vita_iq_source_nbddc_39 = self._get_configured_nbddc(39, nbddc39_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_39, 0), (self, self.num_wbddcs + 40))
            self.nbddc_sources[39] = self.CyberRadio_vita_iq_source_nbddc_39
        if self.num_nbddcs >= 41:
            self.CyberRadio_vita_iq_source_nbddc_40 = self._get_configured_nbddc(40, nbddc40_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_40, 0), (self, self.num_wbddcs + 41))
            self.nbddc_sources[40] = self.CyberRadio_vita_iq_source_nbddc_40
        if self.num_nbddcs >= 42:
            self.CyberRadio_vita_iq_source_nbddc_41 = self._get_configured_nbddc(41, nbddc41_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_41, 0), (self, self.num_wbddcs + 42))
            self.nbddc_sources[41] = self.CyberRadio_vita_iq_source_nbddc_41
        if self.num_nbddcs >= 43:
            self.CyberRadio_vita_iq_source_nbddc_42 = self._get_configured_nbddc(42, nbddc42_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_42, 0), (self, self.num_wbddcs + 43))
            self.nbddc_sources[42] = self.CyberRadio_vita_iq_source_nbddc_42
        if self.num_nbddcs >= 44:
            self.CyberRadio_vita_iq_source_nbddc_43 = self._get_configured_nbddc(43, nbddc43_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_43, 0), (self, self.num_wbddcs + 44))
            self.nbddc_sources[43] = self.CyberRadio_vita_iq_source_nbddc_43
        if self.num_nbddcs >= 45:
            self.CyberRadio_vita_iq_source_nbddc_44 = self._get_configured_nbddc(44, nbddc44_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_44, 0), (self, self.num_wbddcs + 45))
            self.nbddc_sources[44] = self.CyberRadio_vita_iq_source_nbddc_44
        if self.num_nbddcs >= 46:
            self.CyberRadio_vita_iq_source_nbddc_45 = self._get_configured_nbddc(45, nbddc45_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_45, 0), (self, self.num_wbddcs + 46))
            self.nbddc_sources[45] = self.CyberRadio_vita_iq_source_nbddc_45
        if self.num_nbddcs >= 47:
            self.CyberRadio_vita_iq_source_nbddc_46 = self._get_configured_nbddc(46, nbddc46_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_46, 0), (self, self.num_wbddcs + 47))
            self.nbddc_sources[46] = self.CyberRadio_vita_iq_source_nbddc_46
        if self.num_nbddcs >= 48:
            self.CyberRadio_vita_iq_source_nbddc_47 = self._get_configured_nbddc(47, nbddc47_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_47, 0), (self, self.num_wbddcs + 48))
            self.nbddc_sources[47] = self.CyberRadio_vita_iq_source_nbddc_47
        if self.num_nbddcs >= 49:
            self.CyberRadio_vita_iq_source_nbddc_48 = self._get_configured_nbddc(48, nbddc48_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_48, 0), (self, self.num_wbddcs + 49))
            self.nbddc_sources[48] = self.CyberRadio_vita_iq_source_nbddc_48
        if self.num_nbddcs >= 50:
            self.CyberRadio_vita_iq_source_nbddc_49 = self._get_configured_nbddc(49, nbddc49_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_49, 0), (self, self.num_wbddcs + 50))
            self.nbddc_sources[49] = self.CyberRadio_vita_iq_source_nbddc_49
        if self.num_nbddcs >= 51:
            self.CyberRadio_vita_iq_source_nbddc_50 = self._get_configured_nbddc(50, nbddc50_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_50, 0), (self, self.num_wbddcs + 51))
            self.nbddc_sources[50] = self.CyberRadio_vita_iq_source_nbddc_50
        if self.num_nbddcs >= 52:
            self.CyberRadio_vita_iq_source_nbddc_51 = self._get_configured_nbddc(51, nbddc51_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_51, 0), (self, self.num_wbddcs + 52))
            self.nbddc_sources[51] = self.CyberRadio_vita_iq_source_nbddc_51
        if self.num_nbddcs >= 53:
            self.CyberRadio_vita_iq_source_nbddc_52 = self._get_configured_nbddc(52, nbddc52_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_52, 0), (self, self.num_wbddcs + 53))
            self.nbddc_sources[52] = self.CyberRadio_vita_iq_source_nbddc_52
        if self.num_nbddcs >= 54:
            self.CyberRadio_vita_iq_source_nbddc_53 = self._get_configured_nbddc(53, nbddc53_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_53, 0), (self, self.num_wbddcs + 54))
            self.nbddc_sources[53] = self.CyberRadio_vita_iq_source_nbddc_53
        if self.num_nbddcs >= 55:
            self.CyberRadio_vita_iq_source_nbddc_54 = self._get_configured_nbddc(54, nbddc54_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_54, 0), (self, self.num_wbddcs + 55))
            self.nbddc_sources[54] = self.CyberRadio_vita_iq_source_nbddc_54
        if self.num_nbddcs >= 56:
            self.CyberRadio_vita_iq_source_nbddc_55 = self._get_configured_nbddc(55, nbddc55_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_55, 0), (self, self.num_wbddcs + 56))
            self.nbddc_sources[55] = self.CyberRadio_vita_iq_source_nbddc_55
        if self.num_nbddcs >= 57:
            self.CyberRadio_vita_iq_source_nbddc_56 = self._get_configured_nbddc(56, nbddc56_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_56, 0), (self, self.num_wbddcs + 57))
            self.nbddc_sources[56] = self.CyberRadio_vita_iq_source_nbddc_56
        if self.num_nbddcs >= 58:
            self.CyberRadio_vita_iq_source_nbddc_57 = self._get_configured_nbddc(57, nbddc57_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_57, 0), (self, self.num_wbddcs + 58))
            self.nbddc_sources[57] = self.CyberRadio_vita_iq_source_nbddc_57
        if self.num_nbddcs >= 59:
            self.CyberRadio_vita_iq_source_nbddc_58 = self._get_configured_nbddc(58, nbddc58_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_58, 0), (self, self.num_wbddcs + 59))
            self.nbddc_sources[58] = self.CyberRadio_vita_iq_source_nbddc_58
        if self.num_nbddcs >= 60:
            self.CyberRadio_vita_iq_source_nbddc_59 = self._get_configured_nbddc(59, nbddc59_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_59, 0), (self, self.num_wbddcs + 60))
            self.nbddc_sources[59] = self.CyberRadio_vita_iq_source_nbddc_59
        if self.num_nbddcs >= 61:
            self.CyberRadio_vita_iq_source_nbddc_60 = self._get_configured_nbddc(60, nbddc60_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_60, 0), (self, self.num_wbddcs + 61))
            self.nbddc_sources[60] = self.CyberRadio_vita_iq_source_nbddc_60
        if self.num_nbddcs >= 62:
            self.CyberRadio_vita_iq_source_nbddc_61 = self._get_configured_nbddc(61, nbddc61_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_61, 0), (self, self.num_wbddcs + 62))
            self.nbddc_sources[61] = self.CyberRadio_vita_iq_source_nbddc_61
        if self.num_nbddcs >= 63:
            self.CyberRadio_vita_iq_source_nbddc_62 = self._get_configured_nbddc(62, nbddc62_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_62, 0), (self, self.num_wbddcs + 63))
            self.nbddc_sources[62] = self.CyberRadio_vita_iq_source_nbddc_62
        if self.num_nbddcs >= 64:
            self.CyberRadio_vita_iq_source_nbddc_63 = self._get_configured_nbddc(63, nbddc63_param_list)
            self.connect((self.CyberRadio_vita_iq_source_nbddc_63, 0), (self, self.num_wbddcs + 64))
            self.nbddc_sources[63] = self.CyberRadio_vita_iq_source_nbddc_63


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
    # \brief Gets the parameter list for Tuner 0.
    # \return The tuner parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_tuner0_param_list(self):
        return self.tuner0_param_list

    ##
    # \brief Sets the parameter list for Tuner 0.
    # \param param_list The tuner parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_tuner0_param_list(self, param_list):
        self.tuner0_param_list = param_list
        self._set_tuner_param_list(0, param_list)

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
    # \brief Gets the number of WBDDCs in use.
    # \return The the number of WBDDCs in use.
    def get_num_wbddcs(self):
        return self.num_wbddcs

    ##
    # \brief Gets the parameter list for WBDDC 0.
    # \return The WBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbddc0_param_list(self):
        return self.wbddc0_param_list

    ##
    # \brief Sets the parameter list for WBDDC 0.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The WBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbddc0_param_list(self, param_list):
        self.wbddc0_param_list = param_list
        self._set_wbddc_param_list(0, param_list)

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
    # \brief Gets the number of NBDDCs in use.
    # \return The the number of NBDDCs in use.
    def get_num_nbddcs(self):
        return self.num_nbddcs

    ##
    # \brief Gets the parameter list for NBDDC 0.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc0_param_list(self):
        return self.nbddc0_param_list

    ##
    # \brief Sets the parameter list for NBDDC 0.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc0_param_list(self, param_list):
        self.nbddc0_param_list = param_list
        self._set_nbddc_param_list(0, param_list)

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
    # \brief Gets the parameter list for NBDDC 33.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc33_param_list(self):
        return self.nbddc33_param_list

    ##
    # \brief Sets the parameter list for NBDDC 33.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc33_param_list(self, param_list):
        self.nbddc33_param_list = param_list
        self._set_nbddc_param_list(33, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 34.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc34_param_list(self):
        return self.nbddc34_param_list

    ##
    # \brief Sets the parameter list for NBDDC 34.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc34_param_list(self, param_list):
        self.nbddc34_param_list = param_list
        self._set_nbddc_param_list(34, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 35.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc35_param_list(self):
        return self.nbddc35_param_list

    ##
    # \brief Sets the parameter list for NBDDC 35.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc35_param_list(self, param_list):
        self.nbddc35_param_list = param_list
        self._set_nbddc_param_list(35, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 36.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc36_param_list(self):
        return self.nbddc36_param_list

    ##
    # \brief Sets the parameter list for NBDDC 36.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc36_param_list(self, param_list):
        self.nbddc36_param_list = param_list
        self._set_nbddc_param_list(36, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 37.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc37_param_list(self):
        return self.nbddc37_param_list

    ##
    # \brief Sets the parameter list for NBDDC 37.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc37_param_list(self, param_list):
        self.nbddc37_param_list = param_list
        self._set_nbddc_param_list(37, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 38.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc38_param_list(self):
        return self.nbddc38_param_list

    ##
    # \brief Sets the parameter list for NBDDC 38.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc38_param_list(self, param_list):
        self.nbddc38_param_list = param_list
        self._set_nbddc_param_list(38, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 39.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc39_param_list(self):
        return self.nbddc39_param_list

    ##
    # \brief Sets the parameter list for NBDDC 39.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc39_param_list(self, param_list):
        self.nbddc39_param_list = param_list
        self._set_nbddc_param_list(39, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 40.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc40_param_list(self):
        return self.nbddc40_param_list

    ##
    # \brief Sets the parameter list for NBDDC 40.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc40_param_list(self, param_list):
        self.nbddc40_param_list = param_list
        self._set_nbddc_param_list(40, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 41.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc41_param_list(self):
        return self.nbddc41_param_list

    ##
    # \brief Sets the parameter list for NBDDC 41.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc41_param_list(self, param_list):
        self.nbddc41_param_list = param_list
        self._set_nbddc_param_list(41, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 42.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc42_param_list(self):
        return self.nbddc42_param_list

    ##
    # \brief Sets the parameter list for NBDDC 42.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc42_param_list(self, param_list):
        self.nbddc42_param_list = param_list
        self._set_nbddc_param_list(42, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 43.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc43_param_list(self):
        return self.nbddc43_param_list

    ##
    # \brief Sets the parameter list for NBDDC 43.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc43_param_list(self, param_list):
        self.nbddc43_param_list = param_list
        self._set_nbddc_param_list(43, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 44.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc44_param_list(self):
        return self.nbddc44_param_list

    ##
    # \brief Sets the parameter list for NBDDC 44.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc44_param_list(self, param_list):
        self.nbddc44_param_list = param_list
        self._set_nbddc_param_list(44, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 45.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc45_param_list(self):
        return self.nbddc45_param_list

    ##
    # \brief Sets the parameter list for NBDDC 45.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc45_param_list(self, param_list):
        self.nbddc45_param_list = param_list
        self._set_nbddc_param_list(45, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 46.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc46_param_list(self):
        return self.nbddc46_param_list

    ##
    # \brief Sets the parameter list for NBDDC 46.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc46_param_list(self, param_list):
        self.nbddc46_param_list = param_list
        self._set_nbddc_param_list(46, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 47.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc47_param_list(self):
        return self.nbddc47_param_list

    ##
    # \brief Sets the parameter list for NBDDC 47.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc47_param_list(self, param_list):
        self.nbddc47_param_list = param_list
        self._set_nbddc_param_list(47, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 48.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc48_param_list(self):
        return self.nbddc48_param_list

    ##
    # \brief Sets the parameter list for NBDDC 48.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc48_param_list(self, param_list):
        self.nbddc48_param_list = param_list
        self._set_nbddc_param_list(48, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 49.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc49_param_list(self):
        return self.nbddc49_param_list

    ##
    # \brief Sets the parameter list for NBDDC 49.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc49_param_list(self, param_list):
        self.nbddc49_param_list = param_list
        self._set_nbddc_param_list(49, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 50.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc50_param_list(self):
        return self.nbddc50_param_list

    ##
    # \brief Sets the parameter list for NBDDC 50.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc50_param_list(self, param_list):
        self.nbddc50_param_list = param_list
        self._set_nbddc_param_list(50, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 51.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc51_param_list(self):
        return self.nbddc51_param_list

    ##
    # \brief Sets the parameter list for NBDDC 51.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc51_param_list(self, param_list):
        self.nbddc51_param_list = param_list
        self._set_nbddc_param_list(51, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 52.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc52_param_list(self):
        return self.nbddc52_param_list

    ##
    # \brief Sets the parameter list for NBDDC 52.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc52_param_list(self, param_list):
        self.nbddc52_param_list = param_list
        self._set_nbddc_param_list(52, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 53.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc53_param_list(self):
        return self.nbddc53_param_list

    ##
    # \brief Sets the parameter list for NBDDC 53.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc53_param_list(self, param_list):
        self.nbddc53_param_list = param_list
        self._set_nbddc_param_list(53, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 54.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc54_param_list(self):
        return self.nbddc54_param_list

    ##
    # \brief Sets the parameter list for NBDDC 54.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc54_param_list(self, param_list):
        self.nbddc54_param_list = param_list
        self._set_nbddc_param_list(54, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 55.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc55_param_list(self):
        return self.nbddc55_param_list

    ##
    # \brief Sets the parameter list for NBDDC 55.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc55_param_list(self, param_list):
        self.nbddc55_param_list = param_list
        self._set_nbddc_param_list(55, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 56.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc56_param_list(self):
        return self.nbddc56_param_list

    ##
    # \brief Sets the parameter list for NBDDC 56.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc56_param_list(self, param_list):
        self.nbddc56_param_list = param_list
        self._set_nbddc_param_list(56, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 57.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc57_param_list(self):
        return self.nbddc57_param_list

    ##
    # \brief Sets the parameter list for NBDDC 57.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc57_param_list(self, param_list):
        self.nbddc57_param_list = param_list
        self._set_nbddc_param_list(57, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 58.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc58_param_list(self):
        return self.nbddc58_param_list

    ##
    # \brief Sets the parameter list for NBDDC 58.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc58_param_list(self, param_list):
        self.nbddc58_param_list = param_list
        self._set_nbddc_param_list(58, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 59.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc59_param_list(self):
        return self.nbddc59_param_list

    ##
    # \brief Sets the parameter list for NBDDC 59.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc59_param_list(self, param_list):
        self.nbddc59_param_list = param_list
        self._set_nbddc_param_list(59, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 60.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc60_param_list(self):
        return self.nbddc60_param_list

    ##
    # \brief Sets the parameter list for NBDDC 60.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc60_param_list(self, param_list):
        self.nbddc60_param_list = param_list
        self._set_nbddc_param_list(60, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 61.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc61_param_list(self):
        return self.nbddc61_param_list

    ##
    # \brief Sets the parameter list for NBDDC 61.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc61_param_list(self, param_list):
        self.nbddc61_param_list = param_list
        self._set_nbddc_param_list(61, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 62.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc62_param_list(self):
        return self.nbddc62_param_list

    ##
    # \brief Sets the parameter list for NBDDC 62.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc62_param_list(self, param_list):
        self.nbddc62_param_list = param_list
        self._set_nbddc_param_list(62, param_list)

    ##
    # \brief Gets the parameter list for NBDDC 63.
    # \return The NBDDC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_nbddc63_param_list(self):
        return self.nbddc63_param_list

    ##
    # \brief Sets the parameter list for NBDDC 63.
    # \note UDP port and VITA type cannot be changed at run-time.
    # \param param_list The NBDDC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_nbddc63_param_list(self, param_list):
        self.nbddc63_param_list = param_list
        self._set_nbddc_param_list(63, param_list)

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
        tengig_iface_dict = dict(zip(self.tengig_iface_list, 
                                     self.CyberRadio_NDR_driver_interface_0.getGigEIndexRange()))
        return tengig_iface_dict.get(tengig_iface_to_use, 0)
    
    # UDP destination index assignment: 
    # -- 10GigE interface 1
    #    -- 1  = WBDDC 0
    #    -- 2-17 = NBDDCs 0-15 
    # -- 10GigE interface 2
    #    -- 1  = WBDDC 1
    #    -- 2-17 = NBDDCs 16-31 
    # -- 10GigE interface 3
    #    -- 1  = WBDDC 2
    #    -- 2-17 = NBDDCs 32-47 
    # -- 10GigE interface 4
    #    -- 1  = WBDDC 3
    #    -- 2-17 = NBDDCs 48-63 
    
    def _set_udp_dest_info(self):
        configDict = {
            "ipConfiguration": { },
            "ddcConfiguration": { 
                    "wideband": { },
                    "narrowband": { },
                },
            }
        for tengig_iface_index in xrange(0, self.tengig_iface_list, 1):
            destMac, destIp = CyberRadioDriver.getInterfaceAddresses(self.tengig_iface_list[tengig_iface_index])
            srcIpVec = destIp.split(".")
            srcIpVec[-1] = str(int(srcIpVec[-1]) + 100)
            srcIp = ".".join(srcIpVec)
            configDict["ipConfiguration"][tengig_iface_index] = {
                   "sourceIP": srcIp,
                   "destIP": {
                       "all": {
                          "ipAddr": destIp,
                          "macAddr": destMac,
                       },
                   },
                }
            configDict["ddcConfiguration"]["wideband"][tengig_iface_index] = {
                    'udpDest': 1,
                }
            configDict["ddcConfiguration"]["narrowband"].update({
                    tengig_iface_index * 16 + 0: {'udpDest': 2},
                    tengig_iface_index * 16 + 1: {'udpDest': 3},
                    tengig_iface_index * 16 + 2: {'udpDest': 4},
                    tengig_iface_index * 16 + 3: {'udpDest': 5},
                    tengig_iface_index * 16 + 4: {'udpDest': 6},
                    tengig_iface_index * 16 + 5: {'udpDest': 7},
                    tengig_iface_index * 16 + 6: {'udpDest': 8},
                    tengig_iface_index * 16 + 7: {'udpDest': 9},
                    tengig_iface_index * 16 + 8: {'udpDest': 10},
                    tengig_iface_index * 16 + 9: {'udpDest': 11},
                    tengig_iface_index * 16 + 10: {'udpDest': 12},
                    tengig_iface_index * 16 + 11: {'udpDest': 13},
                    tengig_iface_index * 16 + 12: {'udpDest': 14},
                    tengig_iface_index * 16 + 13: {'udpDest': 15},
                    tengig_iface_index * 16 + 14: {'udpDest': 16},
                    tengig_iface_index * 16 + 15: {'udpDest': 17},
                })
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
        
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
                },
            },
          },
        }
        if atinit:
            configDict = self._merge_dicts(configDict, {
              "ipConfiguration": {
                wbddc_index: {
                   "destIP": {
                       wbddc_index: {
                          "sourcePort": wbddc_param_list[0],
                          "destPort": wbddc_param_list[0],
                       },
                   },
                },
              },
              "ddcConfiguration": {
                "wideband": {
                    wbddc_index: {
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
                    'rateIndex': nbddc_param_list[2],
                    'enable': 1 if nbddc_param_list[3] else 0,
                    'frequency': nbddc_param_list[4],
                },
            },
          },
        }
        if atinit:
            configDict = self._merge_dicts(configDict, {
              "ipConfiguration": {
                nbddc_index / 16: {
                   "destIP": {
                       nbddc_index / 16 + 2: {
                          "sourcePort": nbddc_param_list[0],
                          "destPort": nbddc_param_list[0],
                       },
                   },
                },
              },
              "ddcConfiguration": {
                "narrowband": {
                    nbddc_index: {
                        'streamId': nbddc_param_list[0], 
                        'vitaEnable': nbddc_param_list[1],
                    },
                },
              },
            })
        self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
    
    def _get_configured_wbddc(self, wbddc_index, wbddc_param_list):
        self._set_wbddc_param_list(wbddc_index, wbddc_param_list, atinit=True)
        return CyberRadio.NDR551_iq_source(
            iq_scale_factor=2**-15,
            host=self.udp_host_name,
            port=wbddc_param_list[0],
            tagged=self.tagged,
            debug=False,
        )
    
    def _get_configured_nbddc(self, nbddc_index, nbddc_param_list):
        self._set_nbddc_param_list(nbddc_index, nbddc_param_list, atinit=True)
        return CyberRadio.NDR551_iq_source(
            iq_scale_factor=2**-15,
            host=self.udp_host_name,
            port=nbddc_param_list[0],
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


