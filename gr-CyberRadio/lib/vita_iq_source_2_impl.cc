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

/*

    One channel VITA stream:
    1 vector output of packet_size/2 shorts, including VITA in data.
    1 vector output of 2*payload_size / 8 complex, no VITA in data, 
      optionally tagged with VITA.

    Interleaved coherent VITA stream:
    1 vector output of packet_size/2 shorts, including VITA in data.
    6 vector outputs 2*payload_size / (6 * 8) complex, VITA tags optionally 
      on 1st complex output.

    VITA tags are not on every packet, tagging happens once per call to work().
    Short to complex scale factor hard-coded to 32767.
    Receive buffer size set/get-able.  May need to change sysctl net.core.rmem_max
    Checks for dropped packets when VITA frame count is available.

    Other options:
    - Raw data channel optional.
    - VITA in raw data channel optional.
    - Non-vector output without a raw data output.
    - Vector output of shorts on each channel. (Conversion to complex done externally).
    - Settable scale factor.
    - Non-vector output including raw data channel.  Different output lengths per channel
        per call to work().
    - Is there a way to see dropped packets if there is no VITA ?
    
    Issues:
    - In coherent mode, channel 1 doesn't always appear in the first interleaved slot.
      This may be fixable by changing the order that receiver configuration happens.
    - In coherent mode, the timestamp seems to increase by 30 seconds in a 5-second 
      interval.

      This can be fixed by disabling all the channels before configuring.
      The receiver can be put in a strange state, but it is avoidable,

    - Some number of packets are dropped just after reading starts.  To avoid this,
      this component is deliberately dropping the first 100 packets (1500 in coherent
      mode) so the dropped count will start at 0.  With a big enough receive buffer size,
      packets are not dropped after the first ones.
    
    Where does this get checked in ?
    

*/

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "vita_iq_source_2_impl.h"
#include <gnuradio/math.h>
#include <stdexcept>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <time.h>

#include <iostream>

#include <volk/volk.h>


namespace gr
{
  namespace CyberRadio
  {
    vita_iq_source_2::sptr
    vita_iq_source_2::make(int vitaType, 
                          size_t payloadSize, 
                          size_t vitaHeaderSize, 
                          size_t vitaTailSize, 
                          bool byteSwapped, 
                          bool iqSwapped, 
                          const std::string& host, 
                          int port, 
                          bool debug, 
                          bool tagOutput, 
                          bool coherent)
    {
      return gnuradio::get_initial_sptr
        (new vita_iq_source_2_impl(vitaType, payloadSize, 
         vitaHeaderSize, vitaTailSize, byteSwapped, iqSwapped, 
         host, port, debug, tagOutput, coherent));
    }

    /*
     * The private constructor
     */
    vita_iq_source_2_impl::vita_iq_source_2_impl(int vitaType, 
                                               size_t payloadSize, 
                                               size_t vitaHeaderSize, 
                                               size_t vitaTailSize, 
                                               bool byteSwapped, 
                                               bool iqSwapped, 
                                               const std::string& host, 
                                               int port, 
                                               bool debug, 
                                               bool tagOutput, 
                                               bool coherent)
      : gr::sync_block("vita_iq_source_2",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0)),

