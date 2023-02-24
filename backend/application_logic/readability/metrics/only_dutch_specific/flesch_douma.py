"""
The Flesch-Douma readability metric
Calculates the readability score of a text using the Flesch-Douma index.
http://www.kennislink.nl/publicaties/hoe-begrijpelijk-is-mijn-tekst
http://hchiemstra.wordpress.com/2011/02/24/is-de-leesbaarheid-van-een-tekst-objectief-te-meten/
"""
from application_logic.readability.text_analyzer import TextAnalyzer


class FleschDouma(TextAnalyzer):
    """
    FD Class
    """
    def __init__(self, text, locale='nl_NL'):
        """
        :param text: text to be used for calculating the metric
        :param locale: locale of text eg: 'nl_NL'
        """
        TextAnalyzer.__init__(self, text, locale)
        self.set_text_scores()
        self.reading_index = 0
        self.set_reading_index()
        self.difficulty = 'hard'
        self.set_minimum_age()

    def set_reading_index(self):
        """
        Setter for the reading index
        """
        self.reading_index = 206.84 - \
                             (0.77 * self.scores['sentence_len_average']) - \
                             (93 * self.scores['word_len_average'])

    def set_minimum_age(self):
        """
        Mapped the textual descriptions of the target groups on to ages. Extrapolated this beyond
        the index of 100.
        """
        if self.reading_index < 30:
            self.min_age = 24
            self.difficulty = "extremely difficult to read"
        elif self.reading_index >= 30 and self.reading_index < 50:
            self.min_age = 18
            self.difficulty = "very difficult to read"
        elif self.reading_index >= 50 and self.reading_index < 60:
            self.min_age = 16
            self.difficulty = "fairly difficult to read"
        elif self.reading_index >= 60 and self.reading_index < 70:
            self.min_age = 12
            self.difficulty = "plain"
        elif self.reading_index >= 70 and self.reading_index < 80:
            self.min_age = 11
            self.difficulty = "fairly easy to read"
        elif self.reading_index >= 80 and self.reading_index < 90:
            self.min_age = 10
            self.difficulty = "easy to read"
        elif self.reading_index >= 90 and self.reading_index < 100:
            self.min_age = 9
            self.difficulty = "very easy to read"
        # extrapolated from this point
        elif self.reading_index >= 100 and self.reading_index < 110:
            self.min_age = 8
            self.difficulty = "extremely easy to read"
        elif self.reading_index >= 110 and self.reading_index < 120:
            self.min_age = 7
            self.difficulty = "extremely easy to read"
        else:
            self.min_age = 6
            self.difficulty = "extremely easy to read"


def get_name():
    """
    Getter for the name of the metric
    """
    return 'FleschDouma'


def get_description(locale):
    """
    Getter for the description of the metric
    """
    if locale == 'nl_NL':
        return "De Leesindex van de Flesch Reading Easy varieert van 0 tot 100. U moet streven " \
               "naar een minimum van 60+ score. De minimumleeftijd moet zo klein mogelijk zijn, " \
               "wat aangeeft welke leeftijdsgroen de tekst moet kunnen begrijpen. De leeftijd " \
               "is sterk gecorreleerd met het kwaliteitssysteem, daarom is de maximale mogelijke " \
               "leeftijd 24 die overeenkomt met afstuderen met een master."

    return "The Flesch Reading Ease reading index ranges from 0 to 100. You should aim for a " \
           "60+ score minimum. The minimum age should be as small as possible, indicating what " \
           "age groups should be able to understand the text. The age is strongly correlated to " \
           "the grade system, therefore the maximum possible age is 24 which corresponds to " \
           "graduating with a Masters degree."
