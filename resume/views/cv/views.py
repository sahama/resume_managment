from pyramid.view import view_config
from pyramid.request import Request
from resume.models import User
import colander
import deform


@view_config(route_name='resume_list', renderer='list.jinja2')
def resume_list(context, request: Request):
    users = [user for user in User.objects]

    return {'users': users}

@view_config(route_name='resume_view', renderer='view.jinja2')
def resume_view(context, request: Request):
    user_id = request.matchdict['id']
    user = User.objects(id=user_id)


    return {'user': user}

@view_config(route_name='resume_edit', renderer='edit.jinja2', permission='user')
def resume_edit(context, request: Request):
    class ResumeForm(colander.Schema):
        email = colander.SchemaNode(colander.String(), title="Email")
        password = colander.SchemaNode(colander.String(), title="Password")
        first_name = colander.SchemaNode(colander.String(), title="First Name")
        last_name = colander.SchemaNode(colander.String(), title="last Name")
        mobile = colander.SchemaNode(colander.String(), title="Mobile")

    class Education(colander.Schema):
        degree = colander.SchemaNode(colander.String(), title="Degree")
        school = colander.SchemaNode(colander.String(), title="School")

    class Educations(colander.SequenceSchema):
        education = Education()



    class MainSchema(colander.MappingSchema):
        resume_form = ResumeForm(title='Resume')
        educations = Educations(title='Educations')

    def validator(node, appstruct):
        return True

    schema = MainSchema(validator=validator)
    schema = schema.bind(request=request)
    form = deform.Form(schema, use_ajax=False, action=request.route_url('resume_edit'))
    form.buttons.append(deform.Button(name='submit', title='submit'))

    print(dir(form))

    if request.POST:
        controls = request.POST.items()

        try:
            appstruct = form.validate(controls)
            # print(appstruct)


        except:
            appstruct = None
            print('no validate')
        if appstruct:
            pass
    user = request.user


    return {'user': user, 'form': form}

