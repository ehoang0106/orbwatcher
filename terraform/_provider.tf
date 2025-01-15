terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  backend "s3" {
    bucket = "terraform-state-khoahoang"
    region = "us-east-1"
    key    = "terraform_state_orbwatcher"
  }
}

provider "aws" {
  region = "us-west-1"
}