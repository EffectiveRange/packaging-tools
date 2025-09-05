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
    check_files_exist,
)


class WheelDebTest(TestCase):

    def setUp(self):
        delete_directory(TEST_FILE_SYSTEM_ROOT)
        shutil.copytree(
            f"{TEST_RESOURCE_ROOT}/test-project", TEST_PROJECT_ROOT, dirs_exist_ok=True
        )
        print()

    def test_wheel_deb_when_no_output_dir_specified(self):
        # Given
        command = [f"{RESOURCE_ROOT}/pack_wheel-deb", TEST_PROJECT_ROOT]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_amd64.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))

    def test_wheel_deb_when_architecture_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb",
            TEST_PROJECT_ROOT,
            "-A",
            "all",
        ]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(
            f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb\n", result.stdout
        )
        self.assertTrue(check_files_exist(result.stdout))
        self.assertTrue(
            check_files_matches_in_deb(
                f"{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb", [("control", "Architecture: all")],
            )
        )

    def test_wheel_deb_when_service_file_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb",
            TEST_PROJECT_ROOT,
            "-s",
            f"{TEST_PROJECT_ROOT}/service/test-project.service",
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

    def test_wheel_deb_when_lifecycle_files_specified(self):
        # Given
        command = [
            f"{RESOURCE_ROOT}/pack_wheel-deb",
            TEST_PROJECT_ROOT,
            "--preinst-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.preinst",
            "--postinst-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.postinst",
            "--prerm-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.prerm",
            "--postrm-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.postrm",
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
            f"{RESOURCE_ROOT}/pack_wheel-deb",
            TEST_PROJECT_ROOT,
            "-s",
            f"{TEST_PROJECT_ROOT}/service/test-project.service",
            "--preinst-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.preinst",
            "--postinst-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.postinst",
            "--prerm-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.prerm",
            "--postrm-file",
            f"{TEST_PROJECT_ROOT}/scripts/test-project.postrm",
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


if __name__ == "__main__":
    unittest.main()
