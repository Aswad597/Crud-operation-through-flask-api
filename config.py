import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://Aswad:123@DESKTOP-815HJBN\SQLEXPRESS01/AswadDB?driver=ODBC+Driver+17+for+SQL+Server'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_generated_secret_key_here'
