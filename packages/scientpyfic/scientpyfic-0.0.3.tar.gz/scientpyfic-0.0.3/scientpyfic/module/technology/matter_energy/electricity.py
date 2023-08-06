from scientpyfic.API import API


class Electricity:

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

    def electricity(
        self,
        title=None,
        description=None,
        pub_date=None,
        body=None,
        journals=None,
        **kwargs
    ):
        """
        Returns a list with latest news from ScienceDaily about electricity.
        """
        options = {
            "title": title if not title is None else self._title,
            "description": description
            if not description is None
            else self._description,
            "pub_date": pub_date if not pub_date is None else self._pub_date,
            "body": body if not body is None else self._body,
            "journals": journals if not journals is None else self._journals,
        }

        url = "{}/electricity.xml".format(self._url)
        result = API.get(url, name="Electricity", **options, **kwargs)

        return result
