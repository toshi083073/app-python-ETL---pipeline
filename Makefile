# Makefile - Docker操作の簡略化

build:
	docker-compose build

up-jupyter:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up python

up-streamlit:
	docker-compose -f docker-compose.yml -f docker-compose.streamlit.yml up python

copy-batch:
	docker-compose run --rm --entrypoint "" -e PYTHONPATH=/app python python scripts/etl_copy.py

copy-batch-redshift:
	docker-compose run --rm --entrypoint "" -e PYTHONPATH=/app python python scripts/etl_copy_redshift.py

up-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

down:
	docker-compose down

clean:
	docker-compose down -v --rmi all --remove-orphans

# === Fargate用のDockerビルド ===
build-fargate:
	docker build -f Dockerfile.fargate -t redshift-etl:latest .

push-ecr:
	docker tag redshift-etl:latest 802190220015.dkr.ecr.ap-northeast-1.amazonaws.com/redshift-etl:latest
	docker push 802190220015.dkr.ecr.ap-northeast-1.amazonaws.com/redshift-etl:latest

run-fargate:
	source .env.fargate && \
	aws ecs run-task \
	--cluster $$ECS_CLUSTER \
	--launch-type FARGATE \
	--network-configuration "awsvpcConfiguration={subnets=[$$SUBNET_ID],securityGroups=[$$SG_ID],assignPublicIp=ENABLED}" \
	--task-definition $$TASK_DEFINITION
