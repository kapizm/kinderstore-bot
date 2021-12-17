from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from src import database, helpers
from src.models import User


def my_checks_handler(update: Update, context: CallbackContext):
    text = 'Ваши чеки:\n'

    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.callback_query.from_user.id,
        ).first()

        if user.checks:
            for check in user.checks:
                text = f'• {helpers.get_price(check.number)}',
        else:
            text = 'У вас пока нет зарегистрированных чеков'

    buttons = [
        [
            InlineKeyboardButton(
                'Зарегистрировать чек', callback_data='add_check',
            ),
        ],
    ]
    update.callback_query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(buttons),
    )
    return 'SELECT_ACTION'
