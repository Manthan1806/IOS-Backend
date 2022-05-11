from flask import Flask,render_template, request, jsonify
# from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
import json
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'Library'

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# class Books(db.Model, JsonModel):
# 	bookName = db.Column()

mysql = MySQL(app)

@app.route('/')
def basic():
	return "Hello"

@app.route('/login/<string:username>/<string:password>', methods = ['GET'])
def check_User(username: str, password: str):
	cursor = mysql.connection.cursor()
	cursor.execute("Select * from Users where username = %s and password = %s",(username, password,))
	result = cursor.fetchone()
	cursor.close() 
	if result is None:
		return jsonify({'response':"Failure"})
	else:
		return jsonify({'response':"Success"})

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
	result = cursor.fetchall()
	fields = cursor.description
	column_list = []
	for i in fields:
		column_list.append(i[0])
	# print("print final column_list",column_list)
	jsonData_list = []
	for row in result:
		data_dict = {}
		for i in range(len(column_list)):
			data_dict[column_list[i]] = row[i]
		jsonData_list.append(data_dict)
	cursor.close()
	# return json.dumps(result)
	return jsonify({'books': jsonData_list})

@app.route('/getUserBooks/<string:username>', methods = ['GET'])
def get_user_books(username: str):
	cursor = mysql.connection.cursor()
	cursor.execute("Select * from UserBooks where username = %s",(username,))
	result = cursor.fetchall()
	fields = cursor.description
	column_list = []
	for i in fields:
		column_list.append(i[0])
	print("print final column_list",column_list)
	jsonData_list = []
	for row in result:
		data_dict = {}
		for i in range(len(column_list)):
			data_dict[column_list[i]] = row[i]
		jsonData_list.append(data_dict)
	cursor.close()
	# return json.dumps(result)
	return jsonify({'books': jsonData_list})

@app.route('/issueBook/<string:bookName>/<string:username>', methods = ['POST', 'GET'])
def issue_book(bookName: str, username: str):
	cursor = mysql.connection.cursor()
	cursor.execute("Select * from UserBooks where username = %s and book_name = %s",(username, bookName,))
	result = cursor.fetchone()
	cursor.close()
	if result is not None:
		return jsonify({'response':"This book has already been issued to you. Cannot issue it again!"})
	else:
		cursor = mysql.connection.cursor()
		cursor.execute("Select * from Books where book_title = %s",(bookName,))
		result = cursor.fetchone()
		if result is None:
			return jsonify({'response':"Enter valid Book Name"})
		cursor.execute("Insert into UserBooks(book_name, username) values(%s, %s)",(bookName, username,))
		cursor.execute("Update Books set book_count = book_count - 1 where book_title = %s", (bookName,))
		mysql.connection.commit()
		cursor.close()
		return jsonify({'response':"The book "+bookName+" has been successfully issued to you"})

@app.route('/returnBook/<string:bookName>/<string:username>', methods = ['POST', 'GET'])
def return_book(bookName: str, username: str):
	cursor = mysql.connection.cursor()
	cursor.execute("Select * from UserBooks where username = %s and book_name = %s",(username, bookName,))
	result = cursor.fetchone()
	cursor.close()
	if result is None:
		return jsonify({'response':"This book has not been issued to you"})
	else:
		cursor = mysql.connection.cursor()
		cursor.execute("Select * from Books where book_title = %s",(bookName,))
		result = cursor.fetchone()
		if result is None:
			return jsonify({'response':"Enter valid Book Name"})
		cursor.execute("delete from UserBooks where book_name = %s and username = %s",(bookName, username,))
		cursor.execute("Update Books set book_count = book_count + 1 where book_title = %s", (bookName,))
		mysql.connection.commit()
		cursor.close()
		return jsonify({'response':"The book "+bookName+" has been successfully returned"})

app.run(host='0.0.0.0', port=5000)