resource "aws_lambda_function" "HC_data_service_lambda" {
  function_name = "HC_data_service"
  s3_bucket     = "jmpcba-lambda"
  s3_key        = "function.zip"
  role          = "${aws_iam_role.HC_data_service_lambda_role.arn}"
  runtime       = "python3.6"
  handler       = "main.handler"
  environment {
        variables = {
            "db_password" = "${var.db_password}"
            }
        }

}

# IAM
resource "aws_iam_role" "HC_data_service_lambda_role" {
    name        = "lambda-vpc-role"
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