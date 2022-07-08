/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
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
      typedef std::shared_ptr<vector_nlog10_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::vector_nlog10_ff.
       *
       * To avoid accidental use of raw pointers, CyberRadio::vector_nlog10_ff's
       * constructor is in a private implementation
       * class. CyberRadio::vector_nlog10_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(float n, size_t vlen, float k);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_H */
