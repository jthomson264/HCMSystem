import sqlite3
def authenticate(userPass,SSN):
    salt = "1234567654321234565432 this is a salt 23961" 
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM hashes WHERE ssn = '%s'" % SSN)
    if hash(userPass + salt) == c.fetchone():
        return True
    else:
        return False
