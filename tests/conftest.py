import pytest
from werkzeug.datastructures import FileStorage
import os
from app import create_app


@pytest.fixture(scope='module')
def test_client():
    # Create a test client using the Flask application configured for testing
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture()
def dataset():
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    mock_file = FileStorage(
        stream=open(os.path.join(CUR_DIR, "iris.csv"), "rb"),
        filename="iris.csv",
        content_type="application/json",
    )
    return mock_file


@pytest.fixture(scope="module")
def input_line():
    return {
        "Sepal.Length": 2.4,
        "Sepal.Width": 4.9,
        "Petal.Length": 1.5,
        "Petal.Width": 0.6
    }
