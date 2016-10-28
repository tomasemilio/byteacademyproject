from flask import Flask, request, jsonify, redirect, session
from models import *
from flask_cors import CORS, cross_origin
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
app.secret_key = 'whatever'

@app.route('/login', methods=['POST'])
def login():

	username = request.form.get('username')
	password = request.form.get('password')

	query = User.query.filter_by(username=username) 

	if query.first():
		username_query = query.first().username
		password_query = query.first().password 

		if bcrypt.check_password_hash(password_query, password):
			session['logged_in']=True
			return jsonify({'username': username_query, 'status':'success'})

		return jsonify({'status':'wpass'})

	return jsonify({'status':'wusername'})

@app.route('/register', methods=['POST'])
def register():

	username = request.form.get('username')
	password = request.form.get('password')
	password2 = request.form.get('password2')

	query = User.query.filter_by(username=username)

	if not query.first():
		if password == password2:
			new_user = User(username=username, password=bcrypt.generate_password_hash(password), balance=100)
			db.session.add(new_user)
			db.session.commit()
			return jsonify({'username':'ok'})
		return jsonify({'username': 'diffpass'})

	return jsonify({'username':'taken'})

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	return jsonify({'username':'out'})

@app.route('/balance', methods=['POST'])
def balance():
	username = request.form.get('username')
	user = User.query.filter_by(username=username).first().username 
	user_balance = User.query.filter_by(username=username).first().balance

	return jsonify({'user': user, 'balance': user_balance})

@app.route('/bid100', methods=['POST'])
def bid100():
	username = request.form.get('username')

	game = Game.query.filter_by(total_amount=100)[-1]
	last_player = game.last_user_id

	if username == last_player:
		return jsonify({'lastuser': 'forbidden'})


	query = User.query.filter_by(username=username).first()
	query.balance = query.balance - 10
	db.session.commit()
	new_balance = User.query.filter_by(username=username).first().balance

	game = Game.query.filter_by(total_amount=100)[-1]
	game.actual_amount = game.actual_amount + 10
	game.last_user_id = username
	db.session.commit()

	if game.actual_amount == 100:
		query = User.query.filter_by(username=username).first()
		query.balance = query.balance + 100
		new_game = Game(creation_date=datetime.now(), total_amount=100, actual_amount=0, last_user_id=None)
		db.session.add(new_game)
		new_balance = User.query.filter_by(username=username).first().balance
		db.session.commit()

		return jsonify({'user':username, 'balance':new_balance, 'status': 'done', 'lastuser': None})

	return jsonify({'user':username, 'balance':new_balance, 'status':'open', 'lastuser': game.last_user_id})





if __name__ == '__main__':
	app.run(debug=True, port=8000)