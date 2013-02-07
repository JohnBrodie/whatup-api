"""Fixtures for OpenIDWhitelist model"""
from datetime import datetime
from fixture import DataSet


class OpenIDWhitelistData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        name = 'name here'
        is_deleted = False
        email = 'joe@blow.com'

    class SpecifiesNone:
        name = 'name again'
        email = 'carl@carl.cc'
