/* -*- c++ -*- */
/***************************************************************************
 * \file vita_multifile_iq_source_impl.h
 *
 * \brief Implementation of vita_multifile_iq_source block.
 *
 * \author DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_CYBERRADIO_VITA_MULTIFILE_IQ_SOURCE_IMPL_H
#define INCLUDED_CYBERRADIO_VITA_MULTIFILE_IQ_SOURCE_IMPL_H

#include <CyberRadio/api.h>
#include <CyberRadio/vita_multifile_iq_source.h>
#include <LibCyberRadio/Common/Vita49Packet.h>
#include <boost/thread/mutex.hpp>
#include <string>
#include <vector>

typedef LibCyberRadio::Vita49Packet Vita49Packet;

namespace gr {
namespace CyberRadio {
class CYBERRADIO_API vita_multifile_iq_source_impl
    : virtual public vita_multifile_iq_source {
public:
  vita_multifile_iq_source_impl(const std::vector<std::string> &filespecs,
                                bool alphabetical, int vita_type,
                                size_t payload_size, size_t vita_header_size,
                                size_t vita_tail_size, bool byte_swapped,
                                bool iq_swapped, float iq_scale_factor,
                                bool repeat, bool terminate_at_end, bool tagged,
                                bool debug);
  ~vita_multifile_iq_source_impl();
  void open(const std::vector<std::string> &filespecs, bool alphabetical,
            bool repeat, bool terminate_at_end);
  void close();
  void set_iq_scale_factor(float iq_scale_factor);
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
  float get_realtime_sample_rate();

protected:
  void open_immediate(const std::vector<std::string> &filespecs,
                      bool alphabetical, bool repeat, bool terminate_at_end);
  void close_immediate();
  void open_file_immediate();
  void close_file_immediate();
  void next_file_immediate();
  int read_output_items_immediate(gr_complex *out);
  void generate_vita_tags(int output, const Vita49Packet &vp);
  int debug(const char *format, ...);

protected:
  // From block configuration
  bool d_alphabetical;
  int d_vita_type;
  size_t d_payload_size; // maximum transmission unit (packet length)
  size_t d_vita_header_size;
  size_t d_vita_tail_size;
  bool d_byte_swapped;
  bool d_iq_swapped;
  float d_iq_scale_factor;
  bool d_repeat;
  bool d_terminate_at_end;
  bool d_tagged;
  bool d_debug;
  // Internal state data
  std::vector<std::string> d_filenames;
  size_t d_packet_size;
  int d_filename_index;
  FILE *d_fp;
  boost::mutex d_fp_mutex;
  unsigned char *d_buffer;
  int d_buffer_offset;
  bool d_packet_data_available;
  uint64_t d_absolute_packet_num;
  float d_realtime_sample_rate;
  long d_realtime_sample_count;
  time_t d_realtime_last_time;
};

} /* namespace CyberRadio */
} /* namespace gr */

#endif /* INCLUDED_CYBERRADIO_VITA_MULTIFILE_IQ_SOURCE_IMPL_H */
