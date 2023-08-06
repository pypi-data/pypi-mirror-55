from scientpyfic.API import API


class SocialIssues:

    URLS = {
        "surveillance": "science_society/surveillance",
        "transportation_issues": "science_society/transportation_issues",
        "resource_shortage": "science_society/resource_shortage",
        "urbanization": "science_society/urbanization",
        "racial_disparity": "science_society/racial_disparity",
        "world_development": "science_society/world_development",
        "conflict": "science_society/conflict",
        "bioethics": "science_society/bioethics",
        "economics": "science_society/economics",
        "ethics": "science_society/ethics",
        "disaster_plan": "science_society/disaster_plan",
        "justice": "science_society/justice",
        "social_issues": "science_society/social_issues",
        "consumerism": "science_society/consumerism",
        "legal_issues": "science_society/legal_issues",
        "political_science": "science_society/political_science",
        "popular_culture": "science_society/popular_culture",
        "land_management": "science_society/land_management",
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
