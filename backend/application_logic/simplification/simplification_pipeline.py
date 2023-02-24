from application_logic.simplification.machinelearning.t5 import T5
import re


class SimplificationPipeline(object):
    def __init__(self, model_type, options=None, preload=False):
        self.model_type = model_type
        self.model = None
        if model_type == "T5":
            if not preload:
                self.model = T5(options)
            else:
                self.model = T5(options, preload)
        else:
            raise ValueError("Model type not supported")

    def simplify(self, text):
        test_data = self.model.simplify(text)
        test_data = re.sub("([\<]).*?([\>])", "\g<1>\g<2>", test_data)
        test_data = re.sub("[\<].*?[\>]", "", test_data)
        test_data = test_data.strip()
        return test_data

    def get_model_name(self) -> str:
        return self.model.get_model_name()

    def get_model_option(self) -> dict:
        return self.model.get_option()

    def simplify_with_options(self, text, options) -> str:
        og_option = self.model.get_option()
        self.model.set_option(options)

        str_sim = self.model.simplify(text)
        self.model.set_option(og_option)

        return str_sim

def get_models():
    models = [{
        "model_name": "T5",
        "options": [
            {
                "option_name": "max_length_original",
                "option_type": "float",
                "option_description": "Controls the maximum length of the original text that the model "
                                      "will "
                                      "accept. The original text will be truncated if it is longer than "
                                      "this value. The default value is 512.",
            },
            {
                "option_name": "max_length_sum",
                "option_type": "float",
                "option_description": "Controls the maximum length of the simplified text that the model "
                                      "will accept. The simplified text will be truncated if it is longer "
                                      "than this value. The default value is 0.9. "
                                      "Input can range from 0 to 1",
            },
            {
                "option_name": "min_length_sum",
                "option_type": "float",
                "option_description": "Controls the minimum length of the simplified text that the model "
                                      "will accept. The simplified text will be truncated if it is "
                                      "shorter than this value. The default value is 0.1. "
                                      "Input can range from 0 to 1",
            }
        ],
    }]

    return models
