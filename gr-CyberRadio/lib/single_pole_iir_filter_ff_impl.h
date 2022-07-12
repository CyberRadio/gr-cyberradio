/* -*- c++ -*- */
/*
 * Copyright 2022 g3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_IMPL_H
#define INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_IMPL_H

#include <CyberRadio/single_pole_iir_filter_ff.h>
#include <CyberRadio/single_pole_iir.h>
#include <boost/bind/bind.hpp>

namespace gr {
  namespace CyberRadio {

    class single_pole_iir_filter_ff_impl : public single_pole_iir_filter_ff
    {
     private:
      bool d_resetOnAlphaChange;
    	unsigned int d_vlen;
    	std::vector<single_pole_iir<float,float,double> > d_iir;
      void rxResetMsg(pmt::pmt_t msg);

     public:
      single_pole_iir_filter_ff_impl(double alpha, unsigned int vlen, bool resetOnAlphaChange);
      ~single_pole_iir_filter_ff_impl();

      void set_taps(double alpha);
      void reset(bool reset);

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_IMPL_H */
