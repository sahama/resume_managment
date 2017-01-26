from pyramid_layout.panel import panel_config
from resume.libs.path import base
from os.path import join


@panel_config(name='navbar', renderer='templates/panels/navbar.jinja2')
def navbar(context, request):
    return {}

@panel_config(name='footer', renderer='templates/panels/footer.jinja2')
def footer(context, request):

    with open(join(base, 'VERSION.txt')) as f:
        version = f.read()
    return {'version': version}


@panel_config(name='menu', renderer='templates/panels/menu.jinja2')
def menu(context, request):
    def nav_item(name, path, items=[]):
        active = any([item['active'] for item in items]) if items else request.path == path

        item = dict(
            name=name,
            path=path,
            active=active,
            items=items
            )

        return item

    items = []
    # items.append(nav_item('resume', '#', [nav_item(name, request.route_path(name)) for name in ['resume_list','resume_edit']]))
    items.append(nav_item('resume', '#',
                          [nav_item('edit_profile', request.route_path('edit_profile')),
                          nav_item('resume_list', request.route_path('resume_list')),
                          nav_item('resume_edit', request.route_path('resume_edit', id=request.authenticated_userid))] ))
    items.append(nav_item('user_manu', '#', [nav_item(name, request.route_path(name)) for name in ['login','logout','register']]))

    return {'items': items}


@panel_config(name='flash_message', renderer='templates/panels/flash_message.jinja2')
def flash_message(context, request):
    return {}


@panel_config(name='pagination', renderer='templates/panels/pagination.jinja2')
def pagination(context, request, current_page, total_page):
    return {'current_page': current_page, 'total_page': total_page}


@panel_config(name='back_to_top', renderer='templates/panels/back_to_top.jinja2')
def back_to_top(context, request):
    return {}

