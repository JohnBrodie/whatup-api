"""Fixtures for OpenIDWhitelist model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData


class OpenIDWhitelistData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        name = 'name here'
        is_deleted = False
        email = UserData.Default.email

    class SpecifiesNone:
        name = 'name again'
        email = UserData.SpecifiesNone.email
