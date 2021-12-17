from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, ConversationHandler,
    Filters, MessageHandler,
)

from src import database, helpers
from src.models import Chance, Check, User


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
        print(check)
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
            f'Чек не найден {check_data}',
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
            registered_at=check_data['registered_at'],
        )

    with database.Session() as session, session.begin():
        session.add(check)

    Chances_list = []
    chances_counter = helpers.get_chances_from_price(check_data['price'])

    with database.Session() as session:
        chance = session.query(Chance).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()

        while chances_counter > 0:
            chance = Chance(
                check_id=check.id,
            )
            Chances_list.append(chance)
            with database.Session() as session, session.begin():
                session.add(chance)
            chances_counter -= 1

    update.message.reply_text(
        'Дорогой Покупатель!\nПоздравляем вас, вы успешно прошли ',
        'регистрацию на розыгрыш АВТОМОБИЛЯ Chevrolet Spark! 🚗\n',
        'Следите за нашим аккаунтом в Инстаграм @kinderstore_astana 😍\n',
        'Если возникнут вопросы, обращайтесь в тех. поддержку по '
        'номеру телефона нашего call-центра: +7(702)8777045\n',
        f'{Chances_list}',
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    Chances_list.clear()

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
