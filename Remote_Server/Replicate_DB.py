#This Class Replicates HCMS Database


import sqlite3

#Replicate_Database(curs);

def Replicate_Database():
    db_name = "HCMS_DB.sqlite"
    backup_db_name = "HCMS_DB_backup.sqlite"
    tab1 = "Admin"
    tab2 = "Doctor"
    tab3 = "Hashes"
    tab4 = "Medical_Facility"
    tab5 = "Medical_Record"
    tab6 = "Patient"
    tab7 = "Prescription"
    tab8 = "Ticket"
    tab9 = "XRef_Pat_Doc"
    conn = sqlite3.connect('HCMS_DB_backup.sqlite')
    curs = conn.cursor()
    print "Replicating from database %s to database %s" % (db_name,backup_db_name)
    curs.execute("ATTACH '%s' AS parentdb;" %db_name)          
    curs.execute("insert into %s select * from parentdb.%s;" %(tab1,tab1))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab2,tab2))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab3,tab3))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab4,tab4))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab5,tab5))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab6,tab6))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab7,tab7))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab8,tab8))
    curs.execute("insert into %s select * from parentdb.%s;" %(tab9,tab9))
    curs.execute("DETACH parentdb;")
            
            
         

         
