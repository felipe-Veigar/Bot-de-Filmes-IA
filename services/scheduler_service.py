from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.tmdb_service import get_trending_movies
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, CHAT_ID

scheduler = AsyncIOScheduler()


async def send_trending_alert():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    movies = get_trending_movies()

    top3 = movies[:3]

    message = "🎬 Top 3 Filmes em Tendência\n\n"

    for index, movie in enumerate(top3, start=1):
        message += (
            f"{index}. {movie['title']}\n"
            f"⭐ Popularidade: {movie['popularity']}\n\n"
        )

    await bot.send_message(chat_id=CHAT_ID, text=message)


def start_scheduler():
    scheduler.add_job(
        send_trending_alert,
        "interval",
        hours=12
    )

    scheduler.start()
