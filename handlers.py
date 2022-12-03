import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards as kb
from db import sql_data as sq
from language import languages as lang_massive
from language.languages import words, target_languages_dict, source_languages_dict, source_lang_list, target_lang_list
from bot.create_bot import dp
from functional import get_weather, translator, exchange_rates, predictions, rand_number


@dp.message_handler(commands='start')
async def start(m: types.Message):
    user_id = m.from_user.id
    sq.check_user(user_id)
    await m.answer(f'Hi my friend, please choose a language', reply_markup=kb.inline_kb_markup)


@dp.message_handler(text=lang_massive.bt_cancel)
async def main_menu(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    await m.answer(words[lang]["text_to_main_menu"], reply_markup=kb.main_kb_markup(lang))


@dp.callback_query_handler(text='ru')
async def lang_ru(c: types.CallbackQuery):
    user_id = c.from_user.id
    sq.update_lang(user_id, 'ru')
    lang = sq.answer_lang(user_id)
    main_kb_markup = kb.main_kb_markup(lang)
    await c.message.answer(words[lang]["answer_hello"], reply_markup=main_kb_markup)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text='en')
async def lang_en(c: types.CallbackQuery):
    user_id = c.from_user.id
    sq.update_lang(user_id, 'en')
    lang = sq.answer_lang(user_id)
    main_kb_markup = kb.main_kb_markup(lang)
    await c.message.answer(words[lang]["answer_hello"], reply_markup=main_kb_markup)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text='ua')
async def lang_ua(c: types.CallbackQuery):
    user_id = c.from_user.id
    sq.update_lang(user_id, 'ua')
    lang = sq.answer_lang(user_id)
    main_kb_markup = kb.main_kb_markup(lang)
    await c.message.answer(words[lang]["answer_hello"], reply_markup=main_kb_markup)
    await c.message.delete()
    await c.answer()


