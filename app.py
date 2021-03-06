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
	if session2.loggedIn == True:#if session['loggedIn']==1:
        
		return True
	else:
		return False

def getRole():
	#print session['role']
	#return session['role']
        return session2.role
	
def getUser():
	return session2.user_id#session['user_id']

def getSessionData():
	print '--'
	print session2.loggedIn #session['loggedIn']
	print session2.useer_id #session['user_id']
	print session2.role #session['role']
	print '--'
	return

def setSessionData(log, user, role):
	#session['loggedIn'] = log
	session2.loggedIn = log
	#session['user_id'] = user
	session2.user_id = user
	#session['role'] = role
	session2.role = role
	return

#################################################################################
### Set HTML template folder
render = web.template.render('templates/', base='layoutlogged')
render_plain = web.template.render('templates/', base='layoutNotLogged')
#################################################################################
### Register URLs
urls = (
	'/', 'Index',
	'/selDoc', 'Select_Doctor',
	'/adminSelDoc', 'Get_Admins_Doc_Records',
	'/adminSelPat', 'Admin_Sel_Pat',
	'/addMedRec', 'Add_Medical_Record',
	'/getPats', 'Get_Doctors_Pats',
	'/getRec', 'Get_Doctors_Pats_Records',
	'/getMyRec', 'Get_My_Pat_Records',
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
#session = {'loggedIn': False, 'user_id': 'None', 'role': 'None'}
store = web.session.DiskStore('sessions')
if web.config.get('_session') is None:
	 session2 = web.session.Session(app, store, initializer={'loggedIn': False, 'user_id': 'None', 'role': 'None'})
	 web.config._session = session2
	 
	 print 'yes'#debug
else:
	 session2 = web.config._session
	 print 'no'#debug

#################################################################################
### Define Forms
selDocForm = form.Form( form.Textbox("Please enter selected Doctor License ID") )

#################################################################################
### Define classes
#################################################################################
class Index:
	def GET(self):
		print session2.loggedIn
		print session2.user_id
		if logged():
			# DEBUG ONLY PLEASE REMOVE FOR PRODUCTION
			return render.index(role=getRole())
		else:
			return render_plain.login()
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
			return render_plain.login()

	def POST(self):
		i = web.input()
		
		# if not form_data.validates(): # required to work but should never go here due to lack of validation code
			# return render.selDoc(form=form_data, doctors=doc_data)
		# else:
		model.link_patient_doctor(getUser(), i.Doctor_Lic_No)
		return  render.selDocNotify(i.Doctor_Lic_No)
#####################################
class Register:
	def GET(self):
		return render_plain.register()
	def POST(self):
		i = web.input()
		salt = 'not random yet'
		salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
		myhash = hashlib.md5(i.passwd+salt).hexdigest()
		#i.username = 'James' #i.username
		#i.password = 'password12345' #i.password
		
		model.insert_Password(i.user,salt,myhash,i.role)
		setSessionData(True, i.user, i.role)
		return render.index(role=getRole())
#####################################	
		
class Login:
	def GET(self):
		return render_plain.login()
		
	def POST(self):
		print session2.loggedIn
		
		
		i = web.input()
		pID = i.user
		passData = model.get_password(pID)
		if passData:
			x='doingnothing'
		else: return render_plain.noUser()
		passData = passData[0]
		salt = passData.Salt
		
		pwdhash = hashlib.md5(i.passwd+salt).hexdigest()
		
	
		
		# check = authdb.execute('select * from Hashes where SSN=? and Hash=?', (i.username, pwdhash))
		check = (pwdhash == passData.Hash)
		if check: 
			#session2.loggedIn = True
			print session2.user_id
			#session2.user_id = i.user
			
			setSessionData(True, i.user, passData.Role) # TODO : NEED TO GET ROLE SOMEHOW
			print session2.user_id
			raise web.seeother('/')   
		else: return render_plain.incorrectPass()   
		# TODO : put login routine here
		return render.index(role=getRole())
#####################################
class Logout:
	def GET(self):
		setSessionData(False, 'None', 'None')
		return render_plain.login()
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
			return render_plain.login()

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
			return render_plain.login()

#####################################
### Use Case: Patient wants to view his own medical records
class Get_My_Pat_Records:
	def GET(self):
		# TODO
		if logged():
			if getRole() == 'patient':
				med_data = model.get_my_medical_records(getUser())
				return render.medrecords(records=med_data)
			else:
				return render.PermErr('Doctor', getRole())
		else:
			return render_plain.login()
				
#####################################
### Use Case: Admin chooses their docs, then chooses their patient, then uploads a patient record
class Get_Admins_Doc_Records:
	def GET(self):
		if logged():
			if getRole() == 'admin':
				doc_data = model.get_admins_doctors(getUser())
				return render.adminSelDoc(doctors=doc_data)
			else:
				return render.PermErr('admin', getRole())
		else:
			return render_plain.login()
	
	def POST(self):
		i = web.input()
		pat_data = model.get_doctors_pats_by_lic_num(i.Doctor_Lic_No)
		return  render.adminSelPat(pat_data)

class Admin_Sel_Pat:
	def GET(self):
		# NONE - IF WE GO HERE THERE WAS AN ERROR
		return 	render.index(role=getRole())
		
	def POST(self):
		i = web.input()
		return render.addMedicalRecord(i.Patient_SSN)

class Add_Medical_Record:
	def GET(self):
		# NONE - IF WE GO HERE THERE WAS AN ERROR
		return
		
	def POST(self):
		i = web.input()
		model.add_med_rec(i.Patient_SSN, i.rec, i.note)
		return render.index(role=getRole())
			
#################################################################################
### idk what this does I got it from some example code - if it aint broke dont fix it!
application = app.wsgifunc()

#################################################################################
### Main
if __name__=="__main__":
	app.run()
