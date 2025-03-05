import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
DB_PASSWORD_SAKILA = os.getenv("DB_PASSWORD_SAKILA")
DB_PASSWORD_ICH_EDIT = os.getenv("DB_PASSWORD_ICH_EDIT")