@dp.message_handler(text=lang_massive.bt_rand_number)
async def bt_rand_number(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    number_and_sticker = rand_number.rand_num()
    await m.answer_sticker(number_and_sticker[1])
    await m.answer(words[lang]["your_random_number"] + str(number_and_sticker[0]))


@dp.message_handler(text=lang_massive.bt_heads_or_tails)
async def bt_heads_or_tails(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    t = random.randint(0, 1)
    if t == 0:
        await m.answer(words[lang]["heads_up_on_a_coin"])
    else:
        await m.answer(words[lang]["tails_fell_on_a_coin"])


@dp.message_handler(text=lang_massive.bt_change_the_lang)
async def bt_change_the_lang(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    answer = words[lang]["select_the_language"]
    await m.answer(answer, reply_markup=kb.inline_kb_markup_2)


@dp.message_handler(text=lang_massive.bt_info)
async def bt_info(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    answer = words[lang]["info"] + str(user_id)
    await m.answer(answer)


class Weather(StatesGroup):
    town = State()


@dp.message_handler(text=lang_massive.bt_check_the_weather)
async def bt_get_weather(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    text = words[lang]["enter_city_name"]
    await m.answer(text, reply_markup=kb.cancel_kb(lang))
    await Weather.town.set()


@dp.message_handler(lambda message: message.text in ["/start", "Отмена", "⬅ Cancel", "⬅ Отмена",
                                                     "⬅ Назад"], state=Weather)
async def check_word(m: types.Message, state: FSMContext):
    if m.text == "/start":
        await state.finish()
        return await main_menu(m)
    elif m.text == "Отмена":
        await state.finish()
        return await main_menu(m)
    elif m.text in ["⬅ Cancel", "⬅ Отмена", "⬅ Назад"]:
        await state.finish()
        return await main_menu(m)


@dp.message_handler(state=Weather.town)
async def get_name_city(m: types.Message, state: FSMContext):
    await state.update_data(town=m.text)
    data = await state.get_data()
    await state.finish()
    city = data.get('town')
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    await m.answer(get_weather.weather(city, lang))
    await m.answer(words[lang]["answer_after_get_weather"], reply_markup=kb.cancel_kb(lang))
    await Weather.town.set()


class Translator(StatesGroup):
    word = State()
    select_lang = State()


@dp.message_handler(lambda message: message.text in ["/start", "Отмена", "⬅ Cancel", "⬅ Отмена",
                                                     "⬅ Назад"], state=Translator)
async def check_word(m: types.Message, state: FSMContext):
    if m.text == "/start":
        await state.finish()
        return await main_menu(m)
    elif m.text == "Отмена":
        await state.finish()
        return await main_menu(m)
    elif m.text in ["⬅ Cancel", "⬅ Отмена", "⬅ Назад"]:
        await state.finish()
        return await main_menu(m)


@dp.message_handler(text=lang_massive.bt_translator)
async def bt_translator(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    if dest_lang is None or dest_lang == "" or src_lang is None or src_lang == "" \
            or dest_lang in lang_massive.translate_text_list or src_lang in lang_massive.translate_text_list:
        sq.update_source_lang_translator(user_id, words[lang]["choose_source_language"])
        sq.update_target_lang_translator(user_id, words[lang]["choose_target_language"])
        src_lang = sq.answer_source_lang_translator(user_id)
        dest_lang = sq.answer_target_lang_translator(user_id)
        await m.answer(words[lang]["choose_language"], reply_markup=kb.translator_cancel_kb(lang,
                                                                                            src_lang,
                                                                                            dest_lang))

    else:
        await m.answer(words[lang]["enter_text_to_translate"], reply_markup=kb.translator_cancel_kb(lang,
                                                                                                    src_lang,
                                                                                                    dest_lang))
    await Translator.word.set()


@dp.callback_query_handler(text="target_tr_ru", state=Translator)
async def translator_target_lang_ru(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_target_lang_translator(user_id, target_languages_dict["ru"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="target_tr_ua", state=Translator)
async def translator_target_lang_ua(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_target_lang_translator(user_id, target_languages_dict["uk"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="target_tr_en", state=Translator)
async def translator_target_lang_en(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_target_lang_translator(user_id, target_languages_dict["en"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="target_tr_ko", state=Translator)
async def translator_target_lang_ko(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_target_lang_translator(user_id, target_languages_dict["ko"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="target_tr_cz", state=Translator)
async def translator_target_lang_ko(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_target_lang_translator(user_id, target_languages_dict["cs"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="target_tr_de", state=Translator)
async def translator_target_lang_ko(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_target_lang_translator(user_id, target_languages_dict["de"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="src_tr_ru", state=Translator)
async def translator_src_lang_ru(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_source_lang_translator(user_id, source_languages_dict["ru"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="src_tr_ua", state=Translator)
async def translator_src_lang_ua(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_source_lang_translator(user_id, source_languages_dict["uk"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="src_tr_en", state=Translator)
async def translator_src_lang_en(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_source_lang_translator(user_id, source_languages_dict["en"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="src_tr_ko", state=Translator)
async def translator_src_lang_ko(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_source_lang_translator(user_id, source_languages_dict["ko"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="src_tr_cz", state=Translator)
async def translator_src_lang_ko(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_source_lang_translator(user_id, source_languages_dict["cs"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.callback_query_handler(text="src_tr_de", state=Translator)
async def translator_src_lang_ko(c: types.CallbackQuery):
    user_id = c.from_user.id
    lang = sq.answer_lang(user_id)
    sq.update_source_lang_translator(user_id, source_languages_dict["de"])
    src_lang = sq.answer_source_lang_translator(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
    await c.message.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)
    await c.message.delete()
    await c.answer()


@dp.message_handler(text="↔", state=Translator)
async def bt_reverse_translation(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    target_lang = sq.answer_target_lang_translator(user_id)
    source_lang = sq.answer_source_lang_translator(user_id)
    if target_lang not in lang_massive.translate_text_list and source_lang not in lang_massive.translate_text_list:
        sq.reverse_lang_translator(user_id, source_lang, target_lang)
        target_lang = sq.answer_target_lang_translator(user_id)
        source_lang = sq.answer_source_lang_translator(user_id)
        keyboard = kb.translator_cancel_kb(lang, source_lang, target_lang)
        await m.delete()
        await m.answer(words[lang]["successfully_changed_lang"], reply_markup=keyboard)

    else:
        target_lang = sq.answer_target_lang_translator(user_id)
        source_lang = sq.answer_source_lang_translator(user_id)
        keyboard = kb.translator_cancel_kb(lang, source_lang, target_lang)
        await m.delete()
        await m.answer(words[lang]["select_text_lang"], reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in source_lang_list or message.text in ["Выберите язык текста",
                                                                                         "Оберіть мову тексту",
                                                                                         "Select text language"],
                    state=Translator)
async def change_src_translation_language(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    await m.answer(words[lang]["choose_source_language"], reply_markup=kb.translator_src_inline_kb())


@dp.message_handler(lambda message: message.text in target_lang_list or message.text in ["Выберите язык перевода",
                                                                                         "Оберіть мову перекладу",
                                                                                         "Select translation language"],
                    state=Translator)
async def change_target_translation_language(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    await m.answer(words[lang]["choose_target_language"], reply_markup=kb.translator_target_inline_kb())


@dp.message_handler(state=Translator.word)
async def get_translations_word(m: types.Message, state: FSMContext):
    await state.update_data(word=m.text)
    data = await state.get_data()
    await state.finish()
    tr_word = data.get('word')
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    dest_lang = sq.answer_target_lang_translator(user_id)
    src_lang = sq.answer_source_lang_translator(user_id)
    if src_lang is None or src_lang == "" or src_lang == words[lang]["choose_source_language"]:
        await m.answer(words[lang]["choose_source_language"], reply_markup=kb.translator_src_inline_kb())
        await Translator.word.set()

    elif dest_lang is None or dest_lang == "" or dest_lang == words[lang]["choose_target_language"]:
        await m.answer(words[lang]["choose_target_language"], reply_markup=kb.translator_target_inline_kb())
        await Translator.word.set()

    else:
        keyboard = kb.translator_cancel_kb(lang, src_lang, dest_lang)
        answer = words[lang]['your_text'] + tr_word + "\n\n" + words[lang]['translate'] + str(
            translator.translate(tr_word,
                                 src_lang,
                                 dest_lang))
        await m.answer(answer, reply_markup=keyboard)
        await Translator.word.set()


@dp.message_handler(text=lang_massive.bt_exchange_rates)
async def bt_exchange_rates(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    await m.answer(exchange_rates.get_rates(lang))


@dp.message_handler(text=lang_massive.bt_prediction)
async def bt_prediction(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    await m.answer(predictions.get_predict(lang))


@dp.message_handler(content_types=["text"])
async def other_request(m: types.Message):
    user_id = m.from_user.id
    lang = sq.answer_lang(user_id)
    await m.answer(words[lang]["use_navigation_buttons"], reply_markup=kb.main_kb_markup(lang))


def register_handler(disp: dp):
    disp.message_handler(commands=['start'])
