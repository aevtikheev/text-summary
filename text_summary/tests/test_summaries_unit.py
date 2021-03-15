"""Unit tests (with mocked DB calls) for /summaries/ resource."""
from datetime import datetime
import json

import pytest

from app.api import crud


SUMMARIES_ENDPOINT = 'summaries'

ID_FIELD = 'id'
URL_FIELD = 'url'
SUMMARY_FIELD = 'summary'
CREATED_AT_FIELD = 'created_at'
ERROR_DETAIL_FIELD = 'detail'

SUMMARY_DATA = {
        ID_FIELD: 1,
        URL_FIELD: 'http://example.com',
        SUMMARY_FIELD: 'summary',
        CREATED_AT_FIELD: datetime.utcnow().isoformat(),
    }
MULTIPLE_SUMMARIES_DATA = [
    {
        ID_FIELD: 1,
        URL_FIELD: 'http://example.com',
        SUMMARY_FIELD: 'summary',
        CREATED_AT_FIELD: datetime.utcnow().isoformat(),
    },
    {
        ID_FIELD: 2,
        URL_FIELD: 'http://example.com',
        SUMMARY_FIELD: 'summary',
        CREATED_AT_FIELD: datetime.utcnow().isoformat(),
    }
]


async def mock_create(payload):
    return SUMMARY_DATA


async def mock_read(summary_id):
    return SUMMARY_DATA


async def mock_read_nonexistent(summary_id):
    return None


async def mock_read_all():
    return MULTIPLE_SUMMARIES_DATA


async def mock_update(summary_id, payload):
    return SUMMARY_DATA


async def mock_update_nonexistent(summary_id, payload):
    return None


async def mock_delete(summary_id):
    return SUMMARY_DATA


@pytest.mark.skip()
def test_create_summary(test_app, monkeypatch, mocked_summarizer):
    summary_url = SUMMARY_DATA[URL_FIELD]

    monkeypatch.setattr(crud, 'create', mock_create)

    response = test_app.post(
        f'{SUMMARIES_ENDPOINT}/',
        data=json.dumps({URL_FIELD: summary_url}),
    )

    assert response.status_code == 201, f'Invalid response code: {response.status_code}'
    assert response.json()[URL_FIELD] == summary_url, (
        f'Invalid summary URL: {response.json()[URL_FIELD]}',
    )


def test_read_summary(test_app, monkeypatch):
    monkeypatch.setattr(crud, 'read', mock_read)

    summary_id = SUMMARY_DATA[ID_FIELD]
    response = test_app.get(f'{SUMMARIES_ENDPOINT}/{summary_id}/')

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'
    assert response.json() == SUMMARY_DATA, 'Wrong response content'


def test_read_all_summaries(test_app, monkeypatch):
    monkeypatch.setattr(crud, 'read_all', mock_read_all)

    response = test_app.get(f'{SUMMARIES_ENDPOINT}/')

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'

    assert response.json() == MULTIPLE_SUMMARIES_DATA, 'Wrong response content'


def test_update_summary(test_app, monkeypatch):
    monkeypatch.setattr(crud, 'update', mock_update)

    summary_id = SUMMARY_DATA[ID_FIELD]
    summary_url = SUMMARY_DATA[URL_FIELD]

    response = test_app.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps({URL_FIELD: summary_url, SUMMARY_FIELD: 'new_summary'}),
    )

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'

    assert response.json() == SUMMARY_DATA, 'Wrong response content'


def test_delete_summary(test_app, monkeypatch):
    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'delete', mock_delete)

    summary_id = SUMMARY_DATA[ID_FIELD]

    response = test_app.delete(f'{SUMMARIES_ENDPOINT}/{summary_id}/')

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'


@pytest.mark.negative
@pytest.mark.parametrize(
    'payload',
    [{}, {URL_FIELD: 'invalid://url'}],
    ids=['empty payload', 'incorrect url'],
)
def test_create_summary_incorrect_payload(test_app, payload, monkeypatch, mocked_summarizer):
    response = test_app.post(f'{SUMMARIES_ENDPOINT}/', data=json.dumps({}))

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
@pytest.mark.parametrize(
    'summary_id,response_code',
    [('abc', 422), ('0', 422), ('99999999', 404)],
    ids=['non-digit ID', 'zero ID', 'Nonexistent ID'],
)
def test_read_summary_incorrect_id(test_app, summary_id, response_code, monkeypatch):
    monkeypatch.setattr(crud, 'read', mock_read_nonexistent)

    response = test_app.get(f'{SUMMARIES_ENDPOINT}/{summary_id}/')

    assert response.status_code == response_code, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
@pytest.mark.parametrize(
    'summary_id,response_code',
    [('abc', 422), ('0', 422), ('99999999', 404)],
    ids=['non-digit ID', 'zero ID', 'Nonexistent ID'],
)
def test_update_summary_incorrect_id(
        test_app, summary_id, response_code, monkeypatch
):
    monkeypatch.setattr(crud, 'update', mock_update_nonexistent)
    response = test_app.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps({URL_FIELD: 'http://example.com', SUMMARY_FIELD: 'updated_summary'}),
    )

    assert response.status_code == response_code, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
@pytest.mark.parametrize(
    'payload',
    [
        {SUMMARY_FIELD: 'new_summary'},
        {SUMMARY_FIELD: 'new_summary', URL_FIELD: 'invalid://url'},
        {URL_FIELD: 'http://example.com'},
        {},
    ],
    ids=['Missing URL', 'Incorrect URL', 'Missing summary', 'Empty payload'],
)
def test_update_summary_incorrect_payload(test_app, existing_summary, payload, monkeypatch):
    summary_id = SUMMARY_DATA[ID_FIELD]

    response = test_app.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps(payload),
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
@pytest.mark.parametrize(
    'summary_id,response_code',
    [('abc', 422), ('0', 422), ('99999999', 404)],
    ids=['non-digit ID', 'zero ID', 'Nonexistent ID'],
)
def test_delete_summary_incorrect_id(test_app, summary_id, response_code, monkeypatch):
    monkeypatch.setattr(crud, 'read', mock_read_nonexistent)

    response = test_app.delete(f'{SUMMARIES_ENDPOINT}/{summary_id}/')

    assert response.status_code == response_code, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'
