/* -*- c++ -*- */
/***************************************************************************
 * \file vita_iq_source_impl.h
 *
 * \brief Implementation of a generic VITA 49-compatible I/Q data source
 *    block.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_2_IMPL_H
#define INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_2_IMPL_H

#include <CyberRadio/vita_iq_source_2.h>
#include <LibCyberRadio/Common/Vita49Packet.h>
#include <boost/asio.hpp>
#include <boost/format.hpp>
#include <boost/thread.hpp>
#include <stdio.h>
#include <string>
#include <sys/types.h>
#include <time.h>
#include <vector>

typedef LibCyberRadio::Vita49Packet Vita49Packet;

namespace gr {
namespace CyberRadio {

class vita_iq_source_2_impl : public vita_iq_source_2 {
public:
  vita_iq_source_2_impl(int vitaType, size_t payloadSize, size_t vitaHeaderSize,
                        size_t vitaTailSize, bool byteSwapped, bool iqSwapped,
                        const std::string &host, int port, bool debug,
                        bool tagOutput, bool coherent);
  ~vita_iq_source_2_impl();

  void connect(const std::string &host, int port);
  void disconnect();

  void set_receive_buffer_size(int size);
  int get_receive_buffer_size(void);
  void set_scale_factor(int);
  int get_scale_factor();

  // Where all the action really happens
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

protected:
  // Debug output helper
  int debug(const char *format, ...);

private:
  int d_vitaType;
  size_t d_payloadSize; // maximum transmission unit (packet length)
  size_t d_vitaHeaderSize;
  size_t d_vitaTailSize;
  bool d_byteSwapped;
  bool d_iqSwapped;
  bool d_tagOutput;
  bool d_coherent;
  size_t d_packetSize;

  bool d_connected; // are we connected?
  char *d_rxbuf;    // get UDP buffer items
  char *d_residbuf; // hold buffer between calls
  ssize_t
      d_residual;  // hold information about number of bytes stored in residbuf
  ssize_t d_sent;  // track how much of d_residbuf we've outputted
  size_t d_offset; // point to residbuf location offset
  std::string d_host;
  unsigned short d_port;
  bool d_debug;
  int d_scale;

  boost::asio::ip::udp::socket *d_socket;
  boost::asio::ip::udp::endpoint d_endpoint;
  boost::asio::ip::udp::endpoint d_endpoint_rcvd;
  boost::asio::io_service d_io_service;

  size_t d_tmpbuf_size;
  char *d_tmpbuf;
  char *d_tmpbuf2;
  uint32_t d_frame_count;
  uint64_t d_dropped;
  int d_skip_packets;

  gr::thread::condition_variable d_cond_wait;
  gr::thread::mutex d_udp_mutex;
  gr::thread::thread d_udp_thread;

  void start_receive();
  void handle_read(const boost::system::error_code &error,
                   size_t bytes_transferred);
  void run_io_service() { d_io_service.run(); }

  int _read_socket_data(int noutput_items, char *output_buffer);
  int _parse_vita_and_tag(char *output_buffer, int number_of_packets);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_2_IMPL_H */
