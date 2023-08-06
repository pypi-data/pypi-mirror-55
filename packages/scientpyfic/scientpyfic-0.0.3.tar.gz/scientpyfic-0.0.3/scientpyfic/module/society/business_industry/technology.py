from scientpyfic.API import API


class Technology:

    URLS = {
        "markets_and_finance": "computers_math/markets_and_finance",
        "textiles_and_clothing": "matter_energy/textiles_and_clothing",
        "engineerig_and_construction": "matter_energy/engineering_and_construction",
        "energy_and_resources": "matter_energy/energy_and_resources",
        "telecommunications": "matter_energy/telecommunications",
        "automotive_and_transportation": "matter_energy/automotive_and_transportation",
        "computers_and_internet": "computers_math/computers_and_internet",
        "aerospace": "matter_energy/aerospace",
        "consumer_electronics": "matter_energy/consumer_electronics",
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
