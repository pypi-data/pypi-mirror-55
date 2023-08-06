from scientpyfic.API import API


class LivingWell:

    URLS = {
        "child_development": "child_development",
        "stress": "stress",
        "consumer_behavior": "consumer_behavior",
        "spirituality": "spirituality",
        "dieting_and_weight_control": "diet_and_weight_loss",
        "nutrition_research": "nutrition",
        "behavior": "behavior",
        "caregiving": "caregiving",
        "parenting": "parenting",
        "anger_management": "anger_management",
        "gender_difference": "gender_difference",
        "racial_issues": "racial_issues",
        "relationships": "relationships",
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
