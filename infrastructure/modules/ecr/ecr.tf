data "aws_ecr_authorization_token" "token" {}

resource "aws_ecr_repository" "app_repository" {
  name                 = "mutant-repo"
  force_delete         = true
  image_tag_mutability = "MUTABLE"
}

resource "terraform_data" "build_app_image" {
  triggers_replace = [
    sha1(join("", [for f in fileset(path.root, "../app/**") : filesha1(f)])),
    md5(file("${path.root}/../app/Dockerfile")),
  ]

  provisioner "local-exec" {
    command = <<-EOT
      docker login ${data.aws_ecr_authorization_token.token.proxy_endpoint} -u AWS -p ${data.aws_ecr_authorization_token.token.password}
      EOT
  }

  provisioner "local-exec" {
    command = <<-EOT
      docker buildx build --platform linux/arm64 --output type=docker \
      --cache-from type=gha --cache-to type=gha,mode=max \
      -t ${aws_ecr_repository.app_repository.repository_url}:latest \
      -f ${path.root}/../app/Dockerfile ${path.root}/../app/
    EOT
  }

  depends_on = [
    aws_ecr_repository.app_repository
  ]
}

resource "docker_registry_image" "app_image" {
  name          = "${aws_ecr_repository.app_repository.repository_url}:latest"
  keep_remotely = true

  triggers = {
    app_files  = sha1(join("", [for f in fileset(path.root, "../app/**") : filesha1(f)])),
    dockerfile = md5(file("${path.root}/../app/Dockerfile")),
  }
  depends_on = [terraform_data.build_app_image]
}

