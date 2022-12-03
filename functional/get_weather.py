import datetime
import requests as requests

from config.settings import weather_token
from language.languages import words

code_to_smile_ru = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}
code_to_smile_ua = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Хмарно \U00002601",
    "Rain": "Дощ \U00002614",
    "Drizzle": "Дощ \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Сніг \U0001F328",
    "Mist": "Туман \U0001F32B"
}
code_to_smile_en = {
    "Clear": "Clear \U00002600",
    "Clouds": "Clouds \U00002601",
    "Rain": "Rain \U00002614",
    "Drizzle": "Drizzle \U00002614",
    "Thunderstorm": "Thunderstorm \U000026A1",
    "Snow": "Snow \U0001F328",
    "Mist": "Mist \U0001F32B"
}


def weather(city_name, lang):
    wd = ""
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_token}&units=metric"
        )
        data = r.json()

        city_from_user = city_name.capitalize()

        main_weather = data["weather"][0]["main"]
        if lang == "ru":
            if main_weather in code_to_smile_ru:
                wd = code_to_smile_ru[main_weather]
            else:
                wd = "У тебя там какая-то хрень за окном, сам разбирайся"
        elif lang == "ua":
            if main_weather in code_to_smile_ua:
                wd = code_to_smile_ua[main_weather]
            else:
                wd = "Що там у тебе коїться за вікном о_0 "
        elif lang == "en":
            if main_weather in code_to_smile_en:
                wd = code_to_smile_en[main_weather]
            else:
                wd = "You have some kind of crap outside the window, figure it out yourself"

        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        if lang == "ru":
            return f"В городе {city_from_user} сейчас:" \
                   f" {wd} \nТемпература: {cur_temp} С°\nВлажность: {humidity} %\nДавление: {pressure} мм.рт.ст\n" \
                   f"Ветер:" \
                   f" {wind} м/с\nВремя восхода: {sunrise_timestamp}\nВремя захода: {sunset_timestamp}" \
                   f"\nПродолжительность дня: {length_of_the_day}\n"
        elif lang == "ua":
            return f"В місті {city_from_user} зараз:" \
                   f" {wd} \nТемпература: {cur_temp} С°\nВологість: {humidity} %\nТиск: {pressure} мм.рт.ст\nВітер:" \
                   f" {wind} м/с\nЧас сходу: {sunrise_timestamp}\nЧас заходу: {sunset_timestamp}" \
                   f"\nТривалість дня: {length_of_the_day}\n"
        elif lang == "en":
            return f"In the city of {city_from_user} now: {wd} \nTemperature: {cur_temp} С°\n" \
                   f"Humidity: {humidity} %\n" \
                   f"Pressure: {pressure} millimeters of mercury\nWind:" \
                   f" {wind} m/s\nSunrise time: {sunrise_timestamp}\nSunset time: {sunset_timestamp}" \
                   f"\nDay length: {length_of_the_day}\n"

    except Exception as ex:
        print(ex)
        print("Такого города не существует")
        return words[lang]["check_the_city_name"]
