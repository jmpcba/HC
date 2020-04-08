resource "aws_rds_cluster" "dev_db" {
  cluster_identifier      = "hc-rds-dev"
  engine                  = "aurora-mysql"
  engine_version          = "5.7.mysql_aurora.2.03.2"
  engine_mode             = "serverless"
  database_name           = "hc_rds_db"
  master_username         = "hc_admin"
  master_password         = var.db_password
}