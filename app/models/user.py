from datetime import datetime
from mongoengine import Document, StringField, DateTimeField

class User(Document):
    name = StringField(required=True, max_length=50)
    email = StringField(required=True)
    password = StringField(required=True)

    # Logging values
    created_at = DateTimeField(default=datetime.now)
    last_updated = DateTimeField(default=datetime.now, onupdate=datetime.now)
    deleted_at = DateTimeField(default=None)