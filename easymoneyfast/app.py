from flask import Flask, request, jsonify, redirect, session, render_template, url_for
from flask_cors import CORS, cross_origin
from datetime import datetime


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('login.html')

@app.route('/home', methods=['GET'])
def home():
	return render_template('index.html')




if __name__ == '__main__':
	app.run(debug=True, port=5000)