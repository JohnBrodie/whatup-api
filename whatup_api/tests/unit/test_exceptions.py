"""Test case for our custom exceptions"""
from whatup_api.exceptions import APIError

from unittest2 import TestCase


class DescribeAPIError(TestCase):

    errors = {'key': 'value'}

    @classmethod
    def setUpClass(cls):
        cls.exception = APIError(cls.errors)

    def should_set_errors(self):
        self.assertEqual(self.exception.errors, self.errors)
