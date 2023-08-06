# Ask Schools

[
![PyPI](https://img.shields.io/pypi/v/ask_schools.svg)
![PyPI](https://img.shields.io/pypi/pyversions/ask_schools.svg)
![PyPI](https://img.shields.io/github/license/guinslym/ask_schools.svg)
](https://pypi.org/project/ask_schools/)
[![TravisCI](https://travis-ci.org/guinslym/ask_schools.svg?branch=master)](https://travis-ci.org/guinslym/ask_schools)


This package helps convert Ask School suffixes to the school full name.


## Installation

**Ask Schools** can be installed from PyPI using `pip` or your package manager of choice:

```
pip install ask_schools
```

## Usage


Example:

```python

from ask_schools import find_school_by_operator_suffix

def check_school_name_equal_toronto():
  result = find_school_by_operator_suffix('_tor')
  assert result == 'Tordonto'
```

## Code of Conduct

Everyone interacting in the project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).
