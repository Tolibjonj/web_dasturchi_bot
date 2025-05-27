import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7796046680:AAGLkRTcPuqLaeHFl2nkIytgHjMPHXvU2ho'  # BotFather'dan olingan token
ADMIN_CHAT_ID = 7580525260       # Admin Telegram ID (o'zingizni yozing)

bot = telebot.TeleBot('7796046680:AAGLkRTcPuqLaeHFl2nkIytgHjMPHXvU2ho')

# Til sozlamalari
languages = {
    'uz': {
        'choose_service': "Assalomu alaykum, xizmat turini tanlang:",
        'project_prompt': "{service} xizmatini tanladingiz.\nIltimos, loyiha haqida batafsil yozing:",
        'payment_prompt': "Rahmat! Endi quyidagi to'lov usullaridan birini tanlang:",
        'unknown': "Iltimos, menyudan bir xizmat tanlang yoki /start buyrug'ini bosing.",
        'services': [
            "🌐 Web sayt yaratish",
            "📱 Ilova yaratish",
            "🤖 Telegram bot yaratish",
            "💻 IT dasturlarga yordam"
        ]
    },
    'ru': {
        'choose_service': "Здравствуйте, выберите тип услуги:",
        'project_prompt': "Вы выбрали услугу: {service}\nПожалуйста, опишите ваш проект подробнее:",
        'payment_prompt': "Спасибо! Теперь выберите способ оплаты ниже:",
        'unknown': "Пожалуйста, выберите услугу из меню или нажмите /start.",
        'services': [
            "🌐 Создание веб-сайта",
            "📱 Создание приложения",
            "🤖 Создание Telegram-бота",
            "💻 IT-помощь"
        ]
    },
    'en': {
        'choose_service': "Hello, please choose a service:",
        'project_prompt': "You selected: {service}\nPlease describe your project in detail:",
        'payment_prompt': "Thank you! Now choose one of the payment methods below:",
        'unknown': "Please select a service from the menu or type /start.",
        'services': [
            "🌐 Website creation",
            "📱 App development",
            "🤖 Telegram bot development",
            "💻 IT support"
        ]
    }
}

user_lang = {}

# Til tanlash
@bot.message_handler(commands=['start'])
def start(message):
    lang_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    lang_markup.add(KeyboardButton("O'zbek"), KeyboardButton("Русский"), KeyboardButton("English"))
    bot.send_message(message.chat.id, "Tilni tanlang / Choose language / Выберите язык:", reply_markup=lang_markup)

@bot.message_handler(func=lambda m: m.text in ["O'zbek", "Русский", "English"])
def set_language(message):
    lang_map = {"O'zbek": 'uz', "Русский": 'ru', "English": 'en'}
    lang = lang_map[message.text]
    user_lang[message.chat.id] = lang

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for service in languages[lang]['services']:
        markup.add(KeyboardButton(service))
    # Qo'shimcha murojaat qilish tugmasi
    if lang == 'uz':
        markup.add(KeyboardButton("📞 Murojaat qilish"))
    elif lang == 'ru':
        markup.add(KeyboardButton("📞 Связаться"))
    else:  # 'en'
        markup.add(KeyboardButton("📞 Contact"))

    bot.send_message(
        message.chat.id,
        languages[lang]['choose_service'],
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: any(m.text in languages[lang]['services'] for lang in languages))
def handle_service(message):
    lang = user_lang.get(message.chat.id, 'uz')
    service = message.text
    bot.send_message(
        message.chat.id,
        languages[lang]['project_prompt'].format(service=service)
    )
    bot.register_next_step_handler(message, lambda msg: get_project_details(msg, service, lang))

def get_project_details(message, service_type, lang):
    project_info = message.text
    
    pay_markup = InlineKeyboardMarkup(row_width=2)
    pay_markup.add(
        InlineKeyboardButton("Click", url="https://my.click.uz"),
        InlineKeyboardButton("Payme", url="https://checkout.paycom.uz"),
        InlineKeyboardButton("Stripe (Visa/MasterCard)", url="https://buy.stripe.com/test_00g9DN4XdeZCgUMdQQ"),
        InlineKeyboardButton("Crypto (USDT, BTC)", url="https://commerce.coinbase.com")
    )

    bot.send_message(ADMIN_CHAT_ID, f"\u2709\ufe0f Yangi buyurtma:\n\nXizmat turi: {service_type}\n\nTafsilot: {project_info}\n\nFoydalanuvchi: @{message.from_user.username} ({message.chat.id})")

    bot.send_message(message.chat.id, languages[lang]['payment_prompt'], reply_markup=pay_markup)

@bot.message_handler(func=lambda m: m.text in ["📞 Murojaat qilish", "📞 Связаться", "📞 Contact"])
def contact_admin(message):
    lang = user_lang.get(message.chat.id, 'uz')
    if lang == 'uz':
        contact_text = "Biz bilan bog‘laning:\n\nTelegram: @Web_sayt_dasturchi\nTelefon: +998505253330"
    elif lang == 'ru':
        contact_text = "Свяжитесь с нами:\n\nTelegram: @Web_sayt_dasturchi\nТелефон: +998505253330"
    else:
        contact_text = "Contact us:\n\nTelegram: @Web_sayt_dasturchi\nPhone: +998505253330"

    bot.send_message(message.chat.id, contact_text)

@bot.message_handler(func=lambda m: True)
def fallback(message):
    lang = user_lang.get(message.chat.id, 'uz')
    bot.send_message(message.chat.id, languages[lang]['unknown'])

bot.polling()
 