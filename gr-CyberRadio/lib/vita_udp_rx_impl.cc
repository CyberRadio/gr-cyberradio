// -*- c++ -*-
/*
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

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

// VITA 49 VRT IF data packet header, no class ID
// (used without external framing on NDR354/364)
struct V49_No491_Header {
    unsigned int packet_info;
    unsigned int stream_id;
    unsigned int int_timestamp;
    unsigned int frac_timestamp_msw;
    unsigned int frac_timestamp_lsw;
};

struct V49_0_Header {
    uint32_t packet_info;
    uint32_t stream_id;
    uint32_t class_0;
    uint32_t class_1;
    uint32_t int_timestamp;
    uint32_t frac_timestamp_msw;
    uint32_t frac_timestamp_lsw;
    uint32_t ddc_0;
    uint32_t ddc_1;
    uint32_t ddc_2;
    uint32_t ddc_3;
    uint32_t ddc_4;
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
    // strerror
    tag.append(": ");
    if (errno < sys_nerr)
        tag.append(sys_errlist[errno]);
    else
        tag.append("Unknown error ").append(std::to_string(errno));

    // wait until after strerror to avoid polluting errno
    ::close(sock); // this might fail if the sock wasn't open

    throw std::runtime_error(tag);
}

} // namespace

namespace gr {
namespace CyberRadio {

auto vita_udp_rx::make(Cfg const& cfg) -> sptr
{
    return gnuradio::get_initial_sptr(new vita_udp_rx_impl(cfg));
}

vita_udp_rx::vita_udp_rx(std::string const& name,
                         gr::io_signature::sptr input,
                         gr::io_signature::sptr output)
    : gr::block(name, input, output)
{
}

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
                samples_produced += d_samples_per_packet;
                outP += d_samples_per_packet;
                ++d_packetCounter;
            }
        }
    }
    return samples_produced;
}

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
    d_buffer.resize(0); // consume the buffer
    samples_produced += d_samples_per_packet;

    return samples_produced;
}

/*******************************************************************************
 * \brief tag a packet with information from the V49 stream
 * \param stream which output stream this applies to (should always be 0)
 * \param offset the relative sample number to attach tags to
 *******************************************************************************/
auto vita_udp_rx_impl::tag_packet(int stream, int offset) -> void
{
    if (d_tag_packets) {
        auto hdr = reinterpret_cast<V49_0_Header*>(d_buffer.data());

        uint64_t tag_item = nitems_written(0) + offset;

        // Note if we setup byte swap, it's already been done in place

        // timestamp
        {
            auto fractionalTs = uint64_t(0);
            fractionalTs = uint64_t(hdr->frac_timestamp_msw) << 32;
            fractionalTs += uint64_t(hdr->frac_timestamp_lsw) & 0x0FFFFFFFFLL;
            auto tag = pmt::cons(pmt::from_long(hdr->int_timestamp),
                                 pmt::from_uint64(fractionalTs));
            add_item_tag(stream, tag_item, pmt::mp("timestamp"), tag);
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
            auto ddc_filter = ((hdr->ddc_2 >> 20) & 0x0FFF);
            auto tag = pmt::from_float(ndr358_551_ddc_map.at(ddc_filter));
            add_item_tag(stream, tag_item, pmt::mp("ddc_rate"), tag);
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
 * \brief Constructor for vita_udp_rx
 * \param cfg The configuration params for this block
 *******************************************************************************/
vita_udp_rx_impl::vita_udp_rx_impl(Cfg const& cfg)
    : Base("vita_udp_rx",
           gr::io_signature::make(0, 0, 0),
           gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_src_ip(cfg.src_ip),
      d_port(cfg.port),
      d_sock(-1),

      d_samples_per_packet(cfg.samples_per_packet),
      d_header_byte_offset(cfg.header_byte_offset),
      d_bytes_per_packet(cfg.bytes_per_packet),

      d_swap_bytes(cfg.swap_bytes),
      d_swap_iq(cfg.swap_iq),
      d_uses_v49_1(cfg.uses_v49_1),
      d_is_narrowband(cfg.narrowband),
      d_tag_packets(cfg.tag_packets),
      d_debug(cfg.debug),
      d_first_packet(true),
      d_packetCounter(0),
      d_buffer(cfg.bytes_per_packet)
{
    // don't call work() until there is enough space for a whole packet
    set_output_multiple(d_samples_per_packet);

    // Create input port
    message_port_register_in(control_port);
    set_msg_handler(control_port, [this](pmt::pmt_t const& msg) { rxControlMsg(msg); });

    // Create output port
    message_port_register_out(status_port);
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

/*******************************************************************************
 * \brief GNURadio work function. RX's packets on IP/Port specified.\
 *        and decodes them according to configuration. If tagging is enabled
 *        packets are tagged with information.
 * \param noutput_items Number of output items
 * \param ninput_items Vector of Number of input items
 * \param input_items Vector of GNURadio input items
 * \param output_items Vector of output buffers
 * \return number of output items generated
 *******************************************************************************/
int vita_udp_rx_impl::general_work(int noutput_items,
                                   gr_vector_int& ninput_items [[maybe_unused]],
                                   gr_vector_const_void_star& input_items
                                   [[maybe_unused]],
                                   gr_vector_void_star& output_items)
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

    return noutput_items;
}
} // namespace CyberRadio
} // namespace gr
