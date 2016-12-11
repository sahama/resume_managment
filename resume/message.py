import time
from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.events import ContextFound

class Message():
    danger = 'danger'
    warning = 'warning'
    info = 'info'
    success = 'success'
    default = 'default'

    def __init__(self, body='', message_type=info, source='Main', user=None, request=None, mapping={}):
        self.type = message_type
        self.body = body
        self.source = source
        self.request = request
        self.mapping = mapping
        if user:
            self.user = user
        elif request:
            if request.authenticated_userid:
                self.user = self.request.authenticated_userid
            else:
                self.user = 'Guest'
        else:
            self.user = 'Guest'


        if not (source or body):
            self.body = 'no notice found'
            self.type = Message.info

    def add(self, body, message_type=None, source=None, user=None, request=None, mapping=None):
        if message_type:
            self.type = message_type
        if source:
            self.source = source
        if user:
            self.user = user
        if request:
            self.request = request
        if mapping:
            self.mapping = mapping
        self.body = body

        self.request.session.flash({"type": self.type, 'source': self.source, 'user': self.user, 'body': self.body, 'mapping': self.mapping})


    def __repr__(self):

        # return 'source:{0} ip:{4} type:{1} user:{2} message:{3}'.format(
        return '{0} {4} {1} {2} {3}'.format(
            # time.time(),
            '_'.join(self.source).split(),
            '_'.join(self.type).split(),
            self.user,
            (self.body, self.mapping),
            (lambda x : x.remote_addr if x else '')(self.request)
        )

    def __str__(self):
        return self.__repr__()



@subscriber(NewRequest)
def add_message(event):
    request = event.request
    message = Message(request=request)
    request.message = message


# @subscriber(ContextFound)
# def add_message_context(event):
#     request = event.request
#     print(request.message)
#     request.context.message = request.message


def includeme(config):
    config.scan('.message')
