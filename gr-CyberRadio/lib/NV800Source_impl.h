/* -*- c++ -*- */
/*
 * Copyright 2024 Epiq.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_NV800SOURCE_IMPL_H
#define INCLUDED_CYBERRADIO_NV800SOURCE_IMPL_H

#include <CyberRadio/NV800Source.h>

namespace gr {
namespace CyberRadio {

class NV800Source_impl : public NV800Source
{
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
private:
    size_t const d_bytes_per_packet;
    std::vector<uint8_t> d_buffer;
    std::string const d_src_ip;
    unsigned short const d_port;
    int d_sock;
    int const d_samples_per_packet;
    size_t const d_header_byte_offset;
    bool const d_swap_bytes;
    bool const d_swap_iq;
    bool d_debug;
    bool d_first_packet;
    unsigned d_packetCounter : 4;
public:
    NV800Source_impl(std::string src_ip, 
                  unsigned short port);
    ~NV800Source_impl();

    // Where all the action really happens
      int general_work(int noutput_items,
                      gr_vector_int& ninput_items,
                      gr_vector_const_void_star& input_items,
                      gr_vector_void_star& output_items) override;
    bool start() override;
    bool stop() override;
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NV800SOURCE_IMPL_H */
