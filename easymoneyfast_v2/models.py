from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True)
	password = db.Column(db.String(50))
	balance = db.Column(db.Integer)
	transaction = db.relationship('Transaction', backref='user', lazy='dynamic')
	last_player = db.relationship('Game', backref='user', lazy='dynamic')

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	creation_date = db.Column(db.DateTime)
	total_amount = db.Column(db.Integer)
	actual_amount = db.Column(db.Integer)
	last_user_id = db.Column(db.ForeignKey('user.id'))
	transaction = db.relationship('Transaction', backref='game', lazy='dynamic')

class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

if __name__ == '__main__':
	db.drop_all()
	db.create_all()
	user1 = User(username='user1', password=bcrypt.generate_password_hash('123'), balance=100)
	user2 = User(username='user2', password=bcrypt.generate_password_hash('123'), balance=100)
	game1= Game(creation_date=datetime.now(), total_amount=10, actual_amount=0, last_user_id=None)
	game2= Game(creation_date=datetime.now(), total_amount=50, actual_amount=0, last_user_id=None)
	game3= Game(creation_date=datetime.now(), total_amount=100, actual_amount=0, last_user_id=None)
	game4= Game(creation_date=datetime.now(), total_amount=500, actual_amount=0, last_user_id=None)
	trans1 = Transaction(datetime=datetime.now(), user=user1, game=game1)

	db.session.add_all([user1, user2, game1, game2, game3, game4, trans1])
	db.session.commit()
