### Development

This project contains an integrated containerized development environment baked into the [Dockerfile](./Dockerfile) build stages.

#### 1. Create workspace

```bash
$ make workspace
docker build . -t website-checker-workspace --target workspace
[+] Building 142.6s (22/22) FINISHED
...
```

Yikes! It takes **142.6s** to build the workspace? Don't worry, that is only the first run, now it is cached.

#### 2. Get development workspace

```bash
$ make dev
docker build . -t website-checker-workspace --target workspace
[+] Building 1.0s (15/15) FINISHED
docker run -v "$(pwd)":/app --rm -it website-checker-workspace
➜  /app git:(master) ✗
```

Nice! Docker cached and reused the layers and the build finished in **1.0s** before getting a `zsh` in the workspace container.

#### 3. Lint and test changes

We can run our checks in the developer workspace

```bash
$ make dev
...
docker run -v "$(pwd)":/app --rm -it website-checker-workspace
➜  /app git:(main) ✗ pytest --cov
============================= test session starts ==============================
platform linux -- Python 3.8.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /app
plugins: cov-2.10.1, mock-3.3.1
collected 21 items

tests/checks/check_health_test.py ..                                     [  9%]
tests/checks/check_latency_test.py ..                                    [ 19%]
tests/checks/check_network_test.py ...                                   [ 33%]
tests/cli/cli_health_test.py ....                                        [ 52%]
tests/cli/cli_latency_test.py ....                                       [ 71%]
tests/cli/cli_main_test.py ..                                            [ 80%]
tests/cli/cli_network_test.py ....                                       [100%]

----------- coverage: platform linux, python 3.8.5-final-0 -----------
Name                              Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------
src/website_checker/__init__.py       0      0      0      0   100%
src/website_checker/checks.py        13      0      0      0   100%
src/website_checker/cli.py           40      0      6      0   100%
src/website_checker/helpers.py       14      0      0      0   100%
-----------------------------------------------------------------------------
TOTAL                                67      0      6      0   100%

Required test coverage of 80.0% reached. Total coverage: 100.00%

============================== 21 passed in 0.63s ==============================
```

Or we run tests from our host machine

```bash
$ make test
docker run -v "$(pwd)":/app --rm -it website-checker-workspace pre-commit run -a
Black....................................................................Passed
Flake8...................................................................Passed
Reorder python imports...................................................Passed
Check Toml...............................................................Passed
Check Yaml...............................................................Passed
Fix End of Files.........................................................Passed
Trim Trailing Whitespace.................................................Passed
Check for added large files..............................................Passed
docker run -v "$(pwd)":/app --rm -it website-checker-workspace pytest --cov
============================= test session starts ==============================
platform linux -- Python 3.8.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /app
plugins: cov-2.10.1, mock-3.3.1
collected 21 items

tests/checks/check_health_test.py ..                                     [  9%]
tests/checks/check_latency_test.py ..                                    [ 19%]
tests/checks/check_network_test.py ...                                   [ 33%]
tests/cli/cli_health_test.py ....                                        [ 52%]
tests/cli/cli_latency_test.py ....                                       [ 71%]
tests/cli/cli_main_test.py ..                                            [ 80%]
tests/cli/cli_network_test.py ....                                       [100%]

----------- coverage: platform linux, python 3.8.5-final-0 -----------
Name                              Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------
src/website_checker/__init__.py       0      0      0      0   100%
src/website_checker/checks.py        13      0      0      0   100%
src/website_checker/cli.py           40      0      6      0   100%
src/website_checker/helpers.py       14      0      0      0   100%
-----------------------------------------------------------------------------
TOTAL                                67      0      6      0   100%

Required test coverage of 80.0% reached. Total coverage: 100.00%

============================== 21 passed in 0.67s ==============================
```

#### 4. Build local image

```bash
$ make build
docker build . -t website-checker-workspace --target workspace
[+] Building 1.1s (15/15) FINISHED
...
# build python wheel artifact
docker build . -t website-checker-build --target build --cache-from website-checker-workspace
[+] Building 6.7s (18/18) FINISHED
...
# create minimal release image with wheel from build image
docker build . -t website-checker --target release
[+] Building 0.6s (21/21) FINISHED
...
# tag the docker image
docker tag website-checker:latest website-checker:0.1.0
docker tag website-checker:latest website-checker:latest
```

#### 5. (Optional) Install pre-commit

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

#### 6. Release

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
