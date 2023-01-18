/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "vita_udp_rx_impl.h"
#include <gnuradio/io_signature.h>
#include <arpa/inet.h>
#include <sys/socket.h> // consider boost::asio?
#include <volk/volk.h>
#include <cstring>
#include <iomanip>
#include <iostream>

namespace {
auto const control_port = pmt::mp("control");
auto const status_port = pmt::mp("status");
auto const freq_port = pmt::mp("freq");
auto const bw_port = pmt::mp("bw");

// V49 Struct Info
struct V49_308_Header {
    char p;
    char l;
    char r;
    char v;
    unsigned int frame_info;
    unsigned int packet_info;
    unsigned int stream_id;
    unsigned int class_id_1;
    unsigned int class_id_2;
    unsigned int int_timestamp;
    unsigned int frac_timestamp_msw;
    unsigned int frac_timestamp_lsw;
};

struct V49_Packet_info_Header {
    uint16_t packet_size;
    uint8_t packet_count : 4;
    uint8_t tsf : 2;
    uint8_t tsi : 2;
    uint8_t t : 1;
    uint8_t r0 : 1;
    uint8_t r1 : 1;
    uint8_t c : 1;
    uint8_t packet_type : 4;
};

struct V49_No491_wClass_Header {
    uint32_t packet_info;
    uint32_t stream_id;
    uint32_t oui;
    uint32_t class_codes;
    uint32_t int_timestamp;
    uint32_t frac_timestamp_msw;
    uint32_t frac_timestamp_lsw;
};

struct V49_Ctx_WClass_Packet {
    V49_No491_wClass_Header hdr;
    uint32_t ctx_ind;
    uint32_t bw_msw;
    uint32_t bw_lsw;
    uint32_t ref_freq_msw;
    uint32_t ref_freq_lsw;
    uint32_t ref_level;
    uint32_t gain;
    uint32_t sample_rate_msw;
    uint32_t sample_rate_lsw;
    uint32_t if_data_payload_fmt_0;
    uint32_t if_data_payload_fmt_1;
};

// VITA 49 VRT IF data packet header, no class ID
// (used without external framing on NDR354/364)
struct V49_No491_Header {
    unsigned int packet_info;
    unsigned int stream_id;
    unsigned int int_timestamp;
    unsigned int frac_timestamp_msw;
    unsigned int frac_timestamp_lsw;
};



std::map<int, float> ndr358_551_ddc_map = {
    { 0, 0.25e3 }, { 1, 0.5e3 },  { 2, 1.0e3 },  { 3, 2.0e3 },   { 4, 4.0e3 },
    { 5, 8.0e3 },  { 6, 16e3 },   { 7, 32e3 },   { 8, 64e3 },    { 9, 128e3 },
    { 10, 200e3 }, { 11, 256e3 }, { 12, 400e3 }, { 13, 1.28e6 }, { 14, 3.2e6 },
    { 15, 4e6 },   { 16, 2e6 },   { 32, 8e6 },   { 33, 8e6 },    { 34, 16e6 },
    { 35, 16e6 },  { 36, 16e6 },  { 37, 32e6 },  { 38, 32e6 },   { 39, 64e6 },
    { 40, 128e6 }
};

std::map<int, int> ndr358_551_timestamp_diffs = {
    {40, 2000} , {39, 4000} , {38, 8000} , {37, 8000} , {36, 16000},
    {35, 16000}, {34, 16000}, {33, 32000}, {32, 32000}
};

void raise_error(std::string tag, int sock)
{
    // see http://www.club.cc.cmu.edu/~cmccabe/blog_strerror.html for problems with
    // strerror. However, syserr_list and sys_nerr are deprecated, so that approach can't
    // be used
    tag.append(": ");
    char buf[256]; // long enough for any sane message

#if (_POSIX_C_SOURCE >= 200112L || _XOPEN_SOURCE >= 600) && !_GNU_SOURCE
    strerror_r(errno, buf, sizeof(buf));
    tag.append(buf);
#else
    tag.append(strerror_r(errno, buf, sizeof(buf)));
#endif

    // wait until after strerror to avoid polluting errno
    ::close(sock); // this might fail if the sock wasn't open

    throw std::runtime_error(tag);
}

} // namespace

