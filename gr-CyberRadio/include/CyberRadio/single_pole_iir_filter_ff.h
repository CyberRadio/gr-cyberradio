/* -*- c++ -*- */
/*
 * Copyright 2022 g3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_H
#define INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API single_pole_iir_filter_ff : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<single_pole_iir_filter_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::single_pole_iir_filter_ff.
       *
       * To avoid accidental use of raw pointers, CyberRadio::single_pole_iir_filter_ff's
       * constructor is in a private implementation
       * class. CyberRadio::single_pole_iir_filter_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(double alpha, unsigned int vlen, bool resetOnAlphaChange);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_H */
