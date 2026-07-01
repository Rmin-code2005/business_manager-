import os
import logging
import requests

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    PicklePersistence,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_user = update.effective_user

    username = '@'+telegram_user.username
    print(f"Username: {username}")
    telegram_user_id = telegram_user.id

    if username is None:
        await update.message.reply_text(
            "ابتدا برای اکانت تلگرام خود یک Username انتخاب کنید."
        )
        return

    payload = {
        "telegram_username": username,
        "telegram_user_id": telegram_user_id,
    }
    if context.user_data.get("linked", False):
        await update.message.reply_text(
            "✅ حساب شما قبلاً متصل شده است."
        )
        return
    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=10,
        )

        if response.status_code == 200:
            context.user_data["linked"] = True

            await update.message.reply_text(
            "✅ حساب شما با موفقیت متصل شد."
            )

        elif response.status_code == 404:
            await update.message.reply_text(
                "❌ ابتدا Username تلگرام خود را در سایت ثبت کنید."
            )

        elif response.status_code == 409:
            await update.message.reply_text(
                "⚠️ این حساب قبلاً متصل شده است."
            )

        else:
            await update.message.reply_text(
                "خطایی در سرور رخ داد."
            )

    except Exception:
        await update.message.reply_text(
            "ارتباط با سرور برقرار نشد."
        )


def main():

    persistence = PicklePersistence(filepath="bot_data.pkl")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .persistence(persistence)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()