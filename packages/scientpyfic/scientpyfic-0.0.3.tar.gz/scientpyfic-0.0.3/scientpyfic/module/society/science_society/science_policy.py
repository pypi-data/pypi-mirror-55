from scientpyfic.API import API


class SciencePolicy:

    URLS = {
        "energy_issues": "science_society/energy_issues",
        "ocean_policy": "science_society/ocean_policy",
        "scientific_conduct": "science_society/scientific_conduct",
        "space_policy": "science_society/space_policy",
        "government_regulation": "science_society/government_regulation",
        "public_health": "science_society/public_health",
        "privacy_issues": "science_society/privacy_issues",
        "environmental_policies": "science_society/environmental_policy",
        "funding_policy": "science_society/funding_policy",
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
