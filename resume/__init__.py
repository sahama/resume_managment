from pyramid.config import Configurator


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
