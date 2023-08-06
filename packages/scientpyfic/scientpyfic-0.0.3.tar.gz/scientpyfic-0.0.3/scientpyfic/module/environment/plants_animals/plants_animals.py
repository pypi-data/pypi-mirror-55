from .agriculture_food import AgricultureFood
from .animal import Animal
from .business_industry import BusinessIndustry
from .ecology import Ecology
from .education_learning import EducationLearning
from .life_science import LifeScience
from .microbes_more import MicrobesMore

from scientpyfic.API import API


class PlantsAnimals:

    """
    For more information check the official documentation:
        https://github.com/monzita/scientpyfic/wiki/Environment.py
    """

    def __init__(self, url, title, description, pub_date, body, journals):
        self._url = "{}/plants_animals".format(url)
        self._title = title
        self._description = description
        self._pub_date = pub_date
        self._body = body
        self._journals = journals

        self.agriculture_food = AgricultureFood(
            self._url, title, description, pub_date, body, journals
        )
        self.animals = Animal(self._url, title, description, pub_date, body, journals)
        self.business_industry = BusinessIndustry(
            self._url, title, description, pub_date, body, journals
        )
        self.ecology = Ecology(self._url, title, description, pub_date, body, journals)
        self.education_learning = EducationLearning(
            self._url, title, description, pub_date, body, journals
        )
        self.life_science = LifeScience(
            self._url, title, description, pub_date, body, journals
        )
        self.microbes_more = MicrobesMore(
            self._url, title, description, pub_date, body, journals
        )

    def __getattr__(self, name):
        def handler(**kwargs):
            options = {
                "title": kwargs.get("title", None) or self._title,
                "description": kwargs.get("description", None) or self._description,
                "pub_date": kwargs.get("pub_date", None) or self._pub_date,
                "body": kwargs.get("body", None) or self._body,
                "journals": kwargs.get("journals", None) or self._journals,
            }

            url = "{}.xml".format(self._url)
            result = API.get(url, name=name.title(), **options, **kwargs)
            return result

        return handler
