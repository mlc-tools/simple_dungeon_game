<?php

require_once 'mg/IVisitorRequest.php';
require_once 'mg/DataStorage.php';
require_once 'mg/config.php';

function buildRequest($obj) {
	global $MG_SERIALIZE_FORMAT;
	global $MG_XML;

	if ($MG_SERIALIZE_FORMAT == $MG_XML) {
		$class   = $obj->getName();
		$request = new $class;
		$request->deserialize($obj);
	} else {
		$class   = key($obj);
		$request = new $class;
		$request->deserialize($obj->$class);
	}
	return $request;

}

function execute($request_body) {
	try {
		global $MG_SERIALIZE_FORMAT;
		global $MG_XML;
		if ($MG_SERIALIZE_FORMAT == $MG_XML) {
			DataStorage::$PATH_TO_DATA = 'data.xml';

			$xml     = simplexml_load_string($request_body);
			$request = buildRequest($xml);

			$response     = $request->execute();
			$response_xml = simplexml_load_string('<'.$response->get_type().'/>');
			$response->serialize($response_xml);
			echo $response_xml->asXML();
		} else {
			DataStorage::$PATH_TO_DATA = 'data.json';

			$json    = json_decode($request_body);
			$request = buildRequest($json);

			$response      = $request->execute();
			$type          = $response->get_type();
			$response_json = json_decode('{"'.$type.'": {}}');
			$response->serialize($response_json->$type);
			echo json_encode($response_json);
		}

	} catch (Exception $e) {
		echo ('error');
	}
}

// $request_body = '{"RequestOpenTile": {"index": 1}}';
$request_body = $_GET["request"];
execute($request_body)

?>