import importlib.util
import os
import shutil
import subprocess
import sys
from io import StringIO
from os.path import dirname, abspath
from pathlib import Path
from typing import Union
from unittest.mock import patch

sys.path.insert(0, dirname(abspath(__file__) + "/.."))

TEST_RESOURCE_ROOT = str(Path(os.path.dirname(__file__)).absolute())
TEST_FILE_SYSTEM_ROOT = str(Path(TEST_RESOURCE_ROOT).joinpath("test_root").absolute())
TEST_PROJECT_ROOT = str(Path(TEST_FILE_SYSTEM_ROOT).joinpath("etc").joinpath("test-project").absolute())
RESOURCE_ROOT = str(Path(TEST_RESOURCE_ROOT).parent.absolute())


def delete_directory(directory: str) -> None:
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def create_directory(directory: str) -> None:
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)


def delete_file(file: str) -> None:
    if os.path.isfile(file):
        os.remove(file)


def create_file(file: str, content: str) -> None:
    create_directory(os.path.dirname(file))
    with open(file, "w") as f:
        f.write(content)


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    script_path = command[0]
    script_module_name = os.path.splitext(os.path.basename(script_path))[0]
    spec = importlib.util.spec_from_file_location(script_module_name, script_path)
    script_module = importlib.util.module_from_spec(spec)
    sys.modules[script_module_name] = script_module
    spec.loader.exec_module(script_module)

    with patch.object(sys, 'argv', command):
        with patch('sys.stdout', new=StringIO()) as fake_out, patch('sys.stderr', new=StringIO()) as fake_err:
            try:
                script_module.main()
                return_code = 0
            except SystemExit as error:
                return_code = error.code
            stdout = fake_out.getvalue()
            stderr = fake_err.getvalue()

    result = subprocess.CompletedProcess(args=command, returncode=return_code, stdout=stdout, stderr=stderr)

    print("Return code:", result.returncode)
    if result.stdout:
        print("Output:", result.stdout.rstrip("\n"))
    if result.stderr:
        print("Log:", result.stderr.rstrip("\n"))
    print()

    return result


def check_files_exist(file_paths: str) -> bool:
    all_exists = True

    for file_path in file_paths.splitlines():
        if not os.path.exists(file_path):
            all_exists = False
            print(f"{file_path} does not exist")

    return all_exists


def check_file_is_in_deb(deb_file_path: str, file_paths: Union[str, list[str]]) -> bool:
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    return all(file_path in subprocess.run(["dpkg", "-c", deb_file_path], text=True, stdout=subprocess.PIPE).stdout for
               file_path in file_paths)


def check_files_matches_in_deb(deb_file_path: str, files_and_matchers: list[tuple[str, str]]) -> bool:
    temp_dir = f"{TEST_FILE_SYSTEM_ROOT}/tmp"

    delete_directory(temp_dir)
    os.makedirs(temp_dir)

    subprocess.run(["dpkg-deb", "-e", deb_file_path, temp_dir], check=True)

    all_matches = True

    for file_name, matcher in files_and_matchers:
        file_path = os.path.join(temp_dir, file_name)
        with open(os.path.join(temp_dir, file_path), "r") as file:
            content = file.read()
            matches = matcher in content
            all_matches = all_matches and matches

    return all_matches
