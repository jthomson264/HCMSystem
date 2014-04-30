import web
from model import HCMS_Model
from web import form
import random
import hashlib

#################################################################################
### Helper Functions
def logged():
	if session['loggedIn']==1:
		return True
	else:
		return False

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
	'/getRec', 'Get_Pat_Records',
	'/login', 'Login',
        '/register', 'Register'
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

setSessionData(False, 'Nick', 'patient')#debug

#################################################################################
### Define Forms
selDocForm = form.Form( form.Textbox("Please enter selected Doctor ID") )

#################################################################################
### Define classes
#################################################################################
class Index:
	def GET(self):
		if logged():
			return render.index()
		else:
			return render.login()
#####################################
class Select_Doctor:
	def GET(self):
		if logged():
			if session['role']=='patient':
				form_data = selDocForm()
				doc_data = model.get_all_doctors()
				return render.selDoc(form=form_data, doctors=doc_data)
			else:
				return render.permErr('patient', session['role'])
		else:
			return render.login()

	def POST(self): 
		form_data = selDocForm()
		if not form_data.validates(): 
			return render.selDoc(form=form_data, doctors=doc_data)
		else:
			return  render.selDocNotify(form_data['Please enter selected Doctor ID'].value)
#####################################
class Register:
	def GET(self):
		return render.register()
	def POST(self):
		i = web.input()
		salt = 'not random yet'
		myhash = hashlib.md5(i.passwd+salt).hexdigest()
		#i.username = 'James' #i.username
		#i.password = 'password12345' #i.password
		
		model.insert_Password(i.user,salt,myhash)
		return render.index()
		
		
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
			#session.logged_in = True
			#session.username = i.username
			session['loggedIn']=1
			raise web.seeother('/')   
		else: return render.incorrectPass()   
		# TODO : put login routine here
		return render.index()
		
#####################################
class Get_Doctors_Pats:
	def GET(self):
		if logged():
			if session['role']=='patient':
				# TODO: get doctor ID (dID) from the session(?) are we using sessions?
				pat_data = model.get_doctors_patients(session['user_id'])
			else:
				return render.patientlist(patients=pat_data)
		else:
			return render.login()

#####################################
class Get_Pat_Records:
	def GET(self):
		if logged():
			med_data = model.get_medical_records(session['user_id'])
			return render.medrecords(records=med_data)
		else:
			return render.login()
		
application = app.wsgifunc()

#################################################################################
### Main
if __name__=="__main__":
	app.run()
