import pytest
from rest_framework import status

from restapi_readability.tests.setup import hard_text, simple_text, url_sentences as url, description_spache


@pytest.mark.API
def test_hard_spache(client):
    request_data = {
        "text": hard_text,
        "options":
            {
                "metric_name": "Spache"
            }
    }

    correct_response_data = {
        "metric_name": "Spache",
        "description": description_spache,
        "difficult_sentences": [
            "Wij doen u een formulier toekomen waarop u dient aan te geven hoeveel u vorig jaar hebt verdiend met uw "
            "inmiddels failliete bedrijf."
        ]
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == correct_response_data


@pytest.mark.API
def test_simple_spache(client):
    request_data = {
        "text": simple_text,
        "options":
            {
                "metric_name": "Spache"
            }
    }

    correct_response_data = {
        "metric_name": "Spache",
        "description": description_spache,
        "difficult_sentences": []
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == correct_response_data


@pytest.mark.API
def test_no_text(client):
    request_data = {
        "options":
            {
                "metric_name": "SMOG"
            }
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
        "text": "Wij doen u een formulier toekomen waarop u dient aan te geven hoeveel u vorig jaar hebt verdiend met uw inmiddels failliete bedrijf."
    }

    correct_response_data = {
        "detail": "No options field provided"
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_no_metric_name(client):
    request_data = {
        "text": "Wij doen u een formulier toekomen waarop u dient aan te geven hoeveel u vorig jaar hebt verdiend met uw inmiddels failliete bedrijf.",
        "options":
            {
            }
    }

    correct_response_data = {
        "detail": "No metric_name field provided"
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data


@pytest.mark.API
def test_no_metric_name(client):
    request_data = {
        "text": "Wij doen u een formulier toekomen waarop u dient aan te geven hoeveel u vorig jaar hebt verdiend met uw inmiddels failliete bedrijf.",
        "options":
            {
                "metric_name": "invalid_metric_name"
            }
    }

    correct_response_data = {
        "detail": "Invalid metric name provided: invalid_metric_name"
    }
    response = client.post(url, request_data, content_type="application/json", format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == correct_response_data
