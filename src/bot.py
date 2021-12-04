from telegram.ext import Updater, CommandHandler
from src import config


bot = Updater(token=config.TOKEN)


def start_handler(update, context):
    update.message.reply_text("Test")


bot.dispatcher.add_handler(CommandHandler("start", start_handler))
