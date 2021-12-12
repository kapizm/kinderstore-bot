from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, ConversationHandler,
    Filters, MessageHandler,
)

from src import database
from src.models import Check, User


def add_check_handler(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text(
        'Введите номер Вашего чека',
    )
    return 'SAVE_CHECK_ACTION'


def save_check_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()

    check = Check(
        number=update.message.text,
        user_id=user.id,
    )

    with database.Session() as session, session.begin():
        session.add(check)

    buttons = [
        [InlineKeyboardButton(
            'Зарегистрировать чек', callback_data='add_check',
        )],
        [InlineKeyboardButton(
            'Мои чеки', callback_data='my_checks',
        )],
    ]
    update.message.reply_text(
        'Вы успешно добавили чек',
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return 'END_ACTION'


conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        add_check_handler, pattern='^add_check$',
    )],
    states={
        'SAVE_CHECK_ACTION': [MessageHandler(Filters.text, add_check_handler)],
        },
    fallbacks={},
    map_to_parent={
        'END_ACTION': 'SELECT_ACTION',
    },
)
