""" Attachments endpoint test"""
import os
import whatup_api.config as config
from shutil import rmtree
from whatup_api.tests.functional import _FunctionalTestCase


class WhenUploadingFile(_FunctionalTestCase):
    post_headers = [('Content-Type', 'multipart/form-data')]
    expected_status = 200
    endpoint = '/upload'
    filename = 'test.png'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    post_data = {}

    def should_return_attachment_user(self):
        self.assertEqual(self.json['user_id'],
                         self.fixture_data.UserData.Default.id)

    def should_return_filename(self):
        self.assertEqual(self.json['name'], self.filename)

    def should_have_file_in_dir(self):
        try:
            open(config.ATTACHMENTS_DIR + '/' + self.json['location'])
        except IOError:
            assert False

    @classmethod
    def tearDownClass(cls):
        rmtree(config.ATTACHMENTS_DIR)


class WhenValidURLIsProvided(_FunctionalTestCase):
    post_headers = [('Content-Type', 'multipart/form-data')]
    expected_status = 200
    endpoint = '/upload'
    post_data = {'url': 'http://ipv4.download.thinkbroadband.com/5MB.zip'}
    filename = '5MB.zip'

    def should_return_attachment_user(self):
        self.assertEqual(self.json['user_id'],
                         self.fixture_data.UserData.Default.id)

    def should_return_filename(self):
        self.assertEqual(self.json['name'], self.filename)

    def should_have_file_in_dir(self):
        try:
            open(config.ATTACHMENTS_DIR + '/' + self.json['location'])
        except IOError:
            assert False

    @classmethod
    def tearDownClass(cls):
        rmtree(config.ATTACHMENTS_DIR)


class WhenURLIsOversizeFile(_FunctionalTestCase):
    post_headers = [('Content-Type', 'multipart/form-data')]
    post_data = {'url': 'http://ipv4.download.thinkbroadband.com/200MB.zip'}
    expected_status = 400
    endpoint = '/upload'


class WhenURLIsInvalid(_FunctionalTestCase):
    post_headers = [('Content-Type', 'multipart/form-data')]
    post_data = {'url': 'jijijijijijijjijijijfjffjfjjfjfjffffj.net'}
    expected_status = 400
    endpoint = '/upload'


class WhenOmittingFile(_FunctionalTestCase):
    post_headers = [('Content-Type', 'multipart/form-data')]
    expected_status = 400
    endpoint = '/upload'
    filename = 'doesntExist.png'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    post_data = {}

    def should_return_no_file_error(self):
        self.assertEqual('No files in request', self.json['error'])

class WhenDeletingFile(_FunctionalTestCase):
    delete = True
    expected_status = 200
    endpoint = '/attachments/1'
    filepath = config.ATTACHMENTS_DIR + '/' + 'randomstring'
    if not os.path.exists(config.ATTACHMENTS_DIR):
        os.makedirs(config.ATTACHMENTS_DIR)
    open(filepath, 'w').close()

    def should_have_deleted_file(self):
        try:
            f = open(self.filepath)
            f.close()
            self.assertFalse(True)
        except IOError:
            self.assertTrue(True)

    @classmethod
    def tearDownClass(cls):
        rmtree(config.ATTACHMENTS_DIR)

class WhenDeletingNonExistentFile(_FunctionalTestCase):
    delete = True
    expected_status = 400
    endpoint = '/attachments/999'
