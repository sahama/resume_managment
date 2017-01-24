def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_route('home', '/')
    config.add_route('register', '/register')
    config.add_route('translate', '/translate')
    config.add_route('login', '/login') # id user_group exp_date class_service
    config.add_route('logout', '/logout') # id user_group exp_date class_service
    config.add_route('resume_list', '/resume') # id user_group exp_date class_service
    config.add_route('resume_edit', '/resume/edit') # id user_group exp_date class_service
    config.add_route('resume_view', '/resume/{id}') # id user_group exp_date class_service
