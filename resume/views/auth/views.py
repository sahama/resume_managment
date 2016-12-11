from pyramid.view import view_config
from resume.models import User
import colander
import deform


@view_config(route_name='register', renderer='templates/register.jinja2')
def regsiter_view(context, request):

    class Register(colander.Schema):
        username = colander.SchemaNode(colander.String(), title="User Name")
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
            print(appstruct)


        except:
            appstruct = None
            print('no validate')

    return {'project': 'resume', 'form': form}
