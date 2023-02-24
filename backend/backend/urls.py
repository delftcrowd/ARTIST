from django.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "readability",
                "description": "API documentation for /readability endpoints. GET request to /readability/options "
                               "returns metric_options which contains the list of available metrics for measuring of "
                               "readability and calculating difficult sentences which /readability endpoints can "
                               "consume.",
            },
            {
                "name": "simplification",
                "description": "API documentation for /simplification endpoints. GET request to "
                               "/simplification/options "
                               "returns simplification_options and supported_file_types which /simplification "
                               "endpoints can consume."
            },
            {
                "name": "validated-samples",
                "description": "API documentation for /validated-samples endpoints. These endpoints can be used to "
                               "post data to the database. "
            },
        ]

        return swagger


schema_view = get_schema_view(
    openapi.Info(
        title="ARTIST API",
        default_version='v1',
        description="API for project artist",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
    generator_class=CustomOpenAPISchemaGenerator
)
urlpatterns = [
    path("api/readability/", include("restapi_readability.urls")),
    path("api/simplification/", include("restapi_simplification.urls")),
    path("api/validated-samples/", include("restapi_database.urls")),
    re_path(r'^docs/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
