from pyramid.config import Configurator

######### Mahdavi ##############
# this is monkey patch for bower static
import bowerstatic.core as core
def tmp(self):
    with open(self.component.get_filename(self.component.version, self.file_path), encoding='latin1') as f:
        return f.read()

core.Resource.content = tmp


def load_component(self, path, bower_filename, version=None, autoversion=False):

    bower_json_filename = core.os.path.join(path, bower_filename)
    with open(bower_json_filename, 'r', encoding='latin1') as f:
        data = core.json.load(f)
    if 'main' not in data:
        main = []
    elif isinstance(data['main'], list):
        main = data['main']
    else:
        main = [data['main']]
    dependencies = data.get('dependencies')
    if dependencies is None:
        dependencies = {}
    if not version:
        version = data.get('_release')
    if not version:
        try:
            version = data['version']
        except KeyError:
            raise ValueError('Missing _release and version in {}'.format(
                path))
    return core.Component(self.bower,
                     self,
                     path,
                     data['name'],
                     version,
                     main,
                     dependencies,
                     autoversion=autoversion)

core.ComponentCollection.load_component = load_component
############# end ###############


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')
    config.include('pyramid_bowerstatic')
    config.include('pyramid_layout')
    config.include('.factory')
    config.include('.i18n')
    config.include('.message')
    config.include('.routes')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
