import json
import os

import rest_framework.exceptions as rest_exceptions

import application_logic.simplification.simplification_pipeline as simplification
import application_logic.textprocessing.input_processor as input_processor
from restapi_simplification.apps import T5ModelLoad


def get_simplified_text(text, model_name, model_options):
    try:
        preload = None
        if model_name == "T5":
            preload = T5ModelLoad.model_name, T5ModelLoad.model, T5ModelLoad.tokenizer

        simplification_pipeline = simplification.SimplificationPipeline(model_name, model_options, preload)
    except ValueError:
        raise rest_exceptions.ParseError("Invalid model_name provided")
    except Exception:
        raise rest_exceptions.APIException("Something went wrong while loading model")

    try:
        simplified_text = simplification_pipeline.simplify(text)
    except Exception:
        raise rest_exceptions.APIException("Something went wrong while simplifying text")

    return simplified_text


def validate_request(request, input_type):
    if input_type == "file":
        data = request.FILES.get('file')
        options_data = request.data.get("json")
        if options_data is None:
            raise rest_exceptions.ParseError("No json found in request")

        try:
            data_json = json.loads(options_data)
        except Exception:
            raise rest_exceptions.ParseError("Invalid options json input")

        options = data_json.get("options")
        file_type = os.path.splitext(str(data))[1]
    else:
        data = request.data.get("text")
        options = request.data.get("options")
        file_type = None

    text = parse_data(data, input_type, file_type)

    if options is None:
        raise rest_exceptions.ParseError("No options field provided")

    model_name = options.get("model_name")
    if model_name is None:
        raise rest_exceptions.ParseError("No model_name field provided")

    model_options = options.get("model_options")
    if model_options is None:
        return text, model_name, None

    validate_options(model_options, model_name)
    return text, model_name, model_options


def validate_options(options, model_name):
    all_models = simplification.get_models()
    for model in all_models:
        if model_name != model.get("model_name"):
            continue

        correct_options = model.get("options")
        correct_options_names = [option.get("option_name") for option in correct_options]
        for option in options:
            if option not in correct_options_names:
                raise rest_exceptions.ParseError("Invalid option name provided: " + option)
        return True

    raise rest_exceptions.ParseError("Invalid model_name provided: " + model_name)


def parse_data(data, input_type, file_type=None):
    if input_type == "file":
        if data is None or file_type not in input_processor.get_supported_files():
            raise rest_exceptions.ParseError("No file found in request")

        try:
            text = input_processor.InputProcessor(file_type).to_str(data)
        except Exception:
            raise rest_exceptions.ParseError("Something went wrong while parsing file input")

        return text
    elif input_type == "json":
        if data is None:
            raise rest_exceptions.ParseError("No text found in request")

        return data
