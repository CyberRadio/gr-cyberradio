/***************************************************************************
 * \file BasicList.h
 *
 * \brief Defines what types we want for all basic lists.
 *
 * \author DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_CYBERRADIO_BASIC_LIST_H
#define INCLUDED_CYBERRADIO_BASIC_LIST_H

#include <string>
#include <deque>
#include <list>

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
		#define BASIC_LIST_CONTAINER  std::deque
		/*! \brief Type representing a list of strings. */
		typedef BASIC_LIST_CONTAINER<std::string> BasicStringList;
		/*! \brief Type representing a list of integers. */
		typedef BASIC_LIST_CONTAINER<int> BasicIntList;
	}
}

#endif

