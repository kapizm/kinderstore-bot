from telegram.ext import Updater

from src import config, handlers

bot = Updater(token=config.TOKEN)

bot.dispatcher.add_handler(handlers.conversation_handler)
