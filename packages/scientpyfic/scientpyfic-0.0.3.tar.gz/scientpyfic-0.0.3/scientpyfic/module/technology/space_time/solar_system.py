from scientpyfic.API import API


class SolarSystem:

    URLS = {
        "solar_system": "solar_system",
        "kuiper_belt": "kuiper_belt",
        "moon": "moon",
        "neptune": "neptune",
        "asteroids_comets_meteors": "asteroids,_comets_and_meteors",
        "venus": "venus",
        "saturn": "saturn",
        "mars": "mars",
        "mercury": "mercury",
        "northern_lights": "northern_lights",
        "sun": "sun",
        "uranus": "uranus",
        "jupiter": "jupiter",
        "solar_flare": "solar_flare",
        "pluto": "pluto",
        "eris": "eris",
    }

    """
    For more information check the official documentation:
        https://github.com/monzita/scientpyfic/wiki/Technology
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
