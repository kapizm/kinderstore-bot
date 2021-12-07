from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from src import config
from telegram import ReplyKeybordMarkup, ReplyKeybordRemove, Update


bot = Updater(token=config.TOKEN)


logging.basicConfig(
    format=format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start_handler(update: UPDATE, context: CallbackContext) -> int:
    reply_keyboard = [['Зарегистрировать чек', 'Проверить свои чеки']]

    update.message.reply_text(
        'Здравствуйте! Вы бы хотели зарегистрировать в нашем розыгрыше, или проверить ваши зарегистрированные чеки?'
        'Отправьте /cancel чтобы остановить работу бота\n\n',
        reply_markup=ReplyKeybordMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Регистрация или проверка?'
        ),
    )

    return CHOICE

def registration(update, context) -> int:
    update.message.reply_text("""Здравствуйте! Рады приветствовать Вас в розыгрыше «Игрушки покупай – машину забирай» от сети детских магазинов KinderStore! 
Розыгрыш состоится в прямом эфире на нашей инстаграм странице Kinderstore_astana, подпишитесь что быть в курсе!
С условиями конкурса вы можете ознакомиться по данной ссылке ______
Дата розыгрыша 10 января 2022 года в г. Нур-Султан, в 14:00 по местному времени. 
Тех. поддержка +7 702 8 777 """)
    update.message.reply_text("""Для успешной регистрации в розыгрыше Вам необходимо ввести своё имя и фамилию: 
    """)

    return NAME

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'До свидания!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END    


bot.dispatcher.add_handler(CommandHandler("start", start_handler))
