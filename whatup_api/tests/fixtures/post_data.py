"""Fixtures for Post model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData


class PostData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        created_by = UserData.Default
        last_modified_by = UserData.Default
        topic = 'topic goes here'
        body = 'body goes here'
        is_deleted = False

    class SpecifiesNone:
        body = 'Tortoise, plaid, and Swedish meatballs.'
        created_by = UserData.Default
        last_modified_by = UserData.Default
