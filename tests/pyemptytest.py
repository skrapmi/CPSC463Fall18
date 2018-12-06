import unittest,  sqlite3, os, time, sys

# Global Scope
userdb = None
logindbfile = "../login.db"

def open_db(name):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    return conn , cur

# returns the size of table
def getTableSize(db, tablename):
    try:
        (db.execute("SELECT COUNT(*) FROM " + tablename).fetchall())[0][0]
    except sqlite3.OperationalError:
        print('Test Failed with database error')
        sys.exit(1)
    return (db.execute("SELECT COUNT(*) FROM " + tablename).fetchall())[0][0]

def validateUser(na, pw):
    global userdb, logindbfile
    logindb , cur = open_db(logindbfile)
    count = getTableSize(cur, 'userlogin')
    for i in range (count):
        try:
            if str(na) == str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i]):
                if(str(pw) == str(cur.execute('''SELECT password FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i])): 
                    userdb = ('../' + str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i]))              
                    return("Login Test Pass")
        except:
            return('Login Test Fail')
    return('Login Test Fail')

def Eventtest():
    global userdb
    user_db, user_cur = open_db(userdb)
    count = getTableSize(user_cur, 'eventlist')
    if count == 0:
        return('Event Test Passed - Event Removed')
    else:
        return('Event Test Failed - Items Exists')

validateUser('JohnDoe','password')
print('')
print('Test Section for Event Entry removed made by Selenium')
print(Eventtest())
print('')
