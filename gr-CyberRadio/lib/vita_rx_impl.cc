/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "vita_rx_impl.h"
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

    using output_type = gr_complex;
    vita_rx::sptr
    vita_rx::make(const char * src_ip, 
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
      return gnuradio::make_block_sptr<vita_rx_impl>(
        src_ip, port, header_byte_offset, samples_per_packet, bytes_per_packet,
        swap_bytes, swap_iq, tag_packets, vector_output, uses_v491, narrowband, debug);
    }


    /*
     * The private constructor
     */
    vita_rx_impl::vita_rx_impl(const char * src_ip, 
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
      : gr::sync_block("vita_rx",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1 /* min outputs */, 1 /*max outputs */, sizeof(output_type))),
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
      d_first_ctx_packet(true),
      d_bandwidth(0),
      d_ref_freq(0),
      d_sample_rate(0),
      d_packetCounter(0),
      d_buffer()
    {
      // pre-allocate the memory
      d_buffer.reserve(bytes_per_packet);

      // don't call work() until there is enough space for a whole packet
      set_output_multiple(d_samples_per_packet);

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

    /*
     * Our virtual destructor.
     */
    vita_rx_impl::~vita_rx_impl()
    {
    }

    int
    vita_rx_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      auto out = static_cast<output_type*>(output_items[0]);

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
          samples_needed -= process_packet(outP, samples_needed);
      }
      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

    /*******************************************************************************
    * \brief Recieve a control message. Currntly we just print the rx'd message.
    * \note technically unimplemented.
    *******************************************************************************/
    void vita_rx_impl::rxControlMsg(pmt::pmt_t msg)
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
    void vita_rx_impl::txStatusMsg()
    {
      auto msg = pmt::cons(pmt::mp("packet dropped detected"), pmt::PMT_NIL);
      message_port_pub(status_port, msg);
    }

    /*******************************************************************************
    * \brief Override of GNURadio start function
    * \return true if socket opened false if error
    * \todo should this be allowed to throw or should it just return false?
    *******************************************************************************/
    bool vita_rx_impl::start()
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
        myaddr.sin_addr.s_addr = inet_addr(d_src_ip);
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
    bool vita_rx_impl::stop()
    {
        std::cout << "Socket closing" << std::endl;
        close(d_sock);
        bool ret = true;
        return ret;
    }

    /*******************************************************************************
    * \brief RX a Packet
    * \return true on exit
    *******************************************************************************/
    auto vita_rx_impl::receive_packet() -> bool
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
            this->handle_context_packet( nbytesRx );
            std::cerr
                << "gr::CyberRadio::vita_udp_rx_impl: ERROR: received an incomplete packet. "
                << "received " << nbytesRx << " of " << d_buffer.size() << " expected." << std::endl;
            d_buffer.resize(0);
        }
        return success;
    }
    
    /*!*********************************************************************
     * @brief 
     * 
     * @return int 
     ***********************************************************************/
    auto vita_rx_impl::handle_context_packet( int rx_size ) -> int
    {
        volk_32u_byteswap(reinterpret_cast<uint32_t*>(d_buffer.data()), rx_size);
        auto hdr = reinterpret_cast<V49_Packet_info_Header*>(d_buffer.data());
        if ( hdr->packet_type == 0x4 ){
            V49_Ctx_WClass_Packet * pkt = reinterpret_cast<V49_Ctx_WClass_Packet*>(d_buffer.data());
            // Check if we've gotten an update.
            if ( (0x80000000 & pkt->ctx_ind) || (d_first_ctx_packet) ){
                uint64_t bw = (uint64_t)(pkt->bw_msw) << 32 | (uint64_t)pkt->bw_lsw;
                uint64_t ref_freq = (uint64_t)(pkt->ref_freq_msw) << 32 | (uint64_t)pkt->ref_freq_lsw;
                uint64_t sample_rate = (uint64_t)(pkt->sample_rate_msw) << 32 | (uint64_t)pkt->sample_rate_lsw;
                d_bandwidth = bw >> 20;
                d_sample_rate = sample_rate >> 20;
                d_ref_freq = ref_freq >> 20;
                auto msg0 = pmt::cons(pmt::mp("freq"), pmt::from_double((double)d_ref_freq));
                message_port_pub(freq_port, msg0);
                auto msg1 = pmt::cons(pmt::mp("bw"), pmt::from_double((double)d_sample_rate));
                std::cout << pmt::symbol_to_string(pmt::car(msg0)) << std::endl;
                message_port_pub(bw_port, msg1);
                d_first_ctx_packet = false;
            }
        }
        return 0;
    }

    /*******************************************************************************
    * \brief Process a Packet
    * \return true on exit
    *******************************************************************************/
    auto vita_rx_impl::process_packet(gr_complex*& outP, int samples_needed) -> int
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

        samples_produced += this->handle_dropped_packet(packet_counter, outP, samples_needed);

        if (samples_produced < samples_needed) {
            //tag_packet(0, samples_produced);
            samples_produced += process_IQ(outP);
        }

        return samples_produced;
    }

    /*******************************************************************************
    * \brief Process The IQ of a Packet
    * \return true on exit
    *******************************************************************************/
    auto vita_rx_impl::process_IQ(gr_complex*& outP) -> int
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
        produce(0, d_samples_per_packet);
        d_buffer.resize(0); // consume the buffer
        samples_produced += d_samples_per_packet;

        return samples_produced;
    }

     /*******************************************************************************
    * \brief Check for dropped packet
    * \return true on exit
    *******************************************************************************/
    auto vita_rx_impl::handle_dropped_packet(unsigned packet_counter,
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
                std::ostringstream oss;
                oss << "packet loss detected: expected [" << d_packetCounter << "], recieved [" << packet_counter << "]";
                std::string var = oss.str();
                d_logger->alert(var);
                //std::cout
                //    << "gr::CyberRadio::vita_udp_rx_impl: packet loss detected: expected "
                //    << d_packetCounter << ", received " << packet_counter << std::endl;

                while (d_packetCounter != packet_counter && samples_produced < samples_needed) {
                    std::fill_n(outP, d_samples_per_packet, gr_complex(0));
                    outP += d_samples_per_packet;
                    produce(0, d_samples_per_packet);
                    samples_produced += d_samples_per_packet;
                    ++d_packetCounter;
                }
            }
        }
        return samples_produced;
    }

  } /* namespace CyberRadio */
} /* namespace gr */
