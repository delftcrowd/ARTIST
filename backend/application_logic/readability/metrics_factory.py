"""
Factory Design Pattern for the readability metrics implemented
"""
import application_logic.readability.metrics.flesch_kincaid as fk
import application_logic.readability.metrics.only_dutch_specific.flesch_douma as fd
import application_logic.readability.metrics.only_dutch_specific.kpc as kpc
import application_logic.readability.metrics.smog as smog
import application_logic.readability.metrics.spache_sentences as ss


class MetricsFactory:
    """
    Factory class
    """
    def __init__(self, metric_name, text, difficult_sentence=False):
        self.metric_name = metric_name
        if not difficult_sentence:
            self.metric = None
            if metric_name == fd.get_name():
                self.metric = fd.FleschDouma(text, locale='nl_NL')
            elif metric_name == fk.get_name():
                self.metric = fk.FleschKincaid(text, locale='nl_NL')
            elif metric_name == kpc.get_name():
                self.metric = kpc.KPC(text, locale='nl_NL')
            elif metric_name == smog.get_name():
                self.metric = smog.SMOG(text, locale='nl_NL')
            else:
                raise ValueError("Metric type not supported")
        else:
            if metric_name == ss.get_name():
                self.metric = ss.SpacheSentences(text, locale='nl_NL')
            else:
                raise ValueError("Metric type not supported")

    def get_min_age(self):
        """
        Getter minimum age
        """
        return self.metric.min_age

    def get_difficult_sentences(self):
        """
        Getter difficult sentences
        """
        return self.metric.difficult_sentences

    def get_description(self):
        """
        Getter description
        """
        for option in get_options().get("readability_measures"):
            if option.get("metric_name") == self.metric_name:
                return option.get("description")

        for option in get_options().get("difficult_sentences"):
            if option.get("metric_name") == self.metric_name:
                return option.get("description")

        return ""


def get_options(locale="en_GB"):
    """
    Getter options
    """
    difficult_sentences = []
    measure_readability = [{"metric_name": fd.get_name(),
                            "description": fd.get_description(locale)},
                           {"metric_name": fk.get_name(),
                            "description": fk.get_description(locale)},
                           {"metric_name": kpc.get_name(),
                            "description": kpc.get_description(locale)},
                           {"metric_name": smog.get_name(),
                            "description": smog.get_description(locale)}]
    difficult_sentences.append({"metric_name": ss.get_name(),
                                "description": ss.get_description(locale)})

    options = {"difficult_sentences": difficult_sentences,
               "readability_measures": measure_readability}

    return options


def get_names():
    """
    Getter names
    """
    names = []
    for option in get_options().get("readability_measures"):
        names.append(option["metric_name"])

    for option in get_options().get("difficult_sentences"):
        names.append(option["metric_name"])

    return names
