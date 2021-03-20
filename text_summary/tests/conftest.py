"""Settings and test preparation for summarizer web app tests."""
import json
import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.api import summaries
from app.main import create_application
from app.config import get_settings, Settings


def pytest_configure(config):
    """Hook for pytest configuration."""
    config.addinivalue_line(
        'markers', 'negative: Negative tests.',
    )


def get_settings_override():
    """Override app settings for testing."""
    return Settings(testing=1, database_url=os.getenv('DATABASE_TEST_URL'))


@pytest.fixture(scope='session')
def test_app():
    """Basic client for summarizer app tests without DB."""
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='session')
def test_app_with_db():
    """Client for summarizer app tests with a DB."""
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


@pytest.fixture(scope='function')
def existing_summary(test_app_with_db, mocked_summarizer):
    """Prepare a summary to use in tests."""
    summary_url = 'http://example.com'

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': summary_url}))
    summary_id = response.json()['id']

    return summary_id, summary_url


@pytest.fixture(scope='function')
def mocked_summarizer(monkeypatch):
    """Mock web page parsing and summarization engine."""
    def mock_generate_summary(summary_id, url):
        return 'summary'
    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)
