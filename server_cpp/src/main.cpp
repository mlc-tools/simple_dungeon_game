#ifdef WIN32
#	include <Windows.h>
#endif
#include "HttpServer.h"
#include "utils.h"
#include "mg/DataStorage.h"
#include "mg/Request.h"
#include "mg/mg_Factory.h"
#include "mg/config.h"
#include "mg/mg_extensions.h"
#include "mg/Registrar.h"
#include "pugixml/pugixml.hpp"
#include "jsoncpp/json.h"
#include <sstream>


#if SUPPORT_JSON_PROTOCOL

std::string kDataFileName("data.json");
#define SERIALIZE mg::serialize_command_to_json
#define DESERIALIZE mg::create_command_from_json

#elif SUPPORT_XML_PROTOCOL

std::string kDataFileName("data.xml");
#define SERIALIZE mg::serialize_command_to_xml
#define DESERIALIZE mg::create_command_from_xml

#endif


std::string handler(const std::map<std::string, std::string>& get)
{
	if (get.count("/?request") == 0)
		return "error: cannot parse request";
	auto payload = get.at("/?request");

	auto request = DESERIALIZE<mg::Request>(payload);
	auto response = request->execute();
	auto buffer = SERIALIZE<mg::Response>(response);

	log("Response: %s", buffer.c_str());

	return buffer;
}

void initialize_data_storage(int argc, char **argv)
{
	std::string root;
	if(argc > 1)
		root = argv[1];

	auto buffer = getFileContent(root + kDataFileName);
	if(buffer.empty())
	{
		log("use:\n./server [path to server]\nexample:\n./server /users/user/game/server_cpp/");
		log("current path to data: %s", (root + kDataFileName).c_str());
		exit(1);
	}
#if SUPPORT_JSON_PROTOCOL
	mg::DataStorage::shared().initialize_json(buffer);
#elif SUPPORT_XML_PROTOCOL
	mg::DataStorage::shared().initialize_xml(buffer);
#endif
}

int main(int argc, char **argv)
{
    mg::register_classes();
    initialize_data_storage();

	std::string ip("127.0.0.1");
    HttpServer server(ip, 8045);
	server.setHandler(handler);
    server.run();

	while(1)
	{
		sleep(10);
	}

    return 0;
}
