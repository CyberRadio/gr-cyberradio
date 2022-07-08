/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(vita_rx.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(e5dd149600116691df32f55baebdf3c1)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <CyberRadio/vita_rx.h>
// pydoc.h is automatically generated in the build directory
#include <vita_rx_pydoc.h>

void bind_vita_rx(py::module& m)
{

    using vita_rx    = ::gr::CyberRadio::vita_rx;


    py::class_<vita_rx, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<vita_rx>>(m, "vita_rx", D(vita_rx))

        .def(py::init(&vita_rx::make),
           py::arg("src_ip"),
           py::arg("port"),
           py::arg("header_byte_offset"),
           py::arg("samples_per_packet"),
           py::arg("bytes_per_packet"),
           py::arg("swap_bytes"),
           py::arg("swap_iq"),
           py::arg("tag_packets"),
           py::arg("vector_output"),
           py::arg("uses_v491"),
           py::arg("narrowband"),
           py::arg("debug"),
           D(vita_rx,make)
        )
        



        ;




}








