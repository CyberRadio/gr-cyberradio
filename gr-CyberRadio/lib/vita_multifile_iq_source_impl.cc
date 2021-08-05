/* -*- c++ -*- */
/***************************************************************************
 * \file vita_multifile_iq_source_impl.cpp
 *
 * \brief Implementation of vita_multifile_iq_source block.
 *
 * \author DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "vita_multifile_iq_source_impl.h"
#include <algorithm>
#include <cstdarg>
#include <cstdio>
#include <fcntl.h>
#include <glob.h>
#include <gnuradio/io_signature.h>
#include <gnuradio/thread/thread.h>
#include <iostream>
#include <stdexcept>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <volk/volk.h>

// win32 (mingw/msvc) specific
#ifdef HAVE_IO_H
#include <io.h>
#endif
#ifdef O_BINARY
#define OUR_O_BINARY O_BINARY
#else
#define OUR_O_BINARY 0
#endif
// should be handled via configure
#ifdef O_LARGEFILE
#define OUR_O_LARGEFILE O_LARGEFILE
#else
#define OUR_O_LARGEFILE 0
#endif

namespace gr {
namespace CyberRadio {
vita_multifile_iq_source::sptr vita_multifile_iq_source::make(
    const std::vector<std::string> &filespecs, bool alphabetical, int vita_type,
    size_t payload_size, size_t vita_header_size, size_t vita_tail_size,
    bool byte_swapped, bool iq_swapped, float iq_scale_factor, bool repeat,
    bool terminate_at_end, bool tagged, bool debug) {
  return gnuradio::get_initial_sptr(new vita_multifile_iq_source_impl(
      filespecs, alphabetical, vita_type, payload_size, vita_header_size,
      vita_tail_size, byte_swapped, iq_swapped, iq_scale_factor, repeat,
      terminate_at_end, tagged, debug));
}

vita_multifile_iq_source_impl::vita_multifile_iq_source_impl(
    const std::vector<std::string> &filespecs, bool alphabetical, int vita_type,
    size_t payload_size, size_t vita_header_size, size_t vita_tail_size,
    bool byte_swapped, bool iq_swapped, float iq_scale_factor, bool repeat,
    bool terminate_at_end, bool tagged, bool debug)
    : gr::sync_block("[CyberRadio] VITA Multi-File I/Q Source",
                     io_signature::make(0, 0, 0),
                     io_signature::make(1, 1, sizeof(gr_complex))),
      d_alphabetical(alphabetical), d_vita_type(vita_type),
      d_payload_size(payload_size), d_vita_header_size(vita_header_size),
      d_vita_tail_size(vita_tail_size), d_byte_swapped(byte_swapped),
      d_iq_swapped(iq_swapped), d_iq_scale_factor(iq_scale_factor),
      d_repeat(repeat), d_terminate_at_end(terminate_at_end), d_tagged(tagged),
      d_debug(debug),
      d_packet_size(vita_header_size + payload_size + vita_tail_size),
      d_filename_index(-1), d_fp(NULL), d_buffer(NULL), d_buffer_offset(0),
      d_packet_data_available(false), d_absolute_packet_num(0),
      d_realtime_sample_rate(0.0), d_realtime_sample_count(0),
      d_realtime_last_time(time(NULL)) {
  // Cap number of output items requested to the number of samples
  // we can get out of one VITA payload
  set_min_noutput_items(d_payload_size / sizeof(unsigned short) / 2);
  set_max_noutput_items(d_payload_size / sizeof(unsigned short) / 2);
  // Allocate the packet receive buffer
  d_buffer = new unsigned char[d_packet_size];
  memset(d_buffer, 0, d_packet_size);
  // Do the open action
  open_immediate(filespecs, alphabetical, repeat, terminate_at_end);
}

vita_multifile_iq_source_impl::~vita_multifile_iq_source_impl() {
  // Do the close action
  close_immediate();
  // Deallocate the buffer
  if (d_buffer != NULL)
    delete d_buffer;
}

void vita_multifile_iq_source_impl::open(
    const std::vector<std::string> &filespecs, bool alphabetical, bool repeat,
    bool terminate_at_end) {
  // Obtain exclusive access for duration of this function
  gr::thread::scoped_lock lock(d_fp_mutex);
  // Do the open action
  open_immediate(filespecs, alphabetical, repeat, terminate_at_end);
}

void vita_multifile_iq_source_impl::close() {
  // Obtain exclusive access for duration of this function
  gr::thread::scoped_lock lock(d_fp_mutex);
  // Do the close action
  close_immediate();
}

void vita_multifile_iq_source_impl::set_iq_scale_factor(float iq_scale_factor) {
  d_iq_scale_factor = iq_scale_factor;
}

int vita_multifile_iq_source_impl::work(int noutput_items,
                                        gr_vector_const_void_star &input_items,
                                        gr_vector_void_star &output_items) {
  // Get output buffer
  gr_complex *out = (gr_complex *)output_items[0];
  // Items processed counter
  int noutput_items_processed = 0;
  // Do we have a readable file?
  if ((d_fp != NULL) && (d_filename_index != -1)) {
    // Obtain exclusive access for duration of this function
    gr::thread::scoped_lock lock(d_fp_mutex);
    noutput_items_processed = read_output_items_immediate(out);
  }
  // If the terminate at end flag is set and we are not repeating,
  // return WORK_DONE to terminate the flowgraph if we have
  // reached the end of useable data.
  else if (!d_repeat && d_terminate_at_end) {
    debug("Terminating due to end of useable data\n");
    noutput_items_processed = WORK_DONE;
  }
  // Otherwise, generate (complex) zeros
  else {
    for (int sample = 0; sample < noutput_items; sample++) {
      out[sample].real(0);
      out[sample].imag(0);
    }
    noutput_items_processed = noutput_items;
  }
  //      if (d_debug)
  //        fprintf(stderr, "%04d/%04d ", noutput_items,
  //            noutput_items_processed);
  return noutput_items_processed;
}

void vita_multifile_iq_source_impl::open_immediate(
    const std::vector<std::string> &filespecs, bool alphabetical, bool repeat,
    bool terminate_at_end) {
  // Close any open files and empty the file name list
  close_immediate();
  // Iterate over the file spec list and translate them into
  // file names
  glob_t gbuff;
  int i;
  for (std::vector<std::string>::const_iterator it = filespecs.begin();
       it != filespecs.end(); it++) {
    glob(it->c_str(), GLOB_NOSORT | GLOB_NOCHECK, NULL, &gbuff);
    for (i = 0; i < gbuff.gl_pathc; i++) {
      if (!access(gbuff.gl_pathv[i], R_OK))
        d_filenames.push_back(gbuff.gl_pathv[i]);
    }
    globfree(&gbuff);
  }
  // Check to see if we have any valid file names in the list
  if (d_filenames.size() > 0) {
    // Set file sequence flags
    d_alphabetical = alphabetical;
    d_repeat = repeat;
    d_terminate_at_end = terminate_at_end;
    // Sort if alphabetical order
    if (d_alphabetical)
      std::sort(d_filenames.begin(), d_filenames.end());
    // Open the first file in the list
    next_file_immediate();
  }
}

void vita_multifile_iq_source_impl::close_immediate() {
  // If we already have an open file, close it
  close_file_immediate();
  // Clear any pre-existing file name list
  if (d_filenames.size() > 0)
    d_filenames.clear();
  // Reset file name index
  d_filename_index = -1;
}

void vita_multifile_iq_source_impl::open_file_immediate() {
  // Attempt to open the new file.  The attempt uses open(2) so
  // that we can take advantage of large files.
  int fd = ::open(d_filenames[d_filename_index].c_str(),
                  O_RDONLY | OUR_O_LARGEFILE | OUR_O_BINARY);
  if (fd >= 0) {
    d_fp = fdopen(fd, "rb");
    if (d_fp != NULL) {
      setbuf(d_fp, NULL);
    } else {
      // Don't leak file descriptor if fdopen fails
      ::close(fd);
    }
  }
}

void vita_multifile_iq_source_impl::close_file_immediate() {
  // If we already have an open file, close it
  if (d_fp != NULL) {
    debug("Close opened file\n");
    fclose(d_fp);
    d_fp = NULL;
  }
}

void vita_multifile_iq_source_impl::next_file_immediate() {
  // Close already opened file
  close_file_immediate();
  // Determine next file index
  d_filename_index++;
  // -- Did we run out of files?
  if (d_filename_index >= (int)d_filenames.size()) {
    // -- Are we repeating?
    if (d_repeat) {
      d_filename_index = 0;
      // Reset the buffer
      d_buffer_offset = 0;
      memset(d_buffer, 0, d_packet_size);
    } else
      d_filename_index = -1;
  }
  debug("Next file name index: %d\n", d_filename_index);
  // Open the file at the file index, if available
  if (d_filename_index != -1) {
    debug("Open file: %s\n", d_filenames[d_filename_index].c_str());
    open_file_immediate();
  }
}

int vita_multifile_iq_source_impl::read_output_items_immediate(
    gr_complex *out) {
  int noutput_items_processed = 0;
  int bytes_read = 0;
  int max_bytes_to_read = 0;
  // Number of samples in a given data packet
  int samples_in_packet = d_payload_size / sizeof(unsigned short) / 2;
  // Loop over files and try to read in a full VITA packet
  // -- If using VITA framing, and if no data has been read into the
  //    buffer, read one byte at a time to find a VITA header word
  //    first.
  if (d_vita_type == 0) {
    d_packet_data_available = true;
  } else if (d_buffer_offset == 0) {
    uint32_t tmp;
    // debug("Packet start check: %08x\n", ftell(d_fp));
    bytes_read = fread((void *)&tmp, sizeof(uint32_t), 1, d_fp);
    // debug("-- Bytes read: %d\n", bytes_read);
    if (bytes_read == 1) {
      // debug("-- Word read: %08x\n", tmp);
      // Apply byte-swapping if needed
      if (d_byte_swapped)
        volk_32u_byteswap(&tmp, 1);
      // debug("-- Word after byte-swapping: %08x\n", tmp);
      if (tmp == 0x56524C50) {
        d_packet_data_available = true;
        fseek(d_fp, -sizeof(uint32_t), SEEK_CUR);
        // debug("Packet start found: %08x\n", ftell(d_fp));
      }
    }
  }
  if (d_packet_data_available) {
    do {
      max_bytes_to_read = d_packet_size - d_buffer_offset;
      bytes_read = fread((void *)(d_buffer + d_buffer_offset),
                         sizeof(unsigned char), max_bytes_to_read, d_fp);
      d_buffer_offset += bytes_read;
      if (bytes_read < max_bytes_to_read)
        next_file_immediate();
    } while ((d_filename_index != -1) && (d_buffer_offset < d_packet_size));
  }
  // Continue processing if we did get a full VITA packet
  if (d_buffer_offset >= d_packet_size) {
    // Use the VITA packet to populate output items
    Vita49Packet vp(d_vita_type, d_payload_size, d_vita_header_size,
                    d_vita_tail_size, d_byte_swapped, d_iq_swapped, d_buffer,
                    d_packet_size);
    // Copy the packet's sample data to the correct output stream
#if 0
		for (int sample = 0; sample < samples_in_packet; sample++) {
			out[sample].real(vp.getSampleI(sample) * d_iq_scale_factor);
			out[sample].imag(vp.getSampleQ(sample) * d_iq_scale_factor);
		}
#else
    // This should significantly decrease CPU usage - PKN
    // *2 because each complex sample results in 2 pieces of data
    volk_16i_s32f_convert_32f((float *)out, vp.sampleData,
                              1 / d_iq_scale_factor, samples_in_packet * 2);
#endif
    // Do tagging on the output stream if desired and if
    // VITA 49 frames are being received
    if (d_tagged && (d_vita_type != 0)) {
      //          debug("VITA: timestamp_int=%lu  timestamp_frac=%llu\n",
      //              vp.timestampInt, vp.timestampFrac);
      generate_vita_tags(0, vp);
    }
    noutput_items_processed += samples_in_packet;
    // Calculate real-time sample rate
    time_t now = time(NULL);
    if (now != d_realtime_last_time) {
      d_realtime_sample_rate = (float)d_realtime_sample_count;
      d_realtime_sample_count = noutput_items_processed;
      d_realtime_last_time = now;
    } else {
      d_realtime_sample_count += noutput_items_processed;
    }
    // Reset the buffer
    d_buffer_offset = 0;
    memset(d_buffer, 0, d_packet_size);
    // Increment absolute packet counter
    d_absolute_packet_num++;
  }
  return noutput_items_processed;
}

float vita_multifile_iq_source_impl::get_realtime_sample_rate() {
  return d_realtime_sample_rate;
}

void vita_multifile_iq_source_impl::generate_vita_tags(int output,
                                                       const Vita49Packet &vp) {
  uint64_t absolute_sample_num = nitems_written(output);
  pmt::pmt_t srcid = pmt::string_to_symbol(alias());
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("absolute_sample_num"),
               pmt::from_uint64(absolute_sample_num), srcid);
  add_item_tag(output, absolute_sample_num,
               pmt::string_to_symbol("absolute_packet_num"),
               pmt::from_uint64(d_absolute_packet_num), srcid);
  add_item_tag(output, absolute_sample_num, pmt::string_to_symbol("filename"),
               pmt::string_to_symbol(d_filenames[d_filename_index]), srcid);
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

int vita_multifile_iq_source_impl::debug(const char *format, ...) {
  int ret = 0;
  if (d_debug) {
    ret = printf("[%s] ", name().c_str());
    if (ret >= 0) {
      va_list ap;
      va_start(ap, format);
      ret = vprintf(format, ap);
      va_end(ap);
    }
  }
  return ret;
}

} /* namespace CyberRadio */
} /* namespace gr */