              d_vitaType(vitaType),
              d_payloadSize(payloadSize),
              d_vitaHeaderSize(vitaHeaderSize),
              d_vitaTailSize(vitaTailSize),
              d_byteSwapped(byteSwapped),
              d_iqSwapped(iqSwapped),
              d_host(host),
              d_port(port),
              d_debug(debug),
              d_tagOutput(tagOutput),
              d_coherent(coherent),
              d_scale(32767)
    {
      d_packetSize = (vitaType == 0 ? payloadSize : vitaHeaderSize + payloadSize + vitaTailSize);
      d_connected = false;
      if (!coherent)  {
          set_output_signature(
              gr::io_signature::make2(0, 2, d_packetSize, 2*payloadSize));
      }
      else  {
          set_output_signature(
              gr::io_signature::make2(0, 7, d_packetSize, 2*payloadSize/6));
      }
      //set_output_multiple(d_packetSize);

      d_tmpbuf = 0;
      d_tmpbuf2 = 0;
      d_tmpbuf_size = 0;
      d_frame_count = 0xffff;
      d_dropped = 0;

      if (d_coherent)  {
          d_skip_packets = 1500;
      }
      else  {
          d_skip_packets = 100;
      }

      // Give us some more room to play.
      d_rxbuf = new char[50*d_packetSize];
      d_residbuf = new char[50*d_packetSize];

      std::cout << "\n\nByte swapped? " << d_byteSwapped << " & IQ Swapped? " << d_iqSwapped << ".\n\n" << std::endl;
      GR_LOG_DEBUG(d_logger, "construction");
      this->debug("construction\n");
        this->debug("-- packetSize = %d\n", d_packetSize);
        this->debug("-- payloadSize = %d\n", d_payloadSize);
        this->debug("-- host = %s\n", host.c_str());
        this->debug("-- port = %d\n", port);
            this->debug("-- byteSwapped = %i\n", byteSwapped);
            this->debug("-- iqSwapped = %i\n", iqSwapped);
            this->debug("-- tagOutput = %i\n", tagOutput);
            this->debug("-- coherent = %i\n", coherent);
      this->connect(host, port);
            this->debug("-- rcvr buffer size: %i\n", this->get_receive_buffer_size());
    }

    /*
     * Our virtual destructor.
     */
    vita_iq_source_2_impl::~vita_iq_source_2_impl()
    {
      if (d_connected)
          disconnect();

      delete [] d_rxbuf;
      delete [] d_residbuf;

      if (d_tmpbuf)
          delete [] d_tmpbuf;
      if (d_tmpbuf2)
          delete [] d_tmpbuf2;
    }

    void
    vita_iq_source_2_impl::connect(const std::string &host, int port)
    {
      GR_LOG_DEBUG(d_logger, "connect");
      if(d_connected)
        disconnect();

      d_host = host;
      d_port = static_cast<unsigned short>(port);

      std::string s_port;
      s_port = (boost::format("%d")%d_port).str();

      if(host.size() > 0) {
        boost::asio::ip::udp::resolver resolver(d_io_service);
        boost::asio::ip::udp::resolver::query query(
            boost::asio::ip::udp::v4(),
            d_host, s_port,
            boost::asio::ip::resolver_query_base::passive);
        d_endpoint = *resolver.resolve(query);

        d_socket = new boost::asio::ip::udp::socket(d_io_service);
        d_socket->open(d_endpoint.protocol());

        boost::asio::socket_base::linger loption(true, 0);
        d_socket->set_option(loption);

        boost::asio::socket_base::reuse_address roption(true);
        d_socket->set_option(roption);

        d_socket->bind(d_endpoint);

  //      start_receive();
  //      d_udp_thread = gr::thread::thread(boost::bind(&g3udp_impl::run_io_service, this));
        d_connected = true;
      }
    }

    void
    vita_iq_source_2_impl::disconnect()
    {
      //gr::thread::scoped_lock lock(d_setlock);

      GR_LOG_DEBUG(d_logger, "disconnect");
      if(!d_connected)
        return;

      d_io_service.reset();
      d_io_service.stop();
      d_udp_thread.join();

      d_socket->close();
      delete d_socket;

      d_connected = false;
    }

    void
    vita_iq_source_2_impl::start_receive()
    {
      GR_LOG_WARN(d_logger, "start_receive");
      d_socket->async_receive_from(boost::asio::buffer((void*)d_rxbuf, d_packetSize),
              d_endpoint_rcvd,
              boost::bind(&vita_iq_source_2_impl::handle_read, this,
                  boost::asio::placeholders::error,
                  boost::asio::placeholders::bytes_transferred));
    }

    void
    vita_iq_source_2_impl::handle_read(const boost::system::error_code& error,
                                 size_t bytes_transferred)
    {

      GR_LOG_WARN(d_logger, "handle_read.");
      if(!error) {
        {
          boost::lock_guard<gr::thread::mutex> lock(d_udp_mutex);
          // Make sure we never go beyond the boundary of the
          // residual buffer.  This will just drop the last bit of
          // data in the buffer if we've run out of room.
          if((int)(d_residual + bytes_transferred) >= (50*d_packetSize)) {
            char msg[100];
            sprintf(msg,"d_packetSize %d bytes_transferred %d",
                (int)d_packetSize, (int)bytes_transferred);
            GR_LOG_WARN(d_logger, msg);
            GR_LOG_WARN(d_logger, "TOO much data; dropping packet.");
          }
          else {
            // otherwise, copy received data into local buffer for
            // copying later.
            memcpy(d_residbuf+d_residual, d_rxbuf, bytes_transferred);
            d_residual += bytes_transferred;
          }
          d_cond_wait.notify_one();
        }
      }
      start_receive();
    }

