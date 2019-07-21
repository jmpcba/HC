terraform {
    backend "s3" {
        bucket = "jmpcba-remote"
        key = "estados/HC_databroker.tfstate"
        region = "us-east-1"
    }
}