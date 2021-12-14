from src import config
from src.bot import bot

WEBHOOK_URL_TEMPLATE = 'https://{}.herokuapp.com/{}'


def main():
    if config.HEROKU_APP_NAME:
        bot.start_webhook(
            listen='0.0.0.0',
            port=config.PORT,
            url_path=config.TOKEN,
            webhook_url=WEBHOOK_URL_TEMPLATE.format(
                config.HEROKU_APP_NAME, config.TOKEN,
            ),
        )
    else:
        bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
