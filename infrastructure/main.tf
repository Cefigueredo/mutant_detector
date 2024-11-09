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
    tls = {
      source  = "hashicorp/tls"
      version = "4.0.4"
    }
  }
}

module "networking" {
  source = "./modules/networking"
}

module "ecrRepo" {
  source = "./modules/ecr"
}

module "ecsCluster" {
  source = "./modules/ecs"

  mutant_repo_url           = module.ecrRepo.repository_url
  mutant_repo_arn           = module.ecrRepo.repository_arn
  alb_tg_arn                = module.networking.target_group_arn
  subnet_ids                = module.networking.subnet_ids
  service_security_group_id = module.networking.service_security_group_id
}