resource "aws_ecs_cluster" "mutant_cluster" {
  name = "mutant-cluster"
}

resource "aws_ecs_task_definition" "task_definition" {
  family                   = "mutant-task-definition"
  container_definitions    = <<DEFINITION
  [
    {
      "name": "mutant-task",
      "image": "${var.mutant_repo_url}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ],
      "memory": 1024,
      "cpu": 512,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "/ecs/mutant-task",
            "awslogs-create-group": "true",
            "awslogs-region": "us-east-2",
            "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 1024
  cpu                      = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }
}


resource "aws_ecs_service" "mutant_service" {
  name            = "mutant-service"
  cluster         = aws_ecs_cluster.mutant_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  load_balancer {
    target_group_arn = var.alb_tg_arn
    container_name   = "mutant-task"
    container_port   = 8000
  }

  network_configuration {
    subnets          = var.subnet_ids
    assign_public_ip = true
    security_groups  = [var.service_security_group_id]
  }
}