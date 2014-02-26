#!/usr/bin/env python

import codecs
import os
import random
import re
import string
from flask import Flask, abort, make_response, redirect, render_template, request, url_for

app = Flask(__name__)
pwd = os.path.dirname(__file__)

def random_string(length):
	return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
	paste_id = random_string(5)
	filename = os.path.join(pwd, 'pastes', paste_id)
	with codecs.open(filename, 'wb', 'utf8') as file:
		file.write(request.form['paste'])
	return redirect(url_for('view', paste_id=paste_id))

@app.route('/view/<paste_id>')
def view(paste_id):
	paste_id = re.sub(r'\W+', '', paste_id)
	filename = os.path.join(pwd, 'pastes', paste_id)
	if not os.path.exists(filename):
		abort(404)
	with codecs.open(filename, 'rb', 'utf8') as file:
		paste = file.read()
	resp = make_response(paste, 200)
	resp.headers['Content-Type'] = 'text/plain;charset=utf-8'
	return resp

if __name__ == '__main__':
	app.run()
