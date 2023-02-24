## Readability Measures Documentation

### How to add a new metric to the system?
Please follow the format of any metric that has been implemented so far.\


Any class you add should follow the following template:

<code> class NewMetric(TextAnalyzer):

    def __init__(self, text, locale='nl_NL'):
        TextAnalyzer.__init__(self, text, locale)
        self.set_text_scores()
        self.us_grade = 0
        self.set_grade()
        self.min_age = get_minimum_age_from_us_grade(self.us_grade)
</code>

<code>locale</code> is initially set to 'nl_NL' as default as this is tool was initially built to work for the Dutch
language. You can change this to match your desired locale when you are using the APIs or change its default.
A good new default would be 'en_GB' and set your desired locale only in the API calls.

<code>set_text_scores</code> is where you are supposed to implement the formula of the new metric you are adding. 

### What is TextAnalyzer and how do I use it?
<code> class TextAnalyzer</code> is the interface that all metrics implement. This is where the text is set to be used
 further, this is where the text is divided into words and sentences and also where the locale is actually set.
As you can observe, the default <code>locale</code> here is actually 'en_GB' and it is being set to a different one in
 each metric, but it can be changed from within the metric as well, otherwise the default is going to be used. This 
locale is necessary because we are using the NLTK module to help us split the text correctly into words and sentences,
 etc. and it requires to know what the language of the text is so that it can split it according to the 
grammar and spelling rules of that language.