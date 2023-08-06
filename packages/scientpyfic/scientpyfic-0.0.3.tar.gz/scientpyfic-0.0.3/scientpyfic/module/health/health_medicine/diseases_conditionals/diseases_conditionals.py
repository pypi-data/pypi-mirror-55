from .cancer import Cancer
from .cold_flu import ColdAndFlu
from .heart_health import HeartHealth

from scientpyfic.API import API


class DiseaseConditional:

    URLS = {
        "bladder_disorders": "bladder_disorders",
        "copd": "copd",
        "ebola": "ebola",
        "irritable_bowel_syndrome": "irritable_bowel_syndrome",
        "restless_leg_syndrome": "restless_leg_syndrome",
        "cerebral_palsy": "cerebral_palsy",
        "malaria": "malaria",
        "prostate_health": "prostate_health",
        "birth_defects": "birth_defects",
        "eating_disorder_research": "eating_disorders",
        "pneumonia": "pneumonia",
        "infectious_diseases": "infectious_diseases",
        "alzheimers_research": "alzheimer's",
        "allergy": "allergy",
        "epilepsy_research": "epilepsy",
        "fibromyalgia": "fibromyalgia",
        "gastrointestinal_problems": "gastrointestinal_problems",
        "mumps_measles_rubella": "mumps,_measles,_rubella",
        "obesity": "obesity",
        "thyroid_disease": "thyroid_disease",
        "triglycerides": "triglycerides",
        "tuberculosis": "tuberculosis",
        "insomnia_research": "insomnia",
        "hormone_disorders": "hormone_disorders",
        "joint_pain": "joint_pain",
        "ulcers": "ulcers",
        "colitis": "colitis",
        "cystic_fibrosis": "cystic_fibrosis",
        "asthma": "asthma",
        "erectile_dysfunction": "erectile_dysfunction",
        "lyme_disease": "lyme_disease",
        "multiple_sclerosis_research": "multiple_sclerosis",
        "mental_health_research": "mental_health",
        "urology": "urology",
        "lung_disease": "lung_disease",
        "crohns_disease": "crohn's_disease",
        "parkinsons_research": "parkinson's_disease",
        "attention_deficit_disorder": "add_and_adhd",
        "down_syndrome": "down's_syndrome",
        "hiv_and_aids": "hiv_and_aids",
        "hair_loss": "hair_loss",
        "herpes": "herpes",
        "anemia": "anemia",
        "arthritis": "arthritis",
        "blood_clots": "blood_clots",
        "chronic_fatigue_syndrome": "chronic_fatigue_syndrome",
        "lupus": "lupus",
        "muscular_dystrophy": "muscular_dystrophy",
        "psoriasis": "psoriasis",
        "sleep_disorder_research": "sleep_disorders",
        "headache_research": "headaches",
        "hypertension": "hypertension",
        "neuropathy": "neuropathy",
        "liver_disease": "liver_disease",
        "sickle_cell_anemia": "sickle_cell_anemia",
        "amyotrophic_lateral_sclerosis": "amyotrophic_lateral_sclerosis",
        "diabetes": "diabetes",
        "hearing_loss": "hearing_loss",
        "osteoporosis": "osteoporosis",
        "kidney_disease": "kidney_disease",
        "heartburn": "heartburn",
        "diseases_and_conditions": "diseases_and_conditions",
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

        self.cancer = Cancer(url, title, description, pub_date, body, journals)
        self.cold_flu = ColdAndFlu(url, title, description, pub_date, body, journals)
        self.heart_health = HeartHealth(
            url, title, description, pub_date, body, journals
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
