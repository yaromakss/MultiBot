import requests
from language.languages import words


def get_rates(lang):
    try:
        r = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
        data = r.json()

        usd_to_uah_buy = round(float(data[0]["buy"]), 2)
        usd_to_uah_sale = round(float(data[0]["sale"]), 2)
        eur_to_uah_buy = round(float(data[1]["buy"]), 2)
        eur_to_uah_sale = round(float(data[1]["sale"]), 2)
        # btc_to_usd_buy = round(float(data[2]["buy"]), 2)     # тимчасово не працює
        # btc_to_usd_sale = round(float(data[2]["sale"]), 2)

        return f"🇺🇸 USD: {usd_to_uah_buy} грн / {usd_to_uah_sale} грн\n" \
               f"🇪🇺 EUR: {eur_to_uah_buy} грн / {eur_to_uah_sale} грн\n" \
               # f"🪙 BTC: {btc_to_usd_buy} $ / {btc_to_usd_sale} $"

    except Exception as ex:
        print(ex)
        return words[lang]["currency_error"]
