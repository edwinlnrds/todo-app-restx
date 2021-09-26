from mongoengine import connect

class DatabaseManager(object):
    def __init__(self):
        self.db = None

    @staticmethod
    def open_database():
        from app.config import Config
        connect(
            host=f'mongodb+srv://{Config.MONGODB_USERNAME}:{Config.MONGODB_PASSWORD}@{Config.MONGODB_HOST}/{Config.MONGODB_NAME}?retryWrites=true&w=majority'
        )
