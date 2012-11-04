from flask.ext.script import Manager

from whatup_api.hello import app
import whatup_api.tests.fixtures as _fixtures
import whatup_api.models as m

manager = Manager(app)


@manager.command
def tables():
    "Create database tables."
    m.create_tables(app)


@manager.command
def fixtures():
    "Install test data fixtures into the configured database."
    _fixtures.install(app, *_fixtures.all_data)


if __name__ == "__main__":
    manager.run()
