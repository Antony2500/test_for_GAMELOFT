import os


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATA_FILE = 'fixtures.json'
