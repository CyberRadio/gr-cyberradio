/***************************************************************************
 * \file BasicList.h
 *
 * \brief Defines what types we want for all basic lists.
 *
 * \author DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_BASIC_LIST_H
#define INCLUDED_LIBCYBERRADIO_BASIC_LIST_H

#include <string>
#include <deque>
#include <list>

/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
	#define BASIC_LIST_CONTAINER  std::deque
	/*! \brief Type representing a list of strings. */
	typedef BASIC_LIST_CONTAINER<std::string> BasicStringList;
	/*! \brief Type representing a list of integers. */
	typedef BASIC_LIST_CONTAINER<int> BasicIntList;
}

#endif

