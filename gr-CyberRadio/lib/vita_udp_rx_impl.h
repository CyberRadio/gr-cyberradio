/* -*- c++ -*- */
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

// C Includes
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

#include <CyberRadio/vita_udp_rx.h>
#include <volk/volk.h>

#define RECV_TIMEOUT 100

std::map<int, float> ndr358_551_ddc_map = {
  { 0, 0.25e3},
  { 1, 0.5e3},
  { 2, 1.0e3},
  { 3, 2.0e3},
  { 4, 4.0e3},
  { 5, 8.0e3},
  { 6, 16e3},
  { 7, 32e3},
  { 8, 64e3},
  { 9, 128e3},
  {10, 200e3},
  {11, 256e3},
  {12, 400e3},
  {13, 1.28e6},
  {14, 3.2e6},
  {15, 4e6},
  {16, 2e6},
  {32, 8e6},
  {33, 8e6},
  {34, 16e6},
  {35, 16e6},
  {36, 16e6},
  {37, 32e6},
  {38, 32e6},
  {39, 64e6},
  {40, 128e6}
};

// V49 Struct Info
typedef struct {
  char p;
  char l;
  char r;
  char v;
  unsigned int frame_info;
  unsigned int packet_info;
  unsigned int stream_id;
  unsigned int class_id_1;
  unsigned int class_id_2;
  unsigned int int_timestamp;
  unsigned int frac_timestamp_msw;
  unsigned int frac_timestamp_lsw;
} V49_308_Header;

// VITA 49 VRT IF data packet header, no class ID
// (used without external framing on NDR354/364)
typedef struct {
  unsigned int packet_info;
  unsigned int stream_id;
  unsigned int int_timestamp;
  unsigned int frac_timestamp_msw;
  unsigned int frac_timestamp_lsw;
} V49_No491_Header;

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

class vita_udp_rx_impl : public vita_udp_rx {
private:
  // Variables
  int samples_per_packet;
  bool swap_bytes, swap_iq;
  bool vector_output;
  std::string src_ip;
  unsigned short port;
  unsigned int header_byte_offset;
  unsigned int bytes_per_packet;
  bool uses_v491, is_narrowband;
  int sock_fd;
  bool tag_packets;
  bool debug;
  uint8_t *buffer;
  struct pollfd pfd;
  int d_packetCounter;
  bool d_coherent;

  // Methods
  void tag_packet(int index);
  int initSocket();

public:
  vita_udp_rx_impl(const std::string &src_ip, unsigned short port,
                   unsigned int header_byte_offset, int samples_per_packet,
                   int bytes_per_packet, bool swap_bytes, bool swap_iq,
                   bool tag_packets, bool vector_output, bool uses_v491 = true,
                   bool narrowband = false, bool debug = false);
  ~vita_udp_rx_impl();

  void rxControlMsg(pmt::pmt_t msg);
  void txStatusMsg(void);

  bool start();
  bool stop();

  // Where all the action really happens
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H */
