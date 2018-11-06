import flask
from flask import Flask, render_template
from flask import request, jsonify
from config import Config
from flask import url_for
from flask_wtf import Form
from wtforms import TextField
import sqlite3
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'development key'

# Global Scope
userdb = None
logindbfile = "login.db"

class ContactForm(Form):
    name = TextField("Test Name")

# Opens all db files and cursor attachments and returns them
def open_db(name):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    # Let rows returned be of dict/tuple type
    conn.row_factory = sqlite3.Row
    print ("Openned database %s as %r" % (name, conn))

    #create login file is not already exists
    if name == 'login.db':
        conn.execute('''CREATE TABLE IF NOT EXISTS userlogin (
	    user_id	INTEGER PRIMARY KEY AUTOINCREMENT,
	    username	TEXT NOT NULL,
	    password	TEXT NOT NULL,
	    userdbfilename	TEXT NOT NULL
        )
        ''')
    return conn , cur

# returns the size of table
def getTableSize(db, tablename):
    print('*************************************** print table ***************************************')
    return int(db.execute("SELECT COUNT(*) FROM " + tablename).fetchone()[0])

# Creates User login file if not exists
def createUser(na,pw,first,last,email):
    global userdb, logindbfile
    logindb, cur = open_db(logindbfile)

    # Check if username is available
    usercount = getTableSize(logindb, 'userlogin')    
    for i in range (usercount):
        if na == logindb.execute('''SELECT username FROM userlogin ''').fetchone()[i]:
            ################################################ HTML Rejections needed here?
            print('ERROR: Username taken')
            return
    usercount += 1

    userdb = 'user' + str(usercount) + '.db'
    # Create a new userX.db that copies from the base
    user_db, user_cur = open_db(userdb)

    user_db.execute('''CREATE TABLE IF NOT EXISTS eventitems (
	item_id	    INTEGER PRIMARY KEY AUTOINCREMENT,
	event_id	INTEGER NOT NULL,
	itemdescription 	TEXT NOT NULL,
	quantity	INTEGER NOT NULL DEFAULT 1,
	price	REAL NOT NULL DEFAULT 1.00,
	linkeduser_id	INTEGER NOT NULL
    )
    ''')
    #FOREIGN KEY(event_id) REFERENCES eventlist(eventlist_id),
	#FOREIGN KEY(linkeduser_id) REFERENCES linkedusers (linkeduser_id)
    #)
    #''')

    user_db.execute('''CREATE TABLE IF NOT EXISTS eventlist (
	eventlist_id	INTEGER PRIMARY KEY AUTOINCREMENT,
	eventname	TEXT NOT NULL,
	location	TEXT NOT NULL,
	date	TEXT NOT NULL,
	overallamount	REAL NOT NULL DEFAULT 0.00
    )
    ''')

    user_db.execute('''CREATE TABLE IF NOT EXISTS linkedusers (
	linkeduser_id	INTEGER NOT NULL,
	PRIMARY KEY(linkeduser_id)
    )
    ''')

    user_db.execute('''CREATE TABLE IF NOT EXISTS userinformation (
	firstname	TEXT NOT NULL,
	lastname	TEXT NOT NULL,
	email	TEXT NOT NULL,
	primaryuser_id	INTEGER NOT NULL
    )
    ''')

    cur.execute('INSERT INTO userlogin(username, password, userdbfilename) VALUES(?, ?, ?)', (na, pw, userdb))
    primaryuser_id = int((cur.execute('SELECT user_id from userlogin WHERE username=(?)',[na]).fetchone())[0])
    user_cur.execute('INSERT INTO userinformation(firstname, lastname, email, primaryuser_id) VALUES(?,?,?,?)', (first, last , email, primaryuser_id))
    logindb.commit()
    user_db.commit()
    logindb.close()
    user_db.close()
    print("New user created")

@app.route('/', methods=['GET', 'POST'])
def home():
    user = request.args.get('log_username')
    userpass = request.args.get('log_password')
    if (user != None) and (userpass != None):
        return (validateUser(user, userpass))
    form = ContactForm()
    return render_template('index.html', form = form)

