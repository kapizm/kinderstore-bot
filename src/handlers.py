from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext, CommandHandler, ConversationHandler, Filters,
    MessageHandler,
)

from src import database
from src.models import User


def start_handler(update: Update, context: CallbackContext):
    reply_keyboard = [['Зарегистрировать чек', 'Проверить свои чеки']]
    update.message.reply_text(
        'Здравствуйте! Вы бы хотели зарегистрировать в нашем розыгрыше, или '
        'проверить ваши зарегистрированные чеки? Отправьте /cancel для отмены',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )
    return 'registration or check'


def registration_handler(update: Update, context: CallbackContext):
    with database.Session() as session:
        users = session.query(User).filter(
            User.telegram_id == update.message.from_user.id,
        )

    if users:
        update.message.reply_text('Вы уже зарегистрированы')
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
        'ввести своё полное имя:',
    )
    return 'registration_name'


def registration_name_handler(update: Update, context: CallbackContext):
    user = User(
        telegram_id=update.message.from_user.id,
        full_name=update.message.text,
    )

    with database.Session() as session, session.begin():
        session.add(user)

    update.message.reply_text('Пользователь сохранен')
    update.message.reply_text('Введите свой номер телефона')
    return 'phone_number'


def phone_handler(update: Update, context: CallbackContext):
    query = database.session.query(User)
    query = query.Filter(User.telegram_id == update.message.from_user.id)
    record = query.one()
    record.phone_number = update.message.text

    update.message.reply_text(
        'Спасибо! Пожалуйста, введите Ваш никнейм '
        'в Instagram',
    )
    return 'ig_account'


def ig_account_handler(update: Update, context: CallbackContext):
    query = database.session.query(User)
    query = query.Filter(User.telegram_id == update.message.from_user.id)
    record = query.one()
    record.ig_account = update.message.text

    update.message.reply_text(
        'Отлично! Пожалуйста, введите номер Вашего чека '
        'с магазина KinderStore',
    )
    return 'store_check'


def registration_end_handler(update: Update, context: CallbackContext):
    pass


def check_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Чекаем')
    return ConversationHandler.END


def cancel_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Отмена', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_handler)],
    states={
        'registration or check': [
            MessageHandler(
                Filters.regex('^Зарегистрировать чек$'), registration_handler,
            ),
            MessageHandler(
                Filters.regex('^Проверить свои чеки$'), check_handler,
            ),
        ],
        'registration_name': [
            MessageHandler(
                Filters.text, registration_name_handler,
            ),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel_handler)],
)
