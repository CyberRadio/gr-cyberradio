/***************************************************************************
 * \file Debuggable.cpp
 *
 * \brief Class that supports debug output.
 *
 * \author DA
* \copyright 2016 CyberRadio Solutions, Inc.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "LibCyberRadio/Common/Debuggable.h"
#include <stdarg.h>
#include <stdio.h>
#include <time.h>

#define DEBUGBOOL(x) (x ? "TRUE" : "FALSE")

namespace LibCyberRadio
{

	Debuggable::Debuggable(bool debug, const std::string& debug_name, FILE* debug_fp) :
		d_debug(debug),
		d_debug_name(debug_name),
		d_debug_fp(debug_fp)
	{
	}

	Debuggable::~Debuggable()
	{
	}

	int Debuggable::debug(const char *format, ...)
	{
		int ret = 0;
		if ( d_debug && (d_debug_fp != NULL) )
		{
			ret += fprintf(d_debug_fp, "[%010lu]", time(NULL));
			if (d_debug_name.length() > 0)
				ret += fprintf(d_debug_fp, "[%s] ", d_debug_name.c_str());
			if (ret >= 0)
			{
				va_list ap;
				va_start(ap, format);
				ret += vfprintf(d_debug_fp, format, ap);
				va_end(ap);
			}
		}
		return ret;
	}

} /* namespace LibCyberRadio */

