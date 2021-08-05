/* -*- c++ -*- */
/***************************************************************************
 * \file NDR651_duc_sink_mk2_impl.h
 *
 * \brief Implementation of the digital upconverter (DUC) transmission
 *    sink block for the NDR651 (Mk2).
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_DUC_SINK_MK2_IMPL_H
#define INCLUDED_CYBERRADIO_NDR651_DUC_SINK_MK2_IMPL_H

#include "CyberRadio/NDR651_duc_sink_mk2.h"
#include "LibCyberRadio/NDR651/DUCSink.h"
#include <stdio.h>
#include <sys/types.h>
#include <time.h>

namespace gr {
namespace CyberRadio {
class NDR651_duc_sink_mk2_impl : public NDR651_duc_sink_mk2 {
public:
  NDR651_duc_sink_mk2_impl(
      /* For the radio in general */
      const std::string &radio_host_name = "",
      unsigned int radio_tcp_port = 8617, unsigned int tengig_iface_index = 1,
      float iq_scale_factor = 1.0,
      /* For an individual DUC on the radio */
      unsigned int duc_channel = 1,
      const std::string &duc_iface_string = "eth0",
      unsigned int duc_rate_index = 0, long duc_frequency = 0,
      float duc_attenuation = 0, unsigned int duc_tx_channels = 0,
      double duc_tx_frequency = 900, unsigned int duc_tx_attenuation = 0,
      unsigned int duc_stream_id = 40001, bool config_tx = false,
      bool debug = false, unsigned int fc_update_rate = 20,
      bool use_udp = false, bool use_ring_buffer = false,
      unsigned int duchsPfThresh = 25, unsigned int duchsPeThresh = 24,
      unsigned int duchsPeriod = 10, bool updatePE = false, int txinv_mode = 0);
  ~NDR651_duc_sink_mk2_impl();
  std::string get_radio_host_name() const;
  int get_radio_tcp_port() const;
  std::vector<std::string> get_tengig_iface_list() const;
  void set_radio_params(const std::string &radio_host_name, int radio_tcp_port,
                        const std::vector<std::string> &tengig_iface_list);
  float get_iq_scale_factor() const;
  void set_iq_scale_factor(float iq_scale_factor);
  int get_duc_channel() const;
  void set_duc_channel(int duc_channel);
  std::string get_duc_iface_string() const;
  int get_duc_iface_index() const;
  void set_duc_iface_string(const std::string &duc_iface_string);
  int get_duc_rate_index() const;
  void set_duc_rate_index(int duc_rate_index);
  long get_duc_frequency() const;
  void set_duc_frequency(long duc_frequency);
  void set_duc_txinv_mode(int txinv_mode);
  float get_duc_attenuation() const;
  void set_duc_attenuation(float duc_attenuation);
  unsigned int get_duc_tx_channels() const;
  void set_duc_tx_channels(unsigned int duc_tx_channels);
  double get_duc_tx_frequency() const;
  void set_duc_tx_frequency(double duc_tx_frequency);
  unsigned int get_duc_tx_attenuation() const;
  void set_duc_tx_attenuation(unsigned int duc_tx_attenuation);
  unsigned int get_duc_stream_id() const;
  void set_duc_stream_id(unsigned int duc_stream_id);
  long get_duc_sample_rate() const;

  void set_duchs_pf_threshold(int duchsPfThresh);
  void set_duchs_pe_threshold(int duchsPeThresh);
  void set_duchs_period(int duchsPeriod);
  void set_duchs_update_pe(bool updatePE);

  bool start();
  bool stop();
  // OVERRIDE
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

private:
  LibCyberRadio::NDR651::DUCSink *d_sink;
};

} // namespace CyberRadio

} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NDR651_DUC_SINK_MK2_IMPL_H */
