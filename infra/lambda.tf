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
  s3_key        = "hc_backend.zip"
  role          = aws_iam_role.HC_lambda_role.arn
  runtime       = "python3.6"
  handler       = "main.handler"
  publish       = true
  timeout       = 60
  environment {
    variables = {
      "DB_PASSWORD" = var.db_password
      "DB_USER" = var.db_user
    }
  }
  vpc_config {
    security_group_ids = [aws_security_group.RDS.id,]
    subnet_ids = [
                  "subnet-5d7fe773", 
                  "subnet-605bc53c", 
                  "subnet-8ff7dac5", 
                  "subnet-8ff7dac5", 
                  "subnet-e05ffede", 
                  "subnet-f94017f6"
                  ]
  }
}

# IAM
resource "aws_iam_role" "HC_lambda_role" {
    name        = "HC-lambda-vpc-role"
    description = "Allows Lambda functions to call AWS services on your behalf."

    tags = {
          "name" = "lambda-vpc-role"
        }

    assume_role_policy = data.aws_iam_policy_document.HC_lambda_assume_role_policy_document.json
    }

data "aws_iam_policy_document" "HC_lambda_assume_role_policy_document" {
  version = "2012-10-17"
  
  statement {
    actions = ["sts:AssumeRole",]
    principals {
      type = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

#resource "aws_iam_policy" "lambda_logging_policy" {
#  name        = "lambda_logging"
#  description = "IAM policy for logging from a lambda"
#  policy = data.aws_iam_policy_document.HC_cloudwatch_policy_doc.json
#}

# equivalent to managed policy AWSLambdaVPCAccessExecutionRole
#data "aws_iam_policy_document" "HC_cloudwatch_policy_doc" {
#  version = "2012-10-17"
#  statement {
#    actions = [
#        "logs:CreateLogGroup",
#        "logs:CreateLogStream",
#        "logs:PutLogEvents",
#        "ec2:CreateNetworkInterface",
#        "ec2:DescribeNetworkInterfaces",
#        "ec2:DeleteNetworkInterface"
#      ]
#    resources = ["*",]
#  }
#}

resource "aws_iam_role_policy_attachment" "lambda_logs_attachment" {
  role       = aws_iam_role.HC_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}
