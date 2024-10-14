/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H
#define INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H

#include <CyberRadio/vita_udp_rx.h>

typedef struct {
    uint32_t packet_info;
    uint32_t stream_id;
    uint32_t class_0;
    uint32_t class_1;
    uint32_t int_timestamp;
    uint32_t frac_timestamp_msw;
    uint32_t frac_timestamp_lsw;
    uint32_t ddc_0;
    uint32_t ddc_1;
    uint32_t ddc_2;
    uint32_t ddc_3;
    uint32_t ddc_4;
} V49_0_Header;

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
      bool d_use_vector_output;
      uint64_t d_frac_last_timestamp;

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
      ~vita_udp_rx_impl();

      vita_udp_rx_impl(std::string src_ip, 
                  unsigned short port, 
                  unsigned int header_byte_offset, 
                  int samples_per_packet, 
                  int bytes_per_packet, 
                  bool swap_bytes, 
                  bool swap_iq, 
                  bool tag_packets, 
                  bool vector_output, 
                  bool uses_v491, 
                  bool narrowband, 
                  bool debug);

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

#endif /* INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H */
