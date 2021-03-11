import json
import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.main import create_application
from app.config import get_settings, Settings


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'negative: Negative tests.'
    )


def get_settings_override():
    return Settings(testing=1, database_url=os.getenv('DATABASE_TEST_URL'))


@pytest.fixture(scope='module')
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='module')
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    register_tortoise(
        app,
        db_url=os.getenv('DATABASE_TEST_URL'),
        modules={'models': ['app.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='module')
def existing_summary(test_app_with_db):
    summary_url = 'http://example.com'

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': summary_url}))
    summary_id = response.json()['id']

    return summary_id, summary_url
