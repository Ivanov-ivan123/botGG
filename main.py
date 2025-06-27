import telebot
from telebot import types
import time

BOT_TOKEN = '8132206321:AAF5tzB0T8WEJrdMaLFmrrnMLnKM7t0lsQk'

SPONSOR_CHANNELS = [
    'https://t.me/+YhHwXw-c7T03YTEy',
    'https://t.me/gg_team_13'
]

bot = telebot.TeleBot(BOT_TOKEN)

PHOTO_URL = 'https://i.ibb.co/1t4sn358/photo-2025-06-26-12-08-01.jpg'

START_TEXT = (
    "Літній підгон для наших людей від спонсорів каналів.\n\n"
    "Буде роздано 3 таких подарунків! Та 33 преміум на 12 місяців!\n\n"
    "Шо потрібно зробити? Все просто!\n\n"
    "Натисни «хочу»"
)

STEP_2_TEXT = (
    "Хочемо відразу сказати:\n\n"
    "⭐це все безкоshтвно\n"
    "⭐ми не потребуємо ніякої вашої інформації\n"
    "(це наш єдиний офіційний бот)"
)

STEP_3_TEXT = "Розіграш буде 07.07.2025\n\nЩоб приймати участь натисни ⬇"

STEP_4_TEXT = (
    "Ми дуже старались та хотіли б порадувати кожного нашого підписника.\n\n"
    "В нас є лише одна легка умова.\n"
    "Потрібно підписатись на наших спонсорів.\n\n"
    "⭐️ [ПЕРШИЙ КАНАЛ](https://t.me/+YhHwXw-c7T03YTEy)\n"
    "⭐️ [ДРУГИЙ КАНАЛ](https://t.me/gg_team_13)\n\n"
    "Після підписки тобі потрібно поставити ❤️ на кожний останній допис в группі."
)

SUCCESS_TEXT = "✅ Вітаємо! Ви успішно взяли участь у розіграші! Очікуйте результати 07.07.2025 🎉"
FAIL_TEXT = "❌ Ви не підписані на всі канали. Підпишіться та повторіть спробу."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("ХОЧУ"))
    bot.send_photo(message.chat.id, photo=PHOTO_URL, caption=START_TEXT, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "ХОЧУ")
def step_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("ЗАБРАТЬ"))
    bot.send_message(message.chat.id, STEP_2_TEXT, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "ЗАБРАТЬ")
def step_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("ТУТ"))
    bot.send_message(message.chat.id, STEP_3_TEXT, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "ТУТ")
def step_4(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ПЕРЕВІРИТИ ПІДПИСКУ ТА ПОЛУЧИТИ ПЕПУ", callback_data="check_subscription"))
    bot.send_message(message.chat.id, STEP_4_TEXT, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'check_subscription')
def handle_check_subscription(call):
    user_id = call.from_user.id
    is_subscribed = True

    for link in SPONSOR_CHANNELS:
        try:
            channel_username = link.split("/")[-1].replace("+", "")
            chat = bot.get_chat(channel_username)
            member = bot.get_chat_member(chat.id, user_id)
            if member.status in ['left', 'kicked']:
                is_subscribed = False
                break
        except Exception as e:
            print(f"Error checking {link}: {e}")
            is_subscribed = False
            break
        time.sleep(1)

    if is_subscribed:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=SUCCESS_TEXT
        )
    else:
        bot.answer_callback_query(
            call.id,
            text=FAIL_TEXT,
            show_alert=True
        )

print("Бот запущен...")
bot.infinity_polling()
