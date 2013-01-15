"""Test case for Attachment model"""
from whatup_api.tests.unit.models import _ModelTestCase


class AttachmentModelTestCase(_ModelTestCase):
    """Tests for Attachment model"""

    model_name = 'Attachment'


class DescribeAttachmentModel(AttachmentModelTestCase):

    def should_have_name(self):
        self.assertEquals(self.Default.name, self.attachment_data.Default.name)

    def should_have_name_as_string(self):
        self.assertTrue(self.is_type('name', self.db.String))

    def should_have_name_with_length(self):
        self.assertEquals(self.get_length('name'), 100)

    def should_have_non_nullable_name(self):
        self.assertFalse(self.is_nullable('name'))

    def should_have_location(self):
        self.assertEquals(self.Default.location, self.attachment_data.Default.location)

    def should_have_location_as_string(self):
        self.assertTrue(self.is_type('location', self.db.String))

    def should_have_location_with_length(self):
        self.assertEquals(self.get_length('location'), 100)

    def should_have_non_nullable_location(self):
        self.assertFalse(self.is_nullable('location'))

    def should_have_non_nullable_user(self):
        self.assertFalse(self.is_nullable('user_id'))

    def should_have_post(self):
        post = self.Default.post
        self.assertEqual(post.id, self.post_data.Default.id)

    def should_have_uploader(self):
        uploader = self.Default.uploader
        self.assertEqual(uploader.id, self.user_data.Default.id)
