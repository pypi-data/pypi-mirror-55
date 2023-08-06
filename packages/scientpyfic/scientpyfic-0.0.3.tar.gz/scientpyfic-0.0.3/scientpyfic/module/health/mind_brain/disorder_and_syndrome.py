from scientpyfic.API import API


class DisorderAndSyndrome:

    URLS = {
        "add_and_adhd": "add_and_adhd",
        "alzheimers": "alzheimer's",
        "dementia": "dementia",
        "schizophrenia": "schizophrenia",
        "borderline_personality_disorder": "borderline_personality_disorder",
        "bipolar_disorder": "bipolar_disorder",
        "depression": "depression",
        "huntingtons_disease": "huntington's_disease",
        "insomnia": "insomnia",
        "parkinsons": "parkinson's",
        "stroke": "stroke",
        "headaches": "headaches",
        "multiple_sclerosis": "multiple_sclerosis",
        "tinnitus": "tinnitus",
        "autism": "autism",
        "hearing_impairment": "hearing_loss",
        "epilepsy": "epilepsy",
        "obstructive_sleep_apnea": "obstructive_sleep_apnea",
        "sleep_disorders": "sleep_disorders",
        "ptsd": "ptsd",
        "mad_cow_disease": "mad_cow_disease",
        "disorders_and_syndromes": "disorders_and_syndromes",
        "brain_injury": "brain_injury",
    }

    """
    For more information check the official documentation:
      https://github.com/monzita/scientpyfic/wiki/Health
    """

    def __init__(self, url, title, description, pub_date, body, journals):
        self._url = url
        self._title = title
        self._description = description
        self._pub_date = pub_date
        self._body = body
        self._journals = journals

    def __getattr__(self, name):
        def handler(**kwargs):
            options = {
                "title": kwargs.get("title", None) or self._title,
                "description": kwargs.get("description", None) or self._description,
                "pub_date": kwargs.get("pub_date", None) or self._pub_date,
                "body": kwargs.get("body", None) or self._body,
                "journals": kwargs.get("journals", None) or self._journals,
            }

            url = "{}/{}.xml".format(self._url, self.URLS[name])
            result = API.get(url, name=name.title(), **options, **kwargs)
            return result

        return handler
