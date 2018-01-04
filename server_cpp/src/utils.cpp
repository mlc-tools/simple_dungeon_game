//
//  utils.cpp
//  server
//
//  Created by Владимир Толмачев on 04/01/2018.
//  Copyright © 2018 user-i157. All rights reserved.
//

#include "utils.h"
#include <stdio.h>
#include <stdarg.h>
#include <algorithm>
#include <iostream>
#include <fstream>

#ifdef WIN32
#	include <Windows.h>
#	include <WinBase.h>
#endif

#define MAX_LOG_LENGTH 16*1024

void _log(const char *format, va_list args);

void log(const char* szFormat, ...)
{
	va_list args;
	va_start(args, szFormat);
	_log(szFormat, args);
	va_end(args);
}

void _log(const char *format, va_list args)
{
	int bufferSize = MAX_LOG_LENGTH;
	char* buf = nullptr;
	do
	{
		buf = new char[bufferSize];
		if (buf == nullptr)
			return;
		
		int ret = vsnprintf(buf, bufferSize - 3, format, args);
		if (ret < 0)
		{
			bufferSize *= 2;
			
			delete[] buf;
		}
		else
			break;
		
	} while (true);
	
#ifdef WIN32
	int pos = 0;
	int len = strlen(buf);
	char tempBuf[MAX_LOG_LENGTH + 1] = { 0 };
	WCHAR wszBuf[MAX_LOG_LENGTH + 1] = { 0 };
	
	do
	{
		std::copy(buf + pos, buf + pos + MAX_LOG_LENGTH, tempBuf);
		
		tempBuf[MAX_LOG_LENGTH] = 0;
		
		MultiByteToWideChar(CP_UTF8, 0, tempBuf, -1, wszBuf, sizeof(wszBuf));
		OutputDebugStringW(wszBuf);
		OutputDebugStringW(L"\n");
		WideCharToMultiByte(CP_ACP, 0, wszBuf, -1, tempBuf, sizeof(tempBuf), nullptr, FALSE);
		printf("%s\n", tempBuf);
		
		pos += MAX_LOG_LENGTH;
		
	} while (pos < len);
	
#else
	std::cout << buf << std::endl;
#endif
	fflush(stdout);
}

std::string getFileContent(const std::string& path)
{
	std::fstream stream(path, std::ios::in);
	if (stream.is_open() == false)
		return "";
	std::string str((std::istreambuf_iterator<char>(stream)), std::istreambuf_iterator<char>());
	return str;
}


Exception::Exception(const std::string& message) noexcept
: _message(message)
{
}

const char* Exception::what() const noexcept
{
	return _message.c_str();
}

