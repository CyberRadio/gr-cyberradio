/***************************************************************************
 * \file BasicDict.h
 *
 * \brief Defines what types we want for all basic dictionary types.
 *
 * \author DA
 * \copyright Copyright (c) 2017 CyberRadio Solutions, Inc.
 *
 * \note The basic dictionary type supports very simple key-value mappings.
 *    Nested dictionaries (such as available in Python) are beyond the scope
 *    of anything accessible here.
 */

#ifndef INCLUDED_LIBCYBERRADIO_BASIC_DICT_H
#define INCLUDED_LIBCYBERRADIO_BASIC_DICT_H

#include <string>
#include <map>

/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    #define BASIC_DICT_CONTAINER  std::map
    /*! \brief Type representing a dictionary of strings, keyed by string values. */
    typedef BASIC_DICT_CONTAINER<std::string, std::string> BasicStringStringDict;
    /*! \brief Type representing a dictionary of integers, keyed by string values. */
    typedef BASIC_DICT_CONTAINER<std::string, int> BasicStringIntDict;
    /*! \brief Type representing a dictionary of strings, keyed by integer values. */
    typedef BASIC_DICT_CONTAINER<int, std::string> BasicIntStringDict;
    /*! \brief Type representing a dictionary of integers, keyed by integer values. */
    typedef BASIC_DICT_CONTAINER<int, int> BasicIntIntDict;
    /*! \brief Type representing a dictionary of unsigned integers, keyed by integer values. */
    typedef BASIC_DICT_CONTAINER<int, unsigned int> BasicIntUIntDict;
}

#endif /* INCLUDED_LIBCYBERRADIO_BASIC_DICT_H */
