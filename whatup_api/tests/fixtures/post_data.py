"""Fixtures for Post model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData


class PostData(DataSet):

    class default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        author = UserData.default
        user_id = UserData.default.ref('id')
        topic = 'topic goes here'
        body = 'body goes here'
