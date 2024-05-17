import telebot as tb

from API_funcs import get_data
from settings import bot_token

# Инициализация бота
bot = tb.TeleBot(bot_token)

# Создание клавиатуры
action_keyboard = tb.types.ReplyKeyboardMarkup()
action_keyboard.row(tb.types.KeyboardButton("Получить список"))


# Отработка старта бота
@bot.message_handler(commands=['start', 'restart'])
def welcome(message):
    bot.send_message(
        message.from_user.id,
        'Для получения списка организаций находящихся в определенной области нажмите на кнопку <b>"Получить список"</b>',
        parse_mode='html',
        reply_markup=action_keyboard
    )


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id

        if "Получить список" == message.text:
            bot.send_message(
                user_id,
                "Введите две пары широты и долготы\n\n<b>Например:</b> \n43.1181166, 131.8863094 \n43.1181166, 131.8863094",
                parse_mode='html',
                reply_markup=action_keyboard
            )
            bot.register_next_step_handler(message, send_data)


# Шаг по обработке сообщения и формировании отчета
def send_data(mes):
    user_id = mes.chat.id
    try:
        lat1, lon1, lat2, lon2 = [float(num) for num in mes.text.replace('\n', ' ').replace(',', ' ').split()]
        dataCount = get_data(lat1, lon1, lat2, lon2, user_id)
        bot.send_message(
            user_id,
            f'Было найдено {dataCount} организация в данной области.',
            parse_mode='html',
            reply_markup=action_keyboard
        )
        bot.send_document(user_id, open(f'{user_id}_output.csv', mode='rb'))
    except Exception:
        bot.send_message(
            user_id,
            "Возможно вы ошиблись при вводе. Повторите попытку пожалуйста.\n"
            "Дробные числа вводите через ТОЧКУ.\n<b>Например:</b> \n43.1181166, 131.8863094 \n43.1181166, 131.8863094",
            parse_mode='html'
        )
        bot.register_next_step_handler(mes, send_data)


if __name__ == '__main__':
    bot.enable_save_next_step_handlers(delay=1)
    bot.load_next_step_handlers()
    bot.polling(skip_pending=True)
