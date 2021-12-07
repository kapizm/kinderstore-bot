import os

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

PORT = os.getenv('PORT')
