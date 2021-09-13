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

#ifndef INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H
#define INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H

#include "CyberRadio/vita_udp_rx.h"
#include <vector>

namespace gr {
namespace CyberRadio {

class vita_udp_rx_impl : public vita_udp_rx
{
    using Base = vita_udp_rx;

private:
    // Variables
    std::string const d_src_ip;
    unsigned short const d_port;
    int d_sock;

    int const d_samples_per_packet;
    size_t const d_header_byte_offset;
    size_t const d_bytes_per_packet;
    bool const d_swap_bytes;
    bool const d_swap_iq;
    bool const d_uses_v49_1;
    bool const d_is_narrowband;
    bool const d_tag_packets;
    bool d_debug;
    bool d_first_packet;
    unsigned d_packetCounter : 4;

    std::vector<uint8_t> d_buffer;

protected:
    // Methods
    auto receive_packet() -> bool;
    auto process_packet(gr_complex*& outP, int samples_needed) -> int;
    auto process_v491_packet(gr_complex*& outP) -> int;
    auto handle_dropped_packet(unsigned packet_counter,
                               gr_complex*& outP,
                               int samples_needed) -> int;
    auto process_IQ(gr_complex*& outP) -> int;


    auto tag_packet(int stream, int offset) -> void;
    auto tag_v491_packet(int stream, int offset) -> void;

public:
    vita_udp_rx_impl(Cfg const& cfg);

    void rxControlMsg(pmt::pmt_t msg);
    void txStatusMsg();

    bool start() override;
    bool stop() override;

    // Where all the action really happens
    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items) override;
};

} // namespace CyberRadio
} // namespace gr

#endif // INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H
