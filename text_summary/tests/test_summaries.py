"""Tests for /summaries/ resource."""
import json

import pytest

SUMMARIES_ENDPOINT = '/summaries'
ID_FIELD = 'id'
URL_FIELD = 'url'
SUMMARY_FIELD = 'summary'
CREATED_AT_FIELD = 'created_at'
ERROR_DETAIL_FIELD = 'detail'


def test_create_summary(test_app_with_db):
    summary_url = 'http://example.com'
    response = test_app_with_db.post(
        f'{SUMMARIES_ENDPOINT}/',
        data=json.dumps({URL_FIELD: summary_url})
    )

    assert response.status_code == 201, f'Invalid response code: {response.status_code}'
    assert response.json()[URL_FIELD] == summary_url, (
        f'Invalid summary URL: {response.json()[URL_FIELD]}'
    )


@pytest.mark.negative
def test_create_summary_empty_payload(test_app_with_db):
    response = test_app_with_db.post(f'{SUMMARIES_ENDPOINT}/', data=json.dumps({}))

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_create_summary_incorrect_url(test_app_with_db):
    response = test_app_with_db.post(
        f'{SUMMARIES_ENDPOINT}/',
        data=json.dumps({URL_FIELD: 'invalid://url'})
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


def test_read_summary(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.get(f'{SUMMARIES_ENDPOINT}/{summary_id}/')

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'

    response_json = response.json()
    assert response_json[ID_FIELD] == summary_id, f'Invalid id field: {response_json[ID_FIELD]}'
    assert response_json[URL_FIELD] == summary_url, f'Invalid url field: {response_json[URL_FIELD]}'
    assert response_json.get(SUMMARY_FIELD), 'Missing or empty summary field'
    assert response_json.get(CREATED_AT_FIELD), 'Missing or empty created_at field'


def test_read_all_summaries(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.get(f'{SUMMARIES_ENDPOINT}/')

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'

    response_json = response.json()
    assert len(list(filter(lambda summary: summary[ID_FIELD] == summary_id, response_json))) == 1, (
        'Existing summary is not present in the result.'
    )


@pytest.mark.negative
def test_read_nonexistent_summary(test_app_with_db):
    response = test_app_with_db.get(f'{SUMMARIES_ENDPOINT}/9999999/')

    assert response.status_code == 404, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(f'{SUMMARIES_ENDPOINT}/abc/')

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_read_summary_zero_id(test_app_with_db):
    response = test_app_with_db.get(f'{SUMMARIES_ENDPOINT}/0/')

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


def test_update_summary(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    new_summary = 'updated_summary'
    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps({URL_FIELD: summary_url, SUMMARY_FIELD: new_summary})
    )

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'

    response_json = response.json()
    assert response_json[ID_FIELD] == summary_id, f'Invalid id field: {response_json[ID_FIELD]}'
    assert response_json[URL_FIELD] == summary_url, f'Invalid url field: {response_json[URL_FIELD]}'
    assert response_json[SUMMARY_FIELD] == new_summary, (
        f'Invalid summary field: {response_json[SUMMARY_FIELD]}'
    )
    assert response_json.get(CREATED_AT_FIELD), 'Missing or empty created_at field'


@pytest.mark.negative
def test_update_nonexistent_summary(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/9999999/',
        data=json.dumps({URL_FIELD: summary_url, SUMMARY_FIELD: 'updated_summary'})
    )

    assert response.status_code == 404, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_update_summary_incorrect_id(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/abc/',
        data=json.dumps({URL_FIELD: summary_url, SUMMARY_FIELD: 'updated_summary'})
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_update_summary_zero_id(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/0/',
        data=json.dumps({URL_FIELD: summary_url, SUMMARY_FIELD: 'updated_summary'})
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_update_summary_missing_url(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    new_summary = 'updated_summary'
    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps({SUMMARY_FIELD: new_summary})
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_update_summary_incorrect_url(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    new_summary = 'updated_summary'
    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps({SUMMARY_FIELD: new_summary, URL_FIELD: 'invalid://url'})
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_update_summary_missing_summary(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps({URL_FIELD: summary_url})
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_update_summary_empty_payload(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.put(
        f'{SUMMARIES_ENDPOINT}/{summary_id}/',
        data=json.dumps({})
    )

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


def test_delete_summary(test_app_with_db, existing_summary):
    summary_id, summary_url = existing_summary

    response = test_app_with_db.delete(f'{SUMMARIES_ENDPOINT}/{summary_id}/')

    assert response.status_code == 200, f'Invalid response code: {response.status_code}'


@pytest.mark.negative
def test_delete_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete(f'{SUMMARIES_ENDPOINT}/abc/')

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_delete_summary_zero_id(test_app_with_db):
    response = test_app_with_db.delete(f'{SUMMARIES_ENDPOINT}/0/')

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'


@pytest.mark.negative
def test_delete_nonexistent_summary(test_app_with_db):
    response = test_app_with_db.delete(f'{SUMMARIES_ENDPOINT}/9999999/')

    assert response.status_code == 404, f'Invalid response code: {response.status_code}'
    assert response.json().get(ERROR_DETAIL_FIELD), 'Details about the error are not provided'
