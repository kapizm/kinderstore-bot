import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

PORT = os.getenv('PORT')

DATABASE_URL = os.getenv('DATABASE_URL')

API_BASE_URL = os.getenv('API_BASE_URL')

API_TOKEN = os.getenv('API_TOKEN')
