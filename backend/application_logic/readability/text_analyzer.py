"""
The text analyzer used for all the readability metrics.
"""
from __future__ import division

import os
import re

import nltk
import pyphen
from nltk.tokenize import sent_tokenize

nltk.download('punkt')


# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore", category=PendingDeprecationWarning, message='Deprecated imp module in favour of importlib.*')
#     warnings.filterwarnings("ignore", category=ImportWarning, message='Directory.*ndg.* not imported')
#     warnings.filterwarnings("ignore", category=ImportWarning, message='Directory.*mpl_toolkits.* not imported')


class TextAnalyzer:
    def __init__(self, text, locale='en_GB'):
        self.set_text(text)
        self.locale = locale
        self.set_locale(locale)
        self.sentences = []
        self.simple_words = []
        self.min_age = 0
        self.scores = {
            'sentence_count': 0,  # nr of sentences
            'word_count': 0,  # nr of words
            'letter_count': 0,  # nr of characters in words (no spaces)
            'syll_count': 0,  # nr of syllables
            'polysyllword_count': 0,  # nr of words with more than 2 syllables
            'simpleword_count': 0,  # nr of simplewords (depends on provided list)
            'sentence_len_average': 0,  # words per sentence
            'word_len_average': 0,  # syllables per word
            'wordletter_average': 0,  # letters per word
            'wordsent_average': 0  # sentences per word
        }
        self.re_words = re.compile(r'\w+', flags=re.UNICODE)

    def set_text(self, text):
        """
        Sets the text
        """
        self.text = text

    def set_locale(self, locale):
        """
        Sets locale-related data.
        :param locale: locale of data eg: 'nl_NL'
        """
        if os.path.exists(locale):
            self.hyphenator = pyphen.Pyphen(filename=locale)
        elif len(locale) > 1 and locale in pyphen.LANGUAGES:
            self.hyphenator = pyphen.Pyphen(lang=locale)
            self.set_tokenize_language(locale)
        else:
            raise LookupError("provided locale not supported by pyphen")

    def set_tokenize_language(self, locale):
        """
        Set the language NLTK's sent_tokenize uses.
        Based on local available punkt tokenizers.
        This is done in the init, but can also be changed by calling this.
        :param locale: locale of data eg: 'nl_NL'
        """
        self.tokenize_language = self.__get_tokenize_language(locale[:2])

    def set_text_scores(self):
        """
        Wrapper for setting all the scores.
        """
        self.set_sentences()
        self.parse_sentences()
        self.set_averages()

    def set_sentences(self):
        """
        Tokenize the sentences from the text. Depending on the locale,
        a custom tokenize language may be used if available.
        """
        try:
            self.sentences = sent_tokenize(self.text, language=self.tokenize_language)
        except LookupError:
            # maybe custom tokenize language not available on fs, do default
            self.sentences = sent_tokenize(self.text, language="english")

        self.scores['sentence_count'] = len(self.sentences)

    def parse_sentences(self):
        """
        Parse each sentence and each word, and count the individual countable scores.
        """
        for s in self.sentences:
            words = self.re_words.findall(s)
            self.scores['word_count'] += len(words)

            for w in words:
                syllables_count = self.hyphenator.inserted(w).count('-') + 1
                self.scores['syll_count'] += syllables_count
                self.scores['letter_count'] += len(w)

                if syllables_count > 2:
                    self.scores['polysyllword_count'] += 1

                if self.simple_words:
                    if w.lower() in self.simple_words:
                        self.scores['simpleword_count'] += 1

    def set_averages(self):
        """
        Sets all relevant averages based on the
        individual counts.
        """
        if self.scores['sentence_count'] > 0:
            self.scores['sentence_len_average'] = self.scores['word_count'] / self.scores['sentence_count']

        if self.scores['word_count'] > 0:
            self.scores['word_len_average'] = self.scores['syll_count'] / self.scores['word_count']
            self.scores['wordletter_average'] = self.scores['letter_count'] / self.scores['word_count']
            self.scores['wordsent_average'] = self.scores['sentence_count'] / self.scores['word_count']

    def __get_tokenize_language(self, locale_lookup):
        """
        Try to find a value for provided locale key.
        Return "english" by default.
        :param locale_lookup: locale of data eg: 'nl_NL'
        """
        lookup_value = "english"
        lookup = {
            "en": "english",
            "nl": "dutch"
        }

        if locale_lookup in lookup:
            lookup_value = lookup[locale_lookup]

        return lookup_value
