import json

import pytest
from rest_framework import status

from restapi_simplification.tests.setup import original_text, simplified_text, correct_options, docx_path, plain_path, \
    url_simplification_file as url, invalid_options_model_name, invalid_options_option_name


# @pytest.mark.API
# def test_simplification(client):
#     request_json = {
#         "options": correct_options
#     }
#     with open(pdf_path, 'rb') as pdf_file:
#         request_data = {
#             "file": pdf_file,
#             "json": json.dumps(request_json)
#         }
#         response = client.post(url, request_data)
#
#     correct_response_data = {
#         "original_text": original_text,
#         "model_name": "T5",
#         "simplified_text": simplified_text
#     }
#
#     assert response.data == correct_response_data
#     assert response.status_code == status.HTTP_200_OK
#
#
@pytest.mark.API
def test_simplification_docx(client):
    request_json = {
        "options": correct_options
    }
    with open(docx_path, 'rb') as docx_file:
        request_data = {
            "file": docx_file,
            "json": json.dumps(request_json)
        }
        response = client.post(url, request_data)

    correct_response_data = {
        "original_text": original_text,
        "model_name": "T5",
        "simplified_text": simplified_text
    }

    assert response.data == correct_response_data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.API
def test_simplification_txt(client):
    request_json = {
        "options": correct_options
    }
    with open(plain_path, 'rb') as plain_file:
        request_data = {
            "file": plain_file,
            "json": json.dumps(request_json)
        }
        response = client.post(url, request_data)

    correct_response_data = {
        "original_text": original_text,
        "model_name": "T5",
        "simplified_text": simplified_text
    }

    assert response.data == correct_response_data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.API
def test_no_text(client):
    request_json = {
        "options": correct_options
    }
    request_data = {
        "json": json.dumps(request_json)
    }
    response = client.post(url, request_data)

    correct_response_data = {
        "detail": "No file found in request"
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_no_json(client):
    with open(docx_path, 'rb') as docx_file:
        request_data = {
            "file": docx_file,
        }
        response = client.post(url, request_data)

    correct_response_data = {
        "detail": "No json found in request"
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_no_options(client):
    request_json = {}
    with open(plain_path, 'rb') as plain_file:
        request_data = {
            "file": plain_file,
            "json": json.dumps(request_json)
        }
        response = client.post(url, request_data)

    correct_response_data = {
        "detail": "No options field provided"
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_invalid_model_name(client):
    request_json = {
        "options": invalid_options_model_name
    }
    with open(docx_path, 'rb') as docx_file:
        request_data = {
            "file": docx_file,
            "json": json.dumps(request_json)
        }
        response = client.post(url, request_data)

    correct_response_data = {
        "detail": "Invalid model_name provided: invalid_model_name"
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_invalid_option_name(client):
    request_json = {
        "options": invalid_options_option_name
    }
    with open(docx_path, 'rb') as docx_file:
        request_data = {
            "file": docx_file,
            "json": json.dumps(request_json)
        }
        response = client.post(url, request_data)

    correct_response_data = {
        "detail": "Invalid option name provided: invalid_option_name"
    }

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data
