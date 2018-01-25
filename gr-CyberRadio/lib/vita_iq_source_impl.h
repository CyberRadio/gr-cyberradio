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

#ifndef INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_IMPL_H
#define INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_IMPL_H

#include <CyberRadio/vita_iq_source.h>
#include <LibCyberRadio/Common/Vita49Packet.h>
#include <boost/asio.hpp>
#include <boost/format.hpp>
#include <boost/thread.hpp>
#include <stdio.h>
#include <time.h>
#include <sys/types.h> 
#include <string>
#include <vector>

typedef LibCyberRadio::Vita49Packet Vita49Packet;

namespace gr
{
  namespace CyberRadio
  {

    /*
     * Class that grabs channel I/Q data from a UDP port.
     */
    class vita_iq_udp_port
    {
    public:
      vita_iq_udp_port(const std::string& host = "0.0.0.0",
                   int port = 40001,
               int packet_size = 8192,
               bool debug = false);
      ~vita_iq_udp_port();
      void read_data();
      void clear_buffer();
      bool is_packet_ready() const;

    protected:
      // Debug output helper
      int debug(const char *format, ...);

    public:
      std::string host;
      int port;
      int packet_size;
      bool connected;    // are we connected?
      boost::asio::ip::udp::socket *socket;
      boost::asio::ip::udp::endpoint endpoint;
      boost::asio::io_service io_service;
      char* recv_buffer;
      int bytes_recvd;
      bool d_debug;

    };


    class vita_iq_source_impl : public vita_iq_source
    {
    public:
      vita_iq_source_impl(int vita_type,
                size_t payload_size,
                size_t vita_header_size,
                size_t vita_tail_size,
                bool byte_swapped,
                bool iq_swapped,
                float iq_scale_factor,
                const std::string& host,
                const std::vector<unsigned short>& port_list,
                bool tagged,
                        bool debug);
      ~vita_iq_source_impl();
      // Where all the action really happens
      int work(int noutput_items,
               gr_vector_const_void_star &input_items,
               gr_vector_void_star &output_items);
      float get_realtime_sample_rate(int output);

    protected:
      // Debug output helper
      int debug(const char *format, ...);
      // Packet size recalculator
      void recalc_packet_size();
      // Connect all UDP ports
      void connect_udp_ports();
      // Disconnect all UDP ports
      void disconnect_udp_ports();
      // Generate tags for an output stream from a Vita 49
      // packet
      void generate_vita_tags(int output, const Vita49Packet& vp);

    private:
      int     d_vita_type;
      size_t  d_payload_size;  // maximum transmission unit (packet length)
      size_t  d_vita_header_size;
      size_t  d_vita_tail_size;
      bool    d_byte_swapped;
      bool    d_iq_swapped;
      float   d_iq_scale_factor;
      int     d_num_outputs;
      std::string d_host;
      std::vector<unsigned short> d_port_list;
      size_t  d_packet_size;
      bool    d_tagged;
      bool    d_debug;
      std::vector<vita_iq_udp_port*> d_udp_ports;
      boost::mutex d_udp_port_mtx;
      std::vector<float> d_realtime_sample_rates;
      std::vector<long> d_realtime_sample_counts;
      time_t d_realtime_last_time;
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_IMPL_H */

