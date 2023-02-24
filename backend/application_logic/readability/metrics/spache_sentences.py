from __future__ import division

import os

import pyphen
from wordfreq import zipf_frequency

from application_logic.readability.common import syllable_count_english
from application_logic.readability.text_analyzer import TextAnalyzer


class SpacheSentences(TextAnalyzer):
    def __init__(self, text, locale='nl_NL'):
        TextAnalyzer.__init__(self, text, locale)
        self.set_text_scores()
        self.difficult_sentences = self.get_difficult_sentences()

    # RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)
    def get_difficult_sentences(self):
        difficult = []
        for sentence in self.sentences:
            diff_words_per_sentence = []
            total_words = 0
            counter = 0
            for word in sentence[:-1].split(' '):
                total_words = total_words + 1
                freq = zipf_frequency(word, self.locale[:2])
                syllables_count = 0
                if (self.locale[:2] == ' '):
                    syllables_count = syllable_count_english(word)
                else:
                    if os.path.exists(self.locale):
                        hyphenator = pyphen.Pyphen(filename=self.locale)
                    elif len(self.locale) > 1 and self.locale in pyphen.LANGUAGES:
                        hyphenator = pyphen.Pyphen(lang=self.locale)
                    else:
                        raise LookupError("provided locale not supported by pyphen")

                    syllables_count = hyphenator.inserted(word).count('-') + 1
                if (freq <= 3.0 or syllables_count > 3):
                    # word is difficult if more than 3 syllables or the frequency less than 3
                    diff_words_per_sentence.append(word)
                    counter = counter + 1

            # if(counter >= ((total_words - counter) + 2.27) / 3.537):
            if (counter >= 2.068 - (0.101 * (total_words - counter)) - 0.84):
                # formula based on the Readability of Ease formula for a whole text (206.835 – (1.015 x ASL) –
                # (84.6 x ASW))
                # ASL = Average Sentence Length
                # ASW = Average number of syllables per word
                difficult.append(sentence)

        return difficult


def get_name():
    return "Spache"


def get_description(locale):
    if(locale == 'nl_NL'):
        return "Deze metriek berekent de harde zinnen van een tekst in overeenstemming met de frequentie van " \
               "woorden in de gegeven taal en hun aantal lettergrepen. Daarom, als een zin meer dan een bepaalde " \
               "drempel van moeilijke/laag voorkomende woorden bevat, wordt deze als moeilijk beschouwd."
    else:
        return "This metric calculates the hard sentences of a text in accordance to the frequency of words in the " \
               "given language and their number of syllables. Therefore, if a sentence contains more than a given " \
               "threshold of difficult/low frequent words, it is considered difficult."
