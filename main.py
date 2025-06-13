import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Вставьте сюда ваш токен
TOKEN = '8098389316:AAEMKwE8BN-BVIOQJLAFHMR2au3WkYSHRlU'

# Функция парсинга сайта
def get_results(url):
    try:
        response = requests.get(url)
        print(f"Запрос к {url} — статус: {response.status_code}")
        if response.status_code != 200:
            return f"Ошибка: сайт недоступен (статус {response.status_code})"
        soup = BeautifulSoup(response.text, 'html.parser')
        # ВАЖНО: нужные результаты нужно найти в правильном блоке. Ниже пример.
        # Напишите селектор, соответствующий структуре сайта.
        # Ниже — общий пример получения текста, адаптируйте под сайт.
        # Пример: все результаты в таблице с классом 'result-table'
        result_block = soup.find('div', class_='result')  # Замените на правильный селектор
        if result_block:
            text = result_block.get_text(separator='\n', strip=True)
            return text[:2000]  # Ограничение длины
        else:
            # Если не нашли, возвращаем весь текст страницы — или сообщение
            full_text = soup.get_text(separator=' ', strip=True)
            return full_text[:2000]
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return "Ошибка при получении данных"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Лотерея 6/52", callback_data='6_52')],
        [InlineKeyboardButton("Кено 20/80", callback_data='20_80')],
        [InlineKeyboardButton("Максима 5/45", callback_data='5_45')],
        [InlineKeyboardButton("Лото 6/36", callback_data='6_36')],
        [InlineKeyboardButton("Сделать ставку", callback_data='make_bet')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите игру:', reply_markup=reply_markup)

# Обработчик нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print(f"Кнопка нажата: {query.data}")

    url_mapping = {
        '6_52': 'https://unl.ua/uk/games/superloto/results',
        '20_80': 'https://unl.ua/uk/games/keno/results',
        '5_45': 'https://unl.ua/uk/games/maxima/results',
        '6_36': 'https://unl.ua/uk/games/loto636/results'
    }

    if query.data in url_mapping:
        url = url_mapping[query.data]
        results = get_results(url)
        await query.edit_message_text(text=f"Результаты:\n{results}")
    elif query.data == 'make_bet':
        await query.edit_message_text(text="Функционал для ставки еще в разработке...")

# Основная часть запуска
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот запущен")
    app.run_polling()
