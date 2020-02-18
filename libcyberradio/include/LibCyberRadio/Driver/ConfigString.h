/***************************************************************************
 * \file ConfigString.h
 * \brief Defines a string class that supports several non-string data
 *    types for value setting and retrieval.
 * \author DA
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 * \note Requires C++11 compiler support.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_CONFIGSTRING_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_CONFIGSTRING_H

#include <string>


/**
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    /**
     * \brief Provides programming elements for driving CRS NDR-class radios.
     */
    namespace Driver
    {
        /**
         * \brief Configuration value string class.
         *
         * This class supports all standard std::string semantics for
         * manipulating the string form of the value.
         *
         * This class overloads the assignment (=) operator for setting
         * values using non-string data values, and defines several methods
         * for converting the stored value back to non-string data types.
         *
         */
        class ConfigString : public std::string
        {
            public:
                /**
                 * \brief Constructs an empty ConfigString object.
                 */
                ConfigString() : std::string() {}
                /**
                 * \brief Constructs a ConfigString object from a string.
                 * \param str String to copy.
                 */
                ConfigString(const std::string& str) : std::string(str) {}
                /**
                 * \brief Constructs a ConfigString object from a substring.
                 * \param str String to extract from
                 * \param pos Start position (0 = beginning)
                 * \param len Length of substring.  If this is npos, copy to end.
                 */
                ConfigString(const std::string& str, size_t pos, size_t len = npos) :
                    std::string(str, pos, len) {}
                /**
                 * \brief Constructs a ConfigString object from a string literal.
                 * \param s String to copy.
                 */
                ConfigString(const char* s) : std::string(s) {}
                /**
                 * \brief Constructs a ConfigString object from a buffer.
                 * \param s String buffer
                 * \param n Number of characters to copy
                 */
                ConfigString(const char* s, size_t n) : std::string(s, n) {}
                /**
                 * \brief Constructs a ConfigString object from a fill character.
                 */
                ConfigString(size_t n, char c) : std::string(n, c) {}
                /**
                 * \brief Constructs a ConfigString object from a range.
                 * \param first Iterator to first character in the range
                 * \param last Iterator to last character in the range
                 */
                template <class InputIterator>
                    ConfigString(InputIterator first, InputIterator last) :
                        std::string(first, last) {}
                /**
                 * \brief Constructs a ConfigString object from an initializer list.
                 * \param il Initializer list
                 */
                ConfigString(std::initializer_list<char> il) : std::string(il) {}
                /**
                 * \brief Move constructor.
                 * \param str String to move.
                 */
                ConfigString(std::string&& str) noexcept : std::string(str) {}
                /**
                 * \brief Constructs a ConfigString object.
                 * \param i String value, as an integer.
                 */
                ConfigString(int i) : std::string( std::to_string(i) ) {}
                /**
                 * \brief Constructs a ConfigString object.
                 * \param i String value, as an unsigned integer.
                 */
                ConfigString(unsigned int i) : std::string( std::to_string(i) ) {}
                /**
                 * \brief Constructs a ConfigString object.
                 * \param l String value, as a long integer.
                 */
                ConfigString(long l) : std::string( std::to_string(l) ) {}
                /**
                 * \brief Constructs a ConfigString object.
                 * \param b String value, as a Boolean value.
                 */
                ConfigString(bool b) : std::string( b ? "1" : "0" ) {}
                /**
                 * \brief Constructs a ConfigString object.
                 * \param f String value, as a floating-point value.
                 */
                ConfigString(float f) : std::string( std::to_string(f) ) {}
                /**
                 * \brief Constructs a ConfigString object.
                 * \param f String value, as a double floating-point value.
                 */
                ConfigString(double f) : std::string( std::to_string(f) ) {}
                /**
                 * \brief Destroys a ConfigString object.
                 */
                virtual ~ConfigString() {}
                /**
                 * \brief Assigns a value to this object.
                 * \param s String value.
                 */
                ConfigString& operator=(const std::string& s);
                /**
                 * \brief Assigns a value to this object.
                 * \param s String literal value.
                 */
                ConfigString& operator=(const char* s);
                /**
                 * \brief Assigns a value to this object.
                 * \param i String value, as an integer.
                 */
                ConfigString& operator=(int i);
                /**
                 * \brief Assigns a value to this object.
                 * \param i String value, as an unsigned integer.
                 */
                ConfigString& operator=(unsigned int i);
                /**
                 * \brief Assigns a value to this object.
                 * \param l String value, as a long integer.
                 */
                ConfigString& operator=(long l);
                /**
                 * \brief Assigns a value to this object.
                 * \param b String value, as a Boolean value.
                 */
                ConfigString& operator=(bool b);
                /**
                 * \brief Assigns a value to this object.
                 * \param f String value, as a floating-point value.
                 */
                ConfigString& operator=(float f);
                /**
                 * \brief Assigns a value to this object.
                 * \param f String value, as a double floating-point value.
                 */
                ConfigString& operator=(double f);
                /**
                 * \brief Retrieves a value from this object.
                 * \returns The value, as an integer.
                 */
                int asInt() const;
                /**
                 * \brief Retrieves a value from this object.
                 * \returns The value, as an unsigned integer.
                 */
                unsigned int asUInt() const;
                /**
                 * \brief Retrieves a value from this object.
                 * \returns The value, as a long integer.
                 */
                long asLong() const;
                /**
                 * \brief Retrieves a value from this object.
                 * \returns The value, as a Boolean value.
                 */
                bool asBool() const;
                /**
                 * \brief Retrieves a value from this object.
                 * \returns The value, as a floating-point value.
                 */
                float asFloat() const;
                /**
                 * \brief Retrieves a value from this object.
                 * \returns The value, as a double floating-point value.
                 */
                double asDouble() const;

        }; // class ConfigString

    } // namespace Driver

} // namespace LibCyberRadio

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_CONFIGSTRING_H */
