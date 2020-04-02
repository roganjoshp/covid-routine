import os
import platform

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PW = os.environ.get('POSTGRES_PW')
    POSTGRES_URL = os.environ.get('POSTGRES_URL')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
                                                            user=POSTGRES_USER,
                                                            pw=POSTGRES_PW,
                                                            url=POSTGRES_URL,
                                                            db=POSTGRES_DB)

    SQLALCHEMY_DATABASE_URI = DB_URL
    
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    PERMANENT_SESSION_LIFETIME = 604800
    WTF_CSRF_TIME_LIMIT = None