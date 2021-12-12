from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, CommandHandler,
    ConversationHandler, Updater,
)

from src import config, database
from src.handlers import add_check, registration, my_checks
from src.models import User

bot = Updater(token=config.TOKEN)


def start_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()

    buttons = []

    if user:
        buttons.extend([
            [
                InlineKeyboardButton(
                    'Зарегистрировать чек', callback_data='add_check',
                ),
            ],
            [
                InlineKeyboardButton('Мои чеки', callback_data='my_checks'),
            ],
        ])
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    'Зарегистрироваться', callback_data='registration',
                ),
            ],
        )

    update.message.reply_text(
        'Здравствуйте! Выберите действие',
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return 'SELECT_ACTION'


def cancel_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Отменено')
    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_handler)],
    states={
        'SELECT_ACTION': [
            registration.conversation_handler,
            add_check.conversation_handler,
            CallbackQueryHandler(my_checks.my_checks_handler, pattern='^my_checks$'),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel_handler)],
)

bot.dispatcher.add_handler(conversation_handler)
