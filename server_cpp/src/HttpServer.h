//
//  HttpServer.hpp
//  libEvent
//
//  Created by user-i157 on 14/02/17.
//  Copyright © 2017 user-i157. All rights reserved.
//

#ifndef HttpServer_hpp
#define HttpServer_hpp

#include <stdio.h>
#include <map>
#include <list>
#include <vector>
#include <thread>
#include <string>
#include <functional>

struct evhttp_request;

class HttpServer
{
	using Handler = std::function<std::string(const std::map<std::string, std::string>&)>;
public:
    HttpServer(const std::string& ip, int port);
	void setHandler(const Handler& handler);
    void run();
protected:
    static void _callback(evhttp_request* req, void* arg);
	std::string handle(const std::map<std::string, std::string>& request);
private:
    std::string _ip;
    int _port;
    int _socket;
    std::list<std::thread> _threads;
	Handler _handler;
};

#endif /* HttpServer_hpp */
