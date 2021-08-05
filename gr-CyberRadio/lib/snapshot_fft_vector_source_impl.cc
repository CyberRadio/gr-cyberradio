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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "snapshot_fft_vector_source_impl.h"
#include <gnuradio/io_signature.h>
#include <sys/uio.h>

namespace gr {
namespace CyberRadio {

snapshot_fft_vector_source::sptr snapshot_fft_vector_source::make(
    const std::string radio_type, const std::string &ip, unsigned int port,
    unsigned int block_size, unsigned int block_rate) {
  return gnuradio::get_initial_sptr(new snapshot_fft_vector_source_impl(
      radio_type, ip, port, block_size, block_rate));
}

/*
 * The private constructor
 */
snapshot_fft_vector_source_impl::snapshot_fft_vector_source_impl(
    const std::string radio_type, const std::string &ip, unsigned int port,
    unsigned int block_size, unsigned int block_rate)
    : gr::sync_block("snapshot_fft_vector_source",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(1, 1, sizeof(int8_t) * block_size)),
      d_radio_type(radio_type), d_ip(ip), d_port(port),
      d_block_size(block_size), d_block_rate(block_rate), d_tag_frame(false),
      thisCount(0), lastCount(0), d_byte_swap(false), d_iq_swap(true),
      initializing(true), running(false), _parseHeader(_parseHeaderNull) {
  // this->set_iqSwap(false);
  // this->set_byteSwap(true);
  this->d_samples_per_frame = 8192;

  //~ this->_parseHeader = this->_parseHeaderNdr551;

  this->rxVec[0].iov_base = new char[48];
  this->rxVec[0].iov_len = 48;

  this->rxVec[1].iov_base = new int8_t[this->d_samples_per_frame];
  this->rxVec[1].iov_len = sizeof(int8_t) * this->d_samples_per_frame;

  this->rxVec[2].iov_base = new char[8];
  this->rxVec[2].iov_len = 8;

  for (int i = 0; i < 3; i++) {
    std::cout << "[1]rxVec[" << i << "].iov_len = " << rxVec[i].iov_len
              << std::endl;
    this->expectedRxSize += rxVec[i].iov_len;
  }
  // this->set_bswap_flags();

  // Save GRC Paramters
  this->ip = std::string(ip);
  this->port = port;
  this->block_size = block_size;
  this->block_rate = block_rate;
  this->packets_per_block = (int)ceil(static_cast<float>(this->block_size) /
                                      this->d_samples_per_frame);

  // Init a huge vector that will hold all the samples
  this->sampleVector = std::vector<int8_t>(block_size);
}

bool snapshot_fft_vector_source_impl::start(void) {
  this->initializing = false;
  this->running = true;

  // Init block counting and prebuffering state
  this->stream_counter = 0;
  this->sample_counter = 0;
  this->program_starting = true; // We have to pre buffer some data for gnuradio
  this->sock_fd = this->initSocket("0.0.0.0", port); // create recv socket
  if (this->sock_fd < 0) {
    perror("Could not create socket.  Check that /proc/sys/net/core/rmem_max "
           "is set to 268435456");
    throw "Socket Creation Error";
  }

  return true;
}

bool snapshot_fft_vector_source_impl::stop(void) {
  this->running = false;
  return true;
}

int snapshot_fft_vector_source_impl::initSocket(const std::string ip,
                                                unsigned short port) {

  // /proc/sys/net/core/rmem_max holds this value must be >= recv_buffer_size
  // linux kernel receiver buffer size. this is not to be confused with the size
  // of this class' ring buffer.
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
  //~ if (setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &recv_buffer_size,
  // sizeof(unsigned long long)) == -1) { ~ perror("couldn't set recv buf
  // size."); ~ return -1;
  //~ }

  while (setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &recv_buffer_size,
                    sizeof(unsigned long long)) == -1) {
    std::cerr << "Couldn't set recv buf size = " << recv_buffer_size << "."
              << std::endl;
    recv_buffer_size <<= 1;
  }

  /* Verify this sock opt took */
  unsigned long long check_size = 0;
  unsigned int arg_len = sizeof(check_size);
  getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &check_size, &arg_len);
  if (check_size != 2 * recv_buffer_size) {
    fprintf(stderr, "ERROR: set recv buf size, but it is incorrect in kernel. "
                    "check max limit in /proc/sys/net/core/rmem_max\n");
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

void snapshot_fft_vector_source_impl::pause() {
  // Close our recv socket
  close(this->sock_fd);
  //~ printf("\n");

  // Sleep
  if (this->block_rate > 0) {
    usleep(950000 / this->block_rate);
  }

  // Open a new socket
  this->sock_fd = this->initSocket(this->ip, this->port);
  if (this->sock_fd < 0) {
    perror("Could not create socket.  Check that /proc/sys/net/core/rmem_max "
           "is set to 268435456");
    throw "Socket Creation Error";
  }
}

/*
 * Our virtual destructor.
 */
snapshot_fft_vector_source_impl::~snapshot_fft_vector_source_impl() {}

int snapshot_fft_vector_source_impl::work(
    int noutput_items, gr_vector_const_void_star &input_items,
    gr_vector_void_star &output_items) {
  int8_t *out = (int8_t *)output_items[0];
  int samps2use;
  // Recv a packet
  //~ recv(this->sock_fd, rxbuff, sizeof(Ndr308Frame), 0);
  int rxSize = readv(this->sock_fd, this->rxVec, 3);
  // printf("rxsize = %d\n", rxSize);

  // make sure the packet was big enough to be a data packet.
  // Ignore Context Packets
  if (rxSize > 1000) {
    if (this->d_tag_frame) {
      // Decode the Vita49 header
      _parseHeader((char *)(this->rxVec[0].iov_base), this->rxVec[0].iov_len);
    }

    // Increment our counter of packets received
    this->stream_counter++;
    this->sample_counter += this->d_samples_per_frame;

    // Check to see if it's time to sleep
    if (this->stream_counter >= this->packets_per_block) {
      this->stream_counter = 0;
      this->sample_counter = 0;
      if (this->block_rate > 0) {
        this->pause();
      }

      // Copy Sample Vector to output vector
      memcpy(out, this->rxVec[1].iov_base, this->block_size * sizeof(int8_t));

      return 1;
    }
  }
  // We need more samples
  return 0;
}

} /* namespace CyberRadio */
} /* namespace gr */
