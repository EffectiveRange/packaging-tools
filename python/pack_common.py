# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import re
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from os.path import exists
from subprocess import PIPE, Popen
from typing import Generator, Union


def check_workspace(workspace_dir: str) -> None:
    if not exists(workspace_dir):
        print(f'Workspace directory {workspace_dir} does not exist', file=sys.stderr)
        exit(1)

    if not exists(f'{workspace_dir}/setup.py'):
        print(f'There is no setup.py in the workspace directory {workspace_dir}', file=sys.stderr)
        exit(2)


def run_command(workspace_dir: str, command: Union[str, list[str]], matcher: str,
                first_match_only: bool = True) -> Generator[str, None, None]:
    command_line = command if isinstance(command, str) else ' '.join(command)

    print(f"Running command '{command_line}' with output matcher {matcher}", file=sys.stderr)

    with Popen(command_line, cwd=workspace_dir, shell=True, text=True, stdout=PIPE, stderr=PIPE) as process:
        pattern = re.compile(matcher)
        output: list[str] = []

        with ThreadPoolExecutor(2) as pool:
            exhaust = partial(pool.submit, partial(deque, maxlen=0))
            if process.stdout:
                exhaust(filter(line, pattern, output) for line in process.stdout)
            if process.stderr:
                exhaust(print(line[:-1], file=sys.stderr) for line in process.stderr)

        return_code = process.poll()

        if return_code:
            print(f"Command '{command_line}' failed with return code {return_code}", file=sys.stderr)
            exit(return_code)

        for line in output:
            yield line
            if first_match_only:
                break


def filter(line: str, pattern: re.Pattern[str], output: list[str]) -> str:
    print(line[:-1], file=sys.stderr)

    if match := pattern.match(line):
        output.append(match.group(1))

    return line


def get_absolute_path(path: str, base_path: str) -> str:
    if path.startswith('/'):
        return path
    else:
        return f'{base_path}/{path}'
