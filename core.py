import telebot
from telebot import types
import bot_functions as bf


def main():
    # This is our Telegram bot token. You can get one here -> https://t.me/BotFather
    token = "123456:abcdefghijklmn"
    
    try:
        bot = telebot.TeleBot(token)
        bot.get_me()
        print('Connection to the bot was successful!')

    except telebot.apihelper.ApiException:
        print('A request to the Telegram API was unsuccessful.')


    print("Book Store is started!")

    @bot.message_handler(commands=["start"])
    def start(message):
        bf.sending_start_message(bot, message, types)
        bf.start_func(message)

    @bot.message_handler(commands=["help"])
    def helping(message):
        bf.sending_help_message(bot, message)

    @bot.message_handler(content_types=["text"])
    def message_handler(message):
        if message.chat.type == 'private':
            bf.handler(bot, types, message, None)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        bf.handler(bot, types, None, call)

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