namespace gr {
  namespace CyberRadio {
    /*!*************************************************************************
    **
    **
    ***************************************************************************/
    using output_type = gr_complex;
    vita_udp_rx::sptr vita_udp_rx::make(std::string src_ip, 
                  unsigned short port, 
                  unsigned int header_byte_offset, 
                  int samples_per_packet, 
                  int bytes_per_packet, 
                  bool swap_bytes, 
                  bool swap_iq, 
                  bool tag_packets, 
                  bool vector_output, 
                  bool uses_v491, 
                  bool narrowband, 
                  bool debug)
    {
      return gnuradio::make_block_sptr<vita_udp_rx_impl>( 
        src_ip, port, header_byte_offset, samples_per_packet, bytes_per_packet,
        swap_bytes, swap_iq, tag_packets, vector_output, uses_v491, narrowband, debug );
    }

    /*!*************************************************************************
    **
    **
    ***************************************************************************/
    vita_udp_rx_impl::vita_udp_rx_impl( std::string src_ip, 
                  unsigned short port, 
                  unsigned int header_byte_offset, 
                  int samples_per_packet, 
                  int bytes_per_packet, 
                  bool swap_bytes, 
                  bool swap_iq, 
                  bool tag_packets, 
                  bool vector_output, 
                  bool uses_v491, 
                  bool narrowband, 
                  bool debug)
      : gr::block("vita_udp_rx",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(output_type))),
      d_src_ip(src_ip),
      d_port(port),
      d_sock(-1),
      d_samples_per_packet(samples_per_packet),
      d_header_byte_offset(header_byte_offset),
      d_bytes_per_packet(bytes_per_packet),
      d_swap_bytes(swap_bytes),
      d_swap_iq(swap_iq),
      d_uses_v49_1(uses_v491),
      d_is_narrowband(narrowband),
      d_tag_packets(tag_packets),
      d_debug(debug),
      d_first_packet(true),
      d_packetCounter(0),
      d_buffer(),
      d_frac_last_timestamp( 0 ),
      d_use_vector_output( vector_output )
    {
      if( this->d_use_vector_output )
      {
        this->set_output_signature(gr::io_signature::make( 1, 1, d_samples_per_packet * sizeof(output_type) ) );
      }
        // pre-allocate the memory
      d_buffer.reserve(bytes_per_packet);

      // don't call work() until there is enough space for a whole packet
      if( !d_use_vector_output ) {
        set_output_multiple(d_samples_per_packet);
      } else {
        set_output_multiple(1);
      }

      // Create input port
      message_port_register_in(control_port);
      set_msg_handler(control_port, [this](pmt::pmt_t const& msg) { rxControlMsg(msg); });

      // Create output port
      message_port_register_out(status_port);
      // Create output port
      message_port_register_out(freq_port);
      // Create output port
      message_port_register_out(bw_port);
    }

    /*******************************************************************************
     * \brief 
     * \param  
     * \param  
     *******************************************************************************/
    auto vita_udp_rx_impl::receive_packet() -> bool
    {
        auto success = false;

        // If this is called, it's because we need to fill the buffer. Make sure it is sized,
        // then fill it
        d_buffer.resize(d_bytes_per_packet);

        auto nbytesRx = recv(d_sock, d_buffer.data(), d_buffer.size(), 0);
        if (nbytesRx == d_buffer.size()) {

            // Byte-swap the header if needed so we can read it
            if (d_swap_bytes) {
                volk_32u_byteswap(reinterpret_cast<uint32_t*>(d_buffer.data()),
                                  d_header_byte_offset / 4);
            }

            success = true;
        } else {
            std::cerr
                << "gr::CyberRadio::vita_udp_rx_impl: ERROR: received an incomplete packet. "
                << "received " << nbytesRx << " of " << d_buffer.size() << " expected.";
            d_buffer.resize(0);
        }
        return success;
    }

