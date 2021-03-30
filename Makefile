GIT_COMMIT?=$(shell git rev-parse HEAD)
BRANCH_NAME?=$(shell git rev-parse --abbrev-ref HEAD)
BRANCH_TAG=$(subst /,_,$(BRANCH_NAME))

DOCKER_REPO=cloud_hosted_docker_repository.example.com
DOCKER_NAME=protectyourfriend_service

DOCKER_IMAGE=${DOCKER_NAME}:${GIT_COMMIT}
DOCKER_BRANCH_IMAGE=${DOCKER_NAME}:${BRANCH_NAME}-latest

# local dev debug is enabled by default. The use of make & Makefile are not
# for production.
export DEBUG_ENABLED?=1

.DEFAULT_GOAL := all
.PHONY: all install clean run test docker_build docker_test up down ps docs lint fixtures

export DB_HOST?=127.0.0.1
export DB_NAME=service
export DB_USER=service
export DB_PASS=service
export DB_PORT?=5432
export POSTGRES_HOST?=127.0.0.1
export POSTGRES_NAME=service
export POSTGRES_USER=service
export POSTGRES_PASS=service
export POSTGRES_PORT?=5432

all:
	echo "Please choose a make target to run."

install:
	pip install -r requirements-test.txt

clean:
	rm -rf dist/ build/
	rm -f README.pdf
	find . -iname '*.pyc' -exec rm {} \; -print

docker_build: clean
	docker build \
		-t ${DOCKER_IMAGE} \
		-t ${DOCKER_BRANCH_IMAGE} \
		-t ${DOCKER_REPO}/${DOCKER_IMAGE} \
		-t ${DOCKER_REPO}/${DOCKER_BRANCH_IMAGE} \
		--target prod .
	docker build \
		-t ${DOCKER_IMAGE}-test \
		-t ${DOCKER_BRANCH_IMAGE}-test \
		-t ${DOCKER_REPO}/${DOCKER_IMAGE}-test \
		-t ${DOCKER_REPO}/${DOCKER_BRANCH_IMAGE}-test \
		--target test .

README.pdf: *.rst
	rst2pdf README.rst

docs: README.pdf

collect:
	python manage.py collectstatic --noinput

run: collect
	python manage.py runserver

migrate:
	python manage.py migrate

up:
	docker-compose --project-name ${DOCKER_NAME} up --remove-orphans

ps:
	docker-compose --project-name ${DOCKER_NAME} ps

down:
	docker-compose --project-name ${DOCKER_NAME} logs -t
	docker-compose --project-name ${DOCKER_NAME} down --remove-orphans

docker_test:
	docker run \
		--rm \
		--network=${DOCKER_NAME}_default \
		-e DB_HOST=postgres \
		-e DB_USER=${DB_USER} \
		-e DB_NAME=${DB_NAME} \
		-e DB_PASS=${DB_PASS} \
		-e DB_PORT=${DB_PORT} \
		${DOCKER_IMAGE}-test \
		bash -c "make test"

docker_release:
	docker push ${DOCKER_REPO}/${DOCKER_IMAGE}
	docker push ${DOCKER_REPO}/${DOCKER_BRANCH_IMAGE}

lint:
	flake8 --ignore=E501 webapp api

fixtures: migrate
	python manage.py fixtures

superuser:
	python manage.py createsuperuser

test: lint
	pytest -s --ds=webapp.settings --cov=api --cov=webapp
