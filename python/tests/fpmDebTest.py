import os
import shutil
import unittest
from unittest import TestCase

from utils import TEST_PROJECT_ROOT, TEST_RESOURCE_ROOT, delete_directory, TEST_FILE_SYSTEM_ROOT, \
    RESOURCE_ROOT, run_command, check_file_is_in_deb, check_files_matches_in_deb, check_files_exist


class FpmDebTest(TestCase):

    def setUp(self):
        delete_directory(TEST_FILE_SYSTEM_ROOT)
        shutil.copytree(f'{TEST_RESOURCE_ROOT}/test-project', TEST_PROJECT_ROOT, dirs_exist_ok=True)
        print()

    def test_fpm_deb_when_no_output_dir_specified(self):
        # Given
        command = [f'{RESOURCE_ROOT}/fpm-deb', TEST_PROJECT_ROOT]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_fpm_deb_when_relative_output_dir_specified(self):
        # Given
        output_dir = 'tests/test_root/etc/dist' if os.path.exists('tests') else 'test_root/etc/dist'
        command = [f'{RESOURCE_ROOT}/fpm-deb', TEST_PROJECT_ROOT, '-o', output_dir]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{os.getcwd()}/{output_dir}/python3-test-project_1.0.0_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_fpm_deb_when_absolute_output_dir_specified(self):
        # Given
        command = [f'{RESOURCE_ROOT}/fpm-deb', TEST_PROJECT_ROOT, '-o', f'{TEST_FILE_SYSTEM_ROOT}/etc/dist']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_FILE_SYSTEM_ROOT}/etc/dist/python3-test-project_1.0.0_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_fpm_deb_when_service_file_specified(self):
        # Given
        command = [f'{RESOURCE_ROOT}/fpm-deb', TEST_PROJECT_ROOT,
                   '-a', f'--deb-systemd {TEST_PROJECT_ROOT}/service/test-project.service']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))
        self.assertTrue(check_file_is_in_deb(f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb',
                                             'lib/systemd/system/test-project.service'))

    def test_fpm_deb_when_extra_files_specified(self):
        # Given
        command = [f'{RESOURCE_ROOT}/fpm-deb', TEST_PROJECT_ROOT,
                   '-a', f'--after-install {TEST_PROJECT_ROOT}/scripts/test-project.postinst']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))
        self.assertTrue(check_files_matches_in_deb(f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb',
                                                   [('postinst', 'test-project successfully installed')]))

    def test_propagates_return_code_of_command(self):
        # Given
        command = [f'{RESOURCE_ROOT}/fpm-deb', TEST_PROJECT_ROOT, '-p', '/invalid/path']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(1, result.returncode)
        self.assertEqual('', result.stdout)


if __name__ == '__main__':
    unittest.main()
