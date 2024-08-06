# Python packaging

Packaging scripts to create installable packages from Python projects.

## Features

- [x] Create binary wheel package
- [x] Create debian .deb package
- [x] Support for packaging virtualenv into .deb
- [x] Support for adding systemd service
- [x] Support for adding postinst, prerm etc. scripts

## Overview

The main entry point is `pack_python` script.
It is calling the packaging-specific scripts and passing arguments to them.
Also parses the configuration from the target project's `setup.cfg` file if there is any.

## Requirements

### python

```bash
$ sudo apt-get install python3 python3-pip
```

### wheel

```bash
$ pip install wheel
```

### fpm

```bash
$ sudo apt-get install ruby ruby-dev rubygems build-essential
$ sudo gem install -N fpm
```

### dh-virtualenv

```bash
$ sudo apt-get install debhelper devscripts equivs dh-virtualenv dh-python python3-virtualenv python3-all
$ pip install stdeb
```

## Configuration

The configuration is read from the `setup.cfg` file in the target project's root directory by default.

Example configuration:

```ini
[pack-python]
default = fpm-deb
packaging =
    wheel
    fpm-deb
    dh-virtualenv
fpm-deb = -a "--deb-systemd service/test-project.service --after-install scripts/test-project.postinst"
dh-virtualenv = -s service/test-project.service -e scripts/*
```

## Usage

```bash
$ ./pack_python --help
usage: pack_python [-h] [-s SCRIPTS] [-a | --all | --no-all] [-c CONFIG_FILE] [-p PYTHON_BIN] [-o OUTPUT_DIR] workspace_dir

positional arguments:
  workspace_dir         workspace directory where setup.py is located

options:
  -h, --help            show this help message and exit
  -s SCRIPTS, --scripts SCRIPTS
                        space separated packaging scripts to run (default: None)
  -a, --all, --no-all   run all configured packaging scripts (default: False)
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        config file path relative to workspace directory (default: setup.cfg)
  -p PYTHON_BIN, --python-bin PYTHON_BIN
                        python executable to use (default: python3)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        package output directory (default: None)
```

Example using the configured default packaging script:

```bash
$ ./pack_python tests/test-project
/home/attilagombos/EffectiveRange/packaging-tools/python/tests/test-project/dist/python3-test-project_1.0.0_all.deb
```

Example using all configured packaging scripts:

```bash
$ ./pack_python tests/test-project --all
/home/attilagombos/EffectiveRange/packaging-tools/python/tests/test-project/dist/test_project-1.0.0-py3-none-any.whl
/home/attilagombos/EffectiveRange/packaging-tools/python/tests/test-project/dist/python3-test-project_1.0.0_all.deb
/home/attilagombos/EffectiveRange/packaging-tools/python/tests/test-project/dist/test-project_1.0.0-1_all.deb
```

Example using specific packaging scripts:

```bash
$ ./pack_python tests/test-project --scripts "wheel fpm-deb"
/home/attilagombos/EffectiveRange/packaging-tools/python/tests/test-project/dist/test_project-1.0.0-py3-none-any.whl
/home/attilagombos/EffectiveRange/packaging-tools/python/tests/test-project/dist/python3-test-project_1.0.0_all.deb
```

## Packaging scripts

- `wheel` - Create binary wheel package
- `fpm-deb` - Create debian .deb package using [FPM](https://fpm.readthedocs.io/en/latest/index.html)
- `dh-virtualenv` - Create debian .deb package using [dh-virtualenv](https://pack_dh-virtualenv.readthedocs.io/en/latest/)
  and [stdeb](https://github.com/astraw/stdeb)

### wheel

The `wheel` script is using the `bdist_wheel` setuptools command to create a binary wheel package.

```bash
$ wheel --help
usage: wheel [-h] [-p PYTHON_BIN] [-o OUTPUT_DIR] workspace_dir

positional arguments:
  workspace_dir         workspace directory where setup.py is located

options:
  -h, --help            show this help message and exit
  -p PYTHON_BIN, --python-bin PYTHON_BIN
                        python executable to use (default: python3)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        package output directory (default: None)
```

### fpm-deb

The `fpm-deb` script is using the `fpm` to create a debian .deb package.

```bash
$ fpm-deb --help
usage: fpm-deb [-h] [-a ARGUMENTS] [-p PYTHON_BIN] [-o OUTPUT_DIR] workspace_dir

positional arguments:
  workspace_dir         workspace directory where setup.py is located

options:
  -h, --help            show this help message and exit
  -a ARGUMENTS, --arguments ARGUMENTS
                        extra arguments passed to fpm (default: None)
  -p PYTHON_BIN, --python-bin PYTHON_BIN
                        python executable to use (default: python3)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        package output directory (default: None)
```

### dh-virtualenv

The `dh-virtualenv` script is using `stdeb` and `dh-virtualenv` to create a debian .deb package
with all Python dependecies pre-installed in a virtual environment.

```bash
$ dh-virtualenv --help
usage: dh-virtualenv [-h] [-a ARGUMENTS] [-p PYTHON_BIN] [-s SERVICE_FILE] [-e EXTRA_FILES] [-o OUTPUT_DIR] workspace_dir

positional arguments:
  workspace_dir         workspace directory where setup.py is located

options:
  -h, --help            show this help message and exit
  -a ARGUMENTS, --arguments ARGUMENTS
                        extra arguments passed to stdeb (default: None)
  -p PYTHON_BIN, --python-bin PYTHON_BIN
                        python executable to use (default: python3)
  -s SERVICE_FILE, --service-file SERVICE_FILE
                        service unit file path (default: None)
  -e EXTRA_FILES, --extra-files EXTRA_FILES
                        add extra files into debian folder before build (default: None)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        package output directory (default: None)
```
