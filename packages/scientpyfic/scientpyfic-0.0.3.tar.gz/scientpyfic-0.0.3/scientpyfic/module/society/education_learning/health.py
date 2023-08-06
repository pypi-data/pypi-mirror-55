from scientpyfic.API import API


class Health:

    URLS = {
        "dyslexia": "mind_brain/dyslexia",
        "educational_psychology": "mind_brain/educational_psychology",
        "k_12_education": "mind_brain/k-12_education",
        "numeracy": "mind_brain/numeracy",
        "public_health_education": "health_medicine/public_health_education",
        "medical_education_and_training": "health_medicine/medical_education_and_training",
        "brain_computer_interfaces": "mind_brain/brain_computer_interfaces",
        "learning_disorders": "mind_brain/learning_disorders",
        "language_acquisition": "mind_brain/language_acquisition",
        "music": "mind_brain/music",
        "patient_education_and_counseling": "health_medicine/patient_education_and_counseling",
        "creativity": "mind_brain/creativity",
        "infant_and_preschool_learning": "mind_brain/infant_and_preschool_learning",
        "literacy": "mind_brain/literacy",
        "intelligence": "mind_brain/intelligence",
    }

    """
    For more information check the official documentation:
        https://github.com/monzita/scientpyfic/wiki/Society
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
