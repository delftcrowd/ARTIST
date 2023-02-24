from drf_yasg import openapi
from rest_framework import status

model_options_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    description='List of model options which have been used to do the simplification.',
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
            'option_value': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the value of the option',
                example='1'
                        '300'),
        },
        description='JSON object containing the name, type and value of the model option.'),
)

model_info_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'model_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='A string of the name of the model which can be to simplify the text.'),
        'model_options': model_options_schema,
    }
)

request_schema_post_simplification = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=
    {
        'unsimplified_text': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='String of the text to be used for simplification.',
            example='Unsimplified text.'),
        'simplified_by_model': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='String of the text which is the output of the model.',
            example='Simplified text by model.'),
        'simplified_by_user': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='String of the text which has been corrected by the user.',
            example='Correct simplified text.'),
        'model_info': model_info_schema,
    },
    description='The data in the request body will be posted to the database.')

request_schema_post_feedback = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=
    {
        'unsimplified_text': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='String of the text to be used for simplification.',
            example='Unsimplified text.'),
        'simplified_by_model': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='String of the text which is the output of the model.',
            example='Simplified text by model.'),
        'simplified_by_user': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='String of the text which has been corrected by the user.',
            example='Correct simplified text.'),
        'rating_simplification': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='A rating of the given simplification. The rating is an integer between 1 and 5.',
            example=5),
        'comments': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Textual comments about the given simplification and difficult sentences.',
            example='The simplified text and analysis of difficult sentences is great!'),
        'model_info': model_info_schema,
        'difficult_sentences_original': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='List of difficult sentences in the original text.',
            items=openapi.Schema(type=openapi.TYPE_STRING, example='This is a simple sentence.')),
        'difficult_sentences_simplified': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='List of difficult sentences in the simplified text.',
            items=openapi.Schema(type=openapi.TYPE_STRING, example='This is a difficult sentence.')),
        'rating_sentences': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='A rating of the given difficult sentences. The rating is an integer between 1 and 5.',
            example=5),
        'metric_options': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=
            {
                'metric_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='A string of the name of the metric which was used',
                    example='FleschDouma'),
            })
    },
    description='The data in the request body will be posted to the database.')

response_schema_post_feedback = {
    status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_STRING, example="Success."),
}
response_schema_post_simplification = {
    status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_STRING, example="Success."),
}
response_schema_get = {
    status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_STRING, example="Online."),
}
