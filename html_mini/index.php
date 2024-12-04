<?php
function respond($message, $type = "text")
{
    if ($type === "json") {
        header('Content-Type: application/json');
        echo json_encode($message, JSON_PRETTY_PRINT);
    } else {
        echo $message;
    }
    die();
}

function respondWithError($message)
{
    http_response_code(400); // Bad Request
    respond($message);
}

// Ensure the request method is POST
if ($_SERVER['REQUEST_METHOD'] != 'POST') {
    respondWithError('ERR_NO_POST');
}

// Read the raw POST data
$post = file_get_contents("php://input");
if (!$post) {
    respondWithError('STILL_NO_POST');
}

// Constants
const FORMAT_UNKNOWN = "unknown";
const FORMAT_JSON = "json";
const FORMAT_XML = "xml";
const XML_VARIANT_CONFIG = "_config.xml";
const XML_VARIANT_READING = "_reading";
const HC_OK_STR = 'HC_OK';
const SUCCESS_STR = 'SUCCESS';
const DATA_RESPONSE = "data_response";

$post_format = FORMAT_XML;
$xml_variant = FORMAT_UNKNOWN;

// Determine the format of the POST data
if (!$device_data = json_decode($post, false)) {
    libxml_use_internal_errors(true);
    $device_data = simplexml_load_string($post);
    if ($device_data) {
        $post_format = FORMAT_XML;
        if (isset($device_data->device)) {
            $xml_variant = XML_VARIANT_CONFIG;
        } elseif (isset($device_data->reading)) {
            $xml_variant = XML_VARIANT_READING;
        }
    } else {
        $post_format = FORMAT_UNKNOWN;
    }
} else {
    $post_format = FORMAT_JSON;
}

// Respond based on the XML variant
if ($xml_variant == XML_VARIANT_CONFIG) {
    respond(HC_OK_STR);
} elseif (strpos($xml_variant, XML_VARIANT_READING) !== false) {
    respond(SUCCESS_STR);
} else {
    respond([DATA_RESPONSE => SUCCESS_STR], "json");
}
