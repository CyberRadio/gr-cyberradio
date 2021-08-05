/* -*- c++ -*- */
/***************************************************************************
 * \file NDR651_duc_sink_mk2_impl.cpp
 *
 * \brief Implementation of the digital upconverter (DUC) transmission
 *    sink block for the NDR651 (Mk2).
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "NDR651_duc_sink_mk2_impl.h"
#include <gnuradio/io_signature.h>
#include <iostream>
#include <math.h>
#include <stdarg.h>
#include <volk/volk.h>

namespace gr {
namespace CyberRadio {
NDR651_duc_sink_mk2::sptr NDR651_duc_sink_mk2::make(
    const std::string &radio_host_name, unsigned int radio_tcp_port,
    unsigned int tengig_iface_index, float iq_scale_factor,
    unsigned int duc_channel, const std::string &duc_iface_string,
    unsigned int duc_rate_index, long duc_frequency, float duc_attenuation,
    unsigned int duc_tx_channels, double duc_tx_frequency,
    unsigned int duc_tx_attenuation, unsigned int duc_stream_id, bool config_tx,
    bool debug, unsigned int duchsPfThresh, unsigned int duchsPeThresh,
    unsigned int duchsPeriod, bool updatePE, int txinv_mode) {
  return gnuradio::get_initial_sptr(new NDR651_duc_sink_mk2_impl(
      radio_host_name, radio_tcp_port, tengig_iface_index, iq_scale_factor,
      duc_channel, duc_iface_string, duc_rate_index, duc_frequency,
      duc_attenuation, duc_tx_channels, duc_tx_frequency, duc_tx_attenuation,
      duc_stream_id, config_tx, debug,
      /* fc_update_rate */ 20,
      /* use_udp */ false,
      /* use_ring_buffer */ false, duchsPfThresh, duchsPeThresh, duchsPeriod,
      updatePE, txinv_mode));
}

/*
 * The private constructor
 */
NDR651_duc_sink_mk2_impl::NDR651_duc_sink_mk2_impl(
    const std::string &radio_host_name, unsigned int radio_tcp_port,
    unsigned int tengig_iface_index, float iq_scale_factor,
    unsigned int duc_channel, const std::string &duc_iface_string,
    unsigned int duc_rate_index, long duc_frequency, float duc_attenuation,
    unsigned int duc_tx_channels, double duc_tx_frequency,
    unsigned int duc_tx_attenuation, unsigned int duc_stream_id, bool config_tx,
    bool debug, unsigned int fc_update_rate, bool use_udp, bool use_ring_buffer,
    unsigned int duchsPfThresh, unsigned int duchsPeThresh,
    unsigned int duchsPeriod, bool updatePE, int txinv_mode)
    : gr::sync_decimator("[CyberRadio] NDR651 DUC Sink (Mk2)",
                         gr::io_signature::make(1, 1, sizeof(gr_complex)),
                         gr::io_signature::make(0, 0, 0), SAMPLES_PER_FRAME),
      d_sink(NULL) {

  d_sink = new LibCyberRadio::NDR651::DUCSink(
      "[CyberRadio] NDR651 DUC Sink (Mk2)", radio_host_name, radio_tcp_port,
      tengig_iface_index, iq_scale_factor, duc_channel, duc_iface_string,
      duc_rate_index, duc_frequency, duc_attenuation, duc_tx_channels,
      duc_tx_frequency, duc_tx_attenuation, duc_stream_id, config_tx, debug,
      fc_update_rate, use_udp, use_ring_buffer, duchsPfThresh, duchsPeThresh,
      duchsPeriod, updatePE, txinv_mode);
}

/*
 * Our virtual destructor.
 */
NDR651_duc_sink_mk2_impl::~NDR651_duc_sink_mk2_impl() { delete d_sink; }

std::string NDR651_duc_sink_mk2_impl::get_radio_host_name() const {
  return d_sink->get_radio_host_name();
}

int NDR651_duc_sink_mk2_impl::get_radio_tcp_port() const {
  return d_sink->get_radio_tcp_port();
}

std::vector<std::string>
NDR651_duc_sink_mk2_impl::get_tengig_iface_list() const {
  return d_sink->get_tengig_iface_list();
}

void NDR651_duc_sink_mk2_impl::set_radio_params(
    const std::string &radio_host_name, int radio_tcp_port,
    const std::vector<std::string> &tengig_iface_list) {
  d_sink->set_radio_params(radio_host_name, radio_tcp_port, tengig_iface_list);
}

float NDR651_duc_sink_mk2_impl::get_iq_scale_factor() const {
  return d_sink->get_iq_scale_factor();
}

void NDR651_duc_sink_mk2_impl::set_iq_scale_factor(float iq_scale_factor) {
  d_sink->set_iq_scale_factor(iq_scale_factor);
}

