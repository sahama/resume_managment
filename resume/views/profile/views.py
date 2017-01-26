from pyramid.view import view_config
from resume.models import User
import colander
import deform
import json



@view_config(route_name='edit_profile', renderer='templates/edit.jinja2', permission='user')
def profile_view(context, request):

    class Profile(colander.Schema):
        email = colander.SchemaNode(colander.String(), title="Email", readonly=True)
        password = colander.SchemaNode(colander.String(), title="Password", missing='')
        mobile = colander.SchemaNode(colander.String(), title="Mobile")
        first_name = colander.SchemaNode(colander.String(), title="First Name")
        last_name = colander.SchemaNode(colander.String(), title="Last Name")
        gender = colander.SchemaNode(colander.String(), title="Gender")

    class MainSchema(colander.MappingSchema):
        profile = Profile(title='Profile')

    def validator(node, appstruct):
        return True

    schema = MainSchema(validator=validator)
    schema = schema.bind(request=request)
    form = deform.Form(schema, use_ajax=False, action=request.route_url('edit_profile'))
    form.buttons.append(deform.Button(name='submit', title='submit'))
    # print(request.user.to_json())
    # from bson import json_util
    # tmp = json_util.dumps(request.user._collection_obj.find(request.user.objects()._query))
    # print(tmp)

    if request.POST:
        controls = request.POST.items()

        try:
            appstruct = form.validate(controls)
            print(appstruct)


        except:
            appstruct = None
            print('no validate')
        if appstruct:

            user = request.user
            user.to_mongo(appstruct)
            user.email = appstruct['profile']['email']
            user.first_name = appstruct['profile']['first_name']
            user.last_name = appstruct['profile']['last_name']
            user.mobile = appstruct['profile']['mobile']
            user.password = appstruct['profile']['password']
            user.gender = appstruct['profile']['gender']

            user.save()
            request.message.add('your registration complete')

    user_data_json = request.user.to_json()
    user_data = {'profile': json.loads(user_data_json)}
    print(user_data)
    print(request.user.gender)


    return {'form': form, 'user_data': user_data}
