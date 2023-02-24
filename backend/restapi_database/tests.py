from django.test import TestCase
from django.test.runner import DiscoverRunner


class MongoDBTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


class MongoDBTestCase(TestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass
