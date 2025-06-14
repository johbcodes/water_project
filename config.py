import os

class Config:
    SECRET_KEY = '0d2f82a0ddfbfb49c5ac71b5a0c1df10820390501dc23ab14d47bfe304f3f9f1'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:123456@localhost/water_db'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '0d2f82a0ddfbfb49c5ac71b5a0c1df10820390501dc23ab14d47bfe304f3f9f1')  # For JWT
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Enable SQL query logging
        # Flask settings
    # SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')  # For Flask sessions
    
