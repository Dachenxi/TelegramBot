# 🚀 Quick Start Guide

Panduan cepat untuk menjalankan Multi-Platform Media Downloader Bot.

## 📋 Prerequisites

- Python 3.8 atau lebih baru
- pip (Python package manager)
- FFmpeg (optional, tapi direkomendasikan)

## 🔧 Setup dalam 5 Langkah

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/TelegramBot.git
cd TelegramBot
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies yang akan diinstall:**
- `python-telegram-bot==20.3` - Telegram Bot API
- `yt-dlp>=2023.10.13` - Universal video downloader
- `instaloader==4.10.1` - Instagram fallback
- `python-dotenv==0.21.0` - Environment variables

### 3️⃣ Setup Bot Token

1. Buka Telegram dan cari `@BotFather`
2. Kirim command `/newbot`
3. Ikuti instruksi untuk membuat bot baru
4. Copy token yang diberikan

5. Buat file `.env` di folder `utils/`:
   ```bash
   # Windows PowerShell
   Copy-Item utils\.env.example utils\.env
   
   # Linux/Mac
   cp utils/.env.example utils/.env
   ```

6. Edit file `utils/.env` dan paste token:
   ```
   TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### 4️⃣ Buat Folder Temp

```bash
# Windows PowerShell
New-Item -ItemType Directory -Path temp -Force

# Linux/Mac
mkdir -p temp
```

### 5️⃣ Jalankan Bot

```bash
python app.py
```

Jika berhasil, akan muncul:
```
Bot sedang berjalan...
```

## ✅ Testing Bot

1. Buka Telegram dan cari username bot Anda
2. Kirim command `/start`
3. Bot akan membalas dengan welcome message
4. Coba kirim link YouTube atau Instagram
5. Bot akan download dan kirim media!

## 📱 Contoh Link untuk Testing

**YouTube:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Instagram:**
```
https://www.instagram.com/p/XXXXXXXXXX/
```

**TikTok:**
```
https://www.tiktok.com/@username/video/1234567890
```

**Twitter:**
```
https://twitter.com/username/status/1234567890
```

## 🔧 Optional: Install FFmpeg

FFmpeg diperlukan untuk konversi video pada beberapa platform.

### Windows (dengan Chocolatey)
```powershell
choco install ffmpeg
```

### Windows (Manual)
1. Download dari https://ffmpeg.org/download.html
2. Extract ke `C:\ffmpeg`
3. Tambahkan `C:\ffmpeg\bin` ke PATH

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### MacOS (dengan Homebrew)
```bash
brew install ffmpeg
```

## 🐛 Troubleshooting

### Error: "No module named 'telegram'"
**Solusi:**
```bash
pip install python-telegram-bot
```

### Error: "No module named 'yt_dlp'"
**Solusi:**
```bash
pip install yt-dlp
```

### Error: "TOKEN not found"
**Solusi:**
- Pastikan file `utils/.env` ada
- Pastikan TOKEN sudah diisi dengan benar
- Pastikan tidak ada spasi sebelum/sesudah TOKEN

### Bot tidak respond
**Solusi:**
- Cek koneksi internet
- Pastikan token valid
- Restart bot dengan `Ctrl+C` lalu `python app.py` lagi

### Error: "Permission denied" saat membuat folder temp
**Solusi:**
```bash
# Windows (Run as Administrator)
New-Item -ItemType Directory -Path temp -Force

# Linux/Mac
sudo mkdir temp
sudo chmod 777 temp
```

## 🎯 Next Steps

Setelah bot berjalan, Anda bisa:
- ✅ Customize caption di `utils/dlp_method.py`
- ✅ Tambah command di `handlers/commands.py`
- ✅ Tambah platform baru di `detect_platform()`
- ✅ Deploy ke server (VPS, Heroku, Railway, dll)

## 🚀 Deploy ke Server

### Option 1: Railway
1. Push ke GitHub
2. Connect ke Railway
3. Add environment variable `TOKEN`
4. Deploy!

### Option 2: Heroku
1. Install Heroku CLI
2. `heroku create`
3. `heroku config:set TOKEN=your_token`
4. `git push heroku main`

### Option 3: VPS (Ubuntu)
```bash
# Install Python & pip
sudo apt update
sudo apt install python3 python3-pip

# Clone & setup
git clone your_repo
cd TelegramBot
pip3 install -r requirements.txt

# Setup .env
nano utils/.env

# Run dengan screen/tmux
screen -S telebot
python3 app.py
# Press Ctrl+A then D to detach
```

## 📞 Need Help?

Jika masih ada masalah:
1. Baca [README.md](README.md) untuk dokumentasi lengkap
2. Cek existing issues di GitHub
3. Buat issue baru dengan detail error

## 🎉 Selamat!

Bot Anda sudah siap digunakan! Selamat mendownload media dari berbagai platform! 🎊

---

Made with ❤️ by [Your Name]

