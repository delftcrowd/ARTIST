# class used by each metric test
class MetricTest():
    def __init__(self, min_test_age):
        self.text = "Readability is the ease with which a reader can understand a written text. In natural language, " \
                    "the readability of text depends on its content (the complexity of its vocabulary and syntax)."
        self.text_nl = "Leesbaarheid is het gemak waarmee een lezer een geschreven tekst kan begrijpen. In de " \
                       "natuurlijke taal hangt de leesbaarheid van tekst af van de inhoud ervan (de complexiteit van " \
                       "zijn vocabulaire en syntaxis)."
        self.min_age_test = min_test_age
        self.test_range = [self.min_age_test, self.min_age_test + 1, self.min_age_test - 1]
        self.test_range_fail_text = "min_age is not within 1 year range of " + str(self.min_age_test)
