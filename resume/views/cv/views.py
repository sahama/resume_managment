from pyramid.view import view_config
from pyramid.request import Request
from resume.models import User



@view_config(route_name='resume_list', renderer='list.jinja2')
def resume_list(context, request: Request):
    users = [user for user in User.objects]

    return {'users': users}

@view_config(route_name='resume_view', renderer='view.jinja2')
def resume_view(context, request: Request):
    user_id = request.matchdict['id']
    user = User.objects(id=user_id)


    return {'user': user}

@view_config(route_name='resume_edit', renderer='edit.jinja2')
def resume_edit(context, request: Request):
    user = request.user


    return {'user': user}

