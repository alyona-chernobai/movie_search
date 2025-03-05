import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from db import Database
from config import API_KEY

TOKEN = API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

db = Database()

logging.basicConfig(level=logging.INFO)


@dp.message(lambda message: message.text.lower().startswith("/start"))
async def start_command(message: Message):
    await message.answer("🎬 Привет! Я бот для поиска фильмов.\n\n"
                         "🔍 Поиск по ключевому слову: /search <слово>\n"
                         "🎭 Поиск по жанру и году: /genre <жанр> <год>\n"
                         "📊 Популярные запросы: /history")


@dp.message(lambda message: message.text.lower().startswith("/search"))
async def search_command(message: Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("❌ Ошибка! Введите ключевое слово после команды.\nПример: `/search Baby`")
        return

    keyword = parts[1]
    results = db.search_by_keyword(keyword)

    if results:
        text = "\n".join([f"🎬 {film['title']} ({film['release_year']})" for film in results])
    else:
        text = "❌ Фильмы не найдены."

    await message.answer(text)


@dp.message(lambda message: message.text.lower().startswith("/genre") or message.text.lower().startswith("/gerne"))
async def genre_command(message: Message):
    parts = message.text.split(maxsplit=2)

    if parts[0].lower() == "/gerne":
        await message.answer("❌ Возможно, вы ошиблись. Правильная команда: `/genre <жанр> <год>`")
        return

    if len(parts) < 3:
        await message.answer("❌ Ошибка! Введите жанр и год через пробел.\nПример: `/genre Horror 1995`")
        return

    genre, year = parts[1], parts[2]

    if not year.isdigit():
        await message.answer("❌ Ошибка! Год должен быть числом. Пример: `/genre Action 2006`")
        return

    results = db.search_by_genre_year(genre, int(year))
    if results:
        text = "\n".join([f"🎬 {film['title']} ({film['release_year']})" for film in results])
    else:
        text = "❌ Фильмы не найдены."

    await message.answer(text)


@dp.message(lambda message: message.text.lower() == "/history")
async def history_command(message: Message):
    results = db.get_popular_queries()

    if results:
        text = "\n".join([f"🔍 {row['query_text']} - {row['search_count']} раз" for row in results])
    else:
        text = "📊 Пока нет популярных запросов."

    await message.answer(text)


async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
