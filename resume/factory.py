from pyramid.security import Allow, Everyone, Deny, Authenticated, authenticated_userid
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import SessionAuthenticationPolicy
from .models import User
from pyramid.session import SignedCookieSessionFactory
import pyramid_bowerstatic
import os
from pyramid.request import Request


def group_finder(userid, request):

    groups = []
    if userid:
        user = User.objects(id=userid)
        # user = request.dbsession.query(User).filter_by(username = userid).one()
        groups = user[0].groups
    return groups




components = pyramid_bowerstatic.create_components(
    'resume',
    os.path.join(os.path.dirname(__file__), 'static', 'bower_components')
)

class RootFactory(object):

    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'user'),
               (Allow, 'admins', ['admin','user']),
               ]

    def __init__(self, request: Request):
        self.request = request
        user = User.objects(id=request.authenticated_userid)
        self.request.user = user[0]


        request.include(components, 'jquery')
        request.include(components, 'bootstrap')
        request.include(components, 'jdate')
        request.include(components, 'angular')
        request.include(components, 'jquery-ui')

        request.include(components, 'bootstrap')
        request.include(components, 'bootstrap-rtl')



def includeme(config):
    config.set_root_factory(RootFactory)
    session_factory = SignedCookieSessionFactory(secret='FG%5*%GHgfdsFK4564', timeout=3600, max_age=3600)
    authn_policy = SessionAuthenticationPolicy(callback=group_finder)
    authz_policy = ACLAuthorizationPolicy()

    config.set_session_factory(session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('user')
