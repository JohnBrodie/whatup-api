"""Fixtures for Attachment model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData
from whatup_api.tests.fixtures.post_data import PostData


class AttachmentData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        uploader = UserData.Default
        post = PostData.Default
        name = "file.file"
        location = "randomstring"

    class SpecifiesNone:
        uploader = UserData.Default
        post = PostData.Default
        name = "file.file"
        location = "randomstring"
