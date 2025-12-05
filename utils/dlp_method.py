import yt_dlp as dlp
import os
import re
from typing import Dict, List, Optional


class MediaDownloader:
    """Class untuk mendownload media dari berbagai platform social media menggunakan yt-dlp"""

    def __init__(self, output_dir: str = "temp"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def detect_platform(self, url: str) -> Optional[str]:
        """
        Mendeteksi platform dari URL
        Returns: platform name atau None jika tidak dikenali
        """
        platform_patterns = {
            'youtube': [r'youtube\.com', r'youtu\.be'],
            'instagram': [r'instagram\.com'],
            'facebook': [r'facebook\.com', r'fb\.watch', r'fb\.com'],
            'twitter': [r'twitter\.com', r'x\.com'],
            'tiktok': [r'tiktok\.com', r'vm\.tiktok\.com'],
            'reddit': [r'reddit\.com', r'redd\.it'],
            'vimeo': [r'vimeo\.com'],
            'twitch': [r'twitch\.tv', r'clips\.twitch\.tv'],
            'pinterest': [r'pinterest\.com', r'pin\.it'],
            'tumblr': [r'tumblr\.com'],
            'dailymotion': [r'dailymotion\.com'],
            'soundcloud': [r'soundcloud\.com']
        }

        for platform, patterns in platform_patterns.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return platform
        return None

    def get_platform_emoji(self, platform: str) -> str:
        """Mendapatkan emoji yang sesuai untuk setiap platform"""
        emojis = {
            'youtube': '🎥',
            'instagram': '📸',
            'facebook': '👥',
            'twitter': '🐦',
            'tiktok': '🎵',
            'reddit': '🤖',
            'vimeo': '📹',
            'twitch': '🎮',
            'pinterest': '📌',
            'tumblr': '📝',
            'dailymotion': '🎬',
            'soundcloud': '🎧'
        }
        return emojis.get(platform, '📥')

    def get_video_info(self, url: str) -> Dict:
        """
        Mengambil informasi video tanpa mendownload
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        try:
            with dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # Format informasi yang akan dikembalikan
                video_info = {
                    'title': info.get('title', 'N/A'),
                    'description': info.get('description', 'N/A'),
                    'uploader': info.get('uploader', 'N/A'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'thumbnail': info.get('thumbnail', None),
                    'upload_date': info.get('upload_date', 'N/A'),
                    'format': info.get('format', 'N/A'),
                    'filesize': info.get('filesize', 0),
                    'ext': info.get('ext', 'mp4'),
                    'platform': self.detect_platform(url)
                }

                return video_info
        except Exception as e:
            raise Exception(f"Gagal mengambil informasi: {str(e)}")

    def format_duration(self, seconds: int) -> str:
        """Format durasi dari detik ke format MM:SS atau HH:MM:SS"""
        if seconds == 0:
            return "N/A"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def format_count(self, count: int) -> str:
        """Format angka besar ke format yang lebih readable (1.2K, 1.5M, dll)"""
        if count == 0 or count is None:
            return "N/A"
        if count >= 1_000_000:
            return f"{count/1_000_000:.1f}M"
        elif count >= 1_000:
            return f"{count/1_000:.1f}K"
        else:
            return str(count)

    def format_filesize(self, size: int) -> str:
        """Format ukuran file ke format yang readable"""
        if size == 0 or size is None:
            return "N/A"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    def create_caption(self, video_info: Dict) -> str:
        """
        Membuat caption menarik dengan informasi video
        """
        platform = video_info.get('platform', 'Unknown')
        emoji = self.get_platform_emoji(platform)

        caption = f"{emoji} **{platform.upper()} DOWNLOADER**\n\n"
        caption += f"📌 **Judul:** {video_info['title'][:100]}{'...' if len(video_info['title']) > 100 else ''}\n"
        caption += f"👤 **Uploader:** {video_info['uploader']}\n"
        caption += f"⏱️ **Durasi:** {self.format_duration(video_info['duration'])}\n"
        caption += f"👁️ **Views:** {self.format_count(video_info['view_count'])}\n"
        caption += f"❤️ **Likes:** {self.format_count(video_info['like_count'])}\n"

        # Tambahkan deskripsi jika ada (maksimal 150 karakter)
        if video_info['description'] and video_info['description'] != 'N/A':
            desc = video_info['description'][:150]
            if len(video_info['description']) > 150:
                desc += '...'
            caption += f"\n📝 **Deskripsi:**\n{desc}\n"

        caption += f"\n📅 **Upload Date:** {video_info['upload_date']}"
        caption += f"\n💾 **Size:** {self.format_filesize(video_info.get('filesize', 0))}"

        return caption

    def download_media(self, url: str, quality: str = 'best') -> List[str]:
        """
        Download media dari URL
        Args:
            url: URL video/foto
            quality: 'best', 'worst', atau format spesifik
        Returns:
            List path file yang telah didownload
        """
        # Buat nama file yang unik
        output_template = os.path.join(self.output_dir, '%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'best' if quality == 'best' else 'worst',
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            # Untuk Instagram dan platform lain yang butuh autentikasi
            'cookiefile': None,  # Bisa ditambahkan jika perlu cookies
        }

        try:
            with dlp.YoutubeDL(ydl_opts) as ydl:
                # Download video
                info = ydl.extract_info(url, download=True)

                # Ambil nama file yang didownload
                if 'entries' in info:
                    # Playlist atau multiple files
                    downloaded_files = []
                    for entry in info['entries']:
                        filename = ydl.prepare_filename(entry)
                        if os.path.exists(filename):
                            downloaded_files.append(filename)
                        else:
                            # Coba cari file dengan ekstensi berbeda
                            base = os.path.splitext(filename)[0]
                            for ext in ['.mp4', '.mkv', '.webm', '.jpg', '.png']:
                                if os.path.exists(base + ext):
                                    downloaded_files.append(base + ext)
                                    break
                    return downloaded_files
                else:
                    # Single file
                    filename = ydl.prepare_filename(info)
                    if os.path.exists(filename):
                        return [filename]
                    else:
                        # Coba cari file dengan ekstensi berbeda
                        base = os.path.splitext(filename)[0]
                        for ext in ['.mp4', '.mkv', '.webm', '.jpg', '.png']:
                            if os.path.exists(base + ext):
                                return [base + ext]

                        # Jika tidak ditemukan, cari di folder temp
                        temp_files = [
                            os.path.join(self.output_dir, f)
                            for f in os.listdir(self.output_dir)
                            if os.path.isfile(os.path.join(self.output_dir, f))
                        ]
                        # Urutkan berdasarkan waktu modifikasi (yang terbaru)
                        if temp_files:
                            temp_files.sort(key=os.path.getmtime, reverse=True)
                            return [temp_files[0]]

                        raise Exception("File yang didownload tidak ditemukan")

        except Exception as e:
            raise Exception(f"Gagal mendownload: {str(e)}")

    def download_photo(self, url: str) -> List[str]:
        """
        Download foto dari URL (khusus untuk Instagram, Pinterest, dll)
        """
        output_template = os.path.join(self.output_dir, '%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'quiet': False,
        }

        try:
            with dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                if os.path.exists(filename):
                    return [filename]
                else:
                    # Cari file di temp folder
                    temp_files = [
                        os.path.join(self.output_dir, f)
                        for f in os.listdir(self.output_dir)
                        if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))
                    ]
                    if temp_files:
                        temp_files.sort(key=os.path.getmtime, reverse=True)
                        return [temp_files[0]]

                    return []

        except Exception as e:
            raise Exception(f"Gagal mendownload foto: {str(e)}")


# Helper functions untuk backward compatibility
def download_video(url: str, output_dir: str = "temp") -> List[str]:
    """Helper function untuk download video"""
    downloader = MediaDownloader(output_dir)
    return downloader.download_media(url)


def get_video_info(url: str) -> Dict:
    """Helper function untuk mendapatkan info video"""
    downloader = MediaDownloader()
    return downloader.get_video_info(url)


def detect_platform(url: str) -> Optional[str]:
    """Helper function untuk deteksi platform"""
    downloader = MediaDownloader()
    return downloader.detect_platform(url)

