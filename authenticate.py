import sqlite3
def authenticate(userPass,SSN):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM hashes WHERE ssn = '%s'" % SSN)
    if hash(userPass) == c.fetchone():
        return True
    else:
        return False
