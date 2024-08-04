import os
import shutil
import subprocess
from pathlib import Path

TEST_RESOURCE_ROOT = str(Path(os.path.dirname(__file__)).absolute())
TEST_FILE_SYSTEM_ROOT = str(Path(TEST_RESOURCE_ROOT).joinpath('test_root').absolute())
TEST_PROJECT_ROOT = str(Path(TEST_FILE_SYSTEM_ROOT).joinpath('etc').joinpath('test-project').absolute())
RESOURCE_ROOT = str(Path(TEST_RESOURCE_ROOT).parent.absolute())


def delete_directory(directory: str) -> None:
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def create_directory(directory: str) -> None:
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)


def create_file(file: str, content: str) -> None:
    create_directory(os.path.dirname(file))
    with open(file, 'w') as f:
        f.write(content)


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    print('Return code:', result.returncode)
    if result.stdout:
        print('Output:', result.stdout.rstrip('\n'))
    if result.stderr:
        print('Error:', result.stderr.rstrip('\n'))
    print()

    return result


def check_files_exist(file_paths: str) -> bool:
    for file_path in file_paths.splitlines():
        return os.path.isfile(file_path)


def check_file_is_in_deb(deb_file_path: str, file_path: str) -> bool:
    return file_path in subprocess.run(['dpkg', '-c', deb_file_path], text=True, stdout=subprocess.PIPE).stdout


def check_files_matches_in_deb(deb_file_path: str, files_and_matchers: list[tuple[str, str]]) -> bool:
    temp_dir = f'{TEST_FILE_SYSTEM_ROOT}/tmp'

    delete_directory(temp_dir)
    os.makedirs(temp_dir)

    subprocess.run(['dpkg-deb', '-e', deb_file_path, temp_dir], check=True)

    all_matches = True

    for file_name, matcher in files_and_matchers:
        file_path = os.path.join(temp_dir, file_name)
        with open(os.path.join(temp_dir, file_path), 'r') as file:
            content = file.read()
            matches = matcher in content
            all_matches = all_matches and matches

    return all_matches
