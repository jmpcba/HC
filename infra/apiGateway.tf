resource "aws_api_gateway_rest_api" "HC_REST_API" {
  name = "HC"
  description = "HC REST service"
}

resource "aws_api_gateway_resource" "databroker" {
    rest_api_id = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    parent_id   = "${aws_api_gateway_rest_api.HC_REST_API.root_resource_id}"
    path_part   = "databroker"
}

resource "aws_api_gateway_method" "databroker_get_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.databroker.id}"
    http_method          = "GET"
    authorization        = "NONE"
    request_validator_id ="0oesex"
    
    request_parameters   = {
            "method.request.querystring.id"    = false
            "method.request.querystring.table" = true
    }
}

resource "aws_api_gateway_integration" "databroker_get_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id             = "${aws_api_gateway_resource.databroker.id}"
    http_method             = "${aws_api_gateway_method.databroker_get_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}