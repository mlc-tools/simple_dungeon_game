#include "HttpServer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

#ifdef _WIN32
#	define _WINSOCK_DEPRECATED_NO_WARNINGS 1
#   include <winsock2.h>
#   include <ws2tcpip.h>
#   include <windows.h>
#   include <io.h>
#   include <fcntl.h>
#   ifndef S_ISDIR
#       define S_ISDIR(x) (((x) & S_IFMT) == S_IFDIR)
#   endif
#	pragma comment(lib, "event_core.lib")
#	pragma comment(lib, "event_extra.lib")
#	pragma comment(lib, "event.lib")
#	pragma comment(lib, "Ws2_32.lib")
#else
#   include <sys/socket.h>
#   include <signal.h>
#   include <fcntl.h>
#   include <unistd.h>
#   include <dirent.h>
#   include <arpa/inet.h>
#endif

#include <event2/event.h>
#include <event2/http.h>
#include <event2/buffer.h>
#include <event2/keyvalq_struct.h>

#ifdef _WIN32
#   ifndef stat
#       define stat _stat
#   endif
#   ifndef fstat
#       define fstat _fstat
#   endif
#   ifndef open
#       define open _open
#   endif
#   ifndef close
#       define close _close
#   endif
#   ifndef O_RDONLY
#       define O_RDONLY _O_RDONLY
#   endif
#endif

HttpServer::HttpServer(const std::string& ip, int port)
    : _ip(ip)
    , _port(port)
{
}

void HttpServer::setHandler(const Handler& handler)
{
	_handler = handler;
}

void HttpServer::run()
{
    try
    {
#ifdef _WIN32
        WSADATA WSAData;
        WSAStartup(0x101, &WSAData);
#else
        if (signal(SIGPIPE, SIG_IGN) == SIG_ERR)
            throw Exception("error");
#endif
    
        _socket = socket(AF_INET, SOCK_STREAM, 0);
        if (evutil_make_listen_socket_reuseable(_socket) != 0)
            throw Exception("evutil_make_listen_socket_reuseable(listener) == 0");
        sockaddr_in addr;
        socklen_t addrLen(sizeof(addr));
        std::memset(&addr, 0, addrLen);
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = inet_addr(_ip.c_str());
        addr.sin_port = htons(_port);
        if (bind(_socket, reinterpret_cast<const sockaddr*>(&addr), addrLen) != 0)
            throw Exception("cannot bind port");
        if (evutil_make_socket_nonblocking(_socket) != 0)
            throw Exception("cannot make port as non blocking");
        if (listen(_socket, -1) != 0)
            throw Exception("cannot listen port");
        
        int32_t threadCount = 1;
        for (; threadCount > 0; --threadCount)
        {
			log("start thread");
            auto func = [this]()
            {
                event_base* base = event_base_new();
                evhttp* event_http = evhttp_new(base);
                if (evhttp_accept_socket(event_http, _socket) != 0)
                    throw Exception("cannot accept socket");
                evhttp_set_gencb(event_http, HttpServer::_callback, this);
                event_base_dispatch(base);
            };
            auto thread = std::thread(func);
            thread.detach();
            _threads.push_back(std::move(thread));
        }
    }
    catch(const std::exception& e)
    {
		log("exception: [%s]", e.what());
        exit(-1);
    }
}

std::string HttpServer::handle(const std::map<std::string, std::string>& request)
{
	return _handler ? _handler(request) : "";
}

void HttpServer::_callback(evhttp_request* req, void* arg)
{
    try
    {
        HttpServer* server = reinterpret_cast<HttpServer*>(arg);
        std::map<std::string, std::string> get;
        
        if (evhttp_request_get_command(req) != EVHTTP_REQ_GET) {
            throw Exception("not GET request");
        }
        std::string uri = evhttp_request_get_uri(req);
		
        struct evkeyvalq headers;
        evhttp_parse_query_str(evhttp_request_get_uri (req), &headers);
        auto begin = headers.tqh_first;
        while(begin && begin != *headers.tqh_last)
        {
            get[begin->key] = begin->value;
            begin = begin->next.tqe_next;
        }
		
		struct evbuffer *evb = evbuffer_new();
		
		auto iter = get.find("/?request");
		if (iter != get.end())
		{
			auto response = server->handle(get);
			evbuffer_add_printf(evb, "%s", response.c_str());
			evhttp_add_header(evhttp_request_get_output_headers(req),
							  "Content-Type",
							  "text/html");
		}
		evhttp_send_reply(req, 200, "OK", evb);
		evbuffer_free(evb);
    }
    catch(const std::exception& e)
    {
		log("exception: [%s]", e.what());
        
        struct evbuffer *evb = evbuffer_new();
        evbuffer_add_printf(evb, "exception: %s", e.what());
        evhttp_add_header(evhttp_request_get_output_headers(req), "Content-Type", "text/html");
        evhttp_send_reply(req, 200, "FAIL", evb);
        evbuffer_free(evb);
    }
}