    void 
    vita_iq_source_2_impl::set_receive_buffer_size(int size)
    {
        boost::asio::socket_base::receive_buffer_size option(size);
        d_socket->set_option(option);
    }

    int
    vita_iq_source_2_impl::get_receive_buffer_size(void)
    {
        boost::asio::socket_base::receive_buffer_size option;
        d_socket->get_option(option);
        int size = option.value();
        return size;
    }

    void
    vita_iq_source_2_impl::set_scale_factor(int scale)
    {
        d_scale = scale;
    }

    int
    vita_iq_source_2_impl::get_scale_factor()
    {
        return d_scale;
    }

    static int count = 0;

    int 
    vita_iq_source_2_impl::_parse_vita_and_tag(char* output_buffer,
                                      int packetNumber)
    {
        char* out = output_buffer;
        //  Check header ID.
        if ((out[0] != 'P') || (out[1] != 'L') ||
            (out[2] != 'R') || (out[3] != 'V'))  {
            char msg[100];
            sprintf(msg, "Wrong packet header: %02x%02x%02x%02x  packet count: %i",
                (uint16_t)out[0], (uint16_t)out[1], (uint16_t)out[2], 
                (uint16_t)out[3], count);
            GR_LOG_WARN(d_logger, msg);
        } 
        //  Check for lost frames.
        unsigned short int frame_count = ((out[7] << 4) | (out[6]&0xf0)>>4) & 0xfff;
        int old_frame_count = d_frame_count;                          
        int dropped = 0;
        if (old_frame_count == 0xffff)  {
            old_frame_count = frame_count;
        }
        else  {
            old_frame_count++;
            if (old_frame_count < frame_count)  {
                dropped = frame_count - old_frame_count;
                old_frame_count = frame_count;
            }
            else if (old_frame_count > 0xfff)  {
                old_frame_count &= 0xfff;
            }
            else if (old_frame_count > frame_count)  {
                dropped = 0xfff - (old_frame_count - frame_count);
                old_frame_count = frame_count;
            }
            d_dropped += dropped;
        }
        d_frame_count = old_frame_count;

        //  Get other VITA values and add tags to the stream.
        if ((packetNumber == 1) && (d_tagOutput))  {
            int packet_count = (out[10] & 0xf);
            char time_frac_type = (out[10] & 0x30) >> 4;
            long int stream_id = *((unsigned int*)&out[12]);
            long int time_int = *((unsigned int*)&out[16]);
            long unsigned int time_frac_msw = *((unsigned int*)&out[20]);
            long unsigned int time_frac_lsw = *((unsigned int*)&out[24]);
            uint64_t time_frac_i = ((uint64_t)time_frac_msw << 32) |
                time_frac_lsw;

            double time_frac = (double)time_frac_i;
            if (time_frac_type == 2)  {
                // time_frac is picoseconds.
                time_frac /= 1.e12;
            }
            else  {
                // time_frac is sample count
                time_frac /= 102.4e6;
            }
            //  Add tags timestamp, packet_count, source_id.
            uint64_t tag_offset = nitems_written(1);
            pmt::pmt_t timestamp = 
                pmt::cons(pmt::mp(time_int),
                pmt::mp(time_frac));
            add_item_tag(1, tag_offset, 
                pmt::intern("timestamp"), timestamp);
            add_item_tag(1, tag_offset, 
                pmt::intern("frame_count"), 
                pmt::mp(frame_count));
            add_item_tag(1, tag_offset, 
                pmt::intern("packet_count"), 
                pmt::mp(packet_count));
            add_item_tag(1, tag_offset, 
                pmt::intern("source_id"), 
                pmt::mp(stream_id));
            add_item_tag(1, tag_offset,
                pmt::intern("dropped"),
                pmt::mp(dropped));
            add_item_tag(1, tag_offset,
                pmt::intern("dropped_total"),
                pmt::mp(d_dropped));
        }
        int ret = 1;
        return ret;
    }

