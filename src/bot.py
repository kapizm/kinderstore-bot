from telegram.ext import Updater
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from src import config
from src.handlers import checks, registration

bot = Updater(token=config.TOKEN)

bot.dispatcher.add_handler(registration.conversation_handler)
bot.dispatcher.add_handler(
    MessageHandler(
        Filters.regex('^Зарегистрировать чек$'),
        checks.register_check_handler,
    ),
)
