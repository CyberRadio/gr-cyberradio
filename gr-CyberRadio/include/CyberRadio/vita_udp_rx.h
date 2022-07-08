/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_VITA_UDP_RX_H
#define INCLUDED_CYBERRADIO_VITA_UDP_RX_H

#include <CyberRadio/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API vita_udp_rx : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<vita_udp_rx> sptr;
      // Because this class takes a number of optional configuration items, and because the
      // signature changed in a way that could lead to undiagnosed errors, collapse all the
      // configuration items to a structure and pass that
      struct Cfg {
          std::string src_ip;          ///< source IP address to bind to
          short port;                  ///< source port to bind to
          unsigned header_byte_offset; ///< number of bytes in the V49 header
          int samples_per_packet;      ///< number of samples in a packet
          int bytes_per_packet;        ///< total size of the V49 packet
          bool swap_bytes;             ///< if the packet should be byteswapped
          bool swap_iq;                ///< change from IQ to QI (or from QI to IQ)
          bool tag_packets;            ///< add GR tags to the stream
          bool uses_v49_1 = true;      ///< VITA 49.1 (VRLP and VEND headers)
          bool narrowband = false;     ///< if using a narrowband DDC
          bool debug = false;          ///< output extra debug info
      };
      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::vita_udp_rx.
       *
       * To avoid accidental use of raw pointers, CyberRadio::vita_udp_rx's
       * constructor is in a private implementation
       * class. CyberRadio::vita_udp_rx::make is the public interface for
       * creating new instances.
       */
      static sptr make(Cfg const& cfg);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_UDP_RX_H */
