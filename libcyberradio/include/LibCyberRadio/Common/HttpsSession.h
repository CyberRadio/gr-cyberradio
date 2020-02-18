/***************************************************************************
 * \file HttpsSession.h
 * \brief Defines an interface for establishing an HTTPS session.
 * \author DA
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 * \note Requires C++11 compiler support.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_HTTPSSESSION_H_
#define INCLUDED_LIBCYBERRADIO_HTTPSSESSION_H_

#include "LibCyberRadio/Common/Debuggable.h"
#include <curl/curl.h>
#include <sstream>
#include <string>


/**
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{

    /**
     * \brief Class that encapsulates an HTTPS session.
     */
    class HttpsSession : public Debuggable
    {
        public:
            /**
             * \brief Constructs an HttpsSession object.
             * \param debug Whether this object produces debug output.
             */
            HttpsSession(
                    bool debug = false
            );
            /**
             * \brief Destroys an HttpsSession object.
             */
            virtual ~HttpsSession();
            /**
             * \brief Gets data from a given URL over HTTPS.
             * \param url URL to use for the request.
             * \param verify Whether or not to use SSL verification.
             * \returns Whether the request was successfully performed.
             *    If this returns false, use getLastRequestErrorInfo()
             *    to get the reason why the request failed.
             */
            virtual bool get(
                    const std::string& url,
                    bool verify = true
            );
            /**
             * \brief Posts data to a given URL over HTTPS.
             * \param url URL to use for the request.
             * \param data Data to send in the body of the request.
             * \param length Length of the data to send (in bytes).
             * \param contentType Content type of the data.
             * \param verify Whether or not to use SSL verification.
             * \returns Whether the request was successfully performed.
             *    If this returns false, use getLastRequestErrorInfo()
             *    to get the reason why the request failed.
             */
            virtual bool post(
                    const std::string& url,
                    void* data,
                    size_t length,
                    const char* contentType = "text/plain",
                    bool verify = true
            );
            /**
             * \brief Gets the HTTPS response code from the last request.
             * \returns The response code.
             */
            virtual long getResponseCode() const;
            /**
             * \brief Gets the HTTPS header from the last request.
             * \returns A string containing the header.
             */
            virtual std::string getResponseHeader() const;
            /**
             * \brief Gets the HTTPS response body from the last request.
             * \returns A string containing the response body.
             */
            virtual std::string getResponseBody() const;
            /**
             * \brief Gets the error information for the last request.
             * \returns A string containing the error message.
             */
            virtual std::string getLastRequestErrorInfo() const;
            /**
             * \brief Write data into the header buffer.
             * \note Not intended to be called by user code.
             * \returns The number of bytes processed.
             */
            virtual size_t writeHeader(
                    char *ptr,
                    size_t size
            );
            /**
             * \brief Write data into the response buffer.
             * \note Not intended to be called by user code.
             * \returns The number of bytes processed.
             */
            virtual size_t writeResponseData(
                    char *ptr,
                    size_t size
            );

        protected:
            /**
             * \brief Initializes the session object to handle a new
             *    request.
             * \returns A libcurl error code.
             */
            virtual CURLcode initializeRequest();
            /**
             * \brief Returns a string corresponding to a libcurl error code.
             * \returns A string containing an error message.
             */
            virtual const char* debugCurl(
                    CURLcode x
            );
            /**
             * \brief Callback function that libcurl "writes" data to when
             *    retrieving an HTTPS response header.
             * \param buffer Buffer containing the data retrieved via HTTPS
             * \param size Size (in bytes) of each data element
             * \param nitems Number of data elements retrieved
             * \param userdata A pointer containing data that the user
             *    specified using CURLOPT_HEADERDATA. For the purposes
             *    of this class, this will be the pointer to an
             *    HttpsSession object.
             * \returns The number of bytes actually handled -- ideally,
             *    size * nmemb.
             */
            static size_t headerCallback(
                    char *buffer,
                    size_t size,
                    size_t nitems,
                    void *userdata
            );
            /**
             * \brief Callback function that libcurl "writes" data to when
             *    retrieving an HTTPS response body.
             * \param ptr Buffer containing the data retrieved via HTTPS
             * \param size Size (in bytes) of each data element
             * \param nmemb Number of data elements retrieved
             * \param userdata A pointer containing data that the user
             *    specified using CURLOPT_WRITEDATA. For the purposes
             *    of this class, this will be the pointer to an
             *    HttpsSession object.
             * \returns The number of bytes actually handled -- ideally,
             *    size * nmemb.
             */
            static size_t writeDataCallback(
                    char *ptr,
                    size_t size,
                    size_t nmemb,
                    void *userdata
            );

        protected:
            // libcurl handle
            CURL* _session;
            // HTTPS request data
            // -- Response code
            long _responseCode;
            // -- Response header
            std::ostringstream _header;
            // -- Response body
            std::ostringstream _response;
            // Error message from the last request
            std::string _lastReqErrInfo;
    };

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_HTTPSSESSION_H_ */
