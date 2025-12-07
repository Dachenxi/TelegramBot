from telegram import Update, error, InputFile
from telegram.ext import CommandHandler, ContextTypes
from utils.api_utils import generate_sticker
import asyncio
import io
import os
from typing import Any, Callable

async def _maybe_await(func: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Helper to call a function that might be sync or async.
    """
    result = func(*args, **kwargs)
    if asyncio.iscoroutine(result):
        return await result
    return result

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start command - show welcome / help text
    """
    start_text = (
        "🎉 **Selamat datang di Multi-Platform Media Downloader Bot!** 🎉\n\n"
        "🌟 Bot ini mendukung download dari berbagai platform:\n"
        "🎥 YouTube\n"
        "📸 Instagram\n"
        "👥 Facebook\n"
        "🐦 Twitter/X\n"
        "🎵 TikTok\n"
        "🤖 Reddit\n"
        "📹 Vimeo\n"
        "🎮 Twitch\n"
        "📌 Pinterest\n"
        "📝 Tumblr\n"
        "🎬 Dailymotion\n"
        "🎧 SoundCloud\n\n"
        "📌 **Cara Menggunakan:**\n"
        "Cukup kirimkan link video/foto dari platform yang didukung!\n\n"
        "💡 Gunakan /help untuk info lebih lanjut."
    )
    # Use Markdown formatting
    await update.message.reply_text(start_text, parse_mode='Markdown')

async def stiker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /stiker <text> - create a sticker from text.
    Uses utils.api_utils.generate_sticker which may return bytes or a file path.
    """
    # If no arguments provided, show usage
    if not context.args:
        await update.message.reply_text(
            "❌ Anda harus memberikan teks setelah perintah /stiker. Contoh: /stiker HALO ASU"
        )
        return

    text = " ".join(context.args)

    try:
        # Call generate_sticker (may be sync or async)
        result = await _maybe_await(generate_sticker, text)

        # If bytes-like, send directly
        if isinstance(result, (bytes, bytearray)):
            bio = io.BytesIO(result)
            bio.name = "sticker.webp"  # Telegram expects a filename for some uploads
            bio.seek(0)
            await update.message.reply_sticker(sticker=InputFile(bio, filename=bio.name))
            return

        # If path string and file exists, send from file
        if isinstance(result, str) and os.path.exists(result):
            await update.message.reply_sticker(sticker=InputFile(result))
            return

        # If the generator returned something else (e.g., a URL), try to send as text feedback
        await update.message.reply_text(
            "❌ Gagal membuat stiker. Fungsi generate_sticker mengembalikan hasil yang tidak dikenali."
        )

    except error.TelegramError as te:
        await update.message.reply_text(f"❌ Telegram error saat mengirim stiker: {te}")
    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi kesalahan saat membuat stiker: {e}")

def get_handlers():
    """
    Returns a list of CommandHandler instances to be added to the application.
    """
    return [
        CommandHandler("start", start_command),
        CommandHandler("stiker", stiker_command),
    ]
