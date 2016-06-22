/* -*- c++ -*- */
/***************************************************************************
 * \file Debuggable.h
 *
 * \brief Class that supports debug output.
 *
 * \author DA
 * \copyright 2016 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_LIBCYBERRADIO_DEBUGGABLE_H_
#define INCLUDED_LIBCYBERRADIO_DEBUGGABLE_H_

#include <string>
#include <stdio.h>


/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
	/*!
	 * \brief Class that supports debug output.
	 *
	 * This class is intended to be a mixin for other classes, allowing them to support
	 * debug output.
	 */
	class Debuggable
	{
		protected:
			/*!
			 * \brief Constructs a Debuggable object.
			 *
			 * The constructor is protected because this class is not meant to be instantiated.
			 *
			 * \param debug Whether or not to create debug output.
			 * \param debug_name Name for identifying this object in debug output.
			 * \param debug_fp File to send debug output to.
			 */
			Debuggable(bool debug = false,
					   const std::string& debug_name = "",
					   FILE* debug_fp = stderr);

		public:
			~Debuggable();

		protected:
			/*!
			 * \brief Outputs debug information.
			 *
			 * This method follows the same semantics as printf().  Output is preceded by the
			 * name of the object, if provided.
			 *
			 * \param format The printf()-style format string.
			 * \return The number of characters outputted.
			 */
			int debug(const char *format, ...);

		public:
			bool d_debug;
			std::string d_debug_name;
			FILE* d_debug_fp;
	};

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DEBUGGABLE_H_ */
