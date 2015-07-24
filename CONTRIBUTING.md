# For Contributors
## Setup
### Requirements

* Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html
* Graphviz: http://www.graphviz.org/Download.php

### Installation
Create a virtualenv:

```
$ make env
```

## Development
### Testing
Manually run the tests:

```
$ make test
```

### Documentation
Build the documentation:

```
$ make doc
```

### Static Analysis
Run linters and static analyzers:

```
$ make flake8
$ make pep257
```

## Release
Release to PyPI:

```
$ make upload-test  # dry run upload to a test server
$ make upload
```
