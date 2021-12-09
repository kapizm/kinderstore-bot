from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, CommandHandler, ConversationHandler, Filters,
    MessageHandler,
)

from src import database
from src.models import User


NAME, PHONE_NUMBER, INSTAGRAM = range(3)


def start_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()

    if user:
        update.message.reply_text(
            f'{user.full_name}, вы уже зарегистрированы',
            reply_markup=ReplyKeyboardMarkup([['Зарегистрировать чек']]),
        )
        return ConversationHandler.END

    update.message.reply_text(
        'Здравствуйте! Рады приветствовать Вас в розыгрыше «Игрушки покупай '
        '– машину забирай» от сети детских магазинов KinderStore!/nРозыгрыш '
        'состоится в прямом эфире на нашей инстаграм странице '
        'Kinderstore_astana, подпишитесь что быть в курсе! С условиями '
        'конкурса вы можете ознакомиться по данной ссылке ______/nДата '
        'розыгрыша 10 января 2022 года в г. Нур-Султан, в 14:00 по '
        'местному времени./nТех. поддержка +7 702 8 777',
    )
    update.message.reply_text(
        'Для успешной регистрации в розыгрыше Вам необходимо '
        'ввести своё полное имя',
    )
    return NAME


def save_name_handler(update: Update, context: CallbackContext):
    user = User(
        telegram_id=update.message.from_user.id,
        full_name=update.message.text,
    )

    with database.Session() as session, session.begin():
        session.add(user)

    update.message.reply_text('Введите свой номер телефона')
    return PHONE_NUMBER


def save_phone_number_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()
        user.phone_number = update.message.text
        session.commit()

    update.message.reply_text('Введите свой никнейм в instagram')
    return INSTAGRAM


def save_instagram_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        user = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        ).first()
        user.ig_account = update.message.text
        session.commit()
        update.message.reply_text(
            f'{user.full_name}, вы успешно зарегистрировались',
            reply_markup=ReplyKeyboardMarkup([['Зарегистрировать чек']]),
        )

    return ConversationHandler.END


def cancel_handler(update: Update, context: CallbackContext):
    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_handler)],
    states={
        NAME: [MessageHandler(
            Filters.text, save_name_handler,
        )],
        PHONE_NUMBER: [MessageHandler(
            Filters.text, save_phone_number_handler,
        )],
        INSTAGRAM: [MessageHandler(
            Filters.text, save_instagram_handler,
        )],
    },
    fallbacks=[CommandHandler('cancel', cancel_handler)],
)
