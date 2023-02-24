from drf_yasg import openapi
from rest_framework import status

max_length_original_description = "Controls the maximum length of the original text that the model will accept. The " \
                                  "original text will be truncated if it is longer than this value. The default value" \
                                  " is 512. "
max_length_sum_description = "Controls the maximum length of the simplified text that the model will accept. The " \
                             "simplified text will be truncated if it is longer than this value. The default value is " \
                             "0.9. Input can range from 0 to 1 "
min_length_sum_description = "Controls the minimum length of the simplified text that the model will accept. The " \
                             "simplified text will be truncated if it is shorter than this value. The default value " \
                             "is 0.1. Input can range from 0 to 1 "
model_name_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description='A string of the name of the model '
                'which was used to simplify the text.')
simplified_text_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description='A string of simplified text.')
original_text_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description='A string of the text which is a result of parsing the file input.')
operation_description_simplification_post = "Note: The model options in this API documentation are specifically for " \
                                            "the T5 model. The model_options have to be adapted when using other " \
                                            "model. The name and description of specific model_options are generated " \
                                            "the OPTIONS request. "

model_options_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=
    {
        'model_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='String of the name of the model to be used for simplification.',
            example='T5'),
        'model_options': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=
            {
                'max_length_original': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description=max_length_original_description,
                    example=512),
                'max_length_sum': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description=max_length_sum_description,
                    example=0.9),
                'min_length_sum': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description=min_length_sum_description,
                    example=0.1),
            }),
    },
    description='JSON object containing the supported model_name and model_options.')

request_schema_post = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'text': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='A string of text which will be simplified.'),
        'options': model_options_schema
    },
    required=['text'],
    description='JSON object containing the text to be simplified and the model options to be used for '
                'simplification.',
)

response_schema_post = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'model_name': model_name_schema,
            'simplified_text': simplified_text_schema,
        },
        description='Returns a JSON object containing the name of the model which was used to simplify the text and '
                    'the simplified text.',
    ),
}

request_schema_post_file = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'options': model_options_schema
    },
    description='JSON object containing the model options to be used for simplification.',
    required=['']
)

response_schema_post_file = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'model_name': model_name_schema,
            'simplified_text': simplified_text_schema,
            'original_text': original_text_schema,
        }
    ),
}

model_options_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    description='List of JSON objects containing the supported model_name and '
                'model_options.',
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=
        {
            'option_name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the name of the option',
                example='max_length_original'),
            'option_type': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the type of the option',
                example='float'),
            'option_description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the description of the option',
                example='Controls the maximum length of the original text that the model will accept. The '
                        'original text will be truncated if it is longer than this value. The default value is 512.'),
        },
        description='JSON object containing the name, type and description of the model option.'),
)
supported_file_types_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_STRING),
    example=['.txt', '.pdf', '.docx', '.doc', '.epub'],
    description='An array of strings containing the supported file types.')

response_schema_options = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'simplification_options': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'model_name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='A string of the name of the model which can be to simplify the text.'),
                        'model_options': model_options_schema,
                        'supported_file_types': supported_file_types_schema,
                    }
                )),
        })}
