import rest_framework.exceptions as rest_exceptions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

import application_logic.readability.metrics_factory as metrics_factory
import restapi_readability.api_documentation as docs
import restapi_readability.request_parser as request_parser


@swagger_auto_schema(
    method='get',
    responses=docs.response_schema_options)
@api_view(['GET'])
def get_options(request):
    metrics_options = metrics_factory.get_options()

    response = {
        "metric_options": metrics_options,
    }

    return Response(response)


@swagger_auto_schema(
    method='post',
    request_body=docs.request_schema_readability_post,
    responses=docs.response_schema_readbilility_post)
@api_view(['POST'])
def readability_post(request):
    text, metric_name = request_parser.validate_request(request)

    try:
        metric = metrics_factory.MetricsFactory(metric_name, text)
        description = metric.get_description()
        min_age = metric.get_min_age()
    except Exception:
        raise rest_exceptions.APIException("Something went wrong while measuring readability")

    response = {
        "metric_name": metric_name,
        "description": description,
        "min_age": min_age
    }

    return Response(response)


@swagger_auto_schema(
    method='post',
    request_body=docs.request_schema_difficult_sentences_post,
    responses=docs.response_schema_difficult_sentences_post)
@api_view(['POST'])
def difficult_sentences_post(request):
    text, metric_name = request_parser.validate_request(request)

    try:
        metric_factory = metrics_factory.MetricsFactory(metric_name, text, difficult_sentence=True)
        description = metric_factory.get_description()
        difficult_sentences = metric_factory.get_difficult_sentences()
    except ValueError:
        raise rest_exceptions.APIException("Difficult sentences not implemented for this metric")
    except Exception:
        raise rest_exceptions.APIException("Something went wrong while calculating difficult sentences")

    response = {
        "metric_name": metric_name,
        "description": description,
        "difficult_sentences": difficult_sentences
    }

    return Response(response)
