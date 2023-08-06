from scientpyfic.API import API


class EnvironmentalScience:

    URLS = {
        "energy_and_the_environment": "energy",
        "desert": "desert",
        "ecology": "ecology",
        "water": "water",
        "coral_reefs": "coral_reefs",
        "rainforests": "rainforests",
        "wildfires": "wildfires",
        "caving": "caving",
        "ecosystems": "ecosystems",
        "environmental_science": "environmental_science",
        "biodiversity": "biodiversity",
        "tundra": "tundra",
        "exotic_species": "invasive_species",
        "forest": "forests",
        "grassland": "grasslands",
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
