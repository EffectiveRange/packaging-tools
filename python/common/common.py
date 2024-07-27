# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import re
import subprocess
import sys
from os.path import exists
from typing import Generator


def check_workspace(workspace_dir: str) -> None:
    if not exists(workspace_dir):
        print(f'Workspace directory {workspace_dir} does not exist', file=sys.stderr)
        exit(1)

    if not exists(f'{workspace_dir}/setup.py'):
        print(f'There is no setup.py in the workspace directory {workspace_dir}', file=sys.stderr)
        exit(2)


def run_command(workspace_dir: str, command: str | list[str], matcher: str,
                first_match_only: bool = True) -> Generator[str, None, None]:
    result = subprocess.run(command, cwd=workspace_dir, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode:
        print(result.stderr, file=sys.stderr)
        exit(result.returncode)

    output = result.stdout.split('\n')
    pattern = re.compile(matcher)

    for line in output:
        if match := pattern.match(line):
            yield match.group(1)
            if first_match_only:
                break
