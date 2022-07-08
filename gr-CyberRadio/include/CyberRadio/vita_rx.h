/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_VITA_RX_H
#define INCLUDED_CYBERRADIO_VITA_RX_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API vita_rx : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<vita_rx> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::vita_rx.
       *
       * To avoid accidental use of raw pointers, CyberRadio::vita_rx's
       * constructor is in a private implementation
       * class. CyberRadio::vita_rx::make is the public interface for
       * creating new instances.
       */
      static sptr make(
                      std::string &src_ip, 
                      unsigned short port, 
                      unsigned int header_byte_offset, 
                      int samples_per_packet, 
                      int bytes_per_packet, 
                      bool swap_bytes, 
                      bool swap_iq, bool 
                      tag_packets, bool 
                      vector_output, 
                      bool uses_v491, 
                      bool narrowband, 
                      bool debug);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_RX_H */
