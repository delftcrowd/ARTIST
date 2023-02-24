import pytest
from rest_framework import status

from restapi_simplification.tests.setup import original_text, simplified_text, correct_options, \
    invalid_options_option_name, invalid_options_model_name, url_simplification as url


@pytest.mark.API
def test_simplification(client):
    request_data = {
        "text": original_text,
        "options": correct_options

    }

    correct_response_data = {
        "model_name": "T5",
        "simplified_text": simplified_text
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == correct_response_data


@pytest.mark.API
def test_no_text(client):
    request_data = {
        "options": correct_options

    }

    correct_response_data = {
        "detail": "No text found in request"
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_no_options(client):
    request_data = {
        "text": original_text
    }

    correct_response_data = {
        "detail": "No options field provided"
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_invalid_model_name(client):
    request_data = {
        "text": original_text,
        "options": invalid_options_model_name

    }

    correct_response_data = {
        "detail": "Invalid model_name provided: invalid_model_name"
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_invalid_option_name(client):
    request_data = {
        "text": original_text,
        "options": invalid_options_option_name
    }

    correct_response_data = {
        "detail": "Invalid option name provided: invalid_option_name"
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data
