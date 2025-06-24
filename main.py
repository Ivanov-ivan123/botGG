import telebot
from telebot import types
import time

# НАСТРОЙКИ БОТА
BOT_TOKEN = '8132206321:AAF5tzB0T8WEJrdMaLFmrrnMLnKM7t0lsQk'  # Получите его у @BotFather

# СПИСОК КАНАЛОВ ДЛЯ ПРОВЕРКИ
SPONSOR_CHANNELS = [
    '@esskaa777',
    '@gg_gtc_music',
    '@vakansi_whatday'
]

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Тексты и данные
PHOTO_URL = 'https://pbt.storage.yandexcloud.net/cp_upload/b2e57cf2ea9c608669263b8651c7f686_full.jpeg'
START_TEXT = "летнему фестивалю быть! 🍉❕\n\nВ этом году мы решили порадовать пользователей супер-призом в виде телеграм-према на 3 месяца!!"
STEP_2_TEXT = "хотим сразу отметить, чтобы вы не беспокоились🖤:\n\n📌это беsплатно\n📌мы не требуем никаких ваших личных данных \n(это наш единственный официальный бот)"
STEP_3_TEXT = "Премиум будет действовать до конца лета 2025, то есть до 31.08.2025 ❤️‍🔥\n\nчтобы получить нажмите «забрать»"
STEP_4_TEXT = "Мы очень старались и хотели порадовать каждого пользователя совершенно безвозмездно🤍\n\nу нас есть всего одно легкое условие, после выполнения которого вы получите прем на 3 мес"
SPONSORS_TEXT = """Чтобы получить премиум на 3 месяца необходимо подписаться на спонсоров проекта:
@esskaa777
@gg_gtc_music
@vakansi_whatday
это единственное условие для получения!""".replace('_', '\\_').replace('!', '\\!')
SUCCESS_TEXT = "Отлично! Мои поздравления! Ожидай премиум в течении 24-х часов. Отписка от групп категорически запрещена! Перед выдачей прем всё будет повторно проверяться!"
FAIL_TEXT = "❌ Доступ ограничен из-за отсутствия подписки на один или несколько ресурсов. Пожалуйста, подпишитесь на все каналы и попробуйте снова."

# ОБРАБОТЧИКИ СООБЩЕНИЙ (КНОПКИ-ОТВЕТЫ)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("УЧАСТВУЮ")
    markup.add(button)
    bot.send_photo(
        message.chat.id,
        photo=PHOTO_URL,
        caption=START_TEXT,
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "УЧАСТВУЮ")
def step_2_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("ОТЛИЧНО")
    markup.add(button)
    bot.send_message(message.chat.id, STEP_2_TEXT, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "ОТЛИЧНО")
def step_3_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("ЗАБРАТЬ")
    markup.add(button)
    bot.send_message(message.chat.id, STEP_3_TEXT, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "ЗАБРАТЬ")
def step_4_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("ДАЛЕЕ")
    markup.add(button)
    bot.send_message(message.chat.id, STEP_4_TEXT, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "ДАЛЕЕ")
def step_5_handler(message):
    # Этот шаг использует ИНЛАЙН-кнопку
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("ПРОВЕРИТЬ ПОДПИСКУ И ПОЛУЧИТЬ МНЕ", callback_data='check_subscription')
    markup.add(button)
    # Отправляем сообщение со списком каналов и инлайн-кнопкой
    # И одновременно УДАЛЯЕМ клавиатуру с кнопками-ответами
    bot.send_message(
        message.chat.id,
        SPONSORS_TEXT,
        reply_markup=markup,
        parse_mode='MarkdownV2',  # Используем MarkdownV2
        disable_web_page_preview=True
    )

# ОБРАБОТЧИК ИНЛАЙН-КНОПКИ (ДЛЯ ПРОВЕРКИ ПОДПИСКИ)
@bot.callback_query_handler(func=lambda call: call.data == 'check_subscription')
def handle_check_subscription(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id, "🔎 Проверяем ваши подписки...")

    is_subscribed = True
    if not SPONSOR_CHANNELS:  # Если список каналов пуст
        bot.answer_callback_query(
            call.id,
            text="Доступ ограничен из-за отсутствия подписки на ресурс",
            show_alert=True
        )
        return
    else:
        for channel in SPONSOR_CHANNELS:
            try:
                if not channel:
                    continue
                chat_member = bot.get_chat_member(chat_id=channel, user_id=user_id)
                if chat_member.status in ['left', 'kicked']:
                    is_subscribed = False
                    break
            except Exception as e:
                print(f"Ошибка проверки канала {channel} для пользователя {user_id}: {e}")
                is_subscribed = False
                break
            time.sleep(2)  # Задержка для избежания лимитов Telegram API

    if is_subscribed:
        # Убираем инлайн кнопку после успешной проверки
        bot.edit_message_text(
            text=SUCCESS_TEXT,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
    else:
        bot.answer_callback_query(
            call.id,
            text=FAIL_TEXT,
            show_alert=True
        )

print("Бот запущен...")
bot.infinity_polling()
