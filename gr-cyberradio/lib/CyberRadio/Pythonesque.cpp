/***************************************************************************
 * \file Pythonesque.cpp
 *
 * \brief Provides string utility functions that mimic string methods from
 *    Python.
 *
 * \author DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#include "Pythonesque.h"
#include <sstream>

namespace gr
{
	namespace CyberRadio
	{
		Pythonesque::Pythonesque(void)
		{
		}

		Pythonesque::~Pythonesque(void)
		{
		}

		std::string Pythonesque::Lstrip(const std::string& str, const std::string& chars)
		{
			std::string ret;

			// Strip whitespace at beginning of the line
			ret = str;
			size_t found = ret.find_first_not_of(chars);
			if ( found != std::string::npos ) {
				ret = ret.substr(found);
			}
			else {
				ret.clear();
			}
			return ret;
		}

		std::string Pythonesque::Rstrip(const std::string& str, const std::string& chars)
		{
			std::string ret;

			// Strip whitespace at end of the line
			ret = str;
			size_t found = ret.find_last_not_of(chars);
			if ( found != std::string::npos ) {
				ret.erase(found+1);
			}
			else {
				ret.clear();
			}
			return ret;
		}

		std::string Pythonesque::Strip(const std::string& str, const std::string& chars)
		{
			return Rstrip(Lstrip(str, chars), chars);
		}

		std::string Pythonesque::Replace(const std::string& str, const std::string &oldstr, const std::string& newstr, int count)
		{
			std::string buf(str);
			std::string::size_type pos = buf.find(oldstr);
			int replaces = 0;
	
			while ( (pos != std::string::npos) && (replaces < count) )
			{
				buf.replace(pos, oldstr.length(), newstr);
				pos = buf.find(oldstr, pos + newstr.length());
				replaces++;
			}
			return buf;
		}

		BasicStringList Pythonesque::Split(const std::string& str, const std::string& sep, int maxsplit)
		{
			BasicStringList ret;
			std::string buf(str);
			std::string::size_type pos = buf.find(sep);
			int splits = 0;
			std::string tmp;

			while ( (pos != std::string::npos) && (splits < maxsplit) )
			{
				tmp = buf.substr(0, pos);
				ret.push_back(tmp);
				splits++;
				buf = buf.substr(pos + sep.length());
				pos = buf.find(sep);
			}
			if ( !buf.empty() )
				ret.push_back(buf);
			return ret;
		}
	
		std::string Pythonesque::Join(const BasicStringList& vec, const std::string& sep)
		{
			std::ostringstream oss;
			for (int i = 0; i < (int)vec.size(); i++)
			{
				oss << vec[i];
				if ( i != (int)vec.size()-1 ) oss << sep;
			}
			return oss.str();
		}

		bool Pythonesque::Startswith(const std::string& str, const std::string& prefix, int start, int end)
		{
			std::string buf = str.substr(start, end);
			std::string::size_type pos = buf.find(prefix);

			return ( pos == 0 );
		}

		bool Pythonesque::Endswith(const std::string& str, const std::string& suffix, int start, int end)
		{
			std::string buf = str.substr(start, end);
			std::string::size_type pos = buf.rfind(suffix);

			return ( pos == (buf.length() - suffix.length()) );
		}

		std::string Pythonesque::Basename(const std::string& path)
		{
			std::string ret = "";
			std::string pathsep;
			// Intelligently determine what the path separator is from the path,
			// or use the OS to determine it
			if ( path.find("\\") != std::string::npos )
				pathsep = "\\";
			else if ( path.find("/") != std::string::npos )
				pathsep = "/";
			else
			{
#ifdef _WIN32
				pathsep = "\\";
#else
				pathsep = "/";
#endif
			}
			BasicStringList vec = Split(path, pathsep);
			if ( vec.size() > 0 )
				ret = vec[vec.size()-1];
			return ret;
		}

	} /* namespace CyberRadio */
}
