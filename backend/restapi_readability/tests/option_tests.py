import pytest
from rest_framework import status

from restapi_readability.tests.setup import url_options as url, description_fd, description_kpc, \
    description_fk, description_smog, description_spache


@pytest.mark.API
def test_hard_fd(client):
    correct_response_data = {
        "metric_options": {
            "difficult_sentences": [
                {
                    "metric_name": "Spache",
                    "description": description_spache
                }
            ],
            "readability_measures": [
                {
                    "metric_name": "FleschDouma",
                    "description": description_fd
                },
                {
                    "metric_name": "FleschKincaid",
                    "description": description_fk
                },
                {
                    "metric_name": "KPC",
                    "description": description_kpc
                },
                {
                    "metric_name": "SMOG",
                    "description": description_smog
                }
            ]
        }
    }
    response = client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == correct_response_data
