def makeNewUser(SSN, password):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM hashes WHERE ssn = '%s'" % SSN)
    if c.fetchone():
        return False
    else:
        c.execute("
