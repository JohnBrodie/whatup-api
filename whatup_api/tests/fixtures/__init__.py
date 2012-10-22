import whatup_api.models as m
from fixture import SQLAlchemyFixture
from fixture.style import NamedDataStyle

def install(app, *args):
    engine = m.create_tables(app)
    db = SQLAlchemyFixture(env=m, style=NamedDataStyle(), engine=engine)
    data = db.data(*args)
    data.setup()
    db.dispose()


# A simple trick for installing all fixtures from an external module.
from whatup_api.tests.fixtures.egg_data import EggData
from whatup_api.tests.fixtures.spam_data import SpamData
all_data = (SpamData, EggData,)
