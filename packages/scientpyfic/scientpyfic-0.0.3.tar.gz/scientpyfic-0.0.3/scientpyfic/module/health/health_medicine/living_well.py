from scientpyfic.API import API


class LivingWell:

    URLS = {
        "healthy_aging": "healthy_aging",
        "mens_health": "men's_health",
        "nutrition": "nutrition",
        "teen_health": "teen_health",
        "pregnancy_and_childbirth": "pregnancy_and_childbirth",
        "elder_care": "caregiving",
        "fitness": "fitness",
        "womens_health": "women's_health",
        "skin_care": "skin_care",
        "todays_healthcare": "today's_healthcare",
        "breastfeeding": "breastfeeding",
        "sports_medicine": "sports_medicine",
        "sexual_health": "sexual_health",
        "fertility": "fertility",
        "cosmetic_surgery": "cosmetic_surgery",
        "vegetarian": "vegetarian",
        "staying_healthy": "staying_healthy",
        "childrens_health": "children's_health",
        "infnants_health": "infnant's_health",
        "diet_and_weight_loss": "diet_and_weight_loss",
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
