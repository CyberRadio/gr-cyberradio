/* -*- c++ -*- */
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


#ifndef INCLUDED_CYBERRADIO_VITA_UDP_RX_H
#define INCLUDED_CYBERRADIO_VITA_UDP_RX_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_interpolator.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API vita_udp_rx : virtual public gr::sync_interpolator
    {
     public:
      typedef boost::shared_ptr<vita_udp_rx> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of vita_udp_rx::vita_udp_rx.
       *
       * To avoid accidental use of raw pointers, vita_udp_rx::vita_udp_rx's
       * constructor is in a private implementation
       * class. vita_udp_rx::vita_udp_rx::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::string &src_ip,
                        unsigned short port,
                        unsigned int header_byte_offset,
                        int samples_per_packet,
                        int bytes_per_packet,
                        bool swap_bytes,
                        bool swap_iq,
                        bool tag_packets,
                        bool vector_output,
                        bool uses_v49_1 = true,
                        bool narrowband = false,
                        bool debug = false);
    
      virtual bool start() = 0;
      virtual bool stop() = 0;

    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_UDP_RX_H */