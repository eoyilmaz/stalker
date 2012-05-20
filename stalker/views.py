from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config, forbidden_view_config

from sqlalchemy.exc import DBAPIError

from stalker.db import DBSession

from stalker import User

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_stalker_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='home', renderer='templates/home.jinja2',
             permission='view')
def home(request):
    login_name = authenticated_userid(request)
    return {'current_user': login_name}


@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        
        # need to find the user
        # first check with the login_name attribute
        user_obj = DBSession.query(User).filter_by(login_name=login).first()
        
        if not user_obj:
            # then by the email
            user_obj = DBSession.query(User).filter_by(email=login).first()
            if user_obj:
                login = user_obj.login_name
        
        if user_obj and user_obj.check_password(password):
            headers = remember(request, login)
            return HTTPFound(
                location=came_from,
                headers=headers
            )
        
        message = 'Wrong username or password!!!'
    
    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password
    )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        location=request.route_url('login'),
        headers=headers
    )
