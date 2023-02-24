import pytest
from rest_framework import status

from restapi_simplification.tests.setup import url_options as url


@pytest.mark.API
def test_hard_fd(client):
    correct_response_data = {
        "simplification_options": [
            [
                {
                    "model_name": "T5",
                    "options": [
                        {
                            "option_name": "max_length_original",
                            "option_type": "float",
                            "option_description": "Controls the maximum length of the original text that the model "
                                                  "will accept. The original text will be truncated if it is longer "
                                                  "than this value. The default value is 512."
                        },
                        {
                            "option_name": "max_length_sum",
                            "option_type": "float",
                            "option_description": "Controls the maximum length of the simplified text that the model "
                                                  "will accept. The simplified text will be truncated if it is longer "
                                                  "than this value. The default value is 0.9. Input can range from 0 "
                                                  "to 1"
                        },
                        {
                            "option_name": "min_length_sum",
                            "option_type": "float",
                            "option_description": "Controls the minimum length of the simplified text that the model "
                                                  "will accept. The simplified text will be truncated if it is "
                                                  "shorter than this value. The default value is 0.1. Input can range "
                                                  "from 0 to 1"
                        }
                    ]
                }
            ]
        ],
        "supported_file_types": [
            ".txt",
            ".pdf",
            ".epub",
            ".doc",
            ".docx"
        ]
    }
    response = client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == correct_response_data
