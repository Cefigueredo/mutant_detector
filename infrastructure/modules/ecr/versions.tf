terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4.1"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.22.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}
