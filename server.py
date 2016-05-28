#!/usr/bin/env python

import web, crypto, hashlib, os, MySQLdb, random
from web import form

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
                     passwd = 'patricksux',
                     db = 'hms',
                     unix_socket = '/media/media/mysql/mysql.sock')
cur = db.cursor()

if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': 0, 'privilege': 0})
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
		pw = hashlib.sha1(form.d.password).hexdigest()

		# ident = db.select('Users', where={'email : $email'}, vars=email)
		cur.execute('SELECT * FROM Users WHERE email=%s', (form.d.email))
		ident = fetchOneAssoc(cur)

		try:
			if pw == ident['encrypted_password']:
				session.login = 1
				session.privilege = ident['privilege']
				render = create_render(session.privilege)
				return render.home('HMS | Home', ident['first_name'] + ' ' + ident['last_name'], '', '', '')
			else:
				session.login = 0
				session.privilege = -1
				render = create_render(session.privilege)
				return render.index('HMS | Login', form, '', '', 'Username/Password Incorrect')
		except:
			session.login = 0
			session.privilege = -1
			render = create_render(session.privilege)
			return render.index('HMS | Login', form, '', '', 'Username/Password Incorrect')

class Register:
	register_form = form.Form(
		form.Textbox("first_name",
			form.notnull,
			description = "First Name",
			class_ = "form-control",
			placeholder='Enter your first name'),
		form.Textbox("last_name",
			form.notnull,
			description = "Last Name",
			class_ = "form-control",
			placeholder='Enter your last name'),
		form.Textbox("email",
			form.notnull,
			description = "Email",
			class_ = "form-control",
			placeholder='Enter your email'),
		form.Dropdown('privilege', 
			[('0', 'Front Desk'), ('1', 'Cleaning Personnel')],
			description = "Role",
			class_ = "form-control",
			placeholder='Select your work position'),
		form.Password("password",
			form.notnull,
			description = "Password",
			class_ = "form-control",
			placeholder='Enter your password'),
		form.Password('confirm_password',
			description = "Confirm Password",
			class_ = "form-control",
			placeholder='Confirm your password'),
		form.Button("Register",
			id='registerButton',
			class_ = "btn btn-default btn-block"),
    	validators = [form.Validator("Passwords didn't match.", lambda i: i.password == i.confirm_password)]
		)

	nullform = form.Form()

	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return render.register("HMS | Register", self.nullform, "", "", "Already logged in.")
		else:
			session.login = 0
			session.privilege = -1
			render = create_render(session.privilege)
			return render.register("HMS | Register", self.register_form(), "", "", "")

	def POST(self):
		global user_ids
		form = self.register_form()
		msg = ""
		err = ""
		
		if not form.validates():
			session.login = 0
			session.privilege = -1
			err = "Invalid fields."
		else:

			email = dict(email = form.d.email)
			ident = db.select('Users', where='email = $email', vars=email)

			try:
				if form.d.email == ident['email']:
					session.login = 0
					session.privilege = -1
					err = "User already registered."
				else:
					self.__helper(form)
			except:
				self.__helper(form)

		render = create_render(session.privilege)
		return render.register("HMS | Register", self.nullform(), "", msg, err)

	def __helper(self, form):

		#Set the password and role: only non-admin "users" can be created
		#through the web interface
		db.insert('Users', 
			first_name = form.d.first_name, 
			last_name = form.d.last_name, 
			encrypted_password = hashlib.sha1(form.d.password).hexdigest(),
			email = form.d.email,
			created_at = web.SQLLiteral("NOW()"),
			updated_at = web.SQLLiteral("NOW()"),
			current_sign_in_at = web.SQLLiteral("NOW()"),
			last_sign_in_at = web.SQLLiteral("NOW()"),
			current_sign_in_ip = web.ctx['ip'],
			last_sign_in_ip = web.ctx['ip'],
			privilege = form.d.privilege)

		msg = "User registered."

		session.login = 1
		session.privilege = form.d.privilege

class Logout:
	def GET(self):
		session.kill()
		raise web.seeother('/')

class Home:
	def GET(self):
		if logged():
			if session.privilege == 0:
				render.home('', '', '', 'Please log in 0.')
			elif session.privilege == 1:
				render.home('', '', '', 'Please log in 1.')
			elif session.privilege == 2:
				render.home('', '', '', 'Please log in 2.')
		else:
			return render.home('', '', '', 'Please log in.')

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
		form.Textarea('comment',
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

def fetchOneAssoc(cursor) :
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