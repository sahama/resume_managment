from pyramid.security import Authenticated
from pyramid.security import Allow, Everyone, Deny, DENY_ALL
from resume.factory import RootFactory
from bson import objectid

class Factory(RootFactory):
    @property
    def __acl__(self):
        owner = self.request.matchdict['id']
        return [(Allow, owner, 'edit') ]

