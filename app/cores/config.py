import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL =  os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:1234@localhost/ecommerceAuth")