import web
from model import HCMS_Model
from web import form
import random

### Init our application
render = web.template.render('templates/')

### Register URLs
urls = (
    '/', 'Index',
    '/loginPat', 'Login_Pat',
    '/loginDoc', 'Login_Doc',
	'/selDoc', 'Select_Doctor',
	'/getPats', 'Get_Doctors_Pats',
	'/getRec', 'Get_Pat_Records',
	'/login', 'Login'
)

app = web.application(urls, globals())

### Open database
db = web.database(dbn='sqlite', db='HCMS_DB/HCMS_DB.sqlite')
model = HCMS_Model(db)

### Define Forms
selDocForm = form.Form( form.Textbox("Please enter selected Doctor ID") )

login = form.Form(
    form.Textbox('username'),
    form.Password('password'),
    form.Button('Login'),
)

### Define classes
class Index:
    def GET(self):
		return render.index()

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
			
## NOT SURE IF WE ARE DOING DUMMY LOGIN OR LOGIN/SESSIONS...
class Login_Pat:
    def GET(self):
		# TODO : runs when Login Patient is clicked
		form_data = login()
		return form_data.render()
		
## NOT SURE IF WE ARE DOING DUMMY LOGIN OR NOT...
class Login_Doc:
    def GET(self):
		# TODO : runs when Login Dcotor is clicked
        return web.seeother('/')

class Get_Doctors_Pats:
	def GET(self):
		# TODO: get doctor ID (dID) from the session(?) are we using sessions?
		pat_data = model.get_doctors_patients(d(dID)
		return render.patientlist(patients=pat_data)
		
class Get_Pat_Records:
	def GET(self):
		# TODO: get patient ID (pID) from the session(?) are we using sessions?
		med_data = model.get_medical_records(pID)
		return render.medrecords(records=med_data)

application = app.wsgifunc()

if __name__=="__main__":
    #model.init_schema()
    app.run()
