from context_logger import get_logger

log = get_logger('TestClass')


class TestClass:

    def test_method(self):
        log.info('test_method called')
