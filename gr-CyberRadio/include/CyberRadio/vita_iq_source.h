/* -*- c++ -*- */
/***************************************************************************
 * \file vita_iq_source.h
 *
 * \brief Generic VITA 49-compatible I/Q data source block.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */


#ifndef INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_H
#define INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

/*!
 * \brief Provides GNU Radio blocks.
 */
namespace gr
{
  /*!
   * \brief Provides GNU Radio blocks for CyberRadio Solutions products.
   */
  namespace CyberRadio
  {

    /*!
     * \ingroup CyberRadioBase
     *
     * \brief A generic VITA 49-compatible I/Q data source block.
     *
     * \details
     * The vita_iq_source block outputs VITA 49 or raw I/Q data coming
     * from an NDR-class radio.  The source block listens for incoming
     * I/Q data using UDP and dispatches it to its output port(s)
     * as needed.  Dispatching is governed by which UDP port the data
     * comes in on, so each data stream needs to be assigned its own
     * UDP port on the radio side.
     *
     * This class is designed to be as flexible as possible in dealing
     * with data streams, since each NDR-class radio varies in how it
     * packages data streams.
     *
     * The vita_iq_source block can also produce stream tags at the
     * beginning of each received VITA 49 frame.  The block generates
     * the following stream tags, as appropriate for the radio:
     * \li absolute_sample_num -- The absolute sample number
     * \li frame_counter -- The VITA frame counter
     * \li frame_size -- The VITA frame size
     * \li packet_type -- The VITA packet type
     * \li packet_counter -- The VITA packet counter
     * \li packet_size -- The VITA packet size
     * \li stream_id -- The VITA stream ID
     * \li timestamp_int_type -- The VITA timestamp integer (TSI) field type
     * \li timestamp_int -- The VITA timestamp integer (TSI) field
     * \li timestamp_frac_type -- The VITA timestamp fractional (TSF) field type
     * \li timestamp_frac -- The VITA timestamp fractional (TSF) field
     * \li organizationally_unique_id -- The organizationally unique ID (OUI)
     * \li information_class_code -- The information class code (ICC)
     * \li packet_class_code -- The packet class code (PCC)
     * If the radio is sending raw I/Q data instead of VITA 49 frames, this
     * block will not produce stream tags regardless of the tagged setting.
     */
    class CYBERRADIO_API vita_iq_source : virtual public gr::sync_block
    {
    public:
      typedef boost::shared_ptr<vita_iq_source> sptr;

      /*!
       * \brief Creates a vita_iq_source block.
       *
       * \param vita_type The VITA 49 enable option value.  The range of valid
       *     values depends on the radio, but 0 always disables VITA 49
       *     formatting.  In that case, the data format is raw I/Q.
       * \param payload_size The VITA 49 or I/Q payload size for the radio, in
       *     bytes.  If VITA 49 output is disabled, then this parameter provides
       *     the total size of all raw I/Q data transmitted in a single packet.
       * \param vita_header_size The VITA 49 header size for the radio, in bytes.
       *     If VITA 49 output is disabled, then this parameter is ignored.
       * \param vita_tail_size The VITA 49 tail size for the radio, in bytes.
       *     If VITA 49 output is disabled, then this parameter is ignored.
       * \param byte_swapped Whether the bytes in the packet are swapped (with
       *     respect to the endianness employed by the host operating system).
       * \param iq_swapped Whether I and Q data in the payload are swapped.
       * \param iq_scale_factor Scale factor for coverting I/Q data from
       *    native sample format to complex output.
       * \param host The IP address or host name to bind listening UDP ports
       *    on.  Specify this as "0.0.0.0" to listen on all network interfaces.
       * \param port_list The list of UDP port numbers to listen on.  This block
       *    creates one output for each entry in this list, with each output
       *    corresponding to its associated port.  This block will have one output
       *    for each port number in this list.
       * \param debug Whether the block should produce debug output.  Defaults to
       *    False.
       * \param tagged Whether the block should produce stream tags.  Defaults to
       *    False.
       *
       * \return A boost::shared_ptr<vita_iq_source> representing the new source
       *    block.
       */
      static sptr make(int vita_type = 0,
               size_t payload_size = 8192,
               size_t vita_header_size = 0,
               size_t vita_tail_size = 0,
               bool byte_swapped = false,
               bool iq_swapped = false,
               float iq_scale_factor = 1.0,
               const std::string& host = "0.0.0.0",
               const std::vector<unsigned short>& port_list = std::vector<unsigned short>(),
               bool debug = false,
               bool tagged = false);

      /*!
       * \brief Gets the real-time calculated sample rate for a specific
       *    output.
       * \param output Which output to get the sample rate for.
       * \return The sample rate (in samples per second).
       */
      virtual float get_realtime_sample_rate(int output = 0) = 0;

    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_H */

