from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__, static_url_path='/static')

#config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MySQL
mysql = MySQL(app)

#index
@app.route('/')
def index():
	return render_template('index.html')

#home
@app.route('/home')
def about():
	return render_template('home.html')

#register form class
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords do not match')])
	confirm = PasswordField('Confirm Password')

#user register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(user_id, username, password, eventlist_id, userinformation_id, userlist_id) VALUES(%s, %s, %s, %s, %s, %s)", (user_id, username, password, eventlist_id, userinformation_id, userlist_id))

        mysql.connection.commit()
        cur.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    	#get form fields
    	username = request.form['username']
    	password_candidate = request.form['password']

    	#create cursor
    	cur = mysql.connection.cursor()

    	#get user by username
    	result = cur.execute("SELECT * FROM user WHERE username = %s", [username])

    	if result > 0:
    		#get stored hash
    		data = cur.fetchone()
    		password = data['password']

    		#compare passwords
    		if sha256_crypt.verify(password_candidate, password):
    			session['logged_in'] = True
    			session['username'] = username

    			flash('You are now logged in', 'success')
    			return redirect(url_for('dashboard'))
    		else:
    			error = 'Invalid login'
    			return render_template('login.html', error = error)

    		cur.close()

    	else:
    		error = 'Username not found'
    		return render_template('login.html', error = error)

    return render_template('login.html')

#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap


#logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))


#add customer
@app.route('/add_customer', methods=['Get','POST'])
@is_logged_in
def add_customer():
	form = CustomerForm(request.form)
	if request.method == 'POST' and form.validate():
		CustID = form.CustID.data
		Fname = form.Fname.data
	 	Lname= form.Lname.data
		phone = form.phone.data
		email = form.email.data

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO customers(CustID, Fname, Lname, phone, email) VALUES(%s, %s, %s, %s, %s)", (CustID, Fname, Lname, phone, email))

		mysql.connection.commit()
		cur.close()

		flash('Customer Added', 'success')
		return redirect(url_for('adding'))

	return render_template('add_customer.html', form=form)

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug = True)
