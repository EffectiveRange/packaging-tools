import os
import shutil
import unittest
from unittest import TestCase

from utils import TEST_PROJECT_ROOT, TEST_RESOURCE_ROOT, TEST_FILE_SYSTEM_ROOT, \
    delete_directory, check_file_is_in_deb, SCRIPTS_DIR, run_command, check_files_matches_in_deb


class DhVirtualenvTest(TestCase):

    def setUp(self):
        delete_directory(TEST_FILE_SYSTEM_ROOT)
        shutil.copytree(f'{TEST_RESOURCE_ROOT}/test-project', TEST_PROJECT_ROOT, dirs_exist_ok=True)
        print()

    def test_dh_virtualenv_when_no_output_dir_specified(self):
        # Given
        command = [f'{SCRIPTS_DIR}/dh-virtualenv', TEST_PROJECT_ROOT]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb\n', result.stdout)

    def test_dh_virtualenv_when_relative_output_dir_specified(self):
        # Given
        output_dir = 'tests/test_root/etc/dist' if os.path.exists('tests') else 'test_root/etc/dist'
        command = [f'{SCRIPTS_DIR}/dh-virtualenv', TEST_PROJECT_ROOT, '-o', output_dir]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{os.getcwd()}/{output_dir}/test-project_1.0.0-1_all.deb\n', result.stdout)

    def test_dh_virtualenv_when_absolute_output_dir_specified(self):
        # Given
        command = [f'{SCRIPTS_DIR}/dh-virtualenv', TEST_PROJECT_ROOT, '-o', f'{TEST_FILE_SYSTEM_ROOT}/etc/dist']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_FILE_SYSTEM_ROOT}/etc/dist/test-project_1.0.0-1_all.deb\n', result.stdout)

    def test_dh_virtualenv_when_service_file_specified(self):
        # Given
        command = [f'{SCRIPTS_DIR}/dh-virtualenv', TEST_PROJECT_ROOT,
                   '-s', f'{TEST_PROJECT_ROOT}/service/test-project.service']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb\n', result.stdout)
        self.assertTrue(check_file_is_in_deb(f'{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb',
                                             'lib/systemd/system/test-project.service'))

    def test_dh_virtualenv_when_extra_files_specified(self):
        # Given
        command = [f'{SCRIPTS_DIR}/dh-virtualenv', TEST_PROJECT_ROOT, '-e', f'{TEST_PROJECT_ROOT}/scripts/*']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb\n', result.stdout)
        self.assertTrue(check_files_matches_in_deb(f'{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb',
                                                   [('postinst', 'test-project successfully installed'),
                                                    ('postrm', 'test-project successfully removed')]))


if __name__ == '__main__':
    unittest.main()
