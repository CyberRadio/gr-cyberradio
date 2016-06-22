/* -*- c++ -*- */
/***************************************************************************
 * \file VitaIqSource.h
 *
 * \brief Generic VITA 49-compatible I/Q data source block.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */


#ifndef INCLUDED_LIBCYBERRADIO_VITAIQSOURCE_H_
#define INCLUDED_LIBCYBERRADIO_VITAIQSOURCE_H_

#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/Common/Vita49Packet.h"
#include "LibCyberRadio/Common/VitaIqUdpPort.h"
#include <boost/thread.hpp>
#include <string>
#include <vector>


/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
	typedef std::vector<Vita49Packet> Vita49PacketVector;

	/*!
	 * \ingroup foo
	 *
	 * \brief A generic VITA 49-compatible I/Q data source object.
	 *
	 * \details
	 * The vita_iq_source object provides VITA 49 or raw I/Q data coming
	 * from an NDR-class radio via UDP.
	 *
	 * This class is designed to be as flexible as possible in dealing
	 * with data streams, since each NDR-class radio varies in how it
	 * packages data streams.
	 *
	 */
	class VitaIqSource : public Debuggable
	{
		public:

			/*!
			 * \brief Creates a VitaIqSource object.
			 *
			 * \param name An identifying name for this source object.
			 * \param vita_type The VITA 49 enable option value.  The range of valid
			 *     values depends on the radio, but 0 always disables VITA 49
			 *     formatting.  In that case, the data format is raw I/Q.
			 * \param payload_size The VITA 49 or I/Q payload size for the radio, in
			 *     bytes.  If VITA 49 output is disabled, then this parameter provides
			 *     the total size of all raw I/Q data transmitted in a single packet.
			 * \param vita_header_size The VITA 49 header size for the radio, in bytes.
			 *     If VITA 49 output is disabled, then this parameter is ignored.
			 * \param vita_tail_size The VITA 49 tail size for the radio, in bytes.
			 *     If VITA 49 output is disabled, then this parameter is ignored.
			 * \param byte_swapped Whether the bytes in the packet are swapped (with
			 *     respect to the endianness employed by the host operating system).
			 * \param iq_swapped Whether I and Q data in the payload are swapped.
			 * \param host The IP address or host name to bind listening UDP ports
			 *    on.  Specify this as "0.0.0.0" to listen on all network interfaces.
			 * \param port The UDP port number to listen on.
			 * \param debug Whether the block should produce debug output.  Defaults to
			 *    False.
			 */
			VitaIqSource(const std::string& name = "VitaIqSource",
					     int vita_type = 0,
						 size_t payload_size = 8192,
						 size_t vita_header_size = 0,
						 size_t vita_tail_size = 0,
						 bool byte_swapped = false,
						 bool iq_swapped = false,
						 const std::string& host = "0.0.0.0",
						 unsigned short port = 0,
						 bool debug = false);
			/*!
			 * \brief Destroys a vita_iq_source object.
			 */
			virtual ~VitaIqSource();
			/*!
			 * \brief Gets VITA 49 or I/Q data packets.
			 *
			 * \param noutput_items Number of packets requested.
			 * \param output_items Vector of output packets.
			 *
			 * \return The number of output packets actually retrieved.
			 */
			virtual int getPackets(int noutput_items, Vita49PacketVector& output_items);
			/*!
			 * \brief Gets the VITA 49 or I/Q packet size.
			 *
			 * \return The packet size.
			 */
			virtual int getPacketSize() const;
			/*!
			 * \brief Gets the byte-swapping state.
			 *
			 * \return True if the packet is byte-swapped, false otherwise.
			 */
			bool isByteSwapped() const;
			/*!
			 * \brief Gets the I/Q-swapping state.
			 *
			 * \return True if the packet is I/Q-swapped, false otherwise.
			 */
			bool isIqSwapped() const;
			/*!
			 * \brief Gets the payload size.
			 *
			 * \return The payload size.
			 */
			size_t getPayloadSize() const;
			/*!
			 * \brief Gets the VITA 49 frame header size.
			 *
			 * \return The header size.
			 */
			size_t getVitaHeaderSize() const;
			/*!
			 * \brief Gets the VITA 49 frame trailer size.
			 *
			 * \return The trailer size.
			 */
			size_t getVitaTailSize() const;
			/*!
			 * \brief Gets the VITA type.
			 *
			 * Supported VITA types vary by radio, but VITA type 0 always represents
			 *    raw (unframed) I/Q data.
			 *
			 * \return The VITA type.
			 */
			int getVitaType() const;

		protected:
			// Packet size recalculator
			void recalc_packet_size();
			// Connect UDP port
			void connect_udp_port();
			// Disconnect UDP port
			void disconnect_udp_port();

		private:
			std::string d_name;
			int     d_vita_type;
			size_t  d_payload_size;  // maximum transmission unit (packet length)
			size_t  d_vita_header_size;
			size_t  d_vita_tail_size;
			bool    d_byte_swapped;
			bool    d_iq_swapped;
			std::string d_host;
			unsigned short d_port;
			size_t  d_packet_size;
			VitaIqUdpPort* d_udp_port;
			boost::mutex d_udp_port_mtx;
	};

} // namespace LibCyberRadio

#endif /* INCLUDED_LIBCYBERRADIO_VITAIQSOURCE_H_ */

