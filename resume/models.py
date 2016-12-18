from mongoengine import *
GENDER = ('Male', 'Female')
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

class Resume(Document):
    firstname = StringField(max_length=200, required=True)
    lastname = StringField(max_length=200, required=True)
    birthday = DateTimeField()
    nationality = StringField(max_length=50, required=True)
    gender = StringField(max_length=2, choices=GENDER)#انتخاب
    mobile_number =IntField(max_length=20, required=True)#integer
    phone_number = IntField(max_length=20, required=True)#integer
    education = StringField(max_length=500)
    languages = StringField(max_length=60)
    job_history = StringField(max_length=500)
    favorites = StringField(max_length=300)

    #نام:
   # نام خانوادگی:
    #تاریخ تولد:
#محل تولد
#جنسیت:
#شماره تلفن همراه:
#تلفن محل سکونت:#
#تحصیلات
#زبان ها
#سوابق شغلی
#زمینه های کاری (تخصص / علایق):


