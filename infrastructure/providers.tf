provider "aws" {
  region = "us-east-2"
  default_tags {
    tags = {
      project   = "mutant"
      comments  = "this resource is managed by terraform"
      terraform = "true"
    }
  }
}

provider "docker" {
  registry_auth {
    address  = data.aws_ecr_authorization_token.token.proxy_endpoint
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}

data "aws_ecr_authorization_token" "token" {}