/* -*- c++ -*- */
/***************************************************************************
 * \file Debuggable.h
 *
 * \brief Class that supports debug output.
 *
 * \author DA
 * \copyright 2017 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_LIBCYBERRADIO_DEBUGGABLE_H_
#define INCLUDED_LIBCYBERRADIO_DEBUGGABLE_H_

#include <string>
#include <stdio.h>

/**
 * Debug file pointer.
 */
#define DEBUG_FP stderr
/**
 * Debug time format.  This is a time format string compatible with strftime().
 */
#define DEBUG_TIME_FMT "%H:%M:%S"


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
        public:
            /*!
             * \brief Constructs a Debuggable object.
             *
             * \param debug Whether or not to create debug output.
             * \param debug_name Name for identifying this object in debug output.
             * \param debug_fp File to send debug output to.
             * \param debug_timefmt Format string for displaying timestamp, as compatible
             *     with strftime().  If this is an empty string, don't display a timestamp.
             */
            Debuggable(
                    bool debug = false,
                    const std::string& debug_name = "",
                    FILE* debug_fp = DEBUG_FP,
                    const std::string& debug_timefmt = DEBUG_TIME_FMT
            );
            /*!
             * \brief Destroys a Debuggable object.
             */
            virtual ~Debuggable();
            /*!
             * \brief Copies a Debuggable object.
             * \param other The Debuggable object to copy.
             */
            Debuggable(const Debuggable& other);
            /**
             * \brief Assignment operator for Debuggable objects.
             * \param other The Debuggable object to copy.
             * \returns A reference to the assigned object.
             */
            Debuggable& operator=(const Debuggable& other);
            /*!
             * \brief Sets the debug name for this object.
             *
             * Use this method to set unique debug names for objects of the same
             *    class for easy differentiation.
             *
             * \param debug_name Name for identifying this object in debug output.
             */
            virtual void setDebugName(
                    const std::string& debug_name
            );
            /*!
             * \brief Sets the debug file pointer for this object.
             *
             * \param debug_fp File to send debug output to.
             */
            virtual void setDebugFile(
                    FILE* debug_fp
            );
            /*!
             * \brief Sets the debug time format for this object.
             *
             * \param debug_timefmt Format string for displaying timestamp, as compatible
             *     with strftime().  If this is an empty string, don't display a timestamp.
             */
            virtual void setDebugTimeFormat(
                    const std::string& debug_timefmt
            );
            /*!
             * \brief Outputs debug information.
             *
             * This method follows the same semantics as printf().  Output is preceded
             * by a timestamp and the name of the object, if provided.
             *
             * \param format The printf()-style format string.
             * \param ... Comma-separated list of arguments to print.  Note that these
             *     need to be arguments that can be supported natively through
             *     printf().
             * \return The number of characters outputted.
             */
            virtual int debug(
                    const char *format,
                    ...
            );
            /**
             * \brief Gets a debug output string for a Boolean value.
             * \param x Boolean value
             * \returns A constant string, either "true" or "false".
             */
            virtual const char* debugBool(
                    bool x
            );
            /**
             * \brief Gets whether this object produces debug output.
             * \returns True if producing debug, false otherwise.
             */
            virtual bool isDebug() const;
            /**
             * \brief Gets the debug name for this object.
             * \returns The debug name, as a string.
             */
            virtual std::string getDebugName() const;
            /**
             * \brief Gets a "raw" string representation of a given data
             *     string.
             *
             * "Raw" string representations mimic Python string
             * representations.  Whitespace characters are denoted by
             * backslash representations ("\\r", "\\n", "\\t", "\\v",
             * "\\f"), while other non-printable characters are
             * represented with hex representation ("\\x00", etc.)
             *
             * \param data Data string
             * \returns The data's "raw" representation.
             */
            virtual std::string rawString(const std::string& data);

        protected:
            bool _debug;
            std::string _debugName;
            FILE* _debugFp;
            std::string _debugTimeFmt;
            char* _debugTimestamp;
            size_t _debugTimestampSize;
    };

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DEBUGGABLE_H_ */
