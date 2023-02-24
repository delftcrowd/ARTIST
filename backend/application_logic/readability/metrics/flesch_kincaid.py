"""
The Flesch-Kincaid readability metric
Calculates the readability score of a text using the Flesch-Kincaid Grade Level.
http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_test
"""
from application_logic.readability.common import get_minimum_age_from_us_grade
from application_logic.readability.text_analyzer import TextAnalyzer


class FleschKincaid(TextAnalyzer):
    """
    FK Class
    """
    def __init__(self, text, locale='en_GB'):
        """
        :param text: the text to be used for calculating the metric
        :param locale: the locale of data eg: 'nl_NL'
        """
        TextAnalyzer.__init__(self, text, locale)
        self.set_text_scores()
        self.us_grade = 0
        self.set_grade()
        self.min_age = get_minimum_age_from_us_grade(self.us_grade)
        self.difficulty = 'hard'

    def set_grade(self):
        """
        Calculates US grade as a float from the available text scores.
        """
        self.us_grade = (0.39 * self.scores['sentence_len_average']) + \
                        (11.8 * self.scores['word_len_average']) - 15.59


def get_name():
    """
    Getter for the name of the metric
    """
    return 'FleschKincaid'


def get_description(locale):
    """
    Getter for the description of the metric
    """
    if locale == 'nl_NL':
        return "De Leesindex van de Flesch Reading Easy varieert van 0 tot 100. U moet streven " \
               "naar een minimum van 60+ score. De minimumleeftijd moet zo klein mogelijk zijn, " \
               "wat aangeeft welke leeftijdsgroen de tekst moet kunnen begrijpen. De leeftijd is" \
               " sterk gecorreleerd met het kwaliteitssysteem, daarom is de maximale mogelijke " \
               "leeftijd 24 die overeenkomt met afstuderen met een master."

    return "The Flesch Reading Ease reading index ranges from 0 to 100. You should aim for a 60+ " \
           "score minimum. The minimum age should be as small as possible, indicating what age " \
           "groups should be able to understand the text. The age is strongly correlated to the " \
           "grade system, therefore the maximum possible age is 24 which corresponds to " \
           "graduating with a Masters degree."
