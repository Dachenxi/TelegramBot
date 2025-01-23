import requests
import os

def generate_sticker(text: str) -> str:
    """
    Memanggil API untuk menghasilkan stiker dengan teks.
    :param text: Teks yang akan digunakan untuk membuat stiker
    :return: Path file stiker yang diunduh
    """
    url = f"https://api.rifandavinci.my.id/sticker/brat?text={text}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Simpan file sementara
        temp_folder = "temp"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        
        # Tentukan nama file dari respons atau gunakan default
        filename = "brat.png"
        content_disposition = response.headers.get("content-disposition")
        if content_disposition and "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        
        sticker_path = os.path.join(temp_folder, filename)
        with open(sticker_path, "wb") as file:
            file.write(response.content)
        
        return sticker_path
    else:
        raise Exception(f"API Error: {response.status_code}, {response.text}")