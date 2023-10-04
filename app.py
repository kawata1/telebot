import telebot
from config import keys, TOKEN
from extensions import  ConvertionException, CurrentConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду: \n<название валюты> \
<в какую валюту перевести> <номинал>\nЧтобы увидеть список доступной валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступная валюта:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много значений.')

        quote, base, amount = values
        total_base = CurrentConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Боту не удалось выполнить команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert_currency(message):
    try:
        current, amount = message.text.split()
        raise APIException('Неправильно введен код валюты или количество')

    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')

    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: {e}')

bot.polling()