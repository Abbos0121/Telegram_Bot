import telebot
from telebot import types

bot = telebot.TeleBot('6469384473:AAGHd-SwNvBqOoUmUhVlKOAyBThai7-lgSA')

user_language = {}
user_data = {}

# States
STATE_SELECT_LANGUAGE = "select_language"
STATE_ENTER_NAME = "enter_name"
STATE_ENTER_PHONE = 3


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('English', 'Русский', 'O\'zbek')
    bot.send_message(message.chat.id, "Choose your language / Выберите язык / Tilni tanlang:", reply_markup=markup)

    user_data[message.chat.id] = {'state': STATE_ENTER_NAME}


@bot.message_handler(func=lambda message: message.text in ['English', 'Русский', 'O\'zbek'])
def set_language(message):
    selected_language = message.text.lower()
    user_data[message.chat.id] = {'language': selected_language}

    if message.text == 'English':
        bot.send_message(message.chat.id, f"Language set to {selected_language.lower()}.")
        bot.send_message(message.chat.id, "Please enter your first and lastname:")
        user_data[message.chat.id]['state'] = STATE_ENTER_NAME
    if message.text == 'Русский':
        bot.send_message(message.chat.id, f"Вы выбрали {selected_language.lower()} язык.")
        bot.send_message(message.chat.id, "Пожалуйста введите ваше имя и фамилию:")
        user_data[message.chat.id]['state'] = STATE_ENTER_NAME
    elif message.text == 'O\'zbek':
        bot.send_message(message.chat.id, f"Siz {selected_language.lower()} tilini tanladingiz.")
        bot.send_message(message.chat.id, "Iltimos ism familiyangizni kiriting:")
        user_data[message.chat.id]['state'] = STATE_ENTER_NAME


@bot.message_handler(func=lambda message: user_data[message.chat.id]['state'] == STATE_ENTER_NAME)
def process_name(message):
    name = message.text.strip()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    request_contact_button = types.KeyboardButton(text="📲 Отправить номер телефона", request_contact=True)
    keyboard.add(request_contact_button)
    bot.send_message(message.chat.id, f"Великолепно {name}")
    bot.send_message(message.chat.id, f"Нажмите на кнопку чтобы отправить свой номер телефона:",
                     reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        phone = message.contact.phone_number
        bot.send_message(message.chat.id, f"Ваш номер телефона {phone} был сохранён.")
        bot.send_message(message.chat.id, "🎉 Поздравляю, вы успешно зарегистрировались в боте, для продолжения нажмите /continue")
        user_data[message.chat.id]['state'] = None
        user_data[message.chat.id]['name'] = None


@bot.message_handler(commands=['continue'])
def continue_bot(message):
    website_link = "https://example.com"
    keyboard = types.InlineKeyboardMarkup()
    my_profile_button = types.InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile")
    support_button = types.InlineKeyboardButton(text="🧯 Служба поддержки", callback_data="support")
    rules_button = types.InlineKeyboardButton(text="📖 Правила", callback_data="rules")
    share_button = types.InlineKeyboardButton(text="🔺 Поделиться", switch_inline_query="")

    keyboard.add(my_profile_button, support_button, rules_button, share_button)

    bot.send_message(message.chat.id,
                     f"Добро пожаловать в телеграм-бот интернет-магазина <a href='{website_link}'>Online_Store.uz</a>",
                     parse_mode="html", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "my_profile")
def my_profile_callback(call):
    user = call.from_user
    user_id = user.id
    user_name = user.first_name

    if user.username:
        user_username = f"@{user.username}"
    else:
        user_username = "Нет username"

    profile_info = f"Имя: {user_name}\nID: {user_id}\nUsername: {user_username}"

    bot.send_message(user_id, "Это ваш профиль!\n" + profile_info)


@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_callback(call):
    user_id = call.from_user.id


@bot.callback_query_handler(func=lambda call: call.data == "rules")
def support_c(call):

    bot.send_message(call.message.chat.id, "Уважение пользователей: Обязательно соблюдайте уважение к пользователям. Избегайте оскорбительных, непристойных или дискриминационных сообщений.Четкая функциональность: Определите функции бота и убедитесь, что он выполняет их четко и эффективно. Не давайте боту излишнюю сложность, сосредоточьтесь на основных задачах.Безопасность данных: Защищайте данные пользователей. Не храните или передавайте личную информацию без разрешения пользователя.Не спамить: Не посылайте нежелательные сообщения пользователям и не рекламируйте ничего, что не связано с функциональностью бота.Ответы на сообщения: Сделайте бота отзывчивым и предоставьте информацию, которую пользователи запрашивают.")


@bot.callback_query_handler(func=lambda call: call.data == "support")
def support_c(call):
    telegram_link = "https://t.me/abbos010101"

    bot.send_message(call.message.chat.id, f"<a href='{telegram_link}'>Чат поддержки</a>",
                     parse_mode="html")


@bot.message_handler()
def get_user_text(message):
    bot.send_message(message.chat.id, 'Пожалуйста введите команду ☺️', parse_mode='html')


bot.polling(none_stop=True)







