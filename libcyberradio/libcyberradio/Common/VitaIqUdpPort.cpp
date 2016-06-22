/***************************************************************************
 * \file VitaIqUdpPort.cpp
 *
 * \brief UDP port for handling incoming VITA 49 or I/Q data.
 *
 * \author DA
* \copyright 2016 CyberRadio Solutions, Inc.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <LibCyberRadio/Common/VitaIqUdpPort.h>
#include <stdarg.h>
#include <sstream>


namespace LibCyberRadio
{

	VitaIqUdpPort::VitaIqUdpPort(const std::string& host,
									   int port,
									   int packet_size,
									   bool debug) :
		Debuggable(debug, ""),
		host(host),
		port(port),
		packet_size(packet_size),
		connected(false),
		socket(NULL),
		recv_buffer(NULL),
		bytes_recvd(0)
	{
		// Set the object debug name
		std::ostringstream oss;
		oss << "VitaIqUdpPort " << port;
		d_debug_name = oss.str();
		// Allocate the receive buffer
		recv_buffer = new unsigned char[packet_size];
		memset(recv_buffer, 0, packet_size);
		// Connect to the UDP port
		boost::system::error_code error = boost::asio::error::host_not_found;
		std::string s_port = (boost::format("%d") % port).str();
		if (host.size() > 0)
		{
			boost::asio::ip::udp::resolver resolver(io_service);
			boost::asio::ip::udp::resolver::query query(boost::asio::ip::udp::v4(),
														host, s_port,
														boost::asio::ip::resolver_query_base::passive);
			io_service.run();
			endpoint = *resolver.resolve(query);
			if (errno > 0)
			{
				printf("cannot resolve host IP %s error: %s\n", host.c_str(),
						strerror(errno));
			}
			else
			{
				socket = new boost::asio::ip::udp::socket(io_service);
				socket->open(endpoint.protocol());
				boost::asio::socket_base::linger loption(true, 0);
				socket->set_option(loption);
				boost::asio::socket_base::reuse_address roption(true);
				socket->set_option(roption);
				socket->bind(endpoint);
				connected = true;
			}
		}
	}

	VitaIqUdpPort::~VitaIqUdpPort()
	{
		connected = false;
		io_service.reset();
		io_service.stop();
		if (socket != NULL)
		{
			socket->close();
			delete socket;
		}
		// Deallocate the receive buffer
		if (recv_buffer != NULL)
			delete [] recv_buffer;
	}

	void VitaIqUdpPort::read_data()
	{
		int socket_fd, result, num_received;
		fd_set readset;
		struct timeval timeout;
		timeout.tv_sec  = 0;
		timeout.tv_usec = 100;

		socket_fd = socket->native();
		/* Socket has been created and connected to the other party */
		do
		{
			FD_ZERO(&readset);
			FD_SET(socket_fd, &readset);
			result = select(socket_fd + 1, &readset, NULL, NULL, &timeout);
		} while (result == -1 && errno == EINTR);

		if (result > 0)
		{
			if (FD_ISSET(socket_fd, &readset))
			{
				/* The socket_fd has data available to be read */
				do
				{
					num_received = socket->receive(
							boost::asio::buffer(
								(void*)(recv_buffer + bytes_recvd),
								packet_size - bytes_recvd
								)
							);
					bytes_recvd += num_received;
				}
				while ( (num_received != 0) && (bytes_recvd < packet_size));
			}
		}
		else if (result < 0)
		{
			/* An error ocurred, just print it to stdout */
		}

	}

	void VitaIqUdpPort::clear_buffer()
	{
		memset(recv_buffer, 0, packet_size);
		bytes_recvd = 0;
	}

	bool VitaIqUdpPort::is_packet_ready() const
	{
		return (bytes_recvd == packet_size);
	}

} /* namespace LibCyberRadio */

