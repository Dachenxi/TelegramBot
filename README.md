# 🎥 Multi-Platform Media Downloader Bot

Bot Telegram untuk mendownload video dan foto dari berbagai platform social media menggunakan Python dan yt-dlp.

## ✨ Fitur Utama

- 🌐 **Multi-Platform Support**: Download dari 12+ platform social media
- 🤖 **Auto-Detection**: Otomatis mendeteksi platform dari URL
- 📊 **Info Lengkap**: Tampilkan informasi video (judul, uploader, durasi, views, likes)
- 🎨 **Caption Menarik**: Caption dengan emoji dan format yang menarik
- 🗑️ **Auto-Cleanup**: Otomatis menghapus file setelah dikirim
- 📁 **Multi-File Support**: Support download multiple files sekaligus

## 🌐 Platform yang Didukung

| Platform | Icon | Status |
|----------|------|--------|
| YouTube | 🎥 | ✅ |
| Instagram | 📸 | ✅ |
| Facebook | 👥 | ✅ |
| Twitter/X | 🐦 | ✅ |
| TikTok | 🎵 | ✅ |
| Reddit | 🤖 | ✅ |
| Vimeo | 📹 | ✅ |
| Twitch | 🎮 | ✅ |
| Pinterest | 📌 | ✅ |
| Tumblr | 📝 | ✅ |
| Dailymotion | 🎬 | ✅ |
| SoundCloud | 🎧 | ✅ |

## 📋 Requirements

- Python 3.8+
- python-telegram-bot
- yt-dlp
- python-dotenv
- instaloader (fallback untuk Instagram)

## 🚀 Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/TelegramBot.git
   cd TelegramBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   
   Buat file `utils/.env` dan tambahkan token bot:
   ```
   TOKEN=your_telegram_bot_token_here
   ```

4. **Buat folder temp**
   ```bash
   mkdir temp
   ```

5. **Jalankan bot**
   ```bash
   python app.py
   ```

## 📖 Cara Penggunaan

### Command

- `/start` - Mulai bot dan tampilkan welcome message
- `/help` - Tampilkan panduan lengkap
- `/stiker <teks>` - Generate stiker dengan teks
- `/uptime` - Cek uptime bot

### Download Media

Cukup kirimkan link video/foto dari platform yang didukung:

**Contoh:**
```
https://www.youtube.com/watch?v=xxxxx
https://www.instagram.com/p/xxxxx/
https://www.tiktok.com/@username/video/xxxxx
https://twitter.com/username/status/xxxxx
```

Bot akan:
1. Mendeteksi platform secara otomatis
2. Mengambil informasi media
3. Download media
4. Mengirim dengan caption lengkap
5. Membersihkan file temporary

## 🏗️ Struktur Project

```
TelegramBot/
├── app.py                 # Entry point aplikasi
├── requirements.txt       # Dependencies
├── LICENSE               # License file
├── README.md             # Dokumentasi
├── handlers/
│   ├── commands.py       # Command handlers (/start, /help, dll)
│   └── messages.py       # Message handlers (URL processing)
├── utils/
│   ├── .env             # Environment variables (TOKEN)
│   ├── api_utils.py     # API utilities (sticker generation)
│   ├── dlp_method.py    # yt-dlp wrapper untuk download media
│   ├── file_utils.py    # File management utilities
│   └── instagram.py     # Instagram fallback downloader
└── temp/                # Temporary download folder
```

## 🔧 Konfigurasi

### MediaDownloader Class

Class utama untuk download media dengan berbagai method:

```python
from utils.dlp_method import MediaDownloader

# Inisialisasi
downloader = MediaDownloader(output_dir="temp")

# Deteksi platform
platform = downloader.detect_platform(url)

# Ambil info video
info = downloader.get_video_info(url)

# Download media
files = downloader.download_media(url)

# Buat caption
caption = downloader.create_caption(info)
```

### Custom Configuration

Edit `utils/dlp_method.py` untuk customize:
- Format download (best/worst quality)
- Output template
- Post-processing options

## 📝 Contoh Output

Ketika user mengirim link, bot akan membalas dengan:

```
📸 INSTAGRAM DOWNLOADER

📌 Judul: Beautiful sunset at the beach
👤 Uploader: @username
⏱️ Durasi: 00:45
👁️ Views: 1.2M
❤️ Likes: 45.3K

📝 Deskripsi:
Amazing sunset captured at Bali beach...

📅 Upload Date: 20231205
💾 Size: 15.42 MB
```

## ⚠️ Catatan Penting

1. **File Size Limit**: Telegram memiliki batasan 50MB untuk video/photo. File lebih besar akan dikirim sebagai document.

2. **Rate Limiting**: Beberapa platform memiliki rate limiting. Bot akan menangani error dengan graceful.

3. **Private Content**: Bot hanya bisa download konten yang bisa diakses publik.

4. **FFmpeg**: Untuk beberapa platform, yt-dlp memerlukan FFmpeg untuk konversi video. Install FFmpeg jika diperlukan:
   ```bash
   # Windows (dengan chocolatey)
   choco install ffmpeg
   
   # Linux (Ubuntu/Debian)
   sudo apt install ffmpeg
   
   # MacOS (dengan homebrew)
   brew install ffmpeg
   ```

## 🛠️ Troubleshooting

### Error: "Gagal mendownload"
- Pastikan link valid dan bisa diakses
- Cek koneksi internet
- Beberapa konten private tidak bisa didownload

### Error: "File tidak ditemukan"
- Pastikan folder `temp` sudah dibuat
- Cek permission folder

### Error: "Module not found"
- Jalankan: `pip install -r requirements.txt`

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 License

Project ini menggunakan lisensi yang tertera di file [LICENSE](LICENSE).

## 👤 Author

Dibuat dengan ❤️ untuk memudahkan download media dari berbagai platform.

## 🙏 Credits

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Universal video downloader
- [instaloader](https://github.com/instaloader/instaloader) - Instagram downloader fallback

## 📞 Support

Jika ada pertanyaan atau masalah, silakan buat issue di repository ini.

---

⭐ Jangan lupa star repository ini jika bermanfaat!

