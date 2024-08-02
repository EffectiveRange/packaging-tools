from setuptools import setup

setup(
    name='test-project',
    version='1.0.0',
    description='Test project',
    long_description='Test project for testing Python packaging',
    author='Ferenc Nandor Janky & Attila Gombos',
    author_email='info@effective-range.com',
    packages=['test_module'],
    scripts=['bin/test-project.py'],
    install_requires=['python-context-logger@git+https://github.com/EffectiveRange/python-context-logger.git@latest']
)
