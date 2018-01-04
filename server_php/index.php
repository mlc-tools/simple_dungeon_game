<?php

require_once 'mg/IVisitorRequest.php';
require_once 'mg/DataStorage.php';

function buildRequest($xml) {
	$class   = $xml->getName();
	$request = new $class;
	$request->deserialize($xml);

	return $request;
}

function execute($request_body) {
	try {
		DataStorage::$PATH_TO_DATA = 'data.xml';
		$xml                       = simplexml_load_string($request_body);

		$request      = buildRequest($xml);
		$response     = $request->execute();
		$response_xml = simplexml_load_string('<'.$response->get_type().'/>');
		$response->serialize($response_xml);
		echo $response_xml->asXML();
	} catch (Exception $e) {
		echo ('error');
	}
}

$request_body = $_GET["request"];
execute($request_body)

?>