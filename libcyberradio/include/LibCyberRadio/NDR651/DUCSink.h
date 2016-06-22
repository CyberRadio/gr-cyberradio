/* -*- c++ -*- */
/***************************************************************************
 * \file DUCSink.h
 *
 * \brief Implementation of the digital upconverter (DUC) transmission
 *    sink block for the NDR651.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_DUC_SINK_H
#define INCLUDED_LIBCYBERRADIO_NDR651_DUC_SINK_H

#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/NDR651/TransmitPacketizer.h"
#include <stdio.h>
#include <time.h>
#include <sys/types.h>
#include <vector>
#include <complex>
#include <string>


/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
	/*!
	 * \brief Provides programming elements for controlling the CyberRadio Solutions
	 *    NDR651 radio.
	 */
	namespace NDR651
	{
		/*!
		 * \brief DUC sink class.
		 */
		class DUCSink : public Debuggable
		{
			public:
				/*!
				 * \brief Creates a DUCSink object.
				 * \param name Name to give to this object for debug purposes.
				 * \param radio_host_name The radio host name.  If this is an empty
				 *    string, then the block will not connect to a radio.
				 * \param radio_tcp_port The radio TCP port.
				 * \param tengig_iface_list The list of 10GigE interfaces used by
				 *    the radio.
				 * \param iq_scale_factor Scale factor for converting I/Q data from
				 *    complex input to native sample format.
				 * \param duc_channel The channel number for the DUC in use.
				 * \param duc_iface_string The interface string for the DUC in use.
				 * \param duc_rate_index The rate index for the DUC in use.
				 * \param duc_frequency The frequency offset for the DUC in use.
				 * \param duc_attenuation The attenuation for the DUC in use.
				 * \param duc_tx_channels The transmit channel mask for the DUC in use.
				 * \param duc_tx_frequency The transmit center frequency for the DUC in use.
				 * \param duc_tx_attenuation The transmit attenuation for the DUC in use.
				 * \param duc_stream_id The stream ID/UDP port for the DUC in use.
				 * \param config_tx Whether or not to configure the transmitter.
				 * \param debug Whether the block should produce debug output.  Defaults to
				 *    False.
				 * \param fc_update_rate Number of updates to make per second.
				 * \param use_udp Whether or not to use UDP.
				 * \param use_ring_buffer Whether or not to use a ring buffer.
				 */
				DUCSink(
						  const std::string& name = "DUCSink",
						  /* For the radio in general */
						  const std::string& radio_host_name = "",
						  unsigned int radio_tcp_port = 8617,
						  const std::vector<std::string>& tengig_iface_list = std::vector<std::string>(),
						  float iq_scale_factor = 1.0,
						  /* For an individual DUC on the radio */
						  unsigned int duc_channel = 1,
						  const std::string& duc_iface_string = "eth0",
						  unsigned int duc_rate_index = 0,
						  long duc_frequency = 0,
						  float duc_attenuation = 0,
						  unsigned int duc_tx_channels = 0,
						  unsigned int duc_tx_frequency = 900,
						  unsigned int duc_tx_attenuation = 0,
						  unsigned int duc_stream_id = 40001,
						  bool config_tx = false,
						  bool debug = false,
						  unsigned int fc_update_rate = 20,
						  bool use_udp = false,
						  bool use_ring_buffer = false);
				/*!
				 * \brief Destroys a DUCSink object.
				 */
				~DUCSink();
				/*!
				 * \brief Gets the radio host name.
				 * \return The radio host name.
				 */
				std::string get_radio_host_name() const;
				/*!
				 * \brief Gets the radio TCP port.
				 * \return The port number.
				 */
				int get_radio_tcp_port() const;
				/*!
				 * \brief Gets the 10GigE interface list for the radio.
				 * \return The interface list.
				 */
				std::vector<std::string> get_tengig_iface_list() const;
				/*!
				 * \brief Sets the radio parameters.
				 * \param radio_host_name The radio host name.
				 * \param radio_tcp_port The port number.
				 * \param tengig_iface_list The 10GigE interface list.
				 */
				void set_radio_params(const std::string& radio_host_name,
									  int radio_tcp_port,
									  const std::vector<std::string>& tengig_iface_list);
				/*!
				 * \brief Gets the I/Q scale factor used for the radio.
				 * \return The scale factor.
				 */
				float get_iq_scale_factor() const;
				/*!
				 * \brief Sets the I/Q scale factor used for the radio.
				 * \param iq_scale_factor The scale factor.
				 */
				void set_iq_scale_factor(float iq_scale_factor);
				/*!
				 * \brief Gets the channel number for the DUC
				 *    in use.
				 * \return The channel number.
				 */
				int get_duc_channel() const;
				/*!
				 * \brief Sets the channel number for the DUC
				 *    in use.
				 * \param duc_channel The channel number for the DUC in use.
				 */
				void set_duc_channel(int duc_channel);
				/*!
				 * \brief Gets the interface name for the DUC in use.
				 * \return The interface name.
				 */
				std::string get_duc_iface_string() const;
				/*!
				 * \brief Gets the interface index (one-based) for the DUC
				 *    in use.
				 * \return The interface index.
				 */
				int get_duc_iface_index() const;
				/*!
				 * \brief Sets the interface name for the DUC in use.
				 * \param duc_iface_string The interface string for the DUC in use.
				 */
				void set_duc_iface_string(const std::string& duc_iface_string);
				/*!
				 * \brief Gets the rate index (zero-based) for the DUC
				 *    in use.
				 * \return The rate index.
				 */
				int get_duc_rate_index() const;
				/*!
				 * \brief Sets the rate index (zero-based) for the DUC
				 *    in use.
				 * \param duc_rate_index The rate index for the DUC in use.
				 */
				void set_duc_rate_index(int duc_rate_index);
				/*!
				 * \brief Gets the frequency offset for the DUC
				 *    in use.
				 * \return The frequency offset.
				 */
				long get_duc_frequency() const;
				/*!
				 * \brief Sets the frequency offset for the DUC
				 *    in use.
				 * \param duc_frequency The frequency offset for the DUC in use.
				 */
				void set_duc_frequency(long duc_frequency);
				/*!
				 * \brief Gets the attenuation for the DUC
				 *    in use.
				 * \return The attenuation.
				 */
				float get_duc_attenuation() const;
				/*!
				 * \brief Sets the attenuation for the DUC
				 *    in use.
				 * \param duc_attenuation The attenuation for the DUC in use.
				 */
				void set_duc_attenuation(float duc_attenuation);
				/*!
				 * \brief Gets the transmit channel mask for the DUC
				 *    in use.
				 * \return The transmit channel mask.
				 */
				unsigned int get_duc_tx_channels() const;
				/*!
				 * \brief Sets the transmit channel mask for the DUC
				 *    in use.
				 * \param duc_tx_channels The transmit channel mask for the DUC in use.
				 */
				void set_duc_tx_channels(unsigned int duc_tx_channels);
				/*!
				 * \brief Gets the transmit center frequency (in MHz) for
				 *    the DUC in use.
				 * \return The transmit center frequency.
				 */
				unsigned int get_duc_tx_frequency() const;
				/*!
				 * \brief Sets the transmit center frequency (in MHz) for
				 *    the DUC in use.
				 * \param duc_tx_frequency The transmit center frequency for the DUC in use.
				 */
				void set_duc_tx_frequency(unsigned int duc_tx_frequency);
				/*!
				 * \brief Gets the transmit attenuation (in dB) for the DUC in use.
				 * \return The transmit attenuation.
				 */
				unsigned int get_duc_tx_attenuation() const;
				/*!
				 * \brief Sets the transmit attenuation (in dB) for the DUC in use.
				 * \param duc_tx_attenuation The transmit attenuation for the DUC
				 *    in use.
				 */
				void set_duc_tx_attenuation(unsigned int duc_tx_attenuation);
				/*!
				 * \brief Gets the VITA stream ID for the DUC.
				 * \return The stream ID.
				 */
				unsigned int get_duc_stream_id() const;
				/*!
				 * \brief Sets the VITA stream ID for the DUC.
				 * \param duc_stream_id The stream ID.
				 */
				void set_duc_stream_id(unsigned int duc_stream_id);
				/*!
				 * \brief Gets the sample rate (in Hz) for the DUC in use,
				 *    based on the rate index.
				 * \return The sample rate.
				 */
				long get_duc_sample_rate() const;
				/*!
				 * \brief Starts the sink.
				 */
				bool start();
				/*!
				 * \brief Stops the sink.
				 */
				bool stop();
				/*!
				 * \brief Sends a number of VITA 49 frames.
				 * \param noutput_items Number of VITA 49 frames to send.
				 * \param input_items Pointer to an array of complex samples.  This
				 *    buffer must have enough samples to fill the number of VITA frames
				 *    requested.
				 * \returns The number of VITA frames actually sent.
				 */
				int sendFrames(int noutput_items,
							   std::complex<float>* input_items);

			protected:
				// Get the DUC interface index number from the interface
				// string
				void set_duc_iface_index_from_string();

			protected:
				std::string d_name;
				std::string d_radio_host_name;
				unsigned int d_radio_tcp_port;
				std::vector<std::string> d_tengig_iface_list;
				float d_iq_scale_factor;
				unsigned int d_duc_channel;
				std::string d_duc_iface_string;
				unsigned int d_duc_iface_index;
				unsigned int d_duc_rate_index;
				long d_duc_frequency;
				float d_duc_attenuation;
				unsigned int d_duc_tx_channels;
				unsigned int d_duc_tx_frequency;
				unsigned int d_duc_tx_attenuation;
				unsigned int d_duc_stream_id;
				bool    d_config_tx;
				unsigned int d_fc_update_rate;
				bool d_use_udp;
				bool d_use_ring_buffer;
				TransmitPacketizer* d_tx;
				short d_sample_buffer[SAMPLES_PER_FRAME * 2];
		};

	} // namespace NDR651

} // namespace LibCyberRadio

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_DUC_SINK_H */

