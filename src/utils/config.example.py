
class Config():
    SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = ''

    ONEID_LOGIN = ""
    ONEID_PASSWORD = ""
    ONEID_URL = "" 

    HOST = ''
    PORT = None

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass