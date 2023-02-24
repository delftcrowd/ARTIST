import restapi_database.apps as apps

class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response[
            "Access-Control-Allow-Headers"] = \
            "Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, " \
            "Access-Control-Request-Method, Access-Control-Request-Headers, Authorization"
        response["Access-Control-Allow-Credentials"] = True
        response["Access-Control-Allow-Methods"] = "GET, DELETE, PUT, OPTIONS, POST"
        response["Access-Control-Allow-Origin"] = apps.RestapiConfig.CORS_URL

        return response
