/***************************************************************************
 * \file ConfigString.cpp
 * \brief Defines a string class that supports several non-string data
 *    types for value setting and retrieval.
 * \author DA
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 * \note Requires C++11 compiler support.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/ConfigString.h"
//#include <iostream>


namespace LibCyberRadio
{
    namespace Driver
    {

        ConfigString& ConfigString::operator=(const std::string& s)
        {
            //std::cout << "[ConfigString assign][in] string=\"" << s << "\"" << std::endl;
            std::string::operator=( s );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        ConfigString& ConfigString::operator=(const char* s)
        {
            //std::cout << "[ConfigString assign][in] literal=\"" << s << "\"" << std::endl;
            std::string::operator=( s );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        ConfigString& ConfigString::operator=(int i)
        {
            //std::cout << "[ConfigString assign][in] int=" << i << std::endl;
            std::string::operator=( std::to_string(i) );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        ConfigString& ConfigString::operator=(unsigned int i)
        {
            //std::cout << "[ConfigString assign][in] uint=" << i << std::endl;
            std::string::operator=( std::to_string(i) );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        ConfigString& ConfigString::operator=(long l)
        {
            //std::cout << "[ConfigString assign][in] long=" << l << std::endl;
            std::string::operator=( std::to_string(l) );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        ConfigString& ConfigString::operator=(bool b)
        {
            //std::cout << "[ConfigString assign][in] bool=" << (b ? "true" : "false") << std::endl;
            std::string::operator=( b ? "1" : "0" );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        ConfigString& ConfigString::operator=(float f)
        {
            //std::cout << "[ConfigString assign][in] float=" << f << std::endl;
            std::string::operator=( std::to_string(f) );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        ConfigString& ConfigString::operator=(double f)
        {
            //std::cout << "[ConfigString assign][in] dbl=" << f << std::endl;
            std::string::operator=( std::to_string(f) );
            //std::cout << "[ConfigString assign][out] string=\"" << *this << "\"" << std::endl;
            return *this;
        }

        int ConfigString::asInt() const
        {
            return std::stoi(*this);
        }

        unsigned int ConfigString::asUInt() const
        {
            return (unsigned int)std::stoul(*this);
        }

        long ConfigString::asLong() const
        {
            return std::stol(*this);
        }

        bool ConfigString::asBool() const
        {
            int tmp = this->asInt();
            return !(tmp == 0);
        }

        float ConfigString::asFloat() const
        {
            return std::stof(*this);
        }

        double ConfigString::asDouble() const
        {
            return std::stod(*this);
        }

    } // namespace Driver

} // namespace LibCyberRadio
