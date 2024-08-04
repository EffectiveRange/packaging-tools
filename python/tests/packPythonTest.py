import os
import shutil
import unittest
from unittest import TestCase

from utils import TEST_PROJECT_ROOT, RESOURCE_ROOT, TEST_RESOURCE_ROOT, delete_directory, TEST_FILE_SYSTEM_ROOT, \
    run_command, create_file, check_files_exist


class PackPythonTest(TestCase):

    def setUp(self):
        delete_directory(TEST_FILE_SYSTEM_ROOT)
        shutil.copytree(f'{TEST_RESOURCE_ROOT}/test-project', TEST_PROJECT_ROOT, dirs_exist_ok=True)
        print()

    def test_pack_python_when_packaging_default(self):
        # Given
        command = [f'{RESOURCE_ROOT}/pack_python', TEST_PROJECT_ROOT]

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_pack_python_when_packaging_default_and_config_file_specified(self):
        # Given
        create_file(f'{TEST_FILE_SYSTEM_ROOT}/tmp/setup.cfg',
                    '[pack-python]\n'
                    'default = dh-virtualenv\n')

        command = [f'{RESOURCE_ROOT}/pack_python', TEST_PROJECT_ROOT, '-c', f'{TEST_FILE_SYSTEM_ROOT}/tmp/setup.cfg']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_pack_python_when_packaging_specified(self):
        # Given
        command = [f'{RESOURCE_ROOT}/pack_python', TEST_PROJECT_ROOT, '-s', 'wheel fpm-deb']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/test_project-1.0.0-py3-none-any.whl\n'
                         f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_pack_python_when_packaging_all_and_no_output_dir_specified(self):
        # Given
        command = [f'{RESOURCE_ROOT}/pack_python', TEST_PROJECT_ROOT, '--all']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_PROJECT_ROOT}/dist/test_project-1.0.0-py3-none-any.whl\n'
                         f'{TEST_PROJECT_ROOT}/dist/python3-test-project_1.0.0_all.deb\n'
                         f'{TEST_PROJECT_ROOT}/dist/test-project_1.0.0-1_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_pack_python_when_packaging_all_and_relative_output_dir_specified(self):
        # Given
        output_dir = 'tests/test_root/etc/dist' if os.path.exists('tests') else 'test_root/etc/dist'
        command = [f'{RESOURCE_ROOT}/pack_python', TEST_PROJECT_ROOT, '-o', output_dir, '--all']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{os.getcwd()}/{output_dir}/test_project-1.0.0-py3-none-any.whl\n'
                         f'{os.getcwd()}/{output_dir}/python3-test-project_1.0.0_all.deb\n'
                         f'{os.getcwd()}/{output_dir}/test-project_1.0.0-1_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_pack_python_when_packaging_all_and_absolute_output_dir_specified(self):
        # Given
        command = [f'{RESOURCE_ROOT}/pack_python', TEST_PROJECT_ROOT, '-o', f'{TEST_FILE_SYSTEM_ROOT}/etc/dist',
                   '--all']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(0, result.returncode)
        self.assertEqual(f'{TEST_FILE_SYSTEM_ROOT}/etc/dist/test_project-1.0.0-py3-none-any.whl\n'
                         f'{TEST_FILE_SYSTEM_ROOT}/etc/dist/python3-test-project_1.0.0_all.deb\n'
                         f'{TEST_FILE_SYSTEM_ROOT}/etc/dist/test-project_1.0.0-1_all.deb\n', result.stdout)
        self.assertTrue(check_files_exist(result.stdout))

    def test_propagates_return_code_of_command(self):
        # Given
        command = [f'{RESOURCE_ROOT}/pack_python', TEST_PROJECT_ROOT, '-o', f'{TEST_FILE_SYSTEM_ROOT}/etc/dist',
                   '--all', '-p', '/invalid/path']

        # When
        result = run_command(command)

        # Then
        self.assertEqual(127, result.returncode)
        self.assertEqual('', result.stdout)


if __name__ == '__main__':
    unittest.main()
