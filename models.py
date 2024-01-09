from flask_mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):
    username = db.StringField(max_length=20, unique=True, required=True)
    password = db.StringField(required=True)
    # MongoEngine does not require a separate relationship field like SQLAlchemy.
    # Relationships are typically handled by reference fields within the documents themselves.

class Player(db.Document):
    name = db.StringField(max_length=100, required=True)
    position = db.StringField(max_length=10, required=True)
    at_bats = db.IntField(required=True)
    hits = db.IntField(required=True)
    avg = db.FloatField(required=True)
    user_id = db.ReferenceField(User, required=True)
