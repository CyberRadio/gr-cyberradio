/* -*- c++ -*- */
/***************************************************************************
 * \file vita_iq_source_impl.cpp
 *
 * \brief Implementation of a generic VITA 49-compatible I/Q data source
 *    block.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "CyberRadio/vita_iq_source.h"
#include "vita_iq_source_impl.h"
#include <algorithm>
#include <gnuradio/io_signature.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include <volk/volk.h>

namespace gr {
namespace CyberRadio {
vita_iq_udp_port::vita_iq_udp_port(const std::string &host, int port,
                                   int packet_size, bool debug)
    : host(host), port(port), packet_size(packet_size), connected(false),
      socket(NULL), recv_buffer(NULL), bytes_recvd(0), d_debug(debug) {
  // Allocate the receive buffer
  recv_buffer = new char[packet_size];
  memset(recv_buffer, 0, packet_size);
  // Connect to the UDP port
  boost::system::error_code error = boost::asio::error::host_not_found;
  std::string s_port = (boost::format("%d") % port).str();
  if (host.size() > 0) {
    boost::asio::ip::udp::resolver resolver(io_service);
    boost::asio::ip::udp::resolver::query query(
        boost::asio::ip::udp::v4(), host, s_port,
        boost::asio::ip::resolver_query_base::passive);
    io_service.run();
    endpoint = *resolver.resolve(query);
    if (errno > 0) {
      printf("cannot resolve host IP %s error: %s\n", host.c_str(),
             strerror(errno));
    } else {
      socket = new boost::asio::ip::udp::socket(io_service);
      socket->open(endpoint.protocol());
      boost::asio::socket_base::linger loption(true, 0);
      socket->set_option(loption);
      boost::asio::socket_base::reuse_address roption(true);
      socket->set_option(roption);
      socket->bind(endpoint);
      connected = true;
    }
  }
}

vita_iq_udp_port::~vita_iq_udp_port() {
  connected = false;
  io_service.reset();
  io_service.stop();
  if (socket != NULL) {
    socket->close();
    delete socket;
  }
  // Deallocate the receive buffer
  if (recv_buffer != NULL)
    delete recv_buffer;
}

void vita_iq_udp_port::read_data() {
  int socket_fd, result, num_received;
  fd_set readset;
  struct timeval timeout;
  timeout.tv_sec = 0;
  timeout.tv_usec = 0; // 100000;

  socket_fd = socket->native_handle();
  /* Socket has been created and connected to the other party */
  do {
    FD_ZERO(&readset);
    FD_SET(socket_fd, &readset);
    result = select(socket_fd + 1, &readset, NULL, NULL, &timeout);
  } while (result == -1 && errno == EINTR);

  if (result > 0) {
    if (FD_ISSET(socket_fd, &readset)) {
      /* The socket_fd has data available to be read */
      do {
        num_received = socket->receive(boost::asio::buffer(
            (void *)(recv_buffer + bytes_recvd), packet_size - bytes_recvd));
        bytes_recvd += num_received;
      } while ((num_received != 0) && (bytes_recvd < packet_size));
    }
  } else if (result < 0) {
    /* An error ocurred, just print it to stdout */
  }
}

void vita_iq_udp_port::clear_buffer() {
  memset(recv_buffer, 0, packet_size);
  bytes_recvd = 0;
}

bool vita_iq_udp_port::is_packet_ready() const {
  return (bytes_recvd == packet_size);
}

int vita_iq_udp_port::debug(const char *format, ...) {
  int ret = 0;
  if (d_debug) {
    ret = printf("[vita_iq_udp_port %d] ", port);
    if (ret >= 0) {
      va_list ap;
      va_start(ap, format);
      ret = vprintf(format, ap);
      va_end(ap);
    }
  }
  return ret;
}

vita_iq_source::sptr vita_iq_source::make(
    int vita_type, size_t payload_size, size_t vita_header_size,
    size_t vita_tail_size, bool byte_swapped, bool iq_swapped,
    float iq_scale_factor, const std::string &host,
    const std::vector<unsigned short> &port_list, bool tagged, bool debug) {
  return gnuradio::get_initial_sptr(new vita_iq_source_impl(
      vita_type, payload_size, vita_header_size, vita_tail_size, byte_swapped,
      iq_swapped, iq_scale_factor, host, port_list, tagged, debug));
}

/*
 * The private constructor
 */
