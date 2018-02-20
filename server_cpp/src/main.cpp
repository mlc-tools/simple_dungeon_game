#ifdef WIN32
#	include <Windows.h>
#endif
#include "HttpServer.h"
#include "utils.h"
#include "mg/DataStorage.h"
#include "mg/Request.h"
#include "Factory.h"
#include "pugixml/pugixml.hpp"
#include "jsoncpp/json.h"
#include <sstream>
#include "mg/config.h"

#if MG_SERIALIZE_FORMAT == MG_JSON

intrusive_ptr<mg::Request> createRequest(const std::string& payload)
{
	Json::Value json;
	Json::Reader reader;
	reader.parse(payload, json);
	
	auto type = json.getMemberNames()[0];
	auto request = Factory::shared().build<mg::Request>(type);
	if (request != nullptr)
		request->deserialize(json[type]);
	return request;
}

std::string getSerializedString(const mg::SerializedObject* object)
{
	Json::Value json;
	object->serialize(json[object->get_type()]);
	
	Json::StreamWriterBuilder wbuilder;
	wbuilder["indentation"] = "";
	auto string = Json::writeString(wbuilder, json);
	
	return string;
}

#elif MG_SERIALIZE_FORMAT == MG_XML

intrusive_ptr<mg::Request> createRequest(const std::string& payload)
{
	pugi::xml_document doc;
	doc.load(payload.c_str());
	auto root = doc.root().first_child();
	auto request = Factory::shared().build<mg::Request>(root.name());
	request->deserialize(root);
	return request;
}

std::string getSerializedString(const mg::SerializedObject* object)
{
	pugi::xml_document doc;
	auto root = doc.append_child(object->get_type().c_str());
	object->serialize(root);
	
	std::stringstream stream;
	pugi::xml_writer_stream writer(stream);
	doc.save(writer, "", pugi::format_no_declaration | pugi::format_raw, pugi::xml_encoding::encoding_utf8);
	return stream.str();
}

#endif



std::string handler(const std::map<std::string, std::string>& get)
{
	if (get.count("/?request") == 0)
		return "error: cannot parse request";
	auto payload = get.at("/?request");
	log("\n Request: %s", payload.c_str());
	auto request = createRequest(payload);
	auto response = request->execute();
	auto buffer = getSerializedString(response);
	log("Response: %s", buffer.c_str());

	return buffer;
}

int main(int argc, char **argv)
{
	std::string root;
	if(argc > 1)
		root = argv[1];

#if MG_SERIALIZE_FORMAT == MG_JSON
	auto buffer = getFileContent(root + "data.json");
#else
	auto buffer = getFileContent(root + "data.xml");
#endif
	if(buffer.empty())
	{
		log("use:\n./server [path to server]\nexemple:\n./server /users/user/game/server_cpp/");
		exit(1);
	}
	mg::DataStorage::shared().initialize(buffer);

	std::string ip("127.0.0.1");
    HttpServer server(ip, 8045);
	server.setHandler(handler);
    server.run();
	while(1)
	{
		sleep(1);
	}
	
    return 0;
}
