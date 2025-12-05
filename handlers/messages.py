from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, Application
from utils.instagram import download_instagram_post
from utils.file_utils import clear_temp_folder
from utils.dlp_method import MediaDownloader
import os
import re


def is_url(text: str) -> bool:
    """Cek apakah text adalah URL yang valid"""
    url_pattern = re.compile(
        r'^https?://'  # http:// atau https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...atau ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(text) is not None


async def handle_social_media_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk mendownload media dari berbagai platform social media"""
    message = update.message
    url = message.text.strip()

    # Validasi apakah text adalah URL
    if not is_url(url):
        return

    # Inisialisasi downloader
    downloader = MediaDownloader(output_dir="temp")

    # Deteksi platform
    platform = downloader.detect_platform(url)

    if not platform:
        # Jika platform tidak dikenali, skip
        return

    # Emoji untuk platform
    emoji = downloader.get_platform_emoji(platform)

    # Kirim status awal
    status_message = await message.reply_text(
        f"{emoji} Mendeteksi link dari **{platform.upper()}**...\n"
        f"⏳ Sedang mengambil informasi..."
    )

    try:
        # Ambil informasi video terlebih dahulu
        try:
            video_info = downloader.get_video_info(url)
            info_caption = downloader.create_caption(video_info)

            # Update status dengan info video
            await status_message.edit_text(
                f"{emoji} **{platform.upper()}** terdeteksi!\n\n"
                f"📌 Judul: {video_info['title'][:80]}...\n"
                f"👤 Uploader: {video_info['uploader']}\n"
                f"⏱️ Durasi: {downloader.format_duration(video_info['duration'])}\n\n"
                f"⬇️ Sedang mendownload..."
            )
        except Exception as e:
            # Jika gagal ambil info, tetap lanjutkan download
            info_caption = None
            await status_message.edit_text(
                f"{emoji} Link **{platform.upper()}** terdeteksi!\n"
                f"⬇️ Sedang mendownload..."
            )

        # Download media
        media_files = downloader.download_media(url)

        if not media_files:
            await status_message.edit_text("❌ Tidak ada media yang bisa didownload.")
            return

        # Update status
        await status_message.edit_text(
            f"✅ Download selesai!\n"
            f"📤 Mengirim {len(media_files)} file..."
        )

        # Kirim media ke user
        for idx, media_path in enumerate(media_files):
            try:
                file_size = os.path.getsize(media_path)

                # Jika file terlalu besar (> 50MB), kirim sebagai document
                if file_size > 50 * 1024 * 1024:
                    with open(media_path, 'rb') as media_file:
                        caption = info_caption if idx == 0 and info_caption else None
                        await context.bot.send_document(
                            chat_id=message.chat_id,
                            document=media_file,
                            caption=caption,
                            parse_mode='Markdown'
                        )
                else:
                    # Deteksi tipe file
                    if media_path.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        # Kirim sebagai foto
                        with open(media_path, 'rb') as media_file:
                            caption = info_caption if idx == 0 and info_caption else None
                            await context.bot.send_photo(
                                chat_id=message.chat_id,
                                photo=media_file,
                                caption=caption,
                                parse_mode='Markdown'
                            )
                    else:
                        # Kirim sebagai video
                        with open(media_path, 'rb') as media_file:
                            caption = info_caption if idx == 0 and info_caption else None
                            await context.bot.send_video(
                                chat_id=message.chat_id,
                                video=media_file,
                                caption=caption,
                                parse_mode='Markdown',
                                supports_streaming=True
                            )
            except Exception as e:
                # Jika gagal kirim sebagai video/photo, coba kirim sebagai document
                try:
                    with open(media_path, 'rb') as media_file:
                        await context.bot.send_document(
                            chat_id=message.chat_id,
                            document=media_file
                        )
                except Exception as doc_error:
                    await message.reply_text(f"❌ Gagal mengirim file: {str(doc_error)}")

        # Hapus status message
        await status_message.delete()

        # Bersihkan file yang sudah didownload
        clear_temp_folder()

    except Exception as e:
        await status_message.edit_text(
            f"❌ Terjadi kesalahan saat memproses link {platform}:\n"
            f"💡 Tips: Pastikan link valid dan bisa diakses."
        )
        # Tetap bersihkan temp folder meski error
        try:
            clear_temp_folder()
        except:
            pass


async def handle_instagram_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Legacy handler untuk Instagram (fallback jika yt-dlp gagal)"""
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
    # Handler utama untuk semua platform menggunakan yt-dlp
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_social_media_url))
