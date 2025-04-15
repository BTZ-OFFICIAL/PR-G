import telebot
from transformers import pipeline
import os

# Получаем токен бота из переменной окружения (чтобы не светить его в коде!)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# Загружаем модель для генерации текста
generator = pipeline('text-generation', model='sberbank-ai/rugpt3large_based_on_gpt2')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который умеет генерировать текст. Отправь мне что-нибудь, и я попробую это продолжить!")

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def generate_text(message):
    try:
        # Генерируем текст на основе сообщения пользователя
        generated_text = generator(message.text, max_length=200, num_return_sequences=1)[0]['generated_text']
        bot.reply_to(message, generated_text)
    except Exception as e:
        bot.reply_to(message, f"Упс, что-то пошло не так: {e}")

# Запускаем бота
bot.infinity_polling()
