terraform {
    backend "s3" {
        bucket = "jmpcba-remote"
        key = "estados/HC_backend.tfstate"
        region = "us-east-1"
    }
}