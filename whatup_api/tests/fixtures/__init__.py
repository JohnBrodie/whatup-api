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
all_data = (UserData, TagData,)