def validateUser(na, pw):
    global userdb, logindbfile
    #dbuser = None
    #dbpass = None
    logindb , cur = open_db(logindbfile)
    count = getTableSize(cur, 'userlogin')
    for i in range ( 0, count):
        if str(na) == str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i]):
            print(type(str(na)), ' ', type(str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i])))
            if(str(pw) == str(cur.execute('''SELECT password FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i])): 
                userdb = (str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i]))
                return userOwes(na)
    logindb.close()
    print("no match")
    return render_template('index.html')

def userOwes(name):
    print('*************************************************** user owes *************************************')
    global userdb
    user_db, user_cur = open_db(userdb)
    count = getTableSize(user_cur, 'eventlist')
    results = []
    temp = ()
    for i in range (0, count):
        temp = user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i]
        # temp = (str(user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][2]), \
        #         str(user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][3]), \
        #         str(user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][1]))
        results.append(temp)
    user_db.close()
    return render_template("home.html", msg = results, count = count)

# Logs new user into app
@app.route('/action_page.php', methods=['GET', 'POST'])
def next_page():
    logindb, cur = open_db(logindbfile)
    form = ContactForm()
    # New signup with this form
    nuser = str(request.args.get('username'))
    npass = str(request.args.get('psw'))
    npsrep = str(request.args.get('psw-repeat'))
    first = str(request.args.get('firstname'))
    last = str(request.args.get('lastname'))
    email = str(request.args.get('email'))
    if(nuser != None):
        count = getTableSize(cur, 'userlogin')
        for i in range ( 0, count):
            if str(nuser) == str(cur.execute('''SELECT username FROM userlogin''').fetchone()[i]):
                print('Username not available')
                return  render_template('index.html', form = form) ############## Where do  we return to ?
        if(npass == npsrep):
            createUser(nuser, npass, first, last , email)
            return userOwes(nuser)  #render_template('result.html', msg = ("User %s created" % nuser))
    if(nuser != None):
        return (validateUser(nuser, npass))
    return render_template('index.html', form = form)

@app.route('/addevent/', methods =['POST'])
def add_event():
    global userdb
    user_db , user_cur = open_db(userdb)
    event = request.form['event']
    location = request.form['location']
    date = request.form['date']
    
    
    # if (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [user]).fetchall()) != "[]") and (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [owed]).fetchall()) != "[]"):
    #     owedid = int(cur.execute('''SELECT user_id FROM userlogin WHERE username=(?)''', [owed]).fetchone()[0])
    #     db = str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', [user]).fetchone()[0])
    #     usdb, uscur = open_db(db)
    #     user_db, user_cur = open_db(userdb)
    #     itemcount = getTableSize(uscur, 'items')
    #     itemcount += 1
    #     uscur.execute('''INSERT INTO items(item_id, description, quantity, price, linkeduser_id) VALUES(?,?,?,?,?)''', (itemcount, item, 1, price, owedid))
    #     usdb.commit()
    #     usdb.close()
    #     return render_template('result.html', msg = ("Event %s added to %s owing %s dollars to %s" % (item, user, price, owed)))
    # return ("One or more users in this addition was not found")

    user_cur.execute('INSERT INTO eventlist(eventname, location, date) VALUES(?,?,?)', (event, location, date))
    display_items()
    return ("Event Addied")
    










@app.route('/add/', methods =['POST'])
def add_item():
    global userdb, logindbfile
    user = request.form['user']
    item = request.form['item']
    price = request.form['price']
    owed = request.form['owed']
    logindb , cur = open_db(logindbfile)
    
    if (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [user]).fetchall()) != "[]") and (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [owed]).fetchall()) != "[]"):
        owedid = int(cur.execute('''SELECT user_id FROM userlogin WHERE username=(?)''', [owed]).fetchone()[0])
        db = str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', [user]).fetchone()[0])
        usdb, uscur = open_db(db)
        user_db, user_cur = open_db(userdb)
        itemcount = getTableSize(uscur, 'items')
        itemcount += 1
        uscur.execute('''INSERT INTO items(item_id, description, quantity, price, linkeduser_id) VALUES(?,?,?,?,?)''', (itemcount, item, 1, price, owedid))
        usdb.commit()
        usdb.close()
        return render_template('result.html', msg = ("Event %s added to %s owing %s dollars to %s" % (item, user, price, owed)))
    return ("One or more users in this addition was not found")


















    







@app.route('/eventitems/', methods=['GET', 'POST'])
def display_items():
    global userdb, logindbfile
    logindb, cur = open_db(logindbfile)
    user_db, user_cur = open_db(userdb)
    event_num = 0
    count = getTableSize(user_cur, 'eventlist')
    if request.method == 'POST':
        for i in range (count):
            if (request.form['button'].decode('utf-8')).split(' on ')[0] == (str(user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][2])):
                event_num = user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][1]
    count = getTableSize(user_cur, 'events')
    results = []
    associate_event = []
    for i in range (count):
        if event_num == user_cur.execute('''SELECT * FROM events''').fetchall()[i][0]:
            #associate_event.append(user_cur.execute('''SELECT * FROM events''').fetchall()[i])
            assoc_count = getTableSize(user_cur, 'eventsuserlist')
            for j in range (assoc_count):
                if event_num == user_cur.execute('''SELECT * FROM eventsuserlist''').fetchall()[j][2]:
                    associate_event.append(user_cur.execute('''SELECT * FROM eventsuserlist''').fetchall()[j][1])
                    print(associate_event)
            itemcount = getTableSize(user_cur, 'events')
            for i in range (itemcount):
                subitemcount = getTableSize(cur, 'userlogin')
                for k in range (subitemcount):
                    print(associate_event[1])
                    print(int(user_cur.execute('''SELECT * FROM items''').fetchall()[i][0]))
                    if str(cur.execute('''SELECT * FROM userlogin''').fetchall()[k][0]) == str(user_cur.execute('''SELECT * FROM items''').fetchall()[i][4]) and \
                        associate_event[1] == int(user_cur.execute('''SELECT * FROM items''').fetchall()[i][0]):
                        temp2 = (str(user_cur.execute('''SELECT * FROM items''').fetchall()[i][0]), \
                                str(user_cur.execute('''SELECT * FROM items''').fetchall()[i][1]), \
                                str(user_cur.execute('''SELECT * FROM items''').fetchall()[i][2]), \
                                str(user_cur.execute('''SELECT * FROM items''').fetchall()[i][3]), \
                                str(cur.execute('''SELECT * FROM userlogin''').fetchall()[k][1]))
                        break
                results.append(temp2)
    user_db.close()
    logindb.close()
    return render_template("event.html", msg2 = results, msg = associate_event)


@app.route('/remove/', methods =['POST'])
def remove_item():
    user = request.form['user']
    item = request.form['item']
    logindb, cur = open_db(logindbfile)
    if (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [user]).fetchall()) != "[]"):
        db = str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', [user]).fetchone()[0])
        usdb , uscur = open_db(db)
        if(str(uscur.execute('''SELECT item_id FROM items WHERE description=(?)''', [item]).fetchall()) != "[]"):
            itemid = int(uscur.execute('''SELECT item_id FROM items WHERE description=(?)''', [item]).fetchone()[0])
            uscur.execute('''DELETE FROM items WHERE item_id=(?)''', [itemid])
            usdb.commit()
            usdb.close()
            return render_template('result.html', msg = ("Event %s removed from %s" % (item, user)))
        usdb.close()
    return ("One or more users in this removal was not found")

@app.route('/additem.html', methods =['GET', 'POST'])
def add_page():
    form = ContactForm()
    return render_template('additem.html', form = form)

@app.route('/removeitem.html', methods =['GET', 'POST'])
def remove_page():
    form = ContactForm()
    return render_template('removeitem.html', form = form)

if __name__ == '__main__':
    app.run()










################################################  What's this for?
@app.route('/home', methods=['GET' , 'POST'])
def eventlist():
    event_id = request.args.get('button')

################################################ What's this for?
# endpoint to show all users
@app.route("/users", methods=["GET"])
def get_users():
    print('*************************************** get users *****************************************')
    global userdb, logindbfile
    logindb, cur = open_db(logindbfile)
    users = ()
    usercount = getTableSize(cur, 'userlogin')
    for i in range(0, usercount):
        users.append(str(cur.execute("SELECT * FROM userlogin").fetchall()[i][1]))
    logindb.close()
    return render_template('result.html', msg = str(users))