# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import re
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from fileinput import FileInput
from functools import partial
from os.path import exists
from subprocess import PIPE, Popen
from typing import Generator, Union


def check_workspace(workspace_dir: str) -> None:
    if not exists(workspace_dir):
        print(f"Workspace directory {workspace_dir} does not exist", file=sys.stderr)
        exit(1)

    if not exists(f"{workspace_dir}/setup.py"):
        print(f"There is no setup.py in the workspace directory {workspace_dir}", file=sys.stderr)
        exit(2)


def get_build_architecture() -> str:
    with Popen("dpkg --print-architecture", shell=True, text=True, stdout=PIPE, stderr=PIPE) as process:
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Failed to get build architecture: {stderr.strip()}", file=sys.stderr)
            exit(process.returncode)

        return stdout.strip()


def is_cross_build(target_architecture: str | None) -> bool:
    build_architecture = get_build_architecture()
    target_architecture = target_architecture or build_architecture
    return target_architecture != build_architecture


def rsync(source: str, destination: str, exclude: list[str] | None = None) -> None:
    command = ["rsync", "-av", "--mkpath"]

    if exclude is not None:
        for pattern in exclude:
            command.append(f"--exclude={pattern}")

    command.extend([source, destination])

    command_line = " ".join(command)

    with Popen(command_line, shell=True, text=True, stdout=PIPE, stderr=PIPE) as process:
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Failed to run rsync: {stderr.strip()}", file=sys.stderr)
            exit(process.returncode)


def rsync_to_buildroot(workspace_dir: str, exclude=None) -> None:
    rsync(f"{workspace_dir}/", f"/var/chroot/buildroot{workspace_dir}/", exclude)


def rsync_from_buildroot(workspace_dir: str, exclude=None) -> None:
    rsync(f"/var/chroot/buildroot{workspace_dir}/", f"{workspace_dir}/", exclude)


def get_buildroot_command(workspace_dir: str, args: Union[str, list[str]]) -> list[str]:
    if isinstance(args, str):
        args = args.split()

    return ["schroot", "-d", workspace_dir, "-u", "root", "-c", "buildroot", "--"] + list(args)


def run_build_command(run_in_buildroot: bool, workspace_dir: str, command: Union[str, list[str]],
                      matcher: str, first_match_only: bool = True) -> Generator[str, None, None]:
    if run_in_buildroot:
        workspace_dir = workspace_dir.replace("/var/chroot/buildroot", "")
        command = get_buildroot_command(workspace_dir, command)

    return run_command(workspace_dir, command, matcher, first_match_only)


def run_command(workspace_dir: str, command: Union[str, list[str]], matcher: str,
                first_match_only: bool = True) -> Generator[str, None, None]:
    command_line = command if isinstance(command, str) else " ".join(command)

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
    if path.startswith("/"):
        return path
    else:
        return f"{base_path}/{path}"


def replace_in_file(file_path: str, pattern: str, replacement: str) -> None:
    if not exists(file_path):
        return

    with open(file_path, "r") as file:
        original_content = file.read()

    replaced_content = re.sub(pattern, replacement, original_content, flags=re.MULTILINE)

    with open(file_path, "w") as file:
        file.write(replaced_content)


def extract_package_name(workspace_dir: str) -> str:
    with open(f"{workspace_dir}/setup.py", "r") as file:
        setup_code = file.read()

    pattern = r"name\s*=\s*['\"]([^'\"]+)['\"]"

    match = re.search(pattern, setup_code)

    if match:
        return match.group(1)
    else:
        return workspace_dir.split("/")[-1]


def extract_version(workspace_dir: str) -> str:
    with open(f"{workspace_dir}/setup.py", "r") as file:
        setup_code = file.read()

    pattern = r"version\s*=\s*['\"]([^'\"]+)['\"]"

    match = re.search(pattern, setup_code)

    if match:
        return match.group(1)
    else:
        return "0.0.0"


def override_architecture(architecture: str, debian_dir: str) -> None:
    with FileInput(f"{debian_dir}/control", inplace=True) as file:
        for line in file:
            if "Architecture:" in line:
                line = f"Architecture: {architecture}\n"
            print(line, end="")
