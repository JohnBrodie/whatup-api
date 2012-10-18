""" Hello world sample test"""
from whatup_api import hello
from httplib import OK
from unittest2 import TestCase

class HelloWorldTestCase(TestCase):

    def setUp(self):
        hello.app.config['TESTING'] = True
        self.app = hello.app.test_client()

    def should_return_hello(self):
        resp = self.app.get('/')
        assert 'Hello World!' in resp.data

    def should_return_200_OK(self):
	resp = self.app.get('/')
	assert resp.status_code == OK