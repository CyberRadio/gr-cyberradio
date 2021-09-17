// -*- c++ -*-
/*
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_CYBERRADIO_VITA_UDP_RX_H
#define INCLUDED_CYBERRADIO_VITA_UDP_RX_H

#include <gnuradio/block.h>
#include <CyberRadio/api.h>

namespace gr {
namespace CyberRadio {

/*!
 * \brief <+description of block+>
 * \ingroup CyberRadio
 *
 */

// Note: the recommendation from GNU Radio developers is the sources and sinks should
// always inherit from gr::block, not one of the more derived types
class CYBERRADIO_API vita_udp_rx : public gr::block
{
public:
    using BaseBlock = gr::block;
    using sptr = boost::shared_ptr<vita_udp_rx>;

    // Because this class takes a number of optional configuration items, and because the
    // signature changed in a way that could lead to undiagnosed errors, collapse all the
    // configuration items to a structure and pass that
    struct Cfg {
        std::string src_ip;          ///< source IP address to bind to
        short port;                  ///< source port to bind to
        unsigned header_byte_offset; ///< number of bytes in the V49 header
        int samples_per_packet;      ///< number of samples in a packet
        int bytes_per_packet;        ///< total size of the V49 packet
        bool swap_bytes;             ///< if the packet should be byteswapped
        bool swap_iq;                ///< change from IQ to QI (or from QI to IQ)
        bool tag_packets;            ///< add GR tags to the stream
        bool uses_v49_1 = true;      ///< VITA 49.1 (VRLP and VEND headers)
        bool narrowband = false;     ///< if using a narrowband DDC
        bool debug = false;          ///< output extra debug info
    };

    /*!
     * \brief Return a shared_ptr to a new instance of vita_udp_rx::vita_udp_rx.
     *
     * To avoid accidental use of raw pointers, vita_udp_rx::vita_udp_rx's
     * constructor is in a private implementation class. vita_udp_rx::vita_udp_rx::make
     * is the public interface for creating new instances.
     */
    static auto make(Cfg const& cfg) -> sptr;

    // these are already virtual ... do we need the pure virtual?
    bool start() override = 0;
    bool stop() override = 0;

protected:
    using BaseBlock::block;
};

} // namespace CyberRadio
} // namespace gr

#endif // INCLUDED_CYBERRADIO_VITA_UDP_RX_H
