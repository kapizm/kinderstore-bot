from src.bot import bot

def main(): 
    bot.start_polling()
    bot.idle()
if __name__ == '__main__':
    main()