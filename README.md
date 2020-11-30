<!-- [![Tests](https://github.com/aidanmelen/website-checker/workflows/Tests/badge.svg)](https://github.com/aidanmelen/website-checker/actions?workflow=Tests) -->
<!-- [![Codecov](https://codecov.io/gh/aidanmelen/website-checker/branch/master/graph/badge.svg)](https://codecov.io/gh/aidanmelen/website-checker) -->
<!-- [![PyPI](https://img.shields.io/pypi/v/website-checker.svg)](https://pypi.org/project/website-checker/) -->
<!-- [![Read the Docs](https://readthedocs.org/projects/website-checker/badge/)](https://website-checker.readthedocs.io/) -->
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# website_checker

A simple python application for running checks against websites.

## Usage

### Install

```bash
$ pipx install website-check
  installed package site-check 0.1.0, Python 3.9.0
  These apps are now globally available
    - check
done! ✨ 🌟 ✨

# or install into system python with pip
# pip install website-check
```

### Example

Display help message

```bash
$ check --help
Usage: check [OPTIONS] COMMAND [ARGS]...

  The main entrypoint.

Options:
  --debug / --no-debug  Toggle debug mode.
  --version             Show the version and exit.
  --help                Show this message and exit.

Commands:
  health   Check website health.
  latency  Check website latency.
  network  Check website network connectivity.
```

Some examples

```bash
$ check network -u https://google.com -u https://blarg.com
{"event": {"check": "network", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:27:23.413281"}
{"event": {"check": "network", "input": {"timeout": 5, "url": "https://blarg.com"}, "output": "fail"}, "logger": "website-checker", "timestamp": "2020-11-30T05:27:23.443994"}

$ check health --url https://google.com
{"event": {"check": "health", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:27:49.413241"}

$ check latency --url https://google.com
{"event": {"check": "latency", "input": {"threshold": 500, "timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:28:14.460530"}

# force a check failure with a latency threshold of 1ms
$ check latency -u https://google.com -T 1
{"event": {"check": "latency", "input": {"threshold": 1, "timeout": 5, "url": "https://google.com"}, "output": "fail"}, "logger": "website-checker", "timestamp": "2020-11-30T15:17:30.897261"}
```

### Docker

The default Makefile target will run **all** stages in the Dockerfile.

```bash
$ make
# build all stages: base, workspace, build, release
docker build . -t website-checker
[+] Building 0.9s (22/22) FINISHED
...

# verify image and look at the size!
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
website-checker     latest              4ea3d7e18eec        18 seconds ago      55.6MB

# run website check with container
$ docker run --rm -it website-checker \
health --url https://google.com
{"event": {"check": "health", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:00:23.444290"}
```

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

#### 2. Get development shell

```bash
$ make dev
docker build . -t website-checker-workspace --target workspace
[+] Building 1.0s (15/15) FINISHED
docker run -v "$(pwd)":/app --rm -it website-checker-workspace
➜  /app git:(master) ✗
```

Nice! Docker cached and reused the layers and the build finished in **1.0s** before getting a `zsh` in the workspace container.

#### 3. Lint and test changes

We can run our checks in the workspace

```bash
➜  /app git:(master) ✗ pytest tests
====================================================================================== test session starts ======================================================================================
platform linux -- Python 3.8.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /app
plugins: cov-2.10.1, mock-3.3.1
collected 21 items

tests/checks/check_health_test.py ..                                                                                                                                                      [  9%]
tests/checks/check_latency_test.py ..                                                                                                                                                     [ 19%]
tests/checks/check_network_test.py ...                                                                                                                                                    [ 33%]
tests/cli/cli_health_test.py ....                                                                                                                                                         [ 52%]
tests/cli/cli_latency_test.py ....                                                                                                                                                        [ 71%]
tests/cli/cli_main_test.py ..                                                                                                                                                             [ 80%]
tests/cli/cli_network_test.py ....                                                                                                                                                        [100%]

====================================================================================== 21 passed in 0.25s =======================================================================================
```

Or we run tests from our host machine

```bash
$ make test
# pre-commit
docker run -v "$(pwd)":/app --rm -it website-checker-workspace pre-commit run -a
Black....................................................................Passed
Flake8...................................................................Passed
Reorder python imports...................................................Passed
Check Toml...............................................................Passed
Check Yaml...............................................................Passed
Fix End of Files.........................................................Passed
Trim Trailing Whitespace.................................................Passed
Check for added large files..............................................Passed
# test
docker run -v "$(pwd)":/app --rm -it website-checker-workspace pytest -vvv --cov src -vvv
=================================================================== test session starts ====================================================================
platform linux -- Python 3.8.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- /root/.cache/pypoetry/virtualenvs/website-checker-9TtSrW0h-py3.8/bin/python
cachedir: .pytest_cache
rootdir: /app
plugins: cov-2.10.1, mock-3.3.1
collected 21 items

tests/checks/check_health_test.py::test_health_check_with_200_response_code PASSED                                                                   [  4%]
tests/checks/check_health_test.py::test_health_check_with_bad_response_code PASSED                                                                   [  9%]
tests/checks/check_latency_test.py::test_latency_check_happy_path PASSED                                                                             [ 14%]
tests/checks/check_latency_test.py::test_latency_check_sad_path PASSED                                                                               [ 19%]
tests/checks/check_network_test.py::test_network_check_can_connect PASSED                                                                            [ 23%]
tests/checks/check_network_test.py::test_network_check_cannot_connect PASSED                                                                         [ 28%]
tests/checks/check_network_test.py::test_network_check_raises_exception_on_sad_path PASSED                                                           [ 33%]
tests/cli/cli_health_test.py::test_health_subcommand_prints_usage PASSED                                                                             [ 38%]
tests/cli/cli_health_test.py::test_health_subcommand_invokes_health_happy_path PASSED                                                                [ 42%]
tests/cli/cli_health_test.py::test_health_subcommand_invokes_health_sad_path PASSED                                                                  [ 47%]
tests/cli/cli_health_test.py::test_health_subcommand_raises_on_exception PASSED                                                                      [ 52%]
tests/cli/cli_latency_test.py::test_latency_subcommand_prints_usage PASSED                                                                           [ 57%]
tests/cli/cli_latency_test.py::test_latency_subcommand_invokes_latency_happy_path PASSED                                                             [ 61%]
tests/cli/cli_latency_test.py::test_latency_subcommand_invokes_latency_sad_path PASSED                                                               [ 66%]
tests/cli/cli_latency_test.py::test_latency_subcommand_raises_on_exception PASSED                                                                    [ 71%]
tests/cli/cli_main_test.py::test_main_command_succeeds PASSED                                                                                        [ 76%]
tests/cli/cli_main_test.py::test_main_command_prints_usage PASSED                                                                                    [ 80%]
tests/cli/cli_network_test.py::test_network_check_prints_usage PASSED                                                                                [ 85%]
tests/cli/cli_network_test.py::test_network_check_invokes_network_happy_path PASSED                                                                  [ 90%]
tests/cli/cli_network_test.py::test_network_check_invokes_network_sad_path PASSED                                                                    [ 95%]
tests/cli/cli_network_test.py::test_network_check_raises_on_exception PASSED                                                                         [100%]

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

==================================================================== 21 passed in 1.50s ====================================================================
```

#### 4. Build release image

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

# Credits

Check out the [CREDITS.md](./docs/CREDITS.md) for more information.
