from .business_industry import BusinessIndustry
from .earth_science import EarthScience
from .education_learning import EducationLearning
from .environmental_issues import EnvironmentalIssue
from .environmental_science import EnvironmentalScience
from .natural_disaster import NaturalDisaster

from scientpyfic.API import API


class EarthClimate:

    URLS = {"earth_climate": "earth_climate"}

    """
    For more information check the official documentation:
        https://github.com/monzita/scientpyfic/wiki/Environment.py
    """

    def __init__(self, url, title, description, pub_date, body, journals):
        self._url = "{}/earth_climate".format(url)
        self._title = title
        self._description = description
        self._pub_date = pub_date
        self._body = body
        self._journals = journals

        self.business_industry = BusinessIndustry(
            self._url, title, description, pub_date, body, journals
        )
        self.earth_science = EarthScience(
            self._url, title, description, pub_date, body, journals
        )
        self.education_learning = EducationLearning(
            self._url, title, description, pub_date, body, journals
        )
        self.environmental_issues = EnvironmentalIssue(
            self._url, title, description, pub_date, body, journals
        )
        self.environmental_science = EnvironmentalScience(
            self._url, title, description, pub_date, body, journals
        )
        self.natural_disasters = NaturalDisaster(
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

            url = "{}.xml".format(self.URLS[name])
            result = API.get(url, name=name.title(), **options, **kwargs)
            return result

        return handler
