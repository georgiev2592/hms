#!/usr/bin/env python

import web, hashlib, os, MySQLdb, random
from web import form
from datetime import datetime
from os import urandom
import time

web.config.debug = False

# render = web.template.render('templates/', base='layout')

urls = (
    '/', 'Login',
    '/logout', 'Logout',
    '/register', 'Register',
    '/home', 'Home',
    '/about', 'About',
    '/contact', 'Contact'
)

app = web.application(urls, globals())
# db = web.database(dbn='mysql', db='hms', user='wreckingball', pw='patricksux', host='hms.cytvwijmz1je.us-west-2.rds.amazonaws.com')
db = MySQLdb.connect(host = 'hms.cytvwijmz1je.us-west-2.rds.amazonaws.com',
                     user = 'wreckingball',
                     passwd = 'hmsFinalProject',
                     db = 'hms',
                     unix_socket = '/media/media/mysql/mysql.sock')
cur = db.cursor()

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': 0, 'privilege': -1, 'name': ''})
    web.config._session = session
else:
    session = web.config._session

class Login:
    login_form = form.Form(
        form.Textbox('email',
            form.notnull,
            description='Email',
            id='emailBox',
            class_ = 'form-control',
            placeholder='Enter your email'),
        form.Password('password',
            form.notnull,
            description='Password',
            id='passwordBox',
            class_ = 'form-control',
            placeholder='Enter your password'),
        form.Button('Login',
            id='loginButton',
            class_ = 'btn btn-default btn-block'))

    nullform = form.Form()

    def GET(self):
        if logged():
            render = create_render(session.privilege)
            return '%s' % render.index('HMS | Login', self.nullform, '', '', 'Already logged in.')
        else:
            render = create_render(session.privilege)
            return '%s' % render.index('HMS | Login', self.login_form(), '', '', '')

    def POST(self):
        form = self.login_form()

        if not form.validates():
            session.login = 0
            session.privilege = -1
            render = create_render(session.privilege)
            return render.index('HMS | Login', form, '', '', 'Invalid form data.')

        email = dict(email = form.d.email)

        # ident = db.select('Users', where={'email : $email'}, vars=email)
        cur.execute('SELECT * FROM Users WHERE email=%s', (form.d.email))
        ident = fetchOneAssoc(cur)

        salt = ident['encrypted_password'][:40]
        pw = hashlib.sha1(salt + form.d.password).hexdigest()

        # try:
        if pw == ident['encrypted_password'][40:]:
            session.login = 1
            session.privilege = ident['privilege']
            session.name = ident['first_name'] + ' ' + ident['last_name']
            render = create_render(session.privilege)

            list_of_users = self._generateList()
            list_of_comments = self._generateListComments()

            return render.home('HMS | Home', ident['first_name'] + ' ' + ident['last_name'], '', '', '', list_of_users, list_of_comments)
        else:
            session.login = 0
            session.privilege = -1
            render = create_render(session.privilege)
            return render.index('HMS | Login', form, '', '', 'Username/Password Incorrect')
        # except:
        #     session.login = 0
        #     session.privilege = -1
        #     render = create_render(session.privilege)
        #     return render.index('HMS | Login', form, '', '', 'Username/Password Incorrect')

    def _generateList(self):
        cur.execute('SELECT * FROM Users')
        count = 0

        for row in cur.fetchall():
            count += 1

        cur.execute('SELECT * FROM Users')
        list_of_users = [fetchOneAssoc(cur) for k in range(count)]

        print list_of_users
        return list_of_users

    def _generateListComments(self):
        cur.execute('SELECT * FROM Comments')
        count = 0

        for row in cur.fetchall():
            count += 1

        cur.execute('SELECT * FROM Comments')
        list_of_comments = [fetchOneAssoc(cur) for k in range(count)]

        print list_of_comments
        return list_of_comments

