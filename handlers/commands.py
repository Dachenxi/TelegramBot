from telegram import Update, error
from telegram.ext import CommandHandler, ContextTypes, Application
from utils.api_utils import generate_sticker
import asyncio

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya adalah bot download Instagram.\n"
        "Kirimkan saya link post Instagram dan saya akan mendownloadnya untuk Anda."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Cara menggunakan bot:
1. Kirim link post Instagram
2. Tunggu beberapa saat
3. Bot akan mengirimkan media dari post tersebut
""")

async def stiker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler untuk perintah /stiker.
    Menggunakan API untuk menghasilkan stiker dengan teks.
    """
    if not context.args:
        await update.message.reply_text("❌ Anda harus memberikan teks setelah perintah /stiker. Contoh: /stiker HALO ASU")
        return
    
    text = " ".join(context.args)  # Gabungkan teks setelah /stiker
    try:
        sticker_path = generate_sticker(text)
        if sticker_path:
            with open(sticker_path, "rb") as sticker_file:
                await update.message.reply_document(document=sticker_file)
        else:
            await update.message.reply_text("❌ Gagal membuat stiker. Coba lagi nanti.")
    except error.NetworkError as e: 
        await asyncio.sleep(2)
    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi kesalahan: {e}")

def register_command_handlers(application: Application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stiker", stiker_command)) 
