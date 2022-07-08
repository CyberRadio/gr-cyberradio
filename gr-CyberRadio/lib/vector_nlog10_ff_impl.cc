/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "vector_nlog10_ff_impl.h"
#include <volk/volk.h>

namespace gr {
  namespace CyberRadio {

    using input_type = float;
    using output_type = float;
    vector_nlog10_ff::sptr
    vector_nlog10_ff::make(float n, size_t vlen, float k)
    {
      return gnuradio::make_block_sptr<vector_nlog10_ff_impl>(
        n, vlen, k);
    }


    /*
     * The private constructor
     */
    vector_nlog10_ff_impl::vector_nlog10_ff_impl(float n, size_t vlen, float k)
      : gr::sync_block("vector_nlog10_ff",
              gr::io_signature::make(1, 1, sizeof(input_type) * vlen),
              gr::io_signature::make(1, 1, sizeof(output_type) * vlen)),
      d_n(log2(10)/n),
      d_vlen(vlen),
      d_k(k)
    {}

    /*
     * Our virtual destructor.
     */
    vector_nlog10_ff_impl::~vector_nlog10_ff_impl()
    {
    }

    int
    vector_nlog10_ff_impl::work (int noutput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
    float *out = (float *) output_items[0];
    int noi = noutput_items * d_vlen;
    int size = noutput_items * d_vlen;
    float n = d_n;
    float k = d_k;

    volk_32f_log2_32f(out, in, noi);
    volk_32f_s32f_normalize(out, d_n, noi);
    return noutput_items;
    }

  } /* namespace CyberRadio */
} /* namespace gr */
