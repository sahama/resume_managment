from pyramid.view import view_config, forbidden_view_config
from resume.models import User
import colander
import deform
from pyramid.httpexceptions import (
    HTTPFound
)
from pyramid.security import (
    remember,
    forget
)



@view_config(route_name='register', renderer='templates/register.jinja2', permission='view')
def regsiter_view(context, request):

    class Register(colander.Schema):
        email = colander.SchemaNode(colander.String(), title="Email")
        password = colander.SchemaNode(colander.String(), title="Password")

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
            old_emails = User.objects(email=appstruct['register']['email'])
            if not old_emails:
                user = User()
                user.email = appstruct['register']['email']
                user.password = appstruct['register']['password']
                user.mobile = '123'
                user.save()
                request.message.add('your registration complete')
            else:
                request.message.add('this email address already token')

    for i in User.objects:
        print(dir(i))
        print(i.id)

    return {'project': 'resume', 'form': form}

@forbidden_view_config(renderer='templates/login.jinja2')
@view_config(route_name='login', renderer='templates/login.jinja2', permission='view')
def login_view(context, request):

    class Login(colander.Schema):
        email = colander.SchemaNode(colander.String(), title="Email")
        password = colander.SchemaNode(colander.String(), title="Password")

    class MainSchema(colander.MappingSchema):
        login = Login(title='Register')

    def validator(node, appstruct):
        return True

    schema = MainSchema(validator=validator)
    schema = schema.bind(request=request)
    form = deform.Form(schema, use_ajax=False, action=request.route_url('login'))
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
            user = User.objects(email=appstruct['login']['email'])
            if user and user[0].check_password(appstruct['login']['password']):
                request.message.add('login')

                headers = remember(request, user[0].id)
            else:
                headers = forget(request)
                request.message.add('not login')

            return HTTPFound(location='/', headers=headers)



    return {'form': form}


@view_config(route_name='logout', permission='view')
def logout_view(context, request):
    headers = forget(request)
    request.session.invalidate()
    return HTTPFound(location=request.route_url('home'), headers=headers)


