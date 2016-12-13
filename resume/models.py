from mongoengine import *

class User(Document):
    email = StringField(max_length=200, required=True)
    username = StringField(max_length=200, required=True)
    _password = StringField(max_length=200, required=True)
    mobile = StringField(max_length=200, required=True)
    groups = ListField(StringField(max_length=30))

    @property
    def password(self):
        return 'password should be hashed in database'

    @password.setter
    def password(self, new_password):
        # TODO: using a method to hashing password in database
        self._password = new_password

    def check_password(self, new_password):
        return self._password == new_password



