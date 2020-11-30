IMAGE_NAME = $(shell awk -F "=" '/name/ {print $$2}' pyproject.toml | head -n 1 | tr -d '"' | tr -d ' ')
VERSION = $(shell poetry version -s)

.PHONY: all
all:
	# build all stages: base, workspace, build, release
	docker build . -t $(IMAGE_NAME)

.PHONY: dev
dev: workspace
	docker run -v "$$(pwd)":/app --rm -it $(IMAGE_NAME)-workspace

.PHONY: test
test:
	# pre-commit
	docker run -v "$$(pwd)":/app --rm -it $(IMAGE_NAME)-workspace pre-commit run -a

	# test
	docker run -v "$$(pwd)":/app --rm -it $(IMAGE_NAME)-workspace pytest -vvv --cov src -vvv

.PHONY: build
build: workspace
	# build python wheel artifact
	docker build . -t $(IMAGE_NAME)-build --target build --cache-from $(IMAGE_NAME)-workspace

	# create minimal release image with wheel from build image
	docker build . -t $(IMAGE_NAME) --target release

	# tag the docker image
	docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(VERSION)
	docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):latest

.PHONY: run
run: workspace
	docker run --rm --env-file env.example $(IMAGE_NAME) network
	docker run --rm --env-file env.example $(IMAGE_NAME) health
	docker run --rm --env-file env.example $(IMAGE_NAME) latency

.PHONY: workspace
workspace:
	docker build . -t $(IMAGE_NAME)-workspace --target workspace

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
