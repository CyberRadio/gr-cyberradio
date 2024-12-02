/* -*- c++ -*- */
/*
 * Copyright 2024 Epiq.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_NV800SOURCE_H
#define INCLUDED_CYBERRADIO_NV800SOURCE_H

#include <gnuradio/sync_block.h>
#include <CyberRadio/api.h>

namespace gr {
namespace CyberRadio {

/*!
 * \brief <+description of block+>
 * \ingroup CyberRadio
 *
 */
class CYBERRADIO_API NV800Source : virtual public gr::block
{
public:
    typedef std::shared_ptr<NV800Source> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of CyberRadio::NV800Source.
     *
     * To avoid accidental use of raw pointers, CyberRadio::NV800Source's
     * constructor is in a private implementation
     * class. CyberRadio::NV800Source::make is the public interface for
     * creating new instances.
     */
    static sptr make(std::string src_ip, 
                  unsigned short port);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NV800SOURCE_H */
