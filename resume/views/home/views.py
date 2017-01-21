from pyramid.view import view_config
from pyramid.request import Request
from resume.models import User


@view_config(route_name='home', renderer='templates.jinja2')
def my_view(context, request: Request):
    user = None
    if request.authenticated_userid:
        user = User.objects(id=request.authenticated_userid)[0]
        print(user.email)

    return {'user': user}
