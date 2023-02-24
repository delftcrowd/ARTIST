from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from . import model_interface


# https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py
class T5(model_interface.ModelInterface):
    def __init__(self, options: dict = None, model_name_loaded=None, tokenizer_loaded=None, model_loaded=None):
        super().__init__()
        if model_name_loaded is None or tokenizer_loaded is None or model_loaded is None:
            self.model_name = "yhavinga/t5-v1.1-base-dutch-cnn-test"
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        else:
            self.model_name = model_name_loaded
            self.model = model_loaded
            self.tokenizer = tokenizer_loaded

        self.max_length_original = 512
        self.max_length_sum = 0.9
        self.min_length_sum = 0.1

        if options is not None:
            max_length_original_option = options.get("max_length_original")
            max_length_sum_option = options.get("max_length_sum")
            min_length_sum_option = options.get("min_length_sum")
            if max_length_original_option is not None:
                self.max_length_original = max_length_original_option
            if max_length_sum_option is not None:
                self.max_length_sum = max_length_sum_option
            if min_length_sum_option is not None:
                self.min_length_sum = min_length_sum_option

    def simplify_list(self, par: list) -> str:

        """Description
        :type self:
        :param self:

        :type par:list:
        :param par:list: List of paragraphs to be simplified

        :raises:

        :rtype: str of simplified text
        """
        summary = ""
        for text in par:
            length_original = len(text.split(" "))
            max_length_sum = int(length_original * self.max_length_sum)
            min_length_sum = int(length_original * self.min_length_sum)

            if max_length_sum <= 2:
                summary += text + "\n"
            elif (self.max_length_original > 0) & (max_length_sum > 0):
                inputs = self.tokenizer.encode(
                    "summarize: " + text,
                    return_tensors="pt",
                    max_length=self.max_length_original,
                    truncation=True,
                )

                summary_ids = self.model.generate(
                    inputs,
                    max_length=max_length_sum,
                    min_length=min_length_sum,
                    length_penalty=5,
                    num_beams=2,
                )

                summary += self.tokenizer.decode(summary_ids[0]) + "\n"

        return summary

    def simplify(self, text: str) -> str:

        """Description
        :type self:
        :param self:

        :type text:str:
        :param text:str: Text to be simplified

        :raises:None

        :rtype: calls the simplify_list function after breaking the text into paragraphs

        """
        # split text into paragraphs
        paragraph_list = text.split("\n\n")
        return self.simplify_list(paragraph_list)

    def get_option(self) -> dict:

        """Description
        :type self:
        :param self:

        :raises:

        :rtype: dict of options that are user configurable and their current values
        """
        return {
            "max_length_original": self.max_length_original,
            "max_length_sum": self.max_length_sum,
            "min_length_sum": self.min_length_sum,
        }

    def set_options(self, options: dict):

        """Description
        :type self:
        :param self:

        :type options:dict:
        :param options:dict: dictionary of options that are user configurable and their new values values

        :raises: value error for invalid values

        :rtype: none
        """
        if options.get("max_length_original") is not None:
            if options.get("max_length_original") > 0  and options.get("max_length_original") < 10000:
                self.max_length_original = options["max_length_original"]
            else:
                raise ValueError("max_length_original must be between 0 and 1000")

        if options.get("max_length_sum") is not None:
            if options.get("max_length_sum") > 0 and options.get("max_length_sum") < 1:
                self.max_length_sum = options["max_length_sum"]
            else:
                raise ValueError("max_length_sum must be between 0 and 1")
        
        if options.get("min_length_sum") is not None:
            if options.get("min_length_sum") > 0 and options.get("min_length_sum") < 1:
                self.min_length_sum = options["min_length_sum"]
            else:
                raise ValueError("min_length_sum must be between 0 and 1")
