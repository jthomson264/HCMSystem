import web
from model import HCMS_Model
from web import form
import random
import hashlib
import base64
import uuid

#################################################################################
### Helper Functions
def logged():
	if session['loggedIn']==1:
		return True
	else:
		return False

def getRole():
	return session['role']
	
def getUser():
	return session['user_id']

def getSessionData():
	print '--'
	print session['loggedIn']
	print session['user_id']
	print session['role']
	print '--'
	return

def setSessionData(log, user, role):
	session['loggedIn'] = log
	session['user_id'] = user
	session['role'] = role
	return

#################################################################################
### Set HTML template folder
render = web.template.render('templates/')

#################################################################################
### Register URLs
urls = (
	'/', 'Index',
	'/selDoc', 'Select_Doctor',
	'/getPats', 'Get_Doctors_Pats',
	'/getRec', 'Get_Doctors_Pats_Records',
	'/login', 'Login',
	'/register', 'Register',
	'/logout', 'Logout'
)

#################################################################################
### Init our application
app = web.application(urls, globals())

#################################################################################
### Open database
db = web.database(dbn='sqlite', db='HCMS_DB/HCMS_DB.sqlite')
model = HCMS_Model(db)

#################################################################################
### Initialize the session
# sessions wasnt working so using a regular dictionary to store data...
session = {'loggedIn': False, 'user_id': 'None', 'role': 'None'}
#store = web.session.DiskStore('sessions')
# if web.config.get('_session') is None:
	# session = web.session.Session(app, store, initializer={'loggedIn': False, 'user_id': 'None', 'role': 'None'})
	# web.config._session = session
	# print 'yes'#debug
# else:
	# session = web.config._session
	# print 'no'#debug

#################################################################################
### Define Forms
selDocForm = form.Form( form.Textbox("Please enter selected Doctor License ID") )

#################################################################################
### Define classes
#################################################################################
class Index:
	def GET(self):
		if logged():
			session['role']='doctor' # DEBUG
			return render.index()
		else:
			return render.login()
#####################################
### Use Case: Patient wants to view his list of doctors and select one to add 
class Select_Doctor:
	def GET(self):
		if logged():
			if getRole() == 'patient':
				form_data = selDocForm()
				doc_data = model.get_all_doctors()
				return render.selDoc(form=form_data, doctors=doc_data)
			else:
				return render.permErr('Patient', getRole())
		else:
			return render.login()

	def POST(self): 
		form_data = selDocForm()
		if not form_data.validates(): # required to work but should never go here due to lack of validation code
			return render.selDoc(form=form_data, doctors=doc_data)
		else:
			return  render.selDocNotify(form_data['Please enter selected Doctor License ID'].value)
#####################################
class Register:
	def GET(self):
		return render.register()
	def POST(self):
		i = web.input()
		salt = 'not random yet'
		salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
		myhash = hashlib.md5(i.passwd+salt).hexdigest()
		#i.username = 'James' #i.username
		#i.password = 'password12345' #i.password
		
		model.insert_Password(i.user,salt,myhash)
		setSessionData(True, i.user, 'None')
		return render.index()
#####################################	
		
class Login:
	def GET(self):
		return render.login()
		
	def POST(self):
		i = web.input()
		pID = i.user
		print pID
		print i
		passData = model.get_password(pID)
		if passData:
			x='doingnothing'
		else: return render.noUser()
		passData = passData[0]
		salt = passData.Salt
		
		pwdhash = hashlib.md5(i.passwd+salt).hexdigest()
		
		
		
		# check = authdb.execute('select * from Hashes where SSN=? and Hash=?', (i.username, pwdhash))
		check = (pwdhash == passData.Hash)
		if check: 
			setSessionData(True, i.user, 'None') # TODO : NEED TO GET ROLE SOMEHOW
			raise web.seeother('/')   
		else: return render.incorrectPass()   
		# TODO : put login routine here
		return render.index()
#####################################
class Logout:
	def GET(self):
		setSessionData(False, 'None', 'None')
		return render.login()
#####################################
### Use Case: Doctor wants to view his list of patients 
class Get_Doctors_Pats: 
	def GET(self):
		if logged():
			if getRole() == 'doctor':			
				pat_data = model.get_doctors_patients(getUser())
				return render.patientlist(pat_data)
			else:
				return render.permErr('Doctor', getRole())
		else:
			return render.login()

#####################################
### Use Case: Doctor wants to view his patient's medical records
class Get_Doctors_Pats_Records:
	def GET(self):
		if logged():
			if getRole() == 'doctor':
				med_data = model.get_pat_medical_records(getUser())
				return render.medrecords(records=med_data)
			else:
				return render.PermErr('Doctor', getRole())
		else:
			return render.login()

#####################################
### Use Case: Patient wants to view his own medical records
class Get_My_Pat_Records:
		def GET(self):
			# TODO
			return

#################################################################################
### idk what this does I got it from some example code - if it aint broke dont fix it!
application = app.wsgifunc()

#################################################################################
### Main
if __name__=="__main__":
	app.run()
