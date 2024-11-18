terraform {
  backend "s3" {
    bucket = "awseks-vasu" # S3 bucket name
    key    = "EKS/terraform.tfstate"
    region = "ap-south-1"
  }
}
