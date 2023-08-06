from scientpyfic.API import API

from .severe_weather import SevereWeather


class NaturalDisaster:

    URLS = {
        "natural_disasters": "natural_disasters",
        "volcanoes": "volcanoes",
        "snow_and_avalanches": "snow_and_avalanches",
        "tsunamis": "tsunamis",
        "geomagnetic_storms": "geomagnetic_storms",
        "landslides": "landslides",
        "earthquakes": "earthquakes",
        "near_earth_object_impacts": "near-earth_object_impacts",
    }

    """
    For more information check the official documentation:
        https://github.com/monzita/scientpyfic/wiki/Environment.py
    """

    def __init__(self, url, title, description, pub_date, body, journals):
        self._url = url
        self._title = title
        self._description = description
        self._pub_date = pub_date
        self._body = body
        self._journals = journals

        self.severe_weather = SevereWeather(
            url, title, description, pub_date, body, journals
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

            url = "{}/{}.xml".format(self._url, self.URLS[name])
            result = API.get(url, name=name.title(), **options, **kwargs)
            return result

        return handler
