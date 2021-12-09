from telegram import Update
from telegram.ext import CallbackContext


def register_check_handler(update: Update, context: CallbackContext):
    update.message.reply_text('register_check_handler')
