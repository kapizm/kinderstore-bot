from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext, CommandHandler, ConversationHandler, Filters,
    MessageHandler,
)


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
    update.message.reply_text(
        'Здравствуйте! Рады приветствовать Вас в розыгрыше «Игрушки покупай '
        '– машину забирай» от сети детских магазинов KinderStore! Розыгрыш '
        'состоится в прямом эфире на нашей инстаграм странице '
        'Kinderstore_astana, подпишитесь что быть в курсе! С условиями '
        'конкурса вы можете ознакомиться по данной ссылке ______ Дата '
        'розыгрыша 10 января 2022 года в г. Нур-Султан, в 14:00 по '
        'местному времени. Тех. поддержка +7 702 8 777',
    )
    update.message.reply_text(
        'Для успешной регистрации в розыгрыше Вам необходимо ввести своё имя '
        'и фамилию:',
    )
    return ConversationHandler.END


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
    },
    fallbacks=[CommandHandler('cancel', cancel_handler)],
)
