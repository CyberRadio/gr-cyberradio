#!/usr/bin/env python
###############################################################
# \package CyberRadio.NDR651_sink
# 
# \brief I/Q data transmission sink block using the NDR651 radio
#
# \author DA
# 
# \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.  
#    All rights reserved.
#
###############################################################

from gnuradio import gr
from gnuradio.filter import firdes
import CyberRadio
import sys

TX_PARAM_ENABLE = 0
TX_PARAM_FREQ = 1
TX_PARAM_ATTEN = 2
DUC_PARAM_IFACE = 0
DUC_PARAM_RATE = 1
DUC_PARAM_FREQ = 2 
DUC_PARAM_ATTEN = 3 
DUC_PARAM_TXCHANS = 4
DUC_PARAM_STREAM = 5

##
# \class NDR651_sink
# \ingroup CyberRadioNDR651
# \brief I/Q data transmission sink block using the NDR651 radio.
#
# The NDR651_sink object supplies wideband DUC inputs, as indicated 
# by the Number of WBDUCs setting. Any inputs supplied by this block are 
# optional, so the user does not need to connect them if they are not 
# being used.  The NDR651_sink object also supplies a character-stream 
# output for collecting logging data from the underlying driver interface.
#
# Transmitters and WBDUCs are configured via parameter lists.  Parameter 
# lists are standard Python lists, formatted as follows:
# \li A transmitter parameter list contains the following elements: 
#    [transmitter enabled flag, transmitter frequency (MHz), transmitter 
#    attenuation (dB)]. 
# \li A WBDUC parameter list contains the following elements: [10GigE
#    interface to use, DUC rate index, DUC frequency offset (Hz), 
#    DUC attenuation (dB), transmitter index, stream ID/UDP port].
# 
# \note The parameter list scheme is a workaround to get around the
#    (undocumented) parameter limit that GNU Radio Companion 
#    silently imposes.
# 
class NDR651_sink(gr.hier_block2):

    ##
    # \brief Constructs an NDR651_sink object.
    #
    # \param verbose_mode Verbose mode for logging.
    # \param radio_host_name Host name for the radio.
    # \param radio_host_port TCP port to use for communicating with the 
    #    radio.
    # \param tengig_iface_list The list of 10GigE interface names used
    #    for the radio.
    # \param iq_scale_factor The scale factor to use for all WBDUCs on 
    #    the radio.
    # \param num_transmitters Number of transmitters to use.
    # \param transmitter1_param_list Transmitter 1 parameter list. 
    # \param transmitter2_param_list Transmitter 2 parameter list.
    # \param num_wbducs Number of WBDUCs to use.
    # \param wbduc1_param_list WBDUC 1 parameter list. 
    # \param wbduc2_param_list WBDUC 2 parameter list.
    # \param wbduc3_param_list WBDUC 3 parameter list.
    # \param wbduc4_param_list WBDUC 4 parameter list.
    # \param wbduc5_param_list WBDUC 5 parameter list.
    # \param wbduc6_param_list WBDUC 6 parameter list.
    # \param wbduc7_param_list WBDUC 7 parameter list.
    # \param wbduc8_param_list WBDUC 8 parameter list.
    # \param debug Whether the block should produce debug output.
    def __init__(self, 
                 verbose_mode=True, 
                 radio_host_name="ndr651", 
                 radio_host_port=8617, 
                 tengig_iface_list=['eth10', 'eth11'], 
                 iq_scale_factor=2**15,
                 num_transmitters=1,
                 transmitter1_param_list=[False, 900, 0],
                 transmitter2_param_list=[False, 900, 0],
                 num_wbducs=1, 
                 wbduc1_param_list=["eth10", 0, 0, 0, 1, 40001], 
                 wbduc2_param_list=["eth10", 0, 0, 0, 1, 40002],
                 wbduc3_param_list=["eth10", 0, 0, 0, 1, 40003],
                 wbduc4_param_list=["eth10", 0, 0, 0, 1, 40004],
                 wbduc5_param_list=["eth10", 0, 0, 0, 1, 40005],
                 wbduc6_param_list=["eth10", 0, 0, 0, 1, 40006],
                 wbduc7_param_list=["eth10", 0, 0, 0, 1, 40007],
                 wbduc8_param_list=["eth10", 0, 0, 0, 1, 40008],
                 debug=False,
                 ):
        gr.hier_block2.__init__(
            self, "[CyberRadio] NDR651 Sink",
            gr.io_signaturev(num_wbducs, num_wbducs, 
                             num_wbducs * [gr.sizeof_gr_complex*1]),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )
        self.transmitter_param_lists = {}
        self.wbduc_sources = {}
        self.wbduc_param_lists = {}
        self.verbose_mode = verbose_mode
        self.radio_host_name = radio_host_name
        self.radio_host_port = radio_host_port
        self.tengig_iface_list = tengig_iface_list
        self.iq_scale_factor = iq_scale_factor
        self.num_transmitters = num_transmitters
        self.transmitter_param_lists[1] = transmitter1_param_list
        self.transmitter_param_lists[2] = transmitter2_param_list
        self.num_wbducs = num_wbducs
        self.wbduc_param_lists[1] = wbduc1_param_list
        self.wbduc_param_lists[2] = wbduc2_param_list
        self.wbduc_param_lists[3] = wbduc3_param_list
        self.wbduc_param_lists[4] = wbduc4_param_list
        self.wbduc_param_lists[5] = wbduc5_param_list
        self.wbduc_param_lists[6] = wbduc6_param_list
        self.wbduc_param_lists[7] = wbduc7_param_list
        self.wbduc_param_lists[8] = wbduc8_param_list
        self.debug = debug
        self.CyberRadio_file_like_object_source_0 = CyberRadio.file_like_object_source()
        self.CyberRadio_NDR_driver_interface_0 = CyberRadio.NDR_driver_interface(
            radio_type="ndr651",
            verbose=verbose_mode,
            log_file=self.CyberRadio_file_like_object_source_0,
            connect_mode="tcp",
            host_name=radio_host_name,
            host_port=radio_host_port,
        )
        self.connect((self.CyberRadio_file_like_object_source_0, 0), (self, 0))
        for transmitter_index in xrange(1, self.num_transmitters + 1, 1):
            self._set_transmitter_param_list(transmitter_index, 
                                             self.transmitter_param_lists[transmitter_index], 
                                             True)
        for wbduc_index in xrange(1, self.num_wbducs + 1, 1):
            self.wbduc_sources[wbduc_index] = self._get_configured_wbduc(
                                                    wbduc_index, 
                                                    self.wbduc_param_lists[wbduc_index])
            self.connect((self, wbduc_index-1), (self.wbduc_sources[wbduc_index], 0))

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
    # \brief Sets the radio parameters.
    # \param radio_host_name The radio host name.
    # \param radio_tcp_port The radio TCP port.
    # \param tengig_iface_list The 10GigE interface list.
    def set_radio_params(self, radio_host_name, radio_tcp_port, 
                         tengig_iface_list):
        for wbduc_index in self.wbduc_sources:
            self.wbduc_sources[wbduc_index].set_radio_params(radio_host_name, 
                                                             radio_tcp_port, 
                                                             tengig_iface_list)
        pass
    
    ##
    # \brief Sets the I/Q scale factor.
    # \param iq_scale_factor The scale factor to use for all WBDUCs on 
    #    the radio.
    def set_iq_scale_factor(self, iq_scale_factor):
        for wbduc_index in self.wbduc_sources:
            self.wbduc_sources[wbduc_index].set_iq_scale_factor(iq_scale_factor)
        pass
    
    ##
    # \brief Gets the number of transmitters in use.
    # \return The the number of transmitters in use.
    def get_num_transmitters(self):
        return self.num_transmitters

    ##
    # \brief Gets the parameter list for Transmitter 1.
    # \return The transmitter parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_transmitter1_param_list(self):
        return self.transmitter_param_lists[1]

    ##
    # \brief Sets the parameter list for Transmitter 1.
    # \param param_list The transmitter parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_transmitter1_param_list(self, param_list):
        self._set_transmitter_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for Transmitter 2.
    # \return The transmitter parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_transmitter2_param_list(self):
        return self.transmitter_param_lists[2]

    ##
    # \brief Sets the parameter list for Transmitter 2.
    # \param param_list The transmitter parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_transmitter2_param_list(self, param_list):
        self._set_transmitter_param_list(2, param_list)

    ##
    # \brief Gets the number of WBDUCs in use.
    # \return The the number of WBDUCs in use.
    def get_num_wbducs(self):
        return self.num_wbducs

    ##
    # \brief Gets the parameter list for WBDUC 1.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc1_param_list(self):
        return self.wbduc_param_lists[1]

    ##
    # \brief Sets the parameter list for WBDUC 1.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc1_param_list(self, param_list):
        self._set_wbduc_param_list(1, param_list)

    ##
    # \brief Gets the parameter list for WBDUC 2.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc2_param_list(self):
        return self.wbduc_param_lists[2]

    ##
    # \brief Sets the parameter list for WBDUC 2.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc2_param_list(self, param_list):
        self._set_wbduc_param_list(2, param_list)

    ##
    # \brief Gets the parameter list for WBDUC 3.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc3_param_list(self):
        return self.wbduc_param_lists[3]

    ##
    # \brief Sets the parameter list for WBDUC 3.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc3_param_list(self, param_list):
        self._set_wbduc_param_list(3, param_list)

    ##
    # \brief Gets the parameter list for WBDUC 4.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc4_param_list(self):
        return self.wbduc_param_lists[4]

    ##
    # \brief Sets the parameter list for WBDUC 4.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc4_param_list(self, param_list):
        self._set_wbduc_param_list(4, param_list)

    ##
    # \brief Gets the parameter list for WBDUC 5.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc5_param_list(self):
        return self.wbduc_param_lists[5]

    ##
    # \brief Sets the parameter list for WBDUC 5.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc5_param_list(self, param_list):
        self._set_wbduc_param_list(5, param_list)

    ##
    # \brief Gets the parameter list for WBDUC 6.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc6_param_list(self):
        return self.wbduc_param_lists[6]

    ##
    # \brief Sets the parameter list for WBDUC 6.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc6_param_list(self, param_list):
        self._set_wbduc_param_list(6, param_list)

    ##
    # \brief Gets the parameter list for WBDUC 7.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc7_param_list(self):
        return self.wbduc_param_lists[7]

    ##
    # \brief Sets the parameter list for WBDUC 7.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc7_param_list(self, param_list):
        self._set_wbduc_param_list(7, param_list)

    ##
    # \brief Gets the parameter list for WBDUC 8.
    # \return The WBDUC parameter list.  See the class documentation for 
    #    the meaning of the values returned in the list.
    def get_wbduc8_param_list(self):
        return self.wbduc_param_lists[8]

    ##
    # \brief Sets the parameter list for WBDUC 8.
    # \param param_list The WBDUC parameter list.  See the class 
    #    documentation for the values to be provided in the list.
    def set_wbduc8_param_list(self, param_list):
        self._set_wbduc_param_list(8, param_list)

    ##
    # \brief Gets the nominal (expected) sample rate for a given WBDUC.
    # \param wbduc_index The WBDUC index.
    # \return The sample rate, in samples per second.
    def get_wbduc_nominal_sample_rate(self, wbduc_index):
        rate_index = self.CyberRadio_NDR_driver_interface_0.getConfiguration()['ducConfiguration']['wideband'][wbduc_index]['rateIndex']
        rate_set = self.CyberRadio_NDR_driver_interface_0.getWbducRateSet()
        return rate_set.get(rate_index, 0)
    
    def _set_transmitter_param_list(self, transmitter_index, transmitter_param_list, atinit=False):
        self._debug("[DBG] TX PARAM LIST UPDATE index=", transmitter_index, \
                    " params=", transmitter_param_list)
        # We have to be careful with configuring transmitter power-up
        # states because fiddling with these settings can cause DUC 
        # settings to get lost on the radio.  To get around this, we
        # configure all transmitters to be enabled, but we internally 
        # modify the TX channels bitmask for each DUC to reference only
        # transmitters that are explicity enabled by the user.
        self.transmitter_param_lists[transmitter_index] = transmitter_param_list
        if atinit:
            configDict = {
              "txConfiguration": {
                    transmitter_index: {
                        'enable': 1,
                        'frequency': transmitter_param_list[TX_PARAM_FREQ] * 1e6,
                        'attenuation': transmitter_param_list[TX_PARAM_ATTEN],
                    },
              },
            }
            self.CyberRadio_NDR_driver_interface_0.setConfiguration(configDict)
        else:
            for wbduc_index in self.wbduc_sources:
                self._debug("[DBG] -- DUC index=", wbduc_index)
                transmitter_bit = (1 << (transmitter_index-1))
                self._debug("[DBG]    -- TX bit=", transmitter_bit)
                self._debug("[DBG]    -- DUC TX bitmask=", self.wbduc_param_lists[wbduc_index][DUC_PARAM_TXCHANS])
                self._debug("[DBG]    -- TX enabled bitmask=", self._get_transmitters_enabled_bitmask())
                duc_tx_channels = self.wbduc_param_lists[wbduc_index][DUC_PARAM_TXCHANS] & self._get_transmitters_enabled_bitmask()
                self.wbduc_sources[wbduc_index].set_duc_tx_channels(duc_tx_channels)
                if duc_tx_channels & transmitter_bit == transmitter_bit:
                    self._debug("[DBG]    -- UPDATE DUC")
                    self.wbduc_sources[wbduc_index].set_duc_tx_frequency(transmitter_param_list[TX_PARAM_FREQ])
                    self.wbduc_sources[wbduc_index].set_duc_tx_attenuation(transmitter_param_list[TX_PARAM_ATTEN])
                    self._debug("[DBG]    -- UPDATE DUC COMPLETE")
        self._debug("[DBG] TX PARAM LIST UPDATE COMPLETE")
                
    def _set_wbduc_param_list(self, wbduc_index, wbduc_param_list, atinit=False):
        self._debug("[DBG] DUC PARAM LIST UPDATE index=", wbduc_index, \
                    " params=", wbduc_param_list)
        self.wbduc_param_lists[wbduc_index] = wbduc_param_list
        self.wbduc_sources[wbduc_index].set_duc_iface_string(wbduc_param_list[DUC_PARAM_IFACE])
        self.wbduc_sources[wbduc_index].set_duc_rate_index(wbduc_param_list[DUC_PARAM_RATE])
        self.wbduc_sources[wbduc_index].set_duc_frequency(wbduc_param_list[DUC_PARAM_FREQ])
        self.wbduc_sources[wbduc_index].set_duc_attenuation(wbduc_param_list[DUC_PARAM_ATTEN])
        duc_tx_channels = wbduc_param_list[DUC_PARAM_TXCHANS] & self._get_transmitters_enabled_bitmask()
        self.wbduc_sources[wbduc_index].set_duc_tx_channels(duc_tx_channels)
        self.wbduc_sources[wbduc_index].set_duc_stream_id(wbduc_param_list[DUC_PARAM_STREAM])
        if duc_tx_channels & 1 == 1:
            self.wbduc_sources[wbduc_index].set_duc_tx_frequency(self.transmitter_param_lists[1][TX_PARAM_FREQ])
            self.wbduc_sources[wbduc_index].set_duc_tx_attenuation(self.transmitter_param_lists[1][TX_PARAM_ATTEN])
        if duc_tx_channels & 2 == 2:
            self.wbduc_sources[wbduc_index].set_duc_tx_frequency(self.transmitter_param_lists[2][TX_PARAM_FREQ])
            self.wbduc_sources[wbduc_index].set_duc_tx_attenuation(self.transmitter_param_lists[2][TX_PARAM_ATTEN])
        self._debug("[DBG] DUC PARAM LIST UPDATE COMPLETE")
    
    def _get_configured_wbduc(self, wbduc_index, wbduc_param_list):
        self._debug("[DBG] DUC SINK SPAWN index=", wbduc_index, \
                    " params=", wbduc_param_list)
        self.wbduc_param_lists[wbduc_index] = wbduc_param_list
        duc_tx_frequency = 0
        duc_tx_attenuation = 0
        duc_tx_channels = wbduc_param_list[DUC_PARAM_TXCHANS] & self._get_transmitters_enabled_bitmask()
        if (duc_tx_channels & 1) == 1:
            duc_tx_frequency = self.transmitter_param_lists[1][TX_PARAM_FREQ]
            duc_tx_attenuation = self.transmitter_param_lists[1][TX_PARAM_ATTEN]
        if (duc_tx_channels & 2) == 2:
            duc_tx_frequency = self.transmitter_param_lists[2][TX_PARAM_FREQ]
            duc_tx_attenuation = self.transmitter_param_lists[2][TX_PARAM_ATTEN]
        return CyberRadio.NDR651_duc_sink(
            radio_host_name=self.radio_host_name, 
            radio_tcp_port=self.radio_host_port, 
            tengig_iface_list=self.tengig_iface_list,
            iq_scale_factor=self.iq_scale_factor,
            duc_channel=wbduc_index, 
            duc_iface_string=wbduc_param_list[DUC_PARAM_IFACE], 
            duc_rate_index=wbduc_param_list[DUC_PARAM_RATE], 
            duc_frequency=wbduc_param_list[DUC_PARAM_FREQ], 
            duc_attenuation=wbduc_param_list[DUC_PARAM_ATTEN], 
            duc_tx_channels=duc_tx_channels, 
            duc_tx_frequency=duc_tx_frequency,
            duc_tx_attenuation=duc_tx_attenuation,
            duc_stream_id=wbduc_param_list[DUC_PARAM_STREAM],
            config_tx=True,
            debug=self.debug, 
        )
        
    def _get_transmitters_enabled_bitmask(self):
        ret = 0
        for transmitter_index in xrange(1, self.num_transmitters + 1, 1):
            ret += ( (1 << (transmitter_index - 1)) if self.transmitter_param_lists[transmitter_index][0] else 0 )
            pass
        return ret
    
    def _debug(self, *args):
        if self.debug:
            for arg in args:
                self.CyberRadio_file_like_object_source_0.write(str(arg))
            self.CyberRadio_file_like_object_source_0.write("\n")
            self.CyberRadio_file_like_object_source_0.flush()
    

