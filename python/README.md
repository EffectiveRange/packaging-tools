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

> [!CAUTION]
> python3-stdeb 0.10.0 package contains a bug that prevents `dh-virtualenv` packaging from working properly.
> The bug is not present in the PyPI version of stdeb, therefore it is recommended to install stdeb using pip.

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

- `pack_wheel` - Create binary wheel package
- `pack_fpm-deb` - Create debian .deb package using [FPM](https://fpm.readthedocs.io/en/latest/index.html)
- `pack_dh-virtualenv` - Create debian .deb package using [dh-virtualenv](https://pack_dh-virtualenv.readthedocs.io/en/latest/) and [stdeb](https://github.com/astraw/stdeb)

### wheel

The `pack_wheel` script is using the `bdist_wheel` setuptools command to create a binary wheel package.

```bash
$ pack_wheel --help
usage: pack_wheel [-h] [-p PYTHON_BIN] [-o OUTPUT_DIR] workspace_dir

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

The `pack_fpm-deb` script is using the `fpm` to create a debian .deb package.

```bash
$ pack_fpm-deb --help
usage: pack_fpm-deb [-h] [-a ARGUMENTS] [-p PYTHON_BIN] [-o OUTPUT_DIR] workspace_dir

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

The `pack_dh-virtualenv` script is using `stdeb` and `dh-virtualenv` to create a debian .deb package
with all Python dependecies pre-installed in a virtual environment.

```bash
$ pack_dh-virtualenv --help
usage: pack_dh-virtualenv [-h] [-a ARGUMENTS] [-p PYTHON_BIN] [-A ARCHITECTURE] [-s SERVICE_FILE] [-e EXTRA_FILES] [-o OUTPUT_DIR] workspace_dir

positional arguments:
  workspace_dir         workspace directory where setup.py is located

options:
  -h, --help            show this help message and exit
  -a ARGUMENTS, --arguments ARGUMENTS
                        extra arguments passed to stdeb (default: None)
  -p PYTHON_BIN, --python-bin PYTHON_BIN
                        python executable to use (default: python3)
  -A ARCHITECTURE, --architecture ARCHITECTURE
                        control file architecture (default: any)
  -s SERVICE_FILE, --service-file SERVICE_FILE
                        service unit file path (default: None)
  -e EXTRA_FILES, --extra-files EXTRA_FILES
                        add extra files into debian folder before build (default: None)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        package output directory (default: None)
```
