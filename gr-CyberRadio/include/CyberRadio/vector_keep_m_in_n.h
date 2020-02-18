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


#ifndef INCLUDED_CYBERRADIO_VECTOR_KEEP_M_IN_N_H
#define INCLUDED_CYBERRADIO_VECTOR_KEEP_M_IN_N_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API vector_keep_m_in_n : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<vector_keep_m_in_n> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of sg1450dsp::vector_keep_m_in_n.
       *
       * To avoid accidental use of raw pointers, sg1450dsp::vector_keep_m_in_n's
       * constructor is in a private implementation
       * class. sg1450dsp::vector_keep_m_in_n::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t itemsize, int m, int n, int offset);

      virtual void set_offset(int offset) = 0;
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VECTOR_KEEP_M_IN_N_H */

