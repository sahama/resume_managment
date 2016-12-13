from pyramid.view import view_config
from resume.models import User
import colander
import deform


@view_config(route_name='register', renderer='templates/register.jinja2')
def regsiter_view(context, request):

    class Register(colander.Schema):
        username = colander.SchemaNode(colander.String(), title="User Name")
        password = colander.SchemaNode(colander.String(), title="Password")
        email = colander.SchemaNode(colander.String(), title="Email")

    class MainSchema(colander.MappingSchema):
        register = Register(title='Register')

    def validator(node, appstruct):
        return True

    schema = MainSchema(validator=validator)
    schema = schema.bind(request=request)
    form = deform.Form(schema, use_ajax=False, action=request.route_url('register'))
    form.buttons.append(deform.Button(name='submit', title='submit'))

    if request.POST:
        controls = request.POST.items()

        try:
            appstruct = form.validate(controls)
            # print(appstruct)


        except:
            appstruct = None
            print('no validate')
        if appstruct:
            old_usernames = User.objects(username=appstruct['register']['username'])
            old_emails = User.objects(email=appstruct['register']['email'])
            print('username', old_usernames)
            print('email', old_emails)
            if not old_usernames and not old_emails:
                user = User()
                user.username = appstruct['register']['username']
                user.email = appstruct['register']['email']
                user.password = appstruct['register']['password']
                user.mobile = '123'

                user.save()
    for i in User.objects:
        print(i.username)

    return {'project': 'resume', 'form': form}
