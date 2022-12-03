import random


cubes = {1: "CAACAgIAAxkBAAEFzXljHidn4xRQ0sYbwZQBKKLHjyV_3AAC3MYBAAFji0YMsbUSFEouGv8pBA",
         2: "CAACAgIAAxkBAAEFzXtjHii_-Z_kz82QKkHE5wPHmL7WIgAC3cYBAAFji0YM608pO-wjAlEpBA",
         3: "CAACAgIAAxkBAAEFzX1jHijLJXq1dxOzIVCiZ2xkXZsj_AAC3sYBAAFji0YMVHH9hav7ILkpBA",
         4: "CAACAgIAAxkBAAEFzX9jHijN2CPREBaAIOegB02AocSoNgAC38YBAAFji0YMHEUTINW7YxcpBA",
         5: "CAACAgIAAxkBAAEFzYFjHijQyIk2x0kzixnjQ6MeGxCUrQAC4MYBAAFji0YMSLHz-sj_JqkpBA",
         6: "CAACAgIAAxkBAAEFzYNjHijUUinLGiv2N8PQmL2_EJZMmAAC4cYBAAFji0YM75p8zae_tHopBA"
         }


def rand_num():
    t = random.randint(1, 6)
    return [t, cubes[t]]