class Register:
    register_form = form.Form(
        form.Textbox("first_name",
            form.notnull,
            description = "First Name",
            class_ = "form-control",
            placeholder='Enter employee first name'),
        form.Textbox("last_name",
            form.notnull,
            description = "Last Name",
            class_ = "form-control",
            placeholder='Enter employee last name'),
        form.Textbox("email",
            form.notnull,
            description = "Email",
            class_ = "form-control",
            placeholder='Enter employee email'),
        form.Dropdown('privilege', 
            [('0', 'Front Desk'), ('1', 'Cleaning Personnel')],
            description = "Role",
            class_ = "form-control",
            placeholder='Select employee work position'),
        form.Password("password",
            form.notnull,
            description = "Password",
            class_ = "form-control",
            placeholder='Enter employee password'),
        form.Password('confirm_password',
            description = "Confirm Password",
            class_ = "form-control",
            placeholder='Confirm employee password'),
        form.Button("Register",
            id='registerButton',
            class_ = "btn btn-default btn-block"),
        validators = [form.Validator("Passwords didn't match.", lambda i: i.password == i.confirm_password)]
        )

    nullform = form.Form()

    def GET(self):
        usr = ''

        if logged():
            usr = 'placeholder'
            # render = create_render(session.privilege)
            # return render.register("HMS | Register", self.nullform, "", "", "Already logged in.")
        else:
            # session.login = 0
            # session.privilege = -1
            pass
        
        render = create_render(session.privilege)
        return render.register("HMS | Register", self.register_form(), usr, "", "")

    def POST(self):
        form = self.register_form()
        msg = ""
        err = ""
        
        if not form.validates():
            session.login = 0
            session.privilege = -1
            err = "Invalid fields."
        else:

            cur.execute('SELECT * FROM Users WHERE email=%s', (form.d.email))
            ident = fetchOneAssoc(cur)

            try:
                if form.d.email == ident['email']:
                    session.login = 0
                    session.privilege = -1
                    err = "User already registered."
                else:
                    self.__helper(form)
                    msg = "User registered."
            except:
                self.__helper(form)
                msg = "User registered."

        list_of_users = self._generateList()

        render = create_render(session.privilege)
        return render.home('HMS | Home', session.name, '', msg, '', list_of_users)

    def __helper(self, form):
        salt = hashlib.sha1(urandom(16)).hexdigest()

        #SQL query to INSERT a record into the table FACTRESTTBL.
        cur.execute('''INSERT INTO Users (first_name, last_name, encrypted_password, email, created_at, updated_at, current_sign_in_at, last_sign_in_at, current_sign_in_ip, last_sign_in_ip, privilege)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (form.d.first_name, 
                        form.d.last_name, 
                        salt + hashlib.sha1(salt + form.d.password).hexdigest(),
                        form.d.email,
                        self.__stamp(datetime.now()),
                        self.__stamp(datetime.now()),
                        self.__stamp(datetime.now()),
                        self.__stamp(datetime.now()),
                        web.ctx['ip'],
                        web.ctx['ip'],
                        form.d.privilege))

        # Commit your changes in the database
        db.commit()

    def __stamp(self, dt):
      # turns a python datetime object into a unix time stamp (seconds)
      return int(time.mktime( dt.timetuple() ))

class Logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')

class Home:
    def GET(self):
        render = create_render(session.privilege)
        return render.home('HMS | Home', '', '', '', '')

class About:
    def GET(self):
        session.login = 0
        session.privilege = -1
        render = create_render(session.privilege)
        return render.about('HMS | About', '')  

class Contact:
    contact_form = form.Form(
        form.Textbox('name',
            form.notnull,
            description="Name",
            class_ = 'form-control',
            placeholder='Enter your first and last name'),
        form.Textbox('email',
            form.notnull,
            description='Email',
            id='emailBox',
            class_ = 'form-control',
            placeholder='Enter your email'),
        form.Textarea('content',
            form.notnull,
            description='Questions or Comments',
            id='passwordBox',
            class_ = 'form-control',
            style = 'height: 150px',
            placeholder='Enter your questions or comments'),
        form.Button('Submit',
            id='submitButton',
            class_ = 'btn btn-default btn-block'))

    nullform = form.Form()


    def GET(self):
        form = self.contact_form()
        msg = ''
        err = ''

        render = create_render(session.privilege)
        return render.contact('HMS | Contact', '', form, msg, err) 

    def POST(self):
        form = self.contact_form()
        msg = ''
        err = ''
        
        if not form.validates():
            err = 'Invalid fields.'
        else:
            msg = "Comment was successfully posted."
            self.__helper(form)

        render = create_render(session.privilege)
        return render.contact('HMS | Contact', '', form, msg, err)

    def __helper(self, form):
        cur.execute('''INSERT INTO Comments (name, email, content)
                        VALUES (%s, %s, %s)''',
                        (form.d.name, 
                        form.d.email, 
                        form.d.content))

        # Commit your changes in the database
        db.commit()

def logged():
    if session.login == 1:
        return True
    else:
        return False

def create_render(privilege):
    if logged():
        if privilege == 0:
            render = web.template.render('templates/front_desk', base='../layout')
        elif privilege == 1:
            render = web.template.render('templates/cleaning_personnel', base='../layout')
        elif privilege == 2:
            render = web.template.render('templates/admin', base='../layout')
        else:
            render = web.template.render('templates/', base='layout')
    else:
        render = web.template.render('templates/', base='layout')
    return render

def fetchOneAssoc(cursor):
    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = {}

    for (name, value) in zip(desc, data) :
        dict[name[0]] = value

    return dict

if __name__ == "__main__":
    app.run()