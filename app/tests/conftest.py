import json
from unittest.mock import patch, mock_open

import pytest

from app.app import app


@pytest.fixture()
def test_client():
    return app.test_client()


@pytest.fixture()
def open_mock():
    with patch('builtins.open', new_callable=mock_open, read_data=json.dumps([{'post_id': 1}])) as mock:
        yield mock
