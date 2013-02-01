"""Fixtures for Revision model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData
from whatup_api.tests.fixtures.post_data import PostData


class RevisionData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        author = UserData.Default
        post = PostData.Default
        body = "Lorem ipsum"

    class SpecifiesNone:
        author = UserData.Default
        post = PostData.Default
        body = "Lorem ipsum"
