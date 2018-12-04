import flask
from flask import Flask, render_template, request, redirect
from flask import request, jsonify
from config import Config
from flask import url_for
from flask_wtf import Form
from wtforms import TextField
from flask import Flask
import sqlite3
import logging, sys


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'development key'
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


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
    print ("Opened database %s as %r" % (name, conn))

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
    return (db.execute("SELECT COUNT(*) FROM " + tablename).fetchall())[0][0]

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
    return render_template("index.html", form = form)

def validateUser(na, pw):
    global userdb, logindbfile
    logindb , cur = open_db(logindbfile)
    count = getTableSize(cur, 'userlogin')
    for i in range (count):
        if str(na) == str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i]):
            if(str(pw) == str(cur.execute('''SELECT password FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i])): 
                userdb = (str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', (na,)).fetchone()[i]))
                return userOwes() 
    logindb.close()
    print("no match")
    return render_template('index.html')

def userOwes(): 
    print('----------------- user owes--------')
    global userdb
    user_db, user_cur = open_db(userdb)
    count = getTableSize(user_cur, 'eventlist')
    results = []
    temp = ()
    for i in range (0, count):
        temp = user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i]
        results.append(temp)
    user_db.commit()
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
            if str(nuser) == str(cur.execute('''SELECT username FROM userlogin''').fetchone())[i]:
                print('Username not available')
                return  render_template('index.html', form = form) ############## Where do  we return to ?
        if(npass == npsrep):
            createUser(nuser, npass, first, last , email)
            return userOwes()
    if(nuser != None):
        return (validateUser(nuser, npass))
    return render_template('index.html', form = form)

@app.route('/addevent/', methods =['GET','POST'])
def add_event():
    print('----------------- add_event--------')
    global userdb
    
    user_db , user_cur = open_db(userdb)
    event = str(request.args.get('event'))
    location = str(request.args.get('location'))
    date = str(request.args.get('date'))
    user_cur.execute('INSERT OR IGNORE INTO eventlist(eventname, location, date) VALUES(?,?,?)', (event, location, date))
    user_db.commit()
    user_db.close()
    msg = "Record successfully added"
    print('Event Added')
    return render_template("result.html", msg = msg)
   

@app.route("/forward/", methods=['GET'])
def move_forward():
    print('----------------- user owes--------')
    global userdb
    user_db, user_cur = open_db(userdb)
    count = getTableSize(user_cur, 'eventlist')
    results = []
    temp = ()
    for i in range (0, count):
        temp = user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i]
        results.append(temp)
    user_db.commit()
    user_db.close()
    return userOwes()


@app.route('/deletevent/', methods =['GET', 'POST'])
def delete_event():
    print('----------------- delete_event--------')
    
    user_db , user_cur = open_db(userdb)
    item = ()
    event = ()
    
    item = (request.form['currItem'])
    itemsId = user_cur.execute('SELECT item_id FROM eventitems WHERE itemdescription = ?', (item,)).fetchone()[0]
    eventId = user_cur.execute('SELECT event_id FROM eventitems WHERE itemdescription = ?', (item,)).fetchone()[0]    
    
    event_item_count = getTableSize(user_cur, 'eventitems')
    for i in range (event_item_count):
        ItemTotal = str('$'+ str(float("{0:.2f}".format(user_cur.execute("SELECT SUM(price) FROM eventitems").fetchone()[0]))))
    
    user_cur.execute('DELETE FROM eventitems WHERE item_id = ?',(itemsId,))
    user_db.commit()
    
    dbSize = user_cur.execute('SELECT event_id FROM eventitems WHERE event_id = ?',(eventId,)).fetchall()
    #eventItemTotal = str('$'+ str((user_cur.execute('SELECT SUM(price) FROM eventitems').fetchone()[0])))
     
    
    #if deleting last item, delete entire event
    if dbSize == []:
        user_cur.execute('DELETE FROM eventlist WHERE eventlist_id = ?', (eventId,))
	
    msg = "Record successfully deleted"
    print('Event Deleted')
    logging.debug(dbSize)
    logging.debug(item)
    logging.debug(itemsId)
    logging.debug(eventId)
    user_db.commit()
    user_db.close()  
    
    return render_template("result.html", msg = msg, msg3 = ItemTotal)
    
    
    
@app.route('/eventitems/', methods=['GET', 'POST'])
def display_items():
    print('----------------- display_items--------')
    global userdb, logindbfile
    logindb, cur = open_db(logindbfile)
    user_db, user_cur = open_db(userdb)
    event_num = 0
    event_count = getTableSize(user_cur, 'eventlist')
    if request.method == 'POST':
        for i in range (event_count):
            if (request.form['button']).split(' on ')[0] == (str(user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][1])):
                event_num = user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][0]
                event_loc = user_cur.execute('''SELECT * FROM eventlist''').fetchall()[i][2]
    
    associate_event = user_cur.execute('SELECT * FROM eventlist WHERE eventlist_id=(?)', (event_num,)).fetchone()
    
    display = ()
    displayitems = []
    ItemTotal = ()
    eventItemTotal = ()
    event = request.form['button']
    event = event.split()[0]
    
    
    event_item_count = getTableSize(user_cur, 'eventitems')
    for i in range (event_item_count):
        if event_num == user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][1]:
            linkeduser = user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][5]
            
            display = (user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][0], \
                                user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][1], \
                                str(user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][2]), \
                                user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][3], \
                                str('$'+ str(float("{0:.2f}".format(user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][4])))), \
                                user_cur.execute('''SELECT * FROM eventitems''').fetchall()[i][5], \
                                str(cur.execute('SELECT username FROM userlogin WHERE user_id=(?)', (linkeduser,)).fetchone()[0]))
	
	    
            ItemTotal = str('$'+ str(float("{0:.2f}".format(user_cur.execute("SELECT SUM(price) FROM eventitems").fetchone()[0]))))
            eventItemTotal = str('$'+ str(float("{0:.2f}".format(user_cur.execute('SELECT SUM(price) FROM eventitems WHERE event_id = ?', (associate_event[0],)).fetchone()[0]))))
            displayitems.append(display)
            
    
	    
    user_db.close()
    logindb.close()
    
    logging.debug(event)
    logging.debug(eventItemTotal)
 
    
    if ItemTotal == ():
        return render_template("event.html", msg2 = displayitems, msg = associate_event, msg3 = str('$' + "0.00"), msg4 = str('$' + "0.00"))
    else:
        return render_template("event.html", msg2 = displayitems, msg = associate_event, msg3 = ItemTotal, msg4 = eventItemTotal)
    
    

@app.route('/additem/', methods =['GET','POST'])
def add_item():
    print('----------------- add_item--------')
    global userdb, logindbfile
    logindb, cur = open_db(logindbfile)
    user_db, user_cur = open_db(userdb)
    item = str(request.args.get('itemname'))
    price = float("{0:.2f}".format(float(request.args.get('price'))))
    quantity = int(request.args.get('itemquantity'))
    eventname = str(request.args.get('submit'))
    #eventname = request.form['event']
    
    logging.debug(eventname)
    eventid = user_cur.execute('SELECT * FROM eventlist WHERE eventname=(?)', (eventname,)).fetchone()[0] #cant enter spaces in event name
    
    user_cur.execute('INSERT INTO eventitems(itemdescription, quantity, price, linkeduser_id, event_id) VALUES(?,?,?,?,?)', (item, quantity, price, 1, eventid))
    new_overall_total = (price) + user_cur.execute('SELECT overallamount FROM eventlist WHERE eventlist_id=(?)', (eventid,)).fetchone()[0]
    print(new_overall_total)
    print(type(new_overall_total))
    user_cur.execute('UPDATE eventlist set overallamount = ? WHERE eventname = ?', (new_overall_total,eventname))
    msg = "item successfully added"
    user_db.commit()
    user_db.close()
    logindb.close()
    return render_template("result.html", msg = msg)



if __name__ == '__main__':
    app.run()



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# Below are items I have not worked on!!!!!




@app.route('/remove/', methods =['POST'])
def remove_item():
    print('----------------- romove_itmes--------')
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
    print('----------------- add_page--------')
    form = ContactForm()
    return render_template('additem.html', form = form)

@app.route('/removeitem.html', methods =['GET', 'POST'])
def remove_page():
    print('----------------- remove_page--------')
    form = ContactForm()
    return render_template('removeitem.html', form = form)








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
    users = []
    usercount = getTableSize(cur, 'userlogin')
    for i in range(0, usercount):
        users.append(str(cur.execute("SELECT * FROM userlogin").fetchall()[i][1]))
    logindb.close()
    return render_template('result.html', msg = str(users))




