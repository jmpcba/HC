output "dev_url" {
  value = module.api.dev_url
}

output "prod_url" {
  value = module.api.prod_url
}

output "rds_dev_endpoint" {
    value = aws_rds_cluster.dev_db.endpoint
}