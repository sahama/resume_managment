from mongoengine import *

class User(Document):
    email = StringField(max_length=200, required=True)
    username = StringField(max_length=200, required=True)
    password = StringField(max_length=200, required=True)
    groups = ListField(StringField(max_length=30))
