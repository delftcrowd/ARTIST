"""
The KPC readability metric
Makes use of the AVI Lelevs.
https://dutchowl.nl/reading/avi-levels/
"""
from __future__ import division

from application_logic.readability.text_analyzer import TextAnalyzer


class KPC(TextAnalyzer):
    """
    KPC Class
    """
    def __init__(self, text, locale='nl_NL'):
        TextAnalyzer.__init__(self, text, locale)
        self.set_text_scores()
        self.avi = 0
        self.reading_index = 0
        self.set_reading_index()
        self.set_avi()
        self.set_minimum_age()

    def set_reading_index(self):
        """
        Calculates reading index required for AVI calculation.
        """
        self.reading_index = 192 - (2 * self.scores['sentence_len_average']) - \
                             (200 / 3 * self.scores['word_len_average'])

    def set_avi(self):
        """
        Calculates AVI level using the old KPC method.
        """
        readingindex = round(self.reading_index)

        if readingindex > 127:
            self.avi = 0
        elif 127 >= readingindex >= 123:
            self.avi = 1
        elif 123 >= readingindex >= 112:
            self.avi = 2
        elif 120 >= readingindex >= 108 \
                and self.scores['word_len_average'] >= 1.10:
            self.avi = 3
        elif 110 >= readingindex >= 100 \
                and self.scores['word_len_average'] >= 1.15:
            self.avi = 4
        elif 99 >= readingindex >= 94:
            self.avi = 5
        else:
            avi = 5
            max_index = 98
            i = 1
            while not self.avi:
                max_index = max_index - 5
                min_index = max_index - 4

                if max_index >= readingindex >= min_index:
                    self.avi = avi + i

                i = i + 1

    def set_minimum_age(self):
        """
        Sets minimum age required for reading a text based
        on set AVI score.  The calculation is based roughly on
        the documentation.
        """
        if self.avi == 0:
            self.min_age = 0
        elif self.avi < 8:
            self.min_age = int(round((self.avi / 3) + 6))
        else:
            self.min_age = int(round((self.avi / 2) + 5))


def get_name():
    """
    Getter name
    """
    return 'KPC'


def get_description(locale):
    """
    Getter description
    """
    if locale == 'nl_NL':
        return "De AVI-niveaus richten zich op technische vaardigheden in plaats van begrijpend " \
               "lezen. Ze gaan over de mogelijkheid om vloeiend en feilloos woorden en zinnen te " \
               "lezen. Hoe hoger het niveau, hoe meer complexe woorden en langere zinnen. " \
               "Voor u wordt het de minimumleeftijd weergegeven die de lezer moet hebben om de " \
               "gegeven tekst te begrijpen. Dit wordt berekend in overeenstemming met de " \
               "AVI -niveaus berekend door KPC, daarom is de maximale mogelijke leeftijd 24 " \
               "die overeenkomt met afstuderen met een master."

    return "The AVI levels focus on technical skills rather than reading comprehension. " \
           "They represent the ability to fluently and flawlessly read words and sentences. " \
           "The higher the level, the more complex words and longer sentences. " \
           "To you it is displayed the minimum age the reader needs to have in order to " \
           "understand the given text. This is calculated in accordance to the AVI levels " \
           "calculated by KPC, therefore the maximum possible age is 24 which corresponds to " \
           "graduating with a Masters degree."
