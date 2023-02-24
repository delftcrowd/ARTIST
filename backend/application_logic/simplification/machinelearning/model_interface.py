class ModelInterface:
    def __init__(self):
        self.model_name = ""
        self.model = None

    def simplify(self, text: str) -> str:
        raise NotImplementedError

    def get_option(self) -> dict:
        return NotImplementedError

    def set_option(self, options: dict):
        raise NotImplementedError

    def get_model_name(self) -> str:
        return self.model_name
