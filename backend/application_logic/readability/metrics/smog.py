"""
SMOG Readability Metric
"""
from __future__ import division

from application_logic.readability.common import get_minimum_age_from_us_grade
from application_logic.readability.text_analyzer import TextAnalyzer


class SMOG(TextAnalyzer):
    """
    SMOG Class
    """
    def __init__(self, text, locale='nl_NL'):
        TextAnalyzer.__init__(self, text, locale)
        self.set_text_scores()
        self.us_grade = 0
        self.set_grade()
        self.min_age = get_minimum_age_from_us_grade(self.us_grade)

    def set_text_scores(self):
        """
        SMOG custom wrapper for setting all the scores.
        """
        self.set_sentences()
        if self.scores["sentence_count"] >= 30:
            sentence_middle = int(self.scores["sentence_count"] / 2)
            self.sentences = self.sentences[:10] + \
                             self.sentences[sentence_middle - 5:5 + sentence_middle] + \
                             self.sentences[-10:]
            self.scores["sentence_count"] = len(self.sentences)
        self.parse_sentences()
        self.set_averages()

    def set_grade(self):
        """
        Calculates US grade as a float from the available
        text scores.
        """
        if self.scores['sentence_count'] != 0:
            self.us_grade = (1.043 * (
                    (self.scores['polysyllword_count'] * (30 / self.scores['sentence_count'])) ** 0.5)) + 3.1291


def get_name():
    """
    Getter name
    """
    return "SMOG"


def get_description(locale):
    """
    Getter description
    """
    if locale == 'nl_NL':
        return "Smog meet hoeveel jaar onderwijs de gemiddelde persoon moet zijn afgestudeerd " \
               "om de tekst te begrijpen. Aan u weergegeven is de minimumleeftijd, die in " \
               "kaart wordt gebracht in overeenstemming met de cijfer berekend door SMOG, daarom " \
               "is de maximaal mogelijke leeftijd 24 die overeenkomt met afstuderen met een " \
               "masterdiploma."

    return "SMOG measures how many years of education the average person needs to have " \
           "graduated in order to understand the text. Displayed to you is the minimum " \
           "age, which is mapped in accordance to the grade calculated by SMOG, " \
           "therefore the maximum possible age is 24 which corresponds to graduating with " \
           "a Masters degree."
