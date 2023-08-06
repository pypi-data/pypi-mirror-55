from scientpyfic.module.health.health_medicine.medical_topics.vitamin import Vitamin

from scientpyfic.API import API


class MedicalTopic:

    URLS = {
        "foot_health": "foot_health",
        "joint_health": "joint_health",
        "gynecology": "gynecology",
        "stem_cells": "stem_cells",
        "alternative_medicine": "alternative_medicine",
        "nervous_system": "nervous_system",
        "controlled_substances": "illegal_drugs",
        "epigenetics": "epigenetics",
        "genes": "genes",
        "immune_system": "immune_system",
        "chronic_illness": "chronic_illness",
        "disability": "disability",
        "foodborne_illness": "foodborne_illness",
        "pain_control": "pain_control",
        "menopause": "menopause",
        "eye_care": "eye_care",
        "gene_therapy": "gene_therapy",
        "food_additives": "food_additives",
        "accident_and_trauma": "accident_and_trauma",
        "dentistry": "dentistry",
        "folic_acid": "folic_acid",
        "forensics": "forensics",
        "bone_and_spine": "bone_and_spine",
        "birth_control": "birth_control",
        "personalized_medicine": "personalized_medicine",
        "medical_imaging": "medical_imaging",
        "wounds_and_healing": "wounds_and_healing",
        "health_policy": "health_policy",
        "human_biology": "human_biology",
        "pharmacology": "pharmacology",
        "psychological_research": "psychology",
        "dietary_supplements_and_minerals": "dietary_supplements",
        "smoking": "smoking",
        "vaccines": "vaccines",
        "viruses": "viruses",
    }

    """
    For more information check the official documentation:
        https://github.com/monzita/scientpyfic/wiki/Health
    """

    def __init__(self, url, title, description, pub_date, body, journals):
        self._url = url
        self._title = title
        self._description = description
        self._pub_date = pub_date
        self._body = body
        self._journals = journals

        self.vitamins = Vitamin(url, title, description, pub_date, body, journals)

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
