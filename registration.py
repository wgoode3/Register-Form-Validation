from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime
import re
#complicated regex given for assignment
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#complicated regex from stack overflow
PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')
#regex that matches strings that resemble dates
DATE_REGEX = re.compile(r'([0-9]{2}[/][0-9]{2}[/][0-9]{4})')
app = Flask(__name__)

app.secret_key = "NCC-1701" #an enterprise grade secret key

@app.route('/')
def registration():
	return render_template('registration.html')

@app.route('/validation', methods=['POST'])
def validation():

	try:
		dob = request.form['dob']
		now = str(datetime.now())
		year = 1000*int(now[0])+100*int(now[1])+10*int(now[2])+int(now[3])
		month = 10*int(now[5])+int(now[6])
		day = 10*int(now[8])+int(now[9])
		#this previously crashed everything if the date wasn't enterred properly, too short, etc
		m, d, y = int(dob.split('/')[0]), int(dob.split('/')[1]), int(dob.split('/')[2])
	except ValueError, IndexError:
		pass

	if len(request.form['fname']) < 1:
		flash('First name cannot be blank!')
	elif len(request.form['lname']) < 1:
		flash('Last name cannot be blank!')
	elif len(request.form['email']) < 1:
		flash('Email cannot be blank!')
	elif not EMAIL_REGEX.match(request.form['email']):
		flash('Invalid Email Address!')
	elif len(dob) < 1:
		flash('Date of Birth cannot be blank!')
	elif not DATE_REGEX.match(request.form['dob']):
		flash('Invalid date! Must be in form MM/DD/YYYY!')
	#I can't be bothered to check each month has the right number of days
	elif m < 1 or m > 12 or d < 1 or d > 31:
		flash('Invalid date!')
	#no time travellers or Methuselahs allowed
	#smart babies allowed
	#check for year out of bounds
	elif y > year or y < (year-125):
		flash('Easy there time traveler!')
	#check for month out of bounds
	elif y == year and m > month:
		flash('Easy there time traveler!')
	#check for day out of bounds
	elif y == year and m == month and d > day:
		flash('Easy there time traveler!')
	elif not PASSWORD_REGEX.match(request.form['password']):
		flash('Password must be 8 characters or more! Containing capital and lowercase letters and a number. Currently no special characters...')
	elif not request.form['password'] == request.form['cpassword']:
		flash('Passwords must match!')
	else:
		flash('Success!')
	return redirect('/')

app.run(debug=True) 
