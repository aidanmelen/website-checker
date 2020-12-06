[![Tests](https://github.com/aidanmelen/website-checker/workflows/Tests/badge.svg)](https://github.com/aidanmelen/website-checker/actions?workflow=Tests)
[![Release](https://github.com/aidanmelen/website-checker/workflows/Release/badge.svg)](https://github.com/aidanmelen/website-checker/actions?workflow=Release)
[![PyPI](https://img.shields.io/pypi/v/website_checker.svg)](https://pypi.org/project/website-checker/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# website_checker

A simple python application for running checks against websites.

## Usage

### Install

```bash
$ pipx install website-checker
  installed package site-check 0.1.0, Python 3.9.0
  These apps are now globally available
    - check
done! ✨ 🌟 ✨

# or install into system python with pip
# pip install website-checker
```

### Example

Display help message

```text
$ check --help
Usage: check [OPTIONS] COMMAND [ARGS]...

  A simple python application for running checks against websites.

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

$ check health -u https://google.com
{"event": {"check": "health", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:27:49.413241"}

$ check latency -u https://google.com
{"event": {"check": "latency", "input": {"threshold": 500, "timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:28:14.460530"}
```

### Docker

```bash
$ docker run --rm -it aidanmelen/website-checker health --url https://google.com
{"event": {"check": "health", "input": {"timeout": 5, "url": "https://google.com"}, "output": "pass"}, "logger": "website-checker", "timestamp": "2020-11-30T05:00:23.444290"}
```

# License

Check out the [LICENSE](./LICENSE) for more information.

# Credits

Check out the [CREDITS](./docs/CREDITS.md) for more information.
