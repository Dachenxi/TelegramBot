from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import instaloader
import os
import re
from urllib.parse import urlparse

class InstagramDownloaderBot:
    def __init__(self, token: str):
        """
        Inisialisasi bot Telegram
        :param token: Token bot dari BotFather
        """
        self.application = Application.builder().token(token).build()
        self.L = instaloader.Instaloader()
        
        # Buat folder untuk menyimpan file sementara
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        # Daftar semua handlers
        self.register_handlers()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /start"""
        await update.message.reply_text(
            "Halo! Saya adalah bot download Instagram.\n"
            "Kirimkan saya link post Instagram dan saya akan mendownloadnya untuk Anda.\n"
            "Bot mendukung single post dan multiple post (carousel)."
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /help"""
        help_text = """
Cara menggunakan bot:
1. Kirim link post Instagram (contoh: https://www.instagram.com/p/ABC123/)
2. Tunggu beberapa saat
3. Bot akan mengirimkan semua media dari post tersebut
   (Termasuk semua foto/video jika itu adalah multiple post)

Perintah yang tersedia:
/start - Memulai bot
/help - Menampilkan bantuan
        """
        await update.message.reply_text(help_text)
    
    def extract_shortcode(self, url: str) -> str:
        """Ekstrak shortcode dari URL Instagram"""
        path = urlparse(url).path
        patterns = [
            r"/p/([^/?]+)",    # Format post biasa
            r"/reel/([^/?]+)",
            r"/reels/([^/?]+)",# Format reels
        ]
        
        for pattern in patterns:
            match = re.search(pattern, path)
            if match:
                return match.group(1)
        return None
    
    async def send_media(self, message, media_path):
        """Kirim media (foto atau video) ke user"""
        if media_path.endswith('.mp4'):
            with open(media_path, 'rb') as video:
                await message.reply_video(video)
        else:
            with open(media_path, 'rb') as photo:
                await message.reply_photo(photo)
    
    async def handle_instagram_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk URL Instagram"""
        message = update.message
        url = message.text
        
        # Periksa apakah URL valid
        if not ("instagram.com/p/" in url or "instagram.com/reel/" in url or "instagram.com/reels/" in url):
            await message.reply_text("Mohon kirimkan link post Instagram yang valid.")
            return
        
        # Beri tahu user bahwa proses dimulai
        status_message = await message.reply_text("⏳ Sedang mengunduh post...")
        
        try:
            # Ekstrak shortcode dari URL
            shortcode = self.extract_shortcode(url)
            if not shortcode:
                await status_message.edit_text("❌ Link tidak valid.")
                return
            
            # Download post
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)
            
            # Cek apakah ini multiple post (carousel)
            if post.mediacount > 1:
                await status_message.edit_text(f"📥 Mengunduh {post.mediacount} item dari post...")
                
                # Download semua item dalam post
                self.L.download_post(post, target="temp")
                
                # Urutkan file berdasarkan nomor
                media_files = []
                for file in os.listdir("temp"):
                    if file.endswith((".jpg", ".mp4")) and not file.endswith(".jpg.xz"):
                        media_files.append(file)
                
                media_files.sort()  # Urutkan file agar sesuai dengan urutan di Instagram
                
                # Kirim setiap media
                for idx, file in enumerate(media_files, 1):
                    file_path = os.path.join("temp", file)
                    await self.send_media(message, file_path)
                    await status_message.edit_text(f"✅ Terkirim {idx}/{len(media_files)} item...")
                    os.remove(file_path)
                
            else:
                # Single post (foto atau video)
                if post.is_video:
                    self.L.download_post(post, target="temp")
                    video_path = None
                    for file in os.listdir("temp"):
                        if file.endswith(".mp4"):
                            video_path = os.path.join("temp", file)
                            break
                    
                    if video_path:
                        await self.send_media(message, video_path)
                        os.remove(video_path)
                else:
                    self.L.download_post(post, target="temp")
                    photo_path = None
                    for file in os.listdir("temp"):
                        if file.endswith(".jpg") and not file.endswith(".jpg.xz"):
                            photo_path = os.path.join("temp", file)
                            break
                    
                    if photo_path:
                        await self.send_media(message, photo_path)
                        os.remove(photo_path)
            
            # Hapus semua file sisa
            for file in os.listdir("temp"):
                if file.endswith((".jpg", ".mp4", ".json", ".txt", ".jpg.xz",".json.xz")):
                    try:
                        os.remove(os.path.join("temp", file))
                    except:
                        pass
            
            await status_message.edit_text("✅ Download selesai!")
            
        except Exception as e:
            await status_message.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
    
    def register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_instagram_url))
    
    def run(self):
        """Menjalankan bot"""
        print("Bot sedang berjalan...")
        self.application.run_polling()

if __name__ == "__main__":
    # Ganti TOKEN dengan token bot Anda dari BotFather
    BOT_TOKEN = "YourTOKEN"
    bot = InstagramDownloaderBot(BOT_TOKEN)
    bot.run()