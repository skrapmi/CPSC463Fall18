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

class ContactForm(Form):
    name = TextField("Test Name")

def open_db(name):
    conn = sqlite3.connect(name)
    # Let rows returned be of dict/tuple type
    conn.row_factory = sqlite3.Row
    print "Openned database %s as %r" % (name, conn)
    return conn


def copyTable(src, dest, db):
    #selection = src.execute('SELECT * FROM %s' % table)
    src.execute("ATTACH DATABASE '%s' AS destin" % dest)
    src.execute("INSERT INTO destin.user SELECT * FROM main.user;")
    db.commit()


def updateCount(userlist):
    count = 0
    for i in userlist:
        count += 1
        print(count)
    return count

def createUser(na,pw):
    log = open_db('login.db')
    users = log.execute("SELECT * FROM userlogin")
    usercount = 0
    cur = log.cursor()
    usercount = updateCount(users)
    usercount += 1
    # Create a new userX.db that copies from the base
    nuser = open_db('user' + str(usercount) + '.db')
    nuser.execute('''CREATE TABLE "eventlist" (
        `eventlist_id` INTEGER NOT NULL, 
        `events_id` INTEGER NOT NULL, 
        `eventname` TEXT NOT NULL, 
        `date` DATE NOT NULL, PRIMARY KEY(`eventlist_id`) 
        )
        ''')
    nuser.execute('''CREATE TABLE "events" (
    `event_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    `location` TEXT, `overallamount` DECIMAL NOT NULL DEFAULT 0 
    )
    ''')
    nuser.execute('''CREATE TABLE "eventsuserlist" (
    `eventuserlist_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    `useritem_id` INTEGER NOT NULL, 
    `associate_event_id` INTEGER NOT NULL, 
    `Overall_money` DECIMAL NOT NULL DEFAULT 0 
    )
    ''')
    nuser.execute('''CREATE TABLE "items" (
    `item_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    `description` TEXT NOT NULL, `quantity` INTEGER NOT NULL DEFAULT 1, 
    `price` DECIMAL NOT NULL DEFAULT 1, 
    `linkeduser_id` INTEGER NOT NULL 
    )
    ''')
    nuser.execute('''CREATE TABLE "linked" (
    `linkeduserlist_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    `linkeduser_id` INTEGER NOT NULL 
    )
    ''')
    nuser.execute('''CREATE TABLE user (
    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL, 
    password TEXT NOT NULL, 
    eventlist_id INTEGER NOT NULL, 
    userinformation_id INTEGER NOT NULL, 
    userlist_id INTEGER NOT NULL 
    )
    ''')
    nuser.execute('''CREATE TABLE userinformation ( 
    userinformation_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    firstname TEXT NOT NULL, 
    lastname TEXT NOT NULL, 
    email TEXT NOT NULL, 
    contactphonenumber TEXT NOT NULL, 
    primaryuser_id INTEGER NOT NULL DEFAULT 0
    )
    ''')
    ndbname = ('user' + str(usercount) + '.db')
    # Find the highest userID
    cur.execute('''SELECT user_id from userlogin ORDER BY user_id DESC LIMIT 1''')
    # increment it by 1 and use it as the userID for the new user
    newid = int(cur.fetchone()[0]) + 1
    cur.execute('''INSERT INTO userlogin(user_id, username, password, userdbfilename) VALUES(?, ?, ?, ?);''', (newid, na, pw, ndbname))
    log.commit()
    log.close()
    print("New user created")

def userOwes(name):
    log = open_db('login.db')
    cur = log.cursor()
    db = str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', [name]).fetchone()[0])
    usdb = open_db(db)
    uscur = usdb.cursor()
    count = int(uscur.execute('''SELECT COUNT(*) FROM items''').fetchone()[0])
    results = ""
    for i in range (0, count):
        results += str(uscur.execute('''SELECT * FROM items''').fetchall()[i][1])
        results += " $"
        results += str(uscur.execute('''SELECT * FROM items''').fetchall()[i][3])
        results += "\n"
    usdb.close()
    log.close()
    print (results)
    return render_template("result.html", msg = results)
    
def validateUser(na, pw):
    match = False
    dbpass = None
    log = open_db('login.db')
    cur = log.cursor()
    if (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [na]).fetchall()) != "[]"):
        dbuser = (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [na]).fetchone()[0]))
        dbpass = (str(cur.execute('''SELECT password FROM userlogin WHERE username=(?)''', [na]).fetchone()[0]))
    if(pw == dbpass):
        match = True
    if match == True:
        return userOwes(na)
    log.close()
    print(match)
    return render_template('result.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    user = request.args.get('username')
    userpass = request.args.get('password')
    if (user != None) and (userpass != None):
        validateUser(user,userpass)
        return (validateUser(user, userpass))
    form = ContactForm()
    return render_template('index.html', form = form)

# endpoint to show all users
@app.route("/users", methods=["GET"])
def get_users():
    log = open_db('login.db')
    cur = log.cursor()
    users = ""
    usercount = int(cur.execute('''SELECT count(*) FROM userlogin''').fetchone()[0])
    for i in range(0, usercount):
        users += (str(cur.execute("SELECT * FROM userlogin").fetchall()[i][1]))
        users += '   '
    log.close()
    return render_template('result.html', msg = str(users))


@app.route('/action_page.php', methods=['GET', 'POST'])
def next_page():
    form = ContactForm()
    email = request.args.get('email')
    npass = request.args.get('psw')
    npsrep = request.args.get('psw-repeat')
    if(email != None):
        if(npass == npsrep):
            createUser(email, npass)
            return render_template('result.html', msg = ("User %s created" % email))
    user = request.args.get('username')
    userpass = request.args.get('password')
    if(user != None):
        validateUser(user, userpass)
        return (validateUser(user, userpass))
    return render_template('index.html', form = form)

@app.route('/add/', methods =['POST'])
def add_item():
    user = request.form['user']
    item = request.form['item']
    price = request.form['price']
    owed = request.form['owed']
    log = open_db('login.db')
    cur = log.cursor()
    if (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [user]).fetchall()) != "[]") and (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [owed]).fetchall()) != "[]"):
        owedid = int(cur.execute('''SELECT user_id FROM userlogin WHERE username=(?)''', [owed]).fetchone()[0])
        db = str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', [user]).fetchone()[0])
        usdb = open_db(db)
        uscur = usdb.cursor()
        itemcount = int(uscur.execute('''SELECT COUNT(*) FROM items''').fetchone()[0])
        itemcount += 1
        uscur.execute('''INSERT INTO items(item_id, description, quantity, price, linkeduser_id) VALUES(?,?,?,?,?)''', (itemcount, item, 1, price, owedid))
        usdb.commit()
        usdb.close()
        return render_template('result.html', msg = ("Event %s added to %s owing %s dollars to %s" % (item, user, price, owed)))
    return ("One or more users in this addition was not found")

@app.route('/remove/', methods =['POST'])
def remove_item():
    user = request.form['user']
    item = request.form['item']
    log = open_db('login.db')
    cur = log.cursor()
    if (str(cur.execute('''SELECT username FROM userlogin WHERE username=(?)''', [user]).fetchall()) != "[]"):
        db = str(cur.execute('''SELECT userdbfilename FROM userlogin WHERE username=(?)''', [user]).fetchone()[0])
        usdb = open_db(db)
        uscur = usdb.cursor()
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

app.run()
