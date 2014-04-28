import datetime

# This is a model - a class dealing with data representation of an object
# This example demonstrates usage of a web.py API
class HCMS_Model:
    def __init__(self, db):
        self._db = db

    # Create database tables
    def init_schema(self):
        # We're using a multi-line string to not worry about line breaks
        self._db.query('''		
				CREATE TABLE users (
					id INTEGER NOT NULL PRIMARY KEY,
					nickname VARCHAR(32) NOT NULL,
					date_created TEXT NOT NULL)		
			''')

    def create(self, nick):
        # Model is a good place to handle all logic related to the database
        # Such as creation times, serializing data, dealing with SQL injection
        now = str(datetime.datetime.now())
        return self._db.insert('users', nickname=nick, date_created=now)

    def get_all_doctors(self):
        return list(self._db.select('Doctor'))
		
    def get_all_patients(self):
        return list(self._db.select('Patient'))

	def link_patient_doctor(self, pID, dID):
		return self._db.insert('XRef_Pat_Doc', Patient_ID=pID, Doctor_ID=dID)
	
	def get_doctors_patients(self, dID):
		#TODO 
		#check XREF table for rows with doctor's ID, then join with patient table
		#output array of all patient data linked to doctor
		return
		
	def get_medical_data(self, pID):
		return list(self._db.select('Medical_Record', where='Patient_ID=$pID'))