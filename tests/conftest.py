import tempfile
import pytest
from backend.app import create_app
from backend.database import init_db

@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp(suffix=".db")
    app = create_app(path)
    init_db(path, seed=True)
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client
    import os
    os.close(fd)
    os.unlink(path)
