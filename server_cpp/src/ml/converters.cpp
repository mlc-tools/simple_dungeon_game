#include "converters.h"
#include <sstream>
#include <stdio.h>

std::string boolToStr(bool value)
{
	return value ? "yes" : "no";
};

std::string intToStr(int value)
{
	return std::to_string(value);
};

std::string floatToStr(float value)
{
	return std::to_string(value);
};

std::string floatToStr2(float value)
{
	return std::to_string(value);
};

bool strToBool(const std::string & value)
{
	if (value.empty())
		return false;
	bool result(false);
	result = result || value == "yes";
	result = result || value == "Yes";
	result = result || value == "true";
	result = result || value == "True";
	return result;
}

int strToInt(const std::string & value)
{
	if(value.empty())
		return 0;
	std::stringstream ss(value);
	int result(0);
	ss >> result;
	return result;
}

float strToFloat(const std::string & value)
{
	if(value.empty())
		return 0;
	std::stringstream ss(value);
	float result(0.f);
	ss >> result;
	return result;
}

