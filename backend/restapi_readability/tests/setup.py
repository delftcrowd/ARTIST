from django.urls import reverse

url_options = reverse('get_options_readability')
url_measure = reverse('readability_post')
url_sentences = reverse('difficult_sentences_post')

hard_text = "Wij doen u een formulier toekomen waarop u dient aan te geven hoeveel u vorig jaar hebt verdiend met uw "\
            "inmiddels failliete bedrijf. "
simple_text = "U krijgt van ons een formulier. Daarop vult u in hoeveel u vorig jaar hebt verdiend."

description_fd = "The Flesch Reading Ease reading index ranges from 0 to 100. You should aim for a 60+ score minimum. "\
                 "The minimum age should be as small as possible, indicating what age groups should be able to " \
                 "understand the text. The age is strongly correlated to the grade system, therefore the maximum " \
                 "possible age is 24 which corresponds to graduating with a Masters degree."
description_fk = "The Flesch Reading Ease reading index ranges from 0 to 100. You should aim for a 60+ score minimum. "\
                 "The minimum age should be as small as possible, indicating what age groups should be able to " \
                 "understand the text. The age is strongly correlated to the grade system, therefore the maximum " \
                 "possible age is 24 which corresponds to graduating with a Masters degree."
description_kpc = "The AVI levels focus on technical skills rather than reading comprehension. They represent the " \
                  "ability to fluently and flawlessly read words and sentences. The higher the level, " \
                  "the more complex words and longer sentences. To you it is displayed the minimum age the reader " \
                  "needs to have in order to understand the given text. This is calculated in accordance to the AVI " \
                  "levels calculated by KPC, therefore the maximum possible age is 24 which corresponds to graduating "\
                  "with a Masters degree."
description_smog = "SMOG measures how many years of education the average person needs to have graduated in order to " \
                   "understand the text. Displayed to you is the minimum age, which is mapped in accordance to the " \
                   "grade calculated by SMOG, therefore the maximum possible age is 24 which corresponds to " \
                   "graduating with a Masters degree."
description_spache = "This metric calculates the hard sentences of a text in accordance to the frequency of words in " \
                     "the given language and their number of syllables. Therefore, if a sentence contains more than a "\
                     "given threshold of difficult/low frequent words, it is considered difficult."
