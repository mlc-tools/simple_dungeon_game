/******************************************************************************/
/*
* Copyright 2014-2015 Vladimir Tolmachev
*
* Author: Vladimir Tolmachev
* Project: ml
* e-mail: tolm_vl@hotmail.com
* If you received the code is not the author, please contact me
*/
/******************************************************************************/

#ifndef __ml_Generics__
#define __ml_Generics__

#include <string>
#include "pugixml/pugixml.hpp"

template <typename T> T strTo(const std::string &value);
template <typename T> std::string toStr(T value);

//XML
template <class T> void set(pugi::xml_attribute& xml, T value);
template <class T> T get(const pugi::xml_attribute& xml);

template <class T> void set(pugi::xml_node& xml, const std::string& key, T value)
{
	auto attribute = xml.append_attribute(key.c_str());
	set<T>(attribute, value);
}
template <class T> T get(const pugi::xml_node& xml, const std::string& key)
{
	auto attribute = xml.attribute(key.c_str());
	if(attribute)
		return get<T>(attribute);
	return 0;
}

#endif
