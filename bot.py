import logging
import os

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
PRICE_LIMIT = 60000
CHECK_INTERVAL_SECONDS = 60


def get_crypto_price() -> float:
    response = requests.get(COINGECKO_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["bitcoin"]["usd"]


async def alarm_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        price = get_crypto_price()
        if price < PRICE_LIMIT:
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f"⚠️ DİKKAT! Bitcoin fiyatı ${PRICE_LIMIT:,} altına düştü: ${price}",
            )
    except Exception as exc:
        logger.exception("Alarm callback failed: %s", exc)


async def set_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()

    context.job_queue.run_repeating(
        alarm_callback,
        interval=CHECK_INTERVAL_SECONDS,
        first=1,
        chat_id=chat_id,
        name=str(chat_id),
    )
    await update.message.reply_text(
        f"Alarm kuruldu! Bitcoin ${PRICE_LIMIT:,} altına düşerse haber vereceğim."
    )


async def stop_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    if not jobs:
        await update.message.reply_text("Aktif alarm bulunmuyor.")
        return

    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text("Alarm durduruldu.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Selam! /fiyat ile güncel Bitcoin fiyatını görebilir, /setalarm ile takip başlatabilir, /stopalarm ile alarmı durdurabilirsin."
    )


async def fiyat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        price = get_crypto_price()
        await update.message.reply_text(f"Güncel Bitcoin fiyatı: ${price}")
    except Exception as exc:
        logger.exception("Price fetch failed: %s", exc)
        await update.message.reply_text("Fiyat alınırken bir hata oluştu. Lütfen tekrar dene.")


if __name__ == "__main__":
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN ortam değişkeni tanımlı değil.")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fiyat", fiyat))
    application.add_handler(CommandHandler("setalarm", set_alarm))
    application.add_handler(CommandHandler("stopalarm", stop_alarm))

    print("Bot çalışıyor...")
    application.run_polling()
