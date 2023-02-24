from drf_yasg import openapi
from rest_framework import status

flesch_douma_description = "The Flesch Reading Ease reading index ranges from 0 to 100. You should aim for a " \
                           "60+ score minimum. The minimum age should be as small as possible, indicating what " \
                           "age groups should be able to understand the text. The age is strongly correlated to " \
                           "the grade system, therefore the maximum possible age is 24 which corresponds to " \
                           "graduating with a Masters degree."
spache_description = "This metric calculates the hard sentences of a text in accordance to the frequency of words in " \
                     "the given language and their number of syllables. Therefore, if a sentence contains more than a " \
                     "given threshold of difficult/low frequent words, it is considered difficult."

request_schema_readability_post = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'text': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='A string of text which will be analysed for readability.',
            example='This is a simple sentence.'),
        'options': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'metric_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='A string of the name of the metric which will be used to '
                                'analyse the text.',
                    example='FleschDouma'),
            }),
    },
    description='The text will be analysed for readability using the metric specified in the options.',
    required=['text']
)

response_schema_readbilility_post = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'metric_name': openapi.Schema(type=openapi.TYPE_STRING,
                                          description='A string of the name of the metric which was used to calculate '
                                                      'difficult '
                                                      'sentences.',
                                          example='FleschDouma'),
            'metric_description': openapi.Schema(type=openapi.TYPE_STRING,
                                                 description='A string of the description of the metric which was '
                                                             'used to calculate '
                                                             'the difficult sentences.',
                                                 example=flesch_douma_description),
            'min_age': openapi.Schema(type=openapi.TYPE_INTEGER,
                                      description='Minimum age to read the text in years, '
                                                  'ranges from 6 to 24',
                                      example=12),
        },
        description='The text was analysed for readability using the metric specified in the options.',
    ),
}

request_schema_difficult_sentences_post = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'text': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='A string of text which will be analyzed.',
            example='This is a sentence.'),
        'options': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'metric_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='A string of the metric name to be used for analysing the text.',
                    example='Spache'),
            }),
    },
    description='The text will be analysed for difficult sentences using the metric specified in the options.',
    required=['text']
)

response_schema_difficult_sentences_post = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'metric_name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the name of the metric which was used to calculate '
                            'difficult sentences.',
                example='Spache'),
            'metric_description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the description of the metric which was used to calculate the difficult '
                            'sentences.',
                example=spache_description),
            'difficult_sentences': openapi.Schema(
                type=openapi.TYPE_ARRAY, description='Array containing difficult sentences',
                items=openapi.Schema(type=openapi.TYPE_STRING,
                                     description='difficult sentence'),
                example=['This is an easy sentence.']),
        },
        description='The response contains the metric name, metric description and an array of difficult sentences.'
    ),
}

supported_metrics_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=
        {
            'metric_name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the name of the model',
                example='FleschDouma'),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='A string of the description of the model',
                example=flesch_douma_description),
        }))

response_schema_options = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'metric_options': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'difficult_sentences': supported_metrics_schema,
                    'readability_measures': supported_metrics_schema,
                }),
        },
        description='The response contains the supported metrics for difficult sentences and readability measures.',
    )}
