resource "aws_rds_cluster" "dev_db" {
  cluster_identifier      = "hc-rds-dev"
  engine                  = "aurora-mysql"
  engine_mode             = "serverless"
  database_name           = "hc_rds_db"
  master_username         = "hc_admin"
  master_password         = var.db_password

  scaling_configuration {
    auto_pause               = true
    max_capacity             = 1
    min_capacity             = 1
    seconds_until_auto_pause = 300
    timeout_action           = "ForceApplyCapacityChange"
  }
}