from pyramid.view import view_config


@view_config(route_name='home', renderer='templates.jinja2')
def my_view(context, request):


    return {'project': 'resume'}
