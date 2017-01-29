from pyramid.view import view_config, view_defaults
from pyramid.request import Request
from resume.models import User
import colander
import deform
from .resource import Factory
import json
from deform import widget


@view_defaults()
class ResemeView():
    def __init__(self,context, request):
        self.request = request
        self.context = context

        class Education(colander.Schema):
            degree = colander.SchemaNode(colander.String(), title="Degree")
            school = colander.SchemaNode(colander.String(), title="School")
            field = colander.SchemaNode(colander.String(), title="Field")

        class Skill(colander.Schema):
            title = colander.SchemaNode(colander.String(), title="Title")

        class Experience(colander.Schema):
            title = colander.SchemaNode(colander.String(), title="Title")
            company = colander.SchemaNode(colander.String(), title="Company")
            from_date = colander.SchemaNode(colander.String(), title="From")
            to_date = colander.SchemaNode(colander.String(), title="To")

        class Educations(colander.SequenceSchema):
            educations = Education()

        class Skills(colander.SequenceSchema):
            skills = Skill()

        class Experiences(colander.SequenceSchema):
            experiences = Experience()

        class ResumeFormEdit(colander.Schema):
            email = colander.SchemaNode(colander.String(), title="Email")
            first_name = colander.SchemaNode(colander.String(), title="First Name")
            last_name = colander.SchemaNode(colander.String(), title="last Name")
            mobile = colander.SchemaNode(colander.String(), title="Mobile", missing='')
            summary = colander.SchemaNode(
                colander.String(),
                widget=widget.RichTextWidget(options={"mode": "exact", "plugins": [
                    'advlist autolink lists link image charmap print preview anchor',
                    'searchreplace visualblocks code fullscreen',
                    'insertdatetime media table contextmenu paste code'
                ],}),
                description='Enter Summery')

            # summary_view = colander.SchemaNode(colander.String(), title="", missing='', readonly=True)

            educations = Educations(widget=deform.widget.SequenceWidget(orderable=True), title='Educations')
            skills = Skills(widget=deform.widget.SequenceWidget(orderable=True), title='Skills')
            experiences = Experiences(widget=deform.widget.SequenceWidget(orderable=True), title='Experiences')

        class ResumeFormView(colander.Schema):
            email = colander.SchemaNode(colander.String(), title="Email")
            first_name = colander.SchemaNode(colander.String(), title="First Name")
            last_name = colander.SchemaNode(colander.String(), title="last Name")
            mobile = colander.SchemaNode(colander.String(), title="Mobile", missing='')
            summary = colander.SchemaNode(colander.String(), title="Summary", missing='')


            educations = Educations(widget=deform.widget.SequenceWidget(orderable=True), title='Educations')
            skills = Skills(widget=deform.widget.SequenceWidget(orderable=True), title='Skills')
            experiences = Experiences(widget=deform.widget.SequenceWidget(orderable=True), title='Experiences')

        class EditSchema(colander.MappingSchema):
            resume_form = ResumeFormEdit(title='Resume')

        class ViewSchema(colander.MappingSchema):
            resume_form = ResumeFormView(title='Resume')

        def validator(node, appstruct):
            return True

        self.view_schema = ViewSchema(validator=validator)
        self.edit_schema = EditSchema(validator=validator)
        self.view_schema = self.view_schema.bind(request=request)
        self.edit_schema = self.edit_schema.bind(request=request)

    @view_config(route_name='resume_list', renderer='list.jinja2')
    def resume_list(self):
        users = [user for user in User.objects]


        return {'users': users}



    @view_config(route_name='resume_view', renderer='view.jinja2')
    def resume_view(self):
        user_id = self.request.matchdict['id']
        user = User.objects(id=user_id)[0]


        user_data_json = user.to_json()
        user_data = {'resume_form': json.loads(user_data_json)}
        print(user_data)

        form = deform.Form(self.view_schema, use_ajax=False)
        # form.children[0].children[4] =  colander.SchemaNode(colander.String(), title="Summary")
        # print(form.children[0].children[4])
        return {'form': form, 'user_data': user_data}




    @view_config(route_name='resume_edit', renderer='edit.jinja2', permission='edit')
    def resume_edit(self):
        user_id = self.request.matchdict['id']
        sample_appstruct={'resume_form': {'last_name': 'مهدوی', 'mobile': '09106853582', 'password': '1', 'email': 's.h.mahdavi@chmail.ir', 'first_name': 'سید حمید'}, 'educations': [{'degree': 'dr', 'school': 'fdsa'}, {'degree': 'fdsfdsa', 'school': 'dd'}]}

        form = deform.Form(self.edit_schema, use_ajax=False, action=self.request.route_url('resume_edit', id=user_id))
        form.buttons.append(deform.Button(name='submit', title='submit'))

        if self.request.POST:
            controls = self.request.POST.items()

            try:
                appstruct = form.validate(controls)
                print(appstruct)


            except:
                appstruct = None
                print('no validate')
            if appstruct:
                user = self.request.user
                # user.to_mongo(appstruct)
                user.email = appstruct['resume_form']['email']
                user.first_name = appstruct['resume_form']['first_name']
                user.last_name = appstruct['resume_form']['last_name']
                user.mobile = appstruct['resume_form']['mobile']
                user.summary = appstruct['resume_form']['summary']

                # for edu in appstruct['profile']['mobile']['educations']:

                user.educations = appstruct['resume_form']['educations']
                user.skills = appstruct['resume_form']['skills']
                user.experiences = appstruct['resume_form']['experiences']
                user.save()
                self.request.message.add('complete')

        user = self.request.user
        user_data_json = self.request.user.to_json()
        user_data = {'resume_form': json.loads(user_data_json)}
        print(user_data)


        return {'form': form, 'user_data': user_data}

