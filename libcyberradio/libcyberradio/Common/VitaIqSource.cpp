/* -*- c++ -*- */
/***************************************************************************
 * \file VitaIqSource.cpp
 *
 * \brief Implementation of a generic VITA 49-compatible I/Q data source
 *    block.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "LibCyberRadio/Common/VitaIqSource.h"


namespace LibCyberRadio
{
	VitaIqSource::VitaIqSource(const std::string& name,
		       	   	   	   	   int vita_type,
			   	   	   	   	   size_t payload_size,
			   	   	   	   	   size_t vita_header_size,
			   	   	   	   	   size_t vita_tail_size,
			   	   	   	   	   bool byte_swapped,
			   	   	   	   	   bool iq_swapped,
			   	   	   	   	   const std::string& host,
			   	   	   	   	   unsigned short port,
			   	   	   	   	   bool debug) :
			  Debuggable(debug, name),
			  d_name(name),
			  d_vita_type(vita_type),
			  d_payload_size(payload_size),
			  d_vita_header_size(vita_header_size),
			  d_vita_tail_size(vita_tail_size),
			  d_byte_swapped(byte_swapped),
			  d_iq_swapped(iq_swapped),
			  d_host(host),
			  d_port(port),
			  d_packet_size(0)
	{
		this->debug("construction\n");
		// Determine packet size
		d_packet_size = (vita_type == 0 ? payload_size : vita_header_size + payload_size + vita_tail_size);
		// Create UDP port for collecting data
		connect_udp_port();
	}

	/*
	 * Our virtual destructor.
	 */
	VitaIqSource::~VitaIqSource()
	{
		this->debug("destruction\n");
		// Destroy/disconnect UDP port for collecting data
		disconnect_udp_port();
	}

	int VitaIqSource::getPackets(int noutput_items, Vita49PacketVector& output_items)
	{
		int noutput_items_processed = 0;
		bool got_data_on_loop = false;
		// Check to see if the UDP port is available for reading
		if ( d_udp_port_mtx.try_lock() )
		{
			// Get as many packets as we can, up to the maximum number requested.
			do
			{
				got_data_on_loop = false;
				// Get data from UDP port if it's available
				d_udp_port->read_data();
				if ( d_udp_port->is_packet_ready() )
				{
					// Handle disposition of the new packet object depending on whether or not
                    // the output vector has been pre-allocated
					if ( noutput_items_processed < (int)output_items.size() )
					{
						output_items[noutput_items_processed] = Vita49Packet(
								        d_vita_type,
										d_payload_size,
										d_vita_header_size,
										d_vita_tail_size,
										d_byte_swapped,
										d_iq_swapped,
										(unsigned char*)(d_udp_port->recv_buffer),
										d_packet_size);
					}
					else
					{
						output_items.push_back( Vita49Packet(
								        d_vita_type,
										d_payload_size,
										d_vita_header_size,
										d_vita_tail_size,
										d_byte_swapped,
										d_iq_swapped,
										(unsigned char*)(d_udp_port->recv_buffer),
										d_packet_size) );
					}
					// Increment the items processed counter
					noutput_items_processed++;
					// Reset the UDP port buffer
					d_udp_port->clear_buffer();
					// Set the got data on loop flag
					got_data_on_loop = true;
				}
			} while ( got_data_on_loop && (noutput_items_processed < noutput_items) );
			d_udp_port_mtx.unlock();
	    }
		return noutput_items_processed;
	}

	int VitaIqSource::getPacketSize() const
	{
		return d_packet_size;
	}

	bool VitaIqSource::isByteSwapped() const
	{
		return d_byte_swapped;
	}

	bool VitaIqSource::isIqSwapped() const
	{
		return d_iq_swapped;
	}

	size_t VitaIqSource::getPayloadSize() const
	{
		return d_payload_size;
	}

	size_t VitaIqSource::getVitaHeaderSize() const
	{
		return d_vita_header_size;
	}

	size_t VitaIqSource::getVitaTailSize() const
	{
		return d_vita_tail_size;
	}

	int VitaIqSource::getVitaType() const
	{
		return d_vita_type;
	}

	void VitaIqSource::recalc_packet_size()
	{
		// Determine packet size
		d_packet_size = (d_vita_type == 0 ? d_payload_size :
				d_vita_header_size + d_payload_size + d_vita_tail_size);
		// Reconnect the UDP port
		disconnect_udp_port();
		connect_udp_port();
	}

	void VitaIqSource::connect_udp_port()
	{
		d_udp_port_mtx.lock();
		// Create UDP port for collecting data
		this->debug("connect udp %s/%d\n", d_host.c_str(), d_port);
		d_udp_port = new VitaIqUdpPort(d_host, d_port, d_packet_size, d_debug);
		this->debug("-- connect result: %d\n", d_udp_port->connected);
		d_udp_port_mtx.unlock();
	}

	void VitaIqSource::disconnect_udp_port()
	{
		d_udp_port_mtx.lock();
		// Destroy UDP port for collecting data
		this->debug("disconnect udp %s/%d\n", d_host.c_str(), d_port);
		delete d_udp_port;
		d_udp_port = NULL;
		d_udp_port_mtx.unlock();
	}


} /* namespace LibCyberRadio */

