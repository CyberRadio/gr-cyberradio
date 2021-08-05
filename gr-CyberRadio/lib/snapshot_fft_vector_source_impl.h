/* -*- c++ -*- */
/*
 * Copyright 2019 G3.
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

#ifndef INCLUDED_CYBERRADIO_SNAPSHOT_FFT_VECTOR_SOURCE_IMPL_H
#define INCLUDED_CYBERRADIO_SNAPSHOT_FFT_VECTOR_SOURCE_IMPL_H

#include <CyberRadio/snapshot_fft_vector_source.h>

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <net/if.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/un.h>
#include <unistd.h>

#include <iostream>
#include <poll.h>
#include <vector>
#include <volk/volk.h>

#include "packet_types.h"

namespace gr {
namespace CyberRadio {

class snapshot_fft_vector_source_impl : public snapshot_fft_vector_source {
private:
  std::string d_radio_type;
  std::string d_ip;
  unsigned int d_port;
  unsigned int d_block_rate;
  unsigned int d_block_size;
  bool d_tag_frame;

  std::string ip;
  unsigned int port;
  unsigned int block_rate;
  unsigned int block_size;
  unsigned int packets_per_block;

  bool d_byteSwap, d_iqSwap;
  bool d_bswap32, d_bswap16;
  int d_samples_per_frame;
  bool initializing, running;

  int stream_counter, sample_counter;
  bool program_starting;
  int sock_fd;
  std::vector<int8_t> sampleVector;
  struct iovec rxVec[3];
  int expectedRxSize;
  struct pollfd pfd;

  int32_t thisCount, lastCount, countDiff;
  bool d_iq_swap, d_byte_swap;

  void (*_parseHeader)(char *, int);
  static void _parseHeaderNull(char *hdr, int hdr_len) {
    std::cout << "_parseHeaderNull" << std::endl;
  };

public:
  snapshot_fft_vector_source_impl(const std::string radio_type,
                                  const std::string &ip, unsigned int port,
                                  unsigned int block_size,
                                  unsigned int block_rate);
  ~snapshot_fft_vector_source_impl();
  int initSocket(const std::string ip, unsigned short port);
  void pause();

  bool start(void);
  bool stop(void);
  // Where all the action really happens
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SNAPSHOT_FFT_VECTOR_SOURCE_IMPL_H */
