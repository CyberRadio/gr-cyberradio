/* -*- c++ -*- */
/***************************************************************************
 * \file NDR651_duc_sink_mk2.h
 *
 * \brief Digital upconverter (DUC) transmission sink block for the NDR651
 *    (Mk2).
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_DUC_SINK_MK2_H
#define INCLUDED_CYBERRADIO_NDR651_DUC_SINK_MK2_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_decimator.h>

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
		 * \ingroup CyberRadioNDR651
		 *
		 * \brief Digital upconverter (DUC) transmission sink block for the
		 *    NDR651 (Mk2).
		 *
		 * \details
		 * The NDR651_duc_sink_mk2 block represents a single digital upconverter
		 * (DUC) on an NDR651 radio, and transmits the signal sent to its
		 * input.
		 *
		 * To use more than one DUC on the NDR651, use multiple sinks,
		 * one for each DUC.
		 *
		 */
		// Internal note -- although this class uses the sync_decimator
		// block as a base, the processing performs no actual decimation
		// on its input samples.  The sync_decimator block simply consumes
	    // N input products to make one output product.  So using it is a
		// quick-and-dirty method of ensuring that the work() function has
		// enough input samples to generate outgoing VITA 49 frames.
		class CYBERRADIO_API NDR651_duc_sink_mk2 : virtual public gr::sync_decimator
		{
			public:
				typedef boost::shared_ptr<NDR651_duc_sink_mk2> sptr;

				/*!
				 * \brief Creates an NDR651_duc_sink_mk2 block.
				 *
				 * \param radio_host_name The radio host name.  If this is an empty
				 *    string, then the block will not connect to a radio.
				 * \param radio_tcp_port The radio TCP port.
				 * \param tengig_iface_list The list of 10GigE interfaces used by
				 *    the radio.
				 * \param iq_scale_factor Scale factor for coverting I/Q data from
				 *    complex input to native sample format.
				 * \param duc_channel The channel number for the DUC in use.
				 * \param duc_iface_string The interface string for the DUC in use.
				 * \param duc_rate_index The rate index for the DUC in use.
				 * \param duc_frequency The frequency offset for the DUC in use.
				 * \param duc_attenuation The attenuation for the DUC in use.
				 * \param duc_tx_channels The transmit channel mask for the DUC in use.
				 * \param duc_tx_frequency The transmit center frequency for the DUC in use.
				 * \param duc_tx_attenuation The transmit attenuation for the DUC in use.
				 * \param duc_stream_id The stream ID/UDP port for the DUC in use.
				 * \param debug Whether the block should produce debug output.  Defaults to
				 *    False.
				 *
				 * \return A boost::shared_ptr<NDR651_duc_sink_mk2> representing the
				 *    new block.
				 */
				static sptr make(
					  /* For the radio in general */
					  const std::string& radio_host_name = "",
					  unsigned int radio_tcp_port = 8617,
					  const std::vector<std::string>& tengig_iface_list = std::vector<std::string>(),
					  float iq_scale_factor = 1.0,
					  /* For an individual DUC on the radio */
					  unsigned int duc_channel = 0,
					  const std::string& duc_iface_string = "eth0",
					  unsigned int duc_rate_index = 0,
					  long duc_frequency = 0,
					  float duc_attenuation = 0,
					  unsigned int duc_tx_channels = 0,
					  unsigned int duc_tx_frequency = 900,
					  unsigned int duc_tx_attenuation = 0,
					  unsigned int duc_stream_id = 40001,
					  bool config_tx = false,
					  bool debug = false);

				/*!
				 * \brief Gets the radio host name.
				 * \return The radio host name.
				 */
				virtual std::string get_radio_host_name() const = 0;

				/*!
				 * \brief Gets the radio TCP port.
				 * \return The port number.
				 */
				virtual int get_radio_tcp_port() const = 0;

				/*!
				 * \brief Gets the 10GigE interface list for the radio.
				 * \return The interface list.
				 */
				virtual std::vector<std::string> get_tengig_iface_list() const = 0;

				/*!
				 * \brief Sets the radio parameters.
				 * \param radio_host_name The radio host name.  If this is an empty
				 *    string, then the block will disconnect any existing connection
				 *    and not attempt to connect to a radio.
				 * \param radio_tcp_port The radio TCP port.
				 * \param tengig_iface_list The list of 10GigE interface names.
				 */
				virtual void set_radio_params(const std::string& radio_host_name,
						                      int radio_tcp_port,
											  const std::vector<std::string>& tengig_iface_list) = 0;

				/*!
				 * \brief Gets the I/Q scale factor used for the radio.
				 * \return The scale factor.
				 */
				virtual float get_iq_scale_factor() const = 0;

				/*!
				 * \brief Sets the I/Q scale factor used for the radio.
				 * \param iq_scale_factor The scale factor.
				 */
				virtual void set_iq_scale_factor(float iq_scale_factor) = 0;

				/*!
				 * \brief Gets the channel number for the DUC
				 *    in use.
				 * \return The channel number.
				 */
				virtual int get_duc_channel() const = 0;

				/*!
				 * \brief Sets the channel number for the DUC
				 *    in use.
				 * \param duc_channel The channel number for the DUC in use.
				 */
				virtual void set_duc_channel(int duc_channel) = 0;

				/*!
				 * \brief Gets the interface name for the DUC in use.
				 * \return The interface name.
				 */
				virtual std::string get_duc_iface_string() const = 0;

				/*!
				 * \brief Gets the interface index (one-based) for the DUC
				 *    in use.
				 * \return The interface index.
				 */
				virtual int get_duc_iface_index() const = 0;

				/*!
				 * \brief Sets the interface name for the DUC in use.
				 * \param duc_iface_string The interface string for the DUC in use.
				 */
				virtual void set_duc_iface_string(const std::string& duc_iface_string) = 0;

				/*!
				 * \brief Gets the rate index (zero-based) for the DUC
				 *    in use.
				 * \return The rate index.
				 */
				virtual int get_duc_rate_index() const = 0;

				/*!
				 * \brief Sets the rate index (zero-based) for the DUC
				 *    in use.
				 * \param duc_rate_index The rate index for the DUC in use.
				 */
				virtual void set_duc_rate_index(int duc_rate_index) = 0;

				/*!
				 * \brief Gets the frequency offset for the DUC
				 *    in use.
				 * \return The frequency offset.
				 */
				virtual long get_duc_frequency() const = 0;

				/*!
				 * \brief Sets the frequency offset for the DUC
				 *    in use.
				 * \param duc_frequency The frequency offset for the DUC in use.
				 */
				virtual void set_duc_frequency(long duc_frequency) = 0;

				/*!
				 * \brief Gets the attenuation for the DUC
				 *    in use.
				 * \return The attenuation.
				 */
				virtual float get_duc_attenuation() const = 0;

				/*!
				 * \brief Sets the attenuation for the DUC
				 *    in use.
				 * \param duc_attenuation The attenuation for the DUC in use.
				 */
				virtual void set_duc_attenuation(float duc_attenuation) = 0;

				/*!
				 * \brief Gets the transmit channel mask for the DUC
				 *    in use.
				 * \return The transmit channel mask.
				 */
				virtual unsigned int get_duc_tx_channels() const = 0;

				/*!
				 * \brief Sets the transmit channel mask for the DUC
				 *    in use.
				 * \param duc_tx_channels The transmit channel mask for the DUC in use.
				 */
				virtual void set_duc_tx_channels(unsigned int duc_tx_channels) = 0;

				/*!
				 * \brief Gets the transmit center frequency (in MHz) for
				 *    the DUC in use.
				 * \return The transmit center frequency.
				 */
				virtual unsigned int get_duc_tx_frequency() const = 0;

				/*!
				 * \brief Sets the transmit center frequency (in MHz) for
				 *    the DUC in use.
				 * \param duc_tx_frequency The transmit center frequency for the DUC in use.
				 */
				virtual void set_duc_tx_frequency(unsigned int duc_tx_frequency) = 0;

				/*!
				 * \brief Gets the transmit attenuation (in dB) for the DUC in use.
				 * \return The transmit attenuation.
				 */
				virtual unsigned int get_duc_tx_attenuation() const = 0;

				/*!
				 * \brief Sets the transmit attenuation (in dB) for the DUC in use.
				 * \param duc_tx_attenuation The transmit attenuation for the DUC
				 *    in use.
				 */
				virtual void set_duc_tx_attenuation(unsigned int duc_tx_attenuation) = 0;

				/*!
				 * \brief Gets the VITA stream ID for the DUC.
				 * \return The stream ID.
				 */
				virtual unsigned int get_duc_stream_id() const = 0;

				/*!
				 * \brief Sets the VITA stream ID for the DUC.
				 * \param duc_stream_id The stream ID.
				 */
				virtual void set_duc_stream_id(unsigned int duc_stream_id) = 0;

				/*!
				 * \brief Gets the sample rate (in Hz) for the DUC in use,
				 *    based on the rate index.
				 * \return The sample rate.
				 */
				virtual long get_duc_sample_rate() const = 0;

		};

	} // namespace CyberRadio

} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NDR651_DUC_SINK_MK2_H */

