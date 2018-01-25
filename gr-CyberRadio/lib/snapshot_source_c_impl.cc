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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <volk/volk.h>
#include <gnuradio/io_signature.h>
#include "snapshot_source_c_impl.h"

namespace gr {
  namespace CyberRadio {

  snapshot_source_c::sptr
  snapshot_source_c::make(const std::string &ip, unsigned int port, unsigned int block_size, unsigned int block_rate)
  {
    return gnuradio::get_initial_sptr
      (new snapshot_source_c_impl(ip, port, block_size, block_rate));
  }

  /*
   * The private constructor
   */
  snapshot_source_c_impl::snapshot_source_c_impl(const std::string &ip, unsigned int port, unsigned int block_size, unsigned int block_rate)
    : gr::sync_interpolator("snapshot_source_c",
            gr::io_signature::make(0, 0, 0),
            gr::io_signature::make(1, 1, sizeof(gr_complex)), 1024),
      thisCount(0),
      lastCount(0),
      d_byte_swap(false),
      d_iq_swap(true)
  {

      // Save GRC Paramters
      this->ip = std::string(ip);
      this->port = port;
      this->block_size = block_size;
      this->block_rate = block_rate;
      this->packets_per_block = this->block_size/1024;

      // Init block counting and prebuffering state
      this->stream_counter = 0;
      this->program_starting = true; // We have to pre buffer some data for gnuradio
      this->sock_fd = this->initSocket("0.0.0.0", port); // create recv socket
      if (this->sock_fd < 0) {
          perror("Could not create socket.  Check that /proc/sys/net/core/rmem_max is set to 268435456");
          throw "Socket Creation Error";
      }
      rxbuff = (struct Ndr308Frame *)malloc(sizeof(Ndr308Frame));
  }

  /*
   * Our virtual destructor.
   */
  snapshot_source_c_impl::~snapshot_source_c_impl()
  {
    free(rxbuff);
  }

  int
  snapshot_source_c_impl::work(int noutput_items,
      gr_vector_const_void_star &input_items,
      gr_vector_void_star &output_items)
  {

    // Declare complex output buffer
    gr_complex *out = (gr_complex *) output_items[0];

    // Recv a packet
    recv(this->sock_fd, rxbuff, sizeof(Ndr308Frame), 0);

    // Copy IQ data to output
    countDiff = (int32_t)(rxbuff->v49.frameCount)-lastCount;
    lastCount = (int32_t)(rxbuff->v49.frameCount);
    if ((this->stream_counter>0)&&(!((countDiff==1)||(countDiff==-4095)))) {
      printf("%d loss @ %d\n", countDiff, this->stream_counter);
    }
    
    // VOLK short->float w/ scale
    //    For the NDR308, we need IQ swap before we can use this
    if (d_byte_swap) {
    if (d_iq_swap) {
      volk_32u_byteswap((uint32_t *)rxbuff->IQ.samples, 1024);
    } else {
      volk_16u_byteswap((uint16_t *)rxbuff->IQ.samples, 2048);
    }
  } else if (d_iq_swap) {
    volk_32u_byteswap((uint32_t *)rxbuff->IQ.samples, 1024);
    volk_16u_byteswap((uint16_t *)rxbuff->IQ.samples, 2048);
  }
    volk_16i_s32f_convert_32f_u( (float*)out, rxbuff->IQ.samples, 32767.0, 2048 );

    // Increment our counter of packets sent
    this->stream_counter++;

    // Check to see if it's time to sleep
    if (this->program_starting) {
        if (this->stream_counter > this->packets_per_block*50) {
            // We have prebuffered 10 FFTs worth of data
            this->stream_counter = 0;
            this->program_starting = false;
            this->pause();
        }
    } else {
        if (this->stream_counter >= this->packets_per_block) {
            this->stream_counter = 0;
            if (this->block_rate>0) {
              this->pause();
            }
        }
    }

    // Tell runtime system how many output items we produced.
    return 1024;
  }


  int snapshot_source_c_impl::initSocket(const std::string ip, unsigned short port)
  {

      // /proc/sys/net/core/rmem_max holds this value must be >= recv_buffer_size
      // linux kernel receiver buffer size. this is not to be confused with the size of this class' ring buffer.
      unsigned long recv_buffer_size = 268435456; // 256 MB

      int sockfd;
      struct sockaddr_in myaddr;
      memset((char *)&myaddr, 0, sizeof(myaddr));
      myaddr.sin_family = AF_INET;
      myaddr.sin_addr.s_addr = inet_addr(ip.c_str());
      myaddr.sin_port = htons(port);

      /* Create a UDP Socket*/
      if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
          perror("cannot create socket\n");
          return -1;
      }

      /* Set socket to reuse address */
      int enable = 1;
      if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0) {
          perror("setsockopt SO_REUSEADDR call failed");
          return -1;
      }

      /* Set recv buffer size */
      if (setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &recv_buffer_size, sizeof(unsigned long long)) == -1) {
          perror("couldn't set recv buf size.");
          return -1;
      }

      /* Verify this sock opt took */
      unsigned long long check_size = 0;
      unsigned int arg_len = sizeof(check_size);
      getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &check_size, &arg_len);
      if (check_size != 2*recv_buffer_size) {
          fprintf(stderr, "ERROR: set recv buf size, but it is incorrect in kernel. check max limit in /proc/sys/net/core/rmem_max\n");
          return -1;
      }

      /* Bind the socket */
      if (bind(sockfd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) {
          perror("bind failed");
          return -1;
      }

      /* Our socket was correctly created */
      return sockfd;

  }

  void snapshot_source_c_impl::pause()
  {
      // Close our recv socket
      close(this->sock_fd);
      //~ printf("\n");

      // Sleep
      if (this->block_rate>0) {
        usleep(950000/this->block_rate);
      }

      // Open a new socket
      this->sock_fd = this->initSocket(this->ip, this->port);
      if (this->sock_fd < 0) {
          perror("Could not create socket.  Check that /proc/sys/net/core/rmem_max is set to 268435456");
          throw "Socket Creation Error";
      }
  }

  } /* namespace CyberRadio */
} /* namespace gr */

