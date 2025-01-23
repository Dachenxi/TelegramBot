from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, Application
from utils.instagram import download_instagram_post
from utils.file_utils import clear_temp_folder

async def handle_instagram_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    url = message.text
    if "instagram.com" not in url:
        return
    status_message = await message.reply_text("⏳ Sedang mengunduh post...")
    try:
        media_files = download_instagram_post(url)
        for media in media_files:
            await context.bot.send_document(chat_id=message.chat_id, document=open(media, 'rb'))
        await status_message.edit_text("✅ Download selesai!")
        await status_message.delete()
        clear_temp_folder()
    except Exception as e:
        await status_message.edit_text(f"❌ Terjadi kesalahan: {e}")

def register_message_handlers(application: Application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_url))
