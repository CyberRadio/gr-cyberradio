/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_IMPL_H
#define INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_IMPL_H

#include <CyberRadio/vector_nlog10_ff.h>

namespace gr {
  namespace CyberRadio {

    class vector_nlog10_ff_impl : public vector_nlog10_ff
    {
     private:
      float  d_n;
      size_t d_vlen;
      float  d_k;

     public:
      vector_nlog10_ff_impl(float n, size_t vlen, float k);
      ~vector_nlog10_ff_impl();

      int work(int noutput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_IMPL_H */
