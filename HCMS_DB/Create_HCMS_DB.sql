
CREATE TABLE "Hashes" ("User_ID" TEXT PRIMARY KEY, "Hash" TEXT, "Salt" TEXT)

CREATE TABLE "Admin" ("Admin_UserID" TEXT REFERENCES "Hashes" ("User_ID"), "Admin_Name" TEXT, "Admin_Address" TEXT, "Admin_Phone" TEXT, "Facility_ID" INTEGER REFERENCES "Medical_Facility" ("Facility_ID"), "SSN" INTEGER, "Admin_ID" INTEGER PRIMARY KEY)

CREATE TABLE "Doctor" ("Doctor_UserID" TEXT REFERENCES "Hashes" ("User_ID"), "Doctor_Name" TEXT, "Doctor_Address" TEXT, "Doctor_Phone" TEXT, "Admin_ID" TEXT REFERENCES "Admin" ("Admin_UserID"), "Doctor_Lic_No" INTEGER PRIMARY KEY, "Specialization" TEXT, "SSN" INTEGER)

CREATE TABLE "Patient" ("Patient_UserID" TEXT REFERENCES "Hashes" ("User_ID"), "Patient_Name" TEXT, "Patient_DOB" DATE, "Patient_Address" TEXT, "Patient_Phone" TEXT, "Emergency_Contact" TEXT, "Sex" TEXT, "SSN" INTEGER PRIMARY KEY, "Insurance_Type" TEXT, "Age" INTEGER, "Medical_Condition" TEXT)

CREATE TABLE "Medical_Record" ("Record_ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Patient_ID" TEXT REFERENCES "Patient" ("Patient_UserID"), "Patient_Record" TEXT, "Date_Created" DATE, "Last_Updated_By_UserID" TEXT REFERENCES "Admin" ("Admin_UserID"), "Last_Updated_Date" DATE, "Doctor's Note" TEXT)

CREATE TABLE "Medical_Facility" ("Facility_ID" INTEGER PRIMARY KEY, "Facility_Name" TEXT, "Facility_Address" TEXT, "Facility_Phone" TEXT)

CREATE TABLE "Prescription" ("Prescription_ID" INTEGER PRIMARY KEY, "Patient_ID" TEXT REFERENCES "Patient" ("Patient_UserID"), "Doctor_ID" TEXT REFERENCES "Doctor" ("Doctor_UserID"), "Drug_Name" TEXT, "Dose_Details" TEXT)

CREATE TABLE "Ticket" ("Ticket_ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Patient_ID" TEXT REFERENCES "Patient" ("Patient_ID"), "Admin_ID" TEXT REFERENCES "Admin" ("Admin_UserID"), "Record_ID" INTEGER REFERENCES "Medical_Record" ("Record_ID"), "Message" TEXT, "Status" TEXT, "Date" DATE)

CREATE TABLE "XRef_Pat_Doc" ("Patient_SSN" INTEGER REFERENCES "Patient" ("Patient_UserID"), "Doctor_Lic_No" INTEGER REFERENCES "Doctor" ("Doctor_UserID"))