from os.path import join

import polib
from pyramid.request import Request
from pyramid.view import view_config, view_defaults

from resume.libs.path import root


@view_defaults(route_name='translate', renderer='./template.jinja2', permission='admin')
class TranslateView():
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context
        self.message = self.request.message
        self.translate = self.request.translate

    @view_config()
    def main_view(self):
        po = polib.pofile(join(root, 'locale', 'en', 'LC_MESSAGES', 'resume.po'))
        if "update_msg" in self.request.POST:
            for i in self.request.params:
                for t in po:
                    if self.request.params[i] and i == t.msgid:
                        t.msgstr = self.request.params[i]
            po.save()
            po.save_as_mofile(join(root, 'locale', 'en', 'LC_MESSAGES', 'resume.mo'))


        if "new_msg" in self.request.POST:
            msgid = self.request.POST.get('msgid','').strip()
            msgstr = self.request.POST.get('msgstr')
            avalable = False
            for t in po:
                if msgid == t.msgid:
                    t.msgstr = msgstr
                    avalable = True
            if not avalable:
                entry = polib.POEntry()
                entry.msgid=msgid
                entry.msgstr=msgstr
                po.append(entry)

            po.save()
            po.save_as_mofile(join(root, 'locale', 'en', 'LC_MESSAGES', 'resume.mo'))

        return {"po": po}
