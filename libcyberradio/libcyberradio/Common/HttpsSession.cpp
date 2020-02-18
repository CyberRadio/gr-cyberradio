/***************************************************************************
 * \file HttpsSession.cpp
 * \brief Implements an interface for establishing an HTTPS session.
 * \author DA
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 * \note Requires C++11 compiler support.
 *
 ***************************************************************************/

#include "LibCyberRadio/Common/HttpsSession.h"
#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <curl/curl.h>
#include <memory>
#include <cstring>


namespace LibCyberRadio
{

    // Singleton-pattern object whose entire purpose is to call
    // curl_global_init() once, when the first HttpsSession object
    // is instantiated.
    class CurlGlobalInitializer : public Debuggable
    {
        public:
            CurlGlobalInitializer(CurlGlobalInitializer const&) = delete;
            CurlGlobalInitializer& operator=(CurlGlobalInitializer const&) = delete;

            static std::shared_ptr<CurlGlobalInitializer> instance()
            {
                static std::shared_ptr<CurlGlobalInitializer> s{new CurlGlobalInitializer};
                return s;
            }

        private:
            CurlGlobalInitializer() :
                Debuggable(false, "CurlGlobalInitializer")
            {
                this->debug("Initializing CURL\n");
                curl_global_init(CURL_GLOBAL_ALL);
            }
    };


    HttpsSession::HttpsSession(
            bool debug
        ) :
        Debuggable(debug, "HttpsSession"),
        _session(curl_easy_init()),
        _responseCode(0),
        //_postHeaders(NULL),
        //_postBuffer(NULL),
        _lastReqErrInfo("")
    {
        CurlGlobalInitializer::instance();
        this->debug("CONSTRUCTED\n");
    }

    HttpsSession::~HttpsSession()
    {
        // Clear post header and data buffers
        //clearPostBuffers();
        // Clean up the session object
        curl_easy_cleanup(_session);
        this->debug("DESTROYED\n");
    }

