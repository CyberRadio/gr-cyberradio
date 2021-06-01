/* -*- c++ -*- */
/* 
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_CYBERRADIO_SNAPSHOT_SOURCE_C_IMPL_H
#define INCLUDED_CYBERRADIO_SNAPSHOT_SOURCE_C_IMPL_H

#include <CyberRadio/snapshot_source_c.h>
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

#include <iostream>

#include "packet_types.h"

namespace gr {
  namespace CyberRadio {

    class snapshot_source_c_impl : public snapshot_source_c
    {
    private:

    std::string ip;
    unsigned int port;
    unsigned int block_rate;
    unsigned int block_size;
    unsigned int packets_per_block;

     int stream_counter;
     bool program_starting;
     int sock_fd;
     //~ uint8_t * rxbuff;
     struct Ndr308Frame* rxbuff;
     int32_t thisCount,lastCount,countDiff;
     bool d_iq_swap, d_byte_swap;
     //~ struct Ndr308Frame * frame;

    public:
     snapshot_source_c_impl(const std::string &ip, unsigned int port, unsigned int block_size, unsigned int block_rate);
     ~snapshot_source_c_impl();
     int initSocket(const std::string ip, unsigned short port);
     void pause();

     // Where all the action really happens
     int work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SNAPSHOT_SOURCE_C_IMPL_H */

