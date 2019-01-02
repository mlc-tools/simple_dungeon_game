<?php

require_once 'mg/DataStorage.php';
require_once 'mg/config.php';
require_once 'mg/Factory.php';

function execute($request_body) {
	try {
		global $MG_SERIALIZE_FORMAT;
		global $MG_XML;

		DataStorage::$PATH_TO_DATA = Config::$SUPPORT_XML_PROTOCOL?'data.xml':'data.json';

        if(Config::$SUPPORT_XML_PROTOCOL){
		    $request  = Factory::create_command_from_xml($request_body);
		    $response = $request->execute();
		    $response = Factory::serialize_command_to_xml($response);
		} else {
		    $request  = Factory::create_command_from_json($request_body);
		    $response = $request->execute();
		    $response = Factory::serialize_command_to_json($response);
		}
		echo $response;

	} catch (Exception $e) {
		echo ('error');
	}
}

$request_body = $_GET["request"];
execute($request_body)

?>