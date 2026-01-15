import os
import shutil
import unittest
from unittest import TestCase

from utils import (
    TEST_PROJECT_ROOT,
    TEST_RESOURCE_ROOT,
    TEST_FILE_SYSTEM_ROOT,
    delete_directory,
    check_file_is_in_deb,
    RESOURCE_ROOT,
    run_command,
    check_files_matches_in_deb,
    check_files_exist, delete_file,
)


class WheelDebTest(TestCase):

    def setUp(self):
        delete_directory(TEST_FILE_SYSTEM_ROOT)
        shutil.copytree(f"{TEST_RESOURCE_ROOT}/test-project", TEST_PROJECT_ROOT, dirs_exist_ok=True)
        delete_file(f"{TEST_PROJECT_ROOT}/pyproject.toml")
        print()

    def test_wheel_deb_when_no_output_dir_specified(self):
        # Given
        command = [f"{RESOURCE_ROOT}/pack_wheel-deb.py", TEST_PROJECT_ROOT, "-t", "amd64"]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_amd64.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))
        self.assertFalse(check_files_exist(f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb\n"))

    def test_wheel_deb_when_relative_output_dir_specified(self):
        # Given
        output_dir = (
            "tests/test_root/etc/dist"
            if os.path.exists("tests")
            else "test_root/etc/dist"
        )
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb.py",
            TEST_PROJECT_ROOT,
            "-o", output_dir,
            "-t", "arm64"
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{os.getcwd()}/{output_dir}/test-project_1.0.0-1_arm64.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))

    def test_wheel_deb_when_absolute_output_dir_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb.py",
            TEST_PROJECT_ROOT,
            "-o", f"{TEST_FILE_SYSTEM_ROOT}/etc/dist",
            "-t", "amd64"
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_FILE_SYSTEM_ROOT}/etc/dist/test-project_1.0.0-1_amd64.deb\n",
            result.stdout,
        )
        self.assertTrue(check_files_exist(result.stdout))

    def test_wheel_deb_when_service_file_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb.py",
            TEST_PROJECT_ROOT,
            "-s", f"{TEST_PROJECT_ROOT}/service/test-project.service",
            "-t", "amd64"
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_amd64.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))
        self.assertTrue(
            check_file_is_in_deb(
                f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_amd64.deb",
                "lib/systemd/system/test-project.service",
            )
        )

    def test_wheel_deb_when_multiple_service_files_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb.py",
            TEST_PROJECT_ROOT,
            "-s", f"{TEST_PROJECT_ROOT}/service/test-project.1.service",
            "-s", f"{TEST_PROJECT_ROOT}/service/test-project.2.service",
            "-t", "arm64"
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_arm64.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))
        self.assertTrue(
            check_file_is_in_deb(
                f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_arm64.deb",
                ["lib/systemd/system/1.service", "lib/systemd/system/2.service"],
            )
        )

    def test_wheel_deb_when_lifecycle_files_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb.py",
            TEST_PROJECT_ROOT,
            "--preinst-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.preinst",
            "--postinst-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.postinst",
            "--prerm-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.prerm",
            "--postrm-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.postrm",
            "-t", "amd64"
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_amd64.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))
        self.assertTrue(
            check_files_matches_in_deb(
                f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_amd64.deb",
                [
                    ("preinst", "installing test-project"),
                    ("postinst", "test-project installed"),
                    ("prerm", "removing test-project"),
                    ("postrm", "test-project removed"),
                ],
            )
        )

    def test_wheel_deb_when_service_and_lifecycle_files_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb.py",
            TEST_PROJECT_ROOT,
            "-s", f"{TEST_PROJECT_ROOT}/service/test-project.service",
            "--preinst-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.preinst",
            "--postinst-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.postinst",
            "--prerm-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.prerm",
            "--postrm-file", f"{TEST_PROJECT_ROOT}/scripts/test-project.postrm",
            "-t", "arm64"
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_arm64.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))
        self.assertTrue(
            check_file_is_in_deb(
                f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_arm64.deb",
                "lib/systemd/system/test-project.service",
            )
        )
        self.assertTrue(
            check_files_matches_in_deb(
                f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_arm64.deb",
                [
                    ("preinst", "installing test-project"),
                    ("postinst", "test-project installed"),
                    ("prerm", "removing test-project"),
                    ("postrm", "test-project removed"),
                ],
            )
        )

    def test_propagates_return_code_of_command(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb.py",
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
