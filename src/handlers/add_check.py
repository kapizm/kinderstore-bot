from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, ConversationHandler,
    Filters, MessageHandler,
)

from src import database, helpers
from src.models import Check, User


def add_check_handler(update: Update, context: CallbackContext):
    update.callback_query.edit_message_text(
        'Введите номер Вашего чека',
    )
    return 'SAVE_CHECK_ACTION'


def save_check_handler(update: Update, context: CallbackContext):
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

    with database.Session() as session:
        check = session.query(Check).filter(
            Check.number == update.message.text,
        ).first()

    if check:
        update.message.reply_text(
            'Чек уже зарегистрирован',
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return 'END_ACTION'

    check_data = helpers.get_check_data_from_api(
        check_number=update.message.text,
    )

    if not check_data:
        update.message.reply_text(
            'Чек не найден',
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return 'END_ACTION'

    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()

    check = Check(
        number=update.message.text,
        user_id=user.id,
        chances=helpers.get_chances_from_price(check_data['price']),
        registered_at=check_data['registered_at'],
    )

    with database.Session() as session, session.begin():
        session.add(check)

    update.message.reply_text(
        'Чек успешно добавлен',
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return 'END_ACTION'


conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(add_check_handler, pattern='^add_check$'),
    ],
    states={
        'SAVE_CHECK_ACTION': [
            MessageHandler(Filters.text, save_check_handler),
        ],
    },
    fallbacks={},
    map_to_parent={
        'END_ACTION': 'SELECT_ACTION',
    },
)
