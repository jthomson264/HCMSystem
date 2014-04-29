import web
from model import HCMS_Model
from web import form
import random

### Init our application
render = web.template.render('templates/')

### Register URLs
urls = (
    '/', 'Index',
	'/selDoc', 'Select_Doctor',
	'/getPats', 'Get_Doctors_Pats',
	'/getRec', 'Get_Pat_Records',
	'/login', 'Login'
)

app = web.application(urls, globals())

### Open database
db = web.database(dbn='sqlite', db='HCMS_DB/HCMS_DB.sqlite')
model = HCMS_Model(db)

### Initialize the session
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'loggedIn': 0, 'SSN': 0})
    web.config._session = session
else:
    session = web.config._session

### Define Forms
selDocForm = form.Form( form.Textbox("Please enter selected Doctor ID") )

#################################################################################
### Define classes
class Index:
    def GET(self):
		if logged():
			return render.index()
		else:
			return render.login()

class Select_Doctor:
	def GET(self):
		form_data = selDocForm()
		doc_data = model.get_all_doctors()
		return render.selDoc(form=form_data, doctors=doc_data)

	def POST(self): 
		form_data = selDocForm()
		if not form_data.validates(): 
			return render.selDoc(form=form_data, doctors=doc_data)
		else:
			return "You have given access rights to doctor # %s to view your profile" % (form_data['Please enter selected Doctor ID'].value)

class Login:
	def GET(self):
		return render.login()
		
	def POST(self):
		# TODO : put login routine here
		return render.index()

class Get_Doctors_Pats:
	def GET(self):
		# TODO: get doctor ID (dID) from the session(?) are we using sessions?
		pat_data = model.get_doctors_patients(dID)
		return render.patientlist(patients=pat_data)

class Get_Pat_Records:
	def GET(self):
		if logged():
			med_data = model.get_medical_records(session.SSN)
			return render.medrecords(records=med_data)
		else:
			return render.login()
		
#################################################################################3
### Helper Functions
def logged():
    if session.loggedIn==1:
        return True
    else:
        return False	
		
application = app.wsgifunc()

#################################################################################
### Main
if __name__=="__main__":
    #model.init_schema()
    app.run()