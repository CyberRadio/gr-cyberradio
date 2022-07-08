/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_VITA_RX_IMPL_H
#define INCLUDED_CYBERRADIO_VITA_RX_IMPL_H

#include <CyberRadio/vita_rx.h>

namespace gr {
  namespace CyberRadio {

    class vita_rx_impl : public vita_rx
    {
     private:
      // Nothing to declare in this block.
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
      bool d_first_ctx_packet;
      unsigned d_packetCounter : 4;
      std::vector<uint8_t> d_buffer;

      uint64_t d_sample_rate;
      uint64_t d_ref_freq;
      uint64_t d_bandwidth;

     protected:
      auto receive_packet() -> bool;
      auto process_IQ(gr_complex*& outP) -> int;
      auto process_packet(gr_complex*& outP, int samples_needed) -> int;
      auto handle_dropped_packet(unsigned packet_counter,
                                 gr_complex*& outP,
                                 int samples_needed) -> int;
      auto handle_context_packet( int rx_size ) -> int;

     public:
      vita_rx_impl(std::string &src_ip, 
                      unsigned short port, 
                      unsigned int header_byte_offset, 
                      int samples_per_packet, 
                      int bytes_per_packet, 
                      bool swap_bytes, 
                      bool swap_iq, bool 
                      tag_packets, bool 
                      vector_output, 
                      bool uses_v491, 
                      bool narrowband, 
                      bool debug);
      ~vita_rx_impl();
      void rxControlMsg(pmt::pmt_t msg);
      void txStatusMsg();

      bool start() override;
      bool stop() override;

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_RX_IMPL_H */
