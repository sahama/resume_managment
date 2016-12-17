from mongoengine import *

class User(Document):
    email = StringField(max_length=200, required=True)
    username = StringField(max_length=200, required=True)
    _password = StringField(max_length=200, required=True)
    mobile = StringField(max_length=200, required=True)
    groups = ListField(StringField(max_length=30))

    @property
    def password(self):
        return 'password should be hashed in database and can not recover'

    @password.setter
    def password(self, new_password):
        self._password = self.hash(new_password)

    def check_password(self, new_password):
        return self._password == self.hash(new_password)

    @classmethod
    def hash(cls, password):
        # TODO: hash password geted as arg
        return password



