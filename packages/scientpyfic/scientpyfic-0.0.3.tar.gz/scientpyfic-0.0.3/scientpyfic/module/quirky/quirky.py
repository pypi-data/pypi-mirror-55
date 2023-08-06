from scientpyfic.API import API


class Quirky:

    URLS = {
        "human_quirks": "human_quirks",
        "health_medicine": "health_medicine",
        "mind_brain": "mind_brain",
        "living_well": "living_well",
        "bizarre_things": "bizarre_things",
        "space_time": "space_time",
        "matter_energy": "matter_energy",
        "computers_math": "computers_math",
        "odd_creatures": "odd_creatures",
        "plants_animals": "plants_animals",
        "earth_climate": "earth_climate",
        "fossils_ruins": "fossils_ruins",
        "weird_world": "weird_world",
        "science_society": "science_society",
        "business_industry": "business_industry",
        "education_learning": "education_learning",
    }

    """
    For more information check the official documentation:
      https://github.com/monzita/scientpyfic/wiki/Quirky
    """

    def __init__(self, url, title, description, pub_date, body, journals):
        self._url = url + "/strange_offbeat"
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

            url = (
                "{}.xml".format(self._url)
                if name == "strange_offbeat"
                else "{}/{}.xml".format(self._url, self.URLS[name])
            )

            result = API.get(url, name=name.title(), **options, **kwargs)
            return result

        return handler
