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


#ifndef INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_H
#define INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API vector_nlog10_ff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<vector_nlog10_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of sg1450dsp::vector_nlog10_ff.
       *
       * To avoid accidental use of raw pointers, sg1450dsp::vector_nlog10_ff's
       * constructor is in a private implementation
       * class. sg1450dsp::vector_nlog10_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(float n=1.0, size_t vlen=1, float k=0.0);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_H */