    /*******************************************************************************
     * \brief 
     * \param  
     * \param  
     *******************************************************************************/
    auto vita_udp_rx_impl::process_packet(gr_complex*& outP, int samples_needed) -> int
    {
        int samples_produced = 0;

        auto hdr = reinterpret_cast<V49_No491_Header*>(d_buffer.data());

        if (d_debug) {
            auto save_flags = std::cout.flags();
            auto save_fill = std::cout.fill();
            std::cout << "**** vita_udp_rx_impl(" << d_src_ip << ":" << d_port
                      << ")::process_packet() "
                      << "PACKET/N491 p_i = " << std::hex << std::setw(8) << std::setfill('0')
                      << hdr->packet_info << "    ****" << std::endl;
            std::cout.flags(save_flags);
            std::cout.fill(save_fill);
        }

        // Dropped packet handling. If the counter doesn't match the expected value, it means
        // a packet was dropped. Report it, and insert null samples into the output
        unsigned packet_counter = (hdr->packet_info >> 16) & 0x000F;

        samples_produced += handle_dropped_packet(packet_counter, outP, samples_needed);

        if (samples_produced < samples_needed) {
            tag_packet(0, samples_produced);
            samples_produced += process_IQ(outP);
        }

        return samples_produced;
    }

    /*******************************************************************************
     * \brief 
     * \param  
     * \param  
     *******************************************************************************/
    auto vita_udp_rx_impl::process_v491_packet(gr_complex*& outP) -> int
    {
        int samples_produced = 0;

        auto hdr = reinterpret_cast<V49_308_Header*>(d_buffer.data());
        if (d_debug) {
            auto save_flags = std::cout.flags();
            auto save_fill = std::cout.fill();
            std::cout << "**** vita_udp_rx_impl::process_v491_packet()"
                      << "PACKET/491 p_i = " << std::hex << std::setw(8) << std::setfill('0')
                      << hdr->packet_info << "    ****" << std::endl;
            std::cout.flags(save_flags);
            std::cout.fill(save_fill);
        }

        tag_v491_packet(0, samples_produced);
        samples_produced += process_IQ(outP);
        return samples_produced;
    }

    /*******************************************************************************
     * \brief 
     * \param  
     * \param  
     *******************************************************************************/
    auto vita_udp_rx_impl::handle_dropped_packet(unsigned packet_counter,
                                                gr_complex*& outP,
                                                int samples_needed) -> int
    {
        int samples_produced = 0;

        // assume the first packet isn't dropped :P
        if (d_first_packet) {
            d_packetCounter = packet_counter;
            d_first_packet = false;
        } else {
            if (++d_packetCounter != packet_counter) {
                txStatusMsg();

                // packets were dropped. Insert nulls
                // (someday, use GR_LOG)
                std::cout
                    << "gr::CyberRadio::vita_udp_rx_impl: packet loss detected: expected "
                    << d_packetCounter << ", received " << packet_counter << std::endl;

                while (d_packetCounter != packet_counter and
                      samples_produced < samples_needed) {
                    std::fill_n(outP, d_samples_per_packet, gr_complex(0));
                    outP += d_samples_per_packet;
                    if( d_use_vector_output )
                    {
                        samples_produced += 1;
                    } else {
                        samples_produced += d_samples_per_packet;
                    }
                    produce(0, samples_produced);
                    ++d_packetCounter;
                }
            }
        }
        return samples_produced;
    }

