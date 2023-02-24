"""
Common functions used in the various readability metrics.
"""
from decimal import Decimal, ROUND_HALF_UP


def get_minimum_age_from_us_grade(us_grade):
    """
    The age has a linear relation with the grade.
    http://en.wikipedia.org/wiki/Education_in_the_United_States#School_grades
    """
    if us_grade == 0:
        return 0

    min_age = int(Decimal(us_grade + 5).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    if min_age < 0:
        return 0

    return min_age


def syllable_count_english(word):
    """
    Additional function to calculate the syllables of English words
    """
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count
