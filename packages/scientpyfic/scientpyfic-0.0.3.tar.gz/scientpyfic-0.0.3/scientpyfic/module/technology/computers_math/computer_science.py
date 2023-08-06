from scientpyfic.API import API


class ComputerScience:

    URLS = {
        "computational_biology": "computers_math/computational_biology",
        "computer_graphics": "computers_math/computer_graphics",
        "computer_modeling": "computers_math/computer_modeling",
        "computer_science": "computers_math/computer_science",
        "encryption": "computers_math/encryption",
        "mobile_computing": "computers_math/mobile_computing",
        "artificial_intelligence": "computers_math/artificial_intelligence",
        "video_games": "computers_math/video_games",
        "virtual_reality": "computers_math/virtual_reality",
        "distributed_computing": "computers_math/distributed_computing",
        "computer_programming": "computers_math/computer_programming",
        "quantum_computers": "computers_math/quantum_computers",
        "spintronics_research": "computers_math/spintronics",
        "wifi": "computers_math/wifi",
        "information_technology": "computers_math/information_technology",
        "robotics": "computers_math/robotics",
        "hacking": "computers_math/hacking",
        "internet": "computers_math/internet",
        "software": "computers_math/software",
        "communications": "computers_math/communications",
        "photography": "computers_math/photography",
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
