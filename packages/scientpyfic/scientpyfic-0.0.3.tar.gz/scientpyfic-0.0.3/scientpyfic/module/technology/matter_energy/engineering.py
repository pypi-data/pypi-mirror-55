from scientpyfic.API import API


class Engineering:

    URLS = {
        "sports_science": "sports_science",
        "virtual_environment": "virtual_reality",
        "weapons_technology": "weapons_technology",
        "civil_engineering": "civil_engineering",
        "forensic_research": "forensics",
        "microarrays": "microarrays",
        "construction": "construction",
        "wearable_technology": "wearable_technology",
        "aviation": "aviation",
        "detectors": "detectors",
        "spintronics": "spintronics",
        "medical_technology": "medical_technology",
        "biometric": "biometric",
        "graphene": "graphene",
        "robotics_research": "robotics",
        "nanotechnology": "nanotechnology",
        "three_d_printing": "3-d_printing",
        "electronics": "electronics",
        "vehicles": "vehicles",
        "engineering": "engineering",
        "materials_science": "materials_science",
        "transportation_science": "transportation_science",
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
