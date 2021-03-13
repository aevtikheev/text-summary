"""Tests for /summaries/ resource."""
import json

import pytest


def test_create_summary(test_app_with_db):
    """
    Create new summary.

    Check that status code is 201 and url field of the response is correct.
    """
    summary_url = 'http://example.com'
    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': summary_url}))

    assert response.status_code == 201, f'Invalid response code: {response.status_code}'
    assert response.json()['url'] == summary_url, f'Invalid summary URL: {response.json()["url"]}'


@pytest.mark.negative
def test_create_summary_empty_payload(test_app_with_db):
    """
    Try to create summary with empty payload.

    Check that status code is 422 and error message says that url field is required.
    """
    response = test_app_with_db.post('/summaries/', data=json.dumps({}))

    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json() == {
        'detail': [
            {
                'loc': ['body', 'url'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }
        ]
    }, 'Invalid error message'


def test_read_summary(test_app_with_db, existing_summary):
    """
    Get the summary by ID.

    Check that status code is 200, id and url fields are correct
     and summary and created_at fields are present.
    """
    summary_id, summary_url = existing_summary

    response = test_app_with_db.get(f'/summaries/{summary_id}/')
    assert response.status_code == 200, f'Invalid response code: {response.status_code}'

    response_json = response.json()
    assert response_json['id'] == summary_id, f'Invalid id field: {response_json["id"]}'
    assert response_json['url'] == summary_url, f'Invalid url field: {response_json["url"]}'
    assert response_json['summary'], 'Missing summary field'
    assert response_json['created_at'], 'Missing created_at field'


@pytest.mark.negative
def test_read_nonexistent_summary(test_app_with_db):
    """
    Try to get a summary by nonexistent ID.

    Check that status code is 404 and error details are provided.
    """
    response = test_app_with_db.get('/summaries/9999999/')
    assert response.status_code == 404, f'Invalid response code: {response.status_code}'
    assert response.json()["detail"], 'Details about the error are not provided'


@pytest.mark.negative
def test_read_invalid_id_summary(test_app_with_db):
    """
    Try to get a summary by invalid ID.

    Check that status code is 422 and error details are provided.
    """
    response = test_app_with_db.get('/summaries/abc/')
    assert response.status_code == 422, f'Invalid response code: {response.status_code}'
    assert response.json()["detail"], 'Details about the error are not provided'


def test_read_all_summaries(test_app_with_db, existing_summary):
    """
    Get all summaries.

    Check that status code is 200 and existing summary is present in the list.
    """
    summary_id, summary_url = existing_summary

    response = test_app_with_db.get('/summaries/')
    assert response.status_code == 200, f'Invalid response code: {response.status_code}'

    response_json = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_json))) == 1, (
        'Existing summary is not present in the result.'
    )


def test_delete_summary(test_app_with_db, existing_summary):
    """
    Delete summary.

    Check that status code is 200.
    """
    summary_id, summary_url = existing_summary

    response = test_app_with_db.delete(f'/summaries/{summary_id}/')
    assert response.status_code == 200, f'Invalid response code: {response.status_code}'


@pytest.mark.negative
def test_delete_nonexistent_summary(test_app_with_db):
    """
    Try to delete a summary by nonexistent ID.

    Check that status code is 404 and error details are provided.
    """
    response = test_app_with_db.delete('/summaries/9999999/')
    assert response.status_code == 404, f'Invalid response code: {response.status_code}'
    assert response.json()["detail"], 'Details about the error are not provided'
