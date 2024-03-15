from os.path import (join, abspath, dirname)
from glob import glob

from app.database import get_db
import pytest

@pytest.fixture(scope='session')
def init_database(request):
    """Initializes the database """
    DB = get_db()
    DB.drop_all()
    DB.create_all()

    base_dir = join(abspath(dirname(__file__)))

#    for fixture_file in glob(join(base_dir, 'seed', '*.json')):
#        fixtures = JSONLoader().load(fixture_file)
#        load_fixtures(DB, fixtures)

#    for fixture_file in sorted(glob(join(base_dir, 'seed', 'demo', '*.json'))):
#        fixtures = JSONLoader().load(fixture_file)
#        load_fixtures(DB, fixtures)


    request.cls.DB = DB

    yield DB

#    close_all_sessions()