    /*******************************************************************************
     * \brief 
     * \param  
     * \param  
     *******************************************************************************/
    auto vita_udp_rx_impl::process_IQ(gr_complex*& outP) -> int
    {
        int samples_produced = 0;

        // Copy IQ data to output
        // The VITA-49 packet sends I/Q as 16-bit signed quantities. What follows is a bit of
        // magic. If the data actually comes as Q/I and we want to swap them, do a 32-bit
        // byteswap (in-place) If we are little-endian and want to swap to host order (and
        // didn't already swap ??), do a 16-bit swap (in-place)
        short* IQ = reinterpret_cast<short*>(&d_buffer[d_header_byte_offset]);

        // Swap bytes if requested
        if (d_swap_iq) {
            volk_32u_byteswap(reinterpret_cast<uint32_t*>(IQ), d_samples_per_packet);
        }
        if (d_swap_bytes xor d_swap_iq) {
            volk_16u_byteswap(reinterpret_cast<uint16_t*>(IQ), 2 * d_samples_per_packet);
        }

        // convert the I/Q samples from short to scaled float; copy the
        // interleaved I/Q floats to the output. In practice, [ (float,float),
        // (float,float),...] is the same as [complex<float>, complex<float>, ...]
        volk_16i_s32f_convert_32f(
            reinterpret_cast<float*>(outP), IQ, 32768.0, 2 * d_samples_per_packet);

        outP += d_samples_per_packet;
        if( d_use_vector_output) {
            samples_produced += 1;
        } else {
            samples_produced += d_samples_per_packet;            
        }
        produce(0, samples_produced);
        d_buffer.resize(0); // consume the buffer
        

        return samples_produced;
    }

    /*******************************************************************************
     * \brief tag a packet with information from the V49 stream
     * \param stream which output stream this applies to (should always be 0)
     * \param offset the relative sample number to attach tags to
     *******************************************************************************/
    auto vita_udp_rx_impl::tag_packet(int stream, int offset) -> void
    {
        uint32_t __ddc_filter = 0;
        if (d_tag_packets) {
            auto hdr = reinterpret_cast<V49_0_Header*>(d_buffer.data());

            uint64_t tag_item = nitems_written(0) + offset;

            // Note if we setup byte swap, it's already been done in place
            {
            // Moved so I have the information for DDC Rate
                auto ddc_filter = ((hdr->ddc_2 >> 20) & 0x0FFF);
                auto tag = pmt::from_float(ndr358_551_ddc_map.at(ddc_filter));
                add_item_tag(stream, tag_item, pmt::mp("ddc_rate"), tag);
                __ddc_filter = ddc_filter;
            }

            // timestamp
            {
                auto fractionalTs = uint64_t(0);
                fractionalTs = uint64_t(hdr->frac_timestamp_msw) << 32;
                fractionalTs += uint64_t(hdr->frac_timestamp_lsw) & 0x0FFFFFFFFLL;
                auto tag = pmt::cons(pmt::from_long(hdr->int_timestamp),
                                    pmt::from_uint64(fractionalTs));
                add_item_tag(stream, tag_item, pmt::mp("timestamp"), tag);

                if( d_first_packet )
                {
                    d_frac_last_timestamp = fractionalTs;
                } else {
                    uint32_t expected_diff = ndr358_551_timestamp_diffs.at(__ddc_filter);
                    if ( (fractionalTs - d_frac_last_timestamp) != expected_diff )
                    {
                        txStatusMsg();
                        std::cout
                            << "gr::CyberRadio::vita_udp_rx_impl: packet loss detected: expected "
                            << expected_diff << ", received " << (fractionalTs - d_frac_last_timestamp) << std::endl;
                    }
                }
            }

            // stream id
            {
                auto tag = pmt::from_long(hdr->stream_id);
                add_item_tag(stream, tag_item, pmt::mp("stream_id"), tag);
            }
            {
                auto tag = pmt::from_long((hdr->ddc_0 >> 28) & 0x0F);
                add_item_tag(stream, tag_item, pmt::mp("rx_channel"), tag);
            }

            // frequency
            {
                auto tuned_freq = uint16_t((hdr->ddc_0 >> 0) & 0x0FFFF);
                auto ddc_offset = int32_t((hdr->ddc_1 >> 0) & 0x0FFFFFFFF);
                {
                    auto tag = pmt::from_long(tuned_freq);
                    add_item_tag(stream, tag_item, pmt::mp("rx_freq"), tag);
                }
                {
                    auto tag = pmt::from_long(ddc_offset);
                    add_item_tag(stream, tag_item, pmt::mp("ddc_offset"), tag);
                }
            }

            {
                auto tag = pmt::from_long((hdr->ddc_2 >> 0) & 0x0001FFFF);
                add_item_tag(stream, tag_item, pmt::mp("delay_time"), tag);
            }

            {
                auto tag = pmt::from_bool(bool((hdr->ddc_0 >> 27) & 0x01));
                add_item_tag(stream, tag_item, pmt::mp("delay_en"), tag);
            }

            {
                auto ovs = (hdr->ddc_4 >> 28) & 0x0F;
                std::string ovs_s;
                switch (ovs) {
                case 0:
                    ovs_s = "1X";
                    break;
                case 1:
                    ovs_s = "2X";
                    break;
                case 2:
                    ovs_s = "4X";
                    break;
                case 3:
                    ovs_s = "8X";
                    break;
                case 4:
                    ovs_s = "16X";
                    break;
                default:
                    ovs_s = std::string("unknown oversample: ") + std::to_string(ovs);
                    break;
                }
                auto tag = pmt::mp(ovs_s.c_str());
                add_item_tag(stream, tag_item, pmt::mp("ddc_ovs"), tag);
            }

            {
                auto tag = pmt::from_long((hdr->ddc_4 >> 16) & 0x0FFF);
                add_item_tag(stream, tag_item, pmt::mp("ddc_agc_gain"), tag);
            }

            {
                auto tag = pmt::from_long(((hdr->ddc_4 >> 0) & 0x000007FF));
                add_item_tag(stream, tag_item, pmt::mp("valid_data_count"), tag);
            }

            {
                auto tag = pmt::from_long((hdr->ddc_0 >> 16) & 0x003F);
                add_item_tag(stream, tag_item, pmt::mp("rx_atten"), tag);
            }
        }
    }

