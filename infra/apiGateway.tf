module "homecare_api" {
    source          = "https://github.com/jmpcba/modulos_tf.git//apigateway?ref=0.0.2"
    api_name        = "HOMECARE BACKEND API"
    api_description = "backend de HomeCare"
    client_name     = "homecare"
}

#especialidades
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "especialidad"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#feriados
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "feriado"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#liquidacion
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "liquidacion"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#modulo
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "modulo"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#submodulo
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "submodulo"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#paciente
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "paciente"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#practica
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "practica"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#prestador
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "prestador"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#usuario
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "usuario"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}

#zonas
module "especialidades_resource" {
    source = "https://github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.2"
    restapi_id = "${module.homecare_api.api_id}"
    resource_path = "zona"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"

}