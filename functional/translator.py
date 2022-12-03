from googletrans import Translator
from language.languages import target_languages_dict, source_languages_dict

translator = Translator()


def get_key_target_lang(d, value):
    for k, v in d.items():
        if v == value:
            return k


def get_key_source_lang(dictionary, values):
    for x, y in dictionary.items():
        if y == values:
            return x


def translate(word, src_lang, dest_lang):
    source_lang_key = get_key_source_lang(source_languages_dict, src_lang)
    target_lang_key = get_key_target_lang(target_languages_dict, dest_lang)
    tr_word = translator.translate(word, src=source_lang_key, dest=target_lang_key)
    return tr_word.text


def reverse_lang(source_lang, target_lang):
    new_source_key = get_key_source_lang(source_languages_dict, source_lang)
    new_source_lang = str(target_languages_dict.get(new_source_key))
    new_target_key = get_key_target_lang(target_languages_dict, target_lang)
    new_target_lang = str(source_languages_dict.get(new_target_key))
    return new_source_lang + "|" + new_target_lang
