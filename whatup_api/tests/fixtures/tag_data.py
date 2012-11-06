"""Fixtures for tag model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData


class TagData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        author = UserData.Default
        summary = 'summary goes here'
        name = 'defaulttagname'
    
    class SpecifiesNone:
        author = UserData.Default
        name = 'specifiesnonetagname'
