from mongoengine import *


class User(Document):
    email = StringField(max_length=200, required=True)
    # username = StringField(max_length=200, required=True)
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
        print(new_password, self._password)
        return self._password == self.hash(new_password)

    @classmethod
    def hash(cls, password):
        # TODO: hash password geted as arg
        return password

class ResumeField(EmbeddedDocument):
    title = StringField(max_length=64, required=True)

    meta = {'allow_inheritance': True}
    # @property
    # def data(self):
    #     raise NotImplemented



class Phone(ResumeField):
    number = StringField(max_length=200, required=True)

class Email(ResumeField):
    address = StringField(max_length=200, required=True)

class Education(ResumeField):
    degree = StringField(max_length=200, required=True)
    field = StringField(max_length=200, required=True)

class Language(ResumeField):
    level = IntField(min_value=1, max_value=5)

class JobHistory(ResumeField):
    company = StringField(max_length=200, required=True)
    from_date = DateTimeField()
    to_date = DateTimeField()

GENDER = ('Male', 'Female')
class Resume(Document):
    first_name = StringField(max_length=200, required=True)
    middle_name = StringField(max_length=200, required=True)
    last_name = StringField(max_length=200, required=True)
    birthday = DateTimeField()
    nationality = StringField(max_length=50, required=True)
    gender = StringField(max_length=2, choices=GENDER)#انتخاب
    phone = ListField(EmbeddedDocumentField(Phone)) # phone is not translatable

    education = ListField(EmbeddedDocumentField(Education))
    languages = ListField(EmbeddedDocumentField(Language))
    job_history = ListField(EmbeddedDocumentField(JobHistory))
    favorites = ListField(StringField(max_length=300))


def includeme(config):
    settings = config.get_settings()
    mongodb_url = settings.get('mongodb.uri')
    connect(host=mongodb_url)
