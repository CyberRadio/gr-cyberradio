/* -*- c++ -*- */
/* 
 * Copyright 2019 G3.
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


#ifndef INCLUDED_CYBERRADIO_SNAPSHOT_FFT_VECTOR_SOURCE_H
#define INCLUDED_CYBERRADIO_SNAPSHOT_FFT_VECTOR_SOURCE_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API snapshot_fft_vector_source : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<snapshot_fft_vector_source> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::snapshot_fft_vector_source.
       *
       * To avoid accidental use of raw pointers, CyberRadio::snapshot_fft_vector_source's
       * constructor is in a private implementation
       * class. CyberRadio::snapshot_fft_vector_source::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::string radio_type,
                                    const std::string &ip,
                                    unsigned int port,
                                    unsigned int block_size,
                                    unsigned int block_rate);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SNAPSHOT_FFT_VECTOR_SOURCE_H */

