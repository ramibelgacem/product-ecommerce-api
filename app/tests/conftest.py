import os

import pytest

from app.db.htmltableinterface import HtmlTableInterface


@pytest.fixture
def fake_db():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_file = os.path.join(base, "templates/test_index.html")
    db = HtmlTableInterface(db_file)
    yield db
    db.clear()
