import os

def clear_temp_folder():
    for file in os.listdir("temp"):
        os.remove(os.path.join("temp", file))
