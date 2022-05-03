from flask import Flask,render_template, request
# from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
import json
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'Library'
 
mysql = MySQL(app)

@app.route('/')
def basic():
	return "Hello"

@app.route('/getBookByName/<string:name>', methods = ['GET'])
def get_Book(name: str):
	cursor = mysql.connection.cursor()
	cursor.execute("Select * from Books where book_title = %s",(name,))
	result=cursor.fetchone()
	cursor.close()
	return json.dumps(result)

@app.route('/getBooksByCategory/<string:category>', methods = ['GET'])
def get_Books(category: str):
	cursor = mysql.connection.cursor()
	cursor.execute("Select * from Books where book_category = %s",(category,))
	result=cursor.fetchall()
	cursor.close()
	return json.dumps(result)

app.run(host='localhost', port=5000)