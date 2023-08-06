from scientpyfic.API import API


class LivingWell:

    URLS = {
        "living_well": "living_well",
        "healthy_aging": "health_medicine/healthy_aging",
        "mens_health": "health_medicine/men's_health",
        "nutrition": "health_medicine/nutrition",
        "teen_health": "health_medicine/teen_health",
        "child_development": "mind_brain/child_development",
        "pregnancy_and_childbirth": "health_medicine/pregnancy_and_childbirth",
        "stress": "mind_brain/stress",
        "elder_care": "health_medicine/caregiving",
        "consumer_behavior": "mind_brain/consumer_behavior",
        "fitness": "health_medicine/fitness",
        "spirituality": "mind_brain/spirituality",
        "womens_health": "health_medicine/women's_health",
        "skin_care": "health_medicine/skin_care",
        "todays_healthcare": "health_medicine/today's_healthcare",
        "breastfeeding": "health_medicine/breastfeeding",
        "sports_medicine": "health_medicine/sports_medicine",
        "sexual_health": "health_medicine/sexual_health",
        "dieting_and_weihgt_control": "mind_brain/diet_and_weight_loss",
        "fertility": "health_medicine/fertility",
        "cosmetic_surgery": "health_medicine/cosmetic_surgery",
        "vegetarian": "health_medicine/vegetarian",
        "nutrition_research": "mind_brain/nutrition",
        "staying_healthy": "health_medicine/staying_healthy",
        "childrens_health": "health_medicine/children's_health",
        "behavior": "mind_brain/behavior",
        "caregiving": "mind_brain/caregiving",
        "infants_health": "health_medicine/infant's_health",
        "parenting": "mind_brain/parenting",
        "anger_management": "mind_brain/anger_management",
        "diet_and_weight_loss": "health_medicine/diet_and_weight_loss",
        "gender_difference": "mind_brain/gender_difference",
        "racial_issues": "mind_brain/racial_issues",
        "relationships": "mind_brain/relationships",
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
