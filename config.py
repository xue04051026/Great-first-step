import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:142857xyp@localhost:3306/studentinfo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

