import os
import shutil
import unittest
from unittest import TestCase

from utils import (
    TEST_PROJECT_ROOT,
    TEST_RESOURCE_ROOT,
    TEST_FILE_SYSTEM_ROOT,
    RESOURCE_ROOT,
    delete_directory,
    run_command,
    check_files_exist,
)


class WheelTest(TestCase):

    def setUp(self):
        delete_directory(TEST_FILE_SYSTEM_ROOT)
        shutil.copytree(
            f"{TEST_RESOURCE_ROOT}/test-project", TEST_PROJECT_ROOT, dirs_exist_ok=True
        )
        print()

    def test_wheel_when_no_output_dir_specified(self):
        # Given
        command = [f"{RESOURCE_ROOT}/pack_wheel", TEST_PROJECT_ROOT]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test_project-1.0.0-py3-none-any.whl\n",
            result.stdout,
        )
        self.assertTrue(check_files_exist(result.stdout))

    def test_wheel_when_relative_output_dir_specified(self):
        # Given
        output_dir = (
            "tests/test_root/etc/dist"
            if os.path.exists("tests")
            else "test_root/etc/dist"
        )
        command = [f"{RESOURCE_ROOT}/pack_wheel", TEST_PROJECT_ROOT, "-o", output_dir]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{os.getcwd()}/{output_dir}/test_project-1.0.0-py3-none-any.whl\n",
            result.stdout,
        )
        self.assertTrue(check_files_exist(result.stdout))

    def test_wheel_when_absolute_output_dir_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel",
            TEST_PROJECT_ROOT,
            "-o",
            f"{TEST_FILE_SYSTEM_ROOT}/etc/dist",
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_FILE_SYSTEM_ROOT}/etc/dist/test_project-1.0.0-py3-none-any.whl\n",
            result.stdout,
        )
        self.assertTrue(check_files_exist(result.stdout))

    def test_propagates_return_code_of_command(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel",
            TEST_PROJECT_ROOT,
            "-p",
            "/invalid/path",
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(127, result.returncode)
        self.assertEqual("", result.stdout)


if __name__ == "__main__":
    unittest.main()
