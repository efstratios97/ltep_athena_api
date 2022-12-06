import pytest

from flask import Flask
from flask_cors import CORS

import ltep_athena_api.microservice as ms


@pytest.fixture
def test_flask_app():
    """This method initializes the Falsk App Instance for testing.
        :returns: Flask App Instance
        :rtype: Flask
    """
    test_app = Flask(__name__)
    CORS(test_app)
    test_app.config.update({
        "TESTING": True,
    })
    test_app.register_blueprint(ms.blueprint)
    yield test_app
