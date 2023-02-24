from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

import application_logic.simplification.simplification_pipeline as simplification
import application_logic.textprocessing.input_processor as input_processor
import restapi_simplification.api_documentation as docs
import restapi_simplification.request_parser as request_parser


@swagger_auto_schema(
    method="post",
    request_body=docs.request_schema_post,
    responses=docs.response_schema_post,
    operation_description=docs.operation_description_simplification_post,
)
@api_view(["POST"])
def post(request):
    text, model_name, model_options = request_parser.validate_request(
        request, input_type="json"
    )

    simplified_text = request_parser.get_simplified_text(
        text, model_name, model_options
    )
    response = {"model_name": model_name, "simplified_text": simplified_text}

    return Response(response)


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            description="File which needs to be parsed and simplified.",
            type=openapi.TYPE_FILE,
        ),
        openapi.Parameter(
            name="json",
            in_=openapi.IN_FORM,
            description="JSON object containing the model_name and model_options. It adheres to the same "
            "exact structure as the options object in the regular "
            "/simplification POST request.",
            type=openapi.TYPE_OBJECT,
        ),
    ],
    responses=docs.response_schema_post_file,
)
@api_view(["POST"])
@parser_classes([MultiPartParser])
def file_post(request):
    text, model_name, model_options = request_parser.validate_request(
        request, input_type="file"
    )

    simplified_text = request_parser.get_simplified_text(
        text, model_name, model_options
    )
    response = {
        "model_name": model_name,
        "simplified_text": simplified_text,
        "original_text": text,
    }

    return Response(response)


@swagger_auto_schema(method="get", responses=docs.response_schema_options)
@api_view(["GET"])
def get_options(request):
    response = {
        "simplification_options": [simplification.get_models()],
        "supported_file_types": input_processor.get_supported_files(),
    }

    return Response(response)
