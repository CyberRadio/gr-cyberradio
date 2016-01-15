/* -*- c++ -*- */
/***************************************************************************
 * \file NDR651_duc_sink_impl.cpp
 *
 * \brief Implementation of the digital upconverter (DUC) transmission
 *    sink block for the NDR651.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include <stdarg.h>
#include <iostream>
#include "NDR651_duc_sink_impl.h"
#include <math.h>


namespace gr
{
	namespace CyberRadio
	{
		NDR651_duc_sink::sptr NDR651_duc_sink::make(
				  const std::string& radio_host_name,
				  unsigned int radio_tcp_port,
				  const std::vector<std::string>& tengig_iface_list,
				  float iq_scale_factor,
				  unsigned int duc_channel,
				  const std::string& duc_iface_string,
				  unsigned int duc_rate_index,
				  long duc_frequency,
				  float duc_attenuation,
				  unsigned int duc_tx_channels,
				  unsigned int duc_tx_frequency,
				  unsigned int duc_tx_attenuation,
				  unsigned int duc_stream_id,
				  bool config_tx,
				  bool debug)
		{
		  return gnuradio::get_initial_sptr
			(new NDR651_duc_sink_impl(
					radio_host_name,
					radio_tcp_port,
					tengig_iface_list,
					iq_scale_factor,
					duc_channel,
					duc_iface_string,
					duc_rate_index,
					duc_frequency,
					duc_attenuation,
					duc_tx_channels,
					duc_tx_frequency,
					duc_tx_attenuation,
					duc_stream_id,
					config_tx,
					debug,
					/* fc_update_rate */ 20,
					/* use_udp */ false,
					/* use_ring_buffer */ false));
		}

		/*
		 * The private constructor
		 */
		NDR651_duc_sink_impl::NDR651_duc_sink_impl(
				  const std::string& radio_host_name,
				  unsigned int radio_tcp_port,
				  const std::vector<std::string>& tengig_iface_list,
				  float iq_scale_factor,
				  unsigned int duc_channel,
				  const std::string& duc_iface_string,
				  unsigned int duc_rate_index,
				  long duc_frequency,
				  float duc_attenuation,
				  unsigned int duc_tx_channels,
				  unsigned int duc_tx_frequency,
				  unsigned int duc_tx_attenuation,
				  unsigned int duc_stream_id,
				  bool config_tx,
				  bool debug,
			      unsigned int fc_update_rate,
			      bool use_udp,
			      bool use_ring_buffer)
		  : gr::sync_decimator("[CyberRadio] NDR651 DUC Sink",
				  gr::io_signature::make(1, 1, sizeof(gr_complex)),
				  gr::io_signature::make(0, 0, 0),
				  SAMPLES_PER_FRAME),
			d_radio_host_name(radio_host_name),
			d_radio_tcp_port(radio_tcp_port),
			d_tengig_iface_list(tengig_iface_list),
			d_iq_scale_factor(iq_scale_factor),
			d_duc_channel(duc_channel),
			d_duc_iface_string(duc_iface_string),
			d_duc_iface_index(0),
			d_duc_rate_index(duc_rate_index),
			d_duc_frequency(duc_frequency),
			d_duc_attenuation(duc_attenuation),
			d_duc_tx_channels(duc_tx_channels),
			d_duc_tx_frequency(duc_tx_frequency),
			d_duc_tx_attenuation(duc_tx_attenuation),
			d_duc_stream_id(duc_stream_id),
			d_config_tx(config_tx),
			d_debug(debug),
			d_fc_update_rate(fc_update_rate),
			d_use_udp(use_udp),
			d_use_ring_buffer(use_ring_buffer),
			d_tx(NULL)
		{
			this->debug("construction\n");
			memset(d_sample_buffer, 0, SAMPLES_PER_FRAME * 2 * sizeof(short));
			set_duc_iface_index_from_string();
			// d_tx initial configuration
			d_tx = new NDR651::TransmitPacketizer(
					d_radio_host_name, d_radio_tcp_port,
					d_duc_channel, d_duc_iface_string,
					d_duc_iface_index, d_duc_rate_index,
					d_duc_tx_channels, d_duc_frequency,
					d_duc_attenuation, d_duc_tx_frequency,
					d_duc_tx_attenuation, d_duc_stream_id,
					d_config_tx, d_debug);
		}

		/*
		 * Our virtual destructor.
		 */
		NDR651_duc_sink_impl::~NDR651_duc_sink_impl()
		{
			this->debug("destruction\n");
			if ( d_tx != NULL )
				delete d_tx;
		}

		std::string NDR651_duc_sink_impl::get_radio_host_name() const
		{
			return d_radio_host_name;
		}

		int NDR651_duc_sink_impl::get_radio_tcp_port() const
		{
			return d_radio_tcp_port;
		}

		std::vector<std::string> NDR651_duc_sink_impl::get_tengig_iface_list() const
		{
			return d_tengig_iface_list;
		}

		float NDR651_duc_sink_impl::get_iq_scale_factor() const
		{
			return d_iq_scale_factor;
		}

		void NDR651_duc_sink_impl::set_iq_scale_factor(float iq_scale_factor)
		{
			d_iq_scale_factor = iq_scale_factor;
		}

		int NDR651_duc_sink_impl::get_duc_channel() const
		{
			return d_duc_channel;
		}

		void NDR651_duc_sink_impl::set_duc_channel(int duc_channel)
		{
			d_duc_channel = duc_channel;
			if ( d_tx != NULL )
				d_tx->setDucChannel(d_duc_channel);
		}

		std::string NDR651_duc_sink_impl::get_duc_iface_string() const
		{
			return d_duc_iface_string;
		}

		int NDR651_duc_sink_impl::get_duc_iface_index() const
		{
			return d_duc_iface_index;
		}

		void NDR651_duc_sink_impl::set_duc_iface_string(const std::string& duc_iface_string)
		{
			d_duc_iface_string = duc_iface_string;
			set_duc_iface_index_from_string();
			if ( d_tx != NULL )
				d_tx->setDucInterface(d_duc_iface_string, d_duc_iface_index);
		}

		int NDR651_duc_sink_impl::get_duc_rate_index() const
		{
			return d_duc_rate_index;
		}

		void NDR651_duc_sink_impl::set_duc_rate_index(int duc_rate_index)
		{
			d_duc_rate_index = duc_rate_index;
			if ( d_tx != NULL )
				d_tx->setDucRate(d_duc_rate_index);
		}

		long NDR651_duc_sink_impl::get_duc_frequency() const
		{
			return d_duc_frequency;
		}

		void NDR651_duc_sink_impl::set_duc_frequency(long duc_frequency)
		{
			d_duc_frequency = duc_frequency;
			if ( d_tx != NULL )
				d_tx->setDucFreq(d_duc_frequency);
		}

		float NDR651_duc_sink_impl::get_duc_attenuation() const
		{
			return d_duc_attenuation;
		}

		void NDR651_duc_sink_impl::set_duc_attenuation(float duc_attenuation)
		{
			d_duc_attenuation = duc_attenuation;
			if ( d_tx != NULL )
				d_tx->setDucAtten(d_duc_attenuation);
		}

		unsigned int NDR651_duc_sink_impl::get_duc_tx_channels() const
		{
			return d_duc_tx_channels;
		}

		void NDR651_duc_sink_impl::set_duc_tx_channels(unsigned int duc_tx_channels)
		{
			d_duc_tx_channels = duc_tx_channels;
			if ( d_tx != NULL )
				d_tx->setDucTxChannels(d_duc_tx_channels);
		}

		unsigned int NDR651_duc_sink_impl::get_duc_tx_frequency() const
		{
			return d_duc_tx_frequency;
		}

		void NDR651_duc_sink_impl::set_duc_tx_frequency(unsigned int duc_tx_frequency)
		{
			d_duc_tx_frequency = duc_tx_frequency;
			if ( (d_tx != NULL)&&d_config_tx )
				d_tx->setTxFreq(d_duc_tx_frequency);
		}

		unsigned int NDR651_duc_sink_impl::get_duc_tx_attenuation() const
		{
			return d_duc_tx_attenuation;
		}

		void NDR651_duc_sink_impl::set_duc_tx_attenuation(unsigned int duc_tx_attenuation)
		{
			d_duc_tx_attenuation = duc_tx_attenuation;
			if ( (d_tx != NULL)&&d_config_tx )
				d_tx->setTxAtten(d_duc_tx_attenuation);
		}

		unsigned int NDR651_duc_sink_impl::get_duc_stream_id() const
		{
			return d_duc_stream_id;
		}

		void NDR651_duc_sink_impl::set_duc_stream_id(unsigned int duc_stream_id)
		{
			d_duc_stream_id = duc_stream_id;
			if ( d_tx != NULL )
				d_tx->setStreamId(d_duc_stream_id);
		}

		long NDR651_duc_sink_impl::get_duc_sample_rate() const
		{
			long ret = 0;
			if ( d_duc_rate_index == 16 )
				ret = 270833;
			else
				ret = (long)(102.4e6 / pow(2, d_duc_rate_index));
			return ret;
		}

		bool NDR651_duc_sink_impl::start()
		{
			d_tx->start();
			return true;
		}

		bool NDR651_duc_sink_impl::stop()
		{
			// d_tx -- need Packetizer method to interrupt sub-threads
			d_tx->stop();
			return true;
		}

		int NDR651_duc_sink_impl::work(int noutput_items,
				  gr_vector_const_void_star &input_items,
				  gr_vector_void_star &output_items)
		{
			// noutput_items = Number of outgoing VITA 49 frames requested
			// input_items.size() = Number of inputs
			// input_items[0] = Pointer to input 0's data buffer.  The
			//     buffer has (noutput_items * SAMPLES_PER_FRAME) gr_complex
			//     values in it.
			// output_items = Not used because this is a sink object.
			// Do <+signal processing+>
			int noutput_items_processed = 0;
			const gr_complex* pSampleBase = (const gr_complex*)input_items[0];
			const gr_complex* pSample;
			int sample;
			bool sending = true;
			// If the transmit packetizer is ready to receive --
			if ( (d_tx != NULL) && d_tx->isReadyToReceive() )
			{
				// While the packetizer stays ready to receive AND we can still
				// process outgoing items:
				while ( d_tx->isReadyToReceive() &&
						sending &&
						(noutput_items_processed < noutput_items) )
				{
					// Fill the sample buffer
					for (sample = 0; sample < SAMPLES_PER_FRAME; sample++)
					{
						pSample = pSampleBase + noutput_items_processed * SAMPLES_PER_FRAME + sample;
						d_sample_buffer[sample * 2] = (short)(pSample->imag() * d_iq_scale_factor);
						d_sample_buffer[sample * 2 + 1] = (short)(pSample->real() * d_iq_scale_factor);
					}
					// Send data
					int samplesSent = d_tx->sendFrame(d_sample_buffer);
					if ( samplesSent > 0 )
						noutput_items_processed++;
					else
						sending = false;
				}
			}
			// If the packetizer wasn't connected at the start, go ahead and
			// consume all of the input items so we don't block up anything
			// supplying our input sample data.
			else
			{
				noutput_items_processed = noutput_items;
			}
			return noutput_items_processed;
		}

		void NDR651_duc_sink_impl::set_radio_params(
				  const std::string& radio_host_name,
	              int radio_tcp_port,
				  const std::vector<std::string>& tengig_iface_list)
		{
			this->debug("setting radio parameters\n");
			d_radio_host_name = radio_host_name;
			d_radio_tcp_port = radio_tcp_port;
			d_tengig_iface_list = tengig_iface_list;
			set_duc_iface_index_from_string();
			if ( d_tx != NULL )
			{
				d_tx->setRadioParameters(d_radio_host_name, d_radio_tcp_port);
				d_tx->setDucInterface(d_duc_iface_string, d_duc_iface_index);
				d_tx->setDucParameters(d_duc_iface_index, d_duc_rate_index,
									  d_duc_tx_channels, d_duc_frequency,
									  d_duc_attenuation, d_duc_tx_frequency,
									  d_duc_attenuation, d_duc_stream_id);
			}
		}

		void NDR651_duc_sink_impl::set_duc_iface_index_from_string()
		{
			d_duc_iface_index = 0;
			for (int idx = 1; idx <= (int)d_tengig_iface_list.size(); idx++)
			{
				if ( d_tengig_iface_list[idx-1] == d_duc_iface_string )
				{
					d_duc_iface_index = idx;
					break;
				}
			}
		}

		int NDR651_duc_sink_impl::debug(const char *format, ...)
		{
			int ret = 0;
			if (d_debug)
			{
				ret = fprintf(stderr, "[%s] ", this->name().c_str());
				if (ret >= 0)
				{
					va_list ap;
					va_start(ap, format);
					ret = vfprintf(stderr, format, ap);
					va_end(ap);
				}
			}
			return ret;
		}


	} /* namespace CyberRadio */
} /* namespace gr */

