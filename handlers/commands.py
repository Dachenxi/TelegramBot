from telegram import Update, error
from telegram.ext import CommandHandler, ContextTypes, Application
from utils.api_utils import generate_sticker
import asyncio

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
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
        "💡 Gunakan /help untuk info lebih lanjut.",
        parse_mode='Markdown'
        await update.message.reply_text("❌ Anda harus memberikan teks setelah perintah /stiker. Contoh: /stiker HALO ASU")
        return
    
    text = " ".join(context.args)  # Gabungkan teks setelah /stiker
🤖 **PANDUAN PENGGUNAAN BOT**

📝 **Cara Menggunakan:**
1️⃣ Kirim link video/foto dari platform yang didukung
2️⃣ Bot akan mendeteksi platform secara otomatis
3️⃣ Tunggu proses download selesai
4️⃣ Bot akan mengirimkan media beserta informasinya

✨ **Fitur:**
• ✅ Auto-detect platform dari URL
• ✅ Informasi lengkap (judul, uploader, durasi, views, likes)
• ✅ Caption menarik dengan emoji
• ✅ Support video dan foto
• ✅ Auto-cleanup setelah kirim
• ✅ Support multiple files

🌐 **Platform yang Didukung:**
🎥 YouTube (video & shorts)
📸 Instagram (post, reels, stories)
👥 Facebook (video & watch)
🐦 Twitter/X
🎵 TikTok
🤖 Reddit
📹 Vimeo
🎮 Twitch (clips & VOD)
📌 Pinterest
📝 Tumblr
🎬 Dailymotion
🎧 SoundCloud

⚠️ **Catatan:**
• Beberapa platform mungkin memiliki batasan
• Pastikan link bisa diakses secara publik
• File besar akan dikirim sebagai document

🔧 **Command Lain:**
/start - Mulai bot
/help - Tampilkan bantuan ini
/stiker <teks> - Buat stiker dengan teks
/uptime - Cek uptime bot

❓ **Butuh bantuan?**
Pastikan link yang dikirim valid dan bisa diakses!
""", parse_mode='Markdown')
