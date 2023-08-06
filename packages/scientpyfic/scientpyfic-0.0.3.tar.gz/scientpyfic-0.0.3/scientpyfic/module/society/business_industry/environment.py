from scientpyfic.API import API


class Environment:

    URLS = {
        "biotechnology_and_bioengineering": "plants_animals/biotechnology_and_bioengineering",
        "food_and_agriculture": "plants_animals/food_and_agriculture",
        "renewable_energy": "earth_climate/renewable_energy",
        "geoengineering": "earth_climate/geoengineering",
        "recycling_and_waste": "earth_climate/recycling_and_waste",
        "mining": "earth_climate/mining",
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
