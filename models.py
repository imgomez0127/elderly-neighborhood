from settings import db

volunteerMeets_table = db.Table('volunteerMeets',
	db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteer.id'), primary_key=True),
    db.Column('volunteer_meets_id', db.Integer, db.ForeignKey('meets.id'), primary_key=True)
)
class User(db.Model):
	__tablename__= "user"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100),unique=True, nullable=False)
	password = db.Column(db.String(10000), unique = True, nullable= False)
	zipCode = db.Column(db.String(10), unique = False, nullable = False)
	typesPref = db.Column(db.String(100), nullable = True)
	phone_number = db.Column(db.Integer, unique = True, nullable = False)
	address = db.Column(db.String(100),nullable = False)
	__mapper_args__ = {
	'polymorphic_identity': 'user',
	}
class Elderly(User):
	__tablename__="elderly"
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	meets_elderly = db.relationship('Meets',uselist=True,back_populates="elderly")
	__mapper_args__ = { 'polymorphic_identity':'elderly'}
	def __str__(self):
		return username
	def __repr__(self):
		return "<Elderly: "+ self.username + ">"

class Volunteer(User):
	__tablename__="volunteer"
	id = db.Column(db.Integer, db.ForeignKey("user"),primary_key=True)
	volunteer_meets = db.relationship("Meets",secondary=volunteerMeets_table,back_populates="meet_volunteers")
	__mapper_args__ = {"polymorphic_identity":"volunteer"}
	def __str__(self):
		return username
	def __repr__(self):
		return "<Volunteer: "+ self.username + ">"

class Meets(db.Model):
	__tablename__  = "meets"
	id = db.Column(db.Integer, primary_key=True)
	meetup_name = db.Column(db.String(100),nullable = False)
	meet_volunteers = db.relationship("Volunteer",secondary=volunteerMeets_table,back_populates="volunteer_meets")
	elders_id = db.Column(db.Integer,db.ForeignKey("elderly.id"))
	elderly = db.relationship("Elderly",back_populates="meets_elderly")
	
	def __str__(self):
		return meetup_name
	def __repr__(self):
		return "<Meets: "+ self.meetup_name + ">"
