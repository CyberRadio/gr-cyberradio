/* -*- c++ -*- */
/* 
 * Copyright 2023 G3.
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
#include "convert_dbfs_dbm_impl.h"

namespace gr {
  namespace CyberRadio {

    convert_dbfs_dbm::sptr
    convert_dbfs_dbm::make(int vec_len, float user_atten, float factory_cal)
    {
      return gnuradio::get_initial_sptr
        (new convert_dbfs_dbm_impl(vec_len, user_atten, factory_cal));
    }

    /*
     * The private constructor
     */
    convert_dbfs_dbm_impl::convert_dbfs_dbm_impl(int vec_len, float user_atten, float factory_cal)
      : gr::block("convert_dbfs_dbm",
              gr::io_signature::make(1, 1, sizeof(float)*vec_len),
              gr::io_signature::make(1, 1, sizeof(float)*vec_len))
    {
      mUserAtten = user_atten;
      mFactoryCal = factory_cal;
      d_vlen = vec_len;
    }

    /*
     * Our virtual destructor.
     */
    convert_dbfs_dbm_impl::~convert_dbfs_dbm_impl()
    {
    }

    void
    convert_dbfs_dbm_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    convert_dbfs_dbm_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];
      unsigned int vlen = d_vlen;

      for ( int i = 0 ; i < noutput_items; i++)
      {
        for( unsigned int j = 0; j < vlen; j++)
        {
          *out++ = *in++ + 10 - mFactoryCal - mUserAtten;
        }
        
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace CyberRadio */
} /* namespace gr */

