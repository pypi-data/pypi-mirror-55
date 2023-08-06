from scientpyfic.API import API


class Animal:

    URLS = {
        "cows_sheep_pigs": "cows,_sheep,_pigs",
        "rodents": "rodents",
        "veterinary_medicine": "veterinary_medicine",
        "dogs": "dogs",
        "mice": "mice",
        "cats": "cats",
        "horses": "horses",
        "spiders_and_ticks": "spiders",
        "birds": "birds",
        "frogs_and_reptiles": "frogs_and_reptiles",
        "apes": "apes",
        "monkeys": "monkeys",
        "new_species": "new_species",
        "fish": "fish",
        "insects": "insects_and_butterflies",
        "dolphins_and_whales": "dolphins_and_whales",
        "animals": "animals",
        "mammals": "mammals",
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
