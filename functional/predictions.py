import random
from language.languages import predictions_dict


def get_predict(lang):
    t = random.randint(1, 10)
    return predictions_dict[lang][t]