    int 
    vita_iq_source_2_impl::_read_socket_data(int noutput_items, 
                                      char* output_buffer)
    {
        if(d_residual < 0)
            return -1;
        
        char* out = output_buffer;
        int packetsRead = 0;
        while (packetsRead < noutput_items)  {
            int num_received = d_socket->receive(boost::asio::buffer((void*)out, d_packetSize)); 
            while (num_received < d_packetSize)
            {
                num_received += d_socket->receive(boost::asio::buffer((void*)out, 
                        d_packetSize-num_received));
          
            }
            packetsRead++;
            if ((d_vitaType != 0) && (count >= d_skip_packets))  {
                _parse_vita_and_tag(out, packetsRead);
            }
            out += d_packetSize;
        }

        return packetsRead;
    }

    int
    vita_iq_source_2_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
        char *out = (char*)output_items[0];
        size_t payload_size = d_payloadSize;
        size_t hdr_size = d_vitaHeaderSize;
        size_t tail_size = d_vitaTailSize;
        if (d_vitaType == 0)  {
            hdr_size = 0;
            tail_size = 0;
        }

        //  noutput_items is the number of packet_size vector items allocated for channel 0.
        int packetsRead = _read_socket_data(noutput_items, out);

        //  Throw away the first 100 packets (1500 in coherent mode).
        if (count < d_skip_packets)  {
            count += noutput_items;
            return 0;
        }
        noutput_items = packetsRead;
        count += packetsRead;

        if (packetsRead == 0)  return 0;

        char* in = out;
        //  get buffer memory.
        if ((2*noutput_items*d_payloadSize) > d_tmpbuf_size)  {
            d_tmpbuf_size = noutput_items * d_payloadSize;
            if (d_tmpbuf)  delete [] d_tmpbuf;
            d_tmpbuf = new char[d_tmpbuf_size];

            if (d_coherent)  {
                if (d_tmpbuf2)  delete [] d_tmpbuf2;
                d_tmpbuf2 = new char[2*d_tmpbuf_size];
            }
        }

        //  copy packet data to buffer, remove VITA.
        out = d_tmpbuf;
        for (int i=0; i<packetsRead; i++)  {
            in += hdr_size;
            memcpy(out, in, payload_size);
            out += payload_size;
            in += payload_size + tail_size;
        }
        out = d_tmpbuf;

        int short_count = (payload_size * packetsRead) / sizeof(uint16_t);
        //  do swapping.
        if (d_byteSwapped)  {
            if (d_iqSwapped)  {
                volk_32u_byteswap((uint32_t*)out, short_count/2);
            }
            else  {
                volk_16u_byteswap((uint16_t*)out, short_count);
            }
        }
        else  {
            if (d_iqSwapped)  {
                volk_32u_byteswap((uint32_t*)out, short_count/2);
                volk_16u_byteswap((uint16_t*)out, short_count);
            }
        }

        //  convert short to float and scale.
        const short* s_buf = (const short *)out;
        if (d_coherent)  {
            volk_16i_s32f_convert_32f((float *)d_tmpbuf2, s_buf, d_scale, short_count);
        }
        else  {
            volk_16i_s32f_convert_32f((float *)output_items[1], s_buf, d_scale, short_count);
        }

        //  deinterleave coherent channels.
        if (d_coherent)  {
            for (int i=0; i<6; i++)  {
                uint64_t* in = (uint64_t*)d_tmpbuf2;
                in += i;
                uint64_t* out = (uint64_t*)output_items[i+1];
                for (int j=0; j<(2*payload_size*packetsRead)/(6*sizeof(uint64_t)); j++)  {
                    out[j] = *in;
                    in += 6;
                }
            }
        }
        
        //~ if (d_iqSwapped)  {
            //~ for (int j=0; j<(payload_size;) {
        //~ 
      //~ }
        //~ }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  int vita_iq_source_2_impl::debug(const char *format, ...)
  {
    int ret = 0;
    if (d_debug)
    {
      ret = printf("[%s] ", this->name().c_str());
      if (ret >= 0)
      {
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

