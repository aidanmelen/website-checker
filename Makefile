NAME = $(shell awk -F "=" '/name/ {print $$2}' pyproject.toml | head -n 1 | tr -d '"' | tr -d ' ')
VERSION = $(shell poetry version -s)

all ::
	# Build release image.
	docker build . -t $(NAME)

dev ::
	# Build the dev stage.
	docker build . -t $(NAME)-dev --target dev;

	# Run the developer workspace.
	docker run -v "$$(pwd)":/app --rm -it $(NAME)-dev

pre-commit ::
	# Run pre-commit checks .i.e black and flake8.
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev run pre-commit run --all-files || git add --all

safety ::
	# Run security vulnerabilities checks for Python dependencies.
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev export --format requirements.txt --output requirements.txt
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev run safety check --full-report --file requirements.txt

pytest ::
	# Run the Python test suite.
	docker run -v "$$(pwd)":/app --rm -it --entrypoint poetry $(NAME)-dev run pytest --cov -vvv

test :: pre-commit safety pytest
	# Run all test checks.

build :: all
	# Build Docker release image and tag.
	docker tag $(NAME):latest $(NAME):latest
	docker tag $(NAME):latest $(NAME):$(VERSION)

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
