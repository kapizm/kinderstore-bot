from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler


def add_check_handler(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text('add_check_handler')


conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(add_check_handler, pattern='^add_check$')],
    states={},
    fallbacks={},
    map_to_parent={
        'END_ACTION': 'SELECT_ACTION',
    },
)