    /*******************************************************************************
     * \brief tag a packet with information from the V491 stream
     * \param stream which output stream this applies to (should always be 0)
     * \param offset the relative sample number to attach tags to
     *******************************************************************************/
    auto vita_udp_rx_impl::tag_v491_packet(int stream, int offset) -> void
    {
        if (d_tag_packets) {
            uint64_t tag_item = nitems_written(0) + offset;

            // Note if we setup byte swap, it's already been done in place

            auto hdr = reinterpret_cast<V49_308_Header*>(d_buffer.data());

            // timestamp
            {
                auto tag = pmt::cons(pmt::from_long(hdr->int_timestamp),
                                    pmt::from_long(hdr->frac_timestamp_lsw));
                add_item_tag(stream, tag_item, pmt::mp("timestamp"), tag);
            }

            // stream id
            {
                auto tag = pmt::from_long(hdr->stream_id);
                add_item_tag(stream, tag_item, pmt::mp("stream_id"), tag);
            }
        }
    }

    /*******************************************************************************
     * \brief Recieve a control message. Currntly we just print the rx'd message.
     * \note technically unimplemented.
     *******************************************************************************/
    void vita_udp_rx_impl::rxControlMsg(pmt::pmt_t msg)
    {
        std::cout << "****    vita_udp_rx_impl::rxControlMsg: " << msg << "    ****"
                  << std::endl;
        // What did we receive?
        pmt::pmt_t msgId = pmt::car(msg);
        pmt::pmt_t content = pmt::cdr(msg);
    }

