#ifdef WIN32
#	include <Windows.h>
#endif
#include "HttpServer.h"
#include "utils.h"
#include "mg/DataStorage.h"
#include "mg/Request.h"
#include "mg/Factory.h"
#include "mg/config.h"
#include "pugixml/pugixml.hpp"
#include "jsoncpp/json.h"
#include <sstream>


#if MG_SERIALIZE_FORMAT == MG_JSON
std::string kDataFileName("data.json");
#else
std::string kDataFileName("data.xml");
#endif


std::string handler(const std::map<std::string, std::string>& get)
{
	if (get.count("/?request") == 0)
		return "error: cannot parse request";
	auto payload = get.at("/?request");
	
	log("\n Request: %s", payload.c_str());
	
	auto request = mg::Factory::create_command<mg::Request>(payload);
	auto response = request->execute();
	auto buffer = mg::Factory::serialize_command(response);
	
	log("Response: %s", buffer.c_str());

	return buffer;
}

int main(int argc, char **argv)
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
	mg::DataStorage::shared().initialize(buffer);

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
