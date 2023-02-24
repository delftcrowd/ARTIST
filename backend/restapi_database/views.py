import json

import rest_framework.exceptions as rest_exceptions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

import application_logic.database.databaseQueries as databaseQueries
import restapi_database.api_documentation as docs


@swagger_auto_schema(
    method='post',
    request_body=docs.request_schema_post_simplification,
    responses=docs.response_schema_post_simplification)
@api_view(['POST'])
def post_simplification(request):
    """
    post is the method that gets called when someone does a post at the specified url from urls.py
    :param request: The request received by the endpoint
    :return: The response
    """
    if request.method == 'POST':
        try:
            json_object = json.loads(str(request.body, encoding='utf-8'))
        except Exception as e:
            raise rest_exceptions.ParseError(detail="Error parsing to json. Error is: " + str(e))

        try:
            if databaseQueries.insert_suggestion_into_db(json_object):
                return Response("Success.")
        except Exception as e:
            raise rest_exceptions.ParseError(detail=str(e))


@swagger_auto_schema(
    method='post',
    request_body=docs.request_schema_post_feedback,
    responses=docs.response_schema_post_feedback)
@api_view(['POST'])
def post_feedback(request):
    """
    post is the method that gets called when someone does a post at the specified url from urls.py
    :param request: The request received by the endpoint
    :return: The response
    """

    try:
        json_object = json.loads(str(request.body, encoding='utf-8'))
    except Exception as e:
        raise rest_exceptions.ParseError(detail="Error parsing to json. Error is: " + str(e))

    try:
        if databaseQueries.insert_feedback_into_db(json_object):
            return Response("Success.")
    except Exception as e:
        raise rest_exceptions.ParseError(detail=str(e))


@swagger_auto_schema(
    method='get',
    responses=docs.response_schema_get)
@api_view(['GET'])
def get(request):
    """
    get is the method that gets called when someone does a get at the specified url from urls.py
    :param request: The request received by the endpoint
    :return: The response
    """
    try:
        return Response(databaseQueries.get_database_status())
    except Exception as e:
        raise rest_exceptions.ParseError(detail=str(e))
