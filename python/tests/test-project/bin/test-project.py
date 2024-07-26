from context_logger import setup_logging
from test_module import TestClass


def main() -> None:
    setup_logging('test-project')

    test_class = TestClass()

    test_class.test_method()


if __name__ == '__main__':
    main()
