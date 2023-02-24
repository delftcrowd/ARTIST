import unittest as ut

import nltk

import application_logic.readability.metric_test as mt
import application_logic.readability.metrics.flesch_kincaid as fk
import application_logic.readability.metrics.only_dutch_specific.flesch_douma as fd
import application_logic.readability.metrics.only_dutch_specific.kpc as kpc
import application_logic.readability.metrics.smog as smog
import application_logic.readability.metrics.spache_sentences as ss

nltk.download('punkt')


class FleschDuomaTest(ut.TestCase, mt.MetricTest):
    def setUp(self):
        mt.MetricTest.__init__(self, 18)

    def test_not_negative_min_age(self):
        self.calc = fd.FleschDouma("")
        self.assertGreaterEqual(self.calc.min_age, 0, "even with no text, min_age should not be negative")

    def test_easy_sentence(self):
        self.calc = fd.FleschDouma("Ik ging naar de winkel en kocht 3 appels. Ik ga naar school.")
        self.assertLessEqual(self.calc.min_age, 10, "easy word")


class FleschKincaidTestCase(ut.TestCase, mt.MetricTest):
    def setUp(self):
        mt.MetricTest.__init__(self, 17)

    def test_not_negative_min_age(self):
        self.calc = fk.FleschKincaid("", 'en_GB')
        self.assertGreaterEqual(self.calc.min_age, 0, "min_age should not be negative even with no text")

    def test_easy(self):
        self.calc = fk.FleschKincaid("I am going to the store. I buy a doll.", 'en_GB')
        self.assertIn(self.calc.min_age, range(0, 6), "The provided text is very easy, score should be less than 6.")


class SMOGTestCase(ut.TestCase, mt.MetricTest):
    def setUp(self):
        mt.MetricTest.__init__(self, 17)

    def test_not_negative_min_age(self):
        self.calc = smog.SMOG("", 'en_GB')
        self.assertGreaterEqual(self.calc.min_age, 0, "min_age should not be negative even with no text")

    def test_easy(self):
        self.calc = smog.SMOG("I am going to the store. I buy a doll.", 'en_GB')
        self.assertIn(self.calc.min_age, range(0, 10), "The provided text is very easy, score should be less than 10.")


class KPCTest(ut.TestCase, mt.MetricTest):
    def setUp(self):
        mt.MetricTest.__init__(self, 18)

    def test_not_negative_min_age(self):
        self.calc = kpc.KPC("")
        self.assertGreaterEqual(self.calc.min_age, 0, "even with no text, min_age should not be negative")

    def test_easy_sentence(self):
        self.calc = kpc.KPC("Ik ging naar de winkel en kocht 3 appels. Ik ga naar school.")
        self.assertLessEqual(self.calc.min_age, 8, "The provided text is very easy, score should be less than 8.")


class DifficultSentencesTest(ut.TestCase, mt.MetricTest):
    def test_difficult_sentences_test(self):
        self.calc = ss.SpacheSentences(
            "amicable friends picnic. Have fun camaraderie capitulate conditional fruit "
            "Supercalifragilisticexpialidocious Worcestershire.",
            'en_GB')
        print(self.calc.get_difficult_sentences())
        # print(self.calc.min_age)
        self.assertEqual(len(self.calc.get_difficult_sentences()), 1)
