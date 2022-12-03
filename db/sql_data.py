from peewee import *
from functional import translator

db = SqliteDatabase("db/database.db")


class Base(Model):
    class Meta:
        database = db


class Users(Base):
    id = IntegerField(primary_key=True)
    user_telegram_id = CharField(unique=True)
    lang = CharField()
    source_lang_translator = CharField()
    target_lang_translator = CharField()


def check_user(user_id):
    try:
        Users.get(Users.user_telegram_id == user_id).user_telegram_id
    except DoesNotExist:
        Users.create(user_telegram_id=user_id, lang="not selected")


def update_lang(user_id, lang):
    Users.update({Users.lang: lang}).where(Users.user_telegram_id == user_id).execute()


def answer_lang(user_id):
    text = Users.get(Users.user_telegram_id == user_id).lang
    return text


def answer_source_lang_translator(user_id):
    return Users.get(Users.user_telegram_id == user_id).source_lang_translator


def update_source_lang_translator(user_id, src_lang):
    Users.update({Users.source_lang_translator: src_lang}).where(Users.user_telegram_id == user_id).execute()


def answer_target_lang_translator(user_id):
    return Users.get(Users.user_telegram_id == user_id).target_lang_translator


def update_target_lang_translator(user_id, target_lang):
    Users.update({Users.target_lang_translator: target_lang}).where(Users.user_telegram_id == user_id).execute()


def reverse_lang_translator(user_id, source_lang, target_lang):
    rev_lang = translator.reverse_lang(source_lang, target_lang)
    rev_lang = rev_lang.split("|")
    Users.update({Users.target_lang_translator: rev_lang[0]}).where(Users.user_telegram_id == user_id).execute()
    Users.update({Users.source_lang_translator: rev_lang[1]}).where(Users.user_telegram_id == user_id).execute()
