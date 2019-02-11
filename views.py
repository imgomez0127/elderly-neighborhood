from flask import make_response, jsonify, request, abort,url_for,session,redirect
from settings import app, db, bcrypt
from models import User,Elderly,Volunteer, Meets, volunteerMeets_table 

def create_elder(userN,passW,zip,types,phoneN,address_):
	try:
		user = Elderly(username=userN,password=passW,zipCode=zip,phone_number=phoneN,typesPref=types,address=address_)
		db.session.add(user)
		db.session.commit()
		db.session.remove()
		return {"Success":"Signup was Successful"}
	except:
		return {"Failure": "Signup Failed"}

def create_volunteer(userN,passW,zip,types,phoneN,address_):
	try:
		user = Volunteer(username=userN,password=passW,zipCode=zip,phone_number=phoneN,typesPref=types,address=address_)
		db.session.add(user)
		db.session.commit()
		db.session.remove()
		return {"Success":"Signup was Successful"}
	except:
		return {"Failure": "Signup Failed"}

@app.route("/signup/elder", methods = ['POST'])
def signup_elder():
	username = request.json.get("Username")
	password = bcrypt.get_password_hash(request.json.get("Password")).decode('utf-8')
	zipCode = request.json.get("zipCode")
	typesPref = request.json.get("typesPref")
	phone_number = int(request.json.get("phone_number"))
	address = request.json.get("address")
	return jsonify(create_elder(username,password,zipCode,typesPref,phone_number,address))

@app.route("/signup/volunteer", methods = ['POST'])
def signup_volunteer():
	username = request.json.get("Username")
	password = request.json.get("Password")
	zipCode = request.json.get("zipCode")
	typesPref = request.json.get("typesPref")
	phone_number = request.json.get("phone_number")
	address = request.json.get("address")
	return jsonify(create_volunteer(username,password,zipCode,typesPref,phone_number,address))

@app.route('/login/elder',methods=["POST"])
def login_elder():
	session["username"] = request.form['Username'] 
	session["password"] = request.form['Password']
	session["User Type"] = "Elder"
	return 	jsonify({"Success": "Elder login was successful"})

@app.route('/login/volunteer',methods=["POST"])
def login_volunteer():
	session["username"] = request.form['Username'] 
	session["password"] = request.form['Password']
	session["User Type"] = "Volunteer"
	return 	jsonify({"Success": "Volunteer login was successful"})

@app.route('/logout')
def logout():
	session.pop('username',None)
	session.pop('password',None)
	session.pop('User Type',None)
	return jsonify({"Success":"Logout was successful"})

@app.route('/get/elder/info',methods = ["GET"])
def get_elder_info():
	elder = Elderly.query.filter_by(username=session["Username"]).first()
	if(elder == None):
		return jsonify({"Not Found": "Elder Not Found"})
	username = elder.username
	password = elder.password
	zipCode = elder.zipCode
	typesPref = elder.typesPref
	phone_number = elder.typesPref
	address = elder.address
	meetings = elder.meets_elderly
	meeting_id = [meeting.id for meeting in meetings]
	elder_json = {
	'Username': username,
	'Password': password,
	'ZipCode' : zipCode,
	'TypesPref' : typesPref,
	'Phone_number' : phone_number,
	'Address': address,
	'Meetings Id': meeting_id
	}
	db.session.remove()
	return jsonify(elder_json)

@app.route('/get/meetings/<int:meeting_id>', methods = ["GET"])
def get_meetings(meeting_id):
	meeting = Meets.query.filter_by(id=meeting_id).first()
	meetup_name = meeting.meetup_name
	meetup_volunteers = [volunteer.username for volunteer in meeting.meet_volunteers]
	meetup_id = meeting.id
	meetup_types = meeting.elderly.typesPref
	meetup_elder = meeting.elderly.username
	meetup_address = meeting.elderly.address
	meetup_zip = meeting.elderly.zipCode
	meetup_json = {
	"Meetup Name":meetup_name,
	"Meetup Volunteers":meetup_volunteers,
	"Meetup Id":meetup_id,
	"Meetup Pref": meetup_types,
	"Meetup Elder": meetup_elder,
	"Meetup Address": meetup_address,
	"Meetup Zip": meetup_zip
	} 
	db.session.remove()
	return jsonify(meetup_json)

@app.route('/get/volunteer/info',methods = ["GET"])
def get_volunteer_info():
	volunteer = Volunteer.query.filter_by(username==session["Username"]).first()
	if(volunteer == None):
		return jsonify({"Not Found": "Volunteer Not Found"})
	username = volunteer.username
	password = volunteer.password
	zipCode = volunteer.zipCode
	typesPref = volunteer.typesPref
	phone_number = volunteer.typesPref
	address = volunteer.address
	meetings = volunteer.meets_elderly
	volunteer_json = {
	'Username': username,
	'Password': password,
	'ZipCode' : zipCode,
	'TypesPref' : typesPref,
	'Phone_number' : phone_number,
	'Address': address,
	'Meetings': meetings
	}
	db.session.remove()
	return jsonify(volunteer_json)

@app.route('/add/volunteer/<int:meeting_id>',methods=["POST"])
def add_volunteer(meeting_id):
	meeting = Meets.query.filter_by(id=meeting_id).first()
	meeting.meet_volunteers.append(Volunteer.query.filter_by(username=session["Username"]))
	db.session.commit()
	db.session.remove()
	return jsonify({"Success":"Application succesfully sent"})

@app.route('/close/meeting/<int:meeting_id>', methods=["POST"])
def close_meeting(meeting_id):
	meeting = Meets.query.filter_by(id=meeting_id).first()
	db.session.delete(meeting)
	db.session.commit()
	db.session.remove()