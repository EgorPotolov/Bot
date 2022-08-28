import telebot
from config import keys, TOKEN
from extensions import ConvertionException, СurrencyConverter


bot = telebot.TeleBot(TOKEN)

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
            total_base = СurrencyConverter.convert(quote, base, amount)
        except ConvertionException as e:
            bot.reply_to(message, f'Ошибка пользователя. \n{e}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}')

        else:
            text = f'Цена {amount} {quote} в {base} - {total_base}'
            bot.send_message(message.chat.id, text)

            total_base = СurrencyConverter.convert(quote, base, amount)


bot.polling()
