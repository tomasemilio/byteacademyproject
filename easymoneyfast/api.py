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






if __name__ == '__main__':
	app.run(debug=True, port=8000)