vita_iq_source_impl::vita_iq_source_impl(
    int vita_type, size_t payload_size, size_t vita_header_size,
    size_t vita_tail_size, bool byte_swapped, bool iq_swapped,
    float iq_scale_factor, const std::string &host,
    const std::vector<unsigned short> &port_list, bool tagged, bool debug)
    : gr::sync_block("[CyberRadio] VITA I/Q Source",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(0, 0, 0)),
      d_vita_type(vita_type), d_payload_size(payload_size),
      d_vita_header_size(vita_header_size), d_vita_tail_size(vita_tail_size),
      d_byte_swapped(byte_swapped), d_iq_swapped(iq_swapped),
      d_iq_scale_factor(iq_scale_factor), d_num_outputs(0), d_host(host),
      d_port_list(port_list), d_packet_size(0), d_tagged(tagged),
      d_debug(debug) {
  this->debug("construction\n");
  // Get number of outputs
  d_num_outputs = (int)d_port_list.size();
  // Determine packet size and create the output signature
  d_packet_size =
      (vita_type == 0 ? payload_size
                      : vita_header_size + payload_size + vita_tail_size);
  // this->set_output_signature(gr::io_signature::make(1, d_num_outputs,
  // sizeof(unsigned short) * d_payload_size / 2));
  this->set_output_signature(
      gr::io_signature::make(1, d_num_outputs, sizeof(gr_complex)));
  // Create UDP ports for collecting data
  connect_udp_ports();
  // Initialize data rate calculation stuff
  for (int output = 0; output < d_num_outputs; output++) {
    d_realtime_sample_rates.push_back(0.0);
    d_realtime_sample_counts.push_back(0);
  }
  d_realtime_last_time = time(NULL);
}

/*
 * Our virtual destructor.
 */
vita_iq_source_impl::~vita_iq_source_impl() {
  this->debug("destruction\n");
  // Destroy/disconnect UDP ports for collecting data
  disconnect_udp_ports();
}

int vita_iq_source_impl::work(int noutput_items,
                              gr_vector_const_void_star &input_items,
                              gr_vector_void_star &output_items) {
  // Pointer to output buffer -- this gets assigned by output
  gr_complex *out;
  // Number of samples in a given data packet
  int samples_in_packet = d_payload_size / sizeof(unsigned short) / 2;
  // Number of output items processed, max number of output items
  // processed, got data on loop flag
  std::vector<int> noutput_items_processed(d_num_outputs, 0);
  int max_noutput_items_processed = 0;
  bool got_data_on_loop = false;
  // Loop counters
  int output;
  int sample;
  // Check to see if the UDP ports are available for reading
  if (d_udp_port_mtx.try_lock()) {
    // Loop over UDP ports and see if we have packet data waiting
    // on them.  If we do, fill output buffer with the packet data.
    do {
      got_data_on_loop = false;
      for (output = 0; output < d_num_outputs; output++) {
        // Calculate pointer to output buffer
        out = (gr_complex *)output_items[output];
        // Get data from UDP port if it's available
        d_udp_ports[output]->read_data();
        // Fill the output with data from the UDP port if
        // available, or zeros if not
        if (d_udp_ports[output]->is_packet_ready()) {
          // Decode received packet
          Vita49Packet vp(d_vita_type, d_payload_size, d_vita_header_size,
                          d_vita_tail_size, d_byte_swapped, d_iq_swapped,
                          (unsigned char *)(d_udp_ports[output]->recv_buffer),
                          d_packet_size);
          // Copy the packet's sample data to the correct output stream
          for (sample = 0; sample < samples_in_packet; sample++) {
            out[sample + noutput_items_processed[output]].real(
                vp.getSampleI(sample) * d_iq_scale_factor);
            out[sample + noutput_items_processed[output]].imag(
                vp.getSampleQ(sample) * d_iq_scale_factor);
          }
          // Do tagging on the output stream if desired and if
          // VITA 49 frames are being received
          if (d_tagged && (d_vita_type != 0)) {
            generate_vita_tags(output, vp);
          }
          // Increase number of items available
          noutput_items_processed[output] += samples_in_packet;
          // Reset the UDP port buffer
          d_udp_ports[output]->clear_buffer();
          // Set the got data on loop flag
          got_data_on_loop = true;
        }
      }
      // Get maximum number of output items processed for our outputs
      max_noutput_items_processed = *std::max_element(
          noutput_items_processed.begin(), noutput_items_processed.end());
    } while (got_data_on_loop &&
             (max_noutput_items_processed + samples_in_packet < noutput_items));
    d_udp_port_mtx.unlock();
    // For each output, calculate real-time sample rates.
    time_t now = time(NULL);
    if (now != d_realtime_last_time) {
      for (output = 0; output < d_num_outputs; output++) {
        d_realtime_sample_rates[output] =
            (float)d_realtime_sample_counts[output];
        d_realtime_sample_counts[output] = noutput_items_processed[output];
      }
      d_realtime_last_time = now;
    } else {
      for (output = 0; output < d_num_outputs; output++) {
        d_realtime_sample_counts[output] += noutput_items_processed[output];
      }
    }
    // If any of the outputs got data, pad outputs that didn't get data
    // with zeros to the same length.  This keeps processing from blocking
    // on UDP ports that are not receiving data (for example, if the
    // corresponding output from the radio is disabled).
    if (max_noutput_items_processed > 0) {
      for (output = 0; output < d_num_outputs; output++) {
        // Calculate pointer to output buffer
        out = (gr_complex *)output_items[output];
        // Pad output with zeros
        for (sample = noutput_items_processed[output];
             sample < max_noutput_items_processed; sample++) {
          out[sample].real(0.0);
          out[sample].imag(0.0);
        }
      }
    }
  }
  return max_noutput_items_processed;
}

