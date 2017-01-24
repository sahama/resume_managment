from pyramid.view import view_config
from pyramid.request import Request
from resume.models import User
import colander
import deform
from .resource import Factory

@view_config(route_name='resume_list', renderer='list.jinja2')
def resume_list(context, request: Request):
    users = [user for user in User.objects]

    return {'users': users}

@view_config(route_name='resume_view', renderer='view.jinja2')
def resume_view(context, request: Request):
    user_id = request.matchdict['id']
    user = User.objects(id=user_id)


    return {'user': user}

@view_config(route_name='resume_edit', renderer='edit.jinja2', permission='edit')
def resume_edit(context, request: Request):
    user_id = request.matchdict['id']
    sample_appstruct={'resume_form': {'last_name': 'مهدوی', 'mobile': '09106853582', 'password': '1', 'email': 's.h.mahdavi@chmail.ir', 'first_name': 'سید حمید'}, 'educations': [{'degree': 'dr', 'school': 'fdsa'}, {'degree': 'fdsfdsa', 'school': 'dd'}]}

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
        educations = Educations(widget=deform.widget.SequenceWidget(orderable=True), title='Educations')

    def validator(node, appstruct):
        return True

    schema = MainSchema(validator=validator)
    schema = schema.bind(request=request)
    form = deform.Form(schema, use_ajax=False, action=request.route_url('resume_edit', id=user_id))
    form.buttons.append(deform.Button(name='submit', title='submit'))


    if request.POST:
        controls = request.POST.items()

        try:
            appstruct = form.validate(controls)
            print(appstruct)


        except:
            appstruct = None
            print('no validate')
        if appstruct:
            pass
    user = request.user


    return {'user': user, 'form': form, 'appstruct': sample_appstruct}

