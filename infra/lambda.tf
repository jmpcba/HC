resource "aws_lambda_permission" "HC_lambda_permission" {
  statement_id  = "Allow_prestador_service_APIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.HC_backend_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${module.api.execution_arn}/*/*/*"
}

resource "aws_lambda_function" "HC_backend_lambda" {
  function_name = "HC_backend_service"
  s3_bucket     = "jmpcba-lambda"
  s3_key        = "function.zip"
  role          = aws_iam_role.HC_lambda_role.arn
  runtime       = "python3.6"
  handler       = "main.handler"
  environment {
    variables = {
       "db_password" = var.db_password
    }
  }
}

# IAM
resource "aws_iam_role" "HC_lambda_role" {
    name        = "HC-lambda-vpc-role"
    description = "Allows Lambda functions to call AWS services on your behalf."

    tags = {
          "name" = "lambda-vpc-role"
        }

    assume_role_policy = <<POLICY
        {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
            }
        ]
        }
        POLICY
    }
