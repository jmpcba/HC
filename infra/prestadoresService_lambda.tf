resource "aws_lambda_permission" "HC_prestador_service_lambda_permission" {
  statement_id  = "Allow_prestador_service_APIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.HC_prestador_service_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.HC_REST_API.execution_arn}/*/*/*"
}

resource "aws_lambda_function" "HC_prestador_service_lambda" {
  function_name = "HC_prestador_service"
  s3_bucket     = "jmpcba-lambda"
  s3_key        = "function.zip"
  role          = "${aws_iam_role.HC_data_service_lambda_role.arn}"
  runtime       = "python3.6"
  handler       = "main.prestador_handler"
  environment {
        variables = {
            "db_password" = "${var.db_password}"
            }
        }

}