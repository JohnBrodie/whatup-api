import unittest2

import whatup_api.models as m
from whatup_api.tests.unit.models import ModelTestCase


class ModelTestCase(ModelTestCase):

    def test_spam(self):
        spam = m.Spam.query.first()
        self.assertEquals(spam.name, 'spam spam spam')

    def test_egg(self):
        egg = m.Egg.query.first()
        self.assertTrue(egg.description.startswith('green'))


if __name__ == '__main__':
    unittest.main()