float vita_iq_source_impl::get_realtime_sample_rate(int output) {
  return d_realtime_sample_rates[output];
}

int vita_iq_source_impl::debug(const char *format, ...) {
  int ret = 0;
  if (d_debug) {
    ret = printf("[%s] ", this->name().c_str());
    if (ret >= 0) {
      va_list ap;
      va_start(ap, format);
      ret = vprintf(format, ap);
      va_end(ap);
    }
  }
  return ret;
}

void vita_iq_source_impl::recalc_packet_size() {
  // Determine packet size
  d_packet_size = (d_vita_type == 0 ? d_payload_size
                                    : d_vita_header_size + d_payload_size +
                                          d_vita_tail_size);
  // Reconnect the UDP ports
  disconnect_udp_ports();
  connect_udp_ports();
}

void vita_iq_source_impl::connect_udp_ports() {
  d_udp_port_mtx.lock();
  // Create UDP ports for collecting data
  for (int i = 0; i < d_num_outputs; i++) {
    this->debug("connect udp %s/%d\n", d_host.c_str(), d_port_list[i]);
    d_udp_ports.push_back(
        new vita_iq_udp_port(d_host, d_port_list[i], d_packet_size, d_debug));
    this->debug("-- connect result: %d\n", d_udp_ports.back()->connected);
  }
  d_udp_port_mtx.unlock();
}

void vita_iq_source_impl::disconnect_udp_ports() {
  d_udp_port_mtx.lock();
  // Destroy UDP ports for collecting data
  for (int i = 0; i < d_num_outputs; i++) {
    this->debug("disconnect udp %s/%d\n", d_host.c_str(), d_port_list[i]);
    delete d_udp_ports.back();
    d_udp_ports.pop_back();
  }
  d_udp_port_mtx.unlock();
}

void vita_iq_source_impl::generate_vita_tags(int output,
                                             const Vita49Packet &vp) {
  uint64_t absolute_sample_num = nitems_written(output);
  pmt::pmt_t srcid = pmt::string_to_symbol(alias());
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("absolute_sample_num"),
               pmt::from_uint64(absolute_sample_num), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("frame_counter"),
               pmt::from_long(vp.frameCount), srcid);
  add_item_tag(output, absolute_sample_num, pmt::string_to_symbol("frame_size"),
               pmt::from_long(vp.frameSize), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("packet_type"),
               pmt::from_long(vp.packetType), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("packet_counter"),
               pmt::from_long(vp.packetCount), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("packet_size"),
               pmt::from_long(vp.packetSize), srcid);
  add_item_tag(output, absolute_sample_num, pmt::string_to_symbol("stream_id"),
               pmt::from_long(vp.streamId), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("timestamp_int_type"),
               pmt::from_long(vp.timestampIntType), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("timestamp_int"),
               pmt::from_long(vp.timestampInt), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("timestamp_frac_type"),
               pmt::from_long(vp.timestampFracType), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("timestamp_frac"),
               pmt::from_uint64(vp.timestampFrac), srcid);
  if (vp.hasClassId != 0) {
    add_item_tag(output, absolute_sample_num,
                 pmt::string_to_symbol("organizationally_unique_id"),
                 pmt::from_long(vp.organizationallyUniqueId), srcid);
    add_item_tag(output, absolute_sample_num,
                 pmt::string_to_symbol("information_class_code"),
                 pmt::from_long(vp.informationClassCode), srcid);
    add_item_tag(output, absolute_sample_num,
                 pmt::string_to_symbol("packet_class_code"),
                 pmt::from_long(vp.packetClassCode), srcid);
  }
}

} /* namespace CyberRadio */
} /* namespace gr */
