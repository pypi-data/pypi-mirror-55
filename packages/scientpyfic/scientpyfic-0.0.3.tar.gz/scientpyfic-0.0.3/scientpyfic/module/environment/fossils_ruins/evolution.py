from scientpyfic.API import API


class Evolution:

    URLS = {
        "ancient_dna": "ancient_dna",
        "human_evolution": "human_evolution",
        "origin_of_life": "origin_of_life",
        "charles_darwin": "charles_darwin",
        "evolution": "evolution",
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
