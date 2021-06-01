/***************************************************************************
 * \file Thread.h
 *
 * \brief Basic threading using Boost Threads.
 *
 * \author DA
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_THREAD_H
#define INCLUDED_LIBCYBERRADIO_THREAD_H

#include <boost/thread.hpp>
#include <string>

/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    /*!
     * \brief Base class for a thread object, based on Boost Threads.
     *
     * Basic procedure for using this class:
     * \li Derive a threading class from Thread.
     * \li Override the run() method to provide the thread's processing
     *     loop.
     * \li Call the sleep() method on occasion within the run()
     *     method implementation to check for user interrupts.
     * \li Override onInterrupt() to perform processing that must
     *     be done when the thread is interrupted (stopped by the
     *     user).
     * \li Override onException() to perform processing that must
     *     be done when an unhandled exception occurs within the
     *     run() method.
     * \li Call the start() method from a higher-level thread or
     *     execution loop to begin thread processing.
     * \li Call the interrupt() method from a higher-level thread
     *     or execution loop to interrupt (stop) thread processing.
     *
     * \note Because this threading class is based on Boost Threads,
     *    users should use its sleep() method to do any waiting,
     *    because it checks for user interrupts within the Boost
     *    threading layer.
     */
    class Thread
    {
        public:
            /*!
             * \brief Creates a Thread object.
             *
             * \param name Name of this thread.
             * \param cls Class identifier string for this thread.
             */
            Thread(const std::string& name = "",
                    const std::string& cls = "");
            /*!
             * \brief Creates a Thread object by copying another Thread object.
             *
             * \param src The Thread object being copied.
             */
            Thread(const Thread& src);
            /*!
             * \brief Creates a Thread object by assignment from another Thread object.
             *
             * \param src The Thread object being copied.
             */
            virtual Thread& operator=(const Thread& src);
            /*!
             * \brief Destroys a Thread object.
             */
            virtual ~Thread();
            /*!
             * \brief Starts thread processing.
             */
            virtual void start();
            /*!
             * \brief Executes the main processing loop for the thread.
             *
             * Override this method in derived classes to perform thread
             * processing.
             */
            virtual void run() = 0;
            /*!
             * \brief Interrupts (stops) the thread.
             */
            virtual void interrupt();
            /*!
             * \brief Pauses thread execution for a given time, checking
             *    for user interrupts during that time.
             *
             * The sleep timer has microsecond resolution.
             *
             * \param secs Number of seconds to "sleep".
             */
            virtual void sleep(double secs);
            /*!
             * \brief Determines if the thread is running or not.
             * \return True if the thread is running, false otherwise.
             */
            virtual bool isRunning() const;
            /*!
             * \brief Sets the name of the thread.
             * \param name The new name of the thread.
             */
            virtual void setName(const std::string& name);
            /*!
             * \brief Sets the class identifer string for the thread.
             * \param cls The new class identifer for the thread.
             */
            virtual void setClass(const std::string& cls);
            /*!
             * \brief Gets the identifier of the underlying Boost thread.
             * \return The thread identifier.  If the thread is not running,
             *    this returns boost::thread().
             */
            virtual boost::thread::id getId() const;
            /*!
             * \brief Gets the identifier string for this thread.
             * \return The thread identifier string.
             */
            virtual std::string getIdString() const;
            /*!
             * \brief Executes code that must run when the thread is
             *    interrupted.
             *
             * The base-class method does nothing.  Override this method
             * in derived classes to perform custom interrupt processing.
             */
            virtual void onInterrupt();
            /*!
             * \brief Executes code that must run when an unhandled
             *    exception occurs within the thread.
             *
             * The base-class method does nothing.  Override this method
             * in derived classes to perform custom exception processing.
             *
             * \param ex The exception that occurred.
             */
            virtual void onException(const std::exception& ex);

        protected:
            virtual void thisThreadRun();

        protected:
            boost::thread _thisThread;
            std::string _name;
            std::string _class;
            bool _isRunning;
    };

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_THREAD_H */
