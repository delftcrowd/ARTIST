import configparser
import os
from django.apps import AppConfig


class RestapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restapi_database"

    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        API = config["API"]
        CORS_URL = API["CORS_URL"]
    except Exception as e:
        print(e)
        CORS_URL = "http://localhost:8080"
    CORS_URL = os.getenv("CORS_URL", CORS_URL)
