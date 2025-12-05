import os
import dotenv

def clear_temp_folder():
    """Bersihkan semua file di folder temp"""
    try:
        if not os.path.exists("temp"):
            os.makedirs("temp")
            return

        for file in os.listdir("temp"):
            file_path = os.path.join("temp", file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error menghapus file {file_path}: {e}")
    except Exception as e:
        print(f"Error saat membersihkan folder temp: {e}")