    /*******************************************************************************
     * \brief Transmit a status message from the block. Currently onlyt tx on
     *        detected packet count errors
     *******************************************************************************/
    void vita_udp_rx_impl::txStatusMsg()
    {
        auto msg = pmt::cons(pmt::mp("packet dropped detected"), pmt::PMT_NIL);
        message_port_pub(status_port, msg);
    }

    /*******************************************************************************
     * \brief Override of GNURadio start function
     * \return true if socket opened false if error
     * \todo should this be allowed to throw or should it just return false?
     *******************************************************************************/
    bool vita_udp_rx_impl::start()
    {
        auto success = false;

        int sockfd = -1;

        // Create a UDP Socket
        if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
            raise_error("cannot create socket\n", sockfd);
        }

        // Set socket to reuse address
        int enable = 1;
        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0) {
            raise_error("setsockopt SO_REUSEADDR call failed", sockfd);
        }

        if (not d_is_narrowband) {
            // /proc/sys/net/core/rmem_max holds this value must be >= recv_buffer_size
            // linux kernel receiver buffer size. this is not to be confused with the size
            // of this class' ring buffer.
            constexpr unsigned long recv_buffer_size = 268435456; // 256 MB

            // Set recv buffer size
            if (setsockopt(sockfd,
                          SOL_SOCKET,
                          SO_RCVBUF,
                          &recv_buffer_size,
                          sizeof(recv_buffer_size)) == -1) {
                raise_error("couldn't set recv buf size.", sockfd);
            }

            // Verify this sock opt took
            unsigned long long check_size = 0;
            unsigned int arg_len = sizeof(check_size);
            getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &check_size, &arg_len);
            if (check_size != 2 * recv_buffer_size) {
                std::ostringstream ss;
                ss << "recv buf size set to " << recv_buffer_size << " but value is "
                  << check_size << "; check max limit in /proc/sys/net/core/rmem_max";
                ::close(sockfd);

                std::cerr << ss.str() << std::endl;
                throw std::runtime_error(ss.str());
            }
        }

        // Bind the socket
        sockaddr_in myaddr;
        memset((char*)&myaddr, 0, sizeof(myaddr));
        myaddr.sin_family = AF_INET;
        myaddr.sin_addr.s_addr = inet_addr(d_src_ip.c_str());
        myaddr.sin_port = htons(d_port);

        if (bind(sockfd, (struct sockaddr*)&myaddr, sizeof(myaddr)) < 0) {
            raise_error("bind failed", sockfd);
        }

        d_sock = sockfd;
        success = true;

        return success;
    }

    /*******************************************************************************
     * \brief override for GNURadio stop function from gr::block
     * \return true on exit
     *******************************************************************************/
    bool vita_udp_rx_impl::stop()
    {
        std::cout << "Socket closing" << std::endl;
        close(d_sock);
        bool ret = true;
        return ret;
    }
    /*
     * Our virtual destructor.
     */
    vita_udp_rx_impl::~vita_udp_rx_impl()
    {
    }

    int
    vita_udp_rx_impl::general_work(int noutput_items,
        gr_vector_int& ninput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      auto samples_needed = noutput_items;
      auto outP = static_cast<gr_complex*>(output_items[0]);

      // This method is called because there is room to fill the output buffer. We know
      // it's at least one packet; wait until the next packet is received
      while (samples_needed > 0) {
          // See if we need a new packet
          if (d_buffer.empty()) {
              auto success = receive_packet();
              if (not success) {
                  // This is generally bad and should never happen. Error logging has
                  // already been done, but at this point we don't have anything to work
                  // with. Return what we have and try again?
                  return noutput_items - samples_needed;
              }
          }
          // one packet is in buffer. Process it
          if (d_uses_v49_1) {
              samples_needed -= process_v491_packet(outP);
          } else {
              samples_needed -= process_packet(outP, samples_needed);
          }
      }

      return WORK_CALLED_PRODUCE;
    }

  } /* namespace CyberRadio */
} /* namespace gr */
