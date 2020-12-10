### Development

This project contains an integrated containerized development environment baked into the [Dockerfile](./Dockerfile) build stages.

#### 1. Develop

The local developer environment has a single dependency: docker. The Dockerfile declares a multi-stage build process: base, dev, build, release.

```bash
$ make dev
# Build the dev stage.
docker build . -t website-checker-dev --target dev;
[+] Building 70.9s (12/12) FINISHED
# Run the developer workspace.
docker run -v "$(pwd)":/app --rm -it website-checker-dev
root@c15c547fbf8d:/app# 
```

Now we have a shell for a Docker container with all of our build dependencies and source code.
But, yikes! It takes **70.9s** to build? Don't worry, that is only for the first run, now Docker has cached the layers.

Exist the container and try getting another developer environment.

```bash
# Build the dev stage.
docker build . -t website-checker-dev --target dev;
[+] Building 1.1s (12/12) FINISHED 
# Run the developer workspace.
docker run -v "$(pwd)":/app --rm -it website-checker-dev
root@4ce1eab082a8:/app# 
```

Okay, **1.1s** builds, I can live with that.

#### 2. Test

We like to test that our project is linted, scanned for security vulnerabilities, and our unittests pass with good coverage.

```bash
$ make dev
...
docker run -v "$(pwd)":/app --rm -it website-checker-dev
root@4ce1eab082a8:/app# pre-commit run run --all-files || git add --all
...
root@4ce1eab082a8:/app# poetry export --format requirements.txt --output requirements.txt
root@4ce1eab082a8:/app# safety check --full-report --file requirements.txt
...
root@4ce1eab082a8:/app# pytest --cov
...
```

Or we can run tests from our host machine

```bash
$ make test
# Run pre-commit checks .i.e black and flake8.
docker run -v "$(pwd)":/app --rm -it --entrypoint poetry website-checker-dev run pre-commit run --all-files || git add --all
...
# Run security vulnerabilities checks for Python dependencies.
docker run -v "$(pwd)":/app --rm -it --entrypoint poetry website-checker-dev export --format requirements.txt --output requirements.txt
docker run -v "$(pwd)":/app --rm -it --entrypoint poetry website-checker-dev run safety check --full-report --file requirements.txt
...
# Run the Python test suite.
docker run -v "$(pwd)":/app --rm -it --entrypoint poetry website-checker-dev run pytest --cov -vvv
```

#### 3. Build local image

In some cases, it can be nice to be able to build a local release image.

```bash
$ make build
# Build release image.
docker build . -t website-checker
...
# Build Docker release image and tag.
docker tag website-checker:latest website-checker:latest
docker tag website-checker:latest website-checker:0.3.3
```

#### 4. (Optional) Install pre-commit

`pre-commit` checks run inside our workspace container by when run with `make test`; however, since all the pre-commit dependencies are manage by Poetry, we can install `pre-commit` on our host machine. For example

```bash
$ poetry install
...

$ pre-commit install
pre-commit installed at .git/hooks/pre-commit

# manually verify with
$ pre-commit run -a
...
```

#### 5. Release

Both PYPI and Dockerhub releases are handled by the [Release Github Action](./.github/worksflows/release.yml). Ensure you bump the Poetry project version accordingly before releasing your changes. e.g. this is how you would do a minor release:

```bash
$ poetry version minor
Bumping version from 0.1.1-alpha.2 to 0.2.0
```

Then push up your code and tag the branch. The Github Actions will trigger on the creation of a new tag.

```bash
$ make release
git tag 0.2.0
git push --tags
...
```
