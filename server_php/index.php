<?php

require_once 'mg/DataStorage.php';
require_once 'mg/config.php';
require_once 'mg/Factory.php';

function execute($request_body) {
	try {
		global $MG_SERIALIZE_FORMAT;
		global $MG_XML;

		DataStorage::$PATH_TO_DATA = $MG_SERIALIZE_FORMAT == $MG_XML?'data.xml':'data.json';

		$request  = Factory::create_command($request_body);
		$response = $request->execute();
		$response = Factory::serialize_command($response);

		echo $response;

	} catch (Exception $e) {
		echo ('error');
	}
}

$request_body = $_GET["request"];
execute($request_body)

?>