from mock import MagicMock, Mock
from whatup_api.helpers.app_helpers import remove_is_admin
import unittest2 as unittest


class _BaseWhenRemovingIsAdminTestCase(unittest.TestCase):

    def setUp(self):
        self.configure()
        self.execute()

    def configure(self):
        self.put_data = MagicMock()
        self.instid = Mock()

    def execute(self):
        self.returned = remove_is_admin(self.put_data, self.instid)

    def should_return_put_data(self):
        self.assertEqual(self.returned, self.put_data)

    def should_check_if_admin_key_exists(self):
        self.put_data.__contains__.assert_called_once_with('is_admin')


class WhenRemovingIsAdminAndAdminKeyExists(_BaseWhenRemovingIsAdminTestCase):

    def configure(self):
        super(WhenRemovingIsAdminAndAdminKeyExists, self).configure()
        self.put_data.__contains__.return_value = True

    def should_delete_admin_key(self):
        self.put_data.__delitem__.assert_called_once_with('is_admin')


class WhenRemovingIsAdminAndAdminKeyNotExists(_BaseWhenRemovingIsAdminTestCase):

    def configure(self):
        super(WhenRemovingIsAdminAndAdminKeyNotExists, self).configure()
        self.put_data.__contains__.return_value = False

    def should_not_delete_admin_key(self):
        self.assertEqual(len(self.put_data.__delitem__.mock_calls), 0)
