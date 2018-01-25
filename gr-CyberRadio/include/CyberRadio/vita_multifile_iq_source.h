/* -*- c++ -*- */
/***************************************************************************
 * \file vita_multifile_iq_source.h
 *
 * \brief Generic VITA 49-compatible I/Q data source block that pulls its
 *    source data from a sequence of files.
 *
 * \author DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 * \note This is a re-implementation of GNU Radio's file_source
 * block.  It includes some new features that make it more useful
 * in a GUI environment.
 *
 */

#ifndef INCLUDED_CYBERRADIO_VITA_MULTIFILE_IQ_SOURCE_H
#define INCLUDED_CYBERRADIO_VITA_MULTIFILE_IQ_SOURCE_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>
#include <string>
#include <vector>


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
     * \ingroup CyberRadioSignals
     *
     * \brief Generic VITA 49-compatible I/Q data source block that
     *    pulls its source data from a sequence of files.
     *
     * \details
     * The vita_multifile_iq_source block provides I/Q data from a
     * sequence of files on disk.  The sequence of files can be
     * explicitly provided by the user, determined by evaluating a
     * wildcard file specification, or some combination of these.
     *
     * The behavior of this block when it has no active files to read
     * data from depends on the Terminate When Data Ends option.  If
     * this option is True, then the flowgraph will terminate.  If it
     * is not set, then it will output (complex) zeros until it does
     * have valid data files.
     *
     * This block assumes that the data being read from disk is in
     * a format returned by an NDR-class radio.  This will be either
     * raw I/Q data (16-bit interleaved I and Q) or VITA 49 frame
     * format.  The output from this block is native (32-bit) complex.
     *
     * The vita_multifile_iq_source block can also produce stream tags at
     * the beginning of each received VITA 49 frame.  The block generates
     * the following stream tags, as appropriate for the radio:
     * \li absolute_sample_num -- The absolute sample number
     * \li absolute_packet_num -- The absolute packet number
     * \li filename -- The file name that the data comes from.  If the
     *   packet spans files, the file name will be the file that the
     *   last segment of the packet data came from.
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
     *
     * In addition, this block provides some features that are useful
     * in a GUI environment, where the file(s) that the user wants to
     * use is (are) not necessarily known when the flowgraph starts.
     * (This is a drawback of the stock file_source object in GNU Radio.)
     *
     */
    class CYBERRADIO_API vita_multifile_iq_source :
        virtual public gr::sync_block
    {
      public:
        // gr::CyberRadio::vita_multifile_iq_source::sptr
        typedef boost::shared_ptr<vita_multifile_iq_source> sptr;

        /*!
         * \brief Creates a vita_multifile_iq_source block.
         *
         * \param filespecs A list of filenames and/or wildcard file
         *    specifications for the data files to use.
         * \param alphabetical Whether the block should alphabetically sort
         *    file names during file spec evaluation.
         * \param vita_type The VITA 49 enable option value.  A value of 0
         *     indicates raw I/Q format, and any other value indicates VITA
         *     49 frame format.
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
         * \param repeat True if the data should be repeated from the
         *    beginning once the last item is processed, False otherwise.
         * \param terminate_at_end True if the flowgraph should terminate when the
         *    all of the file data has been processed.  This option has no effect
         *    if Repeat is True.
         * \param tagged Whether the block should produce stream tags.  Defaults to
         *    False.
         * \param debug Whether the block produces debug output.
         *
         * \return A boost::shared_ptr<vita_multifile_iq_source> representing
         *    the new block.
         */
        static sptr make(const std::vector<std::string>& filespecs = std::vector<std::string>(),
                     bool alphabetical = false,
                 int vita_type = 0,
                     size_t payload_size = 8192,
                     size_t vita_header_size = 0,
                     size_t vita_tail_size = 0,
                     bool byte_swapped = false,
                     bool iq_swapped = false,
                     float iq_scale_factor = 1.0,
                     bool repeat = false,
                 bool terminate_at_end = false,
                 bool tagged = false,
                 bool debug = false);

        /*!
         * \brief Opens a new sequence of files.
         *
         * Calling this method while this block is already
         * reading data closes the file being used and abandons
         * the previous file sequence.
         *
         * \param filespecs A list of filenames and/or wildcard file
         *    specifications for the data files to use.
         * \param alphabetical Whether the block should alphabetically sort
         *    file names during file spec evaluation.
         * \param repeat True if the data should be repeated from the
         *    beginning once the last item is processed, False otherwise.
         * \param terminate_at_end True if the flowgraph should terminate when the
         *    all of the file data has been processed.  This option has no effect
         *    if Repeat is True.
         */
        virtual void open(const std::vector<std::string>& filespecs = std::vector<std::string>(),
                      bool alphabetical = false,
                          bool repeat = false,
                  bool terminate_at_end = false) = 0;

        /*!
         * \brief Close the existing file sequence.
         *
         * Calling this method causes this block to provide
         * zero values until provided with a file sequence than
         * can be opened.
         *
         */
        virtual void close() = 0;

        /*!
         * \brief Sets the I/Q scale factor.
         * \param iq_scale_factor The new I/Q scale factor.
         */
        virtual void set_iq_scale_factor(float iq_scale_factor) = 0;

        /*!
         * \brief Gets the real-time calculated sample rate for a specific
         *    output.
         * \return The sample rate (in samples per second).
         */
        virtual float get_realtime_sample_rate() = 0;
    };

  } /* namespace CyberRadio */
} /* namespace gr */

#endif /* INCLUDED_CYBERRADIO_VITA_MULTIFILE_IQ_SOURCE_H */
