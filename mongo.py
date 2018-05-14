from flask import Flask, jsonify, request, render_template, session, redirect, url_for, Response, make_response
from flask_api import status
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import BSON, json_util, ObjectId
from jinja2 import Template
import json, base64
import hashlib, uuid, os
import sys
from bson.binary import Binary
import io
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

def connect():
	try:
		connection = MongoClient('localhost:27017')
		db = connection.mydata
		return db
	except Exception as err:
		print(err.message)


app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'
db = connect()

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['jpg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_DBNAME'] = 'mydata'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'

mongo = PyMongo(app)

def add_data():
	user_name = request.form['uname']
	pass_word = request.form['psw']
	result = db.userdata.find_one({"Username": user_name})
	#d['Username']
	#h = d.get ('Username')
	if result != None :
		return 'userexist.html'
	else:
		password_salt = os.urandom(8)
		hash = hashlib.sha512()
		hash.update(('%s%s' % (password_salt, pass_word)).encode('utf-8'))
		password_hash = hash.hexdigest()
		result = db.userdata.insert({"Username" : user_name, "Psw": password_hash, "salt" : password_salt})
		return 'usercreate.html'
	
def check_data():
	user_name = request.form['uname']
	pass_word = request.form['psw']
	result = db.userdata.find_one({"Username": user_name})
	error_page = 'error.html'
	if result == None:
		return error_page
	displaypage = 'index.html'
	result['salt']
	salt_password = result.get('salt')
	result['Psw']
	user_pass = result.get('Psw')
	result['Username']
	name = result.get('Username')
	hash = hashlib.sha512()
	hash.update(('%s%s' % (salt_password, pass_word)).encode('utf-8'))
	password = hash.hexdigest()
	if(user_name == name and password == user_pass):
		try:
			session['uname'] = request.form['uname']
			session['logged_in'] = True
			return displaypage
		except NameError:
			print("Display File name is not correct!!!")
	else:
		try:
			return error_page
		except NameError:
			print("Error File name is not correct!!!")

def get_saved_data():
    try:
        data = json.loads(request.cookies.get('character'))
    except TypeError:
           data = {}
    return data


@app.route('/', methods=['GET'])
def home(): 
	if not session.get('logged_in'): 
		data = get_saved_data()
		return render_template('front_end.html') 
	else: 
		return render_template('Displaypage.html')

@app.route('/check/', methods=['POST'])
def check_framework():
	try:
		authentication = check_data()
		response = make_response(redirect(url_for('home')))
		data = get_saved_data()
		data.update(dict(request.form.items()))
		response.set_cookie('character', json.dumps(data))
		return response, render_template(authentication)
	except Exception as e:
		print(e)

@app.route('/delete/', methods=['DELETE'])
def del_framework():
	k = del_data()
	print("Deletion done")
	return '', status.HTTP_204_NO_CONTENT


@app.route('/create/', methods=['POST'])
def add_framework():
	userdetails = add_data()
	return render_template(userdetails)

@app.route('/update_data/', methods=['POST'])
def user_data():
	user_name = session['uname']
	result = db.userdata.find_one({"Username": user_name})
	result['_id']
	user_id = result.get('_id')
	try:
		file = request.files['uploadfile']
		file_name = secure_filename(file.filename)
		APP_ROOT = os.path.abspath(os.path.dirname(file_name))
		file.save(secure_filename(file.filename))
		UPLOAD_FOLDER = os.path.join(APP_ROOT, file_name)
	except Exception as e:
		print(e)
	try:
		with open(UPLOAD_FOLDER, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
	except Exception as err:
		print(err)
	if request.form['submit'] == 'submit':
		abc = db.userdata.insert_one({"image": encoded_string, "f_id": user_id})
		return Response("Inserted")
	elif (request.form['submit'] == 'Update'):
		abc = db.userdata.update_one({"f_id": user_id}, {"$set":{"image" : encoded_string}})
		return Response("Image Updated")
	else:
		return 'Invalid input'
	

@app.route('/images/', methods=['GET'])
def retrieve_image():
	user_name = session['uname']
	result = db.userdata.find_one({"Username": user_name})
	result['_id']
	user_id = result.get('_id')
	user_details = db.userdata.find_one({"f_id": user_id})
	if(user_details is not None):
		user_details['image']
		image = user_details.get('image')
		decode = image.decode()
		img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
		return Response(img_tag)
	else:
		return "NO DATA"


@app.route('/deleteimage/')
def delete_image():
	user_name = session['uname']
	result = db.userdata.find_one({"Username": user_name})
	result['_id']
	user_id = result.get('_id')
	user_details = db.userdata.find_one({"f_id": user_id})
	if user_details != None:
		user_details['image']
		image = user_details.get('image')
		result = db.userdata.delete_one({"image" : image})
		return Response("Image Deleted")
	else:
		return Response("NO DATA IS AVAILABLE FOR DELETION")

@app.route('/logout/')
def logout():
	try:
		user_name = session['uname']
		session['logged_in'] = False
		session.pop(user_name, None)
	except Exception as e:
		print(e)
	return redirect(url_for('home')) 


if __name__=='__main__':
	app.run(debug=True)
