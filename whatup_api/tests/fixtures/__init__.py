import whatup_api.models as m
from fixture import SQLAlchemyFixture
from fixture.style import NamedDataStyle


def install(app, *args):
    engine = m.create_tables(app)
    db = SQLAlchemyFixture(env=m, style=NamedDataStyle(), engine=engine)
    data = db.data(*args)
    data.setup()
    db.dispose()
    return data


# A simple trick for installing all fixtures from an external module.
from whatup_api.tests.fixtures.user_data import UserData
from whatup_api.tests.fixtures.tag_data import TagData
from whatup_api.tests.fixtures.post_data import PostData
from whatup_api.tests.fixtures.subscription_data import SubscriptionData
from whatup_api.tests.fixtures.attachment_data import AttachmentData
from whatup_api.tests.fixtures.revision_data import RevisionData
all_data = (UserData, TagData, PostData, SubscriptionData, AttachmentData, RevisionData,)
