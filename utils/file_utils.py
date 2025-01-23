import os
import dotenv

def clear_temp_folder():
    for file in os.listdir("temp"):
        os.remove(os.path.join("temp", file))

def get_token():
    dotenv.load_dotenv("utils/.env")
    return os.getenv("TOKEN")