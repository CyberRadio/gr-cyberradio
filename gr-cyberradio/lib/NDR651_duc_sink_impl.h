/* -*- c++ -*- */
/***************************************************************************
 * \file NDR651_duc_sink_impl.h
 *
 * \brief Implementation of the digital upconverter (DUC) transmission
 *    sink block for the NDR651.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_DUC_SINK_IMPL_H
#define INCLUDED_CYBERRADIO_NDR651_DUC_SINK_IMPL_H

#include "CyberRadio/NDR651_duc_sink.h"
#include <stdio.h>
#include <time.h>
#include <sys/types.h>
#include "CyberRadio/NDR651/TransmitPacketizer.h"


namespace gr
{
	namespace CyberRadio
	{
		class NDR651_duc_sink_impl : public NDR651_duc_sink
		{
			public:
				NDR651_duc_sink_impl(
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
				~NDR651_duc_sink_impl();
				std::string get_radio_host_name() const;
				int get_radio_tcp_port() const;
				std::vector<std::string> get_tengig_iface_list() const;
				float get_iq_scale_factor() const;
				void set_iq_scale_factor(float iq_scale_factor);
				int get_duc_channel() const;
				void set_duc_channel(int duc_channel);
				std::string get_duc_iface_string() const;
				int get_duc_iface_index() const;
				void set_duc_iface_string(const std::string& duc_iface_string);
				int get_duc_rate_index() const;
				void set_duc_rate_index(int duc_rate_index);
				long get_duc_frequency() const;
				void set_duc_frequency(long duc_frequency);
				float get_duc_attenuation() const;
				void set_duc_attenuation(float duc_attenuation);
				unsigned int get_duc_tx_channels() const;
				void set_duc_tx_channels(unsigned int duc_tx_channels);
				unsigned int get_duc_tx_frequency() const;
				void set_duc_tx_frequency(unsigned int duc_tx_frequency);
				unsigned int get_duc_tx_attenuation() const;
				void set_duc_tx_attenuation(unsigned int duc_tx_attenuation);
				unsigned int get_duc_stream_id() const;
				void set_duc_stream_id(unsigned int duc_stream_id);
				long get_duc_sample_rate() const;

				// OVERRIDE
				// Performs initialization of the block before data streaming
				// begins
				bool start();
				// OVERRIDE
				// Performs shutdown on the block when data streaming ends
				bool stop();
				// OVERRIDE
				// Where all the action really happens
				int work(int noutput_items,
				         gr_vector_const_void_star &input_items,
				         gr_vector_void_star &output_items);

			protected:
				// Radio parameter setting -- we're not exposing the
				// capability to switch radios on the fly yet, so this is
				// protected for now.
				void set_radio_params(const std::string& radio_host_name,
						              int radio_tcp_port,
									  const std::vector<std::string>& tengig_iface_list);
				// Get the DUC interface index number from the interface
				// string
				void set_duc_iface_index_from_string();
				// Debug output helper
				int debug(const char *format, ...);

			protected:
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
				bool    d_debug;
				unsigned int d_fc_update_rate;
				bool d_use_udp;
				bool d_use_ring_buffer;
				NDR651::TransmitPacketizer* d_tx;
				short d_sample_buffer[SAMPLES_PER_FRAME * 2];
		};

	} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NDR651_DUC_SINK_IMPL_H */

