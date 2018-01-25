/* -*- c++ -*- */
/***************************************************************************
 * \file vita_iq_source.h
 *
 * \brief Generic VITA 49-compatible I/Q data source block.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */


#ifndef INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_2_H
#define INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_2_H

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
   * @ingroup vita
   *
   * @brief Creates a VITA 49 and/or I/Q radio data source block for GNU Radio.
   *
   * @details
   * The vita_iq_source block is used to collect VITA 49 or raw I/Q data
   * coming from an NDR-class radio.  The vita_iq_source block establishes
   * a UDP listening port (details specified by the @c host and @c port
   * arguments) and waits for the radio to send packetized data to that
     * address.
     *
   * The source block then makes raw data available on its output 0
   * stream without translating it in any way.
     * If coherent mode is off, 
     * output 1 data has the VITA information stripped off, with byte swapping, 
     * I/Q swapping and tagging optionally available.
   * If coherent mode is on, outputs 1-6 will contain data from each of the six
     * receiver inputs, with byte swapping and I/Q swapping optionally available.
     * Tagging is optionally available on output 1 only.
     *
   * This class is designed to be as flexible as possible in dealing
   * with data streams, since each NDR-class radio varies in how it
   * packages data streams.
   *
   */
    class CYBERRADIO_API vita_iq_source_2 : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<vita_iq_source_2> sptr;

    /*!
      * @brief Return a shared_ptr to a new instance of G3Tech::vita_iq_source.
      *
      * To avoid accidental use of raw pointers, G3Tech::vita_iq_source
      * constructor is in a private implementation class.
      * G3Tech::vita_iq_source::make is the public interface for
      * creating new instances.
      *
      * @param vitaType The VITA 49 enable option value.  The range of valid values
      *     depends on the radio, but 0 always disables VITA 49 formatting.  In that
      *     case, the data format is raw I/Q.
      * @param payloadSize The VITA 49 or I/Q payload size for the radio, in bytes.
      *     If VITA 49 output is disabled, then this parameter provides the total
      *     size of all raw I/Q data transmitted in a single packet.
      * @param vitaHeaderSize The VITA 49 header size for the radio, in bytes.
      *     If VITA 49 output is disabled, then this parameter is ignored.
      * @param vitaTailSize The VITA 49 tail size for the radio, in bytes.
      *     If VITA 49 output is disabled, then this parameter is ignored.
      * @param byteSwapped Whether the bytes in the packet are swapped (with respect
      *     to the endianness employed by the host operating system).
      * @param iqSwapped Whether I and Q data in the payload should be swapped.
      * @param host The IP address or host name for the UDP port to listen on.
      * @param port The port number for the UDP port to listen on.
      * @param debug Whether the block should produce debug output.  Defaults to False.
      * @param tagOutput Whether the second output should contain tags 
      * from the VITA header.  Defaults to False.
      * @param coherent If true, six channels of coherent data are deinterleaved
      * from one UDP stream into six outputs. Default is False.  This requires 
      * the receiver to be configured in coherent mode. (cmd: 'COH 3').
      *
    * @return A boost::shared_ptr<vita_iq_source> representing the new source block.
    *
    */
      static sptr make(int vitaType, size_t payloadSize, size_t vitaHeaderSize, 
          size_t vitaTailSize, bool byteSwapped, bool iqSwapped, 
          const std::string& host, int port, bool debug=false,
          bool tagOutput=false, bool coherent=false);

      /*! \brief Change the connection to a new destination
       *
       * \param host         The name or IP address of the receiving host; use
       *                     NULL or None to break the connection without closing
       * \param port         Destination port to connect to on receiving host
       *
       * Calls disconnect() to terminate any current connection first.
       */
      virtual void connect(const std::string &host, int port) = 0;

      /*! \brief Cut the connection if we have one set up.
       */
      virtual void disconnect() = 0;

      /*! \brief Change the size of the UDP receive buffer.
       *
       * \param size         The size in bytes of the UDP receive buffer.
       */
      virtual void set_receive_buffer_size(int size) = 0;

      /*! \brief Get the size of the UDP receive buffer.
       *
       * \return size        The size in bytes of the UDP receive buffer.
       */
      virtual int get_receive_buffer_size() = 0;

      /*! \brief Set the scale factor used when converting from short to float.
       *    Default is 32767.
       *
       * \param scale       The scale factor  Default is 32767.
       */
      virtual void set_scale_factor(int scale) = 0;

      /*! \brief Get the scale factor used when converting from short to float.
       *
       * \return scale       The scale factor.
       */
      virtual int get_scale_factor() = 0;
     
    };


  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VITA_IQ_SOURCE_H */

