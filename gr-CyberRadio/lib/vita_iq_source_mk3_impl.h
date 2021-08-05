/* -*- c++ -*- */
/***************************************************************************
 * \file vita_iq_source_mk3_impl.h
 *
 * \brief Implementation of a generic VITA 49-compatible I/Q data source
 *    block (Mk3).
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_MK3_IMPL_H
#define INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_MK3_IMPL_H

#include "CyberRadio/vita_iq_source_mk3.h"
#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/Common/Vita49Packet.h"
#include "LibCyberRadio/Common/VitaIqSource.h"
#include <string>
#include <vector>

namespace gr {
namespace CyberRadio {

class vita_iq_source_mk3_impl : public vita_iq_source_mk3,
                                public LibCyberRadio::Debuggable {
public:
  vita_iq_source_mk3_impl(int vita_type, size_t payload_size,
                          size_t vita_header_size, size_t vita_tail_size,
                          bool byte_swapped, bool iq_swapped,
                          float iq_scale_factor, const std::string &host,
                          unsigned short port, bool ddc_coherent,
                          int num_outputs, bool tagged, bool debug);
  ~vita_iq_source_mk3_impl();
  // Where all the action really happens
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
  float get_realtime_sample_rate(int output);

protected:
  // Generate tags for an output stream from a Vita 49
  // packet
  void generate_vita_tags(int output, const LibCyberRadio::Vita49Packet &vp);

private:
  LibCyberRadio::VitaIqSource *d_source;
  size_t d_packet_size;
  float d_iq_scale_factor;
  bool d_ddc_coherent;
  int d_num_outputs;
  int d_vita_packet_vec_size;
  bool d_tagged;
  int d_samples_per_packet;
  int d_samples_per_output;
  std::vector<float> d_realtime_sample_rates;
  std::vector<long> d_realtime_sample_counts;
  time_t d_realtime_last_time;
  LibCyberRadio::Vita49PacketVector d_vita_packets;
};

} // namespace CyberRadio

} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_MK3_IMPL_H */
