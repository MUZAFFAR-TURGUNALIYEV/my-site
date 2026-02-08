import requests
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ===== SOZLAMALAR =====
BOT_TOKEN = "8416322180:AAHmCyi8nC6xTboWfE-VxQ44AvpNpgknPlo"
CITY = "Sirdaryo"
COUNTRY = "Uzbekistan"
METHOD = 2  # hisoblash usuli

# ===== NAMOZ VAQTLARINI API DAN OLISH =====
def get_prayer_times():
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": CITY,
        "country": COUNTRY,
        "method": METHOD
    }
    r = requests.get(url, params=params).json()
    t = r["data"]["timings"]

    return [
        ("Bomdod", t["Fajr"]),
        ("Peshin", t["Dhuhr"]),
        ("Asr", t["Asr"]),
        ("Shom", t["Maghrib"]),
        ("Xufton", t["Isha"]),
    ]

# ===== HAMMA NAMOZ VAQTLARINI MATNGA OLIB BERISH =====
def get_all_prayer_times_text():
    prayers = get_prayer_times()
    text = f"🕌 Bugungi namoz vaqtlari ({CITY})\n\n"
    for name, time in prayers:
        text += f"{name}: {time}\n"
    return text

# ===== /start HANDLER =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🕌 Bugungi namoz vaqtlari", callback_data="now")]
    ])
    await update.message.reply_text(
        "Assalomu alaykum! Namoz vaqtlari botiga xush kelibsiz Dada ",
        reply_markup=keyboard
    )

# ===== TUGMA BOSILGANDA =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = get_all_prayer_times_text()
    await query.message.reply_text(
        text + "\n\nAlloh qabul qilsin 🤲"
    )

# ===== ISHGA TUSHIRISH =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="now"))

    print("🤖 Namoz boti ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
