/***************************************************************************
 * \file Pythonesque.h
 *
 * \brief Provides string utility functions that mimic string methods from
 *    Python.
 *
 * \author DA
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_PYTHONESQUE_H
#define INCLUDED_LIBCYBERRADIO_PYTHONESQUE_H

#include <string>
#include <limits.h>
#include <LibCyberRadio/Common/BasicList.h>

/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    // Define an iterator for such a list
    typedef BasicStringList::iterator BasicStringListIterator;


    /*!
     * \brief Provides string utility functions that mimic string methods from
     *    Python.
     *
     * \note All methods of this class are static methods.
     */
    class Pythonesque
    {
        protected:
            /*!
             * \brief Protected constructor; prevents class instantiation.
             */
            Pythonesque(void);

        public:
            /*!
             * \brief Destructor.
             */
            virtual ~Pythonesque(void);

            /*!
             * \brief Strips leading whitespace from the given string.
             *
             * \param str
             * The original string.
             * \param chars
             * The list of whitespace characters to strip.  If not specified, strip all whitespace characters.
             * \return A string with the leading whitespace stripped.
             */
            static std::string Lstrip(const std::string& str, const std::string& chars = " \r\n\t\v\f");

            /*!
             * \brief Strips trailing whitespace from the given string.
             *
             * \param str
             * The original string.
             * \param chars
             * The list of whitespace characters to strip.  If not specified, strip all whitespace characters.
             * \return A string with the trailing whitespace stripped.
             */
            static std::string Rstrip(const std::string& str, const std::string& chars = " \r\n\t\v\f");

            /*!
             * \brief Strips both leading and trailing whitespace from the given string.
             *
             * \param str
             * The original string.
             * \param chars
             * The list of whitespace characters to strip.  If not specified, strip all whitespace characters.
             * \return A string with the leading and trailing whitespace stripped.
             */
            static std::string Strip(const std::string& str, const std::string& chars = " \r\n\t\v\f");

            /*!
             * \brief Replaces occurrences of one substring with another within the given string.
             *
             * \param str
             * The original string.
             * \param oldstr
             * The substring to be replaced.
             * \param newstr
             * The substring doing the replacing.
             * \param count
             * If specified, only replace the first \<count\> occurrences.  If not specified, replace all occurrences.
             * \return A string with the replacements made.
             */
            static std::string Replace(const std::string& str, const std::string &oldstr, const std::string& newstr,
                    int count = INT_MAX);

            /*!
             * \brief Splits the given string into a list of string tokens.
             *
             * \param str
             * The original string.
             * \param sep
             * The separator that delimits tokens within the string.
             * \param maxsplit
             * If specified, perform only \<maxsplit\> splits.  In this case, the resulting token list will contain at most
             * \<maxsplit+1\> elements; the last element will be the unsplit portion of the string.  If not specified, perform all
             * possible splits.
             * \return A vector of string tokens.
             */
            static BasicStringList Split(const std::string& str, const std::string& sep,
                    int maxsplit = INT_MAX);

            /*!
             * \brief Joins a list of string tokens, concatenating them into a single string.
             *
             * \param vec
             * The list of string tokens to concatenate.
             * \param sep
             * The separator that delimits tokens within the string.
             * \return A string with the tokens joined together.
             */
            static std::string Join(const BasicStringList& vec, const std::string& sep);

            /*!
             * \brief Determines if the given string starts with the specified prefix.
             *
             * \param str
             * The original string.
             * \param prefix
             * The prefix string to look for.
             * \param start
             * The position at which to start looking for the prefix.  0 indicates the beginning.  If not given, 0 is assumed.
             * \param end
             * The position at which to stop looking for the prefix.  If not given, the end of the string is assumed.
             * \return True if the prefix is found, false otherwise.
             */
            static bool Startswith(const std::string& str, const std::string& prefix, int start = 0, int end = INT_MAX);

            /*!
             * \brief Determines if the given string ends with the specified suffix.
             *
             * \param str
             * The original string.
             * \param suffix
             * The suffix string to look for.
             * \param start
             * The position at which to start looking for the suffix.  0 indicates the beginning.  If not given, 0 is assumed.
             * \param end
             * The position at which to stop looking for the suffix.  If not given, the end of the string is assumed.
             * \return True if the suffix is found, false otherwise.
             */
            static bool Endswith(const std::string& str, const std::string& suffix, int start = 0, int end = INT_MAX);

            /*!
             * \brief Gets the base name (the file name itself, without leading path components) from the
             * given file path.
             *
             * \param path
             * The full path name of the given file.
             * \return A string containing the base name.
             */
            static std::string Basename(const std::string& path);

    };

}

#endif /* INCLUDED_LIBCYBERRADIO_PYTHONESQUE_H */
