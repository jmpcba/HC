module "homecare_api" {
    source          = "github.com/jmpcba/modulos_tf.git//apigateway?ref=0.0.3"
    api_name        = "HOMECARE BACKEND API"
    api_description = "backend de HomeCare"
    client_name     = "homecare"
}

#especialidades
module "especialidades_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "especialidad"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#feriados
module "feriados_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "feriado"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#liquidacion
module "liquidacion_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "liquidacion"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#modulo
module "modulo_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "modulo"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#submodulo
module "submodulo_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "submodulo"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#paciente
module "paciente_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "paciente"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#practica
module "practica_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "practica"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#prestador
module "prestador_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "prestador"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#usuario
module "usuario_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource?ref=0.0.3"
    restapi_id = module.homecare_api.api_id
    resource_path = "usuario"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}

#zonas
module "zonas_resource" {
    source = "github.com/jmpcba/modulos_tf.git//apigateway_resource"
    restapi_id = module.homecare_api.api_id
    resource_path = "zona"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_data_service_lambda.arn}/invocations"
}