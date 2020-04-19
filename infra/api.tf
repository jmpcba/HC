locals {
    api_name = "HOMECARE_BACKEND_API"
    api_description = "backend de HomeCare"
    resources = ["ESPECIALIDAD", "FERIADO", "LIQUIDACION", "MODULO", "PACIENTE", "PRACTICA", "PRESTADOR", "SUBMODULO", "USUARIO", "ZONA", "ADMIN"]
}

module "api" {
    source = "github.com/jmpcba/modulos_tf.git//api?ref=single_module"
    lambda_uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.HC_backend_lambda.arn}/invocations"
    api_name = local.api_name
    api_description = local.api_description
    resource_list = local.resources
}