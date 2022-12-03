from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from language.languages import words


def main_kb_markup(lang):
    bt_lang = KeyboardButton(words[lang]["bt_change_the_lang"])
    bt_random_number = KeyboardButton(words[lang]["bt_random_number"])
    bt_check_the_weather = KeyboardButton(words[lang]["bt_check_the_weather"])
    bt_exchange_rates = KeyboardButton(words[lang]["bt_exchange_rates"])
    bt_info = KeyboardButton(words[lang]["bt_info"])
    bt_heads_or_tails = KeyboardButton(words[lang]["bt_heads_or_tails"])
    bt_translator = KeyboardButton(words[lang]["bt_translator"])
    bt_prediction = KeyboardButton(words[lang]["bt_prediction"])
    keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    return keyboard_markup.add(bt_check_the_weather, bt_translator, bt_exchange_rates,
                               bt_prediction, bt_random_number, bt_heads_or_tails, bt_lang, bt_info)


def cancel_kb(lang):
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(words[lang]["bt_cancel"]))


def translator_cancel_kb(lang, src_lang, dest_lang):
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(KeyboardButton(src_lang),
                                                                      KeyboardButton("↔"),
                                                                      KeyboardButton(dest_lang),
                                                                      KeyboardButton(words[lang]["bt_cancel"]))


inline_kb_ru = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru')
inline_kb_en = InlineKeyboardButton(text='🇺🇸 English', callback_data='en')
inline_kb_ua = InlineKeyboardButton(text='🇺🇦 Українська', callback_data='ua')

inline_kb_markup = InlineKeyboardMarkup(row_width=3).add(inline_kb_en,
                                                         inline_kb_ru,
                                                         inline_kb_ua)
inline_kb_markup_2 = InlineKeyboardMarkup(row_width=1).add(inline_kb_en,
                                                           inline_kb_ru,
                                                           inline_kb_ua)

inline_src_translator_kb_ru = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='src_tr_ru')
inline_src_translator_kb_ua = InlineKeyboardButton(text='🇺🇦 Українська', callback_data='src_tr_ua')
inline_src_translator_kb_en = InlineKeyboardButton(text='🇺🇸 English', callback_data='src_tr_en')
inline_src_translator_kb_ko = InlineKeyboardButton(text='🇰🇷 Korean', callback_data='src_tr_ko')
inline_src_translator_kb_cz = InlineKeyboardButton(text='🇨🇿 Czech', callback_data='src_tr_cz')
inline_src_translator_kb_de = InlineKeyboardButton(text='🇩🇪 Deutsch', callback_data='src_tr_de')

inline_target_translator_kb_ru = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='target_tr_ru')
inline_target_translator_kb_ua = InlineKeyboardButton(text='🇺🇦 Українська', callback_data='target_tr_ua')
inline_target_translator_kb_en = InlineKeyboardButton(text='🇺🇸 English', callback_data='target_tr_en')
inline_target_translator_kb_ko = InlineKeyboardButton(text='🇰🇷 Korean', callback_data='target_tr_ko')
inline_target_translator_kb_cz = InlineKeyboardButton(text='🇨🇿 Czech', callback_data='target_tr_cz')
inline_target_translator_kb_de = InlineKeyboardButton(text='🇩🇪 Deutsch', callback_data='target_tr_de')


def translator_src_inline_kb():
    inline_translator_src_kb_markup = InlineKeyboardMarkup(row_width=2).add(inline_src_translator_kb_ru,
                                                                            inline_src_translator_kb_ua,
                                                                            inline_src_translator_kb_en,
                                                                            inline_src_translator_kb_ko,
                                                                            inline_src_translator_kb_cz,
                                                                            inline_src_translator_kb_de)
    return inline_translator_src_kb_markup


def translator_target_inline_kb():
    inline_translator_target_kb_markup = InlineKeyboardMarkup(row_width=2).add(inline_target_translator_kb_ru,
                                                                               inline_target_translator_kb_ua,
                                                                               inline_target_translator_kb_en,
                                                                               inline_target_translator_kb_ko,
                                                                               inline_target_translator_kb_cz,
                                                                               inline_target_translator_kb_de)
    return inline_translator_target_kb_markup
