import json
import requests
import telebot

TOKEN = '5730166317:AAErPcWQkr4hph9D6aZLUSnXHBSoCrweKz0'

bot = telebot.TeleBot(TOKEN)

keys = {
    'рубль': 'RUB',
    'евро': 'EUR',
    'доллар': 'USD',
}


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message: telebot.types.Message):
        text = 'Что бы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
        <в какую валюту перевести> \
        <количество переводимой валюты>\nУвидить список всех доступныз валют: /values'
        bot.reply_to(message, text)

    @bot.message_handler(commands=['values'])
    def values(message: telebot.types.Message):
        text = 'Доступные валюты'
        for key in keys.keys():
            text = '\n'.join((text, key,))
        bot.reply_to(message, text)

    @bot.message_handler(content_types=['text', ])
    def converter(message: telebot.types.Message):
        try:
            values = message.text.split(' ')

            if len(values) != 3:
                raise ConvertionException('Слишком много парааметров.')

            quote, base, amount = values
            total_base = CryptoConverter.convert(quote, base, amount)
        except ConvertionException as e:
            bot.reply_to(message, f'Ошибка пользователя. \n{e}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}')

        else:
            text = f'Цена {amount} {quote} в {base} - {total_base}'
            bot.send_message(message.chat.id, text)

            total_base = CryptoConverter.convert(quote, base, amount)


bot.polling()
