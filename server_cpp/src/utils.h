//
//  utils.hpp
//  server
//
//  Created by Владимир Толмачев on 04/01/2018.
//  Copyright © 2018 user-i157. All rights reserved.
//

#ifndef utils_hpp
#define utils_hpp

#include <string>
#include <memory>
#include <exception>
#include <unistd.h>

#ifdef WIN32
#	define sleep(x) std::this_thread::sleep_for(std::chrono::milliseconds(x))
#endif

std::string getFileContent(const std::string& path);
void log(const char* szFormat, ...);

class Exception : public std::exception
{
public:
	Exception(const std::string& message) noexcept;
	virtual const char* what() const noexcept override;
private:
	std::string _message;
};

#endif /* utils_hpp */
