"""Fixtures for tag model"""
from datetime import datetime
from fixture import DataSet
from fixture.style import NamedDataStyle


class TagData(DataSet):

    class default:
        id = 1
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        #author = UserData.default
        summary = 'summary goes here'
