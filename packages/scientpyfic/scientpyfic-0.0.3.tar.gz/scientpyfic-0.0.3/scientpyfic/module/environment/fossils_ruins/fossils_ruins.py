from .anthropology import Anthropology
from .archaeology import Archaeology
from .evolution import Evolution
from .paleontology import Paleontology

from scientpyfic.API import API


class FossilsRuins:

    URLS = {"fossils_and_ruins": "fossils_ruins"}

    """
    For more information check the official documentation:
        https://github.com/monzita/scientpyfic/wiki/Environment.py
    """

    def __init__(self, url, title, description, pub_date, body, journals):
        self._url = "{}".format(url)
        self._title = title
        self._description = description
        self._pub_date = pub_date
        self._body = body
        self._journals = journals

        self.anthropology = Anthropology(
            self._url, title, description, pub_date, body, journals
        )
        self.archaeology = Archaeology(
            self._url, title, description, pub_date, body, journals
        )
        self.evolution = Evolution(
            self._url, title, description, pub_date, body, journals
        )
        self.paleontology = Paleontology(
            self._url, title, description, pub_date, body, journals
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
