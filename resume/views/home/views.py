from pyramid.view import view_config


@view_config(route_name='home', renderer='templates.jinja2')
def my_view(context, request):
    # print("context is", context)
    # print("USer is", User)
    # for u in User.objects:
    #     print(u.email)


    return {'project': 'resume'}
