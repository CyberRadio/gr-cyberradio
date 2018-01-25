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
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <net/ethernet.h>
#include <net/if.h>
#include <netinet/in.h>
#include <netdb.h>
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

#include <volk/volk.h>
#include <CyberRadio/vita_udp_rx.h>

#define RECV_TIMEOUT 100

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

namespace gr {
  namespace CyberRadio {

    class vita_udp_rx_impl : public vita_udp_rx
    {
     private:
        // Variables
        int samples_per_packet;
        bool swap_bytes, swap_iq;
        bool vector_output;
        std::string src_ip;  
        unsigned short port;
        unsigned int header_byte_offset;   
        unsigned int bytes_per_packet;   
        int sock_fd;
        bool tag_packets;
        uint8_t *buffer;
        struct pollfd pfd;

        // Methods
        void tag_packet();
        int initSocket();

     public:
      vita_udp_rx_impl(const std::string &src_ip,
    		  	  	  	  unsigned short port,
						  unsigned int header_byte_offset,
						  int samples_per_packet,
						  int bytes_per_packet,
						  bool swap_bytes,
						  bool swap_iq,
						  bool tag_packets,
						  bool vector_output);
      ~vita_udp_rx_impl();

      void rxControlMsg(pmt::pmt_t msg);

      bool start();
      bool stop();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_UDP_RX_IMPL_H */

