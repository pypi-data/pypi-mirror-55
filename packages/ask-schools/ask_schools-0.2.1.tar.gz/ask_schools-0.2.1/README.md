# Flake8 Markdown

[
![PyPI](https://img.shields.io/pypi/v/ask_schools.svg)
![PyPI](https://img.shields.io/pypi/pyversions/ask_schools.svg)
![PyPI](https://img.shields.io/github/license/guinslym/ask_schools.svg)
](https://pypi.org/project/ask_schools/)
[![TravisCI](https://travis-ci.org/guinslym/ask_schools.svg?branch=master)](https://travis-ci.org/guinslym/ask_schools)

Flake8 Markdown lints [GitHub-style Python code blocks](https://help.github.com/en/articles/creating-and-highlighting-code-blocks#fenced-code-blocks) in Markdown files using [`flake8`](https://flake8.readthedocs.io/en/stable/).

This package helps improve a Python project's documentation by ensuring that code samples are error-free.

## Features

- Lints code blocks containing regular Python and Python interpreter code ([`pycon`](http://pygments.org/docs/lexers/#pygments.lexers.python.PythonConsoleLexer))
- [pre-commit](#pre-commit-hook) hook to lint on commit

## Installation

Flake8 Markdown can be installed from PyPI using `pip` or your package manager of choice:

```
pip install ask_schools
```

## Usage

### CLI

You can use Flake8 Markdown as a CLI tool using the `ask_schools` command.

`ask_schools` accepts one or more [globs](https://docs.python.org/3.7/library/glob.html) as its arguments.

Example:

```console
$ ask_schools ask_schools "tests/samples/*.md"
tests/samples/emphasized_lines.md:6:1: F821 undefined name 'emphasized_imaginary_function'
tests/samples/basic.md:8:48: E999 SyntaxError: EOL while scanning string literal
tests/samples/basic.md:14:7: F821 undefined name 'undefined_variable'
```

### pre-commit hook

You can also add `ask_schools` to your project using [pre-commit](https://pre-commit.com/). When configured, any staged Markdown files will be linted using `ask_schools` once you run `git commit`.

To enable this hook in your local repository, add the following `repo` to your `.pre-commit-config.yaml` file:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/guinslym/ask_schools
    rev: v0.2.0
    hooks:
      - id: ask_schools
```

## Code of Conduct

Everyone interacting in the project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

## History

## [0.2.0] - 2019-06-14

### Added

- [`pycon`](http://pygments.org/docs/lexers/#pygments.lexers.python.PythonConsoleLexer) code block support

### [0.1.1] - 2019-05-19

#### Changed

- Fixed pre-commit example in README

### [0.1.0] - 2019-05-19

#### Added

- Added code for initial release
