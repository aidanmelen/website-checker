[![Tests](https://github.com/aidanmelen/website-checker/workflows/Tests/badge.svg)](https://github.com/aidanmelen/website-checker/actions?workflow=Tests)
[![PyPI](https://img.shields.io/pypi/v/website-checker.svg)](https://pypi.org/project/website-checker/)
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

# License

Check out the [LICENSE](./LICENSE) for more information.

# Credits

Check out the [CREDITS](./docs/CREDITS.md) for more information.