    bool HttpsSession::get(
            const std::string& url,
            bool verify
        )
    {
        this->debug("[get] Called; URL=%s, verify=%s\n",
                url.c_str(), this->debugBool(verify));
        CURLcode res;
        // Clear HTTPS request stuff
        res = initializeRequest();
        // Set request options
        this->debug("[get] Setting request options\n");
        curl_easy_setopt(_session, CURLOPT_URL, url.c_str());
        curl_easy_setopt(_session, CURLOPT_SSL_VERIFYPEER, verify ? 1L : 0L);
        curl_easy_setopt(_session, CURLOPT_SSL_VERIFYHOST, verify ? 1L : 0L);
        curl_easy_setopt(_session, CURLOPT_HTTPGET, 1L);
        // Execute the request
        this->debug("[get] Executing request\n");
        res = curl_easy_perform(_session);
        this->debug("[get] Request status: %d (%s)\n", res, this->debugCurl(res));
        _lastReqErrInfo = this->debugCurl(res);
        bool ret = (res == CURLE_OK);
        if ( ret )
        {
            curl_easy_getinfo(_session, CURLINFO_RESPONSE_CODE, &_responseCode);
            this->debug("[get] Response code: %ld\n", getResponseCode());
            this->debug("[get] Header:\n%s\n", getResponseHeader().c_str());
            this->debug("[get] Response:\n%s\n", getResponseBody().c_str());
            // Handle HTTPS response codes that indicate error conditions
            // The first line of the header will provide the reason why
            if (_responseCode >= 400)
            {
                ret = false;
                BasicStringList vec = Pythonesque::Split(getResponseHeader(), "\n", 1);
                _lastReqErrInfo = vec[0];
            }
        }
        this->debug("[get] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    bool HttpsSession::post(
            const std::string& url,
            void* data,
            size_t length,
            const char* contentType,
            bool verify
        )
    {
        this->debug("[post] Called; URL=%s, verify=%s\n",
                url.c_str(), this->debugBool(verify));
        CURLcode res;
        // Clear HTTPS request stuff
        initializeRequest();
        // Set request options
        this->debug("[post] Setting request options\n");
        curl_easy_setopt(_session, CURLOPT_VERBOSE, 0L);
        curl_easy_setopt(_session, CURLOPT_URL, url.c_str());
        curl_easy_setopt(_session, CURLOPT_SSL_VERIFYPEER, verify ? 1L : 0L);
        curl_easy_setopt(_session, CURLOPT_SSL_VERIFYHOST, verify ? 1L : 0L);
        struct curl_slist* headers = NULL;
        char ctheader[80];
        memset(ctheader, 0, sizeof(ctheader));
        strcpy(ctheader, "Content-type: ");
        strcat(ctheader, contentType);
        headers = curl_slist_append(headers, ctheader);
        curl_easy_setopt(_session, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(_session, CURLOPT_POSTFIELDS, data);
        curl_easy_setopt(_session, CURLOPT_POSTFIELDSIZE, (long)length);
        curl_easy_setopt(_session, CURLOPT_POST, 1L);
        // Execute the request
        this->debug("[post] Executing request\n");
        res = curl_easy_perform(_session);
        this->debug("[post] Request status: %d (%s)\n", res, this->debugCurl(res));
        _lastReqErrInfo = this->debugCurl(res);
        bool ret = (res == CURLE_OK);
        if ( ret )
        {
            curl_easy_getinfo(_session, CURLINFO_RESPONSE_CODE, &_responseCode);
            this->debug("[post] Response code: %ld\n", getResponseCode());
            this->debug("[post] Header:\n%s\n", getResponseHeader().c_str());
            this->debug("[post] Response:\n%s\n", getResponseBody().c_str());
            // Handle HTTPS response codes that indicate error conditions
            // The first line of the header will provide the reason why
            if (_responseCode >= 400)
            {
                ret = false;
                BasicStringList vec = Pythonesque::Split(getResponseHeader(), "\n", 1);
                _lastReqErrInfo = vec[0];
            }
        }
        curl_slist_free_all(headers);
        this->debug("[post] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    long HttpsSession::getResponseCode() const
    {
        return _responseCode;
    }

    std::string HttpsSession::getResponseHeader() const
    {
        return _header.str();
    }

    std::string HttpsSession::getResponseBody() const
    {
        return _response.str();
    }

    std::string HttpsSession::getLastRequestErrorInfo() const
    {
        return _lastReqErrInfo;
    }

    size_t HttpsSession::writeHeader(
            char *ptr,
            size_t size
        )
    {
        //this->debug("[writeHeader] Called; size=%u\n", size);
        _header.write(ptr, size);
        //this->debug("[writeHeader] Returning\n");
        return size;
    }

    size_t HttpsSession::writeResponseData(
            char *ptr,
            size_t size
        )
    {
        //this->debug("[writeResponseData] Called; size=%u\n", size);
        _response.write(ptr, size);
        //this->debug("[writeResponseData] Returning\n");
        return size;
    }

    CURLcode HttpsSession::initializeRequest()
    {
        this->debug("[initializeRequest] Called\n");
        CURLcode res;
        _header.clear();
        _header.str("");
        _response.clear();
        _response.str("");
        _responseCode = 0;
        //clearPostBuffers();
        curl_easy_reset(_session);
        // Setting up the header buffer takes two steps:
        // -- Set option CURLOPT_HEADERFUNCTION to the static
        //    headerCallback() method
        // -- Set option CURLOPT_HEADERDATA to the "this" pointer
        //    for this object
        res = curl_easy_setopt(_session, CURLOPT_HEADERFUNCTION,
                HttpsSession::headerCallback);
        if ( res == CURLE_OK )
        {
            res = curl_easy_setopt(_session, CURLOPT_HEADERDATA, this);
        }
        // Setting up the response buffer takes two steps:
        // -- Set option CURLOPT_WRITEFUNCTION to the static
        //    writeDataCallback() method
        // -- Set option CURLOPT_WRITEDATA to the "this" pointer
        //    for this object
        if ( res == CURLE_OK )
        {
            res = curl_easy_setopt(_session, CURLOPT_WRITEFUNCTION,
                    HttpsSession::writeDataCallback);
        }
        if ( res == CURLE_OK )
        {
            res = curl_easy_setopt(_session, CURLOPT_WRITEDATA, this);
        }
        this->debug("[initializeRequest] Returning %d (%s)\n", res, this->debugCurl(res));
        return res;
    }

    const char* HttpsSession::debugCurl(
            CURLcode x
        )
    {
        return curl_easy_strerror(x);
    }

    size_t HttpsSession::headerCallback(
            char *buffer,
            size_t size,
            size_t nitems,
            void *userdata
        )
    {
        // "userdata" contains the "this" pointer to the session object
        HttpsSession *session = (HttpsSession *)userdata;
        size_t bytes = size * nitems;
        return session->writeHeader(buffer, bytes);
    }

    size_t HttpsSession::writeDataCallback(
            char *ptr,
            size_t size,
            size_t nmemb,
            void *userdata
        )
    {
        // "userdata" contains the "this" pointer to the session object
        HttpsSession *session = (HttpsSession *)userdata;
        size_t bytes = size * nmemb;
        return session->writeResponseData(ptr, bytes);
    }

} /* namespace LibCyberRadio */