int NDR651_duc_sink_mk2_impl::get_duc_channel() const {
  return d_sink->get_duc_channel();
}

void NDR651_duc_sink_mk2_impl::set_duc_channel(int duc_channel) {
  d_sink->set_duc_channel(duc_channel);
}

std::string NDR651_duc_sink_mk2_impl::get_duc_iface_string() const {
  return d_sink->get_duc_iface_string();
}

int NDR651_duc_sink_mk2_impl::get_duc_iface_index() const {
  return d_sink->get_duc_iface_index();
}

void NDR651_duc_sink_mk2_impl::set_duc_iface_string(
    const std::string &duc_iface_string) {
  d_sink->set_duc_iface_string(duc_iface_string);
}

int NDR651_duc_sink_mk2_impl::get_duc_rate_index() const {
  return d_sink->get_duc_rate_index();
}

void NDR651_duc_sink_mk2_impl::set_duc_rate_index(int duc_rate_index) {
  d_sink->set_duc_rate_index(duc_rate_index);
}

long NDR651_duc_sink_mk2_impl::get_duc_frequency() const {
  return d_sink->get_duc_frequency();
}

void NDR651_duc_sink_mk2_impl::set_duc_frequency(long duc_frequency) {
  d_sink->set_duc_frequency(duc_frequency);
}

void NDR651_duc_sink_mk2_impl::set_duc_txinv_mode(int txinv_mode) {
  d_sink->set_duc_txinv_mode(txinv_mode);
}

float NDR651_duc_sink_mk2_impl::get_duc_attenuation() const {
  return d_sink->get_duc_attenuation();
}

void NDR651_duc_sink_mk2_impl::set_duc_attenuation(float duc_attenuation) {
  d_sink->set_duc_attenuation(duc_attenuation);
}

unsigned int NDR651_duc_sink_mk2_impl::get_duc_tx_channels() const {
  return d_sink->get_duc_tx_channels();
}

void NDR651_duc_sink_mk2_impl::set_duc_tx_channels(
    unsigned int duc_tx_channels) {
  d_sink->set_duc_tx_channels(duc_tx_channels);
}

double NDR651_duc_sink_mk2_impl::get_duc_tx_frequency() const {
  return d_sink->get_duc_tx_frequency();
}

void NDR651_duc_sink_mk2_impl::set_duc_tx_frequency(double duc_tx_frequency) {
  d_sink->set_duc_tx_frequency(duc_tx_frequency);
}

unsigned int NDR651_duc_sink_mk2_impl::get_duc_tx_attenuation() const {
  return d_sink->get_duc_tx_attenuation();
}

void NDR651_duc_sink_mk2_impl::set_duc_tx_attenuation(
    unsigned int duc_tx_attenuation) {
  d_sink->set_duc_tx_attenuation(duc_tx_attenuation);
}

unsigned int NDR651_duc_sink_mk2_impl::get_duc_stream_id() const {
  return d_sink->get_duc_stream_id();
}

void NDR651_duc_sink_mk2_impl::set_duc_stream_id(unsigned int duc_stream_id) {
  d_sink->set_duc_stream_id(duc_stream_id);
}

long NDR651_duc_sink_mk2_impl::get_duc_sample_rate() const {
  return d_sink->get_duc_sample_rate();
}

void NDR651_duc_sink_mk2_impl::set_duchs_pf_threshold(int duchsPfThresh) {
  d_sink->set_duchs_pf_threshold((unsigned int)duchsPfThresh);
}

void NDR651_duc_sink_mk2_impl::set_duchs_pe_threshold(int duchsPeThresh) {
  d_sink->set_duchs_pe_threshold((unsigned int)duchsPeThresh);
}

void NDR651_duc_sink_mk2_impl::set_duchs_period(int duchsPeriod) {
  d_sink->set_duchs_period((unsigned int)duchsPeriod);
}

void NDR651_duc_sink_mk2_impl::set_duchs_update_pe(bool updatePE) {
  d_sink->set_duchs_update_pe(updatePE);
}

bool NDR651_duc_sink_mk2_impl::start() { return d_sink->start(); }

bool NDR651_duc_sink_mk2_impl::stop() { return d_sink->stop(); }

int NDR651_duc_sink_mk2_impl::work(int noutput_items,
                                   gr_vector_const_void_star &input_items,
                                   gr_vector_void_star &output_items) {
  // noutput_items = Number of outgoing VITA 49 frames requested
  // input_items.size() = Number of block inputs
  // input_items[0] = Pointer to input 0's data buffer.  The
  //     buffer has (noutput_items * SAMPLES_PER_FRAME) gr_complex
  //     values in it.
  // output_items = Not used because this is a sink object.
  gr_complex *pSampleBase = (gr_complex *)input_items[0];
  return d_sink->sendFrames(noutput_items, pSampleBase);
}

} /* namespace CyberRadio */

} /* namespace gr */
