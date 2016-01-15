/***************************************************************************
 * \file Thread.cpp
 *
 * \brief Basic threading using Boost Threads.
 *
 * \author DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#include "Thread.h"
#include <boost/chrono.hpp>
#include <sstream>
#include <string>

namespace gr
{
	namespace CyberRadio
	{

		Thread::Thread(const std::string& name, const std::string& cls)
		{
			_name = name;
			_class = cls;
			_isRunning = false;
			_thisThread = boost::thread();
		}

		Thread::Thread(const Thread& src)
		{
			_name = src._name;
			_class = src._class;
			_isRunning = src._isRunning;
		}

		Thread& Thread::operator=(const Thread& src)
		{
			if ( this != &src )
			{
				_name = src._name;
				_class = src._class;
				_isRunning = src._isRunning;
			}
			return *this;
		}

		Thread::~Thread()
		{
			if ( _thisThread.get_id() != boost::thread::id() )
			{
				_thisThread.interrupt();
				_thisThread.join();
			}
		}

		void Thread::start()
		{
			_thisThread = boost::thread(&Thread::thisThreadRun, this);
		}

		void Thread::interrupt()
		{
			_thisThread.interrupt();
		}

		void Thread::sleep(double secs)
		{
			boost::this_thread::sleep_for(boost::chrono::microseconds((int)(secs * 1000000)));
		}

		bool Thread::isRunning() const
		{
			return _isRunning;
		}

		void Thread::setName(const std::string& name)
		{
			_name = name;
		}

		void Thread::setClass(const std::string& cls)
		{
			_class = cls;
		}

		void Thread::onInterrupt()
		{
		}

		boost::thread::id Thread::getId() const
		{
			return _thisThread.get_id();
		}

		std::string Thread::getIdString() const
		{
			std::string ret;
			if ( _name != "" )
				ret = _name;
			else if ( _class != "" )
			{
				std::ostringstream oss;
				oss << _class << "-" << _thisThread.get_id();
				ret = oss.str();
			}
			return ret;
		}

		void Thread::onException(const std::exception& ex)
		{
		}

		void Thread::thisThreadRun()
		{
			_isRunning = true;
			try
			{
				run();
			}
			catch(boost::thread_interrupted& ex)
			{
				onInterrupt();
			}
			catch(std::exception& ex)
			{
				onException(ex);
			}
			_isRunning = false;
			_thisThread = boost::thread();
		}

	} /* namespace CyberRadio */
}

