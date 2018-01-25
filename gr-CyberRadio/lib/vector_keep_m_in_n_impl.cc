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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "vector_keep_m_in_n_impl.h"

namespace gr {
  namespace CyberRadio {

    vector_keep_m_in_n::sptr
    vector_keep_m_in_n::make(size_t itemsize, int m, int n, int offset)
    {
      return gnuradio::get_initial_sptr
        (new vector_keep_m_in_n_impl(itemsize, m, n, offset));
    }

    /*
     * The private constructor
     */
    vector_keep_m_in_n_impl::vector_keep_m_in_n_impl(size_t itemsize, int m, int n, int offset)
      : gr::sync_block("vector_keep_m_in_n",
              gr::io_signature::make(1, 1, itemsize*n),
              gr::io_signature::make(1, 1, itemsize*m)),
    d_m(m),
    d_n(n),
    d_offset(offset),
    d_itemsize(itemsize)
  {
        // sanity checking
        if(d_m <= 0) {
          std::string s = boost::str(boost::format("keep_m_in_n: m=%1% but must be > 0") % d_m);
          throw std::runtime_error(s);
        }
        if(d_n <= 0) {
          std::string s = boost::str(boost::format("keep_m_in_n: n=%1% but must be > 0") % d_n);
          throw std::runtime_error(s);
        }
        if(d_m > d_n) {
          std::string s = boost::str(boost::format("keep_m_in_n: m (%1%) <= n %2%") % d_m % d_n);
          throw std::runtime_error(s);
        }
        if(d_offset > (d_n - d_m)) {
          std::string s = boost::str(boost::format("keep_m_in_n: offset (%1%) <= n (%2%) - m (%3%)") \
                                     % d_offset % d_n % d_m);
          throw std::runtime_error(s);
        }

  }

    /*
     * Our virtual destructor.
     */
    vector_keep_m_in_n_impl::~vector_keep_m_in_n_impl()
    {
    }

    int
    vector_keep_m_in_n_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      uint8_t* out = (uint8_t*)output_items[0];
    const uint8_t* in = (const uint8_t*)input_items[0];
    memcpy(out, in+d_offset*d_itemsize, d_m*d_itemsize);
      return noutput_items;
    }

  } /* namespace CyberRadio */
} /* namespace gr */

