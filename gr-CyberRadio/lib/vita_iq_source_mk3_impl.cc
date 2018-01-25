/* -*- c++ -*- */
/***************************************************************************
 * \file vita_iq_source_mk3_impl.cpp
 *
 * \brief Implementation of a generic VITA 49-compatible I/Q data source
 *    block (Mk3).
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "CyberRadio/vita_iq_source_mk3.h"
#include "vita_iq_source_mk3_impl.h"
#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include <stdarg.h>
#include <string.h>
#include <algorithm>
#include <time.h>
#include <stdio.h>


namespace gr
{
  namespace CyberRadio
  {
    vita_iq_source_mk3::sptr vita_iq_source_mk3::make(int vita_type,
                                              size_t payload_size,
                                              size_t vita_header_size,
                                              size_t vita_tail_size,
                                              bool byte_swapped,
                                              bool iq_swapped,
                        float iq_scale_factor,
                        const std::string& host,
                        unsigned short port,
                        bool ddc_coherent,
                        int num_outputs,
                        bool tagged,
                        bool debug)
    {
      return gnuradio::get_initial_sptr(new vita_iq_source_mk3_impl(
            vita_type, payload_size, vita_header_size,
          vita_tail_size, byte_swapped, iq_swapped,
          iq_scale_factor, host, port, ddc_coherent, num_outputs,
          tagged, debug) );
    }

    /*
     * The private constructor
     */
    vita_iq_source_mk3_impl::vita_iq_source_mk3_impl(int vita_type,
                       size_t payload_size,
                       size_t vita_header_size,
                       size_t vita_tail_size,
                       bool byte_swapped,
                       bool iq_swapped,
                       float iq_scale_factor,
                       const std::string& host,
                       unsigned short port,
                       bool ddc_coherent,
                       int num_outputs,
                       bool tagged,
                       bool debug)
      : gr::sync_interpolator("[CyberRadio] VITA I/Q Source (Mk3)",
          gr::io_signature::make(0, 0, 0),
          gr::io_signature::make(0, 0, 0),
          1),
      LibCyberRadio::Debuggable(debug, "[CyberRadio] VITA I/Q Source (Mk3)", stdout),
      d_source(NULL),
      d_iq_scale_factor(iq_scale_factor),
        d_ddc_coherent(ddc_coherent),
      d_num_outputs(ddc_coherent ? num_outputs : 1),
      // Packet vector size is set here.  It's intended for performance tuning purposes.
      d_vita_packet_vec_size(10),
      d_tagged(tagged)
    {
      // Create the source
      d_source = new LibCyberRadio::VitaIqSource(
          /* const std::string& name */ "[CyberRadio] VITA I/Q Source (Mk3)",
          /* int vita_type */ vita_type,
          /* size_t payload_size */ payload_size,
          /* size_t vita_header_size */ vita_header_size,
          /* size_t vita_tail_size */ vita_tail_size,
          /* bool byte_swapped */ byte_swapped,
          /* bool iq_swapped */ iq_swapped,
          /* const std::string& host */ host,
          /* unsigned short port */ port,
          /* bool debug */ debug);
      // Determine packet size
      d_packet_size = d_source->getPacketSize();
      // Determine samples per packet and samples per output (divided equally between
      // outputs if in DDC-coherent mode)
      d_samples_per_packet = d_source->getPayloadSize() / sizeof(unsigned short) / 2;
      d_samples_per_output = d_samples_per_packet / d_num_outputs;
      // Set interpolation ratio to samples per output
      this->set_interpolation(d_samples_per_output);
      // Create the output signature.  There is one stream per output, each configured
      // as a complex stream.
      this->set_output_signature(gr::io_signature::make(1, d_num_outputs, sizeof(gr_complex)));
      // Initialize data rate calculation stuff
      for (int output = 0; output < d_num_outputs; output++)
      {
        d_realtime_sample_rates.push_back(0.0);
        d_realtime_sample_counts.push_back(0);
      }
      d_realtime_last_time = time(NULL);
      // Pre-allocate a vector to hold VITA 49 packet data coming from the source
      d_vita_packets.reserve(d_vita_packet_vec_size);
    }

    /*
     * Our virtual destructor.
     */
    vita_iq_source_mk3_impl::~vita_iq_source_mk3_impl()
    {
      // Destroy the source
      delete d_source;
    }

    int vita_iq_source_mk3_impl::work(int noutput_items,
                            gr_vector_const_void_star &input_items,
                            gr_vector_void_star &output_items)
    {
      // Pointer to an output buffer.  This will be reassigned as the output
      // being manipulated changes.
      gr_complex *out;
      // Number of output items processed.  This is the number of samples dispatched
      // to each output stream.
      int noutput_items_processed = 0;
      // Loop counters
      int packet;
      int output;
      int sample;
      int offset;
      this->debug("noutput_items = %d\n", noutput_items);
      this->debug("d_samples_per_packet = %d\n", d_samples_per_packet);
      this->debug("d_samples_per_output = %d\n", d_samples_per_output);
      // Get the incoming data from the source.  We will limit the number of packets
      // to either enough to produce the number of output items requested, or the buffer
      // size, whichever is smaller.
      int num_packets = d_source->getPackets( std::min(noutput_items / d_samples_per_output,
                                                   d_vita_packet_vec_size),
                                          d_vita_packets );
      this->debug("num_packets = %d\n", num_packets);
      // Loop over each packet received, and dispatch the samples to each output as required.
      for (packet = 0; packet < num_packets; packet++)
      {
        this->debug("packet = %d\n", packet);
        this->debug("%s\n", d_vita_packets[packet].dump().c_str());
        for (sample = 0; sample < d_samples_per_packet; sample++)
        {
          this->debug("-- sample = %d\n", sample);
          // Calculate the output that this sample should go to
          output = sample % d_num_outputs;
          // Calculate the sample's offset within the output buffer
          offset = (packet * d_samples_per_packet + sample) / d_num_outputs;
          this->debug("   -- output = %d   offset = %d\n", output, offset);
          // Calculate pointer to output buffer
          this->debug("   -- buffer fill start\n");
          out = (gr_complex*)output_items[output];
          out[offset].real(d_vita_packets[packet].getSampleI(sample) * d_iq_scale_factor);
          out[offset].imag(d_vita_packets[packet].getSampleQ(sample) * d_iq_scale_factor);
          this->debug("   -- buffer fill complete\n");
          // Generate VITA tags for this output under certain conditions:
          if (
             // If we want tags in the first place
             d_tagged &&
             // If VITA 49 framing is being used on the source
             (d_source->getVitaType() != 0) &&
             // If this is the first sample of the packet going to this output
             (offset == (packet * d_samples_per_packet / d_num_outputs)) )
          {
            this->debug("   -- tagging start\n");
            generate_vita_tags(output, d_vita_packets[packet]);
            this->debug("   -- tagging complete\n");
          }
        }
        // Increase number of items available
        noutput_items_processed += d_samples_per_output;
        this->debug("-- post-packet noutput_items_processed = %d\n", noutput_items_processed);
      }
      // For each output, calculate real-time sample rates.
      time_t now = time(NULL);
      if ( now != d_realtime_last_time )
      {
        for (output = 0; output < d_num_outputs; output++)
        {
          d_realtime_sample_rates[output] = (float)d_realtime_sample_counts[output];
          d_realtime_sample_counts[output] = noutput_items_processed;
        }
        d_realtime_last_time = now;
      }
      else
      {
        for (output = 0; output < d_num_outputs; output++)
        {
          d_realtime_sample_counts[output] += noutput_items_processed;
        }
      }
      this->debug("noutput_items_processed = %d\n", noutput_items_processed);
      return noutput_items_processed;
    }

    float vita_iq_source_mk3_impl::get_realtime_sample_rate(int output)
    {
      return d_realtime_sample_rates[output];
    }

    void vita_iq_source_mk3_impl::generate_vita_tags(int output,
                                                 const LibCyberRadio::Vita49Packet& vp)
    {
      uint64_t absolute_sample_num = nitems_written(output);
      pmt::pmt_t srcid = pmt::string_to_symbol(alias());
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("absolute_sample_num"),
          pmt::from_uint64(absolute_sample_num),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("frame_counter"),
          pmt::from_long(vp.frameCount),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("frame_size"),
          pmt::from_long(vp.frameSize),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("packet_type"),
          pmt::from_long(vp.packetType),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("packet_counter"),
          pmt::from_long(vp.packetCount),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("packet_size"),
          pmt::from_long(vp.packetSize),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("stream_id"),
          pmt::from_long(vp.streamId),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("timestamp_int_type"),
          pmt::from_long(vp.timestampIntType),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("timestamp_int"),
          pmt::from_long(vp.timestampInt),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("timestamp_frac_type"),
          pmt::from_long(vp.timestampFracType),
          srcid
        );
      add_item_tag(
          output,
          absolute_sample_num,
          pmt::string_to_symbol("timestamp_frac"),
          pmt::from_uint64(vp.timestampFrac),
          srcid
        );
      if ( vp.hasClassId != 0 )
      {
        add_item_tag(
            output,
            absolute_sample_num,
            pmt::string_to_symbol("organizationally_unique_id"),
            pmt::from_long(vp.organizationallyUniqueId),
            srcid
          );
        add_item_tag(
            output,
            absolute_sample_num,
            pmt::string_to_symbol("information_class_code"),
            pmt::from_long(vp.informationClassCode),
            srcid
          );
        add_item_tag(
            output,
            absolute_sample_num,
            pmt::string_to_symbol("packet_class_code"),
            pmt::from_long(vp.packetClassCode),
            srcid
          );
      }
    }

  } /* namespace CyberRadio */
  
} /* namespace gr */

