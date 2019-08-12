# RESTAPI
resource "aws_api_gateway_rest_api" "HC_REST_API" {
  name = "HC"
  description = "HC REST service"
}

resource "aws_api_gateway_resource" "api_version_1" {
    rest_api_id = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    parent_id   = "${aws_api_gateway_rest_api.HC_REST_API.root_resource_id}"
    path_part   = "v1"
}

# DEPLOYMENTS - STAGES
resource "aws_api_gateway_stage" "prod_stage" {
  stage_name    = "${var.prod_stage_name}"
  rest_api_id   = "${aws_api_gateway_rest_api.HC_REST_API.id}"
  deployment_id = "${aws_api_gateway_deployment.databroker_prod_deployment.id}"
}


resource "aws_api_gateway_deployment" "databroker_prod_deployment" {
  depends_on = ["aws_api_gateway_integration.databroker_get_integration"]

  rest_api_id = "${aws_api_gateway_rest_api.HC_REST_API.id}"
  stage_name  = "prod"
}

resource "aws_api_gateway_stage" "dev_stage" {
  stage_name    = "DEV"
  rest_api_id   = "${aws_api_gateway_rest_api.HC_REST_API.id}"
  deployment_id = "${aws_api_gateway_deployment.dev_deployment.id}"
}


resource "aws_api_gateway_deployment" "dev_deployment" {
  depends_on = ["aws_api_gateway_integration.databroker_get_integration"]

  rest_api_id = "${aws_api_gateway_rest_api.HC_REST_API.id}"
  stage_name  = "DEV"
}

# DATABROKER RESOURCES
resource "aws_api_gateway_resource" "databroker" {
    rest_api_id = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    parent_id   = "${aws_api_gateway_resource.api_version_1.id}"
    path_part   = "databroker"
}


resource "aws_api_gateway_method" "databroker_get_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.databroker.id}"
    http_method          = "GET"
    authorization        = "NONE"
  
    request_parameters   = {
            "method.request.querystring.tables" = true
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

# PRESTADORES RESOURCES

resource "aws_api_gateway_resource" "prestador" {
    rest_api_id = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    parent_id   = "${aws_api_gateway_resource.api_version_1.id}"
    path_part   = "prestador"
}


resource "aws_api_gateway_method" "prestadores_put_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.prestador.id}"
    http_method          = "PUT"
    authorization        = "NONE"
  
    request_parameters   = {
            "method.request.querystring.id" = true
            "method.request.querystring.fecha" = true
    }
}

resource "aws_api_gateway_integration" "prestadores_put_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id             = "${aws_api_gateway_resource.prestador.id}"
    http_method             = "${aws_api_gateway_method.prestadores_put_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_prestador_service_lambda.arn}/invocations"
}

resource "aws_api_gateway_method" "prestadores_get_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.prestador.id}"
    http_method          = "GET"
    authorization        = "NONE"
}

resource "aws_api_gateway_integration" "prestadores_get_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id             = "${aws_api_gateway_resource.prestador.id}"
    http_method             = "${aws_api_gateway_method.prestadores_get_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_prestador_service_lambda.arn}/invocations"
}

resource "aws_api_gateway_method" "prestadores_post_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.prestador.id}"
    http_method          = "POST"
    authorization        = "NONE"
}

resource "aws_api_gateway_integration" "prestadores_post_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id             = "${aws_api_gateway_resource.prestador.id}"
    http_method             = "${aws_api_gateway_method.prestadores_post_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_prestador_service_lambda.arn}/invocations"
}

# PACIENTES RESOURCES
resource "aws_api_gateway_resource" "paciente" {
    rest_api_id = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    parent_id   = "${aws_api_gateway_resource.api_version_1.id}"
    path_part   = "paciente"
}


resource "aws_api_gateway_method" "pacientes_put_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.paciente.id}"
    http_method          = "PUT"
    authorization        = "NONE"
}

resource "aws_api_gateway_integration" "pacientes_put_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id             = "${aws_api_gateway_resource.paciente.id}"
    http_method             = "${aws_api_gateway_method.pacientes_put_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_paciente_service_lambda.arn}/invocations"
}

resource "aws_api_gateway_method" "pacientes_get_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.paciente.id}"
    http_method          = "GET"
    authorization        = "NONE"
}

resource "aws_api_gateway_integration" "prestadores_get_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id             = "${aws_api_gateway_resource.paciente.id}"
    http_method             = "${aws_api_gateway_method.pacientes_get_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_paciente_service_lambda.arn}/invocations"
}

resource "aws_api_gateway_method" "pacientes_post_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id          = "${aws_api_gateway_resource.paciente.id}"
    http_method          = "POST"
    authorization        = "NONE"
}

resource "aws_api_gateway_integration" "pacientes_post_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.HC_REST_API.id}"
    resource_id             = "${aws_api_gateway_resource.pacientes.id}"
    http_method             = "${aws_api_gateway_method.pacientes_post_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_pacientes_service_lambda.arn}/invocations"
}