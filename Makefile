NAME = $(shell awk -F "=" '/name/ {print $$2}' pyproject.toml | head -n 1 | tr -d '"' | tr -d ' ')
VERSION = $(shell poetry version -s)

all ::
	# Build release image.
	docker build . -t $(NAME)

build-stages ::
	# Build image for each docker stage.
	for STAGE in base dev build release ; \
		do docker build . -t $(NAME)-$$STAGE --target $$STAGE; \
	done

dev ::
	# Run the development workspace.
	docker run -v "$$(pwd)":/app --rm -it $(NAME)-dev

pre-commit ::
	# Run pre-commit checks .i.e black and flake8.
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev run pre-commit run --all-files || true
	git add --all

safety ::
	# Check Python dependencies for known security vulnerabilities.
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev export --format requirements.txt --output requirements.txt
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev run safety check --full-report --file requirements.txt

pytest ::
	# Run the Python test suite.
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev run pytest --cov -vvv

test :: pre-commit safety pytest
	# Run all test checks.

poetry-build ::
	# Build Python wheel distrubtion
	docker build . -t $(NAME)-build --target build
	docker run -v "$$(pwd)":/app --rm -it $(NAME)-build

docker-build ::
	# Build Docker release image and tag.
	docker build . -t $(NAME) --target release
	docker tag $(NAME):latest $(NAME):latest
	docker tag $(NAME):latest $(NAME):$(VERSION)

build :: poetry-build docker-build
	# Build both Python wheel and Docker release image

run :: all
	# Run end-to-end checks.
	docker run --rm --env-file env.example $(NAME) network
	docker run --rm --env-file env.example $(NAME) health
	docker run --rm --env-file env.example $(NAME) latency

release :: all
	# Push tags and trigger Github Actions release.
	git tag $(VERSION)
	git push --tags

clean ::
	# Remove Python cache files.
	@rm -rf build dist .eggs *.egg-info .venv requirements.txt
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
