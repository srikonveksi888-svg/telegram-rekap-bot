from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from datetime import datetime

TOKEN = "8917415626:AAFuOVMBQvmIi2okJYIppxublPlxXLrL5MU"

CS_CODES = ["AB01", "AB02", "AB03", "AB04", "AB05", "AB07", "AB08"]

data_harian = {}

tanggal_sekarang = datetime.now().strftime("%Y-%m-%d")


def cek_ganti_hari():
    global tanggal_sekarang
    global data_harian

    hari_ini = datetime.now().strftime("%Y-%m-%d")

    if hari_ini != tanggal_sekarang:
        tanggal_sekarang = hari_ini
        data_harian = {}


async def baca_pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global data_harian

    cek_ganti_hari()

    if update.message and update.message.text:
        text = update.message.text.upper()

        for cs in CS_CODES:
            if cs in text:

                if cs not in data_harian:
                    data_harian[cs] = 0

                data_harian[cs] += 1


async def total_hari_ini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cek_ganti_hari()

    sekarang = datetime.now()

    hari_indonesia = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu",
    }

    nama_hari = hari_indonesia[sekarang.strftime("%A")]

    tanggal = sekarang.strftime("%d-%m-%Y")

    pesan = f"📊 REKAP ORDER HARI INI\n"
    pesan += f"{nama_hari}, {tanggal}\n\n"

    total_semua = 0

    for cs in CS_CODES:
        jumlah = data_harian.get(cs, 0)

        pesan += f"{cs} TOTAL INPUT : {jumlah}\n"

        total_semua += jumlah

    pesan += f"\n━━━━━━━━━━\n\n"
    pesan += f"TOTAL SEMUA : {total_semua} INPUT"

    await update.message.reply_text(pesan)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Rekap Aktif ✅")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("totalhariini", total_hari_ini))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, baca_pesan))

print("BOT AKTIF...")

app.run_polling()