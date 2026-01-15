#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
from os.path import abspath, dirname

sys.path.insert(0, dirname(abspath(__file__)))

from pack_common import check_workspace, run_command, get_project_type, ProjectType


def main() -> None:
    arguments = _get_arguments()

    workspace_dir = abspath(arguments.workspace_dir)

    check_workspace(workspace_dir)

    project_type = get_project_type(workspace_dir)

    if project_type == ProjectType.PYPROJECT_TOML:
        command = [arguments.python_bin, "-m", "build", "--wheel"]
        matcher = r"Successfully built (.+\.whl)"
    else:
        command = [arguments.python_bin, "setup.py", "bdist_wheel"]
        matcher = r".*'(.+\.whl)'"

    output_dir = f"{workspace_dir}/dist"

    if arguments.output_dir:
        output_dir = abspath(arguments.output_dir)
        if project_type == ProjectType.PYPROJECT_TOML:
            command.extend(["--outdir", output_dir])
        else:
            command.extend(["--dist-dir", output_dir])

    result = next(run_command(workspace_dir, command, matcher))

    if project_type == ProjectType.PYPROJECT_TOML:
        result = f"{output_dir}/{result}" if arguments.output_dir else f"{output_dir}/{result}"
    else:
        if not result.startswith("/"):
            result = f"{output_dir}/{result}" if arguments.output_dir else f"{workspace_dir}/{result}"
    print(result)


def _get_arguments() -> Namespace:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--python-bin", help="python executable to use", default="python3")
    parser.add_argument("-o", "--output-dir", help="package output directory")
    parser.add_argument("workspace_dir", help="workspace directory where setup.py is located")
    return parser.parse_known_args()[0]


if __name__ == "__main__":
    main()
