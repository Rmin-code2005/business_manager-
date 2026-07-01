from locale import currency
import os
import logging
import requests

from dotenv import load_dotenv

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# -------------------
# ENV
# -------------------
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")  # register telegram endpoint
BASE_URL = "http://127.0.0.1:8000/api"

# -------------------
# LOGGING
# -------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# -------------------
# KEYBOARD
# -------------------
keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📊 Live prices")],
        [
            KeyboardButton("💵 Dollar basket"),
            KeyboardButton("🥇 Gold basket"),
        ],
        [
            KeyboardButton("₿ Crypto basket"),
        ],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


# -------------------
# START
# -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_user = update.effective_user

    if telegram_user.username is None:
        await update.message.reply_text(
            "ابتدا برای حساب تلگرام خود یک Username انتخاب کنید."
        )
        return

    payload = {
        "telegram_username": f"@{telegram_user.username}",
        "telegram_user_id": telegram_user.id,
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10,
        )

        if response.status_code == 200:

            data = response.json()

            context.user_data["telegram_token"] = data["telegram_token"]

            await update.message.reply_text(
                "✅ حساب شما با موفقیت متصل شد.",
                reply_markup=keyboard,
            )

        elif response.status_code == 404:

            await update.message.reply_text(
                "❌ ابتدا Username تلگرام خود را در سایت ثبت کنید."
            )

        elif response.status_code == 409:

            await update.message.reply_text(
                "⚠️ این حساب تلگرام قبلاً به کاربر دیگری متصل شده است."
            )

        else:

            await update.message.reply_text(
                "❌ خطایی در سرور رخ داد."
            )

    except requests.exceptions.RequestException:

        await update.message.reply_text(
            "❌ ارتباط با سرور برقرار نشد."
        )


# -------------------
# MENU
# -------------------

def format_prices(title: str, data: dict) -> str:

    prices = data["data"]["prices"]

    lines = [f"📊 {title}\n"]

    for symbol, info in prices.items():

        current = info["current"]
        min_1h = info["min"]["1hour"]
        max_1h = info["max"]["1hour"]

        lines.append(
            f"💱 {symbol}\n"
            f"   ├ 💰 Current: {current}\n"
            f"   ├ 📉 Min (1h): {min_1h}\n"
            f"   └ 📈 Max (1h): {max_1h}\n"
        )

    return "\n".join(lines)
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    token = context.user_data.get("telegram_token")

    if token is None:

        await update.message.reply_text(
            "ابتدا /start را اجرا کنید."
        )
        return

    headers = {
        "X-Telegram-Token": token
    }

    try:

        # -------------------
        # LIVE PRICES
        # -------------------

        if text == "📊 Live prices":

            currency = requests.get(f"{BASE_URL}/currency/prices/", headers=headers, timeout=10)
            currency_text = format_prices("Currency", currency.json())

            gold = requests.get(
                f"{BASE_URL}/gold/prices/",
                headers=headers,
                timeout=10,
            )
            gold_text = format_prices("Gold", gold.json())
            crypto = requests.get(
                f"{BASE_URL}/crypto/prices/",
                headers=headers,
                timeout=10,
            )
            crypto_text = format_prices("Crypto", crypto.json())
            message = (
                "📊 Live Prices\n\n"
                f"💵 Currency\n{currency_text}\n\n"
                f"🥇 Gold\n{gold_text}\n\n"
                f"₿ Crypto\n{crypto_text}"
            )

            await update.message.reply_text(message)

        # -------------------
        # USD
        # -------------------

        elif text == "💵 Dollar basket":

            res = requests.get(
                f"{BASE_URL}/usd-basket/",
                headers=headers,
                timeout=10,
            )

            await update.message.reply_text(res.text)

        # -------------------
        # GOLD
        # -------------------

        elif text == "🥇 Gold basket":

            res = requests.get(
                f"{BASE_URL}/gold-basket/",
                headers=headers,
                timeout=10,
            )

            await update.message.reply_text(res.text)

        # -------------------
        # CRYPTO
        # -------------------

        elif text == "₿ Crypto basket":

            res = requests.get(
                f"{BASE_URL}/crypto-basket/",
                headers=headers,
                timeout=10,
            )

            await update.message.reply_text(res.text)

        else:

            await update.message.reply_text(
                "دستور نامعتبر است."
            )

    except requests.exceptions.RequestException:

        await update.message.reply_text(
            "❌ ارتباط با سرور برقرار نشد."
        )


# -------------------
# MAIN
# -------------------
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_handler,
        )
    )

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()