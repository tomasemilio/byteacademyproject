from flask import Flask, request, jsonify, redirect, session, render_template, url_for
from models import *
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import random, time 

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
app.secret_key = 'whatever'

def getTime(seconds):
	sec=timedelta(seconds=int(seconds))
	d=datetime(1,1,1)+sec
	answer={'days':d.day-1, 'hours':d.hour, 'minutes':d.minute, 'seconds':d.second}
	return answer

@app.route('/', methods=['GET'])
def index():
	if session.get('logged_in'):
		username = session.get('username')
		return render_template('home.html', username=username)
	else:
		return render_template('login.html')

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
			session['username']=username_query
			
			return jsonify({'status':'success'})

		return jsonify({'status':'wpass'})

	return jsonify({'status':'wusername'})

@app.route('/logout')
def logout():
    # Check if session logged in is True and turn it to false
    if session.get('logged_in'):
        session['logged_in'] = False
        session['username'] = False
    return redirect('/')

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
			session['logged_in']=True
			session['username']=username
			return jsonify({'username':'ok'})
		return jsonify({'username': 'diffpass'})

	return jsonify({'username':'taken'})


@app.route('/initinfo', methods=['POST'])
def initinfo():
	username = request.form.get('username')
	user = User.query.filter_by(username=username).first().username 
	user_balance = User.query.filter_by(username=username).first().balance
	cd10 = Game.query.filter_by(total_amount=10)[-1].creation_date
	cd50 = Game.query.filter_by(total_amount=50)[-1].creation_date
	cd100 = Game.query.filter_by(total_amount=100)[-1].creation_date
	cd500 = Game.query.filter_by(total_amount=500)[-1].creation_date

	cd10 = int(time.mktime(cd10.timetuple()))
	cd50 = int(time.mktime(cd50.timetuple()))
	cd100 = int(time.mktime(cd100.timetuple()))
	cd500 = int(time.mktime(cd500.timetuple()))

	return jsonify({'user': user, 'balance': user_balance, 'cd10': cd10, 'cd50': cd50, 'cd100': cd100, 'cd500': cd500})


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

	new_transaction = Transaction(datetime=datetime.now(), user_id=query.id, game_id=game.id)
	db.session.add(new_transaction)
	db.session.commit()

	if game.actual_amount == bid:
		query = User.query.filter_by(username=username).first()
		query.balance = query.balance + bid
		new_game = Game(creation_date=datetime.now(), total_amount=bid, actual_amount=0, last_user_id=None)
		db.session.add(new_game)
		new_balance = User.query.filter_by(username=username).first().balance
		db.session.commit()
		return jsonify({'user':username, 'balance':new_balance, 'status': 'done', 'lastuser': None, 'new_time':new_game.creation_date})

	return jsonify({'user':username, 'balance':new_balance, 'status':'open', 'lastuser': game.last_user_id})

@app.route('/roulette/<username>')
def roulette(username):
	# 10*30, 50*25, 100*20, 500*15, 1000*9, 10000*1

	prizes = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 10000]

	query=User.query.filter_by(username=username).first()
	user_id=query.id

	roulette_query=Roulette.query.filter_by(user_id=user_id)
	# print(roulette_query)

	try:
		now = datetime.now()
		then = roulette_query[-1].datetime
		interval = int((now-then).total_seconds())

		if interval > 86164:
			new_roulette=Roulette(datetime=datetime.now(), user_id=user_id)
			db.session.add(new_roulette)
			db.session.commit()
			prize = random.choice(prizes)
			query = User.query.filter_by(username=username).first()
			query.balance = query.balance + prize
			db.session.commit()
			return jsonify({'interval':interval, 'status':'ok', 'prize':prize})

		else:
			return jsonify({'interval':interval, 'status':'forbidden', 'prize':0})

	except:
		new_roulette=Roulette(datetime=datetime.now(), user_id=user_id)
		db.session.add(new_roulette)
		db.session.commit()
		prize = random.choice(prizes)
		query = User.query.filter_by(username=username).first()
		query.balance = query.balance + prize
		db.session.commit()
		return jsonify({'interval':0, 'status':'first','prize':prize})






if __name__ == '__main__':
	app.run(debug=True)