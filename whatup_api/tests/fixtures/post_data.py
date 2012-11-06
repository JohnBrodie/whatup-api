"""Fixtures for Post model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData


class PostData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        author = UserData.Default
        topic = 'topic goes here'
        body = 'body goes here'

    class SpecifiesNone:
        body = 'Tortoise, plaid, and Swedish meatballs.'
        author = UserData.Default
