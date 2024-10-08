import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai

# Чтение токенов из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('7562566219:AAGIS0sKuX2M7__e9rSf8Vu9WPtXxrYykLM')
OPENAI_API_KEY = os.getenv('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')

# Устанавливаем API-ключ OpenAI
openai.api_key = OPENAI_API_KEY

# Приветственное сообщение
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я помогу тебе с диагностикой автомобиля. Введи описание проблемы.")

# Обработка сообщений
async def handle_message(update: Update, context):
    user_message = update.message.text
    prompt = f"""
    Ты опытный автомеханик. Для того чтобы помочь пользователю диагностировать поломку автомобиля, спроси марку и год выпуска авто, а затем уточни описание проблемы. После этого предложи возможные причины поломки.
    Пользователь: {user_message}
    Механик:
    """

    # Запрос к OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    # Ответ бота
    await update.message.reply_text(response.choices[0].text.strip())

# Основная функция запуска
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Обработчик команды /start
    start_handler = CommandHandler('start', start)

    # Обработчик сообщений
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

    # Добавляем обработчики в приложение
    app.add_handler(start_handler)
    app.add_handler(message_handler)

    # Запуск бота
    app.run_polling()
