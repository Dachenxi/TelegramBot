from telegram.ext import Application
from handlers.commands import register_command_handlers
from handlers.messages import register_message_handlers
from datetime import datetime

class Bot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.register_handlers()
        self.start_time = datetime.now()
    
    def register_handlers(self):
        register_command_handlers(self.application)
        register_message_handlers(self.application)

    def run(self):
        print("Bot sedang berjalan...")
        self.application.bot_data["start_time"] = self.start_time
        self.application.run_polling()

if __name__ == "__main__":
    BOT_TOKEN = ""
    bot = Bot(BOT_TOKEN)
    bot.run()
