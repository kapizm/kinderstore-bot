from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, ConversationHandler,
    Filters, MessageHandler,
)

from src import database
from src.models import User


def register_handler(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text('Введите свое полное имя')
    return 'SAVE_NAME_ACTION'


def save_name_handler(update: Update, context: CallbackContext):
    user = User(
        telegram_id=update.message.from_user.id,
        full_name=update.message.text,
    )

    with database.Session() as session, session.begin():
        session.add(user)

    update.message.reply_text('Введите свой номер телефона')
    return 'SAVE_PHONE_NUMBER_ACTION'


def save_phone_number_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()
        user.phone_number = update.message.text
        session.commit()

    update.message.reply_text('Введите свой никнейм в instagram')
    return 'SAVE_INSTAGRAM_ACTION'


def save_instagram_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()
        user.ig_account = update.message.text
        session.commit()

    buttons = [
        [
            InlineKeyboardButton(
                'Зарегистрировать чек', callback_data='add_check',
            ),
        ],
        [
            InlineKeyboardButton('Мои чеки', callback_data='my_checks'),
        ],
    ]
    update.message.reply_text(
        'Вы успешно зарегистрировались',
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return 'END_ACTION'


conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(register_handler, pattern='^registration$'),
    ],
    states={
        'SAVE_NAME_ACTION': [MessageHandler(Filters.text, save_name_handler)],
        'SAVE_PHONE_NUMBER_ACTION': [
            MessageHandler(Filters.text, save_phone_number_handler),
        ],
        'SAVE_INSTAGRAM_ACTION': [
            MessageHandler(Filters.text, save_instagram_handler),
        ],
    },
    fallbacks=[],
    map_to_parent={
        'END_ACTION': 'SELECT_ACTION',
    },
)
