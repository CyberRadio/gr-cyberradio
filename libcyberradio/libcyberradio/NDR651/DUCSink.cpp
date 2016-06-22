/* -*- c++ -*- */
/***************************************************************************
 * \file DUCSink.cpp
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

#include "LibCyberRadio/NDR651/DUCSink.h"
#include "LibCyberRadio/NDR651/TransmitPacketizer.h"
#include <stdarg.h>
#include <iostream>
#include <math.h>


namespace LibCyberRadio
{
	namespace NDR651
	{
		DUCSink::DUCSink(
				  const std::string& name,
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
				  bool use_ring_buffer) :
			Debuggable(debug, name),
			d_name(name),
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
		DUCSink::~DUCSink()
		{
			this->debug("destruction\n");
			if ( d_tx != NULL )
				delete d_tx;
		}

		std::string DUCSink::get_radio_host_name() const
		{
			return d_radio_host_name;
		}

		int DUCSink::get_radio_tcp_port() const
		{
			return d_radio_tcp_port;
		}

		std::vector<std::string> DUCSink::get_tengig_iface_list() const
		{
			return d_tengig_iface_list;
		}

		float DUCSink::get_iq_scale_factor() const
		{
			return d_iq_scale_factor;
		}

		void DUCSink::set_iq_scale_factor(float iq_scale_factor)
		{
			d_iq_scale_factor = iq_scale_factor;
		}

		int DUCSink::get_duc_channel() const
		{
			return d_duc_channel;
		}

		void DUCSink::set_duc_channel(int duc_channel)
		{
			d_duc_channel = duc_channel;
			if ( d_tx != NULL )
				d_tx->setDucChannel(d_duc_channel);
		}

		std::string DUCSink::get_duc_iface_string() const
		{
			return d_duc_iface_string;
		}

		int DUCSink::get_duc_iface_index() const
		{
			return d_duc_iface_index;
		}

		void DUCSink::set_duc_iface_string(const std::string& duc_iface_string)
		{
			d_duc_iface_string = duc_iface_string;
			set_duc_iface_index_from_string();
			if ( d_tx != NULL )
				d_tx->setDucInterface(d_duc_iface_string, d_duc_iface_index);
		}

		int DUCSink::get_duc_rate_index() const
		{
			return d_duc_rate_index;
		}

		void DUCSink::set_duc_rate_index(int duc_rate_index)
		{
			d_duc_rate_index = duc_rate_index;
			if ( d_tx != NULL )
				d_tx->setDucRate(d_duc_rate_index);
		}

		long DUCSink::get_duc_frequency() const
		{
			return d_duc_frequency;
		}

		void DUCSink::set_duc_frequency(long duc_frequency)
		{
			d_duc_frequency = duc_frequency;
			if ( d_tx != NULL )
				d_tx->setDucFreq(d_duc_frequency);
		}

		float DUCSink::get_duc_attenuation() const
		{
			return d_duc_attenuation;
		}

		void DUCSink::set_duc_attenuation(float duc_attenuation)
		{
			d_duc_attenuation = duc_attenuation;
			if ( d_tx != NULL )
				d_tx->setDucAtten(d_duc_attenuation);
		}

		unsigned int DUCSink::get_duc_tx_channels() const
		{
			return d_duc_tx_channels;
		}

		void DUCSink::set_duc_tx_channels(unsigned int duc_tx_channels)
		{
			d_duc_tx_channels = duc_tx_channels;
			if ( d_tx != NULL )
				d_tx->setDucTxChannels(d_duc_tx_channels);
		}

		unsigned int DUCSink::get_duc_tx_frequency() const
		{
			return d_duc_tx_frequency;
		}

		void DUCSink::set_duc_tx_frequency(unsigned int duc_tx_frequency)
		{
			d_duc_tx_frequency = duc_tx_frequency;
			if ( (d_tx != NULL)&&d_config_tx )
				d_tx->setTxFreq(d_duc_tx_frequency);
		}

		unsigned int DUCSink::get_duc_tx_attenuation() const
		{
			return d_duc_tx_attenuation;
		}

		void DUCSink::set_duc_tx_attenuation(unsigned int duc_tx_attenuation)
		{
			d_duc_tx_attenuation = duc_tx_attenuation;
			if ( (d_tx != NULL)&&d_config_tx )
				d_tx->setTxAtten(d_duc_tx_attenuation);
		}

		unsigned int DUCSink::get_duc_stream_id() const
		{
			return d_duc_stream_id;
		}

		void DUCSink::set_duc_stream_id(unsigned int duc_stream_id)
		{
			d_duc_stream_id = duc_stream_id;
			if ( d_tx != NULL )
				d_tx->setStreamId(d_duc_stream_id);
		}

		long DUCSink::get_duc_sample_rate() const
		{
			long ret = 0;
			if ( d_duc_rate_index == 16 )
				ret = 270833;
			else
				ret = (long)(102.4e6 / pow(2, d_duc_rate_index));
			return ret;
		}

		bool DUCSink::start()
		{
			d_tx->start();
			return true;
		}

		bool DUCSink::stop()
		{
			// d_tx -- need Packetizer method to interrupt sub-threads
			d_tx->stop();
			return true;
		}

		int DUCSink::sendFrames(int noutput_items, std::complex<float>* input_items)
		{
			// noutput_items = Number of outgoing VITA 49 frames requested
			// input_items = Array of complex samples.  It should have at least
			//     (noutput_items * SAMPLES_PER_FRAME) elements in it.
			int noutput_items_processed = 0;
			int sample;
			int sample_input_item;
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
					// Fill the sample buffer.  Note that I/Q data is filled in reverse order --
					// Q, then I.
					for (sample = 0; sample < SAMPLES_PER_FRAME; sample++)
					{
						sample_input_item = noutput_items_processed * SAMPLES_PER_FRAME + sample;
						d_sample_buffer[sample * 2] = (short)(input_items[sample_input_item].imag() * d_iq_scale_factor);
						d_sample_buffer[sample * 2 + 1] = (short)(input_items[sample_input_item].real() * d_iq_scale_factor);
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

		void DUCSink::set_radio_params(
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

		void DUCSink::set_duc_iface_index_from_string()
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

	} /* namespace NDR651 */

} /* namespace CyberRadio */

