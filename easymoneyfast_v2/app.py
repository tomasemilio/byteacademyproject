from flask import Flask, request, jsonify, redirect, session, render_template, url_for
from models import *
from flask_cors import CORS, cross_origin
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
app.secret_key = 'whatever'


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method=='POST':
		username = request.form.get('username')
		return render_template('home.html', username=username)
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

	username = request.form.get('username')
	password = request.form.get('password')

	query = User.query.filter_by(username=username) 

	if query.first():
		username_query = query.first().username
		password_query = query.first().password 

		if bcrypt.check_password_hash(password_query, password):
			# session['logged_in']=True
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

@app.route('/initinfo', methods=['POST'])
def initinfo():
	username = request.form.get('username')
	user = User.query.filter_by(username=username).first().username 
	user_balance = User.query.filter_by(username=username).first().balance
	cd10 = Game.query.filter_by(total_amount=10)[-1].creation_date
	cd50 = Game.query.filter_by(total_amount=50)[-1].creation_date
	cd100 = Game.query.filter_by(total_amount=100)[-1].creation_date
	cd500 = Game.query.filter_by(total_amount=500)[-1].creation_date

	return jsonify({'user': user, 'balance': user_balance, 'cd10': cd10, 'cd50': cd50, 'cd100': cd100, 'cd500': cd500, })



@app.route('/bid<int:bid>', methods=['POST'])
def bid(bid):
	username = request.form.get('username')
	bidamount = int(bid)/10
	game = Game.query.filter_by(total_amount=bid)[-1]
	last_player = game.last_user_id
	query = User.query.filter_by(username=username).first()

	if username == last_player:
		return jsonify({'status': 'waslast', 'balance':query.balance})

	if query.balance < bidamount:
		return jsonify({'status': 'nomoney', 'balance':query.balance})

	query.balance = query.balance - bidamount
	db.session.commit()
	new_balance = User.query.filter_by(username=username).first().balance

	game = Game.query.filter_by(total_amount=bid)[-1]
	game.actual_amount = game.actual_amount + bidamount
	game.last_user_id = username
	db.session.commit()

	if game.actual_amount == bid:
		query = User.query.filter_by(username=username).first()
		query.balance = query.balance + bid
		new_game = Game(creation_date=datetime.now(), total_amount=bid, actual_amount=0, last_user_id=None)
		db.session.add(new_game)
		new_balance = User.query.filter_by(username=username).first().balance
		db.session.commit()
		return jsonify({'user':username, 'balance':new_balance, 'status': 'done', 'lastuser': None})

	return jsonify({'user':username, 'balance':new_balance, 'status':'open', 'lastuser': game.last_user_id})



if __name__ == '__main__':
	app.run(debug=True)