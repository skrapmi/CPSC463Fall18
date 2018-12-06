#from app import createUser as testnewuser
import unittest,  sqlite3, os, time, sys
#from selenium import webdriver

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

def Eventtest(ename, eitem, edate):
    global userdb
    user_db, user_cur = open_db(userdb)
    count = getTableSize(user_cur, 'eventlist')
    results = []
    temp = ()
    for i in range (0, count):
        try:
            temp = user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i]
        except sqlite3.Error as e:
            return('Event Test Failed - No Valid Database')
    if temp[1] == ename and temp[2] == eitem and temp[3] == edate:
        user_db.close()
        return('Event Test Pass')
    else:
        user_db.close()
        return('Event Test Fail')

def Itemtest(iname, iqty, iamount):
    global userdb
    user_db, user_cur = open_db(userdb)
    count = getTableSize(user_cur, 'eventitems')
    results = []
    temp = ()
    for i in range (0, count):
        try:
            temp = user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i]
        except:
            return('Event Test Failed - No Valid Database')
    if temp[2] ==iname and temp[3] == iqty and temp[4] == iamount:
        user_db.close()
        return('Event Test Pass')
    else:
        user_db.close()
        return('Event Test Fail')


print('Test Section for Username/Password Entry made by Selenium')
print('')
print(validateUser('JohnDoe','password'))
print('Testing for Invalid user not in database: ')
print(validateUser('JohDoe','password'))
print('Testing for Valid user incorrect password in database: ')
print(validateUser('JohnDoe','pasword'))

time.sleep(5)
print('')
print('Test Section for Event Entry made by Selenium')
print(Eventtest('Buying_Books_with_Jane','CSUF_Bookstore','12/01/2018')+ ' using the data of Buying_Books_with_Jane CSUF_Bookstore 12/01/2018')

time.sleep(5)
print('')
print('Test Section for Item Entry made by Selenium')
print(Itemtest('Jane\'s_Bio_Book',1,250.55)+ ' using the data of Jane\'s_Bio_Book 1 250.55')
print('')