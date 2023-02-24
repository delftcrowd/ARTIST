import rest_framework.exceptions as rest_exceptions

import application_logic.readability.metrics_factory as metrics_factory


def validate_request(request):
    text = request.data.get("text")
    if text is None:
        raise rest_exceptions.ParseError("No text found in request")

    options = request.data.get("options")
    if options is None:
        raise rest_exceptions.ParseError("No options field provided")

    metric_name = options.get("metric_name")
    if metric_name is None:
        raise rest_exceptions.ParseError("No metric_name field provided")

    if metric_name not in metrics_factory.get_names():
        raise rest_exceptions.ParseError("Invalid metric name provided: " + metric_name)

    return text, metric_name


