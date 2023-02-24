import configparser
import os

from django.apps import AppConfig
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class RestapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restapi_simplification'

    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        API = config["API"]
        CORS_URL = API["CORS_URL"]
    except Exception as e:
        print(e)
        CORS_URL = "http://localhost:8080"
    CORS_URL = os.getenv("CORS_URL", CORS_URL)


class T5ModelLoad(AppConfig):
    model_name = "yhavinga/t5-v1.1-base-dutch-cnn-test"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
